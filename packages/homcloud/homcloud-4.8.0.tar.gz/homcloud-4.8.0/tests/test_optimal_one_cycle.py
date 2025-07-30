import msgpack

import homcloud.optimal_one_cycle as opt1cyc
import pytest

BOUNDARY_MAP = {
    "chunktype": "boundary_map",
    "type": "simplicial",
    "map": [
        [0, []],
        [0, []],
        [0, []],
        [0, []],
        [1, [1, 0]],
        [1, [3, 1]],
        [1, [3, 0]],
        [1, [3, 2]],
        [1, [1, 2]],
        [1, [0, 2]],
        [2, [5, 6, 4]],
        [2, [5, 7, 8]],
        [2, [4, 8, 9]],
        [2, [6, 7, 9]],
        [3, [10, 11, 13, 12]],
    ],
}


def test_vertices():
    assert opt1cyc.vertices(BOUNDARY_MAP, 7) == [0, 1, 2, 3]


def test_edges():
    assert opt1cyc.edges(BOUNDARY_MAP, 7) == [(4, [1, 0]), (5, [3, 1]), (6, [3, 0])]


def test_adjacent_vertices():
    assert opt1cyc.adjacent_vertices(BOUNDARY_MAP, 7) == {
        0: [(4, 0, 1), (6, 0, 3)],
        1: [(4, 1, 0), (5, 1, 3)],
        2: [],
        3: [(5, 3, 1), (6, 3, 0)],
    }


@pytest.mark.parametrize(
    "birth, expected",
    [
        (7, None),
        (6, [4, 5, 6]),
    ],
)
def test_search(birth, expected):
    assert opt1cyc.search(BOUNDARY_MAP, birth) == expected


@pytest.mark.parametrize(
    "birth, expected",
    [
        (7, None),
        (6, [4, 5, 6]),
    ],
)
def test_search_on_chunk_bytes(birth, expected):
    b = msgpack.packb(BOUNDARY_MAP, use_bin_type=True)
    assert opt1cyc.search_on_chunk_bytes(b, birth) == expected
