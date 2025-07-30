import argparse
import struct
import numpy as np
import ripser

from homcloud.pdgm_format import (
    PDGMWriter,
    PDChunk,
    BoundaryMapChunk,
    RipsInformationChunk,
    GraphWeightsChunk,
)
from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.utils import load_symbols
from homcloud.argparse_common import parse_bool
import homcloud.dipha as dipha
import homcloud.phat_ext as phat


class DistanceMatrix(object):
    def __init__(self, matrix, upper_dim, upper_value=np.inf, vertex_symbols=None):
        assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
        self.matrix = matrix
        self.upper_dim = upper_dim
        self.upper_value = upper_value
        self.vertex_symbols = vertex_symbols

    def build_rips_filtration(self, save_graph=False, save_cocycle=False):
        return RipsFiltration(
            self.matrix.astype(np.float32), self.upper_dim, self.upper_value, save_graph, save_cocycle
        )

    def build_simplicial_filtration(self, save_boundary_map=False):
        simplices = sorted(self.all_simplices(), key=lambda x: (x[0], len(x[1])))
        index_to_level = [level for (level, simplex) in simplices]
        index_to_simplex = [simplex for (level, simplex) in simplices]
        simplex_to_index = {simplex: index for (index, (value, simplex)) in enumerate(simplices)}
        if self.vertex_symbols is None:
            vertex_symbols = [str(k) for k in range(self.matrix.shape[0])]
        else:
            vertex_symbols = self.vertex_symbols

        return SimplicialFiltration(
            self, index_to_level, index_to_simplex, simplex_to_index, vertex_symbols, save_boundary_map
        )

    def all_simplices(self):
        npoints = self.matrix.shape[0]

        def value_of_simplex(simplex, i, value):
            return max(np.max(self.matrix[i, simplex]), value)

        def iter(simplex, value):
            if len(simplex) > self.upper_dim + 1:
                return

            for i in range(simplex[-1] + 1, npoints):
                newvalue = value_of_simplex(simplex, i, value)
                if newvalue >= self.upper_value:
                    continue
                simplex.append(i)
                yield newvalue, tuple(simplex)
                yield from iter(simplex, newvalue)
                simplex.pop()

        for i in range(npoints):
            yield (0.0, (i,))
            yield from iter([i], -np.inf)


class RipsFiltration(object):
    def __init__(self, matrix, upper_dim, upper_value, save_graph, save_cocycle):
        self.matrix = matrix
        self.upper_dim = upper_dim
        self.upper_value = upper_value
        self.save_graph = save_graph
        self.save_cocycle = save_cocycle

    def compute_pdgm(self, f, algorithm=None, save_suppl_info=True):
        algorithm = algorithm or self.favorite_algorithm()

        if algorithm == "ripser":
            self.compute_pdgm_by_ripser(f)
        elif algorithm == "dipha":
            self.compute_pdgm_by_dipha(f)
        else:
            raise (ValueError(f"Unknown algorithm: {algorithm}"))

    def compute_pdgm_by_ripser(self, f):
        def build_pdchunk(d, pairs):
            births = []
            deaths = []
            ess_births = []
            for k in range(pairs.shape[0]):
                birth = pairs[k, 0]
                death = pairs[k, 1]
                if death == np.inf:
                    ess_births.append(birth)
                else:
                    births.append(birth)
                    deaths.append(death)
            return PDChunk("pd", d, births, deaths, ess_births)

        diagrams = ripser.ripser(
            self.matrix,
            self.upper_dim,
            self.upper_value,
            2,  # Z/2Z
            True,  # The first argument is a distane matrix, not a pointcloud
            do_cocycles=self.save_cocycle,
        )

        writer = PDGMWriter(f, "rips", self.upper_dim + 1)

        for d, pairs in enumerate(diagrams["dgms"]):
            writer.append_chunk(build_pdchunk(d, pairs))

        self.append_rips_information_chunk(writer)
        self.append_graph_weights_chunk(writer)

        if self.save_cocycle:
            self.append_cocycle_chunk(writer, diagrams["dgms"], diagrams["cocycles"])

        writer.write()

    def append_graph_weights_chunk(self, writer):
        if not self.save_graph:
            return
        writer.append_chunk(GraphWeightsChunk(self.matrix))

    def append_rips_information_chunk(self, writer):
        writer.append_chunk(RipsInformationChunk(self.num_vertices))

    def append_cocycle_chunk(self, writer, dgms, cocycles):
        for d in range(len(dgms)):
            writer.append_simple_chunk(
                "cocycles", [cocycle.tolist() for (cocycle, pair) in zip(cocycles[d], dgms[d]) if pair[1] != np.inf], d
            )

    @property
    def num_vertices(self):
        return self.matrix.shape[0]

    def compute_pdgm_by_dipha(self, f):
        pd_chunks = [PDChunk("pd", d, [], [], []) for d in range(self.upper_dim + 1)]
        pairs = dipha.pairs_from_filtration(self, 1, False, self.upper_dim, self.upper_value)
        for d, birth, death in pairs:
            if death == np.inf:
                pd_chunks[d].ess_births.append(birth)
            else:
                pd_chunks[d].births.append(birth)
                pd_chunks[d].deaths.append(death)

        writer = PDGMWriter(f, "rips", self.upper_dim + 1)
        writer.extend_chunks(pd_chunks)
        self.append_rips_information_chunk(writer)
        self.append_graph_weights_chunk(writer)
        writer.write()

    def write_dipha_complex(self, output):
        num_vertices = self.matrix.shape[0]

        def write_dipha_header():
            output.write(struct.pack("qqq", 8067171840, 7, num_vertices))

        def write_matrix():
            for i in range(num_vertices):
                for j in range(num_vertices):
                    output.write(struct.pack("d", self.matrix[i, j] * 2))

        write_dipha_header()
        write_matrix()

    def favorite_algorithm(self):
        return "ripser"


