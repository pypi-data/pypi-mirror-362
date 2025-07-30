# pylint: disable=C0111, R0201, C0103
# C0111 for the lack of documentation,
# C0103 for upper characters in method name,
# R0201 for self is not used.
import math

import numpy as np
import pytest

from homcloud import alpha_shape3
from homcloud.alpha_filtration import AlphaShape3


class TestAlphaShape3(object):
    class Test_new(object):
        def test_case_3d_point(self):
            AlphaShape3(np.array([[1.0, 2.0, 3.0]]), False, False)

        def test_case_3d_point_with_weight(self):
            AlphaShape3(np.array([[1.0, 2.0, 3.0, 1.0]]), True, False)

        def test_case_3d_point_with_weight_and_groupname(self):
            AlphaShape3(np.array([[1.0, 2.0, 3.0, 1.0, -1]]), True, True)

        def test_case_3d_point_with_groupname(self):
            AlphaShape3(np.array([[1.0, 2.0, 3.0, -1]]), False, True)

        def test_case_wrong_shape(self):
            with pytest.raises(ValueError, match="Wrong shape of array"):
                AlphaShape3(np.array([1.0, 2.0, 3.0]), False, False)
            with pytest.raises(ValueError, match="Wrong shape of array"):
                AlphaShape3(np.array([[1.0, 2.0]]), False, False)
            with pytest.raises(ValueError, match="Wrong shape of array"):
                AlphaShape3(np.array([[1.0, 2.0, 3.0]]), True, False)
            with pytest.raises(ValueError, match="Wrong shape of array"):
                AlphaShape3(np.array([[1.0, 2.0, 3.0, 1.0]]), False, False)

        def test_case_array_type_error(self):
            with pytest.raises(TypeError, match="Array must be double"):
                AlphaShape3(np.array([[True, False, True]]), False, False)

        def test_case_negative_weight_error(self):
            with pytest.raises(ValueError):
                AlphaShape3(np.array([[1.0, 2.0, 3.0, -1.0]]), True, False)

    class Test_vertices(object):
        def test_case_tetrahedron(self, tetrahedron):
            alpha_shape = AlphaShape3(tetrahedron, False, False)
            vertices = alpha_shape.vertices()
            assert len(vertices) == 4
            assert sorted(vertex.vertex_index for vertex in vertices) == [0, 1, 2, 3]
            for vertex in vertices:
                assert vertex.vertices() == (vertex,)
            assert np.allclose(
                np.sort(np.array([vertex.point() for vertex in vertices]), axis=0), np.sort(tetrahedron, axis=0)
            )
            assert [0.0, 0.0, 0.0, 0.0] == [vertex.weight() for vertex in vertices]
            assert [v.birth_radius for v in vertices] == [0.0, 0.0, 0.0, 0.0]
            assert [v.group_name for v in vertices] == [-1, -1, -1, -1]
            assert alpha_shape.vertices() == vertices
            assert vertices[1] != vertices[0]

        def test_case_trigonal_dipyramid(self, trigonal_dipyramid):
            vertices = AlphaShape3(trigonal_dipyramid, False, False).vertices()
            assert len(vertices) == 5
            assert sorted(vertex.vertex_index for vertex in vertices) == [0, 1, 2, 3, 4]

        def test_case_weighted_tetrahedron(self, tetrahedron_weighted):
            vertices = AlphaShape3(tetrahedron_weighted, True, False).vertices()
            assert sorted([vertex.weight() for vertex in vertices]) == [1.0, 16.0, 16.0, 25.0]
            assert sorted([v.birth_radius for v in vertices]) == [-25.0, -16.0, -16.0, -1.0]

        def test_case_trigonal_dipyramid_groupname(self, trigonal_dipyramid_with_groupname):
            vertices = AlphaShape3(trigonal_dipyramid_with_groupname, False, True).vertices()
            assert sorted((v.vertex_index, v.group_name) for v in vertices) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1)]

    class Test_coordinates(object):
        def test_case_tetrahedron(self, tetrahedron):
            alpha_tetrahedron = AlphaShape3(tetrahedron, False, False)
            assert np.allclose(alpha_tetrahedron.coordinates, tetrahedron)

        def test_case_tetrahedron_weighted(self, tetrahedron_weighted):
            alpha_shape = AlphaShape3(tetrahedron_weighted, True, False)
            assert np.allclose(alpha_shape.coordinates, tetrahedron_weighted[:, 0:3])

    class Test_cells(object):
        def test_case_tetrahedron(self, tetrahedron):
            alpha_shape = AlphaShape3(tetrahedron, False, False)
            cells = alpha_shape.cells()
            assert len(cells) == 1
            assert cells[0].birth_radius == pytest.approx(21.06944444444444)
            assert alpha_shape.cells() == cells
            assert sorted([vertex.vertex_index for vertex in cells[0].vertices()]) == [0, 1, 2, 3]

        def test_case_trigonal_dipyramid(self, trigonal_dipyramid):
            cells = AlphaShape3(trigonal_dipyramid, False, False).cells()
            assert len(cells) == 2
            assert np.allclose(sorted([cell.birth_radius for cell in cells]), [19.700932333717798, 21.06944444444444])
            vs1 = cells[0].vertices()
            vs2 = cells[1].vertices()
            assert sorted(v.vertex_index for v in vs1 + vs2) == [0, 0, 1, 1, 2, 2, 3, 4]
            assert len(set(vs1).intersection(vs2)) == 3

    class Test_edges(object):
        def test_edges(self, tetrahedron):
            edges = AlphaShape3(tetrahedron, False, False).edges()
            assert len(edges) == 6
            pairs = []
            for edge in edges:
                vertices = edge.vertices()
                pairs.append(sorted([vertices[0].vertex_index, vertices[1].vertex_index]))
            assert sorted(pairs) == [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

            birth_radii = [edge.birth_radius for edge in edges]
            assert 4.0**2 in birth_radii
            assert 1.5**2 + 3.0**2 in birth_radii

        def test_case_trigonal_dipyramid(self, trigonal_dipyramid):
            assert len(AlphaShape3(trigonal_dipyramid, False, False).edges()) == 9

        def test_case_weighted_tetrahedron(self, tetrahedron_weighted):
            edges = AlphaShape3(tetrahedron_weighted, True, False).edges()
            birth_radii = [edge.birth_radius for edge in edges]
            assert 3 == [r >= 0 for r in birth_radii].count(True)
            assert 3 == [r < 0 for r in birth_radii].count(True)

    class Test_facets(object):
        def test_case_tetrahedron(self, tetrahedron):
            facets = AlphaShape3(tetrahedron, False, False).facets()
            assert len(facets) == 4
            facets_indices = []
            for facet in facets:
                vertices = sorted([vertex.vertex_index for vertex in facet.vertices()])
                facets_indices.append(vertices)
            assert sorted(facets_indices) == [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

            birth_radii = [facet.birth_radius for facet in facets]
            assert any(abs(19.6 - radius) < 0.000001 for radius in birth_radii)

        def test_case_octahederon(self, trigonal_dipyramid):
            assert len(AlphaShape3(trigonal_dipyramid, False, False).facets()) == 7

    def test_cannot_create_Vertex_Edge_Facet_Cell_by_constructor(self):
        with pytest.raises(TypeError):
            alpha_shape3.Vertex()
        with pytest.raises(TypeError):
            alpha_shape3.Edge()
        with pytest.raises(TypeError):
            alpha_shape3.Facet()
        with pytest.raises(TypeError):
            alpha_shape3.Cell()

    def test_subsets(self, trigonal_dipyramid_with_groupname):
        key = AlphaShape3.simplex_key

        subsets = AlphaShape3(trigonal_dipyramid_with_groupname, False, True).subsets()
        assert set(subsets.keys()) == set([0, 1])

        assert subsets[0].group_name == 0
        assert set(key(s) for s in subsets[0].simplices) == set(
            [
                (0,),
                (1,),
                (2,),
                (3,),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 2),
                (1, 3),
                (2, 3),
                (0, 1, 2),
                (0, 1, 3),
                (0, 2, 3),
                (1, 2, 3),
                (0, 1, 2, 3),
            ]
        )
        assert subsets[0].dim == 3

        assert subsets[1].group_name == 1
        assert set(key(s) for s in subsets[1].simplices) == set([(4,)])
        assert subsets[1].dim == 3
        for subset in subsets.values():
            assert subset.isacyclic()

    def test_check_subsets_acyclicity(self, trigonal_dipyramid_with_groupname):
        AlphaShape3(trigonal_dipyramid_with_groupname, False, True).check_subsets_acyclicity()


class TestCell_Facet_Edge(object):
    class Test_birth_radius:
        def test_case_regular_tetrahedron(self):
            points = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0.5, math.sqrt(3) / 2, 0],
                    [0.5, math.sqrt(3) / 6, math.sqrt(2.0 / 3.0)],
                ]
            )
            alpha_shape = AlphaShape3(points, False, False)
            cell = alpha_shape.cells()[0]
            # 3 / 8 is the square of the circumradius
            assert cell.birth_radius == pytest.approx(3.0 / 8.0)

            # 1 / 3  is the square of the circumradius of a regular triangle
            for facet in alpha_shape.facets():
                assert facet.birth_radius == pytest.approx(1.0 / 3.0)

            # 1 / 4  is the square of the half of an edge
            for edge in alpha_shape.edges():
                assert edge.birth_radius == pytest.approx(1.0 / 4.0)

        def test_case_ortho_tetrahedron(self):
            points = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0.5, math.sqrt(3) / 2, 0],
                    [0.5, math.sqrt(3) / 6, math.sqrt(3.0) / 3],
                ]
            )
            alpha_shape = AlphaShape3(points, False, False)
            cell = alpha_shape.cells()[0]
            # 1 / 3 is the square of the circumradius
            assert cell.birth_radius == pytest.approx(1.0 / 3.0)
            # 1 / 3 is the square of the circumradius of a regular triangle, and
            # r = 4 / 15 is the square of the circumradius of the three triangles
            r = 4.0 / 15.0
            assert np.allclose(sorted([facet.birth_radius for facet in alpha_shape.facets()]), [r, r, r, 1 / 3])
            # 1 / 4 is the square of the half of the longer edges
            # r1 = 1 / 6 is the square of the half of the shorter edges
            r1 = 1.0 / 6.0
            assert np.allclose(
                sorted([edge.birth_radius for edge in alpha_shape.edges()]), [r1, r1, r1, 0.25, 0.25, 0.25]
            )

        def test_case_obcute_tetrahedron(self):
            points = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0.5, math.sqrt(3) / 2, 0],
                    [0.5, math.sqrt(3) / 6, math.sqrt(3.0) / 4],
                ]
            )
            alpha_shape = AlphaShape3(points, False, False)
            # r0 is the square of the circumradius
            r0 = (49.0 + 24**2) / (3 * 24**2)
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(r0)
            # r1 is the square of the circumradius of three triangles
            r1 = (25**2 * 12) / (48**2 * 13)
            assert np.allclose(sorted([facet.birth_radius for facet in alpha_shape.facets()]), [r1, r1, r1, r0])
            r2 = 25 / (48 * 4)
            assert np.allclose(
                sorted([edge.birth_radius for edge in alpha_shape.edges()]),
                [r2, r2, r2, 0.25, 0.25, 0.25],
            )

        def test_case_obcute_obcute_tetrahedron(self):
            points = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0.5, math.sqrt(3) / 2, 0],
                    [0.5, math.sqrt(3) / 6, math.sqrt(3.0) / 9],
                ]
            )
            alpha_shape = AlphaShape3(points, False, False)
            # r0 is the square of the circumradius
            r0 = 25 / 27
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(r0)
            # r1 is the square of the circumradius of three triangles
            r1 = 10**2 / (27 * 13)
            assert np.allclose(sorted([facet.birth_radius for facet in alpha_shape.facets()]), [r1, r1, r1, r0])
            # r2 is the square of the half of the shorter edges
            r2 = 10 / (27 * 4)
            assert np.allclose(
                sorted([edge.birth_radius for edge in alpha_shape.edges()]),
                [r2, r2, r2, r1, r1, r1],
            )

        def test_case_two_obcute_triangles_tetrahedron(self):
            a = 0.05
            b = 0.1
            points = np.array(
                [
                    [0, 0, 0],
                    [1, 0, 0],
                    [0.5, a, b],
                    [0.5, a, -b],
                ]
            )
            alpha_shape = AlphaShape3(points, False, False)
            r0 = ((a**2 + b**2 - 0.25) / (2 * a)) ** 2 + 0.25
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(r0)
            r1 = (a**2 + b**2 + 0.25) ** 2 / (4 * a**2 + 1)
            assert np.allclose(
                sorted([facet.birth_radius for facet in alpha_shape.facets()]),
                [r1, r1, r0, r0],
            )
            e1 = (a**2 + b**2 + 0.25) / 4
            e2 = b**2
            assert np.allclose(
                sorted([edge.birth_radius for edge in alpha_shape.edges()]),
                [e2, e1, e1, e1, e1, r0],
            )

        def test_case_weighted_tetrahedron(self):
            w0 = 0.01
            w1 = 0.3
            w2 = 0.39
            w3 = 0.21
            points = np.array(
                [
                    [-0.12, -0.23, -0.19, w0],
                    [1, 0, 0, w1],
                    [0, 1, 0, w2],
                    [0, 0, 1, w3],
                ]
            )
            alpha_shape = AlphaShape3(points, True, False)
            _, alpha_tetrahedron = self.power_k_sphere(points)
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(alpha_tetrahedron)

            assert np.allclose(
                sorted([facet.birth_radius for facet in alpha_shape.facets()]),
                sorted([self.power_k_sphere(np.vstack([points[:k, :], points[k + 1 :, :]]))[1] for k in range(4)]),
            )
            assert np.allclose(
                sorted([edge.birth_radius for edge in alpha_shape.edges()]),
                sorted(
                    [
                        self.power_k_sphere(np.vstack([points[j, :], points[k, :]]))[1]
                        for k in range(4)
                        for j in range(k)
                    ]
                ),
            )

        @staticmethod
        def power_k_sphere(weighted_points):
            p0 = weighted_points[0, 0:3]
            p = weighted_points[1:, 0:3]
            w = weighted_points[:, 3]
            beta = np.linalg.norm(p, axis=1) ** 2 - np.vdot(p0, p0) + w[0] - w[1:]
            P = p - p0
            l = np.linalg.solve(2 * np.dot(P, np.transpose(P)), beta - 2 * np.dot(P, p0))  # noqa: E741
            pl = np.dot(np.transpose(P), l)
            return p0 + pl, np.linalg.norm(pl) ** 2 - w[0]

        def test_case_weighted_obcute_tetrahedron(self):
            w0 = 0.3
            w1 = 0.12
            w2 = 0.09
            w3 = 0.2
            points = np.array(
                [
                    [0, 0, 0, w0],
                    [1, 0, 0, w1],
                    [0, 1, 0, w2],
                    [0, 0, 1, w3],
                ]
            )
            alpha_shape = AlphaShape3(points, True, False)
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(
                0.25 * (3 * w0**2 + (w1**2 + w2**2 + w3**2) - 2 * (w0 + 1) * (w1 + w2 + w3) + 3 + 2 * w0)
            )
            _, alpha_tetrahedron = self.power_k_sphere(points)
            assert alpha_shape.cells()[0].birth_radius == pytest.approx(alpha_tetrahedron)

            alpha_facets = np.sort(
                [self.power_k_sphere(np.vstack([points[:k, :], points[k + 1 :,]]))[1] for k in range(4)]
            )
            alpha_facets[3] = alpha_tetrahedron
            assert np.allclose(np.sort([facet.birth_radius for facet in alpha_shape.facets()]), alpha_facets)
            alpha_edges = np.sort(
                [self.power_k_sphere(np.vstack([points[j, :], points[k, :]]))[1] for k in range(4) for j in range(k)]
            )
            alpha_edges[3:] = alpha_facets[0:3]
            assert np.allclose(sorted([edge.birth_radius for edge in alpha_shape.edges()]), alpha_edges)
