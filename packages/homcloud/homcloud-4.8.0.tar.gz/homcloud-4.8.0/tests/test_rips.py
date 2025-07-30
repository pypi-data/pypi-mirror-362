import io
import os

from scipy.spatial import distance_matrix
import numpy as np
import pytest

import homcloud.rips as rips
from homcloud.rips import DistanceMatrix
from homcloud.pdgm_format import PDGMReader
from tests.helper import get_pdgm_type


TETRAGON = np.array([[0, 0], [3, 5], [6, 0], [2, -4]])
DISTANEC_MATRIX = distance_matrix(TETRAGON, TETRAGON)


class TestDistanceMatrix(object):
    @pytest.mark.parametrize(
        "upper_dim, upper_value, matrix, expected",
        [
            (
                1,
                np.inf,
                np.array(
                    [
                        [0.0],
                    ]
                ),
                [(0.0, (0,))],
            ),
            (
                1,
                np.inf,
                np.array(
                    [
                        [0, 2, 3],
                        [2, 0, 4],
                        [3, 4, 0],
                    ],
                    dtype=float,
                ),
                [
                    (0.0, (0,)),
                    (0.0, (1,)),
                    (0.0, (2,)),
                    (2.0, (0, 1)),
                    (3.0, (0, 2)),
                    (4.0, (1, 2)),
                    (4.0, (0, 1, 2)),
                ],
            ),
            (
                0,
                np.inf,
                np.array(
                    [
                        [0, 2, 3],
                        [2, 0, 4],
                        [3, 4, 0],
                    ],
                    dtype=float,
                ),
                [
                    (0.0, (0,)),
                    (0.0, (1,)),
                    (0.0, (2,)),
                    (2.0, (0, 1)),
                    (3.0, (0, 2)),
                    (4.0, (1, 2)),
                ],
            ),
            (
                1,
                3.5,
                np.array(
                    [
                        [0, 2, 3],
                        [2, 0, 4],
                        [3, 4, 0],
                    ],
                    dtype=float,
                ),
                [
                    (0.0, (0,)),
                    (0.0, (1,)),
                    (0.0, (2,)),
                    (2.0, (0, 1)),
                    (3.0, (0, 2)),
                ],
            ),
            (
                2,
                np.inf,
                np.array(
                    [
                        [0, 3, 4, 5, np.inf],
                        [3, 0, 2, 6, np.inf],
                        [4, 2, 0, 7, 4.5],
                        [5, 6, 7, 0, np.inf],
                        [np.inf, np.inf, 4.5, np.inf, 0],
                    ],
                    dtype=float,
                ),
                [
                    (0.0, (0,)),
                    (0.0, (1,)),
                    (0.0, (2,)),
                    (0.0, (3,)),
                    (0.0, (4,)),
                    (2.0, (1, 2)),
                    (3.0, (0, 1)),
                    (4.0, (0, 2)),
                    (4.5, (2, 4)),
                    (5.0, (0, 3)),
                    (6.0, (1, 3)),
                    (7.0, (2, 3)),
                    (4.0, (0, 1, 2)),
                    (6.0, (0, 1, 3)),
                    (7.0, (0, 2, 3)),
                    (7.0, (1, 2, 3)),
                    (7.0, (0, 1, 2, 3)),
                ],
            ),
            (
                2,
                5.5,
                np.array(
                    [
                        [0, 3, 4, 5, np.inf],
                        [3, 0, 2, 6, np.inf],
                        [4, 2, 0, 7, 4.5],
                        [5, 6, 7, 0, np.inf],
                        [np.inf, np.inf, 4.5, np.inf, 0],
                    ],
                    dtype=float,
                ),
                [
                    (0.0, (0,)),
                    (0.0, (1,)),
                    (0.0, (2,)),
                    (0.0, (3,)),
                    (0.0, (4,)),
                    (2.0, (1, 2)),
                    (3.0, (0, 1)),
                    (4.0, (0, 2)),
                    (4.5, (2, 4)),
                    (5.0, (0, 3)),
                    (4.0, (0, 1, 2)),
                ],
            ),
        ],
    )
    def test_all_simpliecs(self, upper_value, upper_dim, matrix, expected):
        simplices = DistanceMatrix(matrix, upper_dim, upper_value).all_simplices()
        assert sorted(simplices) == sorted(expected)

    def test_build_simplicial_filtration(self):
        matrix = np.array(
            [
                [0, 2, 3],
                [2, 0, 4],
                [3, 4, 0],
            ],
            dtype=float,
        )
        distance_matrix = DistanceMatrix(matrix, 2, np.inf)
        filt = distance_matrix.build_simplicial_filtration()
        assert filt.index_to_level == [0.0, 0.0, 0.0, 2.0, 3.0, 4.0, 4.0]
        assert filt.index_to_simplex == [
            (0,),
            (1,),
            (2,),
            (0, 1),
            (0, 2),
            (1, 2),
            (0, 1, 2),
        ]
        assert filt.simplex_to_index == {
            (0,): 0,
            (1,): 1,
            (2,): 2,
            (0, 1): 3,
            (0, 2): 4,
            (1, 2): 5,
            (0, 1, 2): 6,
        }
        assert filt.vertex_symbols == ["0", "1", "2"]
        assert filt.boundary_map == [
            [0, []],
            [0, []],
            [0, []],
            [1, [1, 0]],
            [1, [2, 0]],
            [1, [2, 1]],
            [2, [5, 4, 3]],
        ]


