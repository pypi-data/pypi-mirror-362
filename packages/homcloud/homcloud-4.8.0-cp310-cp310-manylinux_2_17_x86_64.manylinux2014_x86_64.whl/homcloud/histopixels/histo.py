import argparse
import math

import numpy as np
import scipy.ndimage
import scipy.misc
from scipy import stats
import matplotlib.pyplot as plt
from sklearn import mixture, cluster
from .mixed_gaussian import WeightedNormal


class RangeAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        begin, end = values.split(":")
        setattr(namespace, "pixelvalue_range", (float(begin), float(end)))


def load_pixels(path):
    image = scipy.ndimage.imread(path, flatten=True)
    if np.max(image) > 255:
        image //= 256

    return image


def plot_gaussians(gaussians, scale):
    for gaussian in gaussians:
        xs = np.linspace(0, 255, 256)
        ys = scale * gaussian.density(xs)
        plt.plot(xs, ys)
        plt.axvline(gaussian.mean, color="r")
        plt.axvline(gaussian.mean + gaussian.sd / 2, color="r")
        plt.axvline(gaussian.mean - gaussian.sd / 2, color="r")


def gmm_plot(pixels, n_components):
    gmm = mixture.GMM(n_components=n_components)
    gmm.fit(pixels)
    plot_gaussians(WeightedNormal.from_gmm(gmm), pixels.size)


class Cluster(object):
    def __init__(self, center, data):
        self.center = center
        self.data = data.flatten()
        (self.size,) = self.data.shape
        self.var = np.cov(self.data)
        self.sd = np.sqrt(self.var)

    def loglikelyhood(self):
        return np.sum(stats.norm.logpdf(self.data, self.center, self.sd))

    def f(self):
        return self.size * math.log(self.var)


def kmeans_bic(kmeans, pixels, n_components):
    clusters = [Cluster(kmeans.cluster_centers_[k, 0], pixels[kmeans.labels_ == k, :]) for k in range(0, n_components)]
    llh = sum([cl.loglikelyhood() for cl in clusters])
    return -2 * llh + 2 * n_components * math.log(pixels.size)


def kmeans_sic(kmeans, pixels, n_components):
    clusters = [Cluster(kmeans.cluster_centers_[k, 0], pixels[kmeans.labels_ == k, :]) for k in range(0, n_components)]
    return sum([cl.f() for cl in clusters]) + 2 * n_components * math.log(pixels.size)


def kmeans_plot(pixels, n_components):
    kmeans = cluster.KMeans(n_components)
    kmeans.fit(pixels)

    for k in range(0, n_components):
        cl = pixels[kmeans.labels_ == k, :]
        center = kmeans.cluster_centers_[k]
        boundary = np.max(cl)
        plt.axvline(boundary, color="g")
        plt.axvline(center, color="r")
        sd = math.sqrt(np.cov(cl.T))
        plt.axvline(center - sd / 2, color="r")
        plt.axvline(center + sd / 2, color="r")

    # print(kmeans_bic(kmeans, pixels, n_components))
    # print(kmeans_sic(kmeans, pixels, n_components))


def dpgmm_plot(pixels, n_components):
    dpgmm = mixture.DPGMM(n_components=n_components)
    dpgmm.fit(pixels)
    plot_gaussians(WeightedNormal.from_dpgmm(dpgmm), pixels.size)


def vbgmm_plot(pixels, n_components):
    vbgmm = mixture.VBGMM(n_components=n_components, alpha=1000)
    vbgmm.fit(pixels)
    print(vbgmm.n_components)
    plot_gaussians(WeightedNormal.from_dpgmm(vbgmm), pixels.size)


def dbscan_plot(pixels):
    dbscan = cluster.DBSCAN(eps=50)
    dbscan.fit(pixels)
    print(dbscan.core_sample_indices_)


def filter_by_range(pixels, minvalue, maxvalue):
    return pixels[(minvalue <= pixels) & (pixels <= maxvalue)]
