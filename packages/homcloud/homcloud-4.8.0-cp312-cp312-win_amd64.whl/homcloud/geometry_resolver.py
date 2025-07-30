import numbers
import itertools
from collections import defaultdict

import numpy as np

from homcloud.cubical_ext import CubeEncoder
from cached_property import cached_property


class GeometryResolverBase(object):
    def boundary_cells(self, cell_indices):
        ret = set()
        for cell_index in cell_indices:
            for b in self.boundary_map(cell_index):
                if b in ret:
                    ret.remove(b)
                else:
                    ret.add(b)
        return ret

    def resolve_cells(self, cell_indices):
        return list(map(self.resolve_cell, cell_indices))

    def resolve_boundary(self, cell_indices):
        return self.resolve_cells(self.boundary_cells(cell_indices))

    def resolve_boundary_vertices(self, cell_indices):
        return self.resolve_vertices(self.boundary_cells(cell_indices))

    def resolve_boundary_loop(self, cell_indices):
        if self.cell_dim(cell_indices[0]) != 2:
            raise ValueError("resolve_boundary_loop is only applicable to 2-d cells")

        edges = [self.boundary_map(b) for b in self.boundary_cells(cell_indices)]
        if len(edges) <= 2:
            return ValueError("resolve_boundary_loop is not applicable to a self-loop and multi-edge")

        adj = defaultdict(list)
        for edge in edges:
            adj[edge[0]].append(edge[1])
            adj[edge[1]].append(edge[0])

        prev, curr = edges[0]
        path = [prev]

        while True:
            path.append(curr)
            curr, prev = (adj[curr][1], curr) if adj[curr][0] == prev else (adj[curr][0], curr)
            if path[0] == curr:
                break

        if len(path) != len(edges):
            return None

        return list(itertools.chain.from_iterable(self.resolve_cells(path)))


class SimplicialResolverBase(GeometryResolverBase):
    def __init__(self, index_to_simplex, vertices, boundary_map):
        self.index_to_simplex = index_to_simplex
        self.vertices = vertices
        self.boundary_map = boundary_map

    def resolve_vertices(self, cell_indices):
        vertices = []
        for cell_index in cell_indices:
            for vertex in self.index_to_simplex[cell_index]:
                vertices.append(vertex)

        return [self.vertices[v] for v in set(vertices)]

    def centroid(self, cell_index):
        return np.mean(self.resolve_cell(cell_index), axis=0)

    def cell_dim(self, cell):
        return len(self.index_to_simplex[cell]) - 1


class SimplicialResolver(SimplicialResolverBase):
    def resolve_cell(self, cell_index):
        return [self.vertices[i] for i in self.index_to_simplex[cell_index]]


class PeriodicSimplicialResolver(SimplicialResolverBase):
    def __init__(self, index_to_simplex, vertices, boundary_map, periodicity, adjust_periodic_boundary):
        super().__init__(index_to_simplex, vertices, boundary_map)
        self.ndim = len(periodicity)
        self.periodicity = np.array(periodicity)
        boundary_ratio, boundary_mirror_ratio = adjust_periodic_boundary
        self.setup_boundary_thresholds(boundary_ratio)
        self.setup_mirror_thresholds(boundary_mirror_ratio)

    def setup_boundary_thresholds(self, boundary_ratio):
        if isinstance(boundary_ratio, numbers.Real):
            r = boundary_ratio
        else:
            boundary_ratio = np.array(boundary_ratio)
            r = boundary_ratio[0, 0]
            assert np.allclose([[r, 1 - r], [r, 1 - r], [r, 1 - r]], boundary_ratio)

        d = self.periodicity[:, 1] - self.periodicity[:, 0]
        assert np.all(d > 0)
        self.min_boundary_thresholds = self.periodicity[:, 0] + r * d
        self.max_boundary_thresholds = self.periodicity[:, 1] - r * d

    def setup_mirror_thresholds(self, mirror_ratio):
        if mirror_ratio is None:
            self.mirror_thresholds = None
        else:
            self.mirror_thresholds = self.periodicity[:, 1] - mirror_ratio * self.widths

    @cached_property
    def widths(self):
        return self.periodicity[:, 1] - self.periodicity[:, 0]

    def resolve_cell(self, cell_index):
        inbox_vertices = np.array([self.vertices[i] for i in self.index_to_simplex[cell_index]])
        for k in range(self.ndim):
            in_lower = inbox_vertices[:, k] < self.min_boundary_thresholds[k]
            in_upper = inbox_vertices[:, k] > self.max_boundary_thresholds[k]
            if np.any(in_lower) and np.any(in_upper):
                inbox_vertices[in_lower, k] += self.periodicity[k, 1] - self.periodicity[k, 0]

        return inbox_vertices.tolist()

    def resolve_cells(self, cell_indices):
        def mirrors(axes):
            return itertools.product(*[(0, -1) if r else (0,) for r in axes])

        cells = super().resolve_cells(cell_indices)
        if self.mirror_thresholds is None:
            return cells
        vertices = np.array(list(itertools.chain.from_iterable(cells)))
        mirror_axes = np.max(vertices, axis=0) > self.periodicity[:, 1]

        ret = []
        for cell in cells:
            cell_mirror_axis = np.max(cell, axis=0) > self.mirror_thresholds
            for m in mirrors(mirror_axes & cell_mirror_axis):
                ret.append((np.array(cell) + np.array(m) * self.widths).tolist())
        return ret


class CubicalResolver(GeometryResolverBase):
    def __init__(self, shape, index_to_cube, boundary_map):
        self.shape = shape
        self.cube_encoder = CubeEncoder(shape)
        self.index_to_cube = index_to_cube
        self.boundary_map = boundary_map

    @property
    def ndim(self):
        return len(self.shape)

    def resolve_cell(self, cell_index):
        return self.cube_encoder.decode_cube(self.index_to_cube[cell_index])

    def resolve_vertices(self, cell_indices):
        ret = set()

        def vertices_of_cube(cube_index):
            coord, nondeg = self.cube_encoder.decode_cube(self.index_to_cube[cube_index])

            def iter(k):
                if k == self.ndim:
                    ret.add(tuple(coord))
                    return
                if nondeg[k]:
                    iter(k + 1)
                    coord[k] += 1
                    iter(k + 1)
                    coord[k] -= 1
                else:
                    iter(k + 1)

            iter(0)
            return ret

        for cube_index in cell_indices:
            vertices_of_cube(cube_index)

        return [list(vertex) for vertex in ret]

    def centroid(self, cell_index):
        coord, nondeg = self.decode_index(cell_index)
        return np.array(coord) + np.array(nondeg) / 2.0

    def decode_index(self, index):
        return self.cube_encoder.decode_cube(self.index_to_cube[index])


class AbstractResolver(GeometryResolverBase):
    def __init__(self, index_to_symbol, boundary_map):
        self.index_to_symbol = index_to_symbol
        self.boundary_map = boundary_map

    def resolve_cell(self, cell_index):
        return self.index_to_symbol[cell_index]


class BitmapResolver(GeometryResolverBase):
    def __init__(self, index_to_pixel):
        self.index_to_pixel = index_to_pixel

    def resolve_cell(self, cell_index):
        return self.index_to_pixel[cell_index]

    @property
    def boundary_map(self):
        raise RuntimeError("boundary is not implemented in bitmap")


class RipsResolver:
    def __init__(self, vertices):
        self.vertices = vertices

    def resolve_graph_path(self, path):
        return [self.vertices[i] for i in path]
