# pylint: disable=no-self-use,invalid-name
import os
import json

import numpy as np
import pytest
import msgpack

import homcloud.pict.tree as tree
import homcloud.pict_tree as tree_ext
from homcloud.pdgm_format import PDGMReader

from tests.helper import get_pdgm_type


@pytest.fixture
def mergetree_upper():
    return tree_ext.MergeTree(np.array([[8, -1, 0], [7, 10, 1], [6, 4, 2]], dtype=float), False, False)


@pytest.fixture
def mergetree_lower():
    return tree_ext.MergeTree(np.array([[3, -1, 0], [1, 3, 4], [2, 9, 8]], dtype=float), False, True)


class TestMergeTree(object):
    def test_compute_lower_sublevel(self):
        bitmap = np.array([[6, 0, 1], [5, 8, 2], [7, 4, 3]], dtype=float)
        mt = tree_ext.MergeTree(bitmap, False, True)
        mt.compute()
        assert mt.num_nodes() == 9
        for n, level in enumerate(bitmap.transpose().ravel()):
            assert mt.node_id(n) == str(int(level))
        for n in range(9):
            assert mt.node_is_trivial(n) == (n not in [1, 3])

        assert mt.node_birth_time(3) == 0.0
        assert mt.node_death_time(3) is None
        assert mt.node_birth_pixel(3) == (0, 1)
        assert mt.node_death_pixel(3) is None
        assert mt.node_parent(3) is None
        assert mt.node_birth_time(1) == 5.0
        assert mt.node_death_time(1) == 6.0
        assert mt.node_birth_pixel(1) == (1, 0)
        assert mt.node_death_pixel(1) == (0, 0)
        assert set(mt.node_volume(1)) == set([(1, 0), (0, 0)])
        assert mt.node_parent(1) == "0"

    def test_compute_upper_sublevel(self):
        bitmap = np.array([[6, 0, 1], [5, 8, 2], [7, 4, 3]], dtype=float)
        mt = tree_ext.MergeTree(bitmap, False, False)
        mt.compute()
        assert mt.num_nodes() == 9
        for n, level in enumerate(bitmap.transpose().ravel()):
            assert mt.node_id(n) == str(int(8 - level))
        assert mt.node_birth_time(4) == 7.0
        assert mt.node_death_time(4) == 8.0
        assert mt.node_birth_pixel(4) == (2, 0)
        assert mt.node_death_pixel(4) == (1, 1)
        assert mt.node_parent(4) is None
        assert mt.node_volume(4) == [(1, 1)]

    def test_compute_lower_superlevel(self):
        bitmap = np.array([[6, 0, 1], [5, 8, 2], [7, 4, 3]], dtype=float)
        mt = tree_ext.MergeTree(bitmap, True, True)
        mt.compute()
        assert mt.num_nodes() == 9
        for n, level in enumerate(bitmap.transpose().ravel()):
            assert mt.node_id(n) == str(int(8 - level))
        for n in range(9):
            assert mt.node_is_trivial(n) == (n not in [0, 2, 4])

        assert mt.node_id(0) == "2"
        assert mt.node_birth_time(0) == 6.0
        assert mt.node_death_time(0) == 5.0
        assert mt.node_children(0) == ["3"]
        assert mt.node_id(2) == "1"
        assert mt.node_birth_time(2) == 7.0
        assert mt.node_death_time(2) == 5.0
        assert mt.node_children(2) == ["2"]
        assert mt.node_id(4) == "0"
        assert mt.node_birth_time(4) == 8.0
        assert mt.node_death_time(4) is None
        assert mt.node_children(4) == ["1", "4", "5", "6", "7", "8"]

    def test_compute_upper_superlevel(self):
        bitmap = np.array([[6, 8, 1], [5, 0, 2], [7, 4, 3]], dtype=float)
        mt = tree_ext.MergeTree(bitmap, True, False)
        mt.compute()
        assert mt.num_nodes() == 9
        for n, level in enumerate(bitmap.transpose().ravel()):
            assert mt.node_id(n) == str(int(level))
        for n in range(9):
            assert mt.node_is_trivial(n) == (n != 4)
        assert mt.node_id(4) == "0"
        assert mt.node_birth_time(4) == 1.0
        assert mt.node_death_time(4) == 0.0


