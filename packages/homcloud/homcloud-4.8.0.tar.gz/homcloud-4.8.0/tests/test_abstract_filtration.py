import io
import os

import pytest

from homcloud.abstract_filtration import AbstractFiltrationLoader, AbstractFiltration, argument_parser, main
from homcloud.pdgm_format import PDGMReader


CODE1 = """
# comment
# id dim time = indices : coefs
0 0 0.0 = :
1 0 0.0 = :
2 1 1.0 = 0 1 : 1 -1
3 0 1.2 = :
4 1 1.3 = 1 3 : 1 -1
5 1 1.3 = 3 0 : 1 -1
6 2 2.1 = 2 4 5 : 1 1 1
"""

BOUNDARY_MAP1 = [
    [0, [], []],
    [0, [], []],
    [1, [0, 1], [1, -1]],
    [0, [], []],  # 0-3
    [1, [1, 3], [1, -1]],
    [1, [3, 0], [1, -1]],  # 4-5
    [2, [2, 4, 5], [1, 1, 1]],  # 6
]

CODE2 = """
# symbol dim time = indices : coefs
autoid: true
autosymbol: false
v0 0 0.0 = :
v1 0 0.0 = :
e0 1 1.0 = 0 1 : 2 -2
"""

BOUNDARY_MAP2 = [[0, [], []], [0, [], []], [1, [0, 1], [2, -2]]]


@pytest.mark.integration
def test_main(tmpdir, datadir):
    inpath = os.path.join(datadir, "abstract.txt")
    outpath = str(tmpdir.join("out.pdgm"))
    main(argument_parser().parse_args([inpath, outpath]))


class TestAbstractFiltrationLoader(object):
    @pytest.mark.parametrize(
        "text, autoid, autosymbol",
        [
            (CODE1, False, True),
            (CODE2, True, False),
        ],
    )
    def test_load(self, text, autoid, autosymbol):
        loader = AbstractFiltrationLoader(io.StringIO(text))
        loader.load()
        assert loader.autoid == autoid
        assert loader.autosymbol == autosymbol

    @pytest.mark.parametrize(
        "text, save_bm, boundary_map",
        [
            (CODE1, False, BOUNDARY_MAP1),
            (CODE2, False, BOUNDARY_MAP2),
            (CODE1, True, BOUNDARY_MAP1),
            (CODE2, True, BOUNDARY_MAP2),
        ],
    )
    def test_filtration(self, text, save_bm, boundary_map):
        loader = AbstractFiltrationLoader(io.StringIO(text))
        loader.load()
        assert loader.filtration(save_bm).boundary_map == boundary_map


class TestAbstractFiltration(object):
    @pytest.mark.parametrize("text, dim", [(CODE1, 2), (CODE2, 1)])
    def test_dim(self, text, dim):
        assert AbstractFiltration.load(io.StringIO(text), False).dim == dim

    @pytest.mark.parametrize(
        "text, levels",
        [
            (CODE1, [0.0, 0.0, 1.0, 1.2, 1.3, 1.3, 2.1]),
            (CODE2, [0.0, 0.0, 1.0]),
        ],
    )
    def test_index_to_level(self, text, levels):
        filtration = AbstractFiltration.load(io.StringIO(text), False)
        assert filtration.index_to_level == levels

    @pytest.mark.parametrize(
        "text, symbols",
        [
            (CODE1, [str(n) for n in range(7)]),
            (CODE2, ["v0", "v1", "e0"]),
        ],
    )
    def test_index_to_symbol(self, text, symbols):
        filtration = AbstractFiltration.load(io.StringIO(text), False)
        assert filtration.index_to_symbol == symbols

    @pytest.mark.parametrize(
        "text, pairs",
        [
            (CODE1, [(0, 1, 2), (0, 3, 4), (1, 5, 6), (0, 0, None)]),
            (CODE2, [(0, 0, None), (0, 1, None), (1, 2, None)]),
            # [[1, 3], [5]], [[2, 4], [6]], [[0], []]),
            # (CODE2, [[], []], [[], []], [[0, 1], [2]]),
        ],
    )
    def test_build_phat_matrix(self, text, pairs):
        filt = AbstractFiltration.load(io.StringIO(text), False)
        matrix = filt.build_phat_matrix()
        matrix.reduce_twist()
        assert matrix.birth_death_pairs() == pairs

    @pytest.mark.parametrize("save_bm", [True, False])
    def test_compute_pdgm(self, save_bm):
        f = io.BytesIO()
        AbstractFiltration.load(io.StringIO(CODE2), save_bm).compute_pdgm(f)
        f.seek(0)
        pdgmreader = PDGMReader(f)

        assert pdgmreader.metadata["filtration_type"] == "abstract"
        assert pdgmreader.metadata["dim"] == 1

        assert pdgmreader.load_pd_chunk("pd", 0) == ([], [], [0.0, 0.0])
        assert pdgmreader.load_pd_chunk("pd", 1) == ([], [], [1.0])

        assert pdgmreader.load_pd_chunk("indexed_pd", 0) == ([], [], [0, 1])
        assert pdgmreader.load_pd_chunk("indexed_pd", 1) == ([], [], [2])

        all_pairs0 = pdgmreader.load_simple_chunk("allpairs", 0)
        assert all_pairs0 == [[0, None], [1, None]]
        all_pairs1 = pdgmreader.load_simple_chunk("allpairs", 1)
        assert all_pairs1 == [[2, None]]

        index_to_level = pdgmreader.load_simple_chunk("index_to_level")
        assert index_to_level == [0.0, 0.0, 1.0]

        index_to_symbols = pdgmreader.load_simple_chunk("index_to_symbol")
        assert index_to_symbols == ["v0", "v1", "e0"]

        if save_bm:
            assert pdgmreader.load_boundary_map_chunk() == {
                "chunktype": "boundary_map",
                "type": "abstract",
                "map": BOUNDARY_MAP2,
            }
        else:
            assert pdgmreader.load_boundary_map_chunk() is None
