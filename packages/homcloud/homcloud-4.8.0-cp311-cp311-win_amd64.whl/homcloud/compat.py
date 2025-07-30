try:
    from tempfile import TemporaryDirectory as TD
except ImportError:
    from backports.tempfile import TemporaryDirectory as TD

try:
    from unittest.mock import Mock as Mk
except ImportError:
    from mock import Mock as Mk

try:
    import imageio.v2 as imageio
except ImportError:
    import imageio


try:
    from sklearn.metrics import DistanceMetric
except ImportError:
    from sklearn.neighbors import DistanceMetric


TemporaryDirectory = TD
Mock = Mk

INFINITY = float("inf")
