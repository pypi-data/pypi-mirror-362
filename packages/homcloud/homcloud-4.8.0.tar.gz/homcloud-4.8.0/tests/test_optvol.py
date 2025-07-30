from unittest.mock import MagicMock, ANY
import os

import pytest
import pulp

import homcloud.optvol as optvol
import homcloud.pc_alpha as pc_alpha
import homcloud.abstract_filtration as abstract_filtration
import homcloud.rips as rips
from homcloud.spatial_searcher import SpatialSearcher
from homcloud.geometry_resolver import SimplicialResolver
import homcloud.utils
import homcloud.pict.binarize_nd as binarize_nd


# Tetragon 1
#     4
#  0 --- 1
#  |(9)  |
# 7|  /8 |5
#  | (10)|
#  3 --- 2
#     6
MAP1 = {
    "type": "simplicial",
    "map": [
        [0, []],
        [0, []],
        [0, []],
        [0, []],  # 0, 1, 2, 3
        [1, [1, 0]],
        [1, [2, 1]],
        [1, [3, 2]],  # 4, 5, 6
        [1, [3, 0]],
        [1, [3, 1]],  # 7, 8
        [2, [8, 7, 4]],
        [2, [6, 8, 5]],  # 9, 10
    ],
}

# Tetragon 2
#     4
#  0 --- 1
#  |(10) |
# 9|  /7 |5
#  |  (8)|
#  3 --- 2
#     6
MAP2 = {
    "type": "simplicial",
    "map": [
        [0, []],
        [0, []],
        [0, []],
        [0, []],  # 0, 1, 2, 3
        [1, [1, 0]],
        [1, [2, 1]],
        [1, [3, 2]],  # 4, 5, 6
        [1, [3, 1]],
        [2, [6, 7, 5]],  # 7, 8
        [1, [3, 0]],
        [2, [7, 9, 4]],  # 9, 10
    ],
}


class TestOptimizer(object):
    @pytest.mark.parametrize(
        "boundary_map, birth, death, active_cells, expected",
        [
            (
                MAP1,
                7,
                10,
                [9, 10],
                (
                    [9, 10],
                    {
                        7: [(-1, 9)],
                        8: [(1, 9), (-1, 10)],
                    },
                ),
            ),
            (MAP2, 9, 10, [10], ([10], {9: [(-1, 10)]})),
            (MAP1, 7, 10, [10], ([10], {7: [], 8: [(-1, 10)]})),
        ],
    )
    def test_build_partial_boundary_matrix(self, boundary_map, birth, death, active_cells, expected):
        def is_active_cell(i):
            return i in active_cells

        optimizer = optvol.Optimizer(birth, death, boundary_map, None)
        assert optimizer.build_partial_boundary_matrix(is_active_cell) == expected

    @pytest.mark.parametrize(
        "birth, death, lpvars, partial_map",
        [
            (7, 10, [9, 10], {7: [(-1, 9)], 8: [(1, 9), (-1, 10)]}),
            (7, 10, [10], {7: [], 8: [(-1, 10)]}),
        ],
    )
    def test_build_lp_problem(self, birth, death, lpvars, partial_map):
        optimizer = optvol.Optimizer(birth, death, None, None)
        optimizer.build_lp_problem(lpvars, partial_map)

    @pytest.mark.parametrize(
        "boundary_map, birth, death, active_cells, result_class, expected_volume",
        [
            (MAP1, 7, 10, [9, 10], optvol.Success, [9, 10]),
            (MAP2, 9, 10, [10], optvol.Success, [10]),
            (MAP1, 7, 10, [10], optvol.Failure, None),
        ],
    )
    def test_find(self, boundary_map, birth, death, active_cells, result_class, expected_volume):
        optimizer = optvol.Optimizer(birth, death, boundary_map, optvol.default_lp_solver())
        result = optimizer.find(lambda i: i in active_cells)
        assert isinstance(result, result_class)
        if isinstance(result, optvol.Success):
            assert result.cell_indices == expected_volume
        else:
            assert result.infeasible


