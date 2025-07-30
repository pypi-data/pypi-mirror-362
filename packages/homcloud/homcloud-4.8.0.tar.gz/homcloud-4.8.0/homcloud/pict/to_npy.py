import argparse

import numpy as np

import homcloud.pict.utils as utils
from homcloud.version import __version__
from homcloud.license import add_argument_for_license


def argument_parser():
    p = argparse.ArgumentParser(description="Convert data to an .npy file")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument(
        "-T",
        "--type",
        default="text_nd",
        help="input data format " "(text2d,text_nd(default),picture2d,pictures3d,npy)",
    )
    p.add_argument("-o", "--output", required=True, help="output complex file name")
    p.add_argument("-O", "--output-type", default="float", help="output data type (float, int, bool)")
    p.add_argument("-t", "--threshold", type=float, help="threshold for boolean output")
    add_argument_for_license(p)
    p.add_argument("input", nargs="*", help="input files")
    return p


def main(args=None):
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, args.type)
    if args.output_type in ["float", "int"]:
        pict = pict.astype(args.output_type)
    elif args.output_type == "bool":
        pict = pict > args.threshold

    np.save(args.output, pict)


if __name__ == "__main__":
    main()
