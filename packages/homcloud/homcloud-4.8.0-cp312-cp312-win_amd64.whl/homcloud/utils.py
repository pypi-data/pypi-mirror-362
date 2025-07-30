# pylint: disable=R0204
import os
import subprocess
import sys
import threading

import numpy as np


def paraview_programname():
    return os.environ.get("HOMCLOUD_PARAVIEW_PROGRAMNAME", "paraview")


def invoke_paraview(*args, wait=False, finalize=lambda: None):
    devnull = subprocess.DEVNULL
    redirect = {"stdin": devnull, "stdout": devnull, "stderr": devnull}
    program_name = paraview_programname()

    def invoke():
        if sys.platform.startswith("darwin"):
            subprocess.check_call(["open", "-a", program_name, "-W", "--args"] + list(args), **redirect)
        elif sys.platform.startswith("win"):
            subprocess.check_call([program_name] + list(args), **redirect)
        else:
            subprocess.check_call(["nohup", program_name] + list(args), **redirect)

        finalize()

    if wait:
        invoke()
    else:
        threading.Thread(target=invoke).start()


def deep_tolist(lst):
    """Convert ndarray to python's list recursively.

    This function is useful to convert data into json/msgpack format.

    TODO: support dict.
    """
    if isinstance(lst, np.ndarray):
        return lst.tolist()
    if isinstance(lst, list):
        return [deep_tolist(sublist) for sublist in lst]
    return lst


def load_symbols(path):
    if path is None:
        return None

    symbols = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            symbols.append(line)
    return symbols
