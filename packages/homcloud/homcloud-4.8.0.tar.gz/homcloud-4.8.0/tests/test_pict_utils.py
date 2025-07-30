# pylint: disable=C0103,C0111,W0201,R0201
import os
import io

import numpy as np
import numpy.testing as npt
import pytest

from homcloud.pict.utils import (
    load_picture,
    nd_indices,
    load_nd_picture,
    read_nd_picture_text,
    stack_picts,
)


@pytest.fixture
def path_bitmap_txt(datadir):
    return os.path.join(datadir, "bitmap.txt")


class Test_load_picture:
    def test_for_pngfile(self, path_5x2_png):
        pict = load_picture(path_5x2_png)
        assert pict.shape == (2, 5)
        assert np.allclose([[0, 255, 255, 255, 255], [255, 255, 0, 0, 0]], pict)

    def test_for_textfile(self, path_bitmap_txt):
        pict = load_picture(path_bitmap_txt, filetype="text")
        assert np.allclose([[0, 1, 5, 4, 2], [2, 3, 4, 3, 2]], pict)


class Test_nd_indices(object):
    def test_for_1x1(self):
        assert np.allclose(np.array([[0, 0]]), nd_indices((1, 1)))

    def test_for_2x3(self):
        npt.assert_almost_equal(np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]), nd_indices((2, 3)))

    def test_for_3d_2x3x1(self):
        npt.assert_almost_equal(
            np.array([[0, 0, 0], [0, 1, 0], [0, 2, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0]]), nd_indices((2, 3, 1))
        )

    def test_for_3d_2x3x2(self):
        npt.assert_almost_equal(
            np.array(
                [
                    [0, 0, 0],
                    [0, 0, 1],
                    [0, 1, 0],
                    [0, 1, 1],
                    [0, 2, 0],
                    [0, 2, 1],
                    [1, 0, 0],
                    [1, 0, 1],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 2, 0],
                    [1, 2, 1],
                ]
            ),
            nd_indices((2, 3, 2)),
        )


class Test_load_nd_picture(object):
    def test_for_npy(self, datadir):
        path = os.path.join(datadir, "test.npy")
        assert np.allclose(load_nd_picture([path], "npy"), np.array([[1, 2, 3], [4, 5, 6]]))

    def test_for_unknown_format(self):
        with pytest.raises(RuntimeError) as exc:
            load_nd_picture(["foo"], "invalid-format")
        assert str(exc.value) == "Unknown file type: invalid-format"

        with pytest.raises(RuntimeError) as exc:
            load_nd_picture(["foo", "bar"], "invalid-format")
        assert str(exc.value) == "Unknown file type: invalid-format"

    @pytest.mark.parametrize("format_name", ["text2d", "picture2d", "text_nd", "npy"])
    def test_for_multiple_files_for_single_file_format(self, format_name):
        with pytest.raises(RuntimeError) as exc:
            load_nd_picture(["foo", "bar"], format_name)
        assert str(exc.value) == "text2d/text_nd/picture2d/npy require only a single file"


@pytest.mark.filterwarnings("ignore:loadtxt")
def test_read_nd_picture_text():
    textdata = io.StringIO(
        """
    # This is comment


    # Next line shows the shape of the array (2x3x4)
    2 3 4
    1 2
    3 4
    5 6

    7 8
    9 10
    11 12

    13 14
    15 16
    17 18

    19 20
    21 22
    23 24
    """
    )
    expected = np.array(
        [
            [
                [1, 2],
                [3, 4],
                [5, 6],
            ],
            [[7, 8], [9, 10], [11, 12]],
            [[13, 14], [15, 16], [17, 18]],
            [[19, 20], [21, 22], [23, 24]],
        ],
        dtype=float,
    )

    assert np.allclose(read_nd_picture_text(textdata), expected)

    textdata = io.StringIO("4 0\n")
    assert read_nd_picture_text(textdata).shape == (0, 4)


class Test_stack_picts(object):
    PICT_A = np.array([[0.0, 1.0], [5.0, 2.0]])
    PICT_B = np.array([[3.0, 3.0], [1.0, 1.0]])
    PICT_C = np.array([[1.0], [4.0]])

    def test_using_pictures_with_same_size(self):
        assert np.allclose(
            stack_picts([self.PICT_A, self.PICT_B, self.PICT_A]),
            np.array([[[0.0, 1.0], [5.0, 2.0]], [[3.0, 3.0], [1.0, 1.0]], [[0.0, 1.0], [5.0, 2.0]]]),
        )

    def test_using_pictures_of_different_sizes(self):
        with pytest.raises(RuntimeError):
            stack_picts([self.PICT_A, self.PICT_B, self.PICT_C])
