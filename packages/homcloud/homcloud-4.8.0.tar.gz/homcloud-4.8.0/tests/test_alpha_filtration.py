# pylint: disable=C0111, R0201, W0621, R0903, C0103
import os
import io

import pytest
import numpy as np
import numpy.testing as npt
import msgpack

from homcloud.alpha_filtration import Simplex, AlphaShape, AlphaShape3, AlphaShape2
from homcloud.pdgm_format import PDGMReader


class TestSimplex(object):
    def test_key(self, alpha_tetrahedron):
        assert set([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]) == set(
            Simplex(v, 0).key for v in alpha_tetrahedron.facets()
        )
        assert set((n,) for n in range(0, 4)) == set(Simplex(v, 0).key for v in alpha_tetrahedron.vertices())
        for vertex in alpha_tetrahedron.vertices():
            assert Simplex(vertex, 0).boundary_keys() == []

    class Test_boundary_keys(object):
        def test_case_tetrahedron(self, alpha_tetrahedron):
            facets = [Simplex(f, 0) for f in alpha_tetrahedron.facets()]
            facet_013 = next(f for f in facets if f.key == (0, 1, 3))
            assert set([(0, 1), (1, 3), (0, 3)]) == set(facet_013.boundary_keys())
            assert Simplex(alpha_tetrahedron.vertices()[0], 0).boundary_keys() == []

        def test_case_obtuse_triangle(self, alpha_obtuse_triangle):
            face = Simplex(alpha_obtuse_triangle.faces()[0], 0)
            assert set([(0, 1), (1, 2), (0, 2)]) == set(face.boundary_keys())
            assert Simplex(alpha_obtuse_triangle.vertices()[0], 0).boundary_keys() == []

    class Test_signed_boundary_keys(object):
        def test_case_tetrahedron(self, alpha_tetrahedron):
            facets = [Simplex(f, 0) for f in alpha_tetrahedron.facets()]
            facet_013 = next(f for f in facets if f.key == (0, 1, 3))
            assert set([(1, (0, 1)), (1, (1, 3)), (-1, (0, 3))]) == set(facet_013.signed_boundary_keys())
            assert Simplex(alpha_tetrahedron.vertices()[0], 0).signed_boundary_keys() == []

        def test_case_obtuse_triangle(self, alpha_obtuse_triangle):
            face = Simplex(alpha_obtuse_triangle.faces()[0], 0)
            assert set([(1, (0, 1)), (1, (1, 2)), (-1, (0, 2))]) == set(face.signed_boundary_keys())
            assert Simplex(alpha_obtuse_triangle.vertices()[0], 0).signed_boundary_keys() == []

    def test_birth_radius(self, alpha_tetrahedron):
        npt.assert_allclose(21.06944444444444, Simplex(alpha_tetrahedron.cells()[0], 0).birth_radius)

    def test_dim(self, alpha_tetrahedron):
        assert Simplex(alpha_tetrahedron.vertices()[0], 0).dim == 0
        assert Simplex(alpha_tetrahedron.edges()[0], 1).dim == 1
        assert Simplex(alpha_tetrahedron.facets()[0], 2).dim == 2
        assert Simplex(alpha_tetrahedron.cells()[0], 3).dim == 3


class TestAlphaShape(object):
    def test_build(self, tetragon):
        with pytest.raises(ValueError) as excinfo:
            AlphaShape.build(tetragon, 4)
        assert str(excinfo.value) == "dimension of a point cloud must be 2 or 3"

    class Test_create_filtration(object):
        def test_case_tetrahedron(self, tetrahedron):
            filtration = AlphaShape3(tetrahedron, False, False).create_filtration()
            simplices = filtration.simplices
            dict_simplices = filtration.dict_simplices
            assert len(simplices) == 1 + 4 + 6 + 4
            assert len(dict_simplices) == 1 + 4 + 6 + 4
            assert isinstance(simplices, list)
            assert isinstance(dict_simplices, dict)
            assert list(range(0, 15)) == [s.index for s in simplices]
            for s1, s2 in pairwise(simplices):
                assert s1.birth_radius <= s2.birth_radius
            for i in range(4):
                assert simplices[i].birth_radius == 0.0

        def test_case_tetragon(self, tetragon):
            filtration = AlphaShape2(tetragon, False, False).create_filtration()
            assert len(filtration.simplices) == 2 + 5 + 4
            assert len(filtration.dict_simplices) == 2 + 5 + 4

        def test_case_acute_triangle(self, acute_triangle):
            filtration = AlphaShape2(acute_triangle, False, False).create_filtration()
            assert np.allclose(
                [0.0, 0.0, 0.0, 0.5**2, 1.04 / 4, 1.64 / 4, 0.4264], [s.birth_radius for s in filtration.simplices]
            )

        def test_case_acute_triangle_no_square(self, acute_triangle):
            from math import sqrt

            filtration = AlphaShape2(acute_triangle, False, False).create_filtration(False)
            assert np.allclose(
                [0.0, 0.0, 0.0, 0.5, sqrt(1.04) / 2, sqrt(1.64) / 2, 0.6529931],
                [s.birth_radius for s in filtration.simplices],
            )


