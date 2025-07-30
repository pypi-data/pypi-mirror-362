from unittest.mock import MagicMock
import os

import numpy as np
import pytest

import homcloud.phtrees as phtrees
import homcloud.geometry_resolver as geom_resolver
import homcloud.interface as hc
from homcloud.spatial_searcher import SpatialSearcher


NODES1 = [[8, 9, 10], [7, 10, np.inf]]
INDEX_TO_LEVEL = {7: 1.0, 8: 2.0, 9: 2.0, 10: 3.0}
INDEX_TO_SIMPLEX = {
    4: [0, 1],
    5: [1, 2],
    6: [2, 3],
    7: [0, 3],
    8: [1, 3],
    9: [0, 1, 3],
    10: [1, 2, 3],
}
VERTEX_SYMBOLS = ["X", "Y", "Z", "U"]
VERTEX_COORDINATES = [[0, 0], [1, 0.5], [2, 0], [1, -0.5]]


@pytest.fixture
def trees1():
    def boundary_map(index):
        if index == 9:
            return [4, 7, 8]
        if index == 10:
            return [5, 6, 8]

    coord_resolver = geom_resolver.SimplicialResolver(INDEX_TO_SIMPLEX, VERTEX_COORDINATES, boundary_map)
    symbol_resolver = geom_resolver.SimplicialResolver(INDEX_TO_SIMPLEX, VERTEX_SYMBOLS, boundary_map)

    return phtrees.PHTrees(NODES1, INDEX_TO_LEVEL, coord_resolver, symbol_resolver)


class TestPHTrees(object):
    class Test_nodes(object):
        def test_case_MAP1(self):
            trees = phtrees.PHTrees(NODES1)
            assert len(trees.nodes) == 2
            trees.nodes[9].birth_index == 8
            trees.nodes[9].death_index == 9
            trees.nodes[9].parent_death == 10

    def test_parent_of(self):
        trees = phtrees.PHTrees(NODES1)
        parent = trees.parent_of(trees.nodes[9])
        assert parent.birth_index == 7
        assert trees.parent_of(parent) is None


class TestNode(object):
    @pytest.fixture
    def node(self, trees1):
        return phtrees.Node(7, 10, np.inf, trees1)

    def test_birth_time(self, node):
        assert node.birth_time() == 1.0

    def test_death_time(self, node):
        assert node.death_time() == 3.0

    def test_lifetime(self, node):
        assert node.lifetime() == 2.0

    def test_birth_simplex(self, node):
        assert sorted(node.birth_simplex()) == sorted([[0, 0], [1, -0.5]])

    def test_death_simplex(self, node):
        assert sorted(node.death_simplex()) == sorted([[1, 0.5], [2, 0], [1, -0.5]])

    def test_birth_simplex_by_symbols(self, node):
        assert sorted(node.birth_simplex("symbols")) == sorted(["X", "U"])

    def test_death_simplex_by_symbols(self, node):
        assert sorted(node.death_simplex("symbols")) == sorted(["Y", "Z", "U"])

    def test_volume_nodes(self, trees1):
        assert trees1.nodes[9].volume_nodes == [trees1.nodes[9]]
        assert trees1.nodes[10].volume_nodes == [trees1.nodes[10], trees1.nodes[9]]

    def test_boundary(self, trees1):
        assert sorted(trees1.nodes[10].boundary("symbols")) == sorted([["X", "Y"], ["Y", "Z"], ["Z", "U"], ["X", "U"]])

    def test_boundary_vertices(self, trees1):
        node = trees1.nodes[10]
        assert sorted(node.boundary_vertices("symbols")) == sorted(
            [
                "X",
                "Y",
                "Z",
                "U",
            ]
        )

    def test_vertices(self, trees1):
        node = trees1.nodes[10]
        assert sorted(node.vertices("symbols")) == sorted(
            [
                "X",
                "Y",
                "Z",
                "U",
            ]
        )

    def test_simplices(self, trees1):
        node = trees1.nodes[10]
        assert sorted(node.simplices("symbols")) == sorted(
            [
                ["X", "Y", "U"],
                ["Y", "Z", "U"],
            ]
        )

    def test_stable_volume(self, trees1):
        node = trees1.nodes[10]
        assert isinstance(node.stable_volume(0.1), phtrees.StableVolume)
        assert node.stable_volume(0.1).volume_nodes == [trees1.nodes[10], trees1.nodes[9]]
        assert node.stable_volume(1.1).volume_nodes == [trees1.nodes[10]]

    def test_to_dict(self, trees1):
        node = trees1.nodes[10]
        dict = node.to_dict()
        assert sorted(dict.keys()) == sorted(
            [
                "birth-index",
                "death-index",
                "birth-time",
                "death-time",
                "boundary",
                "boundary-by-symbols",
                "boundary-vertices",
                "boundary-vertices-by-symbols",
                "vertices",
                "vertices-by-symbols",
                "simplices",
                "simplices-by-symbols",
                "children",
            ]
        )
        assert dict["birth-index"] == 7
        assert dict["death-index"] == 10
        assert dict["birth-time"] == 1.0
        assert dict["death-time"] == 3.0

        assert sorted(dict["boundary"]) == sorted(
            [[[0, 0], [1, 0.5]], [[1, 0.5], [2, 0]], [[2, 0], [1, -0.5]], [[0, 0], [1, -0.5]]]
        )
        assert sorted(dict["boundary-by-symbols"]) == sorted([["X", "Y"], ["Y", "Z"], ["Z", "U"], ["X", "U"]])

        assert sorted(dict["boundary-vertices"]) == sorted([[0, 0], [1, 0.5], [2, 0], [1, -0.5]])
        assert sorted(dict["boundary-vertices-by-symbols"]) == sorted(
            [
                "X",
                "Y",
                "Z",
                "U",
            ]
        )

        assert sorted(dict["vertices"]) == sorted([[0, 0], [1, 0.5], [2, 0], [1, -0.5]])
        assert sorted(dict["vertices-by-symbols"]) == sorted(
            [
                "X",
                "Y",
                "Z",
                "U",
            ]
        )

        assert sorted(dict["simplices"]) == sorted(
            [
                [[0, 0], [1, 0.5], [1, -0.5]],
                [[1, 0.5], [2, 0], [1, -0.5]],
            ]
        )
        assert sorted(dict["simplices-by-symbols"]) == sorted(
            [
                ["X", "Y", "U"],
                ["Y", "Z", "U"],
            ]
        )

        assert dict["children"] == [
            {
                "birth-index": 8,
                "death-index": 9,
                "birth-time": 2.0,
                "death-time": 2.0,
                "children": [],
            }
        ]


