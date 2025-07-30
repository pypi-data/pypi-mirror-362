import argparse
import json

import msgpack

from homcloud.version import __version__
import homcloud.pict.utils as utils
from homcloud.license import add_argument_for_license
import homcloud.pict_tree as ext
from homcloud.paraview_interface import LinesDrawer
from .distance_transform import distance_transform
from .binarize_nd import binarize_picture
from homcloud.pdgm_format import PDGMWriter, PDChunk


def argument_parser():
    p = argparse.ArgumentParser(description="Compute 0th PH tree and (n-1)-th PH tree")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument(
        "-m",
        "--mode",
        required=True,
        help=("mode (white-base or black-base for binarize," + " superlevel or sublevel for levelset)"),
    )

    for_binarize = p.add_argument_group("for binarize")
    for_binarize.add_argument("-t", "--threshold", type=float, default=128)
    for_binarize.add_argument("--gt", type=float, default=None, help="lower threshold")
    for_binarize.add_argument("--lt", type=float, default=None, help="upper threshold")
    for_binarize.add_argument("-s", "--ensmall", action="store_true", default=False, help="ensmall binarized picture")
    for_binarize.add_argument(
        "--metric",
        default="manhattan",
        help="metric used to enlarge binarized image" " (manhattan(default), euclidean, etc.)",
    )
    # for_binarize.add_argument("--matrix", help="not implemnted yet")

    # arguments for input and output
    for_input_output = p.add_argument_group("for input and output")
    for_input_output.add_argument(
        "-T",
        "--type",
        default="text_nd",
        help="input data format " "(text2d, text_nd(default), picture2d, picture3d, npy)",
    )
    for_input_output.add_argument(
        "-O", "--output-type", default="pdgm", help="output file format " "(json, msgpack, pdgm(default))"
    )
    for_input_output.add_argument("-o", "--output", required=True, help="output file")
    p.add_argument("input", nargs="*", help="input files")
    return p


def main(args=None):
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, args.type)
    is_superlevel = args.mode == "superlevel"

    if args.mode in ["black-base", "white-base"]:
        binary_pict = binarize_picture(pict, args.threshold, args.mode, (args.gt, args.lt))
        bitmap = distance_transform(binary_pict, args.metric, args.ensmall)
    elif args.mode in ["sublevel", "superlevel"]:
        bitmap = pict
    else:
        raise RuntimeError("invalid mode")

    lower_mergetree, upper_mergetree = construct_mergetrees(bitmap, is_superlevel)
    dic = construct_dict(bitmap.ndim, is_superlevel, lower_mergetree, upper_mergetree)

    if args.output_type == "json":
        with open(args.output, "w") as f:
            json.dump(dic, f)
    elif args.output_type == "msgpack":
        with open(args.output, "wb") as f:
            msgpack.dump(dic, f, use_bin_type=True)
    elif args.output_type == "pdgm":
        with open(args.output, "wb") as f:
            save_pdgm(f, bitmap.ndim, is_superlevel, lower_mergetree, upper_mergetree)
    else:
        raise RuntimeError("Unknown output format: {}".format(args.output_type))


def save_pdgm(f, dim, sign_flipped, lower_mergetree, upper_mergetree):
    writer = PDGMWriter(f, "bitmap-tree", dim)
    writer.sign_flipped = sign_flipped
    writer.append_chunk(pdchunk(lower_mergetree))
    writer.append_chunk(pdchunk(upper_mergetree))
    writer.append_simple_chunk("bitmap_phtrees", merge_tree_to_dict(lower_mergetree), degree=0)
    writer.append_simple_chunk("bitmap_phtrees", merge_tree_to_dict(upper_mergetree), degree=dim - 1)
    writer.write()


def pdchunk(mt):
    return PDChunk("pd", mt.degree(), *tree_to_pd(mt))


def tree_to_pd(mergetree):
    births = []
    deaths = []
    ess_births = []
    for n in range(mergetree.num_nodes()):
        if mergetree.node_is_trivial(n):
            continue
        if mergetree.node_birth_time(n) == mergetree.node_death_time(n):
            continue
        if mergetree.node_is_essential(n):
            ess_births.append(mergetree.node_birth_time(n))
        else:
            births.append(mergetree.node_birth_time(n))
            deaths.append(mergetree.node_death_time(n))
    return births, deaths, ess_births


def merge_tree_to_dict(mt):
    return {
        "degree": mt.degree(),
        "nodes": {
            mt.node_id(n): {
                "id": mt.node_id(n),
                "birth-time": mt.node_birth_time(n),
                "death-time": mt.node_death_time(n),
                "birth-pixel": mt.node_birth_pixel(n),
                "death-pixel": mt.node_death_pixel(n),
                "volume": mt.node_volume(n),
                "parent": mt.node_parent(n),
                "children": mt.node_children(n),
            }
            for n in range(mt.num_nodes())
            if not mt.node_is_on_boundary(n)
        },
    }


def construct_mergetrees(array, is_superlevel):
    mergetree_lower = ext.MergeTree(array.astype(float), is_superlevel, True)
    mergetree_lower.compute()
    mergetree_upper = ext.MergeTree(array.astype(float), is_superlevel, False)
    mergetree_upper.compute()
    return mergetree_lower, mergetree_upper


def construct_dict(dim, sign_flipped, lower_mergetree, upper_mergetree):
    return {
        "dim": dim,
        "sign-flipped": sign_flipped,
        "lower": merge_tree_to_dict(lower_mergetree),
        "upper": merge_tree_to_dict(upper_mergetree),
    }


def prepare_drawer_for_paraview(n_colors):
    return LinesDrawer(n_colors, {"index": None, "isboundary": "1"})


def draw_volume(drawer, volume, color, index):
    processed_pixels = set()
    for pixel in map(tuple, boundary_volume(volume)):
        for adj in adjacent_pixels(pixel):
            if adj in processed_pixels:
                drawer.draw_line(pixel, adj, color, index=index)
        processed_pixels.add(pixel)


def adjacent_pixels(coord):
    coord = list(coord)
    for n in range(len(coord)):
        for s in [-1, 1]:
            coord[n] += s
            yield tuple(coord)
            coord[n] -= s


def boundary_volume(volume):
    def neighbour_pixels(coord):
        coord = list(coord)
        ret = []

        def iter(k):
            if k == len(coord):
                ret.append(tuple(coord))
                return

            for s in [-1, 1]:
                coord[k] += s
                iter(k + 1)
                coord[k] -= s

        iter(0)
        return ret

    volume_set = set(map(tuple, volume))
    result = []
    for pixel in volume:
        if not all(adj in volume_set for adj in neighbour_pixels(pixel)):
            result.append(pixel)
    return result


if __name__ == "__main__":
    main()
