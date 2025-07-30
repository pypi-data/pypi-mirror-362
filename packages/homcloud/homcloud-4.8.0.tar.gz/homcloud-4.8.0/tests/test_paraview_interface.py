import io
import unittest.mock
import tempfile

import numpy as np
import pytest

import homcloud.paraview_interface as pv
import homcloud.interface as hc
from homcloud.paraview_interface import CubeDrawer, LinesDrawer, SparseCubeDrawer


def build_mock_new_index():
    idx = 0

    def mock_new_index():
        nonlocal idx
        idx += 1
        return idx

    return mock_new_index


class Test_ParaViewCubeDrawer(object):
    def test_coord2index(self):
        drawer = CubeDrawer(10, [20, 30, 40], {})
        assert drawer.coord2index([5, 12, 38]) == 38 + 12 * 40 + 5 * 40 * 30

    def test_index2coord(self):
        drawer = CubeDrawer(10, [20, 30, 40], {})
        assert drawer.index2coord(38 + 12 * 40 + 5 * 40 * 30) == [5, 12, 38]

    def test_dvs(self):
        assert np.allclose(
            CubeDrawer.dvs([0, 1, 1]),
            [
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, 0],
                [0, 1, 1],
            ],
        )

    def test_dls(self):
        assert np.allclose(CubeDrawer.dls([0, 1, 1]), [[0, 1, 0], [0, 0, 1]])
        assert np.allclose(CubeDrawer.dls([1, 1, 1]), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])


class TestParaViewSparseCubeDrawer(object):
    def test_prepare_points(self):
        drawer = SparseCubeDrawer(2, 3, {})
        drawer.points.append([0, 1, 2])
        indices, dvs = drawer.prepare_points([3, 4, 5], [0, 1, 1])
        assert len(drawer.points) == 5
        assert np.all(indices == [[[1, 2], [3, 4]], [[0, 0], [0, 0]]])
        assert np.all(np.array(dvs) == [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1]])


class TestParaViewLinesDrawer(object):
    def test_draw_loop(self, tmpdir):
        drawer = LinesDrawer(1, {"value": None})
        drawer.draw_loop([(0, 1), (1, 1), (1, 0), (0, 1)], 0, value="12")
        with tempfile.NamedTemporaryFile("w") as f:
            drawer.write(f)


def test_write_code():
    with unittest.mock.patch("homcloud.paraview_interface.new_index", build_mock_new_index()):
        n1 = pv.VTK("foobar.vtk").threshold("value", (0.8, 1.2))
        n2 = pv.VTK("baz.vtk", "Bazbaz")
        out = io.StringIO()
        pv.write_python_code(out, [n1, n2], (1, 0.5, 1))
        assert out.getvalue() == (
            "from paraview.simple import *\n"
            "s1 = LegacyVTKReader(FileNames=r'foobar.vtk', guiName=r'foobar.vtk')\n"
            "s2 = Threshold(s1)\n"
            "Show(s2)\n"
            "s2.Scalars = ['CELLS', r'value']\n"
            "s2.ThresholdRange = (0.8, 1.2)\n"
            "dp = GetDisplayProperties(s2)\n"
            "s3 = LegacyVTKReader(FileNames=r'baz.vtk', guiName=r'Bazbaz')\n"
            "Show(s3)\n"
            "dp = GetDisplayProperties(s3)\n"
            "view = GetActiveView()\n"
            "view.Background = [1, 0.5, 1]\n"
            "Render()\n"
        )


class TestPointCloud(object):
    def test_write_code(self):
        with unittest.mock.patch("homcloud.paraview_interface.new_index", build_mock_new_index()):
            n = (
                pv.PointCloud("pointcloud.txt", dim=2, delimiters=" ", gui_name="PC")
                .color_by(field=3)
                .set_pointsize(4)
            )
            out = io.StringIO()
            n.write_code(out, set(), True)
            assert out.getvalue() == (
                "s = CSVReader(FileName=r'pointcloud.txt', FieldDelimiterCharacters=' ', guiName=r'PC', HaveHeaders=0)\n"  # noqa: E501
                "s1 = TableToPoints(s, XColumn='Field 0', YColumn='Field 1', ZColumn='Field 0', a2DPoints=1)\n"
                "Show(s1)\n"
                "dp = GetDisplayProperties(s1)\n"
                "dp.Representation = 'Points'\n"
                "dp.PointSize = 4\n"
                "dp.LookupTable = MakeBlueToRedLT(*s1.PointData[r'Field 3'].GetRange())\n"
                "dp.ColorArrayName = [r'POINTS', r'Field 3']\n"
            )


@pytest.mark.filterwarnings("ignore:HomCloud's Paraview interface is now deprecated.")
def test_show(mocker):
    invoke_paraview = mocker.patch("homcloud.utils.invoke_paraview")

    def invoke_paraview_side_effect(*args, wait=False, finalize=None):
        finalize()

    invoke_paraview.side_effect = invoke_paraview_side_effect

    pointcloud = np.array(
        [
            [0.0, 0.0, 0.0],
            [8.0, 0.0, 0.0],
            [5.0, 6.0, 0.0],
            [4.0, 2.0, 6.0],
        ]
    )
    pdlist = hc.PDList.from_alpha_filtration(pointcloud, save_boundary_map=True, save_phtrees=True)
    optimal_volume = pdlist[1].pair(0).optimal_volume()
    phtrees = pdlist[2].load_phtrees()
    phtrees_node = phtrees.pair_node_nearest_to(5, 8)
    voxeldata = np.random.uniform(0, 100, (5, 5, 5))
    pv.show(
        [
            pv.PointCloud.from_array(pointcloud, gui_name="PC"),
            pv.PointCloud.from_array(pointcloud).threshold("Field 1", (0.5, 0.8)),
            pv.PolyLine(pointcloud, gui_name="PL"),
            pv.VoxelData(voxeldata, gui_name="VX"),
            optimal_volume,
            optimal_volume.to_pvnode().set_color((1, 0, 1)),
            phtrees.to_pvnode_from_nodes([phtrees_node]),
            phtrees_node,
        ]
    )
