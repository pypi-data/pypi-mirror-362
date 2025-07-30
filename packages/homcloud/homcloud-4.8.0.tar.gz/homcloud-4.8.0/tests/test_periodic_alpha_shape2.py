import numpy as np
import pytest

from homcloud.periodic_alpha_shape2 import PeriodicAlphaShape2


@pytest.fixture
def pc_3x3():
    pc = np.array([[x + 0.5, y + 0.5] for x in range(3) for y in range(3)])
    pc += np.random.uniform(-0.0001, 0.0001, size=pc.shape)
    return pc


@pytest.fixture
def alpha_shape_3x3(pc_3x3):
    return PeriodicAlphaShape2(pc_3x3, False, False, 0, 3, 0, 3)


def simplex(indices):
    return tuple(sorted(indices))


def rectangular_vertices_in_3x3(x, y):
    return [
        x * 3 + y,
        x * 3 + ((y + 1) % 3),
        ((x + 1) % 3) * 3 + y,
        ((x + 1) % 3) * 3 + ((y + 1) % 3),
    ]


class TestPeriodicAlphaShape2:
    class Test_init:
        def test_normal_case_3x3(self, pc_3x3):
            alpha_shape = PeriodicAlphaShape2(pc_3x3, False, False, 0, 3, 0, 3)
            assert len(alpha_shape.vertices()) == 9
            assert len(alpha_shape.edges()) == 27
            assert len(alpha_shape.faces()) == 18

        def test_normal_case_random200(self):
            xs = np.random.uniform(0, 2.0, size=200)
            ys = np.random.uniform(0, 3.0, size=200)

            PeriodicAlphaShape2(np.array([xs, ys]).transpose(), False, False, 0, 2.0, 0, 3.0)

        def test_weighted_case(self, pc_3x3):
            with pytest.raises(ValueError, match="2D Periodic alpha shape does not accept weighted points"):
                PeriodicAlphaShape2(pc_3x3, True, False, 0, 3, 0, 3)

        def test_invalid_domain(self, pc_3x3):
            with pytest.raises(ValueError, match="Periodic region invalid"):
                PeriodicAlphaShape2(pc_3x3, False, False, 0, 0, 3, 3)

        def test_too_anistropic_domain(self, pc_3x3):
            with pytest.raises(ValueError, match="Too anistropic periodic region is invalid"):
                PeriodicAlphaShape2(pc_3x3, False, False, 0, 1, 0, 2)

    class TestVertex:
        def test_vertex_index(self, alpha_shape_3x3):
            assert sorted([v.vertex_index for v in alpha_shape_3x3.vertices()]) == list(range(9))

        def test_birth_radius(self, alpha_shape_3x3):
            for v in alpha_shape_3x3.vertices():
                assert v.birth_radius == 0.0

    class TestEdge:
        def test_birth_radius(self, alpha_shape_3x3):
            birth_radii = sorted([e.birth_radius for e in alpha_shape_3x3.edges()])
            assert np.allclose(birth_radii[:18], np.full(18, 0.25), rtol=0.001)
            assert np.allclose(birth_radii[18:], np.full(9, 0.5), rtol=0.001)

        def test_vertices(self, alpha_shape_3x3):
            edges_index_pair = set([simplex(v.vertex_index for v in e.vertices()) for e in alpha_shape_3x3.edges()])
            expected_edges_horizontal = [simplex((k, (k + 3) % 9)) for k in range(9)]
            assert set(expected_edges_horizontal).issubset(edges_index_pair)
            expected_edges_vertical = [simplex((k, k // 3 * 3 + (k + 1) % 3)) for k in range(9)]
            assert set(expected_edges_vertical).issubset(edges_index_pair)

            for x in range(3):
                for y in range(3):
                    p = rectangular_vertices_in_3x3(x, y)
                    e1 = simplex((p[0], p[3]))
                    e2 = simplex((p[1], p[2]))
                    assert (e1 in edges_index_pair) or (e2 in edges_index_pair)
                    assert not ((e1 in edges_index_pair) and (e2 in edges_index_pair))

    class TestFace:
        def test_birth_radius(self, alpha_shape_3x3):
            birth_radii = sorted([f.birth_radius for f in alpha_shape_3x3.faces()])
            assert np.allclose(birth_radii, np.full(18, 0.5), rtol=0.001)

        def test_vertices(self, alpha_shape_3x3):
            faces_vertices_tuples = set(
                [simplex(v.vertex_index for v in f.vertices()) for f in alpha_shape_3x3.faces()]
            )

            assert len(faces_vertices_tuples) == 18

            for f in faces_vertices_tuples:
                assert len(f) == 3

            for x in range(3):
                for y in range(3):
                    p = rectangular_vertices_in_3x3(x, y)
                    f0 = simplex((p[1], p[2], p[3]))
                    f1 = simplex((p[0], p[2], p[3]))
                    f2 = simplex((p[0], p[1], p[3]))
                    f3 = simplex((p[0], p[1], p[2]))
                    assert ((f0 in faces_vertices_tuples) and (f3 in faces_vertices_tuples)) or (
                        (f1 in faces_vertices_tuples) and (f2 in faces_vertices_tuples)
                    )
