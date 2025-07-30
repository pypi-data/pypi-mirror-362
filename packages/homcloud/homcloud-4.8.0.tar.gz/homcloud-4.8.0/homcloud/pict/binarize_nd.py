import argparse
import sys

import numpy as np

import homcloud.pict.utils as utils
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.argparse_common import (
    parse_cubical_periodic_flags,
    parse_bool,
    check_abolished_output,
    check_cubical_option,
)
from homcloud.bitmap import Bitmap
from .distance_transform import distance_transform


def argument_parser():
    """Return ArgumentParser object to parse command line arguments"""
    p = argparse.ArgumentParser()
    p.description = "Create N-dimensional erosion-dilation filtration "
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument(
        "-T", "--type", default="text_nd", help="input data format (text2d,text_nd(default),picture2d,pictures3d,npy)"
    )
    add_argument_for_binarize_threshold(p)
    p.add_argument("-o", "--output", required=True, help="output complex file name")
    p.add_argument("-s", "--ensmall", action="store_true", default=False, help="ensmall binarized picture")
    p.add_argument(
        "--metric",
        default="manhattan",
        help="metric used to enlarge binarized image " "(manhattan(default), euclidean, etc.)",
    )
    p.add_argument(
        "-C", "--cubical", default=False, action="store_true", help="use explicit cubical filtration (slow)"
    )
    p.add_argument(
        "-p",
        "--periodic",
        default=None,
        type=parse_cubical_periodic_flags,
        help="periodic (example: 0,1,1 for y and z are periodic)",
    )
    p.add_argument("--mask", help="mask bitmap")
    p.add_argument("--algorithm", default=None, help="algorithm (dipha, phat-twist, phat-chunk-parallel)")
    p.add_argument(
        "-M",
        "--save-boundary-map",
        default=False,
        type=parse_bool,
        help="save boundary map into idiagram file" "(only available with phat-* algorithms, on/*off*)",
    )
    add_argument_for_license(p)
    p.add_argument("input", nargs="*", help="input files")
    return p


def add_argument_for_binarize_threshold(p):
    p.add_argument(
        "-m",
        "--mode",
        default="black-base",
        help="the way to construct dipha complex (black-base|white-base, " + "default is black-base)",
    )
    p.add_argument("-t", "--threshold", type=float, default=128, help="threshold for binarization (default: 128)")
    p.add_argument("--gt", type=float, default=None, help="lower threshold")
    p.add_argument("--lt", type=float, default=None, help="upper threshold")


def main(args=None):
    args = args or argument_parser().parse_args()
    check_abolished_output(args)
    check_cubical_option(args)

    pict = utils.load_nd_picture(args.input, args.type)
    binary_pict = binarize_picture(pict, args.threshold, args.mode, (args.gt, args.lt))

    mask = load_mask(args.mask, args.type)
    distance_map = distance_transform(binary_pict, args.metric, args.ensmall, obstacle=mask)
    bitmap = Bitmap(distance_map, False, args.periodic, args.save_boundary_map)
    if args.cubical:
        filt = bitmap.build_cubical_filtration()
    else:
        filt = bitmap.build_bitmap_filtration()

    filt.compute_pdgm_and_save(args.output, args.algorithm)

    return 0


def load_mask(path, type):
    if path:
        return utils.load_nd_picture([path], type) > 0
    else:
        return None


def binarize_picture(pict, threshold, mode, bounds):
    """Binarize pict using threshold.

    Args:
    pict -- a gray-scale picture (ndarray)
    threshold -- threshold for binarization
    mode -- "black-base" or "white-base"
    bounds -- a pair of lower and upper bounds
        if both of them are None, the pair of threshold and mode is used
    """
    lower_bound, upper_bound = bounds

    if lower_bound is None and upper_bound is None:
        if mode == "black-base":
            upper_bound = threshold
        elif mode == "white-base":
            lower_bound = threshold
        else:
            raise RuntimeError("Unknown mode {0}".format(mode))

    lower_bound = -float("inf") if lower_bound is None else lower_bound
    upper_bound = float("inf") if upper_bound is None else upper_bound
    return (lower_bound <= pict) & (pict <= upper_bound)


def mahalanobis_vi(weight, angle):
    def rotation_matrix(t):
        from math import cos, sin

        return np.array([[cos(t), sin(t)], [-sin(t), cos(t)]])

    return rotation_matrix(angle) @ np.diag([weight, 1 / weight]) @ rotation_matrix(-angle)


if __name__ == "__main__":
    sys.exit(main())
