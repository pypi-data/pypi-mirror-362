import os

import pytest

from homcloud.modp_reduction_ext import ModpMatrix
import homcloud.modp_reduction as modp_reduction


class TestModpMatrix(object):
    @pytest.mark.parametrize(
        "p, expected",
        [
            (2, [(0, 0, None), (0, 1, 2), (1, 3, 5), (1, 4, None)]),
            (3, [(0, 0, None), (0, 1, 2), (1, 3, None), (1, 4, 5)]),
        ],
    )
    def test_birth_death_pairs(self, p, expected):
        # Mobius ring
        #     2
        # (0) - (1)
        #  |4   |
        #  |  5 |4
        # (1) - (0)
        #     3
        matrix = ModpMatrix(p, [2, 3, 1])
        matrix.add_cell(0)  # 0
        matrix.add_cell(0)  # 1
        matrix.add_cell(1)  # 2
        matrix.add_boundary_coef(2, 0, -1)
        matrix.add_boundary_coef(2, 1, 1)
        matrix.add_cell(1)  # 3
        matrix.add_boundary_coef(3, 0, -1)
        matrix.add_boundary_coef(3, 1, 1)
        matrix.add_cell(1)  # 4
        matrix.add_boundary_coef(4, 0, -1)
        matrix.add_boundary_coef(4, 1, 1)
        matrix.add_cell(2)  # 5
        matrix.add_boundary_coef(5, 2, 1)
        matrix.add_boundary_coef(5, 3, 1)
        matrix.add_boundary_coef(5, 4, 2)
        matrix.reduce()
        pairs = matrix.birth_death_pairs()
        assert sorted(pairs) == sorted(expected)


@pytest.mark.integration
def test_main(datadir, tmpdir):
    input = os.path.join(datadir, "tetrahedron.pdgm")
    output = str(tmpdir.join("tetrahedron-p3.pdgm"))
    modp_reduction.main(modp_reduction.argument_parser().parse_args(["-p", "3", input, output]))
