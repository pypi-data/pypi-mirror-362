from functools import partial
import argparse
import re
from bisect import bisect
from pathlib import Path
import json

import numpy as np
import pulp

from homcloud.argparse_common import parse_range, parse_bool
from homcloud.license import add_argument_for_license
from homcloud.version import __version__
from homcloud.pdgm import PDGM
from homcloud.spatial_searcher import SpatialSearcher
from homcloud.numpyencoder import NumpyEncoder
from homcloud.paraview_interface import SimplexDrawer, CubeDrawer
from homcloud.delegate import forwardable


try:
    from pulp.solvers import PulpSolverError
except ImportError:
    from pulp.apis.core import PulpSolverError


RE_OLD_SOLVER_NAME = re.compile(r"^[a-z\-]+\Z")

def find_lp_solver(solver, options):
    if solver is None:
        return default_lp_solver()

    if isinstance(solver, pulp.apis.LpSolver):
        return solver

    if RE_OLD_SOLVER_NAME.match(solver):
        solver = solver.upper().replace("-", "_")
        if solver == "COIN":
            solver = "COIN_CMD"

    try:
        return pulp.getSolver(solver, **options)
    except PulpSolverError as e:
        raise RuntimeError(str(e))


def default_lp_solver():
    lp_solver = pulp.LpSolverDefault.copy()
    lp_solver.msg = 0
    return lp_solver


def sign_function(boundary_map):
    def sign_simplicial(i, kth):
        return -1 if kth % 2 else 1

    def sign_abstract(i, kth):
        return boundary_map["map"][i][2][kth]

    def sign_cubical(i, kth):
        return -1 if (kth % 4) in (1, 2) else 1

    if boundary_map["type"] == "simplicial":
        return sign_simplicial
    if boundary_map["type"] == "abstract":
        return sign_abstract
    if boundary_map["type"] == "cubical":
        return sign_cubical

    raise RuntimeError("Unknown maptype: {}".format(boundary_map["type"]))


class Optimizer(object):
    def __init__(self, birth, death, boundary_map, lp_solver):
        self.birth = birth
        self.death = death
        self.boundary_map = boundary_map
        self.lp_solver = lp_solver

    def build_partial_boundary_matrix(self, is_active_cell):
        map = self.boundary_map["map"]
        sign = sign_function(self.boundary_map)

        def dim(i):
            return map[i][0]

        degree = dim(self.death) - 1
        partial_map = dict()
        lpvars = []

        for i in range(self.birth, self.death + 1):
            if dim(i) == degree:
                partial_map[i] = list()
            elif dim(i) == degree + 1 and is_active_cell(i):
                lpvars.append(i)
                for kth, j in enumerate(map[i][1]):
                    if j in partial_map:
                        partial_map[j].append((sign(i, kth), i))

        return lpvars, partial_map

    def build_lp_problem(self, lpvar_indices, partial_map):
        prob = pulp.LpProblem("OptimalVolume", pulp.LpMinimize)
        xs = pulp.LpVariable.dicts("x", (lpvar_indices,), -1, 1, "Continuous")
        ys = pulp.LpVariable.dicts("y", (lpvar_indices,), 0, 1, "Continuous")

        prob.setObjective(pulp.lpSum(ys.values()))

        for i in lpvar_indices:
            prob.addConstraint(xs[i] - ys[i] <= 0.0)
            prob.addConstraint(xs[i] + ys[i] >= 0.0)

        for low, constraint in partial_map.items():
            if not constraint:
                continue
            if low == self.birth:
                continue
            prob.addConstraint(pulp.lpSum(s * xs[i] for (s, i) in constraint) == 0)

        prob.addConstraint(xs[self.death] == 1)

        return prob, ys

    def find(self, is_active_cell=lambda _: True):
        lpvars, partial_map = self.build_partial_boundary_matrix(is_active_cell)
        prob, ys = self.build_lp_problem(lpvars, partial_map)
        try:
            status = prob.solve(self.lp_solver)
        except PulpSolverError as err:
            # workaround for cplex and pulp
            if re.search("infeasible", err.args[0]):
                return Failure(pulp.LpStatusInfeasible)
            else:
                raise err

        if status == pulp.LpStatusOptimal:
            return Success(self.optimal_volume_cell_indices(ys))
        else:
            return Failure(status)

    @staticmethod
    def optimal_volume_cell_indices(ys):
        return [index for (index, var) in ys.items() if var.varValue >= 0.00001]


