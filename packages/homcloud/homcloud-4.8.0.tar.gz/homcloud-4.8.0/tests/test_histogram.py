import numpy as np
import pytest

from homcloud.histogram import Ruler, PDHistogram, Histogram, HistoSpec
from homcloud.pdgm import SimplePDGM
import homcloud.pdgm as pdgm


class TestRuler(object):
    class Test_create_xy_rulers(object):
        def test_for_normal_usage(self):
            x_ruler, y_ruler = Ruler.create_xy_rulers((0, 1), 100, (1, 2), 200, None)
            assert x_ruler.minmax == (0, 1)
            assert x_ruler.bins == 100
            assert y_ruler.minmax == (1, 2)
            assert y_ruler.bins == 200

        def test_when_y_range_and_ybins_are_not_given(self):
            x_ruler, y_ruler = Ruler.create_xy_rulers((0, 1), 100, None, None, None)
            assert x_ruler.minmax == (0, 1)
            assert x_ruler.bins == 100
            assert y_ruler.minmax == (0, 1)
            assert y_ruler.bins == 100

        def test_when_xrange_is_not_given(self):
            diagram = SimplePDGM(None, np.array([0.0, 4.0]), np.array([1.0, 5.0]))
            x_ruler, y_ruler = Ruler.create_xy_rulers(None, 100, None, None, diagram)
            assert x_ruler.minmax == (0.0, 5.0)
            assert y_ruler.minmax == (0.0, 5.0)


