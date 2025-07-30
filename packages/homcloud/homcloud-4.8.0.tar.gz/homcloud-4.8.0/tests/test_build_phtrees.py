import io
import os

import pytest
import numpy as np
from unittest.mock import MagicMock

from homcloud.pdgm_format import PDGMReader, AlphaInformationChunk
from homcloud.alpha_filtration import AlphaFiltration
import homcloud.build_phtrees as build_phtrees

from tests.helper import get_pdgm_type

# birth-death pairs: (7, 10), (8, 9)
# tree: 9 -(8)-> 10 -(7)-> ∞
MAP1 = [
    [0, []],
    [0, []],
    [0, []],
    [0, []],  # 0, 1, 2, 3
    [1, [0, 1]],
    [1, [1, 2]],
    [1, [2, 3]],  # 4, 5, 6
    [1, [3, 0]],
    [1, [1, 3]],  # 7, 8
    [2, [4, 7, 8]],
    [2, [5, 6, 8]],  # 9, 10
]

# birth-death pairs: (7, 8), (9, 10)
# tree: 10 -(9)-> ∞ <-(7)- 8
MAP2 = [
    [0, []],
    [0, []],
    [0, []],
    [0, []],  # 0, 1, 2, 3
    [1, [0, 1]],
    [1, [1, 2]],
    [1, [2, 3]],  # 4, 5, 6
    [1, [1, 3]],
    [2, [5, 6, 7]],  # 7, 8
    [1, [0, 3]],
    [2, [4, 7, 9]],  # 9, 10
]


@pytest.mark.parametrize(
    "map, expected",
    [
        (MAP1, {4: [9], 5: [10], 6: [10], 7: [9], 8: [9, 10]}),
        (MAP2, {4: [10], 5: [8], 6: [8], 7: [8, 10], 9: [10]}),
    ],
)
def test_coboundary_map(map, expected):
    assert build_phtrees.coboundary_map(2, map) == expected


class TestPHTrees(object):
    @pytest.mark.parametrize(
        "map, expected_nodedata",
        [
            (MAP1, [(9, 8, 10), (10, 7, np.inf)]),
            (MAP2, [(10, 9, np.inf), (8, 7, np.inf)]),
        ],
    )
    def test_constructor(self, map, expected_nodedata):
        trees = build_phtrees.PHTrees(2, map)
        for death, birth, parent in expected_nodedata:
            assert trees.nodes[death].death_index == death
            assert trees.nodes[death].birth_index == birth
            assert trees.nodes[death].parent == parent

    @pytest.mark.parametrize(
        "map, expected",
        [
            (MAP1, [[8, 9, 10], [7, 10, np.inf]]),
            (MAP2, [[9, 10, np.inf], [7, 8, np.inf]]),
        ],
    )
    def test_to_list(self, map, expected):
        assert sorted(build_phtrees.PHTrees(2, map).to_list()) == sorted(expected)

    @pytest.mark.parametrize(
        "map, expected",
        [
            (MAP1, [(1, 8, 9), (1, 7, 10)]),
            (MAP2, [(1, 9, 10), (1, 7, 8)]),
        ],
    )
    def test_all_pairs(self, map, expected):
        assert sorted(build_phtrees.PHTrees(2, map).all_pairs()) == sorted(expected)

    def test_save_pdgm(self):
        filt = MagicMock(spec=AlphaFiltration)
        filt.periodicity = None
        filt.index_to_level = [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 3]
        filt.symbols = ["a", "b", "c", "d"]
        filt.points = np.array([[0, 0], [0.5, 1], [0, 2], [-0.5, 1]])
        filt.index_to_simplex = [[0], [1, 2]]
        filt.points_weighted = False
        filt.alpha_information_chunk.return_value = AlphaInformationChunk(4, None, False, True)
        tree = build_phtrees.PHTrees(2, MAP1)
        f = io.BytesIO()
        tree.save_pdgm(f, filt)
        f.seek(0)
        reader = PDGMReader(f)
        assert reader.metadata["dim"] == 2
        assert reader.metadata["filtration_type"] == "alpha-phtrees"
        assert reader.load_pd_chunk("pd", 0) == ([], [], [])
        assert reader.load_pd_chunk("pd", 1) == ([1], [3], [])
        assert reader.load_pd_chunk("indexed_pd", 1) == ([7], [10], [])
        assert reader.load_simple_chunk("allpairs", 1) == [[8, 9], [7, 10]]
        assert reader.load_simple_chunk("index_to_level") == filt.index_to_level
        assert reader.load_simple_chunk("vertex_symbols") == ["a", "b", "c", "d"]
        assert np.allclose(reader.load_simple_chunk("vertex_coordintes"), [[0, 0], [0.5, 1], [0, 2], [-0.5, 1]])
        assert reader.load_simple_chunk("index_to_simplex")
        assert reader.load_chunk("alpha_information") == {
            "chunktype": "alpha_information",
            "num_vertices": 4,
            "periodicity": None,
            "weighted": False,
            "squared": True,
        }
        assert reader.load_simple_chunk("phtrees") == [[8, 9, 10], [7, 10, np.inf]]


@pytest.mark.integration
class Test_main:
    def test_case(self, datadir, tmpdir):
        input = os.path.join(datadir, "tetragon.txt")
        output = str(tmpdir.join("tetragon.pdgm"))
        build_phtrees.main(
            build_phtrees.argument_parser().parse_args(
                [
                    "-d",
                    "2",
                    input,
                    output,
                ]
            )
        )
        assert get_pdgm_type(output) == "alpha-phtrees"