class TestAlphaFiltration(object):
    @pytest.fixture
    def points(self):
        return np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]])

    def test_write_dipha_complex(self, tetrahedron, tmpdir):
        complexpath = str(tmpdir.join("tmp.complex"))
        filtration = AlphaShape3(tetrahedron, False, False).create_filtration()

        with open(complexpath, "wb") as f:
            filtration.write_dipha_complex(f)
        assert os.path.getsize(complexpath) == 632

    class Test_isacyclic(object):
        def test_for_filled_tetrahedron(self, tetrahedron):
            filtration = AlphaShape3(tetrahedron, False, False).create_filtration()
            assert filtration.isacyclic()

        def test_for_tetrahedron_boundary(self, tetrahedron):
            filtration = AlphaShape3(tetrahedron, False, False).create_filtration()
            interior = filtration.dict_simplices[(0, 1, 2, 3)]
            filtration.simplices.remove(interior)
            del filtration.dict_simplices[(0, 1, 2, 3)]
            assert not filtration.isacyclic()

    def test_build_phat_matrix(self, alpha_tetrahedron):
        filt = alpha_tetrahedron.create_filtration(True, None, True)
        matrix = filt.build_phat_matrix()
        bmap = msgpack.unpackb(matrix.boundary_map_byte_sequence(), raw=False)
        assert bmap == {
            "chunktype": "boundary_map",
            "type": "simplicial",
            "map": [
                [0, []],
                [0, []],
                [0, []],
                [0, []],
                [1, [1, 0]],
                [1, [3, 1]],
                [1, [3, 0]],
                [1, [3, 2]],
                [1, [1, 2]],
                [1, [0, 2]],
                [2, [5, 6, 4]],
                [2, [5, 7, 8]],
                [2, [4, 8, 9]],
                [2, [6, 7, 9]],
                [3, [10, 11, 13, 12]],
            ],
        }

    @pytest.mark.parametrize(
        "algorithm, save_bm, save_phtrees",
        [
            ("phat-twist", False, False),
            ("phat-twist", True, False),
            ("phat-twist", True, True),
            (None, False, False),
            (None, True, False),
            (None, True, True),
            pytest.param("dipha", False, False, marks=pytest.mark.dipha),
        ],
    )
    def test_compute_pdgm(self, tetrahedron, alpha_tetrahedron, algorithm, save_bm, save_phtrees):
        filt = alpha_tetrahedron.create_filtration(True, ["X", "Y", "Z", "U"], save_bm, save_phtrees)
        f = io.BytesIO()
        filt.compute_pdgm(f, algorithm)
        f.seek(0)
        reader = PDGMReader(f)
        assert reader.metadata["dim"] == 3
        assert reader.metadata["filtration_type"] == "alpha"
        births, deaths, ess_births = reader.load_pd_chunk("pd", 0)
        assert births == [0, 0, 0]
        assert sorted(deaths) == [11.25, 13.25, 14.0]
        assert ess_births == [0]
        births, deaths, ess_births = reader.load_pd_chunk("pd", 1)
        assert births == [14.0, 15.25, 16.0]
        assert len(deaths) == 3
        assert ess_births == []
        births, deaths, ess_births = reader.load_pd_chunk("pd", 2)
        assert births == [19.600000000000005]
        assert deaths == [21.069444444444443]
        assert ess_births == []

        births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 0)
        assert sorted(births) == [1, 2, 3]
        assert sorted(deaths) == [4, 5, 7]
        assert ess_births == [0]
        births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 1)
        assert sorted(births) == [6, 8, 9]
        assert sorted(deaths) == [10, 11, 12]
        assert ess_births == []
        births, deaths, ess_births = reader.load_pd_chunk("indexed_pd", 2)
        assert births == [13]
        assert deaths == [14]
        assert ess_births == []

        index_to_level = reader.load_simple_chunk("index_to_level")
        assert len(index_to_level) == 15
        for i in range(15 - 1):
            assert index_to_level[i] <= index_to_level[i + 1]

        assert sorted(reader.load_simple_chunk("allpairs", 0)) == sorted(
            [
                [0, None],
                [1, 4],
                [2, 7],
                [3, 5],
            ]
        )
        assert sorted(reader.load_simple_chunk("allpairs", 1)) == sorted(
            [
                [6, 10],
                [8, 11],
                [9, 12],
            ]
        )
        assert sorted(reader.load_simple_chunk("allpairs", 2)) == sorted([[13, 14]])

        assert reader.load_simple_chunk("vertex_symbols") == ["X", "Y", "Z", "U"]
        assert np.allclose(reader.load_simple_chunk("vertex_coordintes"), tetrahedron)
        assert list(map(len, reader.load_simple_chunk("index_to_simplex"))) == [
            1,
            1,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            4,
        ]
        assert reader.load_chunk("alpha_information") == {
            "chunktype": "alpha_information",
            "num_vertices": 4,
            "periodicity": None,
            "weighted": False,
            "squared": True,
        }

        if save_bm:
            assert reader.load_boundary_map_chunk() == {
                "chunktype": "boundary_map",
                "type": "simplicial",
                "map": [
                    [0, []],
                    [0, []],
                    [0, []],
                    [0, []],
                    [1, [1, 0]],
                    [1, [3, 1]],
                    [1, [3, 0]],
                    [1, [3, 2]],
                    [1, [1, 2]],
                    [1, [0, 2]],
                    [2, [5, 6, 4]],
                    [2, [5, 7, 8]],
                    [2, [4, 8, 9]],
                    [2, [6, 7, 9]],
                    [3, [10, 11, 13, 12]],
                ],
            }
        else:
            assert reader.load_boundary_map_chunk() is None

        if save_phtrees:
            assert reader.load_simple_chunk("phtrees") == [[13, 14, np.inf]]
        else:
            assert reader.load_simple_chunk("phtrees") is None


