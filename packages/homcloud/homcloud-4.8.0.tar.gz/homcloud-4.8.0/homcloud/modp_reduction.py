import argparse
import sys

from homcloud.version import __version__

from homcloud.license import add_argument_for_license
from homcloud.modp_reduction_ext import ModpMatrix
from homcloud.pdgm import PDGM
from homcloud.pdgm_format import PDGMWriter
from homcloud.int_reduction import setup_matrix, count_num_cells


def main(args=None):
    args = args or argument_parser().parse_args()
    pdgm = PDGM.open(args.input, 0, False)
    matrix = build_matrix(args.p, pdgm.input_dim, pdgm.boundary_map_chunk)

    matrix.reduce()
    pairs = matrix.birth_death_pairs()
    with open(args.output, "wb") as f:
        write_modp_pdgm(f, pdgm, pairs)


def argument_parser():
    p = argparse.ArgumentParser(description="Examine field problem")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("-p", type=int, required=True, help="prime number")
    p.add_argument("input", help="input file")
    p.add_argument("output", help="output file")
    return p


def build_matrix(p, dim, boundary_map):
    matrix = ModpMatrix(p, count_num_cells(dim, boundary_map))
    setup_matrix(matrix, boundary_map)
    return matrix


def write_modp_pdgm(f, orig_pdgm, pairs):
    writer = PDGMWriter(f, orig_pdgm.filtration_type, orig_pdgm.input_dim)
    index_to_level = orig_pdgm.index_to_level
    writer.save_pairs(pairs, index_to_level)
    writer.append_simple_chunk("index_to_level", index_to_level)
    writer.write()


if __name__ == "__main__":
    sys.exit(main())
