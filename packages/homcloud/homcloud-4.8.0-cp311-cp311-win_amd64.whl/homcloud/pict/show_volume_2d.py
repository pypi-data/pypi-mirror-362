import argparse
import json
import os

from PIL import Image, ImageDraw
import numpy as np

from homcloud.version import __version__
from homcloud.view_index_pict import RE_PREDICATE_PAIR, OPERATORS, use_vectorized_histogram_mask
from homcloud.histogram import Histogram
from homcloud.argparse_common import parse_color
from homcloud.pdgm_format import PDGMReader


def main(args=None):
    args = args or argument_parser().parse_args()

    volume_info = load_volume_info(args.diagram, args.degree)
    nodes = [node for node in volume_info["nodes"].values() if available_node(node)]
    nodes = filter_nodes(nodes, args.filter)
    if use_vectorized_histogram_mask(args):
        nodes = filter_nodes_by_mask(nodes, args.vectorized_histogram_mask, args.histoinfo)
    image_drawer = Drawer.load_image(args.picture)
    image_drawer.setup_by_args(args)
    for node in nodes:
        image_drawer.draw_node_volume(node)
    for node in nodes:
        image_drawer.draw_node_birthdeath_pixel(node)

    if args.output:
        image_drawer.save(args.output)


def argument_parser():
    p = argparse.ArgumentParser(description="Show volume on pict2d")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    p.add_argument("-f", "--filter", action="append", default=[], help='filters (ex: "lifetime > 5.0")')
    p.add_argument("-v", "--vectorized-histogram-mask", help="0-1 vector textfile for mask")
    p.add_argument("-H", "--histoinfo", help="vectorize histogram information" " (both -V and -H are required)")
    p.add_argument("-B", "--birth", default=False, action="store_true", help="plot birth pixels")
    p.add_argument("-D", "--death", default=False, action="store_true", help="plot death pixels")
    p.add_argument("--volume", default=False, action="store_true", help="plot volume pixels")
    p.add_argument("--birth-color", type=parse_color, default=(255, 0, 0), help="birth pixel color")
    p.add_argument("--death-color", type=parse_color, default=(0, 0, 255), help="death pixel color")
    p.add_argument("--volume-color", type=parse_color, default=(255, 0, 0), help="volume pixels color")
    p.add_argument("--alpha", type=float, default=0.5, help="alpha value for volume pixels")
    p.add_argument("-S", "--marker-size", default=1, type=int, help="marker size (default: 1)")
    p.add_argument("-o", "--output", help="output filername")
    p.add_argument("picture", help="input Picture file name")
    p.add_argument("diagram", help="persistence diagram file name (.p2mt)")
    return p


def load_volume_info(pdgm_path, degree):
    assert os.path.splitext(pdgm_path)[1] == ".pdgm"
    with PDGMReader.open(pdgm_path) as reader:
        assert degree in [0, reader.metadata["dim"] - 1]
        return reader.load_simple_chunk("bitmap_phtrees", degree)


def available_node(node):
    return (node["death-time"] is not None) and (node["birth-time"] != node["death-time"])


def filter_nodes(nodes, filter_strings):
    predicates = [predicate_from_string(f) for f in filter_strings]
    return [node for node in nodes if all(pred(node) for pred in predicates)]


def predicate_from_string(string):
    m = RE_PREDICATE_PAIR.match(string)
    if not m:
        return None
    getter = {
        "birth": lambda node: node["birth-time"],
        "death": lambda node: node["death-time"],
        "lifetime": lambda node: node["death-time"] - node["birth-time"],
    }[m.group(1)]
    op = OPERATORS[m.group(2)]
    threshold = float(m.group(3))
    return lambda node: op(getter(node), threshold)


def filter_nodes_by_mask(nodes, mask_vector_path, histoinfo_path):
    print(mask_vector_path)
    vector = np.loadtxt(mask_vector_path).astype(bool)
    with open(histoinfo_path) as f:
        histoinfo = json.load(f)
    histogram = Histogram.reconstruct_from_vector(vector, histoinfo)
    return [node for node in nodes if histogram.value_at(node["birth-time"], node["death-time"])]


class Drawer(object):
    def __init__(self, image):
        self.image = image
        self.output_image = image.copy()
        self.draw = ImageDraw.Draw(self.output_image)
        self.draw_birth = self.draw_death = self.draw_volume = False
        self.birth_color = (255, 0, 0)
        self.death_color = (0, 0, 255)
        self.volume_color = (255, 0, 0)
        self.alpha = 0.5
        self.marker_size = 1

    @staticmethod
    def load_image(path):
        return Drawer(Image.open(path).convert("RGB"))

    def setup_by_args(self, args):
        self.draw_birth = args.birth
        self.draw_death = args.death
        self.draw_volume = args.volume
        self.birth_color = args.birth_color
        self.death_color = args.death_color
        self.volume_color = args.volume_color
        self.alpha = args.alpha
        self.marker_size = args.marker_size

    def draw_node_volume(self, node):
        if not self.draw_volume:
            return
        for pixel in node["volume"]:
            self.draw_volume_pixel(pixel)

    def draw_node_birthdeath_pixel(self, node):
        if self.draw_birth:
            self.draw_marker(node["birth-pixel"], self.birth_color)
        if self.draw_death:
            self.draw_marker(node["death-pixel"], self.death_color)

    def draw_marker(self, pixel, color):
        if pixel is None:
            return
        d = self.marker_size // 2
        for y in range(pixel[0] - d, pixel[0] + d + 1):
            for x in range(pixel[1] - d, pixel[1] + d + 1):
                self.draw.point((x, y), fill=color)

    def draw_volume_pixel(self, pixel):
        base_color = self.image.getpixel((pixel[1], pixel[0]))
        pixel_color = tuple(
            int(b * (1 - self.alpha) + c * self.alpha) for (b, c) in zip(base_color, self.volume_color)
        )
        self.draw.point((pixel[1], pixel[0]), fill=pixel_color)

    def save(self, path):
        self.output_image.save(path)


if __name__ == "__main__":
    main()
