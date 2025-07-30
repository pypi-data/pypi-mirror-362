import os

import pytest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import homcloud.codebook as codebook
import homcloud.pdgm as pdgm


@pytest.fixture
def pds(datadir):
    def load_pd(k):
        path = os.path.join(datadir, f"codebook_pds/pd_{k}.txt")
        return pdgm.SimplePDGM.load_from_textfile(path)

    return [load_pd(k) for k in range(10)]


def weighting_function(b, d):
    lifetime = abs(d - b)
    if lifetime < 0.5:
        return 0
    if lifetime < 1.5:
        return lifetime - 0.5
    return 1


def lsort2d(a):
    a = np.array(a)
    return a[np.lexsort(a.T), :]


class TestPBoW:
    class Test_without_weight:
        class Test_init:
            def test_default_random_state(self):
                codebook.PBoW(1000, 8)

            def test_int_random_state(self):
                codebook.PBoW(1000, 8, random_state=32)

        def test_fit(self, pds):
            pbow = codebook.PBoW(1000, 3, random_state=821)
            assert pbow.kmeans is None
            pbow.fit(pds)
            assert pbow.kmeans is not None
            assert pbow.kmeans.cluster_centers_ is not None

        def test_vectorize(self, pds):
            pbow = codebook.PBoW(1000, 3, random_state=821)
            pbow.fit(pds)
            vector = pbow.vectorize(pds[0])
            u = [307, 469, 284]
            expected = np.sqrt(u) / np.linalg.norm(u)
            assert np.allclose(np.sort(vector), np.sort(expected))

        def test_cluster_centers(self, pds):
            pbow = codebook.PBoW(1000, 3, random_state=821)
            pbow.fit(pds)
            assert np.allclose(
                lsort2d(pbow.cluster_centers),
                lsort2d([[3.01925043, 5.46093298], [1.95170448, 2.52094166], [1.02073396, 4.3076858]]),
            )

    class Test_with_weight:
        def test_fit(self, pds):
            pbow = codebook.PBoW(1000, 3, weighting_function=weighting_function, random_state=821)
            pbow.fit(pds)
            assert np.allclose(
                lsort2d(pbow.cluster_centers),
                lsort2d([[2.94204235, 5.54154508], [0.92366807, 4.48630176], [1.71258208, 3.07966693]]),
            )

        def test_vectorize(self, pds):
            pbow = codebook.PBoW(1000, 3, weighting_function=weighting_function, random_state=821, normalize=False)
            pbow.fit(pds)
            assert np.allclose(np.sort(pbow.vectorize(pds[0])), np.sort([298.69863402, 258.0, 91.64135729]))


class TestStablePBoW:
    class Test_without_weight:
        def test_fit(self, pds):
            spbow = codebook.StablePBoW(1000, 3, random_state=821)
            spbow.fit(pds)
            assert np.allclose(
                lsort2d(spbow.cluster_centers),
                lsort2d([[3.03123528, 5.47002996], [1.95663899, 2.49544171], [1.07518623, 4.27283121]]),
            )
            assert np.allclose(np.sort(spbow.cluster_weights), np.sort([0.26144749, 0.43325388, 0.30529864]))
            # assert np.allclose(
            #     spbow.cluster_covariances,
            #     [[[ 1.79841135e-01, -8.74649064e-02],
            #       [-8.74649064e-02, 2.21499434e-01]],
            #      [[ 1.34309407e-01, 8.76435031e-02],
            #       [ 8.76435031e-02, 1.24899702e-01]],
            #      [[ 3.27157040e-01, 1.95987894e-05],
            #       [ 1.95987894e-05, 2.79616056e-01]]]
            # )
            assert spbow.cluster_covariances.shape == (3, 2, 2)

        class Test_vectorize:
            def test_without_normalize(self, pds):
                spbow = codebook.StablePBoW(1000, 3, random_state=821, normalize=False)
                spbow.fit(pds)
                assert np.allclose(np.sort(spbow.vectorize(pds[0])), np.sort([34.06056694, 162.30619526, 23.94188976]))

            def test_with_normalize(self, pds):
                spbow = codebook.StablePBoW(1000, 3, random_state=821, normalize=True)
                spbow.fit(pds)
                v = np.array([34.06056694, 162.30619526, 23.94188976])
                expected = np.sqrt(v) / np.linalg.norm(v)
                assert np.allclose(np.sort(spbow.vectorize(pds[0])), np.sort(expected))

        def test_plot_gmm_density_estimation(self, pds, picture_dir):
            outpath = str(picture_dir.joinpath("codebook_sPBoW_1.png"))
            spbow = codebook.StablePBoW(1000, 3, random_state=821)
            spbow.fit(pds)
            fig, ax = plt.subplots()
            ax.set_aspect("equal")
            spbow.plot_gmm_density_estimation(ax, (0, 7), 256)
            ax.add_line(Line2D((0, 7), (0, 7), linewidth=1, color="black"))
            fig.savefig(outpath)

    class Test_with_weight:
        def test_fit(self, pds):
            spbow = codebook.StablePBoW(1000, 3, random_state=821, weighting_function=weighting_function)
            spbow.fit(pds)
            assert np.allclose(
                lsort2d(spbow.cluster_centers),
                lsort2d([[2.95571761, 5.55503631], [1.0253073, 4.36596102], [1.86385633, 2.73796543]]),
            )

        def test_vectorize(self, pds):
            spbow = codebook.StablePBoW(
                1000, 3, random_state=821, weighting_function=weighting_function, normalize=False
            )
            spbow.fit(pds)
            assert np.allclose(np.sort(spbow.vectorize(pds[0])), np.sort([58.70665629, 37.16256777, 5.17155546]))

        def test_plot_gmm_density_estimation(self, pds, picture_dir):
            outpath = str(picture_dir.joinpath("codebook_sPBoW_2.png"))
            spbow = codebook.StablePBoW(1000, 3, random_state=821, weighting_function=weighting_function)
            spbow.fit(pds)
            fig, ax = plt.subplots()
            ax.set_aspect("equal")
            spbow.plot_gmm_density_estimation(ax, (0, 7), 256)
            ax.add_line(Line2D((0, 7), (0, 7), linewidth=1, color="black"))
            fig.savefig(outpath)


class TestPFV:
    def test_vectorize(self, pds):
        pfv = codebook.PFV(1000, 3, random_state=821, weighting_function=weighting_function)
        pfv.fit(pds)
        expected = [
            3.22722753,
            -6.64272193,
            29.69096701,
            32.83770879,
            12.24513142,
            -12.87951575,
            26.54489239,
            32.77945265,
            19.97563371,
            -32.13695718,
            44.48873629,
            50.31785117,
        ]
        assert np.allclose(np.sort(pfv.vectorize(pds[0])), np.sort(expected))