class Success(object):
    def __init__(self, cell_indices):
        self.cell_indices = cell_indices
        self.pair = None
        self.subvolume = None

    success = True
    infeasible = False

    def children(self, death, death_to_birth):
        def valid(c):
            return c != death and c in death_to_birth

        return [(death_to_birth[c], c) for c in self.cell_indices if valid(c)]

    def __repr__(self):
        return "<optvol.Success: {}>".format(self.cell_indices)

    def draw(self, drawer, coord_resolver, volume_color, boundary_color, index, issubvolume=0):
        drawer.draw_cells(
            coord_resolver, self.cell_indices, volume_color, index=index, issimplex=1, issubvolume=issubvolume
        )
        drawer.draw_boundary_cells(
            coord_resolver, self.cell_indices, boundary_color, index=index, isboundary=1, issubvolume=issubvolume
        )
        if self.subvolume:
            self.subvolume.draw(drawer, coord_resolver, drawer.various_colors[2], drawer.various_colors[3], index, 1)


class Failure(object):
    def __init__(self, status):
        self.status = status
        self.pair = None

    success = False

    @property
    def infeasible(self):
        # NOTE: GLPK solver returns pulp.LpStatusUndefined when a problem is infeasible.
        # Therefore pulp.LpStatusUndefined is treated as an infeasible failure.
        # This is an workaround for GLPK.
        return self.status in [pulp.LpStatusInfeasible, pulp.LpStatusUndefined]

    @property
    def message(self):
        msg = pulp.LpStatus[self.status]
        if self.pair:
            return "{} at ({}, {})".format(msg, *self.pair)
        else:
            return msg

    def __repr__(self):
        return "<optvol.Failure: {}>".format(self.message)

    def draw(self, drawer, coord_resolver, volume_color, boundary_color, index):
        pass


class RetryOptimizer(object):
    def __init__(self, optimizer, is_active_cell, times):
        self.optimizer = optimizer
        self.is_active_cell = is_active_cell
        self.times = times

    def find(self):
        for n in range(self.times):
            result = self.optimizer.find(partial(self.is_active_cell, n))
            if result.infeasible:
                pass
            else:
                return result

        return result  # This line always returns infeasible result


def is_active_cell(coord_resolver, center, threshold, n, cell_index):
    if threshold is None:
        return True
    centroid = np.array(coord_resolver.centroid(cell_index))
    return np.linalg.norm(center - centroid) < threshold * (2**n)


class OptimizerBuilder(object):
    def __init__(self, degree, boundary_map, lp_solver):
        self.degree = degree
        self.boundary_map = boundary_map
        self.lp_solver = lp_solver

    def build(self, birth, death):
        return Optimizer(birth, death, self.boundary_map, self.lp_solver)

    def to_query_dict(self):
        return {"degree": self.degree, "solver-name": self.solver_name, "solver-options": self.solver_options}

    @property
    def solver_name(self):
        return self.lp_solver.__class__.__name__

    @property
    def solver_options(self):
        if hasattr(self.lp_solver, "getOptions"):
            return self.lp_solver.getOptions()
        else:
            return None

    @staticmethod
    def from_alpha_pdgm(pdgm, cutoff_radius, retry, lp_solver):
        return RetryOptimizerBuilder(
            pdgm.degree, pdgm.boundary_map_chunk, lp_solver, pdgm.alpha_coord_resolver, cutoff_radius, retry
        )

    @staticmethod
    def from_cubical_pdgm(pdgm, cutoff_radius, retry, lp_solver):
        return RetryOptimizerBuilder(
            pdgm.degree, pdgm.boundary_map_chunk, lp_solver, pdgm.cubical_geometry_resolver, cutoff_radius, retry
        )

    def builder_without_retry(self):
        return self


