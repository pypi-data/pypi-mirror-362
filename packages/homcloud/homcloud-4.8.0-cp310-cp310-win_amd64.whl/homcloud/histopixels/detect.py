import argparse
import json
import sys
import numpy as np
from sklearn import mixture, cluster

from . import histo


def argument_parser():
    p = argparse.ArgumentParser(description="Output fitting information with json format")
    # p.add_argument("-n", default=2, type=int, help="Number of component")
    p.add_argument("-M", "--method", default="gmm", help="(k-means|gmm)")
    p.add_argument("-N", "--noise", metavar="SD", type=float, default=None, help="Additive gaussian noise")
    p.add_argument("-p", "--pixelvalue-range", metavar="RANGE", action=histo.RangeAction)
    p.add_argument("input", help="Input image file name")
    p.add_argument("output", nargs="?", help="Output json file name")
    return p


def fit_gmm(pixels):
    gmm = mixture.GMM(n_components=2)
    gmm.fit(pixels)
    dists = histo.WeightedNormal.from_gmm(gmm)

    boundary = None
    for k in range(int(dists[0].mean), int(dists[1].mean)):
        if dists[0].density(k) < dists[1].density(k):
            boundary = k
            break

    return {
        "boundary": boundary,
        "gaussians": [
            {"mean": dists[0].mean, "sd": dists[0].sd, "weight": dists[0].weight},
            {"mean": dists[1].mean, "sd": dists[1].sd, "weight": dists[1].weight},
        ],
    }


def fit_kmeans(pixels):
    k_means = cluster.KMeans(2)
    k_means.fit(pixels)

    return 0


def main(args):
    pixels = histo.load_pixels(args.input)

    if args.noise is not None:
        pixels = pixels + args.noise * np.random.randn(*pixels.shape)

    if args.pixelvalue_range:
        pixels = histo.filter_by_range(pixels, *args.pixelvalue_range)

    pixels = pixels.reshape((pixels.size, 1))

    if args.method == "gmm":
        dic = fit_gmm(pixels)
    elif args.method == "k-means":
        dic = fit_kmeans(pixels)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(dic, f)
    else:
        json.dump(dic, sys.stdout)


if __name__ == "__main__":
    main(argument_parser().parse_args())