class TestPointQuery(object):
    @pytest.fixture
    def spatial_searcher(self):
        spatial_searcher = MagicMock(spec=SpatialSearcher)
        spatial_searcher.nearest_pair.return_value = 10
        return spatial_searcher

    def test_query(self, trees1, spatial_searcher):
        query = phtrees.PointQuery((1.1, 3.1), phtrees.GetOptimalVolume(trees1), spatial_searcher)
        query.invoke()

        spatial_searcher.nearest_pair.assert_called_with(1.1, 3.1)
        assert query.result == [trees1.nodes[10]]

    def test_to_dict(self, trees1, spatial_searcher):
        query = phtrees.PointQuery((1.1, 3.1), phtrees.GetOptimalVolume(trees1), spatial_searcher, 3)

        assert query.to_dict() == {
            "format-version": 2,
            "query": {
                "query-type": "signle",
                "query-target": "optimal-volume",
                "degree": 2,
                "birth": 1.1,
                "death": 3.1,
                "ancestor-pairs": False,
                "query-children": False,
            },
            "dimension": 3,
            "result": [],
        }


@pytest.mark.integration
class Test_main(object):
    def build_alpha_pdgm(self, path):
        hc.PDList.from_alpha_filtration(
            np.array([[0, 0], [1, 0.6], [2.0001, 0.000], [1.001, -0.6]]),
            save_to=path,
            save_boundary_map=True,
            save_phtrees=True,
        )

    def test_case_point_query(self, tmpdir):
        path = str(tmpdir.join("four_points.pdgm"))
        json = str(tmpdir.join("four_points.json"))
        self.build_alpha_pdgm(path)
        phtrees.main(phtrees.argument_parser().parse_args(["-x", "0.34", "-y", "0.46", path, "-j", json]))
        assert os.path.exists(json)
        # import subprocess
        # subprocess.run(["cat", json], check=True)

    def test_case_rectangle_query(self, tmpdir):
        path = str(tmpdir.join("four_points.pdgm"))
        json = str(tmpdir.join("four_points.json"))
        self.build_alpha_pdgm(path)
        phtrees.main(phtrees.argument_parser().parse_args(["-X", "0.3:0.5", "-Y", "0.3:0.5", path, "-j", json]))
        assert os.path.exists(json)
