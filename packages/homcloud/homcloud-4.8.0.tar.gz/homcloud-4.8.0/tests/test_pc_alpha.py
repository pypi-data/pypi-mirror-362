# pylint: disable=C0111, R0201, C0103
import os

import numpy as np
import pytest

from homcloud.pc_alpha import main, argument_parser, noise_array
from tests.helper import get_pdgm_type


def test_argument_parser():
    parser = argument_parser()
    assert "dipha" in parser.description
    args = parser.parse_args(["-t", "text", "in.txt", "out.complex"])
    assert args.type == "text"
    assert args.input == "in.txt"
    assert args.output == "out.complex"


@pytest.mark.parametrize(
    ("level,dim,weighted,partial,num_points,shape"),
    [
        (0.0001, 3, False, False, 10, (10, 3)),
        (0.0001, 3, True, False, 10, (10, 4)),
        (0.0001, 3, False, True, 10, (10, 4)),
        (0.0001, 3, True, True, 10, (10, 5)),
    ],
)
def test_noisy_array(level, dim, weighted, partial, num_points, shape):
    ary = noise_array(level, dim, weighted, partial, num_points)
    assert ary.shape == shape
    assert not np.allclose(ary, np.zeros(shape), atol=0.000000001)
    assert np.allclose(ary, np.zeros(shape), atol=0.01)
    assert np.all(ary[:, 3:] == 0.0)


@pytest.mark.integration
class Test_main:
    @pytest.fixture
    def idiagrampath(self, tmpdir):
        return str(tmpdir.join("output.idiagram"))

    @pytest.fixture
    def pdgmpath(self, tmpdir):
        return str(tmpdir.join("output.pdgm"))

    @pytest.fixture
    def tetrahedron_path(self, datadir):
        return os.path.join(datadir, "tetrahedron.txt")

    def test_case_basic(self, tetrahedron_path, pdgmpath):
        main(argument_parser().parse_args(["-d", "3", tetrahedron_path, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"

    def test_case_2d_data(self, datadir, pdgmpath):
        infile = os.path.join(datadir, "tetragon.txt")
        main(argument_parser().parse_args(["-d", "2", infile, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"

    def test_case_2d_data_without_suppl_info(self, datadir, pdgmpath):
        infile = os.path.join(datadir, "tetragon.txt")
        main(argument_parser().parse_args(["-d", "2", "--save-suppl-info", "no", infile, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"

    def test_case_w_option_without_weight(self, tetrahedron_path, pdgmpath):
        with pytest.raises(RuntimeError):
            main(argument_parser().parse_args(["-d", "3", "-w", tetrahedron_path, pdgmpath]))

    def test_for_input_with_weights(self, datadir, pdgmpath):
        infile = os.path.join(datadir, "tetrahedron-with-weight.txt")
        main(argument_parser().parse_args(["-d", "3", "-w", infile, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"

    def test_for_input_with_weights_and_noise(self, datadir, pdgmpath):
        infile = os.path.join(datadir, "tetrahedron-with-weight.txt")
        main(argument_parser().parse_args(["-d", "3", "-w", "-n", "0.000001", infile, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"

    def test_for_2d_weighted_input(self, tetrahedron_path, pdgmpath):
        with pytest.raises(RuntimeError):
            main(argument_parser().parse_args(["-d", "2", "-w", tetrahedron_path, pdgmpath]))

    @pytest.fixture
    def tetragon_with_groupname_path(self, datadir):
        return os.path.join(datadir, "tetragon-with-group.txt")

    def test_for_P_option(self, tetragon_with_groupname_path, pdgmpath):
        main(argument_parser().parse_args(["-d", "2", "-P", "-A", tetragon_with_groupname_path, pdgmpath]))
        assert get_pdgm_type(pdgmpath) == "alpha"
