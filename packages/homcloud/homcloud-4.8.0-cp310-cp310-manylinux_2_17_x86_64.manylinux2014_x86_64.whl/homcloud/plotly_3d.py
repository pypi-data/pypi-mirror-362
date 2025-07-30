"""
This module provides helper functions for plotly (https://plotly.com/python/) for HomCloud.
"""

import plotly.graph_objects as go
import numpy as np


def PointCloud(array, color=None, size=1, name=""):
    """
    Returns a plotly's trace object for a pointcloud.

    Args:
        array (np.array): 3D pointcloud
        color (string or None): The name of color
        size (int): The size of each point
        name (string): The name of pointcloud

    Returns:
        plotly.graph_objects.Scatter3d: Plotly's trace object for the visualization of the pointcloud
    """
    assert array.ndim == 2 and array.shape[1] >= 3
    if array.shape[1] == 4 and color is True:
        color = array[:, 3]
    return go.Scatter3d(
        x=array[:, 0], y=array[:, 1], z=array[:, 2], name=name, mode="markers", marker=dict(size=size, color=color)
    )


def SimplicesMesh(simplices, color=None, name=""):
    vertices = dict()
    coordinates = []
    n = 0
    for simplex in simplices:
        for vertex in simplex:
            v = tuple(vertex)
            if v not in vertices:
                vertices[v] = n
                coordinates.append(vertex)
                n += 1

    simplices_by_vertex_index = np.array([[vertices[tuple(v)] for v in simplex] for simplex in simplices])
    coordinates = np.array(coordinates)

    return go.Mesh3d(
        x=coordinates[:, 0],
        y=coordinates[:, 1],
        z=coordinates[:, 2],
        i=simplices_by_vertex_index[:, 0],
        j=simplices_by_vertex_index[:, 1],
        k=simplices_by_vertex_index[:, 2],
        name=name,
        color=color,
    )


def Simplices(simplices, color=None, width=1, name=""):
    d = len(simplices[0])
    ij_pairs = [(i, j) for j in range(d) for i in range(j + 1, d)]
    xs = []
    ys = []
    zs = []
    for simplex in simplices:
        for i, j in ij_pairs:
            xs.extend([simplex[i][0], simplex[j][0], None])
            ys.extend([simplex[i][1], simplex[j][1], None])
            zs.extend([simplex[i][2], simplex[j][2], None])
    return go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode="lines",
        name=name,
        showlegend=False,
        line=dict(color=color, width=width),
    )


def Loop(vertices, color=None, width=1, name=""):
    vs = np.concatenate([vertices, [vertices[0]]])
    return go.Scatter3d(
        x=vs[:, 0],
        y=vs[:, 1],
        z=vs[:, 2],
        mode="lines",
        line=dict(color=color, width=width),
        name=name,
        showlegend=False,
    )


class VertexIndexer(object):
    def __init__(self):
        self.vertex2index = dict()
        self.index2vertex = list()
        self.last_index = 0

    def index_of(self, vertex):
        if vertex in self.vertex2index:
            return self.vertex2index[vertex]
        self.vertex2index[vertex] = self.last_index
        self.index2vertex.append(vertex)
        self.last_index += 1

        return self.last_index - 1

    def coordinates(self):
        return np.array(self.index2vertex)


class VoxelDrawer(object):
    def __init__(self, bitmap, color, name, offsets):
        self.bitmap = bitmap
        self.shape = bitmap.shape
        self.color = color
        self.offsets = offsets
        self.vertex_indexer = VertexIndexer()
        self.triangles = []
        self.name = name

    def isface(self, x, y, z, dx, dy, dz):
        return self.at(x, y, z) != self.at(x + dx, y + dy, z + dz)

    def at(self, x, y, z):
        if x < 0 or y < 0 or z < 0:
            return False
        if x >= self.shape[2] or y >= self.shape[1] or z >= self.shape[0]:
            return False
        return self.bitmap[z, y, x]

    def putface(self, x, y, z, dx, dy, dz):
        vertices = self.square_vertices(x, y, z, dx, dy, dz)
        vertex_indices = [self.vertex_indexer.index_of(vertex) for vertex in vertices]
        self.triangles.append([vertex_indices[0], vertex_indices[1], vertex_indices[2]])
        self.triangles.append([vertex_indices[1], vertex_indices[3], vertex_indices[2]])

    def square_vertices(self, x, y, z, dx, dy, dz):
        z += self.offsets[0]
        y += self.offsets[1]
        x += self.offsets[2]

        if dx == 1:
            return (
                (x + 0.5, y - 0.5, z - 0.5),
                (x + 0.5, y + 0.5, z - 0.5),
                (x + 0.5, y - 0.5, z + 0.5),
                (x + 0.5, y + 0.5, z + 0.5),
            )
        if dy == 1:
            return (
                (x - 0.5, y + 0.5, z - 0.5),
                (x + 0.5, y + 0.5, z - 0.5),
                (x - 0.5, y + 0.5, z + 0.5),
                (x + 0.5, y + 0.5, z + 0.5),
            )
        if dz == 1:
            return (
                (x - 0.5, y - 0.5, z + 0.5),
                (x + 0.5, y - 0.5, z + 0.5),
                (x - 0.5, y + 0.5, z + 0.5),
                (x + 0.5, y + 0.5, z + 0.5),
            )

    def graph_object(self):
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            for z in range(-1, self.shape[0] + 1):
                for y in range(-1, self.shape[1] + 1):
                    for x in range(-1, self.shape[2] + 1):
                        if self.isface(x, y, z, dx, dy, dz):
                            self.putface(x, y, z, dx, dy, dz)

        coordinates = self.vertex_indexer.coordinates()
        triangles = np.array(self.triangles)
        return go.Mesh3d(
            x=coordinates[:, 0],
            y=coordinates[:, 1],
            z=coordinates[:, 2],
            i=triangles[:, 0],
            j=triangles[:, 1],
            k=triangles[:, 2],
            name=self.name,
            color=self.color,
        )


