# pylint: disable=C0111, R0201, C0103
from itertools import chain

import numpy as np
import pytest

from homcloud.alpha_filtration import AlphaShape2
from homcloud import alpha_shape2


def square_circumradius(points):
    from numpy.linalg import norm

    a = norm(points[0, :] - points[1, :])
    b = norm(points[1, :] - points[2, :])
    c = norm(points[2, :] - points[0, :])
    return (a * b * c) ** 2 / ((a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c))


class TestAlphaShape2(object):
    class Test_new(object):
        def test_case_2d_points(self):
            AlphaShape2(np.array([[1.0, 2.0], [3.0, 4.0], [10.0, -1.0]]), False, False)

        def test_case_2d_points_groupnames(self):
            AlphaShape2(np.array([[1.0, 2.0, 0], [3.0, 4.0, 0], [10.0, -1.0, 1]]), False, True)

        def test_case_2d_points_weights(self):
            AlphaShape2(np.array([[1.0, 2.0, 1.0], [3.0, 4.0, 2.0], [10.0, -1.0, 2.0]]), True, False)

        def test_case_shape_mismatch(self):
            with pytest.raises(ValueError):
                AlphaShape2(np.array([[1.0, 2.0, 1.0], [3.0, 4.0, 2.0], [10.0, -1.0, 2.0]]), False, False)

        def test_case_type_error(self):
            with pytest.raises(TypeError):
                AlphaShape2(np.array([[True, False], [False, False], [True, True]]), False, False)

        def test_case_shape_mismatch2(self):
            with pytest.raises(ValueError):
                AlphaShape2(np.array([[1.0, 2.0, 3.0, 4.0], [10.0, -1.0, 8.0, 1.0]]), False, False)

    class Test_vertices(object):
        def test_case_tegragon(self, tetragon):
            alpha_tetragon = AlphaShape2(tetragon, False, False)
            vertices = alpha_tetragon.vertices()
            assert len(vertices) == 4
            assert np.allclose(np.sort(tetragon, axis=0), np.sort(np.array([v.point() for v in vertices]), axis=0))
            assert [0, 1, 2, 3] == sorted([v.vertex_index for v in vertices])
            assert [0.0] * 4 == [v.weight() for v in vertices]
            for vertex in vertices:
                assert (vertex,) == vertex.vertices()
            assert vertices == alpha_tetragon.vertices()
            assert all(v.group_name == -1 for v in vertices)

        def test_case_tetragon_with_groupname(self, tetragon_groupname):
            alpha_shape = AlphaShape2(tetragon_groupname, False, True)
            assert sorted((v.vertex_index, v.group_name) for v in alpha_shape.vertices()) == [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 1),
            ]

        def test_case_tetragon_weighted(self, tetragon_weighted):
            alpha_shape = AlphaShape2(tetragon_weighted, True, False)
            assert sorted((v.vertex_index, v.weight(), v.birth_radius) for v in alpha_shape.vertices()) == [
                (0, 1.0, -1.0),
                (1, 4.0, -4.0),
                (2, 0.0, -0.0),
                (3, 1.0, -1.0),
            ]

    def test_coordinates(self, tetragon):
        assert np.allclose(AlphaShape2(tetragon, False, False).coordinates, tetragon)

    class Test_faces(object):
        def test_case_tetragon(self, tetragon):
            alpha_shape = AlphaShape2(tetragon, False, False)
            faces = alpha_shape.faces()
            assert 2 == len(faces)
            assert np.allclose(
                [square_circumradius(tetragon[[0, 2, 3], :]), square_circumradius(tetragon[[0, 1, 2], :])],
                sorted([f.birth_radius for f in faces]),
            )
            vs1 = faces[0].vertices()
            vs2 = faces[1].vertices()
            assert 2 == len(set(vs1).intersection(vs2))
            assert set([0, 1, 2, 3]) == set(v.vertex_index for v in vs1 + vs2)

        def test_case_obtuse_triangle(self, obtuse_triangle):
            alpha_shape = AlphaShape2(obtuse_triangle, False, False)
            assert np.isclose(square_circumradius(obtuse_triangle), alpha_shape.faces()[0].birth_radius)

        def test_case_weighted_tetragon(self, tetragon_weighted):
            alpha_shape = AlphaShape2(tetragon_weighted, True, False)
            faces = alpha_shape.faces()
            assert sorted(sorted(v.vertex_index for v in f.vertices()) for f in faces) == [[0, 1, 2], [0, 2, 3]]
            assert np.all(
                np.array(sorted(f.birth_radius for f in faces))
                < [
                    square_circumradius(tetragon_weighted[[0, 2, 3], :2]),
                    square_circumradius(tetragon_weighted[[0, 1, 2], :2]),
                ]
            )

    class Test_edges(object):
        def test_case_tetragon(self, tetragon):
            edges = AlphaShape2(tetragon, False, False).edges()
            assert len(edges) == 5
            assert all(len(e.vertices()) == 2 for e in edges)
            assert sorted(chain.from_iterable([v.vertex_index for v in e.vertices()] for e in edges)) == [
                0,
                0,
                0,
                1,
                1,
                2,
                2,
                2,
                3,
                3,
            ]
            assert np.allclose(
                sorted([e.birth_radius for e in edges]),
                sorted([(25 + 9) / 4.0, (25 + 9) / 4.0, 36 / 4, 32 / 4.0, 20 / 4.0]),
            )

        def test_case_obtuse_triagnle(self, obtuse_triangle):
            alpha_shape = AlphaShape2(obtuse_triangle, False, False)
            assert np.allclose(
                [(0.2**2 + 0.1**2) / 4, (0.8**2 + 0.1**2) / 4, square_circumradius(obtuse_triangle)],
                sorted([e.birth_radius for e in alpha_shape.edges()]),
            )

        def test_case_weighted_tetragon(self, tetragon_weighted):
            def r(x0, x1, ell):
                return ((x1 - x0 + ell**2) / (2 * ell)) ** 2 - x1

            alpha_shape = AlphaShape2(tetragon_weighted, True, False)
            edges = alpha_shape.edges()
            print(r(1, 1, np.sqrt(3**2 + 4**2)))
            assert np.allclose(
                sorted(e.birth_radius for e in edges),
                sorted(
                    [
                        r(1, 4, np.sqrt(3**2 + 5**2)),
                        r(4, 0, np.sqrt(3**2 + 5**2)),
                        r(1, 0, np.sqrt(6**2)),
                        r(1, 1, np.sqrt(2**2 + 4**2)),
                        r(1, 0, np.sqrt(4**2 + 4**2)),
                    ]
                ),
            )

    def test_cannot_create_Vertex_Edge_Face_by_constructor(self):
        with pytest.raises(TypeError):
            alpha_shape2.Vertex()

        with pytest.raises(TypeError):
            alpha_shape2.Edge()
        with pytest.raises(TypeError):
            alpha_shape2.Face()

    class Test_subsets(object):
        def test_case_tetragon(self, tetragon):
            shape = AlphaShape2(tetragon, False, False)
            assert shape.subsets() == {}

        def test_case_tetragon_groupname(self, tetragon_groupname):
            key = AlphaShape2.simplex_key

            shape = AlphaShape2(tetragon_groupname, False, True)
            subsets = shape.subsets()
            assert sorted(subsets.keys()) == [0, 1]
            assert subsets[0].group_name == 0
            assert sorted(key(s) for s in subsets[0].simplices) == sorted(
                [
                    (0,),
                    (1,),
                    (2,),
                    (0, 1),
                    (0, 2),
                    (1, 2),
                    (0, 1, 2),
                ]
            )
            assert np.allclose(subsets[0].coordinates, shape.coordinates)
            assert subsets[0].dim == 2
            assert subsets[1].group_name == 1

            assert sorted(key(s) for s in subsets[1].simplices) == [(3,)]
            assert np.allclose(subsets[1].coordinates, shape.coordinates)
            assert subsets[1].dim == 2
            for subset in subsets.values():
                assert subset.isacyclic()

    class Test_all_subsets_acyclic:
        def test_for_tetragon_with_acyclicity(self, tetragon_groupname):
            alpha_shape = AlphaShape2(tetragon_groupname, False, True)
            assert alpha_shape.all_subsets_acyclic()

        def test_for_triangle_without_acyclicity(self, triangle_groupname_noacyclic):
            alpha_shape = AlphaShape2(triangle_groupname_noacyclic, False, True)
            assert not alpha_shape.all_subsets_acyclic()

    def test_become_partial_shape(self, tetragon_groupname):
        alpha_shape = AlphaShape2(tetragon_groupname, False, True)
        alpha_shape.become_partial_shape()
        assert set(AlphaShape2.simplex_key(s) for s in alpha_shape.simplices if s.birth_radius == -np.inf) == set(
            [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2), (3,)]
        )
        assert set(AlphaShape2.simplex_key(s) for s in alpha_shape.simplices if s.birth_radius != -np.inf) == set(
            [
                (0, 3),
                (2, 3),
                (0, 2, 3),
            ]
        )
