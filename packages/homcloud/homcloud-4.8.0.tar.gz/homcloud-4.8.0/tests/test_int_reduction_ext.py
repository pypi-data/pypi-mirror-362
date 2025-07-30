import pytest

import homcloud.int_reduction_ext as int_reduction_ext


class TestChecker(object):
    @pytest.mark.parametrize(
        "num_cells, matrix, expected",
        [
            ([2], [(0, []), (0, [])], (0, 0)),
            (
                [4, 6, 2],
                [  # Mobius ring (see mobius.svg)
                    (0, []),
                    (0, []),
                    (0, []),
                    (0, []),
                    (1, [(0, 1), (3, -1)]),
                    (1, [(1, 1), (2, -1)]),  # 4-5
                    (1, [(0, 1), (2, -1)]),
                    (1, [(1, 1), (3, -1)]),  # 6-7
                    (1, [(0, 1), (1, -1)]),
                    (1, [(2, 1), (3, -1)]),  # 8-9
                    (2, [(6, -1), (7, 1), (8, 1), (9, -1)]),  # 10
                    (2, [(4, -1), (5, 1), (8, 1), (9, 1)]),  # 10
                ],
                (2, 11),
            ),
        ],
    )
    def test_check(self, num_cells, matrix, expected):
        checker = int_reduction_ext.Checker(num_cells)
        for col, (dim, column) in enumerate(matrix):
            checker.add_cell(dim)
            for row, value in column:
                checker.add_boundary_coef(col, row, value)
        assert checker.check() == expected

    def test_column(self):
        checker = int_reduction_ext.Checker([3, 1])
        checker.add_cell(0)
        checker.add_cell(0)
        checker.add_cell(0)
        checker.add_cell(1)
        checker.add_boundary_coef(3, 0, 1)
        checker.add_boundary_coef(3, 2, -1)
        assert checker.column(0) == []
        assert checker.column(3) == [1, 0, -1]
