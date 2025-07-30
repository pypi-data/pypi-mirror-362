import pytest
import homcloud.hera_bottleneck as hera_bt
import homcloud.hera_wasserstein as hera_ws

import numpy as np
import math


@pytest.mark.parametrize(
    "births_1, deaths_1, births_2, deaths_2, delta, expected",
    [
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([0.0, 2.0]), np.array([1.0, 2.5]), 0.01, 0.0),
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([2.0, 0.0]), np.array([2.5, 1.0]), 0.0, 0.0),
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([]), np.array([]), 0.0, 0.5),
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([]), np.array([]), 0.01, 0.5),
    ],
)
def test_bottleneck_distance(births_1, deaths_1, births_2, deaths_2, delta, expected):
    assert hera_bt.bottleneck_distance(births_1, deaths_1, births_2, deaths_2, delta) == pytest.approx(
        expected, abs=delta
    )


@pytest.mark.parametrize(
    "births_1, deaths_1, births_2, deaths_2, power, internal_p, delta, expected",
    [
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([0.0, 2.0]), np.array([1.0, 2.5]), 2, np.inf, 0.01, 0.0),
        (np.array([0.0, 2.0]), np.array([1.0, 2.5]), np.array([2.0, 0.0]), np.array([2.5, 1.0]), 2, np.inf, 0.0, 0.0),
        (
            np.array([0.0, 2.0]),
            np.array([1.0, 2.5]),
            np.array([]),
            np.array([]),
            2,
            np.inf,
            0.01,
            math.sqrt(0.5**2 + 0.25**2),
        ),
        (
            np.array([0.0, 2.0]),
            np.array([1.0, 2.5]),
            np.array([]),
            np.array([]),
            2,
            2,
            0.01,
            math.sqrt(0.5**2 * 2 + 0.25**2 * 2),
        ),
        (
            np.array([0.0, 2.0]),
            np.array([1.0, 2.5]),
            np.array([0.1, 1.7]),
            np.array([0.8, 2.3]),
            2,
            np.inf,
            0.01,
            math.sqrt(0.2**2 + 0.3**2),
        ),
        (
            np.array([0.0, 2.0]),
            np.array([1.0, 2.5]),
            np.array([0.1, 1.5]),
            np.array([0.8, 2.3]),
            2,
            np.inf,
            0.01,
            math.sqrt(0.2**2 + 0.25**2 + 0.4**2),
        ),
    ],
)
def test_wasserstein_distance(births_1, deaths_1, births_2, deaths_2, power, internal_p, delta, expected):
    assert hera_ws.wasserstein_distance(
        births_1, deaths_1, births_2, deaths_2, power, internal_p, delta
    ) == pytest.approx(expected, rel=delta)
