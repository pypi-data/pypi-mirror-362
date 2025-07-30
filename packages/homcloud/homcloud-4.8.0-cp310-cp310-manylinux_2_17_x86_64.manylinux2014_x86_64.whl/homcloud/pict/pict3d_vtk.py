import sys
from argparse import ArgumentParser

import numpy as np

from homcloud.version import __version__
import homcloud.pict.utils as utils
from homcloud.license import add_argument_for_license


def main(args=None):
    args = args or argument_parser().parse_args()
    pict = utils.load_nd_picture(args.input, args.type)
    if pict.ndim != 3:
        raise RuntimeError("Input picture should be 3d")

    with open(args.output, "w") as f:
        write_vtk_file(f, args.input[0], pict)


def write_vtk_file(f, path, pict):
    zw, yw, xw = pict.shape

    def at(x, y, z):
        return x * (zw + 1) * (yw + 1) + y * (zw + 1) + z

    f.write("# vtk DataFile Version 3.0\n")
    f.write("%s\n" % path)
    f.write("ASCII\n")
    f.write("DATASET UNSTRUCTURED_GRID\n")
    f.write("\n")

    f.write("POINTS %d float\n" % ((zw + 1) * (yw + 1) * (xw + 1)))
    for x in range(xw + 1):
        for y in range(yw + 1):
            for z in range(zw + 1):
                f.write("%f %f %f\n" % (x - 0.5, y - 0.5, z - 0.5))
    f.write("\n")
    f.write("CELLS %d %d\n" % (xw * yw * zw, xw * yw * zw * 9))
    for x in range(xw):
        for y in range(yw):
            for z in range(zw):
                f.write(
                    "8 %d %d %d %d %d %d %d %d\n"
                    % (
                        at(x, y, z),
                        at(x + 1, y, z),
                        at(x, y + 1, z),
                        at(x + 1, y + 1, z),
                        at(x, y, z + 1),
                        at(x + 1, y, z + 1),
                        at(x, y + 1, z + 1),
                        at(x + 1, y + 1, z + 1),
                    )
                )
    f.write("\n")
    f.write("CELL_TYPES %d\n" % (xw * yw * zw))
    for _ in range(xw * yw * zw):
        f.write("11\n")
    f.write("\n")
    f.write("CELL_DATA %d" % (xw * yw * zw))
    f.write("SCALARS value float 1\n")
    f.write("LOOKUP_TABLE default\n")
    for value in pict.ravel():
        f.write("%f\n" % value)


def extend_2d_3d(array, default_value):
    if len(array) == 2:
        return default_value, array[0], array[1]
    else:
        return array


def write_vti_xmlfile(f, pict, offsets=[0.0, 0.0, 0.0]):
    zw, yw, xw = extend_2d_3d(pict.shape, 1)
    offsets = extend_2d_3d(offsets, 0.0)

    header = """<?xml version="1.0"?>
    <VTKFile type="ImageData" byte_order="LittleEndian" header_type="UInt64">
      <ImageData WholeExtent="0 {0} 0 {1} 0 {2}"
                 Origin="{3} {4} {5}"
                 Spacing="1.0 1.0 1.0">
        <Piece Extent="0 {0} 0 {1} 0 {2}">
          <CellData Scalars="value">
            <DataArray Name="value" type="Float64" format="ascii">
    """.format(
        xw, yw, zw, offsets[2] - 0.5, offsets[1] - 0.5, offsets[0] - 0.5
    )

    footer = """
            </DataArray>
          </CellData>
        </Piece>
      </ImageData>
    </VTKFile>
    """
    f.write(header)
    np.savetxt(f, pict.astype(np.float64).ravel())
    f.write(footer)


def argument_parser():
    p = ArgumentParser(description="Convert 3d picture to a vtk file")
    p.add_argument("-V", "--version", action="version", version=__version__)
    p.add_argument(
        "-T",
        "--type",
        default="text_nd",
        help="input data format " "(text2d,text_nd(default),picture2d,pictures3d,npy)",
    )
    p.add_argument("-o", "--output", required=True, help="output file name")
    add_argument_for_license(p)
    p.add_argument("input", nargs="*", help="input files")
    return p


if __name__ == "__main__":
    sys.exit(main())
