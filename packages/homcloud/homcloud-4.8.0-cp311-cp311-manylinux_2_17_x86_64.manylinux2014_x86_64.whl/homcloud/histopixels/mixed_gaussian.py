import math

import numpy as np
from sklearn import mixture


class MixedGaussians2(object):
    """Represents 2 mixed gaussians."""

    def __init__(self, gaussians):
        self.gaussians = gaussians
        self.boundary = self.find_boundary()

    def find_boundary(self):
        """Compute the value that which density is larger is changing."""
        (g0, g1) = self.gaussians
        for k in np.linspace(g0.mean, g1.mean, 256):
            if g0.density(k) < g1.density(k):
                return k
        return None

    @staticmethod
    def fit(pixels):
        """Fitting the values of pixels by 2-components GMM."""
        gmm = mixture.GMM(n_components=2)
        gmm.fit(pixels.reshape(pixels.size, 1))
        return MixedGaussians2(WeightedNormal.from_gmm(gmm))


class WeightedNormal(object):
    """This class represents weighted normal distribution.

    If weight is 1.0, the instance represents normal gaussian distribution.
    """

    def __init__(self, mean, var, weight):
        self.mean = mean
        self.var = var
        self.sd = math.sqrt(var)
        self.weight = weight

    def density(self, x):
        """Returns the density at x (in float)"""
        from scipy import stats

        return self.weight * stats.norm.pdf(x, self.mean, self.sd)

    @staticmethod
    def from_gmm(gmm):
        """Create a list of WeightedNormal objecsts from sklearn.mixture.GMM."""
        means = gmm.means_.flatten()
        variances = gmm.covars_.flatten()
        weights = gmm.weights_
        dists = [WeightedNormal(m, v, w) for (m, v, w) in zip(means, variances, weights)]
        dists.sort(key=lambda d: d.mean)
        return dists
