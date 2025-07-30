import argparse
import sys

from homcloud.version import __version__
from homcloud.argparse_common import add_arguments_for_load_diagrams, parse_bool
from homcloud.pdgm import PDGM


def main(args=None):
    args = args or argument_parser().parse_args()
    output_text(args, get_output_io(args))


def argument_parser():
    """Returns the parser of args"""
    p = argparse.ArgumentParser(description="Dump pairs in dipha's diagram")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    p.add_argument("-o", "--output", help="output text file")
    p.add_argument(
        "-S",
        "--show-simplices",
        type=parse_bool,
        default=False,
        help="show birth/death simplices (yes/no, default:no)",
    )
    p.add_argument(
        "-E",
        "--show-essential-pairs",
        type=parse_bool,
        default=False,
        help="show essential pairs (yes/no, default:no)",
    )
    p.add_argument(
        "-s",
        "--symbols",
        type=parse_bool,
        default=False,
        help="show birth/death simplices by symbols" "(yes/no default:no)",
    )
    p.add_argument("input", help="input pdgm file")
    return p


def get_output_io(args):
    if args.output:
        return open(args.output, "w")
    else:
        return sys.stdout


def output_text(args, output):
    if args.show_simplices:
        pdgm = PDGM.open(args.input, args.degree)
        resolve_index = pdgm.get_geometry_resolver("symbols" if args.symbols else "default").resolve_cell
        write_pairs_with_geometry(pdgm, output, args.show_essential_pairs, resolve_index)
    else:
        write_pairs(PDGM.open(args.input, args.degree, False), output, args.show_essential_pairs)


def write_pairs(diagram, io, show_essential_pairs):
    for birth, death in zip(diagram.births, diagram.deaths):
        io.write("{} {}\n".format(birth, death))

    if show_essential_pairs:
        inf = inf_string(diagram)
        for birth in diagram.essential_births:
            io.write("{} {}\n".format(birth, inf))


def write_pairs_with_geometry(pdgm, io, show_essential_pairs, resolve_index):
    def format_geometry(index):
        def format(obj):
            if isinstance(obj, list):
                return "(" + ",".join(format(item) for item in obj) + ")"
            else:
                return str(obj)

        return format(resolve_index(index))

    pairs = zip(pdgm.births, pdgm.deaths, pdgm.birth_indices, pdgm.death_indices)
    for birth, death, birth_index, death_index in pairs:
        io.write("{} {} {} {}\n".format(birth, death, format_geometry(birth_index), format_geometry(death_index)))

    if show_essential_pairs:
        inf = inf_string(pdgm)
        for birth, birth_index in zip(pdgm.essential_births, pdgm.essential_birth_indices):
            io.write("{} {} {}\n".format(birth, inf, format_geometry(birth_index)))


def inf_string(diagram):
    return "-inf" if diagram.sign_flipped else "inf"


if __name__ == "__main__":
    main()
