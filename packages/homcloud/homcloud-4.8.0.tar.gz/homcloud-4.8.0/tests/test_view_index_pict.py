# pylint: disable=C0111,W0201,R0201,C0103
import os

from homcloud import view_index_pict
from homcloud.view_index_pict import Pair

import pytest


@pytest.mark.parametrize(
    "string,birth,death,expected",
    [
        ("lifetime > 5.0", 1.0, 6.1, True),
        ("lifetime > 5.0", 1.0, 5.9, False),
        ("birth > 2.0", 2.1, 2.2, True),
        ("birth > 2.0", 2.0, 2.1, False),
        ("birth >= 2.0", 2.0, 2.1, True),
        ("death < 3.0", 2.8, 2.9, True),
        ("death < 3.0", 2.8, 3.04, False),
        ("death < -3.0", -4.0, -3.1, True),
        ("death < -3.0", -4.0, -2.9, False),
    ],
)
def test_predicate_from_string(string, birth, death, expected):
    pred = view_index_pict.predicate_from_string(string)
    assert pred(Pair(birth, death, None, None)) == expected


@pytest.mark.parametrize(
    "data,expected",
    [
        (5, False),
        (0, False),
        (4, True),
    ],
)
def test_all_true(data, expected):
    predicates = [lambda x: x > 2, lambda x: x % 2 == 0]
    assert view_index_pict.all_true(predicates, data) == expected


class Test_main(object):
    @pytest.fixture
    def png_path(self, datadir):
        return str(os.path.join(datadir, "bin.png"))

    @pytest.fixture
    def vectorized_histogram_mask_info(self, datadir):
        return (os.path.join(datadir, "bin_vect.txt"), os.path.join(datadir, "histoinfo.json"))

    @pytest.mark.integration
    def test_for_lifetime_filtering(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-f",
                    "lifetime > 3",
                    "-s",
                    "3",
                    "-B",
                    "-D",
                    "-L",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict0.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_for_birthdeath_filtering(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-s",
                    "10",
                    "-B",
                    "-L",
                    "-f",
                    "birth == -5.0",
                    "-f",
                    "death == -4.0",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict1.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_without_label(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-f",
                    "lifetime > 3",
                    "-s",
                    "3",
                    "-B",
                    "-D",
                    "-L",
                    "--no-label",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict2.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_with_vectorized_histogram_mask(
        self, png_path, path_bin_pdgm, vectorized_histogram_mask_info, picture_dir
    ):
        mask, histoinfo = vectorized_histogram_mask_info
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-v",
                    mask,
                    "-H",
                    histoinfo,
                    "-B",
                    "-D",
                    "-L",
                    "--no-label",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict3.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_with_S_option(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-f",
                    "lifetime > 3",
                    "-s",
                    "3",
                    "-B",
                    "-D",
                    "-L",
                    "--no-label",
                    "-S",
                    "4",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict4.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_with_M_option(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-f",
                    "lifetime > 3",
                    "-s",
                    "3",
                    "-B",
                    "-D",
                    "-L",
                    "--no-label",
                    "-S",
                    "4",
                    "-M",
                    "square",
                    png_path,
                    path_bin_pdgm,
                    "-o",
                    str(picture_dir.joinpath("view_index_pict5.png")),
                ]
            )
        )

    @pytest.mark.integration
    def test_with_color_options(self, png_path, path_bin_pdgm, picture_dir):
        view_index_pict.main(
            view_index_pict.argument_parser().parse_args(
                [
                    "-d",
                    "0",
                    "-f",
                    "lifetime > 3",
                    "-s",
                    "3",
                    "-B",
                    "-D",
                    "-L",
                    "--no-label",
                    "-S",
                    "4",
                    "-M",
                    "filled-square",
                    png_path,
                    path_bin_pdgm,
                    "--birth-color",
                    "#ff00ff",
                    "--death-color",
                    "#00ff00",
                    "--line-color",
                    "#801040",
                    "-o",
                    str(picture_dir.joinpath("view_index_pict6.png")),
                ]
            )
        )
