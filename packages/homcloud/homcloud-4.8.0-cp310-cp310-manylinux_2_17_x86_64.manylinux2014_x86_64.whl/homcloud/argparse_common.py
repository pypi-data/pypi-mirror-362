import re
import os


def add_arguments_for_load_diagrams(parser):
    parser.add_argument("-d", "--degree", type=int, required=True, help="degree of PH")
    parser.add_argument("-T", "--type", help="input file format (dipha, idipha, text) (default: autodetect)")
    parser.add_argument(
        "-N",
        "--negate",
        default=False,
        action="store_true",
        help="flip the sign of birth/death times for superlevel persistence (default: False)",
    )


def add_arguments_for_histogram_rulers(parser):
    parser.add_argument("-x", "--x-range", type=parse_range, help="birth range")
    parser.add_argument("-X", "--xbins", type=int, default=128, help="number of bins in birth-axis")
    parser.add_argument("-y", "--y-range", type=parse_range, default=None, help="death range")
    parser.add_argument("-Y", "--ybins", type=int, default=None, help="number of bins in death-axis")


def add_arguments_for_gaussian_diffusion(parser):
    parser.add_argument(
        "-D", "--gaussian-sd", type=float, required=True, help="standard deviation of gaussian diffusion"
    )


def add_arguments_for_kernel_weight(parser):
    parser.add_argument("-C", type=float, help="weight constant C")
    parser.add_argument("-p", type=float, default=1.0, help="weight constant p")


FLOAT_REGEXP = r"[+-]?\d+(\.\d+)?"
RANGE_REGEXPS = [
    re.compile(r"\A(?P<begin>{0}):(?P<end>{0})\Z".format(FLOAT_REGEXP)),
    re.compile(r"\A\[(?P<begin>{0}):(?P<end>{0})\]\Z".format(FLOAT_REGEXP)),
]


def parse_range(string):
    for regexp in RANGE_REGEXPS:
        m = regexp.match(string)
        if m:
            return (float(m.group("begin")), float(m.group("end")))
    raise ValueError("{} cannot be parsed as range".format(string))


def parse_bool(string):
    s = string.lower()
    if s == "true" or s == "yes" or s == "1" or s == "on":
        return True
    if s == "false" or s == "no" or s == "0" or s == "off":
        return False
    raise ValueError("{} cannot be parsed as boolean".format(string))


def parse_color(string):
    if re.match(r"#[0-9a-fA-F]{6}\Z", string):
        return tuple(int(string[i : i + 2], 16) for i in [1, 3, 5])
    raise ValueError("{} cannot be parsed as color".format(string))


def parse_cubical_periodic_flags(arg):
    return [bool(int(el)) for el in re.split(",", arg)]


def check_abolished_output(args):
    if os.path.splitext(args.output)[1] in [".complex", ".icomplex", ".diagram", ".idiagram"]:
        raise RuntimeError(
            "Now this program does not support outputting " ".diagram, .complex, .icomplex, and .idiagram files"
        )


def check_cubical_option(args):
    if args.save_boundary_map and not args.cubical:
        raise RuntimeError("-M (--save-boundary-map) option must be with" " -C (--cubical) option")
