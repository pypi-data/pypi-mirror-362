import re
from functools import reduce
import operator

import numpy as np
import imageio


def load_nd_picture(paths, inputtype):
    def check_single_file():
        if len(paths) != 1:
            raise RuntimeError("text2d/text_nd/picture2d/npy require only a single file")

    if inputtype == "pictures3d":
        return stack_picts([load_picture(path) for path in paths])
    if inputtype == "picture2d":
        check_single_file()
        return load_picture(paths[0])
    if inputtype == "text2d":
        check_single_file()
        return np.loadtxt(paths[0])
    if inputtype == "text_nd":
        check_single_file()
        return load_nd_picture_from_text(paths[0])
    if inputtype == "npy":
        check_single_file()
        return np.load(paths[0])

    raise RuntimeError("Unknown file type: {}".format(inputtype))


def load_nd_picture_from_text(path):
    with open(path) as f:
        return read_nd_picture_text(f)


def read_nd_picture_text(f):
    while True:
        line = f.readline()
        if line is None:
            raise ValueError("Format error")

        if re.match(r"\s+#", line) or re.match(r"\s+\Z", line):
            continue

        shape = np.fromstring(line, sep=" ", dtype=int)[::-1]
        return np.loadtxt(f).reshape(shape)


def stack_picts(picts):
    """Stacking pictures into one ndarray"""
    if not all([pict.shape == picts[0].shape for pict in picts]):
        raise RuntimeError("Sizes of all pictures should be same")
    return np.array(picts)


def load_picture(path, filetype="picture"):
    """Load a picture and return 2D ndarray whose values are less than 256."""
    if filetype == "picture":
        pict = imageio.v3.imread(path, mode="L")
        if np.max(pict) > 255:
            pict //= 256
        return pict
    elif filetype == "text":
        return np.loadtxt(path)


def nd_indices(shape):
    """Create an array of all indices of the array of given shape.

    Example:
    nd_indices((2, 3)
    # => np.array([[0, 0], [0, 1], [0, 2],
    #              [1, 0], [1, 1], [1, 2]])
    """
    n = reduce(operator.mul, shape, 1)
    return np.indices(shape).reshape(len(shape), n).transpose()


def build_levelset_filtration(pict, cubical, periodic, superlevel, save_boundary_map):
    from homcloud.bitmap import Bitmap

    if cubical or periodic or save_boundary_map:
        return Bitmap(pict, superlevel, periodic, save_boundary_map).build_cubical_filtration()
    else:
        return Bitmap(pict, superlevel).build_bitmap_filtration()
