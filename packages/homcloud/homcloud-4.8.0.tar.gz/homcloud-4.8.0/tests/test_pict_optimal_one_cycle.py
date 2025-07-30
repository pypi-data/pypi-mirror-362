import pytest
import numpy as np

from homcloud.pict.optimal_one_cycle import search, Result


@pytest.mark.parametrize(
    "bitmap, birth_level, start, expected_path",
    [
        (
            np.array([[2, 1, 0, 15], [3, 12, 10, 4], [11, 14, 13, 5], [8, 7, 6, 9]]),
            11,
            (2, 0),
            [(2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0)],
        ),
        (
            np.array(
                [[9, 12, 10, 23, 22], [15, 24, 11, 20, 21], [13, 14, 16, 4, 3], [8, 19, 17, 18, 5], [7, 6, 0, 1, 2]]
            ),
            16,
            (2, 2),
            [(2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        ),
        (
            np.array(
                [
                    [[12, 13, 14], [0, 15, 1], [2, 3, 4]],
                    [[16, 17, 18], [5, 19, 6], [20, 21, 22]],
                    [[7, 8, 9], [10, 23, 11], [24, 25, 26]],
                ]
            ),
            11,
            (2, 1, 2),
            [
                (2, 1, 2),
                (2, 0, 2),
                (2, 0, 1),
                (2, 0, 0),
                (2, 1, 0),
                (1, 1, 0),
                (0, 1, 0),
                (0, 2, 0),
                (0, 2, 1),
                (0, 2, 2),
                (0, 1, 2),
                (1, 1, 2),
                (2, 1, 2),
            ],
        ),
    ],
)
def test_search(bitmap, birth_level, start, expected_path):
    assert search(bitmap, birth_level, start) == expected_path


class TestResult(object):
    @pytest.mark.parametrize(
        "path, expected_path, expected_boundary_points",
        [
            (
                [(0, 1), (1, 1), (1, 0), (0, 0), (0, 1)],
                [[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]],
                [[0, 1], [1, 1], [1, 0], [0, 0]],
            ),
            (
                [(2, 1, 2), (1, 1, 2), (1, 2, 2), (2, 2, 2), (2, 1, 2)],
                [[2, 1, 2], [1, 1, 2], [1, 2, 2], [2, 2, 2], [2, 1, 2]],
                [[2, 1, 2], [1, 1, 2], [1, 2, 2], [2, 2, 2]],
            ),
        ],
    )
    def test_to_jsondict(self, path, expected_path, expected_boundary_points):
        result = Result(8.124, 9.13, path)
        dic = result.to_jsondict()
        assert sorted(dic.keys()) == sorted(
            [
                "birth-time",
                "death-time",
                "boundary-points",
                "path",
            ]
        )
        assert dic["birth-time"] == 8.124
        assert dic["death-time"] == 9.13
        assert dic["path"] == expected_path
        assert sorted(dic["boundary-points"]) == sorted(expected_boundary_points)
