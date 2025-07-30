import math
import struct
from collections import defaultdict
from operator import attrgetter

from cached_property import cached_property
import msgpack

from homcloud.alpha_shape2 import AlphaShape2 as AlphaShape2Base
from homcloud.alpha_shape3 import AlphaShape3 as AlphaShape3Base
from homcloud.periodic_alpha_shape2 import PeriodicAlphaShape2 as PeriodicAlphaShape2Base
from homcloud.periodic_alpha_shape3 import PeriodicAlphaShape3 as PeriodicAlphaShape3Base
from homcloud.base_filtration import Filtration
from homcloud.pdgm_format import PDGMWriter, BinaryChunk, AlphaInformationChunk
import homcloud.phat_ext as phat
import homcloud.build_phtrees as build_phtrees


class AlphaShape(object):
    @staticmethod
    def build(points, dim, weighted=False, use_relative_homology=False, periodicity=None):
        if dim == 2:
            if periodicity is None:
                return AlphaShape2(points, weighted, use_relative_homology)
            else:
                return PeriodicAlphaShape2(points, weighted, use_relative_homology, periodicity)
        if dim == 3:
            if periodicity is None:
                return AlphaShape3(points, weighted, use_relative_homology)
            else:
                return PeriodicAlphaShape3(points, weighted, use_relative_homology, periodicity)

        raise ValueError("dimension of a point cloud must be 2 or 3")

    def create_filtration(self, squared=True, symbols=None, save_boundary_map=False, save_phtrees=False):
        simplices = [
            Simplex(alpha_simplex, i, squared)
            for (i, alpha_simplex) in enumerate(sorted(self.simplices, key=attrgetter("birth_radius")))
        ]

        dict_simplices = {simplex.key: simplex for simplex in simplices}
        return AlphaFiltration(
            self.coordinates,
            self.weights,
            squared,
            self.periodicity,
            simplices,
            dict_simplices,
            self.dim,
            symbols,
            save_boundary_map,
            save_phtrees,
        )

    def subsets(self):
        def group_of_simplex(simplex):
            """
            If all vertices of the simplex belong to the same group,
            returns an integer which is the name of the group.
            Otherwise, returns None.
            """
            group_names = [v.group_name for v in simplex.vertices()]
            if group_names[0] == -1:
                return None
            if all(gn == group_names[0] for gn in group_names):
                return group_names[0]
            else:
                return None

        def group_by(collection, key):
            groups = defaultdict(list)
            for item in collection:
                k = key(item)
                if k is not None:
                    groups[k].append(item)
            return groups

        return {
            group_name: AlphaSubset(group_name, self.coordinates, self.weights, self.periodicity, simplices, self.dim)
            for (group_name, simplices) in group_by(self.simplices, group_of_simplex).items()
        }

    def all_subsets_acyclic(self):
        return all(subset.isacyclic() for subset in self.subsets().values())

    def check_subsets_acyclicity(self):
        for subset in self.subsets().values():
            if not subset.isacyclic():
                message = "Subset {} is not acyclic".format(subset.group_name)
                raise RuntimeError(message)

    def become_partial_shape(self):
        for subset in self.subsets().values():
            for simplex in subset.simplices:
                simplex.birth_radius = -math.inf

    @staticmethod
    def simplex_key(simplex):
        return tuple(sorted(v.vertex_index for v in simplex.vertices()))


class AlphaShape3(AlphaShape3Base, AlphaShape):
    def __init__(self, points, weighted, rel_homology):
        super().__init__(points, weighted, rel_homology)
        self.weights = points[:, 3] if weighted else None
        self.coordinates = points[:, 0:3]
        self.simplices = self.vertices() + self.edges() + self.facets() + self.cells()

    @property
    def dim(self):
        return 3

    @property
    def periodicity(self):
        return None


