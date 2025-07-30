import pytest
import numpy as np
import msgpack

from homcloud.geometry_resolver import (
    SimplicialResolver,
    PeriodicSimplicialResolver,
    AbstractResolver,
    CubicalResolver,
)
from homcloud.bitmap import Bitmap


def sort_cells(cells):
    return sorted(map(sorted, cells))


class TestSimplicialResolver(object):
    @pytest.fixture
    def resolver(self):
        vertex_symbols = ["P", "Q", "R", "S"]
        index_to_simplex = [[0], [1], [0, 1], [2], [1, 2], [2, 0], [0, 1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
        simplex_to_index = {tuple(sorted(simplex)): index for index, simplex in enumerate(index_to_simplex)}

        def boundary_map(index):
            simplex = index_to_simplex[index]
            return [simplex_to_index[tuple(simplex[:k] + simplex[k + 1 :])] for k in range(len(simplex))]

        return SimplicialResolver(index_to_simplex, vertex_symbols, boundary_map)

    @pytest.mark.parametrize(
        "cells, expected",
        [
            ([], []),
            ([0, 2], [["P"], ["P", "Q"]]),
        ],
    )
    def test_resovle_cells(self, resolver, cells, expected):
        assert resolver.resolve_cells(cells) == expected

    @pytest.mark.parametrize(
        "cells, expected",
        [
            ([], []),
            ([0, 2], ["P", "Q"]),
            ([0, 3, 6], ["P", "Q", "R"]),
        ],
    )
    def test_resolve_vertices(self, resolver, cells, expected):
        assert set(resolver.resolve_vertices(cells)) == set(expected)

    @pytest.mark.parametrize("cells, expected", [([], []), ([2, 4], [0, 3]), ([2, 4, 5], []), ([6, 10], [2, 5, 8, 9])])
    def test_boundary_cells(self, resolver, cells, expected):
        assert set(resolver.boundary_cells(cells)) == set(expected)

    @pytest.mark.parametrize(
        "cells, expected",
        [
            ([], []),
            ([2, 4], [["P"], ["R"]]),
            ([2, 4, 5], []),
            ([10], [["Q", "R"], ["R", "S"], ["S", "Q"]]),
            ([6, 10], [["P", "Q"], ["P", "R"], ["Q", "S"], ["R", "S"]]),
        ],
    )
    def test_resolve_boundary(self, resolver, cells, expected):
        assert sort_cells(resolver.resolve_boundary(cells)) == sort_cells(expected)

    @pytest.mark.parametrize(
        "cells, expected",
        [
            ([], []),
            ([2, 4], ["P", "R"]),
            ([2, 4, 5], []),
            ([10], ["Q", "R", "S"]),
            ([6, 10], ["P", "Q", "R", "S"]),
        ],
    )
    def test_resolve_boundary_vertices(self, resolver, cells, expected):
        assert sorted(resolver.resolve_boundary_vertices(cells)) == sorted(expected)

    def test_centroid(self):
        resolver = SimplicialResolver([[0, 1, 2]], [[0, 0], [1, 1], [0, 1]], None)
        assert np.allclose(resolver.centroid(0), [1.0 / 3, 2.0 / 3])

    def test_resolve_boundary_loop(self, resolver):
        assert resolver.resolve_boundary_loop([6]) == ["Q", "P", "R"]
        assert resolver.resolve_boundary_loop([6, 10]) == ["Q", "P", "R", "S"]


class TestPeriodicSimplicialResolver:
    @staticmethod
    def resolver(boundary_ratio):
        simplices = [[0], [1], [2], [3], [0, 1], [1, 2], [2, 0], [0, 3]]
        vertices = [[0.5, 1.5, 0.5], [1.5, 2.5, 1.5], [2.5, 3.5, 2.5], [1.5, 3.5, 0.7]]
        boundary_map = [[], [], [], [], [0, 1], [1, 2], [2, 0], [0, 3]]
        periodicity = [[0, 3], [1, 4], [0, 3]]
        return PeriodicSimplicialResolver(simplices, vertices, lambda n: boundary_map[n], periodicity, boundary_ratio)

    @pytest.mark.parametrize(
        "pbc, cell_index, expected",
        [
            ((0.1, 0.0), 0, [[0.5, 1.5, 0.5]]),
            ((0.3, 0.0), 0, [[0.5, 1.5, 0.5]]),
            ((0.1, 0.0), 7, [[0.5, 1.5, 0.5], [1.5, 3.5, 0.7]]),
            ((0.3, 0.0), 7, [[0.5, 4.5, 0.5], [1.5, 3.5, 0.7]]),
            ((0.1, 0.0), 6, [[2.5, 3.5, 2.5], [0.5, 1.5, 0.5]]),
            ((0.3, 0.0), 6, [[2.5, 3.5, 2.5], [3.5, 4.5, 3.5]]),
        ],
    )
    def test_resolve_cell(self, pbc, cell_index, expected):
        assert self.resolver(pbc).resolve_cell(cell_index) == expected

    @pytest.mark.parametrize(
        "pbc, cell_indices, expected",
        [
            ((0.1, None), [0], [[[0.5, 1.5, 0.5]]]),
            ((0.3, None), [0], [[[0.5, 1.5, 0.5]]]),
            ((0.1, None), [7], [[[0.5, 1.5, 0.5], [1.5, 3.5, 0.7]]]),
            ((0.3, None), [7], [[[0.5, 4.5, 0.5], [1.5, 3.5, 0.7]]]),
            ((0.3, 0.0), [7], [[[0.5, 4.5, 0.5], [1.5, 3.5, 0.7]], [[0.5, 1.5, 0.5], [1.5, 0.5, 0.7]]]),
            ((0.3, 0.3), [7], [[[0.5, 4.5, 0.5], [1.5, 3.5, 0.7]], [[0.5, 1.5, 0.5], [1.5, 0.5, 0.7]]]),
            ((0.3, -0.3), [7], [[[0.5, 4.5, 0.5], [1.5, 3.5, 0.7]]]),
            ((0.1, None), [6], [[[2.5, 3.5, 2.5], [0.5, 1.5, 0.5]]]),
            ((0.3, None), [6], [[[2.5, 3.5, 2.5], [3.5, 4.5, 3.5]]]),
            (
                (0.3, 0.3),
                [6],
                [
                    [[2.5, 3.5, 2.5], [3.5, 4.5, 3.5]],
                    [[2.5, 3.5, -0.5], [3.5, 4.5, 0.5]],
                    [[2.5, 0.5, 2.5], [3.5, 1.5, 3.5]],
                    [[2.5, 0.5, -0.5], [3.5, 1.5, 0.5]],
                    [[-0.5, 3.5, 2.5], [0.5, 4.5, 3.5]],
                    [[-0.5, 3.5, -0.5], [0.5, 4.5, 0.5]],
                    [[-0.5, 0.5, 2.5], [0.5, 1.5, 3.5]],
                    [[-0.5, 0.5, -0.5], [0.5, 1.5, 0.5]],
                ],
            ),
        ],
    )
    def test_resolve_cells(self, pbc, cell_indices, expected):
        assert self.resolver(pbc).resolve_cells(cell_indices) == expected


class TestAbstractResolver(object):
    @pytest.fixture
    def resolver(self):
        index_to_symbol = ["A", "B", "AB", "C", "AC", "BC", "ABC"]
        boundary_map = [[], [], [1, 0], [], [0, 3], [1, 3], [2, 4, 5]]
        return AbstractResolver(index_to_symbol, lambda n: boundary_map[n])

    @pytest.mark.parametrize(
        "cell, expected",
        [
            (2, "AB"),
            (1, "B"),
        ],
    )
    def test_resolve_cell(self, resolver, cell, expected):
        assert resolver.resolve_cell(cell) == expected

    @pytest.mark.parametrize(
        "cells, expected",
        [
            ([0, 1], []),
            ([2, 4, 5], []),
            ([2, 4], ["B", "C"]),
            ([6], ["AB", "AC", "BC"]),
        ],
    )
    def test_resolve_boundary(self, resolver, cells, expected):
        assert sorted(resolver.resolve_boundary(cells)) == expected


class TestCubicalResolver(object):
    @pytest.fixture
    def c2i_resolver(self):
        bitmap = Bitmap(np.random.uniform(size=(3, 3, 3)), save_boundary_map=True)
        filt = bitmap.build_cubical_filtration()
        _, boundary_map_byte_sequence = filt.compute_pairs()
        boundary_map = msgpack.loads(boundary_map_byte_sequence, raw=False)
        sorted_cubes = filt.cubefilt_ext.sorted_cubes
        cube_to_index = {cube: index for (index, cube) in enumerate(sorted_cubes)}

        def coord_to_index(coord, nondeg):
            return cube_to_index[filt.encode_cube(coord, nondeg)]

        return (coord_to_index, CubicalResolver([3, 3, 3], sorted_cubes, lambda i: boundary_map["map"][i][1]))

    @pytest.mark.parametrize(
        "coord, nondeg",
        [
            ([0, 0, 0], [0, 0, 0]),
            ([2, 0, 1], [0, 1, 1]),
            ([1, 1, 1], [1, 1, 1]),
        ],
    )
    def test_resolve_cell(self, c2i_resolver, coord, nondeg):
        coord_to_index, resolver = c2i_resolver
        index = coord_to_index(coord, nondeg)
        assert resolver.resolve_cell(index) == (coord, nondeg)

    @pytest.mark.parametrize(
        "cubes, expected",
        [
            ([], []),
            ([([0, 0, 0], [0, 0, 1])], [([0, 0, 0], [0, 0, 0]), ([0, 0, 1], [0, 0, 0])]),
            ([([0, 0, 0], [0, 0, 1]), ([0, 0, 1], [0, 0, 1])], [([0, 0, 0], [0, 0, 0]), ([0, 0, 2], [0, 0, 0])]),
            (
                [([0, 0, 0], [0, 1, 1]), ([0, 0, 1], [1, 1, 0])],
                [
                    ([0, 0, 0], [0, 0, 1]),
                    ([0, 0, 0], [0, 1, 0]),
                    ([0, 1, 0], [0, 0, 1]),
                    ([0, 0, 1], [1, 0, 0]),
                    ([0, 1, 1], [1, 0, 0]),
                    ([1, 0, 1], [0, 1, 0]),
                ],
            ),
        ],
    )
    def test_resolve_boundary(self, c2i_resolver, cubes, expected):
        coord_to_index, resolver = c2i_resolver
        cube_indices = [coord_to_index(*c) for c in cubes]
        assert sorted(resolver.resolve_boundary(cube_indices)) == sorted(expected)

    @pytest.mark.parametrize(
        "cubes, expected",
        [
            ([], []),
            ([([0, 0, 0], [0, 0, 1])], [[0, 0, 0], [0, 0, 1]]),
            ([([0, 0, 0], [0, 0, 1]), ([0, 0, 1], [0, 0, 1])], [[0, 0, 0], [0, 0, 2]]),
            (
                [([0, 0, 0], [0, 1, 1]), ([0, 0, 1], [1, 1, 0])],
                [[0, 0, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 0, 1], [0, 0, 1]],
            ),
        ],
    )
    def test_resolve_boundary_vertices(self, c2i_resolver, cubes, expected):
        coord_to_index, resolver = c2i_resolver
        cube_indices = [coord_to_index(*c) for c in cubes]
        assert sorted(resolver.resolve_boundary_vertices(cube_indices)) == sorted(expected)

    @pytest.mark.parametrize(
        "cubes, expected",
        [
            ([], []),
            ([([0, 0, 0], [0, 0, 0])], [[0, 0, 0]]),
            ([([0, 0, 0], [0, 1, 0])], [[0, 0, 0], [0, 1, 0]]),
            ([([0, 0, 0], [0, 1, 0]), ([0, 1, 0], [1, 0, 0])], [[0, 0, 0], [0, 1, 0], [1, 1, 0]]),
            (
                [([0, 0, 0], [1, 1, 1])],
                [
                    [0, 0, 0],
                    [0, 0, 1],
                    [0, 1, 0],
                    [0, 1, 1],
                    [1, 0, 0],
                    [1, 0, 1],
                    [1, 1, 0],
                    [1, 1, 1],
                ],
            ),
        ],
    )
    def test_resolve_vertices(self, c2i_resolver, cubes, expected):
        coord_to_index, resolver = c2i_resolver
        cube_indices = [coord_to_index(*c) for c in cubes]
        assert sorted(resolver.resolve_vertices(cube_indices)) == expected

    def test_centroid(self, c2i_resolver):
        coord_to_index, resolver = c2i_resolver
        cube_index = coord_to_index([0, 2, 1], [1, 0, 0])
        assert np.allclose(resolver.centroid(cube_index), [0.5, 2.0, 1.0])
