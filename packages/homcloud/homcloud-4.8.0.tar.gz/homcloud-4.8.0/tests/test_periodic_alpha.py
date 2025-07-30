from operator import attrgetter

import numpy as np
import pytest

import homcloud.cgal_info as cgal_info
from homcloud.alpha_filtration import PeriodicAlphaShape3
from homcloud.pdgm import PDGM


def multiplicity_pd(path, dim, birth, death, epsilon=0.01):
    count = 0
    with PDGM.open(path, dim) as pdgm:
        for b, d in zip(pdgm.births, pdgm.deaths):
            if abs(b - birth) < epsilon and abs(d - death) < epsilon:
                count += 1
    return count


class TestPeriodicAlphaShape(object):
    @pytest.mark.parametrize("additive_noise", [False, True])
    def test_sc_5x5x5_vertices(self, tmpdir, additive_noise, lattice_5x5x5):
        if additive_noise:
            pointcloud = lattice_5x5x5 + np.random.uniform(-0.00001, 0.00001, size=lattice_5x5x5.shape)
        else:
            pointcloud = lattice_5x5x5

        periodic_alpha = PeriodicAlphaShape3(pointcloud, False, False, [(-0.5, 4.5)] * 3)

        assert len(periodic_alpha.vertices()) == 125

        sorted_vertices = sorted(periodic_alpha.vertices(), key=attrgetter("vertex_index"))
        assert [v.vertex_index for v in sorted_vertices] == list(range(125))
        assert np.allclose(sorted_vertices[0].point(), (0, 0, 0), atol=0.0001)

        for vertex in periodic_alpha.vertices():
            assert vertex.vertices() == (vertex,)
        assert np.allclose(
            np.sort(np.array([vertex.point() for vertex in periodic_alpha.vertices()]), axis=0),
            np.sort(pointcloud, axis=0),
        )
        assert [v.weight() for v in periodic_alpha.vertices()] == [0.0 for i in range(125)]
        assert [v.birth_radius for v in periodic_alpha.vertices()] == [0.0 for i in range(125)]
        assert [v.group_name for v in periodic_alpha.vertices()] == [-1 for i in range(125)]
        filtration = periodic_alpha.create_filtration(True, None, True)
        pdgmpath = str(tmpdir.join("sc.pdgm"))
        filtration.compute_pdgm_and_save(pdgmpath)
        assert multiplicity_pd(pdgmpath, 0, 0, 0.25) == 124
        assert multiplicity_pd(pdgmpath, 1, 0.25, 0.5) == 248
        assert multiplicity_pd(pdgmpath, 2, 0.5, 0.75) == 124

        with PDGM.open(pdgmpath, 0) as pdgm:
            assert pdgm.alpha_information == {
                "chunktype": "alpha_information",
                "num_vertices": 125,
                "periodicity": [[-0.5, 4.5]] * 3,
                "weighted": False,
                "squared": True,
            }

    @pytest.mark.skipif(cgal_info.numerical_version < 1050601000, reason="CGAL version < 5.6")
    def test_case_non_cubic_box(self, tmpdir):
        lattice_5x4x5 = np.array([(x, y, z) for z in range(5) for y in range(4) for x in range(5)], dtype=float)
        lattice_5x4x5 += np.random.uniform(-0.00001, 0.00001, size=(5 * 4 * 5, 3))
        periodic_alpha = PeriodicAlphaShape3(lattice_5x4x5, False, False, [(-0.5, 4.5), (-0.5, 3.5), (-0.5, 4.5)])

        assert len(periodic_alpha.vertices()) == 100
        filtration = periodic_alpha.create_filtration(True, None, True)
        pdgmpath = str(tmpdir.join("sc.pdgm"))
        filtration.compute_pdgm_and_save(pdgmpath)

        assert multiplicity_pd(pdgmpath, 0, 0, 0.25) == 99
        assert multiplicity_pd(pdgmpath, 1, 0.25, 0.50) == 198
        assert multiplicity_pd(pdgmpath, 2, 0.5, 0.75) == 99

        with PDGM.open(pdgmpath, 0) as pdgm:
            assert pdgm.alpha_information == {
                "chunktype": "alpha_information",
                "num_vertices": 100,
                "periodicity": [[-0.5, 4.5], [-0.5, 3.5], [-0.5, 4.5]],
                "weighted": False,
                "squared": True,
            }

    def test_optimal_volume(self, lattice_5x5x5):
        import homcloud.interface as hc

        pdlist = hc.PDList.from_alpha_filtration(
            lattice_5x5x5 + np.random.uniform(-0.00001, 0.00001, size=lattice_5x5x5.shape),
            save_boundary_map=True,
            periodicity=([(-0.5, 4.5)] * 3),
        )
        pair = pdlist.dth_diagram(1).nearest_pair_to(0.26, 0.49)
        sv = pair.stable_volume(0.001)
        assert len(sv.boundary_points()) == 4
        assert len(sv.boundary()) == 4
        boundary = sv.boundary()
        for edge in boundary:
            p, q = edge
            d1, d2, d3 = np.sort(np.abs(np.array(p) - np.array(q)))
            assert d1 == pytest.approx(0, abs=0.001)
            assert d2 == pytest.approx(0, abs=0.001)
            assert d3 == pytest.approx(1, abs=0.001) or d3 == pytest.approx(4, abs=0.001)