class TestHistoSpec(object):
    @pytest.mark.parametrize(
        "sign_flipped, expected",
        [
            (False, [[0, 1, 1, 2, 2, 2], [0, 0, 1, 0, 1, 2]]),
            (True, [[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2], [0, 1, 2, 3, 0, 1, 2, 3, 1, 2, 3]]),
        ],
    )
    def test_indices_for_vectorization(self, sign_flipped, expected):
        histospec = HistoSpec(np.array([0, 1, 2, 3, 4]), np.array([-0.5, 0.5, 1.5, 2.5]), sign_flipped)
        assert np.allclose(histospec.indices_for_vectorization(), expected)

    @pytest.mark.parametrize(
        "xruler, yruler, sign_flipped, expected",
        [
            (
                Ruler((0, 1), 5),
                Ruler((0, 1), 5),
                False,
                np.array(
                    [
                        [1, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1],
                    ],
                    dtype=bool,
                ),
            ),
            (
                Ruler((0, 1), 5),
                Ruler((0, 1), 5),
                True,
                np.array(
                    [
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1],
                        [0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 1],
                    ],
                    dtype=bool,
                ),
            ),
            (
                Ruler((-2, 2), 4),
                Ruler((0, 5), 5),
                False,
                np.array(
                    [
                        [1, 1, 1, 0],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                    ],
                    dtype=bool,
                ),
            ),
            (
                Ruler((-2, 2), 4),
                Ruler((0, 5), 5),
                True,
                np.array(
                    [
                        [0, 0, 1, 1],
                        [0, 0, 0, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                    ],
                    dtype=bool,
                ),
            ),
            (
                Ruler((0, 4), 4),
                Ruler((-0.5, 3.5), 4),
                False,
                np.array([[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]], dtype=bool),
            ),
            (
                Ruler((0, 4), 4),
                Ruler((-0.5, 3.5), 4),
                True,
                np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1]], dtype=bool),
            ),
        ],
    )
    def test_vectorize_mask(self, xruler, yruler, sign_flipped, expected):
        histospec = HistoSpec(xruler.edges(), yruler.edges(), sign_flipped)
        assert np.allclose(histospec.vectorize_mask(), expected)

    def test_centers_of_vectorize_bins(self):
        histospec = HistoSpec(np.linspace(0, 4, 5), np.linspace(-0.5, 3.5, 5), False)
        assert np.allclose(
            histospec.centers_of_vectorize_bins(),
            np.array(
                [
                    [0.5, 0.0],
                    [0.5, 1.0],
                    [1.5, 1.0],
                    [0.5, 2.0],
                    [1.5, 2.0],
                    [2.5, 2.0],
                    [0.5, 3.0],
                    [1.5, 3.0],
                    [2.5, 3.0],
                    [3.5, 3.0],
                ]
            ),
        )

    @pytest.mark.parametrize(
        "sign_flipped, expected",
        [
            (
                False,
                [
                    [0, 1, 2, 3],
                    [0, 1, 2, 3],
                    [0, 1, 2, 3],
                ],
            ),
            (
                True,
                [
                    [1, 2, 3, 4],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4],
                ],
            ),
        ],
    )
    def test_xedges_of_bins(self, sign_flipped, expected):
        histospec = HistoSpec(np.linspace(0, 4, 5), np.linspace(-0.5, 2.5, 4), sign_flipped)
        assert np.allclose(histospec.xedges_of_bins(), expected)

    @pytest.mark.parametrize(
        "sign_flipped, expected",
        [
            (False, [[0.5, 0.5, 0.5, 0.5], [1.5, 1.5, 1.5, 1.5], [2.5, 2.5, 2.5, 2.5]]),
            (True, [[-0.5, -0.5, -0.5, -0.5], [0.5, 0.5, 0.5, 0.5], [1.5, 1.5, 1.5, 1.5]]),
        ],
    )
    def test_yedges_of_bins(self, sign_flipped, expected):
        histospec = HistoSpec(np.linspace(0, 4, 5), np.linspace(-0.5, 2.5, 4), sign_flipped)
        assert np.allclose(histospec.yedges_of_bins(), expected)

    def test_coordinate_of_center_of_bins(self):
        histospec = HistoSpec(np.linspace(0, 4, 5), np.linspace(-0.5, 2.5, 4), False)
        xs, ys = histospec.coordinates_of_center_of_bins()
        assert np.allclose(
            xs,
            [
                [0.5, 1.5, 2.5, 3.5],
                [0.5, 1.5, 2.5, 3.5],
                [0.5, 1.5, 2.5, 3.5],
            ],
        )
        assert np.allclose(
            ys,
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [2, 2, 2, 2],
            ],
        )

    @pytest.mark.parametrize(
        "vector, dtype, expected_values",
        [
            (np.array([0.4, -0.2, 0.1]), float, [[0, 0, 0], [0.4, 0, 0], [-0.2, 0.1, 0]]),
            (np.array([True, True, False]), bool, [[0, 0, 0], [1, 0, 0], [1, 0, 0]]),
        ],
    )
    def test_histogram_from_vector(self, vector, dtype, expected_values):
        histospec = HistoSpec.from_rulers(Ruler((1, 4), 3), Ruler((0, 3), 3), False)
        histogram = histospec.histogram_from_vector(vector)
        assert np.allclose(histogram.values, expected_values)
        assert histogram.values.dtype == dtype

    @pytest.mark.parametrize(
        "ess_values, has_ess_values",
        [
            (None, False),
            (np.array([0.5, 1.0, 0.0]), True),
        ],
    )
    def test_histogram_from_2darray(self, ess_values, has_ess_values):
        histospec = HistoSpec.from_rulers(Ruler((1, 4), 3), Ruler((0, 3), 3), False)
        values = np.array([[0, 0, 0], [0.4, 0, 0], [-0.2, 0.1, 0]])
        histogram = histospec.histogram_from_2darray(values, ess_values)
        assert np.allclose(histogram.values, values)
        assert histogram.has_ess_values() == has_ess_values
        if histogram.has_ess_values():
            assert np.allclose(histogram.ess_values, ess_values)


