import math

import homcloud.hera_bottleneck as hera_bottleneck
import homcloud.hera_wasserstein as hera_wasserstein


def bottleneck(pd1, pd2, delta=0.000001):
    """
    Compute the bottleneck distance between two diagrams.

    The parameter `delta` determines the acceptable relative error.
    If delta is zero, the return value is exact but slower.
    If delta is positive, the return value is not exact but faster.

    Notes:
        This function uses hera library <https://bitbucket.org/grey_narn/hera>.
        See the following paper for theoretical details:
        Michael Kerber, Dmitriy Morozov, and Arnur Nigmetov,
        "Geometry Helps to Compare Persistence Diagrams.",
        Journal of Experimental Algorithmics, vol. 22, 2017, pp. 1--20.
        (conference version: ALENEX 2016).

    Args:
        pd1 (PD): A persistence diagram
        pd2 (PD): Another persistence diagram
        delta (float): Acceptable relative error, must be zero or positive

    Returns:
        float: the bottleneck distance betweeen two diagrams
    """
    return hera_bottleneck.bottleneck_distance(pd1.births, pd1.deaths, pd2.births, pd2.deaths, delta)


def wasserstein(pd1, pd2, power=2, internal_p=math.inf, delta=0.000001):
    """
    Compute the Wasserstein distance between two diagrams.

    Example:
        >>> import homcloud.interface as hc
        >>> hc.distance.wasserstein(pd1, pd2, delta=0.01)
        Returns 2-Wasserstein distance with relative error <= 0.01

    Notes:
        This function uses hera library <https://bitbucket.org/grey_narn/hera>.
        See the following paper for theoretical details:
        Michael Kerber, Dmitriy Morozov, and Arnur Nigmetov,
        "Geometry Helps to Compare Persistence Diagrams.",
        Journal of Experimental Algorithmics, vol. 22, 2017, pp. 1--20.
        (conference version: ALENEX 2016).

    Args:
        pd1 (PD): A persistence diagram
        pd2 (PD): Another persistence diagram
        power (float): Wasserstein degree, must be larger than or equal to 1
        internal_p (float): The internal norm in Wasserstein distance,
            must be larger than or equal to 1 including infinity
        delta (float): Acceptable relative error, must be zero or positive

    Returns:
        float: the Wasserstein distance betweeen two diagrams
    """
    return hera_wasserstein.wasserstein_distance(
        pd1.births, pd1.deaths, pd2.births, pd2.deaths, power, internal_p, delta
    )
