"""
*This module is now deprecated. Please use pyvista instead.*


This module provides the paraview interface from homcloud.interface module.

The basic model of this module is "pipeline" model. A data object is
filtered by the chain of pipeline nodes, and the result is shown.
The objects of :class:`PipelineNode` correspond the node of the pipeline,
and you can adjust visualization by these objects.

You can use many methods of :class:`PipelineNode` to adjust the visualization,
and you can construct a new pipeline node by the following methods:

* :meth:`PipelineNode.threshold`
* :meth:`PipelineNode.clip_sphere`

Todo:

* Add clip_box method

"""

import numbers
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
import itertools
import math
import warnings

import numpy as np

import homcloud.utils as utils
import homcloud.pict.pict3d_vtk as pict3d_vtk
from homcloud.delegate import forwardable


class ParaViewColors(object):
    def __init__(self, n_colors):
        self.n_colors = n_colors
        self.color_scalars = np.linspace(0, 1.0, n_colors + 3)

    @property
    def various_colors(self):
        return self.color_scalars[:-3]

    def birth_color(self):
        return self.color_scalars[-2]

    def death_color(self):
        return self.color_scalars[-1]

    def output_lookup_table(self, f):
        f.write("LOOKUP_TABLE color_table {}\n".format(self.n_colors + 3))
        for x in np.linspace(0.0, 1.0, self.n_colors + 1):
            self.output_various_colors(f, x)
        self.output_birthdeath_colors(f)

    def output_various_colors(self, f, relative_value):
        f.write("{} {} {} 1.0\n".format(*self.color_spec(relative_value)))

    @staticmethod
    def color_spec(x):
        y, k = math.modf(x * 6)
        if k == 0 or k == 6:
            return (1, y, 0)
        if k == 1:
            return (1 - y, 1, 0)
        if k == 2:
            return (0, 1, y)
        if k == 3:
            return (0, 1 - y, 1)
        if k == 4:
            return (y, 0, 1)
        if k == 5:
            return (1, 0, 1 - y)
        return (0.5, 0.5, 0.5)

    @staticmethod
    def output_birthdeath_colors(f):
        f.write("0.8 0.8 0.8 1.0\n")
        f.write("1.0 1.0 1.0 1.0\n")


# TODO: this class requires unit tests
@forwardable
class BaseDrawer(object):
    """
    This class represents the generator of a VTK file.

    Args:
        n_colors (int): The number of colors
        column_spec (dict[str, float or None]): The pairs of the names of
            the columns and default values.
    """

    def __init__(self, n_colors, column_spec):
        self.pvcolors = ParaViewColors(n_colors)
        self.lines = []
        self.colors = []
        self.columns = {name: list() for name in column_spec}
        self.default_values = {
            name: default_val for (name, default_val) in column_spec.items() if default_val is not None
        }
        self.vertices = []

    __delegator_definitions__ = {"pvcolors": ["various_colors", "birth_color", "death_color"]}

    def draw_line(self, p, q, color, **threshold_values):
        self.lines.append((p, q))
        self.append_attributes(color, threshold_values)

    def append_attributes(self, color, threshold_values):
        self.colors.append(color)
        for key in self.columns:
            self.columns[key].append(self.get_threshold_value(threshold_values, key))

    def get_threshold_value(self, values, key):
        if key in values:
            return values[key]
        else:
            return self.default_values[key]

    def invoke(self, wait=True):
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tmp.vtk")
            self.output(path)
            utils.invoke_paraview(path, wait=wait)

    def output(self, path):
        with open(path, "w") as f:
            self.write(f)

    def write(self, f):
        self.output_header(f)
        self.output_polygon_data(f)
        self.output_line_colors(f)
        self.pvcolors.output_lookup_table(f)
        self.output_columns(f)

    @staticmethod
    def output_header(f):
        f.write("# vtk DataFile Version 2.0\n")
        f.write("volume optimal cycles\n")
        f.write("ASCII\n")

    def output_polygon_data(self, f):
        f.write("DATASET POLYDATA\n")
        self.output_points(f)
        self.output_vertices(f)
        self.output_lines(f)
        self.output_polygons(f)

    def output_vertices(self, f):
        if not self.vertices:
            return
        f.write("VERTICES {} {}\n".format(self.num_vertices(), self.num_vertices() * 2))
        for v in self.vertices:
            f.write("1 {}\n".format(v))
        f.write("\n")

    def output_lines(self, f):
        pass

    def output_polygons(self, f):
        pass

    def output_line_colors(self, f):
        f.write("CELL_DATA {}\n".format(len(self.colors)))
        f.write("SCALARS colors float 1\n")
        f.write("LOOKUP_TABLE color_table\n")
        for n in self.colors:
            f.write("{}\n".format(n))

    def output_columns(self, f):
        for key, values in self.columns.items():
            f.write("SCALARS {} float 1\n".format(key))
            f.write("LOOKUP_TABLE default\n")
            for value in values:
                f.write("{}\n".format(value))

    def num_lines(self):
        return len(self.lines)

    def num_vertices(self):
        return len(self.vertices)

    @staticmethod
    def reformat_point(point):
        if len(point) == 3:
            return point
        if len(point) == 2:
            return (point[0], point[1], 0)


