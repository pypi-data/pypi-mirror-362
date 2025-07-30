import io

import pytest

from homcloud.simplicial_levelset import SimplicialFiltration
from homcloud.pdgm_format import PDGMReader

FILTRATION_FUNCTION = {
    (0,): 0.0,
    (1,): 1.0,
    (2,): 1.0,
    (1, 2): 1.0,
    (0, 1): 1.2,
    (2, 0): 1.5,
    (1, 2, 0): 1.7,
    (3,): 2.0,
    (3, 1): 2.2,
    (3, 2): 2.3,
}


class TestSimplicialFiltration(object):
    @pytest.fixture
    def filtration(self):
        return SimplicialFiltration(FILTRATION_FUNCTION, None, True)

    def test_constructor(self):
        filtration = SimplicialFiltration(FILTRATION_FUNCTION, None, True)
        assert filtration.index_to_level == [0.0, 1.0, 1.0, 1.0, 1.2, 1.5, 1.7, 2.0, 2.2, 2.3]
        assert filtration.index_to_simplex == [
            (0,),
            (1,),
            (2,),
            (1, 2),
            (0, 1),
            (0, 2),
            (0, 1, 2),
            (3,),
            (1, 3),
            (2, 3),
        ]
        assert filtration.simplex_to_index == {
            (0,): 0,
            (1,): 1,
            (2,): 2,
            (1, 2): 3,
            (0, 1): 4,
            (0, 2): 5,
            (0, 1, 2): 6,
            (3,): 7,
            (1, 3): 8,
            (2, 3): 9,
        }

    def test_compute_pairs(self, filtration):
        pairs, _ = filtration.compute_pairs()
        assert pairs == [(0, 2, 3), (0, 1, 4), (1, 5, 6), (0, 7, 8), (0, 0, None), (1, 9, None)]

    def test_num_vertices(self, filtration):
        assert filtration.num_vertices == 4

    @pytest.mark.parametrize("save_bm", [True, False])
    def test_compute_pdgm(self, save_bm):
        filtration = SimplicialFiltration(FILTRATION_FUNCTION, None, save_bm)
        f = io.BytesIO()
        filtration.compute_pdgm(f)
        f.seek(0)

        reader = PDGMReader(f)
        assert reader.filtration_type == "simplicial"
        assert reader.metadata["dim"] == 2
        assert not reader.metadata["sign_flipped"]

        births, deaths, ess_births = reader.load_pd_chunk("pd", 0)
        assert births == [1, 2]
        assert deaths == [1.2, 2.2]
        assert ess_births == [0]

        births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 0)
        assert births == [1, 7]
        assert deaths == [4, 8]
        assert ess_births == [0]

        births, deaths, ess_births = reader.load_pd_chunk("pd", 1)
        assert births == [1.5]
        assert deaths == [1.7]
        assert ess_births == [2.3]

        births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 1)
        assert births == [5]
        assert deaths == [6]
        assert ess_births == [9]

        assert reader.load_simple_chunk("allpairs", 0) == [[2, 3], [1, 4], [7, 8], [0, None]]
        assert reader.load_simple_chunk("allpairs", 1) == [
            [5, 6],
            [9, None],
        ]
        assert reader.load_simple_chunk("allpairs", 2) == []

        assert len(reader.load_simple_chunk("index_to_level")) == 10
        assert len(reader.load_simple_chunk("index_to_simplex")) == 10

        assert reader.load_simple_chunk("vertex_symbols") == ["0", "1", "2", "3"]

        if save_bm:
            bmchunk = reader.load_boundary_map_chunk()
            assert bmchunk["chunktype"] == "boundary_map"
            assert bmchunk["type"] == "simplicial"
            assert bmchunk["map"] == [
                [0, []],
                [0, []],
                [0, []],
                [1, [2, 1]],
                [1, [1, 0]],
                [1, [2, 0]],
                [2, [3, 5, 4]],
                [0, []],
                [1, [7, 1]],
                [1, [7, 2]],
            ]
        else:
            assert reader.load_boundary_map_chunk() is None
