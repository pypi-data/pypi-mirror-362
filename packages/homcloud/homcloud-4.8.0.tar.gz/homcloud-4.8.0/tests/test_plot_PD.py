# pylint: disable=C0103,C0111,W0201,R0201,R0903
import os
import io
from unittest.mock import Mock

import matplotlib.pyplot as plt
import pytest

from homcloud.histogram import Ruler, PDHistogram
from homcloud.pdgm import SimplePDGM
from homcloud import plot_PD
from homcloud.plot_PD import PDPlotter, MarkerDrawer, AuxPlotInfo, PDColorHistogramPlotter, ZSpec


class TestPDPLotter(object):
    @pytest.mark.parametrize(
        ("aux_info", "key", "expected"),
        [
            (AuxPlotInfo(None, None), "Birth", "Birth"),
            (AuxPlotInfo("", "A^2"), "Death", "Death[A^2]"),
        ],
    )
    def test_label_text(self, aux_info, key, expected):
        plotter = PDPlotter(None, ZSpec.Linear(0, 1), aux_info)
        assert plotter.label_text(key) == expected


class TestMarkerDrawer(object):
    def test_parse_line(self):
        parse_line = MarkerDrawer.parse_line
        assert parse_line("") is None
        assert parse_line("# comment") is None
        assert parse_line("  # commnent with spacee") is None
        assert parse_line("point 0.0 1 0 1 0") == ("point", (0.0, 1.0), (0.0, 1.0, 0.0))
        assert parse_line("line 0.0 1 2 3 0 1 0") == ("line", (0.0, 1.0), (2.0, 3.0), (0.0, 1.0, 0.0))
        assert parse_line("arrow 0.0 1 2 3 0 1 0") == ("arrow", (0.0, 1.0), (2.0, 3.0), (0.0, 1.0, 0.0))
        with pytest.raises(ValueError):
            parse_line("unknown 0.0 1 2 3 0 1 0")

    def test_load(self):
        f = io.StringIO(
            """
        # comment
        point 0 1 0 0 1
        line 1 2 3 4 1 0 0
        """
        )
        assert MarkerDrawer.load(f).markers == [("point", (0, 1), (0, 0, 1)), ("line", (1, 2), (3, 4), (1, 0, 0))]

    def test_draw(self):
        marker_drawer = MarkerDrawer(
            [
                ("point", (0, 1), (0, 0, 1)),
                ("arrow", (0, 1), (2, 3), (0, 1, 0)),
                ("line", (1, 2), (3, 4), (1, 0, 0)),
            ]
        )
        ax = Mock()
        marker_drawer.draw(ax)
        ax.arrow.assert_called_once_with(0, 1, 2, 2, color=(0, 1, 0), width=0.0001, length_includes_head=True)
        ax.plot.assert_called_once_with([1, 3], [2, 4], color=(1, 0, 0))
        ax.scatter.assert_called_once_with([0], [1], color=(0, 0, 1), edgecolor="black")


@pytest.mark.integration
@pytest.mark.plotting
class Test_plot(object):
    def test_case_plot(self, picture_dir):
        pd = SimplePDGM(0, [0.0, 1.0, 3.0, 4.0], [1.0, 3.0, 5.0, 5.0])

        ruler = Ruler((0, 7), 64)
        histogram = PDHistogram(pd, ruler, ruler)
        fig, ax = plt.subplots()
        PDColorHistogramPlotter(histogram, ZSpec.Linear(), AuxPlotInfo(None, None)).plot(fig, ax)
        plt.savefig(str(picture_dir.joinpath("plot_PD_plot.png")))

    def test_case_plot_with_ess(self, picture_dir):
        pd = SimplePDGM(0, [0.0, 1.0, 3.0, 4.0], [1.0, 3.0, 5.0, 5.0], [2.0])

        ruler = Ruler((0, 7), 64)
        histogram = PDHistogram(pd, ruler, ruler)
        auxplotinfo = AuxPlotInfo(None, None, plot_ess=True)
        fig, ax = plt.subplots()
        PDColorHistogramPlotter(histogram, ZSpec.Linear(), auxplotinfo).plot(fig, ax)
        plt.savefig(str(picture_dir.joinpath("plot_PD_plot_with_ess.png")))

    def test_case_plot_with_ess_flipped(self, picture_dir):
        pd = SimplePDGM(0, [0.0, 1.0, 3.0, 4.0], [1.0, 3.0, 5.0, 5.0], [2.0], True)
        ruler = Ruler((0, 7), 64)
        histogram = PDHistogram(pd, ruler, ruler)
        auxplotinfo = AuxPlotInfo(None, None, plot_ess=True)
        fig, ax = plt.subplots()
        PDColorHistogramPlotter(histogram, ZSpec.Linear(), auxplotinfo).plot(fig, ax)
        plt.savefig(str(picture_dir.joinpath("plot_PD_plot_with_ess_flipped.png")))