class BaseCellDrawer:
    def draw_cells(self, geom_resolver, cells, color, **values):
        for cell in cells:
            self.draw_cell(geom_resolver, cell, color, **values)

    def draw_boundary_cells(self, geom_resolver, cells, color, **values):
        self.draw_cells(geom_resolver, geom_resolver.boundary_cells(cells), color, **values)


class SimplexDrawer(BaseDrawer, BaseCellDrawer):
    def __init__(self, n_colors, points, column_names):
        super().__init__(n_colors, column_names)
        self.points = [self.reformat_point(p) for p in points]

    def draw_cell(self, geom_resolver, cell_index, color, **threshold_values):
        self.draw_simplex(geom_resolver.index_to_simplex[cell_index], color, **threshold_values)

    def draw_simplex(self, simplex, color, **threshold_values):
        for edge in itertools.combinations(simplex, 2):
            self.draw_line(edge[0], edge[1], color, **threshold_values)

    def draw_vertex(self, vertex, color, **threshold_values):
        self.vertices.append(vertex)
        self.append_attributes(color, threshold_values)

    def draw_all_vertices(self, color, **threshold_values):
        for i in range(len(self.points)):
            self.draw_vertex(i, color, **threshold_values)

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")

    def num_points(self):
        return len(self.points)


class CubeDrawer(BaseDrawer, BaseCellDrawer):
    def __init__(self, n_colors, dims, column_names):
        super().__init__(n_colors, column_names)
        self.dims = dims
        assert len(dims) in [2, 3]

    @staticmethod
    def dvs(non_deg):
        n = len(non_deg)
        dvs = []

        def iter(k, dv):
            if k == n:
                dvs.append(dv.copy())
            else:
                if non_deg[k]:
                    for b in [0, 1]:
                        dv[k] = b
                        iter(k + 1, dv)
                else:
                    iter(k + 1, dv)

        iter(0, np.zeros(n, dtype=int))
        return dvs

    @staticmethod
    def dls(non_deg):
        n = len(non_deg)
        dls = []
        for k in range(n):
            if non_deg[k]:
                dl = np.zeros(n, dtype=int)
                dl[k] = 1
                dls.append(dl)
        return dls

    def draw_cell(self, geom_resolver, cell_index, color, **threshold_values):
        coords, nondeg = geom_resolver.decode_index(cell_index)
        self.draw_cube(coords, nondeg, color, **threshold_values)

    def draw_cube(self, coord, non_deg, color, **threshold_values):
        for dv in self.dvs(non_deg):
            for dl in self.dls(non_deg):
                if np.max(dv + dl) < 2:
                    self.draw_line(coord + dv, coord + dv + dl, color, **threshold_values)

    def ndim(self):
        return len(self.dims)

    def coord2index(self, coord):
        index = 0
        for k in range(self.ndim()):
            index = index * self.dims[k] + coord[k]
        return index

    def index2coord(self, index):
        coord = [0] * self.ndim()
        for k in reversed(range(self.ndim())):
            index, coord[k] = divmod(index, self.dims[k])
        return coord

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for k in range(self.num_points()):
            coord = self.index2coord(k)
            f.write("{} {} {}\n".format(*self.reformat_point(coord)))
        f.write("\n")

    def num_points(self):
        return int(np.prod(self.dims))

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(self.coord2index(line[0]), self.coord2index(line[1])))
        f.write("\n")