class TestPointQuery(object):
    def test_to_dict(self):
        ov_finder = MagicMock(spec=optvol.OptimalVolumeFinder)
        ov_finder.to_query_dict.return_value = {
            "query-target": "optimal-volume",
            "degree": 1,
            "num-retry": 2,
            "cutoff-radius": 0.5,
            "solver-name": "COIN",
            "solver-options": [],
        }
        query = optvol.PointQuery(4.1, 5.2, ov_finder, None)

        assert query.to_dict() == {
            "degree": 1,
            "birth": 4.1,
            "death": 5.2,
            "query-target": "optimal-volume",
            "cutoff-radius": 0.5,
            "num-retry": 2,
            "solver-name": "COIN",
            "solver-options": [],
        }


class TestRectangleQuery(object):
    def test_to_dict(self):
        ov_finder = MagicMock()
        ov_finder.to_query_dict.return_value = {
            "query-target": "optimal-volume",
            "degree": 1,
            "num-retry": 2,
            "cutoff-radius": 0.5,
            "solver-name": "COIN",
            "solver-options": [],
        }
        query = optvol.RectangleQuery((4.1, 4.5), (5.2, 5.8), ov_finder, None, skip_infeasible=False)

        assert query.to_dict() == {
            "degree": 1,
            "birth-range": (4.1, 4.5),
            "death-range": (5.2, 5.8),
            "query-target": "optimal-volume",
            "cutoff-radius": 0.5,
            "num-retry": 2,
            "skip-infeasible": False,
            "solver-name": "COIN",
            "solver-options": [],
        }

    @pytest.mark.parametrize("skip_infeasible", [True, False])
    def test_execute(self, skip_infeasible):
        ov_finder = MagicMock(spec=optvol.OptimalVolumeFinder)
        ov_finder.find.return_value = MagicMock(
            spec=optvol.Failure,
            success=False,
            infeasible=True,
        )
        spatial_searcher = MagicMock(spec=SpatialSearcher)
        spatial_searcher.in_rectangle.return_value = [((1, 2), (3, 4))]
        query = optvol.RectangleQuery((1, 5), (2, 5), ov_finder, spatial_searcher, skip_infeasible=skip_infeasible)
        if skip_infeasible:
            results = query.execute()
            assert results[0] is ov_finder.find.return_value
            assert results[0].pair == (3, 4)
        else:
            with pytest.raises(RuntimeError):
                query.execute()


class TestOptimalVolumeFinder(object):
    def test_to_query_dict(self):
        ovfinder = optvol.OptimalVolumeFinder(
            optvol.RetryOptimizerBuilder(1, None, optvol.default_lp_solver(), None, 0.5, 4)
        )
        wildcard = MagicMock()
        wildcard.__eq__.return_value = True

        d = ovfinder.to_query_dict()
        assert set(d.keys()) == set(
            ["degree", "query-target", "cutoff-radius", "num-retry", "solver-name", "solver-options"]
        )
        assert d["degree"] == 1
        assert d["query-target"] == "optimal-volume"
        assert d["cutoff-radius"] == 0.5
        assert d["num-retry"] == 4


class TestTightenedSubVolumeFinder(object):
    @pytest.mark.parametrize(
        "epsilon, expected",
        [
            (0.1, [9, 10]),
            (1.1, [10]),
        ],
    )
    def test_find(self, epsilon, expected):
        tsvfinder = optvol.TightenedSubVolumeFinder(
            optvol.OptimizerBuilder(1, MAP1, optvol.default_lp_solver()),
            [0, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 3.0, 4.0],
            epsilon,
        )
        result = tsvfinder.find(7, 10, [9, 10])
        assert result.cell_indices == expected


class TestOptimalVolumeTightenedSubVolumeFinder(object):
    @pytest.mark.parametrize(
        "epsilon, expected",
        [
            (0.1, [9, 10]),
            (1.1, [10]),
        ],
    )
    def test_find(self, epsilon, expected):
        optimizer_builder = optvol.OptimizerBuilder(1, MAP1, optvol.default_lp_solver())
        tsvfinder = optvol.OptimalVolumeTightenedSubVolumeFinder(
            optimizer_builder, [0, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 3.0, 4.0], epsilon
        )
        result = tsvfinder.find(7, 10)
        assert result.cell_indices == [9, 10]
        assert result.subvolume.cell_indices == expected