class AlphaShape2(AlphaShape2Base, AlphaShape):
    def __init__(self, points, weighted, rel_homology):
        super().__init__(points, weighted, rel_homology)
        self.weights = points[:, 2] if weighted else None
        self.coordinates = points[:, 0:2]
        self.simplices = self.vertices() + self.edges() + self.faces()

    @property
    def dim(self):
        return 2

    @property
    def periodicity(self):
        return None


class PeriodicAlphaShape2(PeriodicAlphaShape2Base, AlphaShape):
    def __init__(self, points, weighted, rel_homology, periodicity):
        if weighted:
            raise ValueError("Weighted 2D alpha shape is not support due to the limitation of CGAL")
        ((xmin, xmax), (ymin, ymax)) = periodicity
        super().__init__(points, False, rel_homology, xmin, xmax, ymin, ymax)
        self.weights = None
        self.coordinates = points[:, :2]
        self.simplices = self.vertices() + self.edges() + self.faces()
        self.periodicity = periodicity

    @property
    def dim(self):
        return 2


class PeriodicAlphaShape3(PeriodicAlphaShape3Base, AlphaShape):
    def __init__(self, points, weighted, rel_homology, periodicity):
        ((xmin, xmax), (ymin, ymax), (zmin, zmax)) = periodicity
        super().__init__(points, weighted, rel_homology, xmin, xmax, ymin, ymax, zmin, zmax)
        self.coordinates = points[:, 0:3]
        self.weights = points[:, 3] if weighted else None
        self.simplices = self.vertices() + self.edges() + self.facets() + self.cells()
        self.periodicity = periodicity

    @property
    def dim(self):
        return 3


class AlphaSubset(AlphaShape):
    def __init__(self, group_name, points, weights, periodicity, simplices, dim):
        self.group_name = group_name
        self.periodicity = periodicity
        self.simplices = simplices
        self.coordinates = points
        self.weights = weights
        self.dim = dim

    def isacyclic(self):
        return self.create_filtration().isacyclic()


class Simplex(object):
    """A class representing simplex"""

    def __init__(self, alpha_simplex, index, squared=True):
        self.index = index  # NOTE: This index is different from vertex's index
        self.key = AlphaShape.simplex_key(alpha_simplex)
        self.birth_radius = self.normalize_radius(alpha_simplex.birth_radius, squared)
        self.isvertex = alpha_simplex.isvertex()

    def __repr__(self):
        return "alpha_filtration.Simplex(index={}, key={}, birth_radius={})".format(
            self.index, self.key, self.birth_radius
        )

    def boundary_keys(self):
        """Return list of frozensets of vertices of indices of boundary simplices"""
        if self.isvertex:
            return []
        return [self.key[0:n] + self.key[n + 1 :] for n in range(len(self.key))]

    def signed_boundary_keys(self):
        def plusminus_alternative(length):
            return [(-1 if k % 2 else 1) for k in range(length)]

        unsigned = self.boundary_keys()
        return list(zip(plusminus_alternative(len(unsigned)), unsigned))

    @staticmethod
    def normalize_radius(r, squared):
        return r if squared else math.copysign(math.sqrt(abs(r)), r)

    @property
    def dim(self):
        """Return the dimension of the simplex"""
        return len(self.key) - 1


