# pylint: disable=C0103,C0111,W0201,R0201,R0903
import os

import pytest

import homcloud.dump_diagram as dump_diagram


@pytest.mark.integration
class Test_main(object):
    def test_case_pdgm(self, datadir):
        path = os.path.join(datadir, "tetrahedron.pdgm")
        dump_diagram.main(dump_diagram.argument_parser().parse_args(["-d", "1", "-o", os.devnull, "-S", "off", path]))

    def test_case_pdgm_S_option(self, datadir):
        path = os.path.join(datadir, "tetrahedron.pdgm")
        dump_diagram.main(dump_diagram.argument_parser().parse_args(["-d", "1", "-o", os.devnull, "-S", "on", path]))

    def test_case_pdgm_S_s_option(self, datadir):
        path = os.path.join(datadir, "tetrahedron.pdgm")
        dump_diagram.main(
            dump_diagram.argument_parser().parse_args(["-d", "1", "-o", os.devnull, "-S", "on", "-s", "on", path])
        )

    def test_case_pdgm_bitmap(self, datadir):
        path = os.path.join(datadir, "bin.pdgm")
        dump_diagram.main(dump_diagram.argument_parser().parse_args(["-d", "1", "-o", os.devnull, "-S", "on", path]))