def test_failure_to_dict():
    failure = optvol.Failure(pulp.LpStatusInfeasible)
    failure.pair = (3.1, 7.2)
    assert optvol.failure_to_dict(failure) == {
        "birth-time": 3.1,
        "death-time": 7.2,
        "success": False,
        "status": "Infeasible",
    }


class TestSuccessToDictAlpha(object):
    def test_call(self):
        boundary_map = {3: [0, 1], 4: [1, 2]}.__getitem__
        index_to_simplex = [[0], [1], [2], [0, 1], [1, 2]]
        vertices = [[3, 3], [4, 4], [5, 5]]
        symbols = ["A", "B", "C"]

        coord_resolver = SimplicialResolver(index_to_simplex, vertices, boundary_map)
        symbol_resolver = SimplicialResolver(index_to_simplex, symbols, boundary_map)

        success_to_dict = optvol.SuccessToDictAlpha(
            [10, 11, 12, 13, 14], coord_resolver, symbol_resolver, {4: 1, 3: 2}
        )
        d = success_to_dict(optvol.Success([3, 4]))
        assert set(d.keys()) == set(
            [
                "birth-time",
                "death-time",
                "birth-index",
                "death-index",
                "success",
                "points",
                "simplices",
                "boundary",
                "boundary-points",
                "points-symbols",
                "simplices-symbols",
                "boundary-symbols",
                "boundary-points-symbols",
                "children",
                "tightened-subvolume",
            ]
        )
        assert d["birth-time"] == 11
        assert d["death-time"] == 14
        assert d["birth-index"] == 1
        assert d["death-index"] == 4
        assert d["success"]
        assert d["points"] == [[3, 3], [4, 4], [5, 5]]
        assert d["simplices"] == [[[3, 3], [4, 4]], [[4, 4], [5, 5]]]
        assert d["boundary"] == [[[3, 3]], [[5, 5]]]
        assert d["boundary-points"] == [[3, 3], [5, 5]]
        assert d["points-symbols"] == ["A", "B", "C"]
        assert d["simplices-symbols"] == [["A", "B"], ["B", "C"]]
        assert d["boundary-symbols"] == [["A"], ["C"]]
        assert d["boundary-points-symbols"] == ["A", "C"]
        assert d["children"] == [
            {
                "birth-time": 12,
                "death-time": 13,
                "birth-index": 2,
                "death-index": 3,
            }
        ]
        assert d["tightened-subvolume"] is None