class AlphaFiltration(Filtration):
    def __init__(
        self,
        points,
        point_weights,
        squared,
        periodicity,
        simplices,
        dict_simplices,
        dim,
        symbols,
        save_boundary_map,
        save_phtrees,
    ):
        """
        Args:
        points -- list of N-d point coordinates
        point_weights -- weights of points, None if weight is not given
        squared -- whether all radii are squared
        periodicity -- None or list of (min, max)
        simplices -- list of simplices, must be sorted by their birth_radius
        dict_simplices -- dictiorary: simplex.key -> simplex
        dim: -- dimension of the alpha filtration
        symbols -- list of symbols, or None
        save_boundary_map -- bool
        save_phTrees -- bool
        """
        self.points = points
        self.point_weights = point_weights
        self.squared = squared
        self.periodicity = periodicity
        self.simplices = simplices
        self.dict_simplices = dict_simplices
        self.dim = dim
        self.symbols = symbols
        self.save_boundary_map = save_boundary_map
        self.save_phtrees = save_phtrees

    def alpha_information_chunk(self):
        return AlphaInformationChunk(self.points.shape[0], self.periodicity, self.points_weighted, self.squared)

    def compute_pdgm(self, f, algorithm=None, output_suppl_info=True):
        writer = PDGMWriter(f, "alpha", self.dim)
        pairs, boundary_map_byte_sequence = self.compute_pairs(algorithm)
        writer.save_pairs(pairs, self.index_to_level, output_suppl_info)
        writer.append_chunk(self.alpha_information_chunk())

        if output_suppl_info:
            writer.append_simple_chunk("index_to_level", self.index_to_level)
            writer.append_simple_chunk("vertex_symbols", self.symbols)
            writer.append_simple_chunk("vertex_coordintes", self.points.tolist())
            writer.append_simple_chunk("index_to_simplex", self.index_to_simplex)

        if self.save_boundary_map:
            writer.append_chunk(BinaryChunk("boundary_map", boundary_map_byte_sequence))
        if self.save_phtrees:
            boundary_map = msgpack.unpackb(boundary_map_byte_sequence, raw=False).get("map")
            writer.append_simple_chunk("phtrees", self.build_phtrees(boundary_map))
        writer.write()

    @cached_property
    def index_to_level(self):
        return [simplex.birth_radius for simplex in self.simplices]

    @cached_property
    def index_to_simplex(self):
        return [list(simplex.key) for simplex in self.simplices]

    @property
    def points_weighted(self):
        return self.point_weights is not None

    def build_phat_matrix(self):
        matrix = phat.Matrix(len(self.simplices), self.boundary_map_style())
        for simplex in self.simplices:
            boundary = [self.dict_simplices[key].index for key in simplex.boundary_keys()]
            matrix.set_dim_col(simplex.index, simplex.dim, boundary)

        return matrix

    def boundary_map_style(self):
        return "simplicial" if self.save_boundary_map else "none"

    def build_phtrees(self, boundary_map):
        return build_phtrees.PHTrees(self.dim, boundary_map).to_list()

    def isacyclic(self):
        matrix = self.build_phat_matrix()
        matrix.reduce_twist()
        return self.count_essential_pairs(matrix.birth_death_pairs()) == 1

    @staticmethod
    def count_essential_pairs(pairs):
        return sum([1 for pair in pairs if pair[2] is None])

    @staticmethod
    def favorite_algorithm():
        return "phat-twist"

    def write_dipha_complex(self, output, use_index=True):
        """ "Write dipha bondary matrix data to file"""

        def write_dipha_header(num_simplices):
            """Write magic number, type, boundary/coboundary,
            num_simplices, and dimension
            """
            output.write(struct.pack("qqqqq", 8067171840, 0, 0, num_simplices, self.dim))

        def write_dimensions():
            """Write dimensions of each simplex"""
            for simplex in self.simplices:
                output.write(struct.pack("q", simplex.dim))

        def write_birth_radii():
            """Write birth radii for each simplex"""
            for simplex in self.simplices:
                if use_index:
                    output.write(struct.pack("d", simplex.index))
                else:
                    output.write(struct.pack("d", simplex.birth_radius))

        def write_boundary_map_sizes():
            n = 0
            for simplex in self.simplices:
                output.write(struct.pack("q", n))
                n += len(simplex.boundary_keys())
            output.write(struct.pack("q", n))  # Write the number of all boundary elements

        def write_boundary_map():
            for simplex in self.simplices:
                for key in simplex.boundary_keys():
                    output.write(struct.pack("q", self.dict_simplices[key].index))

        write_dipha_header(len(self.simplices))
        write_dimensions()
        write_birth_radii()
        write_boundary_map_sizes()
        write_boundary_map()
