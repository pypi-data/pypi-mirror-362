import sys
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt

from homcloud.argparse_common import add_arguments_for_load_diagrams
from homcloud.version import __version__
import homcloud.pdgm as pdgm


def main(args=None):
    args = args or argument_parser().parse_args()
    pd = pdgm.load_merged_diagrams(args.input, args.type, args.degree)
    transl, mat = transform_to_x_axis(np.array([args.birth1, args.death1]), np.array([args.birth2, args.death2]))
    xy = np.dot(mat, np.array([pd.births, pd.deaths]) - transl.reshape(2, 1))
    mask = (xy[0, :] >= 0) & (xy[0, :] <= 1) & (np.abs(xy[1, :]) < args.width / 2)
    histo_input = xy[0, mask]
    (hist, *_) = plt.hist(histo_input, bins=args.bins, range=(0, 1), log=args.log)
    plt.xlim(0, 1)
    plt.xticks([0, 1])
    ax = plt.gca()
    ax.set_xticklabels(
        [
            construct_label(args.left_label, args.birth1, args.death1),
            construct_label(args.right_label, args.birth2, args.death2),
        ]
    )
    if args.title is not None:
        ax.set_title(args.title)
    if args.output:
        if args.text_output:
            np.savetxt(args.output, hist, fmt="%d")
        else:
            plt.savefig(args.output, dpi=args.dpi)
    else:
        plt.show()


def argument_parser():
    p = ArgumentParser(description="")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    p.add_argument("-l", "--left-label", help="label for starting point")
    p.add_argument("-r", "--right-label", help="label for end point")
    p.add_argument("-b", "--bins", type=int, default=100, help="number of bins")
    p.add_argument("--log", default=False, action="store_true", help="log scale")
    p.add_argument("-o", "--output", help="output file path")
    p.add_argument("--text-output", action="store_true", default=False, help="output histgram data into a text file")
    p.add_argument("-t", "--title", help="title")
    p.add_argument("--dpi", type=int, help="output dpi")
    p.add_argument("birth1", type=float, help="birth of starting point")
    p.add_argument("death1", type=float, help="death of starting point")
    p.add_argument("birth2", type=float, help="birth of end point")
    p.add_argument("death2", type=float, help="death of end point")
    p.add_argument("width", type=float, help="width for histogram")
    p.add_argument("input", nargs="+", help="input file path")
    return p


def transform_to_x_axis(v1, v2):
    d = v2 - v1
    norm = np.linalg.norm(d)
    rotation = np.array([[d[0], d[1]], [-d[1], d[0]]]) / norm
    scale_x = np.array(([1 / norm, 0], [0, 1]))
    return v1, np.dot(scale_x, rotation)


def construct_label(labelstr, birth, death):
    if labelstr is None:
        return "({:4f},{:4f})".format(birth, death)
    else:
        return labelstr


if __name__ == "__main__":
    sys.exit(main())