class TestHistogram:
    class Test_reconstruct_from_vector:
        histinfo = {
            "x-edges": [1, 2, 3, 4],
            "y-edges": [0, 1, 2, 3],
            "x-indices": [0, 0, 1],
            "y-indices": [1, 2, 2],
        }

        def test_for_float_vector(self):
            vector = np.array([0.4, -0.2, 0.1])
            histogram = Histogram.reconstruct_from_vector(vector, self.histinfo)
            assert np.allclose(histogram.xedges, [1, 2, 3, 4])
            assert np.allclose(histogram.yedges, [0, 1, 2, 3])
            assert np.allclose(histogram.values, [[0, 0, 0], [0.4, 0, 0], [-0.2, 0.1, 0]])
            assert histogram.histospec.xy_extent() == [1, 4, 0, 3]
            assert histogram.x_range() == (1, 4)
            assert histogram.y_range() == (0, 3)
            assert histogram.maxvalue() == 0.4

        def test_for_boolean_vector(self):
            vector = np.array([True, True, False], dtype=bool)
            histogram = Histogram.reconstruct_from_vector(vector, self.histinfo)
            assert histogram.values.dtype == bool
            assert np.allclose(histogram.values, [[0, 0, 0], [1, 0, 0], [1, 0, 0]])

    def test_vectorize(self):
        values = np.array([[0, 0, 0], [0.4, 0, 0], [-0.2, 0.1, 0]])
        xedges = np.array([1, 2, 3, 4])
        yedges = np.array([0, 1, 2, 3])
        histogram = Histogram(values, HistoSpec(xedges, yedges))
        assert np.allclose(histogram.vectorize(), [0.4, -0.2, 0.1])

    def test_value_at(self):
        values = np.array([[0, 0, 0], [0.4, 0, 0], [-0.2, 0.1, 0]])
        xedges = np.array([1, 2, 3, 4])
        yedges = np.array([0, 1, 2, 3])
        histogram = Histogram(values, HistoSpec(xedges, yedges))
        assert histogram.value_at(1.5, 2.4) == -0.2
        assert histogram.value_at(1.5, 0.9) == 0.0
        assert histogram.value_at(0.5, 1.5) is None
        assert histogram.value_at(2.5, 4.2) is None

    def test_binary_histogram_by_ranking(self):
        values = np.array([[8.0, 4, 3], [-10, 0, -1], [0, 7, 2]])
        histospec = HistoSpec(np.array([0, 1, 2, 3]), np.array([0, 1, 2, 3]))
        histogram = Histogram(values, histospec)

        assert np.array_equal(
            histogram.binary_histogram_by_ranking((0, 2), +1, True).values,
            np.array([[1, 0, 0], [0, 0, 0], [0, 1, 0]], dtype=bool),
        )
        assert np.array_equal(
            histogram.binary_histogram_by_ranking((0, 2), -1, True).values,
            np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=bool),
        )
        assert np.array_equal(
            histogram.binary_histogram_by_ranking((0, 2), None, True).values,
            np.array([[1, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=bool),
        )
        assert np.array_equal(
            histogram.binary_histogram_by_ranking((0, 2), +1, False).values,
            np.array([[1, 1, 0], [0, 0, 0], [0, 1, 0]], dtype=bool),
        )

    class Test_vectorize(object):
        def test_for_empty_pd(self):
            histogram = PDHistogram(pdgm.empty_pd(), Ruler((-2, 2), 4), Ruler((0, 5), 5))
            assert np.allclose(histogram.vectorize(), np.zeros((19,)))

        def test_for_normal_pd(self):
            diagram = SimplePDGM(None, np.array([0.5, 1.4, 0.7]), np.array([2.4, 1.6, 2.1]))
            histogram = PDHistogram(diagram, Ruler((0, 4), 4), Ruler((-2, 3), 5))
            assert np.allclose(histogram.vectorize(), np.array([0, 0, 1, 2, 0, 0], dtype=float))

        def test_for_sign_flipped_pd(self):
            diagram = SimplePDGM(None, np.array([2.4, 1.6, 2.1, 2.5, 3.5]), np.array([0.5, 1.4, 0.7, 2.5, 1.5]))
            diagram.sign_flipped = True
            histogram = PDHistogram(diagram, Ruler((-2, 3), 5), Ruler((0, 4), 4))
            assert np.allclose(histogram.vectorize(), np.array([0, 0, 2, 1, 0, 1], dtype=float))

    def test_apply_weight(self):
        diagram = SimplePDGM(None, np.array([0.5, 1.4, 0.7]), np.array([2.4, 1.6, 2.1]))
        histogram = PDHistogram(diagram, Ruler((0, 4), 4), Ruler((-2, 3), 5))
        histogram.apply_weight(lambda b, d: 1 if b < 1 else 0)
        assert np.allclose(
            histogram.values,
            np.array(
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [2, 0, 0, 0],
                ],
                dtype=float,
            ),
        )