@pytest.mark.integration
class Test_main(object):
    def test_case_tetragon_point_query(self, mocker, datadir, tmpdir):
        mocker.patch("homcloud.utils.invoke_paraview")

        pointcloud = os.path.join(datadir, "tetragon.txt")
        pdgm = str(tmpdir.join("tetragon.pdgm"))
        json = str(tmpdir.join("tetragon-optimal-volume.json"))
        pc_alpha.main(
            pc_alpha.argument_parser().parse_args(
                [
                    "-d",
                    "2",
                    pointcloud,
                    pdgm,
                ]
            )
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-x", "8.5", "-y", "11.5", "-c", "10", "-P", "-T", "optimal-volume", "-j", json, pdgm]
            )
        )
        homcloud.utils.invoke_paraview.assert_called_once_with(ANY, wait=True)

    def test_case_tetragon_rectangle_query(self, mocker, datadir, tmpdir):
        mocker.patch("homcloud.utils.invoke_paraview")

        pointcloud = os.path.join(datadir, "tetragon.txt")
        pdgm = str(tmpdir.join("tetragon.pdgm"))
        json = str(tmpdir.join("tetragon-optimal-volume.json"))
        pc_alpha.main(
            pc_alpha.argument_parser().parse_args(
                [
                    "-d",
                    "2",
                    pointcloud,
                    pdgm,
                ]
            )
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-X", "6:12", "-Y", "6:12", "-c", "10", "-P", "-T", "optimal-volume", "-j", json, pdgm]
            )
        )
        homcloud.utils.invoke_paraview.assert_called_once_with(ANY, wait=True)

    def test_case_abstract(self, datadir, tmpdir):
        input = os.path.join(datadir, "abstract.txt")
        pdgm = str(tmpdir.join("abstract.pdgm"))
        json = str(tmpdir.join("abstract-optimal-volume.json"))
        abstract_filtration.main(
            abstract_filtration.argument_parser().parse_args(
                [
                    "-M",
                    "on",
                    input,
                    pdgm,
                ]
            )
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-x", "1.3", "-y", "2.0", "-T", "optimal-volume", "-j", json, pdgm]
            )
        )

    def test_case_dmatrix(self, datadir, tmpdir):
        input = os.path.join(datadir, "dmatrix.txt")
        pdgm = str(tmpdir.join("dmatrix.pdgm"))
        json = str(tmpdir.join("dmatrix-optimal-volume.json"))
        rips.main(rips.argument_parser().parse_args(["-d", "1", "-M", "on", input, pdgm]))
        optvol.main(optvol.argument_parser().parse_args(["-d", "1", "-x", "1.4", "-y", "1.6", "-j", json, pdgm]))

    def test_case_tetragon_tightened_volume(self, datadir, tmpdir):
        pointcloud = os.path.join(datadir, "tetragon.txt")
        pdgm = str(tmpdir.join("tetragon.pdgm"))
        json = str(tmpdir.join("tetragon-optimal-volume.json"))
        pc_alpha.main(
            pc_alpha.argument_parser().parse_args(
                [
                    "-d",
                    "2",
                    pointcloud,
                    pdgm,
                ]
            )
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-x", "8.5", "-y", "11.5", "-c", "10", "-T", "tightened-volume", "-j", json, pdgm]
            )
        )

    def test_case_tetragon_tightened_subvolume(self, datadir, tmpdir):
        pointcloud = os.path.join(datadir, "tetragon.txt")
        pdgm = str(tmpdir.join("tetragon.pdgm"))
        json = str(tmpdir.join("tetragon-optimal-subvolume.json"))
        pc_alpha.main(
            pc_alpha.argument_parser().parse_args(
                [
                    "-d",
                    "2",
                    pointcloud,
                    pdgm,
                ]
            )
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-x", "8.5", "-y", "11.5", "-c", "10", "-T", "tightened-subvolume", "-j", json, pdgm]
            )
        )

    def test_case_cubical(self, mocker, datadir, tmpdir):
        mocker.patch("homcloud.utils.invoke_paraview")

        bitmap = os.path.join(datadir, "bin.png")
        pdgm = str(tmpdir.join("bin.pdgm"))
        json = str(tmpdir.join("bin-optimal-volume.json"))
        binarize_nd.main(
            binarize_nd.argument_parser().parse_args(["-s", "-C", "-M", "on", "-T", "picture2d", bitmap, "-o", pdgm])
        )
        optvol.main(
            optvol.argument_parser().parse_args(
                ["-d", "1", "-x", "-5.0", "-y", "3.0", "-c", "10", "-T", "optimal-volume", "-j", json, "-P", pdgm]
            )
        )

        homcloud.utils.invoke_paraview.assert_called_with(ANY, wait=True)


def test_find_lp_solver():
    assert type(optvol.find_lp_solver(pulp.getSolver('CPLEX_CMD'), None)) == pulp.CPLEX_CMD
    assert type(optvol.find_lp_solver("coin", {})) == pulp.COIN_CMD
    assert type(optvol.find_lp_solver(None, None)) == type(pulp.LpSolverDefault)
    with pytest.raises(RuntimeError, match="The solver UNKNOWNSOLVER does not exist in PuLP."):
        optvol.find_lp_solver("UNKNOWNSOLVER", {})
        
    assert type(optvol.find_lp_solver("COIN_CMD", {})) == pulp.COIN_CMD
