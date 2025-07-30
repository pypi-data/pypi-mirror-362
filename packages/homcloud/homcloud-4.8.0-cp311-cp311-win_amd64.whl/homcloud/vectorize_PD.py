import argparse
import json
import sys
import math

import numpy as np

from homcloud.histogram import Ruler, PDHistogram
from homcloud.version import __version__
import homcloud.pdgm as pdgm
from homcloud.argparse_common import add_arguments_for_load_diagrams, add_arguments_for_histogram_rulers


def argument_parser():
    p = argparse.ArgumentParser(description="Create a finite dim vector from PD")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    add_arguments_for_histogram_rulers(p)
    p.add_argument("-D", "--gaussian-sd", type=float, required=True, help="standard deviation of gaussian diffusion")
    p.add_argument("-C", type=float, help="weight constant C")
    p.add_argument("-p", type=float, default=1.0, help="weight constant p")
    p.add_argument("-c", "--coordinates", help="file to write coordinates")
    p.add_argument("-H", "--histogram-information", help="file to write histogram information")
    p.add_argument("-o", "--output", help="output file")
    p.add_argument("-w", "--weight-type", default="atan", help="weight type (atan(default),linear,none)")
    p.add_argument("--reorder-process", default=False, action="store_true")
    p.add_argument("input", help="input file")
    return p


def atan_weight_function(c, p):
    def func(b, d):
        return math.atan(c * abs(d - b) ** p)

    return func


def linear_weight_function(death_max):
    def func(b, d):
        return abs(d - b) / death_max

    return func


def main(args=None):
    args = args or argument_parser().parse_args()
    diagram = pdgm.load(args.input, args.type, args.degree, args.negate)
    check_args(args)

    histogram = tuned_histogram(diagram, args)

    if args.coordinates:
        np.savetxt(args.coordinates, histogram.centers_of_vectorize_bins())

    if args.histogram_information:
        save_histogram_information(args.histogram_information, histogram.histospec)

    if args.output:
        np.savetxt(args.output, histogram.vectorize())
    else:
        np.savetxt(sys.stdout.buffer, histogram.vectorize())


def check_args(args):
    if args.weight_type == "atan" and args.C is None:
        raise RuntimeError('weigth "atan" requires option -C')


def tuned_histogram(diagram, args):
    xy_rulers = Ruler.create_xy_rulers(args.x_range, args.xbins, args.y_range, args.ybins, diagram)
    histogram = PDHistogram(diagram, *xy_rulers)

    def apply_weight():
        if args.weight_type == "atan":
            histogram.apply_weight(atan_weight_function(args.C, args.p))
        elif args.weight_type == "linear":
            histogram.apply_weight(linear_weight_function(np.max(np.abs(diagram.deaths - diagram.births))))
        elif args.weight_type == "none":
            pass
        else:
            raise "Unknown weight type {}".format(args.weight_type)

    def apply_gaussian():
        histogram.apply_gaussian_filter(args.gaussian_sd)

    if args.reorder_process:
        apply_gaussian()
        apply_weight()
    else:
        apply_weight()
        apply_gaussian()

    return histogram


def save_histogram_information(path, histospec):
    with open(path, "w") as f:
        json.dump(histogram_info_dict(histospec), f)


def histogram_info_dict(histospec):
    yindices, xindices = histospec.indices_for_vectorization()
    return {
        "x-edges": histospec.xedges.tolist(),
        "y-edges": histospec.yedges.tolist(),
        "x-indices": xindices.tolist(),
        "y-indices": yindices.tolist(),
        "sign-flipped": histospec.sign_flipped,
    }


if __name__ == "__main__":
    main()
