import numpy as np
import plotly.graph_objects as go

import homcloud.plotly_3d as p3d

SIMPLICES = [
    [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [[2, 2, 2], [1, 2, 2], [2, 1, 2], [2, 2, 1]],
]


def test_PointCloud():
    pointcloud = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert isinstance(p3d.PointCloud(pointcloud), go.Scatter3d)


def test_Simplices():
    assert isinstance(p3d.Simplices(SIMPLICES), go.Scatter3d)


def test_SimplicesMesh():
    assert isinstance(p3d.SimplicesMesh(SIMPLICES), go.Mesh3d)


def test_Loop():
    points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert isinstance(p3d.Loop(points), go.Scatter3d)


def test_Bitmap3d():
    bitmap = np.array(
        [[[0, 1, 1], [1, 0, 1], [1, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 0]], [[0, 0, 1], [0, 0, 1], [1, 1, 1]]]
    )
    assert isinstance(p3d.Bitmap3d(bitmap), go.Mesh3d)


def test_Voxels():
    voxels = [[0, 0, 4], [1, 2, 0], [3, 3, 3]]
    assert isinstance(p3d.Voxels(voxels), go.Mesh3d)