class Test_merge_tree_to_dict(object):
    def test_for_lower(self, mergetree_lower):
        mergetree_lower.compute()
        assert tree.merge_tree_to_dict(mergetree_lower) == {
            "degree": 0,
            "nodes": {
                "0": {
                    "id": "0",
                    "parent": None,
                    "birth-time": -1.0,
                    "death-time": None,
                    "birth-pixel": (0, 1),
                    "death-pixel": None,
                    "volume": [(0, 1), (0, 2), (1, 0), (2, 0), (0, 0), (1, 1), (1, 2), (2, 2), (2, 1)],
                    "children": ["1", "2", "5", "6", "7", "8"],
                },
                "1": {
                    "id": "1",
                    "parent": "0",
                    "birth-time": 0.0,
                    "death-time": 0.0,
                    "birth-pixel": (0, 2),
                    "death-pixel": (0, 2),
                    "volume": [(0, 2)],
                    "children": [],
                },
                "2": {
                    "id": "2",
                    "parent": "0",
                    "birth-time": 1.0,
                    "death-time": 3.0,
                    "birth-pixel": (1, 0),
                    "death-pixel": (0, 0),
                    "volume": [(1, 0), (2, 0), (0, 0)],
                    "children": ["3", "4"],
                },
                "3": {
                    "id": "3",
                    "parent": "2",
                    "birth-time": 2.0,
                    "death-time": 2.0,
                    "birth-pixel": (2, 0),
                    "death-pixel": (2, 0),
                    "volume": [(2, 0)],
                    "children": [],
                },
                "4": {
                    "id": "4",
                    "parent": "2",
                    "birth-time": 3.0,
                    "death-time": 3.0,
                    "birth-pixel": (0, 0),
                    "death-pixel": (0, 0),
                    "volume": [(0, 0)],
                    "children": [],
                },
                "5": {
                    "id": "5",
                    "parent": "0",
                    "birth-time": 3.0,
                    "death-time": 3.0,
                    "birth-pixel": (1, 1),
                    "death-pixel": (1, 1),
                    "volume": [(1, 1)],
                    "children": [],
                },
                "6": {
                    "id": "6",
                    "parent": "0",
                    "birth-time": 4.0,
                    "death-time": 4.0,
                    "birth-pixel": (1, 2),
                    "death-pixel": (1, 2),
                    "volume": [(1, 2)],
                    "children": [],
                },
                "7": {
                    "id": "7",
                    "parent": "0",
                    "birth-time": 8.0,
                    "death-time": 8.0,
                    "birth-pixel": (2, 2),
                    "death-pixel": (2, 2),
                    "volume": [(2, 2)],
                    "children": [],
                },
                "8": {
                    "id": "8",
                    "parent": "0",
                    "birth-time": 9.0,
                    "death-time": 9.0,
                    "birth-pixel": (2, 1),
                    "death-pixel": (2, 1),
                    "volume": [(2, 1)],
                    "children": [],
                },
            },
        }

    def test_for_upper(self, mergetree_upper):
        mergetree_upper.compute()
        assert tree.merge_tree_to_dict(mergetree_upper) == {
            "degree": 1,
            "nodes": {
                "0": {
                    "id": "0",
                    "parent": None,
                    "birth-time": 8,
                    "death-time": 10,
                    "birth-pixel": (0, 0),
                    "death-pixel": (1, 1),
                    "volume": [(1, 1)],
                    "children": [],
                },
            },
        }


class Test_tree_to_pd(object):
    def test_case_lower(self, mergetree_lower):
        mergetree_lower.compute()
        births, deaths, ess_births = tree.tree_to_pd(mergetree_lower)
        assert sorted(zip(births, deaths)) == [(1, 3)]
        assert ess_births == [-1]

    def test_case_upper(self, mergetree_upper):
        mergetree_upper.compute()
        births, deaths, ess_births = tree.tree_to_pd(mergetree_upper)
        assert sorted(zip(births, deaths)) == [(8, 10)]
        assert ess_births == []


@pytest.mark.integration
class Test_main:
    def test_for_pict3d_txt(self, datadir, tmpdir):
        inpath = os.path.join(datadir, "pict3d.txt")
        outpath = str(tmpdir.join("out.json"))
        tree.main(
            tree.argument_parser().parse_args(
                ["-m", "black-base", "-T", "text_nd", inpath, "-O", "json", "-o", outpath]
            )
        )
        with open(outpath) as f:
            json.load(f)

    def test_for_npy(self, datadir, tmpdir):
        inpath = os.path.join(datadir, "test.npy")
        outpath = str(tmpdir.join("out.p2mt"))
        tree.main(
            tree.argument_parser().parse_args(
                [
                    "-m",
                    "superlevel",
                    "-T",
                    "npy",
                    inpath,
                    "-O",
                    "msgpack",
                    "-o",
                    outpath,
                ]
            )
        )
        with open(outpath, "rb") as f:
            msgpack.load(f)

    def test_case_pdgm_output(self, datadir, tmpdir):
        inpath = os.path.join(datadir, "test.npy")
        outpath = str(tmpdir.join("out.pdgm"))
        tree.main(
            tree.argument_parser().parse_args(
                [
                    "-m",
                    "sublevel",
                    "-T",
                    "npy",
                    inpath,
                    "-o",
                    outpath,
                ]
            )
        )
        assert get_pdgm_type(outpath) == "bitmap-tree"
        reader = PDGMReader.open(outpath)
        assert reader.load_pd_chunk("pd", 0) == ([], [], [1.0])
        assert reader.load_pd_chunk("pd", 1) == ([], [], [])
        assert reader.load_pd_chunk("indexed_pd", 0) == (None, None, None)
        mt_low = reader.load_simple_chunk("bitmap_phtrees", 0)
        assert mt_low["degree"] == 0
        assert mt_low["nodes"]["0"]["id"] == "0"
        assert mt_low["nodes"]["0"]["birth-time"] == 1.0
        assert mt_low["nodes"]["0"]["death-time"] is None
        mt_high = reader.load_simple_chunk("bitmap_phtrees", 1)
        assert mt_high["degree"] == 1
