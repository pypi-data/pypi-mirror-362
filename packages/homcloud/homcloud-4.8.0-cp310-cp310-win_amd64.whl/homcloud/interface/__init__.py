"""HomCloud python interface

This module provides the interface to HomCloud from python program.

The API document is written by sphinx with Napolen.
https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
"""

from itertools import chain
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image
import numpy as np

import homcloud.pict.utils as pict_utils
import homcloud.view_index_pict as view_index_pict
import homcloud.pict.slice3d as pict_slice3d

from homcloud.license import LICENSE_TERMS

__all__ = [
    "LICENSE_TERMS",  # .homcloud.licence
    "HomCloudError",
    "VolumeNotFound",  # .exceptions
    "PDList",
    "PD",
    "Pair",  # .pd
    "HistoSpec",
    "Mesh",
    "PIVectorizeSpec",
    "PIVectorizerMesh",
    "Histogram",
    "MaskHistogram",
    "SliceHistogram",  # .histogram
    "Volume",
    "OptimalVolume",
    "EigenVolume",
    "StableVolume",
    "StableSubvolume",  # .optimal_volume
    "PHTrees",  # .phtrees
    "BitmapPHTrees",  # .bitmap_phtrees
    "distance_transform",  # .distance_transform
    "BitmapOptimal1Cycle",  # .bitmap_optimal_1_cycle
    "GraphOptimal1Cycle",  # .graph_optimal_1_cycle
    "Optimal1Cycle",  # .optimal_1_cycle
    "example_data",
    "loadtxt_nd",
    "draw_volumes_on_2d_image",
    "draw_birthdeath_pixels_2d",
    "show_slice3d",
]
from .exceptions import *
from .pd import *
from .histogram import *
from .optimal_volume import *
from .phtrees import *
from .bitmap_phtrees import *
from .bitmap_optimal_1_cycle import *
from .distance_transform import *
from . import bitmap as bitmap
from . import distance


def example_data(name):
    """Returns example data.

    Returns the tetrahedron 3D pointcloud for name == "tetrahedron".

    Args:
        name: Name of the data

    Examples:
        >>> import homcloud.interface as hc
        >>> hc.example_data("tetrahedron")
        array([[ 0.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 5.,  6.,  0.],
               [ 4.,  2.,  6.]])
    """
    if name == "tetrahedron":
        return np.array(
            [
                [0.0, 0.0, 0.0],
                [8.0, 0.0, 0.0],
                [5.0, 6.0, 0.0],
                [4.0, 2.0, 6.0],
            ]
        )
    if name == "bitmap_01_5x5x5":
        return np.array(
            [
                [[0, 0, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1]],
                [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 1, 0]],
                [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]],
                [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]],
                [[1, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 0, 0]],
            ],
            dtype=bool,
        )
    if name == "bitmap_levels_5x5":
        return np.array(
            [
                [0, 0, 1, 1, 1],
                [0, 4, 0, 5, 1],
                [0, 8, 0, 3, 1],
                [0, 0, 4, 7, 1],
                [0, 0, 2, 1, 1],
            ],
            dtype=int,
        )

    raise ValueError("Unknown example name: %s" % name)


def loadtxt_nd(path):
    """
    Load a n-dimensional data from text.

    The format of the text file is as follows.

    * First line represents the shape of data. For example, if the shape of your d
      ata is 200x230x250, first line should be `200 230 250`.
    * The following lines are floating point number values in x-fastest direction
    * A line starting with `#` is skipped as a comment
    * An empty line is also skipped.

    The following is an example::

        # 4x3x2 3D voxel data
        4 3 2

        1 2 3 4
        5 6 7 8
        9 10 11 12

        13 14 15 16
        17 18 19 20
        21 22 23 24

    Args:
        path (string): The path of the text file.
    """
    return pict_utils.load_nd_picture_from_text(path)


def draw_pixels_on_2d_image(image, pixels, color, alpha=1.0):
    for y, x in pixels:
        if x < 0 or y < 0 or x >= image.size[0] or y >= image.size[1]:
            continue
        blended_color = tuple((np.array(image.getpixel((x, y))) * (1 - alpha) + np.array(color) * alpha).astype(int))
        image.putpixel((x, y), blended_color)
    return image


