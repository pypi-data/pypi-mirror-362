import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys

from . import histo


def argument_parser():
    p = argparse.ArgumentParser(description="Clustering pixel value histogram")
    p.add_argument("-n", default=2, type=int, help="Number of component")
    p.add_argument("-M", "--method", default="gmm", help="(kmeanss|gmm)")
    p.add_argument("-N", "--noise", metavar="SD", type=float, default=None, help="Additive gaussian noise")
    p.add_argument("-p", "--pixelvalue-range", metavar="RANGE", action=histo.RangeAction)
    p.add_argument("input", help="Input image file name")
    p.add_argument("output", nargs="?", default=None, help="Histogram output file")
    return p


def main(args):
    from .histo import load_pixels, gmm_plot, kmeans_plot, dpgmm_plot, vbgmm_plot, dbscan_plot

    pixels = load_pixels(args.input)

    if args.noise is not None:
        pixels = pixels + args.noise * np.random.randn(*pixels.shape)

    if args.pixelvalue_range:
        pixels = histo.filter_by_range(pixels, *args.pixelvalue_range)

    pixels = pixels.reshape((pixels.size, 1))

    plt.xlim(0, 280)
    plt.xlabel("Pixel value")
    plt.ylabel("Number of pixels")
    plt.hist(pixels, bins=280, range=(0, 279))

    if args.method == "gmm":
        gmm_plot(pixels, args.n)
    elif args.method == "kmeans":
        kmeans_plot(pixels, args.n)
    elif args.method == "dpgmm":
        dpgmm_plot(pixels, args.n)
    elif args.method == "vbgmm":
        vbgmm_plot(pixels, args.n)
    elif args.method == "DBSCAN":
        dbscan_plot(pixels)
    elif args.method == "nofit":
        pass
    else:
        print("Unknown method: %s" % args.method)
        sys.exit(1)

    if args.output is not None:
        plt.savefig(args.output)
    else:
        plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main(argument_parser().parse_args()))
