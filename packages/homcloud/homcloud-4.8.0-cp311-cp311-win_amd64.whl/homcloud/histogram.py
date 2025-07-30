import numpy as np
from scipy.ndimage import gaussian_filter

from homcloud.delegate import forwardable


@forwardable
class Histogram(object):
    """A histogram, normally used for representing persistence diagrams.
    The PDHistogram subclass is used for this purpose.

    This class is also used for representing vectorized histogram.
    """

    def __init__(self, values, histospec, ess_values=None):
        self.values = values
        self.histospec = histospec
        self.values_as_float = values.astype(float)
        self.ess_values = ess_values

    __delegator_definitions__ = {
        "histospec": ["xedges", "yedges", "sign_flipped", "xy_extent", "x_range", "y_range", "x_bins", "y_bins"]
    }

    def has_ess_values(self):
        return self.ess_values is not None

    def maxvalue(self):
        return max([np.max(self.values), -np.inf if self.ess_values is None else np.max(self.ess_values)])

    def vectorize(self):
        """Return vectorized histogram as a 1D ndarray of floats."""
        return self.values[self.histospec.vectorize_mask()]

    def value_at(self, birth, death):
        """Internally used by vectorize()."""
        y_index = np.searchsorted(self.yedges, death)
        x_index = np.searchsorted(self.xedges, birth)
        if not ((0 < y_index < self.yedges.size) and (0 < x_index < self.xedges.size)):
            return None
        return self.values[y_index - 1, x_index - 1]

    @classmethod
    def reconstruct_from_vector(cls, vector, histinfo):
        """Construct a Histogram object from vector and histinfo

        Args:
        vector -- 1D ndarray of floats, this vector is translated into a histogram.
        histinfo -- a dict that has histogram information.
          The information is generated in vectorize_PD.save_histogram_information().
        """
        x_edges = np.array(histinfo["x-edges"], dtype=float)
        y_edges = np.array(histinfo["y-edges"], dtype=float)
        y_indices = histinfo["y-indices"]
        x_indices = histinfo["x-indices"]
        values = np.zeros((len(y_edges) - 1, len(x_edges) - 1), dtype=vector.dtype)
        for y, x, val in zip(y_indices, x_indices, vector):
            values[y, x] = val

        return cls(values, HistoSpec(x_edges, y_edges))

    def binary_histogram_by_ranking(self, rank_range, sign=None, use_abs=True):
        """Create a binary (bool) histogram by ranking of histogram bin values.

        Args:
        rank_range: a pair of (minimum rank, maximum rank)
        sign: if this value is not None, only bins with positive(sign=+1) or
              negative(sign=-1) value is selected
        use_abs: if true, to compute a ranking, absolute value of each bin is used
        """
        if use_abs:
            values = np.abs(self.values).flatten()
        else:
            values = self.values.flatten()

        min_rank, max_rank = rank_range
        ranks = np.argsort(values.flatten())[::-1][min_rank : max_rank - min_rank + 1]
        mask = np.full_like(values, False, dtype=bool)
        mask[ranks] = True

        mask = mask.reshape(self.values.shape)
        if sign is not None:
            mask &= sign * self.values > 0
        return BinaryHistogram(mask, self.xedges, self.yedges)

    def apply_gaussian_filter(self, sigma):
        """Apply a Gaussian filter to the histogram.

        Note: This method works correctly only if the scale of x-axis and
        the scale of y-axis are the same. This should be fixed in the future.

        Args:
        sigma -- standard deviation of the gaussian distribution
        """
        self.values = gaussian_filter(self.values, self.histospec.normalized_standard_deviation(sigma))

    def apply_weight(self, weight_func):
        """Apply (multiply) weights to all values in bins.

        The weight is computed by weight_func.
        Args:
        weight_func -- an applicable object with two parameters,
          x (birth time) and y (death time)
        """
        xs, ys = self.histospec.coordinates_of_center_of_bins()
        self.values *= np.vectorize(weight_func)(xs, ys)

    def multiply_histogram(self, val):
        """Apply (multiply) a uniform weight to all values in bins.

        Args:
        val -- weight
        """
        self.values *= val


class Ruler(object):
    """A pair of min-max (range) and # of bins."""

    def __init__(self, minmax, bins):
        self.minmax = minmax
        self.bins = bins

    def min(self):
        return self.minmax[0]

    def max(self):
        return self.minmax[1]

    def bin_width(self):
        return (self.max() - self.min()) / float(self.bins)

    def edges(self):
        return np.linspace(self.minmax[0], self.minmax[1], self.bins + 1)

    @staticmethod
    def create_xy_rulers(x_range, xbins, y_range, ybins, diagram):
        x_range = x_range or diagram.minmax_of_birthdeath_time()
        y_range = y_range or x_range
        ybins = ybins or xbins
        return (Ruler(x_range, xbins), Ruler(y_range, ybins))


