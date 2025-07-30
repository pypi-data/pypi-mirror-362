import argparse
import re
from operator import attrgetter
import operator
import os
import subprocess
import json

from PIL import Image, ImageFont, ImageDraw
import numpy as np

from homcloud.version import __version__
from homcloud.histogram import Histogram
from homcloud.compat import TemporaryDirectory
from homcloud.pdgm import PDGM
from homcloud.argparse_common import parse_color


def main(args=None):
    """Main routine of this module"""
    args = args or argument_parser().parse_args()
    pd = PDGM.open(args.diagram, args.degree)
    predicates = [predicate_from_string(string) for string in args.filter]
    if use_vectorized_histogram_mask(args):
        predicates.append(histogram_mask_predicate(args))

    pairs = [pair for pair in pairs_positions(pd) if all_true(predicates, pair)]
    output_image, marker_drawer = setup_images(open_image(args.picture), args.scale, args.no_label)
    marker_drawer.setup_by_args(args)

    for pair in pairs:
        marker_drawer.draw_pair(pair)

    if args.output:
        output_image.save(args.output)
    else:
        display_picture(args.show_command, output_image)


def argument_parser():
    """Return ArgumentParser object used in this program."""
    p = argparse.ArgumentParser(description="Show birth and death cubes in a 2D picture")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    p.add_argument("-f", "--filter", action="append", default=[], help='filters (ex: "lifetime > 5.0")')
    p.add_argument("-v", "--vectorized-histogram-mask", help="0-1 vector textfile for mask")
    p.add_argument("-H", "--histoinfo", help="vectorize histogram information (both -V and -H are required)")
    p.add_argument("-B", "--birth", default=False, action="store_true", help="plot birth pixels")
    p.add_argument("-D", "--death", default=False, action="store_true", help="plot death pixels")
    p.add_argument("-L", "--line", default=False, action="store_true", help="draw line between death and birth pixels")
    p.add_argument("-s", "--scale", default=1, type=int, help="image scaling factor (1, 3, 5, ...)")
    p.add_argument(
        "-M",
        "--marker-type",
        default="filled-diamond",
        help="marker type (point, filled-diamond(default), square, filled-square, circle, filled-circle)",
    )
    p.add_argument("-S", "--marker-size", default=1, type=int, help="marker size (default: 1)")
    p.add_argument("--show-command", default="eog", help="image display command")
    p.add_argument("--no-label", default=False, action="store_true", help="birth-death labels are not drawn")
    p.add_argument("--birth-color", type=parse_color, default=(255, 0, 0), help="birth pixel color")
    p.add_argument("--death-color", type=parse_color, default=(0, 0, 255), help="death pixel color")
    p.add_argument("--line-color", type=parse_color, default=(0, 255, 0), help="birth-death line color")
    p.add_argument("-o", "--output", help="output filername")
    p.add_argument("picture", help="input Picture file name")
    p.add_argument("diagram", help="persistence diagram file name")
    return p


RE_PREDICATE_PAIR = re.compile(r"(lifetime|birth|death)\s*(>|<|>=|<=|==)\s*(-?\d+\.?\d*)")
OPERATORS = {">": operator.gt, "<": operator.lt, ">=": operator.ge, "<=": operator.le, "==": operator.eq}


def predicate_from_string(string):
    """Create a predicate from string

    Example:
    filter_from_string("lifetime > 5.0") # => lambda pair: pair.lifetime > 5.0
    """
    m = RE_PREDICATE_PAIR.match(string)
    if not m:
        return None
    attr = attrgetter(m.group(1))
    op = OPERATORS[m.group(2)]
    threshold = float(m.group(3))
    return lambda x: op(attr(x), threshold)


def use_vectorized_histogram_mask(args):
    if args.vectorized_histogram_mask and args.histoinfo:
        return True
    if (args.vectorized_histogram_mask is None) and (args.histoinfo is None):
        return False
    print("Both -v and -H options are required")
    exit(1)


def histogram_mask_predicate(args):
    vector = np.loadtxt(args.vectorized_histogram_mask, dtype=bool)
    with open(args.histoinfo) as f:
        histoinfo = json.load(f)
    histogram = Histogram.reconstruct_from_vector(vector, histoinfo)

    def predicate(pair):
        return histogram.value_at(pair.birth, pair.death)

    return predicate


def create_base_output_image(original_image, no_label):
    width, height = original_image.size
    if not no_label:
        width += 100
        height += 20

    output_image = Image.new("RGB", (width, height))
    output_image.paste(original_image, (0, 0))
    return output_image


def display_picture(command, image):
    """Display image to your display

    Args:
    command -- command name string to display image (for example, eog)
    image -- image object (PIL.Image)
    """
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "tmp.png")
        image.save(path)
        subprocess.call([command, path])


def all_true(predicates, obj):
    """Return True for all predicates returns True"""
    return all(predicate(obj) for predicate in predicates)


def open_image(path):
    """Open image file and convert it to accept colored drawings"""
    return Image.open(path).convert("RGB")