class RetryOptimizerBuilder(OptimizerBuilder):
    def __init__(self, degree, boundary_map, lp_solver, coord_resolver, cutoff, retry):
        super().__init__(degree, boundary_map, lp_solver)
        self.coord_resolver = coord_resolver
        self.cutoff = cutoff
        self.retry = retry

    def build(self, birth, death):
        return RetryOptimizer(
            super().build(birth, death),
            partial(is_active_cell, self.coord_resolver, self.coord_resolver.centroid(death), self.cutoff),
            self.retry,
        )

    def to_query_dict(self):
        return dict(
            super().to_query_dict(),
            **{
                "cutoff-radius": self.cutoff,
                "num-retry": self.retry,
            },
        )

    def builder_without_retry(self):
        return OptimizerBuilder(self.degree, self.boundary_map, self.lp_solver)


def bisect_tightened(b, d, index_to_level, epsilon):
    k = bisect(index_to_level, index_to_level[b] + epsilon, lo=b, hi=d + 1)
    assert k <= d, "epsilon must be smaller than lifetime"
    # 次の行で k - 1 を使っているのは，Optimizer.build_lp_problemで
    # if low == self.birth:
    #      continue
    # となっている部分と整合性を取るため
    return k - 1


class TightenedVolumeFinder(object):
    def __init__(self, optimizer_builder, index_to_level, epsilon):
        self.optimizer_builder = optimizer_builder
        self.index_to_level = index_to_level
        self.epsilon = epsilon

    def find(self, birth, death):
        k = bisect_tightened(birth, death, self.index_to_level, self.epsilon)
        return self.optimizer_builder.build(k, death).find()

    def to_query_dict(self):
        return dict(self.optimizer_builder.to_query_dict(), **{"query-target": "tightened-volume"})


class OptimalVolumeFinder(object):
    def __init__(self, optimizer_builder):
        self.optimizer_builder = optimizer_builder

    def find(self, birth, death):
        return self.optimizer_builder.build(birth, death).find()

    def to_query_dict(self):
        return dict(self.optimizer_builder.to_query_dict(), **{"query-target": "optimal-volume"})


class TightenedSubVolumeFinder(object):
    def __init__(self, optimizer_builder, index_to_level, epsilon):
        self.optimizer_builder = optimizer_builder
        self.index_to_level = index_to_level
        self.epsilon = epsilon

    def find(self, birth, death, optimal_volume_cells):
        k = bisect_tightened(birth, death, self.index_to_level, self.epsilon)
        return self.optimizer_builder.build(k, death).find(
            partial(self.is_active_cell_for_tightend_subvolume, birth, optimal_volume_cells)
        )

    def is_active_cell_for_tightend_subvolume(self, birth, optimal_volume_cells, cell_index):
        return cell_index in optimal_volume_cells and (
            self.index_to_level[birth] + self.epsilon < self.index_to_level[cell_index]
        )


class OptimalVolumeTightenedSubVolumeFinder(object):
    def __init__(self, optimizer_builder, index_to_level, epsilon):
        self.optimizer_builder = optimizer_builder
        self.tsv_finder = TightenedSubVolumeFinder(optimizer_builder.builder_without_retry(), index_to_level, epsilon)

    def find(self, birth, death):
        optimal_volume = self.optimizer_builder.build(birth, death).find()
        if not optimal_volume.success:
            return optimal_volume
        optimal_volume.subvolume = self.tsv_finder.find(birth, death, optimal_volume.cell_indices)
        return optimal_volume

    def to_query_dict(self):
        return dict(self.optimizer_builder.to_query_dict(), **{"query-target": "tightened-subvolume"})


