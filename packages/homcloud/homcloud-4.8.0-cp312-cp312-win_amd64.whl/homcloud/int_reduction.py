import argparse
import sys

from homcloud.version import __version__

from homcloud.optvol import sign_function
from homcloud.license import add_argument_for_license
import homcloud.int_reduction_ext as int_reduction_ext
from homcloud.pdgm import PDGM


def build_checker(dim, boundary_map):
    checker = int_reduction_ext.Checker(count_num_cells(dim, boundary_map))
    setup_matrix(checker, boundary_map)
    return checker


def setup_matrix(matrix, boundary_map):
    sign = sign_function(boundary_map)
    map = boundary_map["map"]

    def dim(i):
        return map[i][0]

    def column(i):
        return map[i][1]

    for i in range(len(map)):
        matrix.add_cell(dim(i))
        signed_column = [(j, sign(i, kth)) for kth, j in enumerate(column(i))]
        for j, s in sorted(signed_column):
            matrix.add_boundary_coef(i, j, s)


def count_num_cells(dim, boundary_map):
    num_cells = [0] * (dim + 1)
    for d, *_ in boundary_map["map"]:
        num_cells[d] += 1
    return num_cells


def main(args=None):
    args = args or argument_parser().parse_args()
    diagram = PDGM.open(args.input, 0, False)
    checker = build_checker(diagram.input_dim, diagram.boundary_map_chunk)

    stop_coef, stop_index = checker.check()
    if stop_coef == 0:
        print("No Problem")
        return 0
    else:
        stop_time = diagram.index_to_level[stop_index]
        print("Problematic coef: {}, Problematic time: {}".format(stop_coef, stop_time))
        return 1


def argument_parser():
    p = argparse.ArgumentParser(description="Examine field problem")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    p.add_argument("input", help="input file")
    return p


if __name__ == "__main__":
    sys.exit(main())