class SparseCubeDrawer(BaseDrawer):
    def __init__(self, n_colors, ndim, column_names):
        super().__init__(n_colors, column_names)
        self.ndim = ndim
        self.points = []
        assert ndim in [2, 3]

    def draw_cube(self, coord, non_deg, color, **threshold_values):
        indices, dvs = self.prepare_points(coord, non_deg)
        for dv in dvs:
            for dl in CubeDrawer.dls(non_deg):
                if np.max(dv + dl) < 2:
                    self.draw_line(indices[tuple(dv)], indices[tuple(dv + dl)], color, **threshold_values)

    def prepare_points(self, coord, non_deg):
        dvs = CubeDrawer.dvs(non_deg)
        indices = np.zeros([2] * self.ndim, dtype=int)
        for dv in dvs:
            indices[tuple(dv)] = len(self.points)
            self.points.append(np.flip(dv + coord))
        return indices, dvs

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def num_points(self):
        return len(self.points)

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")


class SparseBitmapDrawer(BaseDrawer):
    def __init__(self, n_colors, column_names):
        super().__init__(n_colors, column_names)
        self.vertices = []
        self.n_voxels = 0

    def draw_voxel(self, coord, color, **threshold_values):
        self.n_voxels += 1
        for d1 in (-0.4, 0.4):
            for d2 in (-0.4, 0.4):
                for d3 in (-0.4, 0.4):
                    r = (coord[0] + d1, coord[1] + d2, coord[2] + d3)
                    self.vertices.append(r)
        self.append_attributes(color, threshold_values)

    def output(self, path):
        with open(path, "w") as f:
            self.output_header(f)
            self.output_voxel_data(f)
            self.output_line_colors(f)
            self.pvcolors.output_lookup_table(f)
            self.output_columns(f)

    def output_voxel_data(self, f):
        f.write("DATASET UNSTRUCTURED_GRID\n")
        f.write("POINTS {} double\n".format(len(self.vertices)))
        for r in self.vertices:
            f.write(" ".join(map(str, r)))
            f.write("\n")
        f.write("CELLS {} {}\n".format(self.n_voxels, 9 * self.n_voxels))
        for n in range(self.n_voxels):
            f.write("8 {}\n".format(" ".join(map(str, range(n * 8, (n + 1) * 8)))))
        f.write("CELL_TYPES {}\n".format(self.n_voxels))
        for _ in range(self.n_voxels):
            f.write("11\n")


class LinesDrawer(BaseDrawer):
    def __init__(self, n_colors, column_names):
        super().__init__(n_colors, column_names)
        self.points = []
        self.point2index = dict()
        self.lines = []

    def index_of(self, p):
        if p in self.point2index:
            return self.point2index[p]
        else:
            index = len(self.points)
            self.point2index[p] = index
            self.points.append(p)
            return index

    def draw_line(self, p1, p2, color, **threshold_values):
        index1 = self.index_of(p1)
        index2 = self.index_of(p2)
        self.lines.append((index1, index2))
        self.append_attributes(color, threshold_values)

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            point = self.reformat_point(point)
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def num_points(self):
        return len(self.points)

    def output_lines(self, f):
        f.write("LINES {} {}\n".format(self.num_lines(), self.num_lines() * 3))
        for line in self.lines:
            f.write("2 {} {}\n".format(line[0], line[1]))
        f.write("\n")

    def draw_loop(self, path, color, **threshold_values):
        for k in range(len(path) - 1):
            self.draw_line(path[k], path[k + 1], color, **threshold_values)