def resize_image(image, scale):
    width, height = image.size
    return image.resize((width * scale, height * scale))


def setup_images(picture, scale, no_label):
    input_image = resize_image(picture, scale)
    output_image = create_base_output_image(input_image, no_label)
    marker_drawer = MarkerDrawer(ImageDraw.Draw(output_image))
    return output_image, marker_drawer


def pairs_positions(pd):
    return (Pair(*args) for args in zip(pd.births, pd.deaths, pd.birth_positions, pd.death_positions))


class Pair(object):
    def __init__(self, birth, death, birth_pos, death_pos):
        self.birth = birth
        self.death = death
        self.birth_pos = birth_pos
        self.death_pos = death_pos

    @property
    def lifetime(self):
        return self.death - self.birth

    def display_str(self):
        return "({0}, {1}) - ({2}, {3}) ({4}, {5})".format(
            self.birth, self.death, self.birth_pos[0], self.birth_pos[1], self.death_pos[0], self.death_pos[1]
        )

    def __repr__(self):
        return "Pair({})".format(self.display_str())


class MarkerDrawer(object):
    def __init__(self, draw):
        """Marker Drawer

        Args:
        draw -- PIL.ImageDraw.Draw object
        args -- the return value of argument_parser().parse_args()
        """
        self.draw = draw
        self.font = ImageFont.load_default()
        self.scale = 1
        self.marker_type = "filled-diamond"
        self.marker_size = 1
        self.should_draw_birth_pixel = False
        self.should_draw_death_pixel = False
        self.should_draw_line = False
        self.no_label = True
        self.birth_color = (255, 0, 0)
        self.death_color = (0, 0, 255)
        self.line_color = (0, 255, 0)

    def setup_by_args(self, args):
        self.scale = args.scale
        self.marker_size = args.marker_size
        self.marker_type = args.marker_type
        self.should_draw_birth_pixel = args.birth
        self.should_draw_death_pixel = args.death
        self.should_draw_line = args.line
        self.no_label = args.no_label
        self.birth_color = args.birth_color
        self.death_color = args.death_color
        self.line_color = args.line_color
        return self

    def put_label(self, pos, pair, color):
        if self.no_label:
            return
        self.draw.text(scaling(pos, self.scale), "({}, {})".format(pair.birth, pair.death), font=self.font, fill=color)

    def put_birth_marker(self, pair):
        self.put_marker(pair.birth_pos, self.birth_color)
        self.put_label(pair.birth_pos, pair, self.birth_color)

    def put_death_marker(self, pair):
        self.put_marker(pair.death_pos, self.death_color)
        self.put_label(pair.death_pos, pair, self.death_color)

    def draw_pair(self, pair):
        if self.should_draw_line:
            self.put_line(pair)
        if self.should_draw_birth_pixel:
            self.put_birth_marker(pair)
        if self.should_draw_death_pixel:
            self.put_death_marker(pair)

    def put_line(self, pair):
        """Put a line from the birth pixel to the death pixel of the given pair.

        Put a red marker at the birth pixel.
        Put a blue marker at the death pixel.
        Put a green line between them.

        Args:
        pair -- Pair object
        """
        self.draw.line(
            [scaling(pair.birth_pos, self.scale), scaling(pair.death_pos, self.scale)], fill=self.line_color, width=1
        )
        self.put_marker(pair.birth_pos, self.birth_color)
        self.put_marker(pair.death_pos, self.death_color)

    def put_marker(self, pos, color):
        x, y = scaling(pos, self.scale)

        def bounding_box():
            return [x - self.marker_size, y - self.marker_size, x + self.marker_size, y + self.marker_size]

        def put_point():
            self.draw.point((x, y), fill=color)

        def put_filled_diamond():
            for dx in range(-self.marker_size, self.marker_size + 1):
                for dy in range(-self.marker_size, self.marker_size + 1):
                    if abs(dx) + abs(dy) > self.marker_size:
                        continue
                    self.draw.point((x + dx, y + dy), fill=color)

        def put_circle():
            self.draw.ellipse(bounding_box(), outline=color)

        def put_filled_circle():
            self.draw.ellipse(bounding_box(), outline=color, fill=color)

        def put_square():
            self.draw.rectangle(bounding_box(), outline=color)

        def put_filled_square():
            self.draw.rectangle(bounding_box(), outline=color, fill=color)

        if self.marker_type == "filled-diamond":
            put_filled_diamond()
        elif self.marker_type == "point":
            put_point()
        elif self.marker_type == "circle":
            put_circle()
        elif self.marker_type == "filled-circle":
            put_filled_circle()
        elif self.marker_type == "square":
            put_square()
        elif self.marker_type == "filled-square":
            put_filled_square()
        else:
            raise RuntimeError("Unknown marker type: {}".format(self.marker_type))


def scaling(pos, scale):
    x = pos[1] * scale + scale // 2
    y = pos[0] * scale + scale // 2
    return (x, y)


if __name__ == "__main__":
    main()
