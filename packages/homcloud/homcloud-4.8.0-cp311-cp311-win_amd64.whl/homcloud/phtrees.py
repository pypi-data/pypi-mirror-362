import argparse
import json
import os
from tempfile import TemporaryDirectory

from cached_property import cached_property
import numpy as np

from homcloud.version import __version__
from homcloud.argparse_common import parse_range
from homcloud.pdgm_format import PDGMReader
from homcloud.pdgm import PDGM
from homcloud.spatial_searcher import SpatialSearcher
from homcloud.paraview_interface import SimplexDrawer
import homcloud.utils as utils


class Volume(object):
    def birth_simplex(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_cell(self.birth_index)

    def death_simplex(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_cell(self.death_index)

    def boundary(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_boundary(self.volume_indices())

    def boundary_vertices(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_boundary_vertices(self.volume_indices())

    def vertices(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_vertices(self.volume_indices())

    def simplices(self, by="coordinates"):
        return self.get_geometry_resolver(by).resolve_cells(self.volume_indices())

    def volume_indices(self):
        return (n.death_index for n in self.volume_nodes)

    def to_dict(self):
        return {
            "birth-index": self.birth_index,
            "death-index": self.death_index,
            "birth-time": self.birth_time(),
            "death-time": self.death_time(),
            "boundary": self.boundary(),
            "boundary-by-symbols": self.boundary("symbols"),
            "boundary-vertices": self.boundary_vertices(),
            "boundary-vertices-by-symbols": self.boundary_vertices("symbols"),
            "vertices": self.vertices(),
            "vertices-by-symbols": self.vertices("symbols"),
            "simplices": self.simplices(),
            "simplices-by-symbols": self.simplices("symbols"),
            "children": self.children_dicts(),
        }

    def to_child_dict(self):
        return {
            "birth-index": self.birth_index,
            "death-index": self.death_index,
            "birth-time": self.birth_time(),
            "death-time": self.death_time(),
            "children": self.children_dicts(),
        }

    def children_dicts(self):
        return [child.to_child_dict() for child in self.children]

    def draw_volume(self, drawer, color, **thvalues):
        drawer.draw_boundary_cells(self.get_geometry_resolver(), self.volume_indices(), color, **thvalues)

    def __repr__(self):
        return "{}.{}(birth_time={}, death_time={})".format(
            self.__class__.__module__, self.__class__.__name__, self.birth_time(), self.death_time()
        )


class Node(Volume):
    def __init__(self, birth_index, death_index, parent_death, trees=None):
        self.birth_index = birth_index
        self.death_index = death_index
        self.parent_death = parent_death
        self.trees = trees
        self.volume_cache = None
        self.children = []

    def isroot(self):
        return self.parent_death == np.inf

    def birth_time(self):
        return self.trees.index_to_level[self.birth_index]

    def death_time(self):
        return self.trees.index_to_level[self.death_index]

    def lifetime(self):
        return self.death_time() - self.birth_time()

    @cached_property
    def volume_nodes(self):
        volume_nodes = []

        def iter(n):
            volume_nodes.append(n)
            for child in n.children:
                iter(child)

        iter(self)
        return volume_nodes

    def volume_size(self):
        return len(self.volume_nodes)

    def stable_volume(self, epsilon, cls=None):
        cls = cls or StableVolume
        return cls(self, [child for child in self.children if child.birth_time() > self.birth_time() + epsilon])

    def get_geometry_resolver(self, by="coordinates"):
        return self.trees.get_geometry_resolver(by)


class StableVolume(Volume):
    def __init__(self, root, children):
        self.root = root
        self.children = children
        self.volume_cache = None

    @property
    def trees(self):
        return self.root.trees

    @property
    def birth_index(self):
        return self.root.birth_index

    @property
    def death_index(self):
        return self.root.death_index

    def birth_time(self):
        return self.root.birth_time()

    def death_time(self):
        return self.root.death_time()

    def lifetime(self):
        return self.death_time() - self.birth_time()

    def get_geometry_resolver(self, by="coordinates"):
        return self.root.get_geometry_resolver(by)

    @cached_property
    def volume_nodes(self):
        volume_nodes = [self.root]
        for child in self.children:
            volume_nodes.extend(child.volume_nodes)
        return volume_nodes


class PHTrees(object):
    def __init__(self, nodes, index_to_level=None, coord_resolver=None, symbol_resolver=None, nodeclass=Node):
        assert nodes is not None
        self.nodes = {
            death_index: nodeclass(birth_index, death_index, parent_death, self)
            for (birth_index, death_index, parent_death) in nodes
        }
        self.index_to_level = index_to_level
        self.coord_resolver = coord_resolver
        self.symbol_resolver = symbol_resolver
        self.roots = []
        self.build_tree()

    @staticmethod
    def from_pdgmreader(reader):
        return PHTrees(
            reader.load_simple_chunk("phtrees"),
            reader.load_simple_chunk("index_to_level"),
        )

    @staticmethod
    def from_pdgm(pdgm, nodeclass=Node):
        return PHTrees(
            pdgm.pdgmreader.load_simple_chunk("phtrees"),
            pdgm.index_to_level,
            pdgm.get_geometry_resolver("coordinates"),
            pdgm.get_geometry_resolver("symbols"),
            nodeclass,
        )

    def build_tree(self):
        for node in self.nodes.values():
            if node.isroot():
                self.roots.append(node)
            else:
                self.nodes[node.parent_death].children.append(node)

    def parent_of(self, node):
        if node.isroot():
            return None
        return self.nodes[node.parent_death]

    def get_geometry_resolver(self, type):
        if type == "coordinates":
            return self.coord_resolver
        if type == "symbols":
            return self.symbol_resolver
        raise ValueError("Unknown type: {}".format(type))


class Query(object):
    def __init__(self, query, volume_getter, searcher, input_dim=None, query_ancestors=False, query_children=False):
        self.query = query
        self.volume_getter = volume_getter
        self.searcher = searcher
        self.input_dim = input_dim
        self.query_ancestors = query_ancestors
        self.query_children = query_children
        self.result = []

    @property
    def degree(self):
        return self.phtrees.degree

    def to_dict(self):
        return {
            "format-version": 2,
            "query": {
                "query-type": "signle",
                "query-target": self.volume_getter.query_target_name,
                "degree": self.input_dim - 1,
                "birth": self.query[0],
                "death": self.query[1],
                "ancestor-pairs": self.query_ancestors,
                "query-children": self.query_children,
            },
            "dimension": self.input_dim,
            "result": [r.to_dict() for r in self.result],
        }


class PointQuery(Query):
    def invoke(self):
        death_index = self.searcher.nearest_pair(*self.query)
        self.result = [self.volume_getter(death_index)]


class RectangleQuery(Query):
    def invoke(self):
        death_indices = self.searcher.in_rectangle(
            self.query[0][0], self.query[0][1], self.query[1][0], self.query[1][1]
        )
        self.result = [self.volume_getter(i) for i in death_indices]


class GetOptimalVolume(object):
    def __init__(self, phtrees):
        self.phtrees = phtrees

    def __call__(self, death_index):
        return self.phtrees.nodes[death_index]

    query_target_name = "optimal-volume"


class GetStableVolume(object):
    def __init__(self, phtrees, epsilon):
        self.phtrees = phtrees
        self.epsilon = epsilon

    def __call__(self, death_index):
        return self.phtrees.nodes[death_index].stable_volume(self.epsilon)

    query_target_name = "stable-volume"


def main(args=None):
    if not args:
        args = argument_parser().parse_args()

    with PDGMReader.open(args.input) as reader:
        assert reader.metadata["filtration_type"] in ["alpha", "alpha-phtrees"]
        input_dim = reader.metadata["dim"]
        pdgm = PDGM(reader, input_dim - 1)
        spatial_searcher = SpatialSearcher(pdgm.death_indices, pdgm.births, pdgm.deaths)
        phtrees = PHTrees.from_pdgm(pdgm)

        if is_point_query(args):
            query_class = PointQuery
            query_xy = (args.x, args.y)
        elif is_rectangle_query(args):
            query_class = RectangleQuery
            query_xy = (args.x_range, args.y_range)

        if args.stable_volume:
            volume_getter = GetStableVolume(phtrees, args.stable_volume)
        else:
            volume_getter = GetOptimalVolume(phtrees)

        query = query_class(query_xy, volume_getter, spatial_searcher, input_dim)

        query.invoke()

        if args.json_output:
            with open(args.json_output, "w") as f:
                json.dump(query.to_dict(), f)

        if args.invoke_paraview:
            with TemporaryDirectory() as tmpdir:
                path = os.path.join(tmpdir, "tmp.vtk")
                drawer = SimplexDrawer(len(query.result), phtrees.coord_resolver.vertices, {})
                for i, r in enumerate(query.result):
                    r.draw_volume(drawer, i)
                drawer.output(path)
                utils.invoke_paraview(path, wait=True)


def is_point_query(args):
    return args.x is not None and args.y is not None


def is_rectangle_query(args):
    return args.x_range is not None and args.y_range is not None


def argument_parser():
    p = argparse.ArgumentParser(description="")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-x", type=float, help="birth time of the pair")
    p.add_argument("-y", type=float, help="death time of the pair")
    p.add_argument("-X", "--x-range", type=parse_range, help="birth time of the pair")
    p.add_argument("-Y", "--y-range", type=parse_range, help="death time of the pair")
    p.add_argument("-j", "--json-output", help="output in json format")
    p.add_argument(
        "-P", "--invoke-paraview", default=False, action="store_true", help="invoke paraview for visualization"
    )
    p.add_argument("-S", "--stable-volume", type=float, help="stable volume epsilon")
    p.add_argument("input", help="input pht file")
    return p


if __name__ == "__main__":
    main()