class PolyLineDrawer(BaseDrawer):
    def __init__(self, n_colors, points, column_names):
        super().__init__(n_colors, column_names)
        self.points = [self.reformat_point(p) for p in points]
        self.append_attributes(0, {})

    def output_points(self, f):
        f.write("POINTS {} double\n".format(self.num_points()))
        for point in self.points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def output_lines(self, f):
        f.write("LINES 1 {}\n".format(self.num_points() + 1))
        f.write("{} ".format(self.num_points()))
        for k in range(self.num_points()):
            f.write(" {}".format(k))
        f.write("\n\n")

    def num_points(self):
        return len(self.points)


class SurfaceDrawer(BaseDrawer):
    def __init__(self, n_colors, surface, column_names):
        super().__init__(n_colors, column_names)
        self.num_triagnles = len(surface)
        self.surface = surface
        for _ in range(self.num_triagnles):
            self.append_attributes(0, {})

    def output_points(self, f):
        points = np.array(self.surface).reshape(3 * self.num_triagnles, 3)
        f.write("POINTS {} double\n".format(self.num_triagnles * 3))
        for point in points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))
        f.write("\n")

    def output_polygons(self, f):
        f.write("POLYGONS {} {}\n".format(self.num_triagnles, self.num_triagnles * 4))
        for k in range(self.num_triagnles):
            f.write("3 {} {} {}\n".format(3 * k, 3 * k + 1, 3 * k + 2))


@forwardable
class TempFile(object):
    def __init__(self, suffix):
        self.named_tempfile = NamedTemporaryFile("w+", suffix=suffix, delete=False)
        self.cleanup_done = False

    __delegator_definitions__ = {"named_tempfile": ["name", "close", "write"]}

    def cleanup(self):
        self.close()
        if not self.cleanup_done:
            os.unlink(self.name)
            self.cleanup_done = True

    def __del__(self):
        self.cleanup()

    # NOTE: __enter__ and __exit__ are not implemented since
    # in this module with statement is used to the class


