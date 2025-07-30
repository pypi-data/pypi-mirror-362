# pylint: disable=R0903
import argparse
import sys
import copy
import re

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

import homcloud.pdgm as pdgm
from homcloud.histogram import PDHistogram, Ruler
from homcloud.norms_for_matplotlib import LogNorm, LogPlusOneNorm, LogLogNorm, MidpointNormalize
from homcloud.version import __version__
from homcloud.argparse_common import add_arguments_for_load_diagrams, add_arguments_for_histogram_rulers


def main(args=None):
    """The main routine"""
    args = args or argument_parser().parse_args()
    pd = pdgm.load_merged_diagrams(args.input, args.type, args.degree)
    xy_rulers = Ruler.create_xy_rulers(args.x_range, args.xbins, args.y_range, args.ybins, pd)
    histogram = PDHistogram(pd, *xy_rulers)
    histogram.multiply_histogram(1.0 / args.normalize_constant)
    if args.diffuse_pairs:
        histogram.apply_gaussian_filter(args.diffuse_pairs)
    zspec = ZSpec.create_from_args(args)
    if args.title is None:
        args.title = args.input[0]
    aux_info = AuxPlotInfo.from_args(args)
    plotter = PDPlotter.find_plotter(args.style)(histogram, zspec, aux_info)

    fig, ax = plt.subplots()
    plotter.plot(fig, ax)

    if args.marker:
        MarkerDrawer.load_from_file(args.marker).draw(ax)

    if args.tight_layout or aux_info.require_tight_layout():
        plt.tight_layout()

    if args.output:
        plt.savefig(args.output, dpi=args.dpi)
    else:
        plt.show()

    plt.close(fig)


POWER_NORM_IS_AVAILABLE = hasattr(colors, "PowerNorm")


def argument_parser():
    parser = argparse.ArgumentParser(description="Plot an output by dipha")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(parser)
    add_arguments_for_zspec(parser)
    parser.add_argument(
        "-s", "--style", default="colorhistogram", help="plotting style (colorhistogram(default), contour)"
    )
    add_arguments_for_auxinfo(parser)
    parser.add_argument(
        "-D",
        "--diffuse-pairs",
        metavar="SCATTERING_SIZE",
        type=float,
        default=None,
        help="Diffuse pairs using gaussian distribution of SD=SIGMA",
    )
    parser.add_argument("-o", "--output", help="output file")
    add_arguments_for_histogram_rulers(parser)
    parser.add_argument(
        "-n", "--normalize-constant", type=float, default=1.0, help="normalize constant to histogram height"
    )
    parser.add_argument("-M", "--marker", help="marker file")
    parser.add_argument(
        "--dpi", type=int, default=None, help="output DPI (used with -o option, default is savefig.dpi for matplotlib)"
    )
    parser.add_argument(
        "--tight-layout", action="store_true", default=False, help="use tight layout (adjusting layout)"
    )
    parser.add_argument("input", metavar="INPUT", nargs="+", help="Input file path")
    return parser


def add_arguments_for_zspec(parser):
    if POWER_NORM_IS_AVAILABLE:
        parser.add_argument(
            "-p", "--power", metavar="POWER", type=float, default=None, help="Output x^POWER for each value x"
        )
    parser.add_argument("-l", "--log", action="store_true", default=False, help="Output log(x+1) for each value x")
    parser.add_argument("--loglog", action="store_true", default=False, help="Output log(log(x+1)+1)")
    parser.add_argument("--linear-midpoint", type=float, help="linear with midpoint")
    parser.add_argument(
        "-m", "--vmax", metavar="MAX", type=float, default=None, help="Maximum of colorbar (default: autoscale)"
    )
    parser.add_argument("--vmin", type=float, default=None, help="Minimum of colorbar")
    parser.add_argument("-c", "--colormap", default=None, help="matplotlib colormap name")


def add_arguments_for_auxinfo(parser):
    parser.add_argument("-t", "--title", help="title string")
    parser.add_argument("-U", "--unit-name", help="The unit name of birth and death times")
    parser.add_argument("--font-size", help="font size (default: 12)")
    parser.add_argument("--aspect", default="auto", help="histogram aspect (default: auto)")
    parser.add_argument(
        "--plot-essential", action="store_true", help="whether to plot essential values (default: False)"
    )


class AuxPlotInfo(object):
    def __init__(self, title, unit_name, font_size=None, aspect="auto", plot_ess=False):
        self.title = title
        self.unit_name = unit_name
        self.font_size = font_size
        self.aspect = aspect
        self.plot_ess = plot_ess

    @staticmethod
    def from_args(args):
        return AuxPlotInfo(args.title, args.unit_name, args.font_size, args.aspect, args.plot_essential)

    def require_tight_layout(self):
        return self.font_size is not None


