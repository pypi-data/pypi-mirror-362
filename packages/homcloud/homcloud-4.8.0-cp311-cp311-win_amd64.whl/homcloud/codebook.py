"""
References:

* https://link.springer.com/article/10.1007/s10462-020-09897-4
* https://github.com/bziiuj/pcodebooks
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from matplotlib.colors import LogNorm


def random_sampling_pairs(diagrams, n, weighting_function, random_state):
    births = np.concatenate([pd.births for pd in diagrams])
    deaths = np.concatenate([pd.deaths for pd in diagrams])
    npairs = births.shape[0]

    if weighting_function:
        weights = np.array([weighting_function(b, d) for b, d in zip(births, deaths)])
        p = weights / np.sum(weights)
    else:
        p = weights = None

    pairs = np.stack([births, deaths], axis=-1)
    return pairs[random_state.choice(np.arange(npairs), n, p=p), :], weights


def setup_random_state(random_state):
    if random_state is None:
        return np.random.RandomState()
    elif isinstance(random_state, int):
        return np.random.RandomState(random_state)
    else:
        return random_state


def diagram_weights(pd, weighting_function):
    if weighting_function:
        return np.array([weighting_function(b, d) for b, d in zip(pd.births, pd.deaths)])
    else:
        return None


def diagram2array(diagram):
    return np.stack([diagram.births, diagram.deaths], axis=-1)


def bow_normalize(vector, really_normalize):
    if not really_normalize:
        return vector

    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    else:
        return np.sqrt(vector) / norm


class PBoW:
    def __init__(self, n_random_sampled_pairs, n_clusters, weighting_function=None, random_state=None, normalize=True):
        self.n_random_sampled_pairs = n_random_sampled_pairs
        self.n_clusters = n_clusters
        self.weighting_function = weighting_function
        self.random_state = setup_random_state(random_state)
        self.kmeans = None
        self.normalize = normalize

    def fit(self, diagrams):
        sampled_pairs, _ = random_sampling_pairs(
            diagrams, self.n_random_sampled_pairs, self.weighting_function, self.random_state
        )
        self.kmeans = KMeans(self.n_clusters, init="k-means++", n_init=1, random_state=self.random_state)
        self.kmeans.fit(sampled_pairs)

    @property
    def cluster_centers(self):
        return self.kmeans.cluster_centers_

    def vectorize(self, diagram):
        labels = self.kmeans.predict(np.stack([diagram.births, diagram.deaths], axis=-1))
        counts = np.bincount(labels, diagram_weights(diagram, self.weighting_function), self.n_clusters)
        return bow_normalize(counts, self.normalize)


class GMMClusteringBase:
    def __init__(self, n_random_sampled_pairs, n_clusters, weighting_function=None, random_state=None):
        self.n_random_sampled_pairs = n_random_sampled_pairs
        self.n_clusters = n_clusters
        self.weighting_function = weighting_function
        self.random_state = setup_random_state(random_state)
        self.gmm = None

    def fit(self, diagrams):
        sampled_pairs, _ = random_sampling_pairs(
            diagrams, self.n_random_sampled_pairs, self.weighting_function, self.random_state
        )
        self.gmm = GaussianMixture(self.n_clusters, random_state=self.random_state)
        self.gmm.fit(sampled_pairs)

    @property
    def cluster_centers(self):
        return self.gmm.means_

    @property
    def cluster_weights(self):
        return self.gmm.weights_

    @property
    def cluster_covariances(self):
        return self.gmm.covariances_

    def plot_gmm_density_estimation(self, ax, x_range, x_num, y_range=None, y_num=None):
        if y_range is None:
            y_range = x_range
        if y_num is None:
            y_num = x_num
        x, y = np.meshgrid(np.linspace(x_range[0], x_range[1], x_num), np.linspace(y_range[0], y_range[1], y_num))
        xx = np.array([x.ravel(), y.ravel()]).T
        z = -self.gmm.score_samples(xx)
        z = z.reshape(x.shape)
        zmax = np.max(z)
        ax.contour(x, y, z, norm=LogNorm(vmin=1.0, vmax=zmax), levels=np.logspace(0, np.log(zmax), 20))


class StablePBoW(GMMClusteringBase):
    def __init__(self, n_random_sampled_pairs, n_clusters, weighting_function=None, random_state=None, normalize=True):
        super().__init__(n_random_sampled_pairs, n_clusters, weighting_function, random_state)
        self.normalize = normalize

    def vectorize(self, diagram):
        wlogprob = self.gmm._estimate_weighted_log_prob(np.stack([diagram.births, diagram.deaths], axis=-1))
        if self.weighting_function is None:
            return bow_normalize(np.sum(np.exp(wlogprob), axis=0), self.normalize)
        else:
            dweights = diagram_weights(diagram, self.weighting_function)
            mask = dweights > 0
            return bow_normalize(
                np.sum(np.exp(wlogprob[mask] + np.log(dweights[mask].reshape(-1, 1))), axis=0), self.normalize
            )


# * https://www.vlfeat.org/api/fisher-fundamentals.html
# * F. Perronnin and C. Dance. Fisher kenrels on visual vocabularies
#   for image categorizaton. In Proc. CVPR, 2006.
# * Florent Perronnin, Jorge Sánchez, and Thomas Mensink.
#   Improving the fisher kernel for large-scale image classification. In Proc. ECCV, 2010.
class PFV(GMMClusteringBase):
    def __init__(self, n_random_sampled_pairs, n_clusters, weighting_function=None, random_state=None, normalize=0.5):
        super().__init__(n_random_sampled_pairs, n_clusters, weighting_function, random_state)
        self.normalize = normalize

    def vectorize(self, diagram):
        npairs = diagram.num_pairs
        n_clusters = self.n_clusters

        pairs = diagram2array(diagram)  # (npairs, 2)
        gammas = self.gmm.predict_proba(pairs)  # (npairs, n_clusters)
        r = pairs.reshape(npairs, 1, 2) - self.gmm.means_.reshape(1, n_clusters, 2)  # (npairs, n_clusters, 2)
        sigmas = np.diagonal(self.gmm.covariances_, 0, 1, 2)  # (n_clusters, 2)
        dmu = np.sum(
            gammas.reshape(npairs, n_clusters, 1) * r / sigmas.reshape(1, n_clusters, 2), axis=0
        )  # (n_clusters, 2)
        dsigma = np.sum(
            gammas.reshape(npairs, n_clusters, 1) * ((r**2 / (sigmas**2).reshape(1, n_clusters, 2)) - 1), axis=0
        )  # (n_clusters, 2)
        nc = np.sqrt(n_clusters * self.gmm.weights_).reshape(n_clusters, 1)  # (n_clusters, 2)
        pfv_mu = dmu / nc
        pfv_sigma = dsigma / nc / np.sqrt(2)
        pfv = np.hstack([pfv_mu, pfv_sigma]).ravel()
        if self.normalize:
            return np.sign(pfv) * (np.abs(pfv) ** self.normalize)
        else:
            return pfv
