import argparse
import sys

import numpy as np

from homcloud.alpha_filtration import AlphaShape
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.argparse_common import parse_bool, check_abolished_output
from homcloud.utils import load_symbols


def argument_parser():
    parser = argparse.ArgumentParser(description="Convert a point cloud to dipha's input (boundary matrix)")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("-t", "--type", default="text", help="input file format type")
    parser.add_argument("-n", "--noise", type=float, default=0.0, help="level of additive noise")
    parser.add_argument("-d", "--dimension", type=int, default=3, help="dimension of the input data")
    parser.add_argument(
        "-w", "--weighted", action="store_true", default=False, help="use an weighted alpha filtration"
    )
    parser.add_argument("--square", action="store_true", default=True)
    parser.add_argument(
        "--no-square",
        action="store_const",
        const=False,
        dest="square",
        help="no squared output, if a birth radius is negative, the output is -sqrt(abs(r))",
    )

    parser.add_argument(
        "-P",
        "--partial-filtration",
        default=False,
        action="store_true",
        help="Compute partial filtration (relative homology)",
    )
    parser.add_argument(
        "-A", "--check-acyclicity", default=False, action="store_true", help="Check acyclicity for paritial filtration"
    )
    parser.add_argument(
        "--save-suppl-info", default=True, type=parse_bool, help="save supplementary information of PD"
    )
    parser.add_argument(
        "-M",
        "--save-boundary-map",
        default=True,
        type=parse_bool,
        help="save boundary map into output file" "(only available with phat-* algorithms, *on*/off)",
    )
    parser.add_argument(
        "--save-phtrees",
        default=False,
        type=parse_bool,
        help="save phtrees into output pdgm file" "(only available with phat-* algorithms, *on*/off)",
    )
    parser.add_argument(
        "--algorithm", default=None, help="algorithm (dipha, phat-twist(default), " "phat-chunk-parallel)"
    )
    parser.add_argument("--vertex-symbols", help="vertex symbols file")
    parser.add_argument(
        "--periodicity",
        nargs=6,
        type=float,
        default=None,
        metavar=("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"),
        help="use a periodic alpha filtration",
    )
    add_argument_for_license(parser)
    parser.add_argument("input", metavar="INPUT", help="input file name")
    parser.add_argument("output", metavar="OUTPUT", help="output file name")
    return parser


def noise_array(level, dim, weighted, partial, num_points):
    noise = np.random.uniform(-level, level, (num_points, dim))
    if weighted:
        noise = np.hstack([noise, np.zeros((num_points, 1))])
    if partial:
        noise = np.hstack([noise, np.zeros((num_points, 1))])
    return noise


def parse_periodicity(p):
    return ((p[0], p[1]), (p[2], p[3]), (p[4], p[5])) if p else None


def main(args=None):
    args = args or argument_parser().parse_args()
    if args.dimension == 2 and args.weighted:
        raise RuntimeError("Weighted 2D alpha filtration is not supported now")

    check_abolished_output(args)

    points = np.loadtxt(args.input)

    if points.shape[1] != width(args):
        raise RuntimeError("Input format error")

    if args.noise > 0.0:
        points += noise_array(args.noise, args.dimension, args.weighted, args.partial_filtration, points.shape[0])

    alpha_shape = AlphaShape.build(
        points, args.dimension, args.weighted, args.partial_filtration, parse_periodicity(args.periodicity)
    )

    if args.check_acyclicity:
        alpha_shape.check_subsets_acyclicity()

    if args.partial_filtration:
        alpha_shape.become_partial_shape()

    filtration = alpha_shape.create_filtration(
        args.square, load_symbols(args.vertex_symbols), args.save_boundary_map, args.save_phtrees
    )
    filtration.compute_pdgm_and_save(args.output, args.algorithm, args.save_suppl_info)


def width(args):
    return args.dimension + (1 if args.weighted else 0) + (1 if args.partial_filtration else 0)


if __name__ == "__main__":
    sys.exit(main())