class TestRipsFiltration(object):
    class Test_compute_pdgm:
        @pytest.mark.parametrize(
            "algorithm, save_graph, save_cocycle",
            [
                pytest.param("dipha", False, False, marks=pytest.mark.dipha),
                pytest.param("dipha", True, False, marks=pytest.mark.dipha),
                ("ripser", False, False),
                ("ripser", True, False),
                (None, False, False),
                ("ripser", True, True),
            ],
        )
        def test_without_upper_value(self, algorithm, save_graph, save_cocycle):
            rips = DistanceMatrix(DISTANEC_MATRIX, 2).build_rips_filtration(save_graph, save_cocycle)
            f = io.BytesIO()
            rips.compute_pdgm(f, algorithm)
            f.seek(0)
            reader = PDGMReader(f)

            assert reader.filtration_type == "rips"
            assert reader.metadata["dim"] == 3
            assert not reader.metadata["sign_flipped"]

            births, deaths, ess_births = reader.load_pd_chunk("pd", 0)
            assert births == [0, 0, 0]
            assert np.allclose(deaths, np.sqrt([20, 32, 34]))
            assert ess_births == [0]

            births, deaths, ess_births = reader.load_pd_chunk("pd", 1)
            assert np.allclose(births, [np.sqrt(34)])
            assert deaths == [6]
            assert ess_births == []

            births, deaths, ess_births = reader.load_pd_chunk("pd", 2)
            assert births == []
            assert deaths == []
            assert ess_births == []

            assert reader.load_pd_chunk("indexed_pd", 0) == (None, None, None)
            assert reader.load_pd_chunk("indexed_pd", 1) == (None, None, None)
            assert reader.load_pd_chunk("indexed_pd", 2) == (None, None, None)

            assert reader.load_chunk("rips_information") == {"chunktype": "rips_information", "num_vertices": 4}

            graph_weights = reader.load_chunk("graph_weights")
            if save_graph:
                assert graph_weights["num_vertices"] == 4
                assert len(graph_weights["weights"]) == 6
            else:
                assert graph_weights is None

            if save_cocycle:
                assert reader.load_simple_chunk("cocycles", 0) == []
                assert reader.load_simple_chunk("cocycles", 1) == [[[1, 0, 1]]]
                assert reader.load_simple_chunk("cocycles", 2) == []
                assert reader.load_simple_chunk("cocycles", 3) is None

        @pytest.mark.parametrize(
            "algorithm",
            [
                pytest.param("dipha", marks=pytest.mark.dipha),
                "ripser",
            ],
        )
        def test_with_upper_value(self, algorithm):
            rips = DistanceMatrix(DISTANEC_MATRIX, 2, np.sqrt(33)).build_rips_filtration(False, False)
            f = io.BytesIO()
            rips.compute_pdgm(f, algorithm)
            f.seek(0)
            reader = PDGMReader(f)

            births, deaths, ess_births = reader.load_pd_chunk("pd", 0)
            assert births == [0, 0]
            assert np.allclose(deaths, np.sqrt([20, 32]))
            assert ess_births == [0, 0]

            births, deaths, ess_births = reader.load_pd_chunk("pd", 1)
            assert births == []
            assert deaths == []
            assert ess_births == []

            births, deaths, ess_births = reader.load_pd_chunk("pd", 2)
            assert births == []
            assert deaths == []
            assert ess_births == []