def draw_volumes_on_2d_image(nodes, image, color, alpha=1.0, birth_position=None, death_position=None, marker_size=1):
    """
    Draws optimal volumes for bitmap filtration on an image.

    Args:
        nodes (list of :class:`BitmapPHTrees.Node`):
            The tree nodes to be drawn.
        image (string or numpy.ndarray or PIL.Image.Image):
            The base image data.

            * string: The image file whose name is `image` is used.
            * numpy.ndarray: 2D array is treated as grayscale image.
            * PIL.Image.Image: The image data

            If PIL.Image.Image object is given, the object is overwrited.
        color (tuple[int, int, int]): The color (RGB) of the volumes.
        alpha (float): The alpha value.
           The volume is drawn by using alpha blending.
        birth_position (tuple[int, int, int] or None): If not None,
           birth positions are drawn by the given color
        death_position (tuple[int, int, int] or None): If not None,
           death positions are drawn by the given color
        marker_size (int): The marker size of birth positions and death positions.
           1, 3, 5, ... are available.
    Returns:
        PIL.Image.Image: The image data which optimal volumes are drawn.
    """
    image = to_pil_image(image)

    def draw_marker(position, color):
        d = marker_size // 2
        pixels = [(position[0] + dy, position[1] + dx) for dx in range(-d, d + 1) for dy in range(-d, d + 1)]
        draw_pixels_on_2d_image(image, pixels, color)

    pixels = set(chain.from_iterable([map(tuple, node.volume()) for node in nodes]))
    draw_pixels_on_2d_image(image, pixels, color, alpha)

    if birth_position:
        for node in nodes:
            draw_marker(node.birth_position(), birth_position)
    if death_position:
        for node in nodes:
            draw_marker(node.death_position(), death_position)

    return image


def draw_birthdeath_pixels_2d(
    pairs,
    image,
    draw_birth=False,
    draw_death=False,
    draw_line=False,
    scale=1,
    marker_type="filled-diamond",
    marker_size=1,
    with_label=False,
    birth_color=(255, 0, 0),
    death_color=(0, 0, 255),
    line_color=(0, 255, 0),
):
    """
    Draw birth/death pixels on the given image.

    This function returns PIL.Image.Image object.
    Please see the `document of pillow
    <https://pillow.readthedocs.io/en/latest/reference/Image.html>`_
    to know how to treat this object.

    Args:
        pairs (list of :class:`Pair`): The birth-death pairs.
        image (string or numpy.ndarray or PIL.Image.Image):
            The image data.

            * string: The image file whose name is `image` is used.
            * numpy.ndarray: 2D array is treated as grayscale image.
            * PIL.Image.Image: The image data
        draw_birth (bool): Birth pixels are drawn if True.
        draw_death (bool): Death pixels are drawn if True.
        draw_line (bool): The lines connecting each birth pixels and
            death pixels are drawn.
        scale (int): Image scaling factor.
        marker_type (string): The type of the markers. You can choose
            one of the followings:

            * "filled-diamond"
            * "point"
            * "square"
            * "filled-square"
            * "circle"
            * "filled-circle"
        marker_size (int): The size of the marker.
        with_label (bool): Show birth and death times beside
            each birth/death pixel marker.
        birth_color (tuple[int, int, int]): The color of birth pixel markers.
        death_color (tuple[int, int, int]): The color of death pixel markers.
        line_color (tuple[int, int, int]): The color of lines.

    Returns:
        PIL.Image.Image: The image data which birth/death pixels are drawn.
    """
    image = to_pil_image(image)

    output_image, marker_drawer = view_index_pict.setup_images(image, scale, not with_label)
    marker_drawer.scale = scale
    marker_drawer.marker_size = marker_size
    marker_drawer.should_draw_birth_pixel = draw_birth
    marker_drawer.should_draw_death_pixel = draw_death
    marker_drawer.should_draw_line = draw_line
    marker_drawer.no_label = not with_label
    marker_drawer.birth_color = birth_color
    marker_drawer.death_color = death_color
    marker_drawer.line_color = line_color

    for pair in pairs:
        marker_drawer.draw_pair(pair)

    return output_image


def to_pil_image(image):
    if isinstance(image, str):
        return Image.open(image).convert("RGB")
    elif isinstance(image, np.ndarray):
        upper = np.max(image)
        lower = np.min(image)
        return Image.fromarray(((image - lower) / (upper - lower) * 250).astype(np.uint8)).convert("RGB")
    elif isinstance(image, Image.Image):
        return image
    else:
        raise RuntimeError("{} cannot be converted to PIL.Image".format(repr(image)))


def show_slice3d(volumes, slice=0, spacer=0, range=None, image_viewer="eog -n"):
    """
    Display slices of 3D bitmap data.

    Args:
        volumes (list of numpy.ndarray): multiple 3D bitmap data. These data are
            aligned horizontally.
        slice (int): The direction of slicing: 0, 1, or 2 for z, y, x direction.
        spacer (int): The number of pixels between horizontally aligned slices.
        range (None or tuple[int, int]): The range of the slices.
        image_viewer (str): Command line of the image viewer to see slices.
    """
    with TemporaryDirectory() as tmpdir:
        pict_slice3d.write_volume_slices(volumes, slice, spacer, range, tmpdir)
        subprocess.call("{} {}".format(image_viewer, tmpdir), shell=True)