class PipelineNode(object):
    """This class represents elements in a pipeline in ParaView.

    This class is the base class for paraview interface classes.
    You should not create an instance of this class directly.
    """

    def __init__(self, parent=None):
        self.index = new_index()
        self.parent = parent
        self._representation = None
        self.opacity = None
        self.color = None
        self.color_field = None
        self.colorbar_range = None
        self.pointsize = None
        self.linewidth = None

    def variable(self):
        return "s" + str(self.index)

    def to_paraview_node(self):
        """Returns self."""
        return self

    def representation(self):
        if self._representation:
            return self._representation
        if self.parent is None:
            return False
        return self.parent.representation()

    def write_code(self, out, already_written, isleaf):
        if self.variable() in already_written:
            return
        already_written.add(self.variable())
        if self.parent:
            self.parent.write_code(out, already_written, False)
        self.write_constructor(out)
        if isleaf:
            out.write("Show({})\n".format(self.variable()))
        self.write_specialized_code(out, already_written)
        if isleaf:
            self.write_displayproperty_code(out, already_written)

    def write_displayproperty_code(self, out, already_written):
        out.write("dp = GetDisplayProperties({})\n".format(self.variable()))
        if self.representation():
            out.write("dp.Representation = '{}'\n".format(self.representation()))
        if self.opacity is not None:
            out.write("dp.Opacity = {}\n".format(self.opacity))
        if self.pointsize is not None:
            out.write("dp.PointSize = {}\n".format(self.pointsize))
        if self.color_field is not None:
            self.write_color_filed(out)
        if self.color is not None:
            out.write("dp.AmbientColor = ({}, {}, {})\n".format(*self.color))
            out.write("dp.DiffuseColor = ({}, {}, {})\n".format(*self.color))
            out.write("dp.ColorArrayName = [dp.ColorArrayName[0], r'']\n")
        if self.linewidth is not None:
            out.write("dp.LineWidth = {}\n".format(self.linewidth))

    def write_color_filed(self, out):
        if self.colorbar_range is None:
            out.write(
                "dp.LookupTable = MakeBlueToRedLT(*{}."
                "{}[r'{}'].GetRange())\n".format(self.variable(), self.data_attr_name(), self.color_field)
            )
        else:
            out.write("dp.LookupTable = MakeBlueToRedLT({}, {})\n".format(*self.colorbar_range))
        out.write("dp.ColorArrayName = [r'{}', r'{}']\n".format(self.color_array_type(), self.color_field))

    def write_specialized_code(self, out, already_written):
        pass

    def threshold(self, field, range):
        """
        Create a new pipeline node for thresholding whose parent
        is `self`.

        Only the elements whose `field` are in the `range` when
        the returned object is passed to :meth:`show`.

        Args:
            field (string): The name of the field which have the
                thresholded value.
            range (tuple[float, float] or float): The upper and lower bounds
                of the values.
                If an float number is given, the threshold is (range, range).

        Returns:
            Threshold: A new PipelineNode object for thresholding.

        """
        if isinstance(range, numbers.Number):
            range = (range, range)
        return Threshold(self, field, range)

    def clip_sphere(self, center, radius, inside_out=True):
        """
        Create a new pipeline node to clip the object with a
        sphere shape.

        Args:
            center (tuple[float, float, float]): The center of the
                clipping sphere
            radius (float): The radius of the clipping sphere
            inside_out (bool): If True, only the elements
                *in* the shpere are shown.
                If False, only the elements *outside* of the sphere is
                shown.

        Returns:
            SphereClip: A new PipelineNode object for sphere clipping.

        """
        return SphereClip(self, center, radius, inside_out)

    def color_by(self, field, range=None):
        """
        Set the coloring by field name.

        Args:
            field (string or int): The name of the field.
            range (tuple[float, float] or None): The upper and lower bounds
                of the colorbar. If None, the minimal and maximal values
                of the field are used.
        Returns:
            self
        """
        if isinstance(field, int):
            field = "Field {}".format(field)
        self.color_field = field
        self.colorbar_range = range
        return self

    def data_attr_name(self):
        return self.parent.data_attr_name()

    def color_array_type(self):
        return self.parent.color_array_type()

    def set_opacity(self, opacity):
        """
        Set the opacity.

        * 0.0 - completely transparent
        * 1.0 - completely opaque

        Args:
            opacity (float): The opacity.

        Returns:
            self
        """
        self.opacity = opacity
        return self

    def set_color(self, color):
        """
        Set the color.

        Args:
            color (tuple[float, float, float]): The RGB values (0.0 to 1.0)

        Returns:
            self
        """
        self.color = color
        return self

    def set_pointsize(self, size):
        """
        Set the pointsize.

        Args:
            pointsize (float): The size of the points

        Returns:
            self
        """
        self.pointsize = size
        return self

    def set_representation(self, rep):
        if rep not in ["Wireframe", "Points", "Surface", "Surface With Edges"]:
            raise ValueError("Representation {} is not acceptable".format(rep))
        self._representation = rep
        return self

    def set_linewidth(self, width):
        """
        Set the linewidth.

        Args:
            width (float): The width of the lines

        Returns:
            self
        """
        self.linewidth = width
        return self

    def debug_print(self):
        write_python_code(sys.stdout, [self])
        return self

    def cleanup(self):
        if self.parent:
            self.parent.cleanup()


class VTK(PipelineNode):
    """
    This class represents a VTK data source in paraview.
    """

    def __init__(self, path, gui_name=None, file=None):
        super().__init__()
        self.path = path
        self.gui_name = gui_name if gui_name is not None else path
        self.file = file

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    def write_constructor(self, out):
        out.write(
            "{} = LegacyVTKReader(FileNames=r'{}',"
            " guiName=r'{}')\n".format(self.variable(), self.path, self.gui_name)
        )

    def data_attr_name(self):
        return "CellData"

    def color_array_type(self):
        return "CELLS"


