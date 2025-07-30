import argparse
import json

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from homcloud.plot_PD import add_arguments_for_zspec, add_arguments_for_auxinfo, ZSpec, AuxPlotInfo, PDPlotter
from homcloud.version import __version__
from homcloud.histogram import Histogram


def main(args=None):
    args = args or argument_parser().parse_args()
    vector = np.loadtxt(args.input, ndmin=1)
    args.diffuse_pairs = True
    with open(args.vectorization_info) as f:
        info = json.load(f)

    zspec = ZSpec.create_from_args(args)
    histogram = Histogram.reconstruct_from_vector(vector, info)
    aux_info = AuxPlotInfo.from_args(args)
    plotter = PDPlotter.find_plotter(args.style)(histogram, zspec, aux_info)

    plotter.plot(*plt.subplots())

    if args.output:
        plt.savefig(args.output, dpi=args.dpi)
    else:
        plt.show()


def argument_parser():
    p = argparse.ArgumentParser(description="View vectorized histogram")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-o", "--output", help="output image file")
    add_arguments_for_zspec(p)
    p.add_argument("-s", "--style", default="colorhistogram", help="plotting style (colorhistogram(default), contour)")
    add_arguments_for_auxinfo(p)
    p.add_argument(
        "--dpi", type=int, default=None, help="output DPI (used with -o option, default is savefig.dpi for matplotlib)"
    )
    p.add_argument("input", help="Vector data file")
    p.add_argument("vectorization_info", help="vectorization information json data")
    return p


def draw_diagonal(ax, x_edges):
    x_range = (x_edges[0], x_edges[-1])
    ax.add_line(Line2D(x_range, x_range, linewidth=1, color="black"))


if __name__ == "__main__":
    main()
