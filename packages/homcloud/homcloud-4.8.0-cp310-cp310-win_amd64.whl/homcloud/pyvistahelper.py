"""
This module provides helper functions for pyvista (https://pyvista.org/) for HomCloud.
"""

import pyvista as pv
import numpy as np


def Bitmap3D(array):
    """
    Returns PyVista's mesh object for 3d array bitmap.

    Args:
        array (numpy.ndarray[(Any, Any, Any), float]): 3d array

    Returns:
        pyvista.ImageData: PyVista's mesh object

    """
    array = np.array(array)
    assert array.ndim == 3
    grids = pv.ImageData(dimensions=np.array(array.shape) + 1, origin=(-0.5, -0.5, -0.5))
    grids.cell_data["values"] = array.flatten(order="F")
    return grids


def Lines(lines):
    """
    Returns PyVista's mesh object for lines.

    Args:
        array (numpy.ndarray[(Any, 2, 3), float]): list of lines

    Returns:
        pyvista.PolyData: PyVista's mesh object

    """
    lines = np.array(lines)
    assert lines.ndim == 3 and lines.shape[1] == 2 and lines.shape[2] == 3
    return pv.PolyData(
        lines.reshape((lines.shape[0] * 2, 3)), lines=np.array([[2, 2 * i, 2 * i + 1] for i in range(lines.shape[0])])
    )


def Loop(points):
    """
    Returns PyVista's mesh object for a loop.

    Args:
        array (numpy.ndarray[(Any, 3), float]): list of points

    Returns:
        pyvista.PolyData: PyVista's mesh object

    """
    points = np.array(points)
    assert points.ndim == 2 and points.shape[1] == 3
    return pv.PolyData(points, lines=[[2, k, (k + 1) % points.shape[0]] for k in range(points.shape[0])])


def Triangles(triangles):
    """
    Returns PyVista's mesh object for triangles.

    Args:
        array (numpy.ndarray[(Any, 3, 3), float]): list of triangles

    Returns:
        pyvista.PolyData: PyVista's mesh object

    """
    triangles = np.array(triangles)
    assert triangles.ndim == 3 and triangles.shape[1] == 3 and triangles.shape[2] == 3
    return pv.PolyData(
        triangles.reshape((triangles.shape[0] * 3, 3)),
        faces=[[3, k * 3, k * 3 + 1, k * 3 + 2] for k in range(triangles.shape[0])],
    )


D = np.array(
    [
        [-0.5, -0.5, -0.5],
        [+0.5, -0.5, -0.5],
        [+0.5, +0.5, -0.5],
        [-0.5, +0.5, -0.5],
        [-0.5, -0.5, +0.5],
        [+0.5, -0.5, +0.5],
        [+0.5, +0.5, +0.5],
        [-0.5, +0.5, +0.5],
    ]
)


def SparseVoxels(coords):
    """
    Returns PyVista's mesh object for triangles.

    Args:
        array (numpy.ndarray[(Any, 3), float]): list of voxels

    Returns:
        pyvista.UnstructuredGrid: PyVista's mesh object

    """
    coords = np.array(coords)
    assert coords.ndim == 2 and coords.shape[1] == 3
    n = coords.shape[0]
    return pv.UnstructuredGrid(
        {pv.CellType.HEXAHEDRON: np.arange(n * 8).reshape(n, 8)},
        (coords.reshape(n, 1, 3) + D.reshape(1, 8, 3)).reshape(n * 8, 3),
    )
