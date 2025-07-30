import pytest
import numpy as np

from homcloud.maximal_0_component import Graph
from homcloud.pdgm import PDGM
from homcloud.alpha_filtration import AlphaShape


@pytest.fixture
def tetrahedron_pdgm(tmpdir):
    pointcloud = np.array(
        [
            [1, 1, 10, 0.003],
            [0, 0, 0, 0.002],
            [3, 0, 0, 0.001],
            [1, 2, 0, 0.000],
        ],
        dtype=float,
    )
    alpha_shape = AlphaShape.build(pointcloud, 3, True, None, None)
    filt = alpha_shape.create_filtration(True, None, True, False)
    path = str(tmpdir.join("tetrahedron.pdgm"))
    filt.compute_pdgm_and_save(path, None, True)
    with PDGM.open(path, 0) as pdgm:
        yield pdgm


class TestGraph(object):
    def graph(self, pdgm, death, epsilon):
        k = np.nonzero(np.isclose(pdgm.deaths, death, 0.01))[0][0]
        return Graph(pdgm, pdgm.birth_indices[k], pdgm.death_indices[k], epsilon)

    @pytest.mark.parametrize(
        "death, epsilon, expected",
        [
            (1.25, 0.0, [3]),
            (2.0, 0.0, [2]),
            (25.25, 0.0, [1, 2, 3]),
        ],
    )
    def test_maximal_component(self, tetrahedron_pdgm, death, epsilon, expected):
        graph = self.graph(tetrahedron_pdgm, death, epsilon)
        assert sorted(graph.birth_component) == expected

    @pytest.mark.parametrize(
        "death, epsilon, expected",
        [
            (1.25, 0.0, [1]),
            (2.0, 0.0, [1, 3]),
            (25.25, 0.0, [0]),
        ],
    )
    def test_elder_component(self, tetrahedron_pdgm, death, epsilon, expected):
        graph = self.graph(tetrahedron_pdgm, death, epsilon)
        assert sorted(graph.elder_component) == expected
