import numpy as np

from homcloud.homccube import compute_pd


class TestHomccube(object):
    class Test_compute_pd(object):
        def test_2D_3x3(self):
            pairs = compute_pd(
                np.array(
                    [
                        [0, 1, 2],
                        [6, 8, 7],
                        [3, 4, 5],
                    ],
                    np.int32,
                ),
                [False, False],
                1,
            )
            assert pairs == [(0, 0, None), (0, 3, 6), (1, 7, 8)]

        def test_3D_3x3x3(self):
            pairs = compute_pd(
                np.array(
                    [
                        [[0, 12, 1], [10, 25, 19], [2, 15, 3]],
                        [[8, 18, 13], [22, 26, 23], [9, 21, 17]],
                        [[4, 14, 5], [11, 24, 20], [6, 16, 7]],
                    ],
                    np.int32,
                ),
                [False, False, False],
                1,
            )
            assert pairs == [
                (0, 0, None),
                (0, 4, 8),
                (0, 6, 9),
                (0, 2, 10),
                (0, 1, 12),
                (0, 5, 13),
                (0, 3, 15),
                (0, 7, 16),
                (1, 20, 23),
                (1, 19, 24),
                (1, 17, 21),
                (1, 14, 18),
                (1, 11, 22),
                (2, 25, 26),
            ]

        def test_3D_2x2x2_periodic(self):
            pairs = compute_pd(np.array([[[0, 1], [2, 3]], [[4, 5], [6, 7]]], np.int32), [True, True, True], 1)

            assert pairs == [
                (0, 0, None),
                (1, 4, None),
                (1, 2, None),
                (1, 1, None),
                (2, 6, None),
                (2, 5, None),
                (2, 3, None),
                (3, 7, None),
            ]
