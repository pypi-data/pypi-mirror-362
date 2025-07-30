import pytest

import homcloud.phat_ext as phat


class TestMatrix(object):
    @pytest.fixture
    def matrix(self):
        matrix = phat.Matrix(7, "simplicial")
        matrix.set_dim_col(0, 0, [])
        matrix.set_dim_col(1, 0, [])
        matrix.set_dim_col(2, 1, [0, 1])
        matrix.set_dim_col(3, 0, [])
        matrix.set_dim_col(4, 1, [1, 3])
        matrix.set_dim_col(5, 1, [0, 3])
        matrix.set_dim_col(6, 2, [2, 4, 5])
        return matrix

    def test_birth_death_pairs(self, matrix):
        matrix.reduce_twist()
        assert sorted(matrix.birth_death_pairs()) == sorted([(0, 0, None), (0, 1, 2), (0, 3, 4), (1, 5, 6)])
