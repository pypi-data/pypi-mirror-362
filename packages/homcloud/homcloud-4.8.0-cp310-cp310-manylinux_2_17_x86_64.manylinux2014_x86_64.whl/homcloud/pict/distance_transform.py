import numpy as np

from scipy.ndimage import distance_transform_cdt, distance_transform_edt
from sklearn.neighbors import BallTree
from homcloud.compat import DistanceMetric
from scipy.ndimage import binary_erosion

from homcloud.distance_transform_ext import positive_distance_transform_manhattan_with_mask
from homcloud.pict.utils import nd_indices


def distance_transform(pict, metric, signed=False, periodicity=None, obstacle=None, **opts):
    if obstacle is not None:
        check_arguments_for_obstacle(metric, pict, obstacle)

    if periodicity:
        pict = periodic_extend(pict, periodicity)
        if obstacle:
            obstacle = periodic_extend(pict, periodicity)
        distances = distance_transform(pict, metric, signed, None, obstacle, **opts)
        return periodic_shrink(distances, periodicity)

    npict = ~pict

    if signed:
        ret = -distance_transform(npict, metric, False, periodicity, None, **opts)
    else:
        ret = np.zeros_like(pict, dtype=float)

    if metric == "manhattan" and obstacle is not None:
        positive_distance_transform_manhattan_with_mask(pict, obstacle, ret)
    elif metric == "manhattan":
        ret[npict] = distance_transform_cdt(npict, "taxicab")[npict]
    elif metric == "chebyshev":
        ret[npict] = distance_transform_cdt(npict, "chessboard")[npict]
    elif metric == "euclidean":
        ret[npict] = distance_transform_edt(npict)[npict]
    elif metric == "mahalanobis":
        ret[npict] = distance_transform_mahalanobis(npict, **opts)[npict]
    else:
        raise ValueError("Unknown metric: {}".format(metric))

    return ret


def distance_transform_mahalanobis(npict, VI=None, V=None):
    if VI is not None:
        metric = DistanceMetric.get_metric("mahalanobis", VI=VI)
    elif V is not None:
        metric = DistanceMetric.get_metric("mahalanobis", V=V)

    ret = np.zeros_like(npict, dtype=float)
    balltree = BallTree(boundary_pixels(~npict), leaf_size=30, metric=metric)
    empty_pixels = pixel_positions(npict)

    def compute_distances(targets):
        (d, _) = balltree.query(targets, k=1)
        return d[:, 0]

    np.place(ret, npict, compute_distances(empty_pixels))

    return ret


def check_arguments_for_obstacle(metric, pict, obstacle):
    if metric != "manhattan":
        raise RuntimeError("obstacle is avaiable only with manhattan metric")
    if np.any(pict & obstacle):
        raise RuntimeError("obstacle must not have intersection with input image")


def pixel_positions(pict):
    """Return indices of True in 2D boolean ndarray pict"""
    indices = nd_indices(pict.shape)
    return indices[pict.flatten()]


def boundary_pixels(pict):
    return pixel_positions(np.logical_xor(pict, binary_erosion(pict, iterations=1, border_value=1)))


def periodic_extend(pict, periodicity):
    for nth, p in enumerate(periodicity):
        if p:
            pict = np.concatenate((pict, pict, pict), axis=nth)
    return pict


def periodic_shrink(pict, periodicity):
    for nth, p in enumerate(periodicity):
        if p:
            pict = np.split(pict, 3, axis=nth)[1]
    return pict