class HistoSpec(object):
    def __init__(self, xedges, yedges, sign_flipped=False, x_ruler=None, y_ruler=None):
        self.xedges = xedges
        self.yedges = yedges
        self.sign_flipped = sign_flipped
        self.x_ruler = x_ruler
        self.y_ruler = y_ruler

    @staticmethod
    def from_rulers(x_ruler, y_ruler, sign_flipped=False):
        return HistoSpec(x_ruler.edges(), y_ruler.edges(), sign_flipped, x_ruler, y_ruler)

    def xy_extent(self):
        """Return [xmin, xmax, ymin, ymax]."""
        return [self.xedges[0], self.xedges[-1], self.yedges[0], self.yedges[-1]]

    def x_range(self):
        """Return the range of the histogram along with x-axis as a pair of (min, max)."""
        return (self.xedges[0], self.xedges[-1])

    def y_range(self):
        """Return the range of the histogram along with y-axis as a pair of (min, max)."""
        return (self.yedges[0], self.yedges[-1])

    def x_bins(self):
        """Return the number of bins of x-axis."""
        return self.xedges.size - 1

    def y_bins(self):
        """Return the number of bins of y-axis."""
        return self.yedges.size - 1

    def vectorize_mask(self):
        """Internally used by vectorize()."""
        if self.sign_flipped:
            return self.xedges_of_bins() > self.yedges_of_bins()
        else:
            return self.xedges_of_bins() < self.yedges_of_bins()

    def xedges_of_bins(self):
        """Internally used by vectorize()."""
        xedges = self.xedges[1:] if self.sign_flipped else self.xedges[:-1]
        return np.repeat(xedges.reshape((1, self.x_bins())), self.y_bins(), axis=0)

    def yedges_of_bins(self):
        """Internally used by vectorize()."""
        yedges = self.yedges[:-1] if self.sign_flipped else self.yedges[1:]
        return np.repeat(yedges.reshape((self.y_bins(), 1)), self.x_bins(), axis=1)

    def normalized_standard_deviation(self, sigma):
        """Compute the standard deviation from x-scale and sigma.

        This method is internally used from apply_gaussian_filter.
        """
        return sigma / self.x_ruler.bin_width()

    def coordinates_of_center_of_bins(self):
        """Internally used by vectorize()."""
        x_centers = (self.xedges[:-1] + self.xedges[1:]) / 2
        y_centers = (self.yedges[:-1] + self.yedges[1:]) / 2
        xs = np.repeat(x_centers.reshape((1, self.x_bins())), self.y_bins(), axis=0)
        ys = np.repeat(y_centers.reshape((self.y_bins(), 1)), self.x_bins(), axis=1)
        return (xs, ys)

    def centers_of_vectorize_bins(self):
        xs, ys = self.coordinates_of_center_of_bins()
        mask = self.vectorize_mask()
        return np.vstack((xs[mask], ys[mask])).transpose()

    def indices_for_vectorization(self):
        """Internally used by vectorize()."""
        yindices, xindices = np.indices((self.y_bins(), self.x_bins()))
        mask = self.vectorize_mask()
        return (yindices[mask], xindices[mask])

    def vector_size(self):
        return np.sum(self.vectorize_mask())

    def histogram_from_diagram(self, diagram, cls=Histogram):
        values, *_ = np.histogram2d(
            diagram.deaths,
            diagram.births,
            bins=(self.y_bins(), self.x_bins()),
            range=((self.y_range(), self.x_range())),
        )
        ess_values, _ = np.histogram(diagram.essential_births, bins=self.x_bins(), range=self.x_range())

        return cls(values, self, ess_values)

    def histogram_from_vector(self, vector, cls=Histogram):
        y_indices, x_indices = self.indices_for_vectorization()
        values = np.zeros((self.y_bins(), self.x_bins()), dtype=vector.dtype)
        for y, x, val in zip(y_indices, x_indices, vector):
            values[y, x] = val

        return cls(values, self)

    def histogram_from_2darray(self, values, ess_values=None, cls=Histogram):
        return cls(values, self, ess_values)


def PDHistogram(diagram, x_ruler, y_ruler):
    spec = HistoSpec.from_rulers(x_ruler, y_ruler, diagram.sign_flipped)
    return spec.histogram_from_diagram(diagram)


class BinaryHistogram(Histogram):
    """A PD histogram whose values are bool."""

    def filter_pairs(self, pairs):
        return [pair for pair in pairs if self.value_at(pair.birth, pair.death)]