class SimplicialFiltration(object):
    def __init__(
        self, dmatrix, index_to_level, index_to_simplex, simplex_to_index, vertex_symbols, save_boundary_map=False
    ):
        self.distance_matrix = dmatrix
        self.index_to_level = index_to_level
        self.index_to_simplex = index_to_simplex
        self.simplex_to_index = simplex_to_index
        self.vertex_symbols = vertex_symbols
        self.boundary_map = self.build_boundary_map()
        self.save_boundary_map = save_boundary_map

    def build_boundary_map(self):
        def boundary(simplex):
            if len(simplex) == 1:
                return

            for k in range(len(simplex)):
                key = simplex[:k] + simplex[k + 1 :]
                yield self.simplex_to_index[key]

        return [[len(simplex) - 1, list(boundary(simplex))] for simplex in self.index_to_simplex]

    @property
    def upper_dim(self):
        return self.distance_matrix.upper_dim

    def build_phat_matrix(self):
        phat_matrix = phat.Matrix(len(self.index_to_simplex), "none")
        for index, (dim, col) in enumerate(self.boundary_map):
            phat_matrix.set_dim_col(index, dim, col)

        return phat_matrix

    def compute_pdgm(self, f, algorithm=None, save_suppl_info=True):
        assert save_suppl_info

        phat_matrix = self.build_phat_matrix()
        phat_matrix.reduce(algorithm)
        writer = PDGMWriter(f, "simplicial", self.upper_dim + 1)
        writer.save_pairs(phat_matrix.birth_death_pairs(), self.index_to_level)
        writer.append_simple_chunk("index_to_level", self.index_to_level)
        writer.append_simple_chunk("index_to_simplex", self.index_to_simplex)
        writer.append_simple_chunk("vertex_symbols", self.vertex_symbols)
        if self.save_boundary_map:
            writer.append_chunk(BoundaryMapChunk("simplicial", self.boundary_map))

        writer.write()


def main(args=None):
    args = args or argument_parser().parse_args()
    matrix = DistanceMatrix(
        np.loadtxt(args.input), args.upper_degree, args.upper_value, load_symbols(args.vertex_symbols)
    )
    if args.save_boundary_map:
        filt = matrix.build_simplicial_filtration(True)
    else:
        filt = matrix.build_rips_filtration()

    with open(args.output, "wb") as f:
        filt.compute_pdgm(f, args.algorithm)


def argument_parser():
    p = argparse.ArgumentParser(description="Compute a PD from Vietris-Rips filtration")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument("-d", "--upper-degree", type=int, required=True, help="Maximum computed degree")
    p.add_argument("-u", "--upper-value", type=float, default=np.inf, help="Maximum distance (default: +inf)")
    p.add_argument("--vertex-symbols", help="vertex symbols file")
    p.add_argument(
        "-M",
        "--save-boundary-map",
        default=False,
        type=parse_bool,
        help="save boundary map into output file" "(only available with phat-* algorithms, on/*off*)",
    )
    p.add_argument("--algorithm", default=None, help="algorithm (dipha, ripser)")
    p.add_argument("--parallels", default=1, type=int, help="number of threads (default: 1)")
    add_argument_for_license(p)
    p.add_argument("input", help="input file")
    p.add_argument("output", help="output file")
    return p


if __name__ == "__main__":
    main()