class XMLVTI(PipelineNode):
    """
    This class represents a VTI data source in XML format in paraview.
    """

    def __init__(self, path, gui_name, file=None):
        super().__init__()
        self.path = path
        self.gui_name = gui_name if gui_name is not None else path
        self.file = file
        self._representation = "Surface"
        self.color_field = "value"

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    def write_constructor(self, out):
        out.write(
            "{} = XMLImageDataReader(FileName=r'{}', "
            "guiName=r'{}')\n".format(self.variable(), self.path, self.gui_name)
        )

    def data_attr_name(self):
        return "CellData"

    def color_array_type(self):
        return "CELLS"


def VoxelData(array, gui_name=None, offsets=[0, 0, 0]):
    """
    Returns :class:`PipelineNode` object representing a voxel data.

    Args:
        array (numpy.ndarray): An array.
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Returns:
        VTK: A pipeline node object
    """
    f = TempFile(".vti")
    pict3d_vtk.write_vti_xmlfile(f, array, offsets)
    f.close()
    return XMLVTI(f.name, gui_name, f)


def PolyLine(array, gui_name=None):
    """
    Returns :class:`PipelineNode` object representing a polyline.

    Args:
        array (numpy.ndarray): An array of points.
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Returns:
        VTK: A pipeline node object
    """
    f = TempFile(".vtk")
    drawer = PolyLineDrawer(2, array, {})
    drawer.write(f)
    f.close()
    return VTK(f.name, gui_name, f).set_representation("Wireframe")


def Lines(lines, gui_name=None):
    f = TempFile(".vtk")
    drawer = LinesDrawer(1, {})
    for line in lines:
        drawer.draw_line(tuple(line[0]), tuple(line[1]), 0)
    drawer.write(f)
    f.close()
    return VTK(f.name, gui_name, f).set_representation("Wireframe")


def Surface(surface, gui_name=None):
    f = TempFile(".vtk")
    drawer = SurfaceDrawer(2, surface, {})
    drawer.write(f)
    f.close()
    return VTK(f.name, gui_name, f).set_representation("Surface")


class PointCloud(PipelineNode):
    """
    This class represents a pointcloud data source in paraview.

    Args:
        path (string): The filepath of the pointcloud.
        dim (int): The dimension of the space in which the pointcloud lives.
        delimiter (string): The delimiter of elements in a pointcloud file.
           If you want to show a CSV file, please specify ",".
        gui_name (string or None): The name shown in Pipeline Browser
            in paraview's GUI.

    Notes:
       This is constructed by CSVReader and TableToPoints.
    """

    def __init__(self, path, dim=3, delimiters=" ", gui_name=None, file=None):
        super().__init__()
        self.path = path
        self.dim = dim
        self.delimiters = delimiters
        self.gui_name = gui_name or self.path
        self.file = file
        assert dim in [2, 3]

    def cleanup(self):
        if self.file:
            self.file.cleanup()

    @staticmethod
    def from_array(array, dim=3, gui_name=None):
        """
        Construct a pipeline node for pointcloud from an ndarray object.

        Args:
            array (nupmy.ndarray): The pointcloud data.
            dim (int): The dimension of the space in which the
                pointcloud lives.
            gui_name (string): The name shown in Pipeline Browser in paraview's
                GUI.

        Returns:
            PointCloud: A pipeline node object.
        """
        f = TempFile(".txt")
        np.savetxt(f, array)
        f.close()
        return PointCloud(f.name, dim, " ", gui_name, f)

    def representation(self):
        return "Points"

    def write_constructor(self, out):
        def quote(s):
            return s.translate(
                {
                    "\t": "\\t",
                    "\n": "\\n",
                }
            )

        out.write(
            "s = CSVReader(FileName=r'{}', FieldDelimiterCharacters='{}',"
            " guiName=r'{}', HaveHeaders=0)\n".format(self.path, quote(self.delimiters), self.gui_name)
        )

        out.write(self.table_to_points_template().format(self.variable()))

    def table_to_points_template(self):
        if self.dim == 3:
            return "{} = TableToPoints(s, XColumn='Field 0', YColumn='Field 1', ZColumn='Field 2')\n"
        elif self.dim == 2:
            return "{} = TableToPoints(s, XColumn='Field 0', YColumn='Field 1', ZColumn='Field 0', a2DPoints=1)\n"

    def data_attr_name(self):
        return "PointData"

    def color_array_type(self):
        return "POINTS"


