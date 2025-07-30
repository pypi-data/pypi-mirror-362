# pylint: disable=C0103,C0111,W0201,R0201
import numpy as np

import homcloud.utils as utils


def test_deep_tolist():
    lst = np.array([[0.0, 1.0], [2.0, 3.0]])
    assert utils.deep_tolist(lst) == [[0.0, 1.0], [2.0, 3.0]]
    lst = [np.array([0.0, 1.0]), np.array([2.0, 3.0])]
    assert utils.deep_tolist(lst) == [[0.0, 1.0], [2.0, 3.0]]
    assert utils.deep_tolist([[0.0, 1.0], [2.0, 3.0]]) == [[0.0, 1.0], [2.0, 3.0]]