class PointQuery(object):
    def __init__(self, birth_time, death_time, ovfinder, spatial_searcher):
        self.birth_time = birth_time
        self.death_time = death_time
        self.ovfinder = ovfinder
        self.spatial_searcher = spatial_searcher

    def to_dict(self):
        return dict(
            self.ovfinder.to_query_dict(),
            **{
                "birth": self.birth_time,
                "death": self.death_time,
            },
        )

    def execute(self):
        pair_indices, pair = self.spatial_searcher.nearest_pair(self.birth_time, self.death_time)
        result = self.ovfinder.find(*pair_indices)
        result.pair = pair
        return [result]

    @staticmethod
    def valid_args(args):
        return args.x is not None and args.y is not None


class RectangleQuery(object):
    def __init__(self, birth_range, death_range, ovfinder, spatial_searcher, skip_infeasible):
        self.birth_range = birth_range
        self.death_range = death_range
        self.ovfinder = ovfinder
        self.spatial_searcher = spatial_searcher
        self.skip_infeasible = skip_infeasible

    def to_dict(self):
        return dict(
            self.ovfinder.to_query_dict(),
            **{
                "birth-range": self.birth_range,
                "death-range": self.death_range,
                "skip-infeasible": self.skip_infeasible,
            },
        )

    def pairs_in_rectangle(self):
        return self.spatial_searcher.in_rectangle(
            self.birth_range[0], self.birth_range[1], self.death_range[0], self.death_range[1]
        )

    def execute(self):
        results = []
        for pair_indices, pair in self.pairs_in_rectangle():
            result = self.ovfinder.find(*pair_indices)
            result.pair = pair
            if result.success:
                results.append(result)
            elif result.infeasible and self.skip_infeasible:
                results.append(result)
            else:
                raise RuntimeError(result.message)
        return results

    @staticmethod
    def valid_args(args):
        return args.x_range and args.y_range


class SuccessToDictBase(object):
    def __init__(self, index_to_level, death_to_birth):
        self.index_to_level = index_to_level
        self.death_to_birth = death_to_birth

    def children(self, death, success):
        ret = []
        for b, d in success.children(death, self.death_to_birth):
            birth_time = self.index_to_level[b]
            death_time = self.index_to_level[d]
            if birth_time == death_time:
                pass
            ret.append(
                {
                    "birth-time": birth_time,
                    "death-time": death_time,
                    "birth-index": b,
                    "death-index": d,
                }
            )

        return ret

    def basedict(self, success, death):
        birth = self.death_to_birth[death]

        return {
            "birth-time": self.index_to_level[birth],
            "death-time": self.index_to_level[death],
            "birth-index": birth,
            "death-index": death,
            "success": True,
            "tightened-subvolume": self(success.subvolume),
        }


class SuccessToDictAlpha(SuccessToDictBase):
    def __init__(self, index_to_level, coord_resolver, symbol_resolver, death_to_birth):
        super().__init__(index_to_level, death_to_birth)
        self.coord_resolver = coord_resolver
        self.symbol_resolver = symbol_resolver

    @staticmethod
    def from_pdgm(pdgm):
        return SuccessToDictAlpha(
            pdgm.index_to_level, pdgm.alpha_coord_resolver, pdgm.alpha_symbol_resolver, pdgm.death_index_to_birth_index
        )

    def __call__(self, success):
        if success is None:
            return None

        death = max(success.cell_indices)

        return dict(
            self.basedict(success, death),
            **{
                "points": self.coord_resolver.resolve_vertices(success.cell_indices),
                "simplices": self.coord_resolver.resolve_cells(success.cell_indices),
                "boundary": self.coord_resolver.resolve_cells(
                    self.coord_resolver.boundary_cells(success.cell_indices)
                ),
                "boundary-points": self.coord_resolver.resolve_vertices(
                    self.coord_resolver.boundary_cells(success.cell_indices)
                ),
                "points-symbols": self.symbol_resolver.resolve_vertices(success.cell_indices),
                "simplices-symbols": self.symbol_resolver.resolve_cells(success.cell_indices),
                "boundary-symbols": self.symbol_resolver.resolve_cells(
                    self.symbol_resolver.boundary_cells(success.cell_indices)
                ),
                "boundary-points-symbols": self.symbol_resolver.resolve_vertices(
                    self.symbol_resolver.boundary_cells(success.cell_indices)
                ),
                "children": self.children(death, success),
            },
        )


