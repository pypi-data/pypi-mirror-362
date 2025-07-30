import numpy as np

import homcloud.plotly_3d as p3d
import plotly.graph_objects as go


def circumsphere(tetrahedron):
    """Compute circumsphere

    Args:
        tetrahedron (list of list of double): list of coordinates of vertices

    Returns:
        tuple[np.array, float]: The cneter and radius of the circumsphere

    Example:
    >>> circumsphere([
    >>>     [0, 0, 0],
    >>>     [2, 0, 0],
    >>>     [1, np.sqrt(3), 0],
    >>>     [1, np.sqrt(3) / 3, np.sqrt(6) * 2 / 4.5],
    >>> ])
    -> (array([ 1.        ,  0.57735027, -0.06804138]), 1.156703489647612)
    """
    tetrahedron = np.array(tetrahedron)
    x = tetrahedron[:, 0]
    y = tetrahedron[:, 1]
    z = tetrahedron[:, 2]
    a = np.linalg.det(np.vstack([x, y, z, np.ones(4)]))
    w = x**2 + y**2 + z**2
    Dx = np.linalg.det(np.vstack([w, y, z, np.ones(4)]))
    Dy = -np.linalg.det(np.vstack([w, x, z, np.ones(4)]))
    Dz = np.linalg.det(np.vstack([w, x, y, np.ones(4)]))
    c = np.linalg.det(np.vstack([w, x, y, z]))
    r = np.sqrt(np.inner(Dx, Dx) + np.inner(Dy, Dy) + np.inner(Dz, Dz) - 4 * a * c) / (2 * np.abs(a))
    center = np.array([Dx, Dy, Dz]) / (2 * a)
    np.testing.assert_allclose(np.linalg.norm(center - tetrahedron[0, :]), r)
    np.testing.assert_allclose(np.linalg.norm(center - tetrahedron[1, :]), r)
    np.testing.assert_allclose(np.linalg.norm(center - tetrahedron[2, :]), r)
    np.testing.assert_allclose(np.linalg.norm(center - tetrahedron[3, :]), r)
    return center, r


def circumcircle(tetrahedron, i, j, k):
    """Computes the circumcircle of the triangle in the given tetrahedron
    Args:
        tetrahedron (list of list of double): list of coordinates of vertices
        i (int): The first vertex index, from 0 to 3
        j (int): The second vertex index, from 0 to 3
        k (int): The third vertex index, from 0 to 3

    Returns:
        tuple[np.array, float]: The cneter and radius of the circumcircle

    """
    a = np.array(tetrahedron[i])
    b = np.array(tetrahedron[j])
    c = np.array(tetrahedron[k])
    ac = c - a
    ab = b - a
    g = np.cross(ab, ac)
    d = (np.cross(g, ab) * (np.inner(ac, ac)) + np.cross(ac, g) * (np.inner(ab, ab))) / (2 * np.inner(g, g))
    np.testing.assert_allclose(np.linalg.norm(a + d - b), np.linalg.norm(d))
    np.testing.assert_allclose(np.linalg.norm(a + d - c), np.linalg.norm(d))
    return a + d, np.linalg.norm(d)


def center(tetrahedron, i, j):
    """Computes the center of the edge in the given tetrahedron
    Args:
        tetrahedron (list of list of double): list of coordinates of vertices
        i (int): The first vertex index, from 0 to 3
        j (int): The second vertex index, from 0 to 3

    Returns:
        tuple[np.array, float]: The cneter and radius


    """

    a = np.array(tetrahedron[i])
    b = np.array(tetrahedron[j])
    return (a + b) / 2, np.linalg.norm(b - a) / 2


def minimum_enclosing_ball(tetrahedron):
    """Compute minimum enclosing ball of a tetrahedron

    Args:
        tetrahedron (list of list of double): list of coordinates of vertices

    Returns:
        tuple[np.array, float]: The cneter and radius of the minimum enclosing ball

    Example:
    >>> circumsphere([
    >>>     [0, 0, 0],
    >>>     [2, 0, 0],
    >>>     [1, np.sqrt(3), 0],
    >>>     [1, np.sqrt(3) / 3, np.sqrt(6) * 2 / 4.5],
    >>> ])
    -> (array([ 1.        ,  0.57735027, -0.06804138]), 1.156703489647612)
    """

    def contain(c, r):
        r *= 1.000000001
        return (
            (np.linalg.norm(c - tetrahedron[0]) <= r)
            and (np.linalg.norm(c - tetrahedron[1]) <= r)
            and (np.linalg.norm(c - tetrahedron[2]) <= r)
            and (np.linalg.norm(c - tetrahedron[3]) <= r)
        )

    def find(candidates):
        return min((c for c in candidates if contain(*c)), default=None, key=lambda cand: cand[1])

    candidate = find(center(tetrahedron, i, j) for i in range(4) for j in range(i + 1, 4))
    if candidate is not None:
        return candidate

    candidate = find(
        [
            circumcircle(tetrahedron, 0, 1, 2),
            circumcircle(tetrahedron, 0, 1, 3),
            circumcircle(tetrahedron, 0, 2, 3),
            circumcircle(tetrahedron, 1, 2, 3),
        ]
    )
    if candidate is not None:
        return candidate

    return circumsphere(tetrahedron)


def show_circumcenters(tetrahedron):
    """Method for debug"""
    c0, _ = circumsphere(tetrahedron)
    c1, _ = circumcircle(tetrahedron, 0, 1, 2)
    c2, _ = circumcircle(tetrahedron, 0, 1, 3)
    c3, _ = circumcircle(tetrahedron, 0, 2, 3)
    c4, _ = circumcircle(tetrahedron, 1, 2, 3)
    centers = [center(tetrahedron, i, j)[0] for i in range(4) for j in range(i + 1, 4)]
    cm, _ = minimum_enclosing_ball(tetrahedron)
    fig = go.Figure(
        [
            p3d.Simplices([tetrahedron], color="green", name="tetrahedron"),
            p3d.PointCloud(np.array([c0]), color="black", size=2),
            p3d.PointCloud(np.vstack([c1, c2, c3, c4]), color="red", size=2),
            p3d.PointCloud(np.vstack(centers), color="green", size=2),
            p3d.PointCloud(np.array([cm]), color="blue", size=3),
        ]
    )
    return fig