class PDPlotter(object):
    """Persistence diagram plotter"""

    def __init__(self, histogram, zspec, aux_info):
        self.histogram = histogram
        self.zspec = zspec
        self.aux_info = aux_info
        self.qmesh = None
        self.qmesh_ess = None
        self.set_colorbar_range()

    def plot(self, fig, ax):
        """Plot the diagram to (fix, ax).

        Args:
        fig -- matplotlib.figures.Figure
        ax -- matplotlib.figure.Axes object related to fig
        """
        self.set_plot_range(ax)
        self.draw_labels(ax)
        self.set_title(ax)
        self.draw_diagonal(ax)
        self.set_tick_font_size(ax)
        self.plot_main_box(ax)
        self.draw_grid(ax)
        self.set_aspect(ax)
        self.divider(fig, ax)

    def set_colorbar_range(self):
        if self.zspec.vmax is None:
            self.zspec.vmax = self.histogram.maxvalue()

    def set_plot_range(self, ax):
        ax.set_xlim(*self.histogram.x_range())
        ax.set_ylim(*self.histogram.y_range())

    def draw_labels(self, ax):
        ax.set_xlabel(self.label_text("Birth"), fontsize=self.aux_info.font_size)
        ax.set_ylabel(self.label_text("Death"), fontsize=self.aux_info.font_size)

    def set_title(self, ax):
        if not self.aux_info.plot_ess:
            ax.set_title(self.aux_info.title, fontsize=self.aux_info.font_size)

    def label_text(self, key):
        """Format label text and return the text."""
        if self.aux_info.unit_name is None:
            return key
        else:
            return "{}[{}]".format(key, self.aux_info.unit_name)

    def draw_diagonal(self, ax):
        x_range = self.histogram.x_range()
        ax.add_line(Line2D(x_range, x_range, linewidth=1, color="black"))

    def set_tick_font_size(self, ax):
        ax.tick_params(labelsize=self.aux_info.font_size)

    def set_aspect(self, ax):
        if self.aux_info.aspect in ["auto", "equal"]:
            ax.set_aspect(self.aux_info.aspect)

    def divider(self, fig, ax):
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        colorbar = fig.colorbar(self.qmesh, cax=cax)
        colorbar.ax.tick_params(labelsize=self.aux_info.font_size)
        colorbar.set_label("Value")

        if self.aux_info.plot_ess:
            if self.histogram.sign_flipped:
                ax_ess = divider.append_axes("bottom", "5%", pad=0)
                ax.tick_params(bottom=False, labelbottom=False)
                ax_ess.set_ylabel(self.label_text("-∞"), fontsize=self.aux_info.font_size)
                ax_ess.set_xlabel(self.label_text("Birth"), fontsize=self.aux_info.font_size)
                ax.set_title(self.aux_info.title, fontsize=self.aux_info.font_size)
            else:
                ax_ess = divider.append_axes("top", "5%", pad=0)
                ax_ess.set_ylabel(self.label_text("∞"), fontsize=self.aux_info.font_size)
                ax_ess.set_title(self.aux_info.title, fontsize=self.aux_info.font_size)

            ax_ess.set_xlim(*self.histogram.x_range())
            ax_ess.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
            ax_ess.axhline(y=1.5, c="k", lw="0.3")

            ess_yedges = np.linspace(0.0, 3.0, num=4)
            zeros = np.zeros((3, self.histogram.x_bins()))
            zeros[1] = self.histogram.ess_values
            self.histogram.ess_values_as_float = zeros.astype(float)
            self.qmesh_ess = ax_ess.pcolormesh(
                self.histogram.xedges,
                ess_yedges,
                self.histogram.ess_values_as_float,
                norm=self.zspec.norm(),
                cmap=self.zspec.colormap(),
            )

            ax_ess.grid(axis="x")

    @staticmethod
    def find_plotter(style):
        """Return appropriate plotter class from *style* argument."""
        if style == "colorhistogram":
            return PDColorHistogramPlotter
        elif style == "contour":
            return PDContourPlotter
        else:
            raise ValueError("Unknown plot style: %s" % style)

    @staticmethod
    def draw_grid(ax):
        ax.grid()


class PDColorHistogramPlotter(PDPlotter):
    def plot_main_box(self, ax):
        self.qmesh = ax.pcolormesh(
            self.histogram.xedges,
            self.histogram.yedges,
            self.histogram.values_as_float,
            norm=self.zspec.norm(),
            cmap=self.zspec.colormap(),
        )