class TestSimplicialFiltration(object):
    class Test_compute_pdgm(object):
        @pytest.mark.parametrize("save_bm", [True, False])
        def test_case_tetragon(self, save_bm):
            simplicial = DistanceMatrix(DISTANEC_MATRIX, 2).build_simplicial_filtration(save_bm)
            f = io.BytesIO()
            simplicial.compute_pdgm(f, None)
            f.seek(0)
            reader = PDGMReader(f)

            assert reader.metadata["filtration_type"] == "simplicial"
            assert reader.metadata["dim"] == 3
            assert not reader.metadata["sign_flipped"]

            births, deaths, ess_births = reader.load_pd_chunk("pd", 0)
            assert births == [0, 0, 0]
            assert np.allclose(deaths, np.sqrt([20, 32, 34]))
            assert ess_births == [0]
            births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 0)
            assert births == [3, 2, 1]
            assert deaths == [4, 5, 6]
            assert ess_births == [0]

            births, deaths, ess_births = reader.load_pd_chunk("pd", 1)
            assert np.allclose(births, [np.sqrt(34)])
            assert deaths == [6]
            assert ess_births == []
            births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 1)
            assert births == [7]
            assert deaths == [10]
            assert ess_births == []

            births, deaths, ess_births = reader.load_pd_chunk("pd", 2)
            assert births == []
            assert deaths == []
            assert ess_births == []

            births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 2)
            assert births == []
            assert deaths == []
            assert ess_births == []

            assert reader.load_simple_chunk("allpairs", 0) == [[3, 4], [2, 5], [1, 6], [0, None]]
            assert reader.load_simple_chunk("allpairs", 1) == [
                [8, 9],
                [7, 10],
                [11, 12],
            ]
            assert reader.load_simple_chunk("allpairs", 2) == [[13, 14]]
            assert len(reader.load_simple_chunk("index_to_level")) == 15
            # 14 = 4 + 4*3/2 + 4*3*2/6 + 1

            assert len(reader.load_simple_chunk("index_to_simplex")) == 15

            assert reader.load_simple_chunk("vertex_symbols") == ["0", "1", "2", "3"]
            if save_bm:
                bmchunk = reader.load_boundary_map_chunk()
                assert bmchunk["chunktype"] == "boundary_map"
                assert bmchunk["type"] == "simplicial"
                assert isinstance(bmchunk["map"], list)
                assert len(bmchunk["map"]) == 15
            else:
                assert reader.load_boundary_map_chunk() is None

        def test_case_3points(self):
            matrix = np.array(
                [
                    [0, 2, 3],
                    [2, 0, 4],
                    [3, 4, 0],
                ],
                dtype=float,
            )
            distance_matrix = DistanceMatrix(matrix, 2, np.inf, ["A", "B", "XY"])
            filt = distance_matrix.build_simplicial_filtration(True)
            f = io.BytesIO()
            filt.compute_pdgm(f, None)
            f.seek(0)
            reader = PDGMReader(f)

            assert reader.metadata["filtration_type"] == "simplicial"
            assert reader.metadata["dim"] == 3
            assert not reader.metadata["sign_flipped"]

            assert reader.load_pd_chunk("pd", 0) == ([0, 0], [2, 3], [0])
            assert reader.load_pd_chunk("pd", 1) == (
                [],
                [],
                [],
            )
            assert reader.load_pd_chunk("indexed_pd", 0) == ([1, 2], [3, 4], [0])
            assert reader.load_pd_chunk("indexed_pd", 1) == ([], [], [])
            assert reader.load_simple_chunk("allpairs", 0) == [[1, 3], [2, 4], [0, None]]
            assert reader.load_simple_chunk("allpairs", 1) == [[5, 6]]
            assert reader.load_simple_chunk("index_to_level") == [0.0, 0.0, 0.0, 2.0, 3.0, 4.0, 4.0]
            assert reader.load_simple_chunk("index_to_simplex") == [
                [0],
                [1],
                [2],
                [0, 1],
                [0, 2],
                [1, 2],
                [0, 1, 2],
            ]
            assert reader.load_simple_chunk("vertex_symbols") == ["A", "B", "XY"]
            assert reader.load_boundary_map_chunk() == {
                "chunktype": "boundary_map",
                "type": "simplicial",
                "map": [
                    [0, []],
                    [0, []],
                    [0, []],
                    [1, [1, 0]],
                    [1, [2, 0]],
                    [1, [2, 1]],
                    [2, [5, 4, 3]],
                ],
            }


@pytest.mark.integration
class Test_main:
    def test_case(self, datadir, tmpdir):
        input = os.path.join(datadir, "dmatrix.txt")
        symbols = os.path.join(datadir, "dmatrix-symbols.txt")
        output = str(tmpdir.join("dmatrix.pdgm"))
        rips.main(
            rips.argument_parser().parse_args(
                [
                    "-d",
                    "1",
                    "--vertex-symbols",
                    symbols,
                    input,
                    output,
                ]
            )
        )
        assert get_pdgm_type(output) == "rips"

    def test_case_with_boundary_map(self, datadir, tmpdir):
        input = os.path.join(datadir, "dmatrix.txt")
        symbols = os.path.join(datadir, "dmatrix-symbols.txt")
        output = str(tmpdir.join("dmatrix.pdgm"))
        rips.main(
            rips.argument_parser().parse_args(
                [
                    "-d",
                    "1",
                    "--vertex-symbols",
                    symbols,
                    "-M",
                    "on",
                    input,
                    output,
                ]
            )
        )
        assert get_pdgm_type(output) == "simplicial"
