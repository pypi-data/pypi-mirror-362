# pylint: disable=C0111,W0201,R0201,R0903
import json
import math

import pytest

import homcloud.vectorize_PD as vPD
from homcloud.histogram import Ruler, PDHistogram
import homcloud.pdgm as pdgm


def test_save_histogram_information(tmpdir):
    diagram = pdgm.empty_pd()
    xy_rulers = Ruler.create_xy_rulers((0, 10), 5, (5, 11), 3, diagram)
    histogram = PDHistogram(diagram, *xy_rulers)
    path = str(tmpdir.join("tmp.json"))
    vPD.save_histogram_information(path, histogram.histospec)
    with open(path) as f:
        info = json.load(f)

    expected = {
        "x-edges": list(range(0, 10 + 1, 2)),
        "y-edges": list(range(5, 11 + 1, 2)),
        "x-indices": [0, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
        "y-indices": [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        "sign-flipped": False,
    }
    assert info == expected


@pytest.mark.parametrize(
    "sign_flipped, expected_x_indices, expected_y_indices",
    [
        (False, [0, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4], [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]),
        (True, [2, 3, 4, 3, 4, 4], [0, 0, 0, 1, 1, 2]),
    ],
)
def test_histogram_info_dict(sign_flipped, expected_x_indices, expected_y_indices):
    diagram = pdgm.empty_pd(sign_flipped=sign_flipped)
    xy_rulers = Ruler.create_xy_rulers((0, 10), 5, (5, 11), 3, diagram)
    histogram = PDHistogram(diagram, *xy_rulers)
    assert vPD.histogram_info_dict(histogram.histospec) == {
        "x-edges": list(range(0, 10 + 1, 2)),
        "y-edges": list(range(5, 11 + 1, 2)),
        "x-indices": expected_x_indices,
        "y-indices": expected_y_indices,
        "sign-flipped": sign_flipped,
    }


@pytest.mark.parametrize(
    "death_max, birth, death, expected",
    [
        (4.0, 5.0, 9.0, 1.0),
        (4.0, 5.0, 7.0, 0.5),
        (4.0, 9.0, 5.0, 1.0),
        (4.0, 7.0, 5.0, 0.5),
    ],
)
def test_linear_weight_function(death_max, birth, death, expected):
    f = vPD.linear_weight_function(death_max)
    assert f(birth, death) == pytest.approx(expected)


@pytest.mark.parametrize(
    "c, p, birth, death, expected",
    [
        (1, 2, 2.0, 4.0, math.atan(4)),
        (1, 2, 4.0, 2.0, math.atan(4)),
    ],
)
def test_atan_weight_function(c, p, birth, death, expected):
    assert vPD.atan_weight_function(c, p)(birth, death) == pytest.approx(expected)


@pytest.mark.integration
def test_main(path_test_text_diagram, tmpdir):
    vPD.main(
        vPD.argument_parser().parse_args(
            [
                "-d",
                "1",
                "-T",
                "text",
                "-x",
                "0:1",
                "-X",
                "10",
                "-D",
                "0",
                "-C",
                "2.0",
                "-p",
                "4.0",
                "-H",
                str(tmpdir.join("conf.json")),
                path_test_text_diagram,
            ]
        )
    )

    vPD.main(
        vPD.argument_parser().parse_args(
            [
                "-d",
                "1",
                "-T",
                "text",
                "-x",
                "0:1",
                "-X",
                "10",
                "-D",
                "0",
                "-w",
                "linear",
                "-H",
                str(tmpdir.join("conf.json")),
                path_test_text_diagram,
            ]
        )
    )

    vPD.main(
        vPD.argument_parser().parse_args(
            [
                "-d",
                "1",
                "-T",
                "text",
                "-x",
                "0:1",
                "-X",
                "10",
                "-D",
                "0.2",
                "-w",
                "none",
                "-H",
                str(tmpdir.join("conf.json")),
                path_test_text_diagram,
            ]
        )
    )
