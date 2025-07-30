import homcloud.pict.distance_transform as pict_distance_transform


def distance_transform(pict, signed=False, metric="manhattan", periodicity=None, obstacle=None, VI=None, V=None):
    """Distance transform.

    Args:
        pict (numpy.ndarray): A binary picture. dtype must be bool.
        signed (bool): True for signed distance transform
        metric (string): Metric. The following metrics are available:
            "manhattan", "chebyshev", "euclidean", "mahalanobis"
        periodicity (None or list of bool): Periodic boundary condition
        obstacle (None or numpy.ndarray): Obstacle bitmap
        VI (None or numpy.ndarray): Inverse matrix for Mahalanobis metric
        V (None or numpy.ndarray): Matrix for Mahalanobis metric

    Returns:
        An ndarray object.

    Example:
        >>> import homcloud.interface as hc
        >>> import numpy as np
        >>> bitmap = np.array([[0, 1, 0, 0], [1, 1, 0, 1]], dtype=bool)
        >>> hc.PDList.from_bitmap_levelset(hc.distance_transform(bitmap, True))
        -> Returns a new PDList

    Remarks:
        The current implementation for periodic BC is a simple periodic image
        copy method. Hence the performance is not so good.
        The developers of HomCloud plan to implove the efficiency
        in the future.
    """
    assert pict.dtype == bool
    return pict_distance_transform.distance_transform(
        pict, metric, signed, periodicity=periodicity, obstacle=obstacle, VI=VI, V=V
    )
