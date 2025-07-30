import subprocess
import os
import math
import struct
from tempfile import TemporaryDirectory


def pairs_from_filtration(filtration, parallels=1, dual=False, upper_dim=None, upper_value=None):
    with TemporaryDirectory() as tmpdir:
        complex_path = os.path.join(tmpdir, "tmp.complex")
        diagram_path = os.path.join(tmpdir, "tmp.diagram")
        with open(complex_path, "wb") as f:
            filtration.write_dipha_complex(f)
        run(complex_path, diagram_path, parallels, dual, upper_dim, upper_value)

        with open(diagram_path, "rb") as f:
            yield from read_pairs(f)


def read_pairs(f):
    f.read(16)  # skip header
    (num_pairs,) = struct.unpack("q", f.read(8))

    for _ in range(num_pairs):
        d, birth, death = struct.unpack("qdd", f.read(24))
        if d < 0:
            yield (-d - 1, birth, math.inf)
        else:
            yield (d, birth, death)


def run(inpath, outpath, parallels=1, dual=False, upper_dim=None, upper_value=None):
    options = []

    if os.environ.get("HOMCLOUD_SUPPRESS_MPI") == "1":
        mpi = []
    else:
        mpi = ["mpiexec", "-n", str(parallels)]
    if dual:
        options.append("--dual")
    if upper_dim is not None:
        options.extend(["--upper_dim", str(upper_dim + 1)])
    if upper_value is not None and upper_value != math.inf:
        options.extend(["--upper_value", str(upper_value)])

    subprocess.check_call(mpi + ["dipha"] + options + [inpath, outpath])
