# You should run this script in the same directory of this file.

import os
import platform
import re
from setuptools import setup, Extension
import numpy as np
import glob


if os.environ.get("HOMCLOUD_USE_BUILTIN_BOOST_CGAL", "0") == "1":
    BASE_INCLUDE_DIRS = glob.glob("ext/external/CGAL-*/include") + glob.glob("ext/external/boost_*")
else:
    BASE_INCLUDE_DIRS = []

BASE_INCLUDE_DIRS.append(np.get_include())

if re.match(r'^MSC', platform.python_compiler()):
    CPPLANGOPTS = []
else:
    CPPLANGOPTS = ["-std=c++17", "-Wno-unknown-pragmas"]

LIBS = ["mpfr", "gmp"]

if os.environ.get("HOMCLOUD_BUILD_WITH_OPENMP", "0") == "1":
    openmp_compile_args = ["-fopenmp", "-DHOMCLOUD_OPENMP"]
    openmp_link_args = ["-fopenmp"]
else:
    openmp_compile_args = []
    openmp_link_args = []

PHAT_INCLUDE_DIR = "ext/external/phat/include"
MSGPACK_INCLUDE_DIR = "ext/external/msgpack-c/include"
HERA_INCLUDE_DIR = "ext/external/hera/include"


EXT_MODULES = [
    Extension("homcloud.periodic_alpha_shape2",
              include_dirs=BASE_INCLUDE_DIRS,
              libraries=LIBS,
              extra_compile_args=CPPLANGOPTS,
              define_macros=[("CGAL_HEADER_ONLY", None)],
              sources=["ext/periodic_alpha_shape2.cc"],
              depends=["ext/alpha_shape_common.h",
                       "ext/homcloud_common.h"]),

    Extension("homcloud.modp_reduction_ext",
              include_dirs=BASE_INCLUDE_DIRS,
              sources=["ext/modp_reduction_ext.cc"],
              extra_compile_args=(CPPLANGOPTS + ["-DPYTHON"]),
              depends=[]),
    Extension("homcloud.cgal_info",
              include_dirs=BASE_INCLUDE_DIRS,
              libraries=LIBS,
              extra_compile_args=CPPLANGOPTS,
              define_macros=[("CGAL_HEADER_ONLY", None)],
              sources=["ext/cgal_info.cc"],
              depends=["ext/homcloud_common.h"]),
    Extension("homcloud.alpha_shape3",
              include_dirs=BASE_INCLUDE_DIRS,
              libraries=LIBS,
              extra_compile_args=CPPLANGOPTS,
              define_macros=[("CGAL_HEADER_ONLY", None)],
              sources=["ext/alpha_shape3.cc"],
              depends=["ext/alpha_shape_common.h",
                       "ext/homcloud_common.h"]),
    Extension("homcloud.alpha_shape2",
              include_dirs=BASE_INCLUDE_DIRS,
              libraries=LIBS,
              extra_compile_args=CPPLANGOPTS,
              define_macros=[("CGAL_HEADER_ONLY", None)],
              sources=["ext/alpha_shape2.cc"],
              depends=["ext/alpha_shape_common.h",
                       "ext/homcloud_common.h"]),
    Extension("homcloud.periodic_alpha_shape3",
              libraries=LIBS,
              include_dirs=BASE_INCLUDE_DIRS,
              extra_compile_args=CPPLANGOPTS,
              define_macros=[("CGAL_HEADER_ONLY", None)],
              sources=["ext/periodic_alpha_shape3.cc"],
              depends=["ext/alpha_shape_common.h",
                       "ext/homcloud_common.h"]),
    Extension("homcloud.pict_tree",
              include_dirs=BASE_INCLUDE_DIRS,
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/pict_tree.cc"],
              depends=["ext/homcloud_common.h"]),
    Extension("homcloud.cubical_ext",
              include_dirs=(BASE_INCLUDE_DIRS + [PHAT_INCLUDE_DIR, MSGPACK_INCLUDE_DIR]),
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/cubical_ext.cc"],
              depends=["ext/phat_ext.h"]),
    Extension("homcloud.phat_ext",
              include_dirs=(BASE_INCLUDE_DIRS + [PHAT_INCLUDE_DIR, MSGPACK_INCLUDE_DIR]),
              extra_compile_args=(CPPLANGOPTS + openmp_compile_args),
              extra_link_args=openmp_link_args,
              sources=["ext/phat.cc"],
              depends=["ext/phat_ext.h"]),
    Extension("homcloud.distance_transform_ext",
              include_dirs=BASE_INCLUDE_DIRS,
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/distance_transform_ext.cc"],
              depends=["ext/homcloud_common.h"]),
    Extension("homcloud.int_reduction_ext",
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/int_reduction_ext.cc"],
              depends=[]),
    Extension("homcloud.homccube",
              include_dirs=BASE_INCLUDE_DIRS,
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/homccube.cc"],
              depends=["ext/homcloud_common.h"]),
    Extension("homcloud.optimal_one_cycle_ext",
              include_dirs=(BASE_INCLUDE_DIRS + [MSGPACK_INCLUDE_DIR]),
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/optimal_one_cycle_ext.cc"],
              depends=["ext/homcloud_common.h"]),
    Extension("homcloud.hera_bottleneck",
              include_dirs=(BASE_INCLUDE_DIRS + [HERA_INCLUDE_DIR]),
              extra_compile_args=CPPLANGOPTS,
              sources=["ext/hera_bottleneck.cc"],
              depends=["ext/homcloud_common.h", "ext/homcloud_numpy.h", "ext/hera_common.h"]),
    Extension("homcloud.hera_wasserstein",
              extra_compile_args=CPPLANGOPTS,
              include_dirs=(BASE_INCLUDE_DIRS + [HERA_INCLUDE_DIR]),
              sources=["ext/hera_wasserstein.cc"],
              depends=["ext/homcloud_common.h", "ext/homcloud_numpy.h", "ext/hera_common.h"]),
]


setup(
    ext_modules=EXT_MODULES,
    packages=[
        "homcloud",
        "homcloud.histopixels",
        "homcloud.pict",
        "homcloud.geometry",
        "homcloud.interface",
    ],
)