class SimplexMock(Simplex):
    def __init__(self, index, birth_radius, key):
        self.index = index
        self.birth_radius = birth_radius
        self.true_birth_radius = birth_radius
        self.key = key


@pytest.fixture
def simplices():
    def simplex(index, birth_radius, key):
        return SimplexMock(index, birth_radius, key)

    return [
        simplex(0, 0, (0,)),
        simplex(1, 0, (1,)),
        simplex(2, 0, (2,)),
        simplex(3, 0, (3,)),
        simplex(
            4,
            1,
            (
                0,
                1,
            ),
        ),
        simplex(
            5,
            2,
            (
                1,
                2,
            ),
        ),
        simplex(
            6,
            3,
            (
                0,
                3,
            ),
        ),
        simplex(
            7,
            4,
            (
                0,
                2,
            ),
        ),
        simplex(
            8,
            5,
            (
                0,
                1,
                3,
            ),
        ),
        simplex(
            9,
            6,
            (
                1,
                3,
            ),
        ),
        simplex(
            10,
            7,
            (
                2,
                3,
            ),
        ),
        simplex(
            11,
            8,
            (
                1,
                2,
                3,
            ),
        ),
        simplex(
            12,
            9,
            (
                0,
                1,
                2,
            ),
        ),
        simplex(
            13,
            10,
            (
                0,
                2,
                3,
            ),
        ),
        simplex(
            14,
            11,
            (
                0,
                1,
                2,
                3,
            ),
        ),
    ]


@pytest.fixture
def triangle_and_center():
    points = np.array([[0, 0, 1], [1, 0, 1], [0.48, 0.78, 1], [0.51, 0.31, 0]])
    return AlphaShape2(points, False, True).create_filtration(True, None, False)


@pytest.fixture
def five_points_filtration():
    points = np.array([[0, 0, 0], [1, 0, 0], [0.5, 0.86, 0], [0.51, 0.43, 1], [0.95, 0.5, 1]])
    return AlphaShape2(points, False, True).create_filtration(True, None, False)


@pytest.fixture
def alpha_tetrahedron(tetrahedron):
    return AlphaShape3(tetrahedron, False, False)


@pytest.fixture
def alpha_obtuse_triangle(obtuse_triangle):
    return AlphaShape2(obtuse_triangle, False, False)


def pairwise(lst):
    for i in range(0, len(lst) - 1):
        yield (lst[i], lst[i + 1])