class PDContourPlotter(PDPlotter):
    def __init__(self, histogram, zspec, aux_info, levels=None):
        super().__init__(histogram, zspec, aux_info)
        self.levels = levels

    def plot_main_box(self, ax):
        self.qmesh = ax.contour(
            self.histogram.values_as_float,
            norm=self.zspec.norm(),
            cmap=cm.rainbow,
            extent=self.histogram.xy_extent(),
            levels=self.contour_levels(),
        )

    def contour_levels(self):
        """
        Return list of levels (floats) for matplotlib.axis.Axes.contour.
        The levels is appropriately computed by zspec.
        """
        if self.levels is not None:
            return self.levels
        norm = self.zspec.norm()
        norm.autoscale_None(self.histogram.values_as_float)
        return norm.inverse(np.linspace(0.01, 1.0, 6))


class ZSpec(object):
    """
    Classes under ZSpec hold the information about the visualization of
    z-axis (the number of points in each bin) of the histogram.
    """

    @staticmethod
    def create_from_args(args):
        """Create a zspec object selected by args."""
        colormap = plt.get_cmap(args.colormap) if args.colormap else None
        if args.power:
            return ZSpec.Power(args.power, args.vmax, args.vmin, colormap)
        if args.log and args.diffuse_pairs:
            return ZSpec.LogWithDiffusion(args.vmax, args.vmin, colormap)
        if args.log:
            return ZSpec.Log(args.vmax, args.vmin, colormap)
        if args.loglog:
            return ZSpec.LogLog(args.vmax, args.vmin, colormap)
        if args.linear_midpoint is not None:
            return ZSpec.LinearMidPoint(args.linear_midpoint, args.vmax, args.vmin, colormap)
        return ZSpec.Linear(args.vmax, args.vmin, colormap)

    class Base(object):
        def __init__(self, vmax=None, vmin=None, colormap=None):
            self.vmin = vmin
            self.vmax = vmax
            self.cmap = colormap

        @staticmethod
        def default_colormap():
            return cm.OrRd

        def colormap(self):
            return self.cmap or self.default_colormap()

    class Log(Base):
        def norm(self):
            return LogNorm(vmax=self.vmax, vmin=self.vmin)

        @staticmethod
        def default_colormap():
            cmap = copy.copy(cm.rainbow)
            cmap.set_under("white")
            return cmap

    class Power(Base):
        def __init__(self, power, vmax=None, vmin=None, colormap=None):
            self.power = power
            super().__init__(vmax, vmin, colormap)

        def norm(self):
            return colors.PowerNorm(self.power, vmax=self.vmax, vmin=self.vmin)

    class LogWithDiffusion(Base):
        def norm(self):
            return LogPlusOneNorm(vmax=self.vmax, vmin=self.vmin)

    class LogLog(Base):
        def norm(self):
            return LogLogNorm(vmax=self.vmax, vmin=self.vmin)

    class Linear(Base):
        def norm(self):
            return colors.Normalize(vmax=self.vmax, vmin=self.vmin)

    class LinearMidPoint(Base):
        def __init__(self, midpoint, vmax=None, vmin=None, colormap=None):
            self.midpoint = midpoint
            super().__init__(vmax, vmin, colormap)

        def norm(self):
            return MidpointNormalize(vmax=self.vmax, vmin=self.vmin, midpoint=self.midpoint)

        @staticmethod
        def default_colormap():
            return cm.RdBu_r


def put_markers(markers):
    plt.scatter(markers[:, 0], markers[:, 1], c=markers[:, 2:5])


class MarkerDrawer(object):
    def __init__(self, markers):
        self.markers = markers

    @staticmethod
    def load(f):
        markers = list()
        for line in f:
            marker = MarkerDrawer.parse_line(line)
            if marker:
                markers.append(marker)

        return MarkerDrawer(markers)

    @staticmethod
    def load_from_file(path):
        with open(path) as f:
            return MarkerDrawer.load(f)

    @staticmethod
    def parse_line(line):
        line = line.strip()
        if line == "":
            return None
        if line.startswith("#"):
            return None
        data = re.split(r"\s+", line)
        if data[0] == "point":
            return ("point", (float(data[1]), float(data[2])), (float(data[3]), float(data[4]), float(data[5])))
        if data[0] in ["line", "arrow"]:
            return (
                data[0],
                (float(data[1]), float(data[2])),
                (float(data[3]), float(data[4])),
                (float(data[5]), float(data[6]), float(data[7])),
            )
        raise ValueError("cannot parse {}".format(line))

    def draw(self, ax):
        for marker in self.markers:
            if marker[0] == "arrow":
                (_, (x, y), (xdx, ydy), color) = marker
                ax.arrow(x, y, xdx - x, ydy - y, color=color, width=0.0001, length_includes_head=True)
            elif marker[0] == "line":
                (_, (x1, y1), (x2, y2), color) = marker
                ax.plot([x1, x2], [y1, y2], color=color)
            elif marker[0] == "point":
                (_, (x, y), color) = marker
                ax.scatter([x], [y], color=color, edgecolor="black")


if __name__ == "__main__":
    sys.exit(main())
