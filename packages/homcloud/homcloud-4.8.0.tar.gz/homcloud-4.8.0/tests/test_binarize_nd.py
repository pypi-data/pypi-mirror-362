# pylint: disable=C0103,C0111,W0201,R0201
import os
import pytest

import numpy as np
import numpy.testing as npt

import homcloud.pict.binarize_nd as binarize_nd
from tests.helper import get_pdgm_type


@pytest.mark.integration
class Test_main(object):
    def test_case_text_2d(self, datadir, tmpdir):
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                [
                    "-m",
                    "black-base",
                    "-T",
                    "text2d",
                    "-o",
                    str(tmpdir.join("out.pdgm")),
                    "-t",
                    "2.5",
                    os.path.join(datadir, "bitmap.txt"),
                ]
            )
        )

    def test_case_text_3d(self, datadir, tmpdir):
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                ["-T", "text_nd", "-o", str(tmpdir.join("out.pdgm")), "-t", "0.5", os.path.join(datadir, "pict3d.txt")]
            )
        )

    def test_case_M_option(self, tmpdir, path_5x2_png):
        outpath = str(tmpdir.join("out.pdgm"))
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                [
                    "-m",
                    "black-base",
                    "-T",
                    "pictures3d",
                    "-o",
                    outpath,
                    "-C",
                    "-M",
                    "on",
                    path_5x2_png,
                    path_5x2_png,
                    path_5x2_png,
                    path_5x2_png,
                ]
            )
        )

    def test_case_with_mask(self, tmpdir, path_5x2_png, path_5x2mask_png):
        outpath = str(tmpdir.join("out.pdgm"))
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                [
                    "-m",
                    "black-base",
                    "-T",
                    "picture2d",
                    "-o",
                    outpath,
                    "--mask",
                    path_5x2mask_png,
                    path_5x2_png,
                ]
            )
        )

    def test_case_M_and_mask(self, tmpdir, path_5x2_png, path_5x2mask_png):
        outpath = str(tmpdir.join("out.pdgm"))
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                [
                    "-m",
                    "black-base",
                    "-T",
                    "picture2d",
                    "-o",
                    outpath,
                    "-C",
                    "-M",
                    "on",
                    "--mask",
                    path_5x2mask_png,
                    path_5x2_png,
                ]
            )
        )

    def test_case_pdgm(self, tmpdir, path_5x2_png):
        outpath = str(tmpdir.join("out.pdgm"))
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(
                [
                    "-o",
                    outpath,
                    "-C",
                    "-M",
                    "on",
                    "-T",
                    "picture2d",
                    path_5x2_png,
                ]
            )
        )
        assert get_pdgm_type(outpath) == "cubical"


def test_binarize_picture():
    pict = np.array([[-1.2, 2.5, 2.3, 1.2], [0.8, -2.1, 0.1, 0.2]])
    npt.assert_almost_equal(
        binarize_nd.binarize_picture(pict, 0.0, "white-base", (None, None)),
        np.array([[False, True, True, True], [True, False, True, True]]),
    )
    npt.assert_almost_equal(
        binarize_nd.binarize_picture(pict, 0.0, "black-base", (None, None)),
        np.array([[True, False, False, False], [False, True, False, False]]),
    )
    npt.assert_almost_equal(
        binarize_nd.binarize_picture(pict, 0.0, "white-base", (0.0, None)),
        np.array([[False, True, True, True], [True, False, True, True]]),
    )
    npt.assert_almost_equal(
        binarize_nd.binarize_picture(pict, 0.0, None, (None, 0.0)),
        np.array([[True, False, False, False], [False, True, False, False]]),
    )
    npt.assert_almost_equal(
        binarize_nd.binarize_picture(pict, 0.0, None, (-1.5, 1.5)),
        np.array([[True, False, False, True], [True, False, True, True]]),
    )