@pytest.mark.integration
@pytest.mark.plotting
class Test_main(object):
    def test_for_standard_diagram(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "pdgm",
                    "-l",
                    "-d",
                    "1",
                    "-t",
                    "Title",
                    "-m",
                    "10",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main1.png")),
                ]
            )
        )

    def test_with_xy_range(self, picture_dir, path_test_text_diagram):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "text",
                    "-l",
                    "-D",
                    "0.1",
                    "-t",
                    "Title",
                    "-U",
                    "un",
                    "-d",
                    "1",
                    "-x",
                    "[0:1.0]",
                    "-X",
                    "128",
                    "-y",
                    "[0.1:1.1]",
                    "-Y",
                    "64",
                    path_test_text_diagram,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main2.png")),
                ]
            )
        )

    def test_with_loglog_option(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "pdgm",
                    "--loglog",
                    "-d",
                    "1",
                    "-t",
                    "loglog test",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main3.png")),
                ]
            )
        )

    def test_using_multiple_diagrams(self, picture_dir, path_test_text_diagram, path_test_text_diagram2):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "text",
                    "-x",
                    "[-1.0:1.0]",
                    "-X",
                    "128",
                    "-d",
                    "1",
                    path_test_text_diagram,
                    path_test_text_diagram2,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main4.png")),
                ]
            )
        )

    def test_contour_plot(self, picture_dir, path_test_text_diagram):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "text",
                    "-D",
                    "0.1",
                    "-s",
                    "contour",
                    "-t",
                    "contour plot",
                    "-x",
                    "[0:1.0]",
                    "-X",
                    "256",
                    "-y",
                    "[0.1:1.1]",
                    "-d",
                    "1",
                    path_test_text_diagram,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main6.png")),
                ]
            )
        )

    def test_with_N_option(self, picture_dir, path_test_text_diagram_negative):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-T",
                    "text",
                    "-t",
                    "flip sign",
                    "-d",
                    "1",
                    "-x",
                    "[0:1.0]",
                    "-X",
                    "128",
                    "-N",
                    path_test_text_diagram_negative,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main7.png")),
                ]
            )
        )

    def test_without_options(self, picture_dir, path_test_text_diagram):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-t",
                    "automatic detection of -T, -x, -X",
                    "-d",
                    "1",
                    path_test_text_diagram,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main7.png")),
                ]
            )
        )

    def test_with_n_option(self, picture_dir, path_test_text_diagram):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-t",
                    "with normalize constant by -n",
                    "-d",
                    "1",
                    path_test_text_diagram,
                    "-n",
                    "4",
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main8.png")),
                ]
            )
        )

    def test_with_c_option(self, picture_dir, path_test_text_diagram):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-t",
                    "change colormap",
                    "-c",
                    "Greys",
                    "-D",
                    "0.1",
                    "-d",
                    "1",
                    path_test_text_diagram,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main9.png")),
                ]
            )
        )

    def test_with_M_option(self, picture_dir, datadir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-l",
                    "-d",
                    "1",
                    "-t",
                    "Put markers",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    "-M",
                    os.path.join(datadir, "markers.txt"),
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main10.png")),
                ]
            )
        )

    def test_with_font_size(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-l",
                    "-d",
                    "1",
                    "-t",
                    "Large font",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    "--font-size",
                    "18",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main11.png")),
                ]
            )
        )

    def test_with_linear_midpoint(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-d",
                    "1",
                    "-t",
                    "Midpoint",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    "--linear-midpoint",
                    "2.0",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main12.png")),
                ]
            )
        )

    def test_with_vmin_vmax(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-d",
                    "1",
                    "-t",
                    "vmin vmax",
                    "-x",
                    "0:0.1",
                    "-X",
                    "128",
                    "--vmin",
                    "-5.0",
                    "--vmax",
                    "5.0",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main13.png")),
                ]
            )
        )

    def test_with_aspect(self, picture_dir, path_test_pdgm):
        plot_PD.main(
            plot_PD.argument_parser().parse_args(
                [
                    "-d",
                    "1",
                    "-t",
                    "aspect",
                    "--aspect",
                    "equal",
                    path_test_pdgm,
                    "-o",
                    str(picture_dir.joinpath("plot_PD_main14.png")),
                ]
            )
        )
