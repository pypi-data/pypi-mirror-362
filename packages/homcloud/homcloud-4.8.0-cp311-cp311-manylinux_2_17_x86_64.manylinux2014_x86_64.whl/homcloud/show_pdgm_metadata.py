import argparse
from homcloud.pdgm_format import PDGMReader
from pprint import pprint


def main(args=None):
    if not args:
        args = argument_parser().parse_args()

    with PDGMReader.open(args.input) as reader:
        pprint(reader.metadata)


def argument_parser():
    p = argparse.ArgumentParser(description="show pdgm metadata for debug")
    p.add_argument("input", help="input file path")
    return p


if __name__ == "__main__":
    main()