class SuccessToDictAbstract(SuccessToDictBase):
    def __init__(self, index_to_level, abs_resolver, death_to_birth):
        super().__init__(index_to_level, death_to_birth)
        self.abs_resolver = abs_resolver

    def __call__(self, success):
        if success is None:
            return None

        death = max(success.cell_indices)
        return dict(
            self.basedict(success, death),
            **{
                "cells": self.abs_resolver.resolve_cells(success.cell_indices),
                "boundary": self.abs_resolver.resolve_cells(self.abs_resolver.boundary_cells(success.cell_indices)),
                "children": self.children(death, success),
            },
        )

    @staticmethod
    def from_pdgm(pdgm):
        return SuccessToDictAbstract(
            pdgm.index_to_level, pdgm.abstract_geometry_resolver, pdgm.death_index_to_birth_index
        )


class SuccessToDictSimplicial(SuccessToDictBase):
    def __init__(self, index_to_level, symbol_resolver, death_to_birth):
        super().__init__(index_to_level, death_to_birth)
        self.symbol_resolver = symbol_resolver

    def __call__(self, success):
        if success is None:
            return None

        death = max(success.cell_indices)
        return dict(
            self.basedict(success, death),
            **{
                "points-symbols": self.symbol_resolver.resolve_vertices(success.cell_indices),
                "simplices-symbols": self.symbol_resolver.resolve_cells(success.cell_indices),
                "boundary-symbols": self.symbol_resolver.resolve_cells(
                    self.symbol_resolver.boundary_cells(success.cell_indices)
                ),
                "boundary-points-symbols": self.symbol_resolver.resolve_vertices(
                    self.symbol_resolver.boundary_cells(success.cell_indices)
                ),
                "children": self.children(death, success),
            },
        )

    @staticmethod
    def from_pdgm(pdgm):
        return SuccessToDictSimplicial(
            pdgm.index_to_level, pdgm.simplicial_symbol_resolver, pdgm.death_index_to_birth_index
        )


class SuccessToDictCubical(SuccessToDictBase):
    def __init__(self, index_to_level, cube_resolver, death_to_birth):
        super().__init__(index_to_level, death_to_birth)
        self.cube_resolver = cube_resolver

    @staticmethod
    def from_pdgm(pdgm):
        return SuccessToDictCubical(
            pdgm.index_to_level, pdgm.cubical_geometry_resolver, pdgm.death_index_to_birth_index
        )

    def __call__(self, success):
        if success is None:
            return None

        death = max(success.cell_indices)

        return dict(
            self.basedict(success, death),
            **{
                "points": self.cube_resolver.resolve_vertices(success.cell_indices),
                "cubes": self.cube_resolver.resolve_cells(success.cell_indices),
                "boundary": self.cube_resolver.resolve_cells(self.cube_resolver.boundary_cells(success.cell_indices)),
                "boundary-points": self.cube_resolver.resolve_vertices(
                    self.cube_resolver.boundary_cells(success.cell_indices)
                ),
                "children": self.children(death, success),
            },
        )


def failure_to_dict(failure):
    return {
        "birth-time": failure.pair[0],
        "death-time": failure.pair[1],
        "success": False,
        "status": pulp.LpStatus[failure.status],
    }


