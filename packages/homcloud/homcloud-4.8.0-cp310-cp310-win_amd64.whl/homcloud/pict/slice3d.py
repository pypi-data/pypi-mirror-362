import argparse
from tempfile import TemporaryDirectory
import os
import subprocess
import re

from PIL import Image
import numpy as np


def main(args=None):
    args = args or argument_parser().parse_args()
    volumes = [np.load(path) for path in args.input]

    assert [volume.shape == volumes[0].shape for volume in volumes]

    if args.slice is not None:
        with TemporaryDirectory() as tmpdir:
            write_volume_slices(volumes, args.slice, args.spacer, args.range, tmpdir)
            subprocess.call("{} {}".format(args.image_viewer, tmpdir), shell=True)


def write_volume_slices(volumes, direction, spacer, slice_range, dirname):
    uppers = list(map(np.max, volumes))
    lowers = list(map(np.min, volumes))
    shape = volumes[0].shape[0:direction] + volumes[0].shape[direction + 1 :]
    width = shape[1] * len(volumes) + spacer * (len(volumes) - 1)
    height = shape[0]
    d = shape[1] + spacer
    if not slice_range:
        slice_range = (0, volumes[0].shape[direction])
    for n in range(*slice_range):
        array = np.zeros((height, width), dtype=np.uint8)
        for i, (volume, u, l) in enumerate(zip(volumes, uppers, lowers)):
            u_f = float(u)
            l_f = float(l)
            slice = slice_volume(volume, n, direction)
            array[:, d * i : d * i + shape[1]] = (slice - l_f) * 254 / (u_f - l_f)
        path = os.path.join(dirname, "{:04d}.png".format(n))
        Image.fromarray(array).save(path)


def slice_volume(volume, n, direction):
    if direction == 0:
        return volume[n, :, :]
    if direction == 1:
        return volume[:, n, :]
    if direction == 2:
        return volume[:, :, n]
    raise ValueError("{} is not valid for direction".format(n))


def argument_parser():
    p = argparse.ArgumentParser(description="3d npy data viewer")
    p.add_argument("-s", "--slice", default=0, type=int, help="slicing direction (0, 1, or 2)")
    p.add_argument("-S", "--spacer", default=10, type=int, help="spacer pixels")
    p.add_argument("-r", "--range", default=None, type=parse_range, help="range of slices")
    p.add_argument("--image-viewer", default="eog -n", help="image viewer program name")
    p.add_argument("input", nargs="+", help="input files")
    return p


def parse_range(string):
    l, r = re.split(r":", string)
    return int(l), int(r)


if __name__ == "__main__":
    main()
