import os

import pytest

import homcloud.pict.pixel_levelset_nd as pixel_levelset_nd
from tests.helper import get_pdgm_type


@pytest.mark.integration
class Test_main(object):
    def test_for_npy_input(self, tmpdir, datadir):
        inpath = os.path.join(datadir, "test.npy")
        outpath = str(tmpdir.join("out.pdgm"))
        pixel_levelset_nd.main(pixel_levelset_nd.argument_parser().parse_args(["-o", outpath, "-T", "npy", inpath]))
        assert get_pdgm_type(outpath) == "bitmap"

    def test_for_M_option(self, tmpdir, datadir):
        inpath = os.path.join(datadir, "test.npy")
        outpath = str(tmpdir.join("out.pdgm"))
        pixel_levelset_nd.main(
            pixel_levelset_nd.argument_parser().parse_args(
                [
                    "-o",
                    outpath,
                    "-T",
                    "npy",
                    inpath,
                    "-C",
                    "-M",
                    "on",
                ]
            )
        )
        assert get_pdgm_type(outpath) == "cubical"