class OptimalVolumeError(Exception):
    """Base class for expretions in homcloud.optimal_volume"""

    def __init__(self, message, code):
        self.message = message
        self.code = code


class InfeasibleError(OptimalVolumeError):
    """Exception raised for errors for LpstatusInfeasible."""

    def __init__(self, message, code):
        super().__init__(message, code)


def argument_parser():
    p = argparse.ArgumentParser()
    p.description = "Copmutes optimal volumes and variants of stable volumes"
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)

    tp = p.add_argument_group("target")
    tp.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    tp.add_argument("-x", type=float, help="birth time of the pair")
    tp.add_argument("-y", type=float, help="death time of the pair")
    tp.add_argument("-X", "--x-range", type=parse_range, help="birth time of the pair")
    tp.add_argument("-Y", "--y-range", type=parse_range, help="death time of the pair")

    op = p.add_argument_group("output options")
    op.add_argument("-j", "--json-output", help="output in json format")
    op.add_argument("-P", "--invoke-paraview", default=False, action="store_true", help="invoke paraview")

    cp = p.add_argument_group("computation parameters")
    cp.add_argument(
        "-T",
        "--type",
        default="optimal-volume",
        help="target type (*optimal-volume*, tightened-volume," " or tightened-subvolume",
    )
    cp.add_argument("-e", "--epsilon", type=float, default=0.0, help="tighened-volume/subvolume epsilon")
    cp.add_argument("-c", "--cutoff-radius", type=float, help="cut-off radius in R^n")
    cp.add_argument("-n", "--retry", type=int, default=1, help="number of retry")
    cp.add_argument("--skip-infeasible", default=False, type=parse_bool, help="skip infeasible (on/*off*)")

    sp = p.add_argument_group("solver parameters")
    sp.add_argument("--solver", help="LP solver name")
    sp.add_argument("-O", "--option", action="append", default=[], help="options for LP solver")

    p.add_argument("input", help="input filename")
    return p


def build_spatial_searcher(diagram):
    return SpatialSearcher(
        list(zip(zip(diagram.birth_indices, diagram.death_indices), zip(diagram.births, diagram.deaths))),
        diagram.births,
        diagram.deaths,
    )


