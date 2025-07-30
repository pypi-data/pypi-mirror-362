# pylint: disable=C0111,W0201,R0201,C0103,R0903
import struct
import io
import os

import pytest
import numpy as np
from numpy import inf
import msgpack

from homcloud.bitmap import Bitmap, invert_permutation
from homcloud.pdgm_format import PDGMReader


class TestBitmapFiltration(object):
    class Test_write_dipha_complex(object):
        def test_for_2d_picture(self):
            pict = np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]])
            bitmap = Bitmap(pict).build_bitmap_filtration()
            expected = struct.pack("qqqqqqdddddd", 8067171840, 1, 6, 2, 3, 2, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
            output = io.BytesIO()
            bitmap.write_dipha_complex(output)
            assert output.getvalue() == expected

        def test_for_3d_picture(self):
            pict = np.array([[[1.0, 1], [0, 0]], [[2, 2], [1, 1]]])
            bitmap = Bitmap(pict).build_bitmap_filtration()
            expected = struct.pack("qqqqqqqdddddddd", 8067171840, 1, 8, 3, 2, 2, 2, 2, 3, 0, 1, 6, 7, 4, 5)
            output = io.BytesIO()
            bitmap.write_dipha_complex(output)
            assert output.getvalue() == expected

    class Test_build_bitmap_filtration(object):
        def test_case_2d_picture(self):
            pict = np.array([[5.0, 10.0, 0.0, 10.0], [11.0, 2.0, 9.0, 10.0]])
            bitmap = Bitmap(pict).build_bitmap_filtration()
            assert np.allclose(bitmap.index_bitmap, [[2, 4, 0, 5], [7, 1, 3, 6]])
            assert np.allclose(bitmap.index_to_pixel, [[0, 2], [1, 1], [0, 0], [1, 2], [0, 1], [0, 3], [1, 3], [1, 0]])
            assert np.allclose(bitmap.index_to_level, [0.0, 2.0, 5.0, 9.0, 10.0, 10.0, 10.0, 11.0])

        def test_case_flip_levels_sign_True(self):
            pict = np.array([[5.0, 10.0, 0.0, 10.0], [11.0, 2.0, 9.0, 10.0]])
            bitmap = Bitmap(-pict, True).build_bitmap_filtration()
            index_to_pixel = [[1, 0], [0, 1], [0, 3], [1, 3], [1, 2], [0, 0], [1, 1], [0, 2]]
            index_to_level = [11, 10, 10, 10, 9, 5, 2, 0]
            assert np.allclose(bitmap.index_bitmap, [[5, 1, 7, 2], [0, 6, 4, 3]])
            assert np.allclose(bitmap.index_to_pixel, index_to_pixel)
            assert np.allclose(bitmap.index_to_level, index_to_level)

        def test_case_3d_picture(self):
            pict = np.array([[[0, 1], [1, 2]], [[3, 4], [3, 4]], [[0, 7], [1, 1]]])
            bitmap = Bitmap(pict).build_bitmap_filtration()
            assert np.allclose(bitmap.index_bitmap, [[[0, 2], [3, 6]], [[7, 9], [8, 10]], [[1, 11], [4, 5]]])
            assert np.allclose(
                bitmap.index_to_pixel,
                [
                    [0, 0, 0],
                    [2, 0, 0],
                    [0, 0, 1],
                    [0, 1, 0],
                    [2, 1, 0],
                    [2, 1, 1],
                    [0, 1, 1],
                    [1, 0, 0],
                    [1, 1, 0],
                    [1, 0, 1],
                    [1, 1, 1],
                    [2, 0, 1],
                ],
            )
            assert np.allclose(bitmap.index_to_level, [0, 0, 1, 1, 1, 1, 2, 3, 3, 4, 4, 7])

        def test_case_inf_pixels(self):
            pict = np.array([[inf, -1], [inf, 2]])
            bitmap = Bitmap(pict).build_bitmap_filtration()
            assert np.allclose(bitmap.index_bitmap, [[2, 0], [3, 1]])
            assert np.allclose(bitmap.index_to_level, [-1, 2, inf, inf])

        def test_case_minus_inf_pixels(self):
            pict = np.array([[-inf, -1], [-inf, 2]])
            bitmap = Bitmap(-pict, True).build_bitmap_filtration()
            assert np.allclose(bitmap.index_bitmap, [[2, 1], [3, 0]])
            assert np.allclose(bitmap.index_to_level, [2, -1, -inf, -inf])

    @pytest.mark.parametrize("algorithm", [pytest.param("dipha", marks=pytest.mark.dipha), "homccube-1"])
    def test_compute_pairs(self, algorithm):
        pict = np.array([[0.0, 3.0], [4.0, 1.0]])
        pairs, _ = Bitmap(pict).build_bitmap_filtration().compute_pairs(algorithm)
        assert sorted(pairs) == [(0, 0, None), (0, 1, 2)]

    class Test_compute_pdgm(object):
        def test_case_2x2(self):
            pict = np.array([[0.0, 3.0], [4.0, 1.0]])
            f = io.BytesIO()
            Bitmap(pict).build_bitmap_filtration().compute_pdgm(f, "homccube-1")
            f.seek(0)
            reader = PDGMReader(f)
            assert reader.metadata["dim"] == 2
            assert reader.metadata["filtration_type"] == "bitmap"
            assert reader.load_pd_chunk("pd", 0) == ([1.0], [3.0], [0.0])
            assert reader.load_pd_chunk("pd", 1) == ([], [], [])
            assert reader.load_pd_chunk("pd", 2) == ([], [], [])
            assert reader.load_pd_chunk("pd", 3) == (None, None, None)
            assert reader.load_pd_chunk("indexed_pd", 0) == ([1], [2], [0])
            assert reader.load_pd_chunk("indexed_pd", 1) == ([], [], [])
            assert reader.load_pd_chunk("indexed_pd", 2) == ([], [], [])
            assert reader.load_pd_chunk("indexed_pd", 3) == (None, None, None)
            assert reader.load_simple_chunk("allpairs", 0) == [[0, None], [1, 2]]
            assert reader.load_simple_chunk("index_to_level") == [0.0, 1.0, 3.0, 4.0]
            assert reader.load_simple_chunk("index_to_pixel") == [[0, 0], [1, 1], [0, 1], [1, 0]]
            assert reader.load_chunk("bitmap_information") == {
                "chunktype": "bitmap_information",
                "shape": [2, 2],
                "periodicity": [False, False],
            }

        def test_case_2x2_periodic(self):
            pict = np.array([[0.0, 3.0], [4.0, 1.0]])
            f = io.BytesIO()
            Bitmap(pict, False, [False, True]).build_bitmap_filtration().compute_pdgm(f)
            f.seek(0)
            reader = PDGMReader(f)
            assert reader.metadata["dim"] == 2
            assert reader.metadata["filtration_type"] == "bitmap"
            assert reader.load_pd_chunk("pd", 0) == ([1.0], [3.0], [0.0])
            assert reader.load_pd_chunk("pd", 1) == ([], [], [3.0])
            assert reader.load_pd_chunk("pd", 2) == ([], [], [])
            assert reader.load_chunk("bitmap_information") == {
                "chunktype": "bitmap_information",
                "shape": [2, 2],
                "periodicity": [False, True],
            }

        def test_case_periodic_dipha(self):
            pict = np.array([[0.0, 3.0], [4.0, 1.0]])
            filtration = Bitmap(pict, False, [False, True]).build_bitmap_filtration()
            with pytest.raises(NotImplementedError):
                filtration.compute_pdgm(io.BytesIO(), "dipha")


@pytest.mark.parametrize(
    "input,expected",
    [
        ([0, 1], [0, 1]),
        ([2, 5, 0, 6, 1, 7, 3, 4], [2, 4, 0, 6, 7, 1, 3, 5]),
    ],
)
def test_invert_permutation(input, expected):
    a = np.array(input)
    assert np.allclose(expected, invert_permutation(a))


class TestCubicalFiltration(object):
    def test_write_dipha_complex(self):
        filt = Bitmap(np.random.uniform(size=(10, 14)), periodicity=[False] * 2).build_cubical_filtration()

        with open(os.devnull, "wb") as f:
            filt.write_dipha_complex(f)

    @pytest.fixture
    def array(self):
        #   4 -(4)- 0 -(1)- 1
        #   |       |       |
        #  (4) (7) (7) (9) (9)
        #   |       |       |
        #   2 -(7)- 7 -(9)- 9
        return np.array([[4, 0, 1], [2, 7, 9]])

    @pytest.mark.parametrize(
        "sign_flipped, index_to_level",
        [
            (False, [0, 1, 1, 2, 4, 4, 4, 7, 7, 7, 7, 9, 9, 9, 9]),
            (True, [0, -1, -1, -2, -4, -4, -4, -7, -7, -7, -7, -9, -9, -9, -9]),
        ],
    )
    def test_index_to_level(self, array, sign_flipped, index_to_level):
        filt = Bitmap(array, sign_flipped, [False] * 2).build_cubical_filtration()
        assert filt.sign_flipped == sign_flipped
        assert filt.index_to_level.tolist() == index_to_level

    def assert_sorted_cubes(self, filt, cubes):
        assert [filt.decode_cube(cube) for cube in cubes] == [
            ([0, 1], [0, 0]),
            ([0, 2], [0, 0]),
            ([0, 1], [0, 1]),
            ([1, 0], [0, 0]),
            ([0, 0], [0, 0]),
            ([0, 0], [0, 1]),
            ([0, 0], [1, 0]),
            ([1, 1], [0, 0]),
            ([0, 1], [1, 0]),
            ([1, 0], [0, 1]),
            ([0, 0], [1, 1]),
            ([1, 2], [0, 0]),
            ([0, 2], [1, 0]),
            ([1, 1], [0, 1]),
            ([0, 1], [1, 1]),
        ]

    @pytest.mark.parametrize("save_boundary_map", [True, False])
    def test_build_phat_matrix(self, array, save_boundary_map):
        filt = Bitmap(array, False, [False] * 2, save_boundary_map).build_cubical_filtration()
        matrix = filt.build_phat_matrix()
        matrix.reduce_twist()
        # assert [
        #     pair for pair in matrix.birth_death_pairs() if pair[0] == 0
        # ] == [(0, 2, 4), (0, 0, None)]
        # pd0 = PD.load_from_dipha(io.BytesIO(matrix.dipha_diagram_bytes()), 0)
        # pd0.index_map = filt.index_map
        # pd0.restore_levels(pd0.index_map)
        # assert np.allclose(pd0.births, [2])
        # assert np.allclose(pd0.deaths, [4])
        # assert np.allclose(pd0.essential_births, [0])

        if save_boundary_map:
            self.assert_boundary_map(msgpack.unpackb(matrix.boundary_map_byte_sequence(), raw=False))
        else:
            assert matrix.boundary_map_byte_sequence() is None

    def assert_boundary_map(self, boundary_map):
        assert boundary_map == {
            "chunktype": "boundary_map",
            "type": "cubical",
            "map": [
                [0, []],
                [0, []],
                [1, [1, 0]],
                [0, []],
                [0, []],
                [1, [0, 4]],
                [1, [3, 4]],  # 0-6
                [0, []],
                [1, [7, 0]],
                [1, [7, 3]],
                [2, [9, 5, 8, 6]],  # 7-10
                [0, []],
                [1, [11, 1]],
                [1, [11, 7]],
                [2, [13, 2, 12, 8]],  # 11-14
            ],
        }

    @pytest.mark.parametrize("save_bm", [True, False])
    def test_compute_pdgm(self, array, save_bm):
        filt = Bitmap(array, False, [False] * 2, save_bm).build_cubical_filtration()
        f = io.BytesIO()
        filt.compute_pdgm(f)
        f.seek(0)
        reader = PDGMReader(f)
        assert reader.load_pd_chunk("pd", 0) == ([2], [4], [0])
        assert reader.load_simple_chunk("index_to_level") == [0, 1, 1, 2, 4, 4, 4, 7, 7, 7, 7, 9, 9, 9, 9]
        self.assert_sorted_cubes(filt, reader.load_simple_chunk("index_to_cube"))
        assert reader.load_chunk("bitmap_information") == {
            "chunktype": "bitmap_information",
            "shape": [2, 3],
            "periodicity": [False, False],
        }

        if save_bm:
            self.assert_boundary_map(reader.load_boundary_map_chunk())
        else:
            reader.load_boundary_map_chunk() is None
