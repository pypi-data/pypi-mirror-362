from cached_property import cached_property

from homcloud.base_filtration import Filtration
from homcloud.pdgm_format import PDGMWriter, BinaryChunk

import homcloud.phat_ext as phat


class SimplicialFiltration(Filtration):
    def __init__(self, simplicial_function, vertex_symbols, save_boundary_map):
        self.simplicial_function = self.normalize_simplicial_function(simplicial_function)
        s = sorted((level, len(simplex), simplex) for (simplex, level) in self.simplicial_function.items())
        self.index_to_simplex = [simplex for (_, _, simplex) in s]
        self.index_to_level = [level for (level, _, _) in s]
        self.simplex_to_index = {simplex: index for (index, (_, _, simplex)) in enumerate(s)}
        self.vertex_symbols = vertex_symbols or self.default_vertex_symbols()
        self.save_boundary_map = save_boundary_map

    @staticmethod
    def normalize_simplicial_function(fun):
        retval = dict()
        for simplex, level in fun.items():
            simplex = tuple(sorted(simplex))
            if simplex in retval:
                raise (ValueError("duplicated simplex"))

            retval[simplex] = level

        return retval

    def default_vertex_symbols(self):
        return [str(i) for i in range(self.num_vertices)]

    @cached_property
    def num_vertices(self):
        return max(k[0] for k in self.index_to_simplex if len(k) == 1) + 1

    def build_phat_matrix(self):
        matrix = phat.Matrix(len(self.index_to_simplex), self.boundary_map_style())
        for index, simplex in enumerate(self.index_to_simplex):
            boundary = self.boundary(simplex)
            self.check_boundary(boundary, index)
            matrix.set_dim_col(index, self.simplex_dim(simplex), boundary)
        return matrix

    def boundary_map_style(self):
        return "simplicial" if self.save_boundary_map else "none"

    @staticmethod
    def simplex_dim(simplex):
        return len(simplex) - 1

    def boundary(self, simplex):
        def kth(k):
            return self.simplex_to_index[tuple(simplex[:k] + simplex[k + 1 :])]

        if len(simplex) == 1:
            return []
        else:
            return [kth(k) for k in range(len(simplex))]

    @staticmethod
    def check_boundary(boundary, index):
        for i in boundary:
            assert i < index

    def compute_pdgm(self, f, algorithm=None, output_suppl_info=True):
        writer = PDGMWriter(f, "simplicial", self.dim)
        pairs, boundary_map_byte_sequence = self.compute_pairs(algorithm)
        writer.save_pairs(pairs, self.index_to_level, output_suppl_info)

        if output_suppl_info:
            writer.append_simple_chunk("index_to_level", self.index_to_level)
            writer.append_simple_chunk("index_to_simplex", self.index_to_simplex)
            writer.append_simple_chunk("vertex_symbols", self.vertex_symbols)

        if self.save_boundary_map:
            writer.append_chunk(BinaryChunk("boundary_map", boundary_map_byte_sequence))

        writer.write()

    @property
    def dim(self):
        return max(len(simplex) for simplex in self.index_to_simplex) - 1

    @staticmethod
    def favorite_algorithm():
        return "phat-twist"