@forwardable
class Main(object):
    def __init__(self, args):
        self.args = args

    __delegator_definitions__ = {"args": ["input", "degree", "cutoff_radius", "retry"]}

    def run(self):
        if self.input_is_pdgm:
            with PDGM.open(self.input, self.degree) as pdgm:
                self.setup_pdgm(pdgm)

        ovfinder = self.build_ovfinder()
        query = self.build_query(ovfinder)
        results = query.execute()

        if self.is_json_output:
            self.write_json(query, results)
        if self.args.invoke_paraview:
            self.invoke_paraview(results)

    @property
    def input_is_pdgm(self):
        return Path(self.input).suffix == ".pdgm"

    @property
    def lp_solver(self):
        return find_lp_solver(self.args.solver, self.args.option)

    @property
    def is_json_output(self):
        return self.args.json_output

    @property
    def points(self):
        return self.coord_resolver.vertices

    def setup_pdgm(self, pdgm):
        if pdgm.filtration_type == "alpha":
            self.setup_alpha_pdgm(pdgm)
        elif pdgm.filtration_type == "abstract":
            self.setup_abstract_pdgm(pdgm)
        elif pdgm.filtration_type == "simplicial":
            self.setup_simplicial_pdgm(pdgm)
        elif pdgm.filtration_type == "cubical":
            self.setup_cubical_pdgm(pdgm)
        else:
            raise RuntimeError("Unknown pdgm type: {}".format(pdgm.filtration_type))
        self.filtration_type = pdgm.filtration_type
        self.spatial_searcher = build_spatial_searcher(pdgm)
        self.index_to_level = pdgm.index_to_level

    def setup_alpha_pdgm(self, pdgm):
        self.optimizer_builder = OptimizerBuilder.from_alpha_pdgm(pdgm, self.cutoff_radius, self.retry, self.lp_solver)
        self.success_to_dict = SuccessToDictAlpha.from_pdgm(pdgm)
        self.coord_resolver = pdgm.alpha_coord_resolver

    def setup_abstract_pdgm(self, pdgm):
        self.optimizer_builder = OptimizerBuilder(self.degree, pdgm.boundary_map_chunk, self.lp_solver)
        self.success_to_dict = SuccessToDictAbstract.from_pdgm(pdgm)

    def setup_simplicial_pdgm(self, pdgm):
        self.optimizer_builder = OptimizerBuilder(self.degree, pdgm.boundary_map_chunk, self.lp_solver)
        self.success_to_dict = SuccessToDictSimplicial.from_pdgm(pdgm)

    def setup_cubical_pdgm(self, pdgm):
        self.optimizer_builder = OptimizerBuilder.from_cubical_pdgm(
            pdgm, self.cutoff_radius, self.retry, self.lp_solver
        )
        self.success_to_dict = SuccessToDictCubical.from_pdgm(pdgm)
        self.cube_resolver = pdgm.cubical_geometry_resolver

    def build_ovfinder(self):
        type = self.args.type
        if type == "optimal-volume":
            return OptimalVolumeFinder(self.optimizer_builder)
        elif type == "tightened-volume":
            return TightenedVolumeFinder(self.optimizer_builder, self.index_to_level, self.args.epsilon)
        elif type == "tightened-subvolume":
            return OptimalVolumeTightenedSubVolumeFinder(
                self.optimizer_builder, self.index_to_level, self.args.epsilon
            )
        else:
            raise RuntimeError("Unknown type: {}".format(type))

    def build_query(self, ovfinder):
        if PointQuery.valid_args(self.args):
            return PointQuery(self.args.x, self.args.y, ovfinder, self.spatial_searcher)
        elif RectangleQuery.valid_args(self.args):
            return RectangleQuery(
                self.args.x_range, self.args.y_range, ovfinder, self.spatial_searcher, self.args.skip_infeasible
            )
        else:
            raise RuntimeError("Invalid query")

    def write_json(self, query, results):
        with open(self.args.json_output, "w") as f:
            json.dump(self.build_jsondict(query, results), f, cls=NumpyEncoder)

    def build_jsondict(self, query, results):
        def result_to_dict(result):
            if result.success:
                return self.success_to_dict(result)
            else:
                return failure_to_dict(result)

        return {"format-version": 2.0, "query": query.to_dict(), "result": [result_to_dict(r) for r in results]}

    def invoke_paraview(self, results):
        if self.filtration_type == "alpha":
            drawer = self.draw_volumes_for_alpha(results)
        elif self.filtration_type == "cubical":
            drawer = self.draw_volumes_for_cubical(results)
        else:
            raise RuntimeError("Paraview visualization is not available")

        drawer.invoke()

    def draw_volumes_for_alpha(self, results):
        drawer = drawer_for_alpha(self.points)
        draw_volumes(drawer, results, self.coord_resolver)
        return drawer

    def draw_volumes_for_cubical(self, results):
        drawer = drawer_for_cubical(self.cube_resolver.shape)
        draw_volumes(drawer, results, self.cube_resolver)
        return drawer


def drawer_for_alpha(points):
    return SimplexDrawer(4, points, {"index": None, "isboundary": 0, "issimplex": 0, "issubvolume": 0})


def drawer_for_cubical(shape):
    return CubeDrawer(4, shape, {"index": None, "isboundary": 0, "issimplex": 0, "issubvolume": 0})


def draw_volumes(drawer, results, geom_resolver):
    for i, volume in enumerate(results):
        volume.draw(drawer, geom_resolver, drawer.various_colors[0], drawer.various_colors[1], i)


def main(args=None):
    Main(args or argument_parser().parse_args()).run()


if __name__ == "__main__":
    main()