class Threshold(PipelineNode):
    """
    This class represents a pipeline node for thresholding.

    You should construct the instance of this class by
    :meth:`PipelineNode.threshold`.
    """

    def __init__(self, parent, field, range):
        super().__init__(parent)
        self.field = field
        self.range = range

    def write_constructor(self, out):
        out.write("{} = Threshold({})\n".format(self.variable(), self.parent.variable()))

    def write_specialized_code(self, out, already_written):
        out.write("{}.Scalars = ['CELLS', r'{}']\n".format(self.variable(), self.field))
        out.write("{}.ThresholdRange = ({}, {})\n".format(self.variable(), self.range[0], self.range[1]))


class SphereClip(PipelineNode):
    """
    This class represents a pipeline node for sphere clipping.

    You should construct the instance of this class
    by :meth:`PipelineNode.clip_sphere`.
    """

    def __init__(self, parent, center, radius, inside_out=True):
        super().__init__(parent)
        self.center = center
        self.radius = radius
        self.inside_out = inside_out

    def write_constructor(self, out):
        out.write(
            "{} = Clip({}, InsideOut={}, ClipType='Sphere')\n".format(
                self.variable(),
                self.parent.variable(),
                int(self.inside_out),
            )
        )

    def write_specialized_code(self, out, already_written):
        out.write("{}.ClipType.Center = [{}, {}, {}]\n".format(self.variable(), *self.center))
        out.write("{}.ClipType.Radius = {}\n".format(self.variable(), self.radius))


def write_python_code(out, sources, bgcolor):
    """
    Write a python code generated by `sources` to `out`.

    Args:
        out (io-like): The output IO object.
        sources (list of PipelineNode): Pipeline nodes to be output.
    """
    already_written = set()
    out.write("from paraview.simple import *\n")
    for source in sources:
        source.write_code(out, already_written, True)
    out.write("view = GetActiveView()\n")
    if bgcolor:
        out.write("view.Background = [{}, {}, {}]\n".format(*bgcolor))
    out.write("Render()\n")


def show(sources, path=None, wait=True, bgcolor=None):
    """
    Shows `sources` by invoking paraview.

    Args:
        sources (list of PipelineNode): Pipeline nodes to be output.
        path (string or None): The output filename. If this parameter
            is None, a temporary filepath is generated and use it.
            If `path` is not None, the file remains after stopping paraview.
        wait (bool): If True, this function returns after paraview stops.
            If False, this function returns immediately after
            paraview is invoked by using backgroup process mechanism.
        bgcolor (None or tuple[float, float, float]): Background color.
    """
    warnings.warn(
        "HomCloud's Paraview interface is now deprecated. " "The feature is planned to removed in the future."
    )
    f = open(path, "w") if path else TempFile(".py")
    nodes = [s.to_paraview_node() for s in sources]
    write_python_code(f, nodes, bgcolor)
    f.close()
    # sp.run(["cmd.exe", "/k", "type", path])

    def finalize():
        if isinstance(f, TempFile):
            f.cleanup()
        for node in nodes:
            node.cleanup()

    utils.invoke_paraview("--script={}".format(f.name), wait=wait, finalize=finalize)


current_index = 0


def new_index():
    global current_index
    current_index += 1
    return current_index