def Bitmap3d(bitmap, color=None, name="", offsets=[0, 0, 0]):
    """
    Returns a plotly's trace object for a 3D bitmap.

    Args:
        bitmap (np.array): 3D boolean bitmap
        color (string or None): The name of color
        name (string): The name of pointcloud

    Returns:
        plotly.graph_objects.Mesh3d: Plotly's trace object for the visualization of the pointcloud
    """
    return VoxelDrawer(bitmap, color, name, offsets).graph_object()


def Voxels(voxels, color=None, name=""):
    assert len(voxels[0]) == 3
    zmax, ymax, xmax = np.max(voxels, axis=0) + 1
    bitmap = np.zeros((zmax, ymax, xmax), bool)
    for v in voxels:
        bitmap[v[0], v[1], v[2]] = True
    return Bitmap3d(bitmap, color, name)


def Cubes1d(cubes, color, width, name):
    zs = []
    ys = []
    xs = []
    for cube, d in cubes:
        zs.extend([cube[0], cube[0] + d[0], None])
        ys.extend([cube[1], cube[1] + d[1], None])
        xs.extend([cube[2], cube[2] + d[2], None])
    return go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode="lines",
        name=name,
        showlegend=False,
        line=dict(color=color, width=width),
    )


def rotate3(lst, k):
    return lst[k % 3], lst[(k + 1) % 3], lst[(k + 2) % 3]


def ndeg2rot(ndeg):
    return ndeg.index(0)


def Cubes2d(cubes, color, width, name):
    xyzs = [[], [], []]
    for cube, d in cubes:
        cs1, cs2, cs3 = rotate3(xyzs, ndeg2rot(d))
        c1, c2, c3 = rotate3(cube, ndeg2rot(d))
        cs1.extend([c1, c1, c1, c1, c1, None])
        cs2.extend([c2, c2 + 1, c2 + 1, c2, c2, None])
        cs3.extend([c3, c3, c3 + 1, c3 + 1, c3, None])

    return go.Scatter3d(
        x=xyzs[0],
        y=xyzs[1],
        z=xyzs[2],
        mode="lines",
        name=name,
        showlegend=False,
        line=dict(color=color, width=width),
    )


def Cubes(cubes, color=None, width=1, name=""):
    dim = sum(cubes[0][1])
    if dim == 1:
        return Cubes1d(cubes, color, width, name)
    elif dim == 2:
        return Cubes2d(cubes, color, width, name)
    elif dim == 3:
        raise RuntimeError("Dim 3 cube is not visualizable by homcloud-plotly")


class CubeMeshDrawer(object):
    def __init__(self, cubes, color, name):
        self.cubes = cubes
        self.color = color
        self.name = name
        self.vertex_indexer = VertexIndexer()

    UV = [
        (np.array([0, 1, 0]), np.array([0, 0, 1])),
        (np.array([0, 0, 1]), np.array([1, 0, 0])),
        (np.array([1, 0, 0]), np.array([0, 1, 0])),
    ]

    def graph_object(self):
        triangles = []

        for cube, ndeg in self.cubes:
            u, v = self.UV[ndeg.index(0)]
            p0 = self.vertex_indexer.index_of(tuple(cube))
            p1 = self.vertex_indexer.index_of(tuple(u + cube))
            p2 = self.vertex_indexer.index_of(tuple(u + v + cube))
            p3 = self.vertex_indexer.index_of(tuple(v + cube))
            triangles.append([p0, p1, p2])
            triangles.append([p0, p2, p3])

        coordinates = self.vertex_indexer.coordinates()
        triangles = np.array(triangles)
        return go.Mesh3d(
            x=coordinates[:, 0],
            y=coordinates[:, 1],
            z=coordinates[:, 2],
            i=triangles[:, 0],
            j=triangles[:, 1],
            k=triangles[:, 2],
            name=self.name,
            color=self.color,
        )


def CubesMesh(cubes, color=None, name=""):
    dim = sum(cubes[0][1])
    assert dim == 2

    return CubeMeshDrawer(cubes, color, name).graph_object()


def SimpleScene(xrange=None, yrange=None, zrange=None):
    """
    Returns a plotly's `graph_object.layout.Scene` object to remove x/y/z axes.

    You can use `xrange`/`yrange`/`zrange` to cut off the visualization area

    Args:
        xrange ((float, float) or None): The range of X axis to be visualized
        yrange ((float, float) or None): The range of Y axis to be visualized
        zrange ((float, float) or None): The range of Z axis to be visualized

    Returns:
        plotly.graph_objects.layout.Scene: Plotly's scene object
    """
    return go.layout.Scene(
        xaxis=dict(range=xrange, visible=False),
        yaxis=dict(range=yrange, visible=False),
        zaxis=dict(range=zrange, visible=False),
    )
