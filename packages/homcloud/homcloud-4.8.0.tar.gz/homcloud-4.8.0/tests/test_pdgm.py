import os
import io

import pytest
import numpy as np

from homcloud.pdgm_format import PDGMReader
from homcloud.pdgm import PDGM, FileType
from homcloud.histogram import PDHistogram, Ruler
from homcloud.abstract_filtration import AbstractFiltration
from homcloud.bitmap import Bitmap
from homcloud.rips import DistanceMatrix
from .test_abstract_filtration import CODE2


@pytest.fixture
def tetrahedron_path(datadir):
    return os.path.join(datadir, "tetrahedron.pdgm")


@pytest.fixture
def tetrahedron_format_ver1_path(datadir):
    return os.path.join(datadir, "tetrahedron_format_ver1.pdgm")


@pytest.fixture
def tetrahedron_reader(request, tetrahedron_path):
    reader = PDGMReader.open(tetrahedron_path)
    request.addfinalizer(reader.close)
    return reader


class TestFileType(object):
    @pytest.mark.parametrize(
        "path, typestr, expected",
        [
            ("foo.txt", "pdgm", FileType.PDGM),
            ("foo.pdgm", "text", FileType.TEXT),
            ("test-diagram.txt", None, FileType.TEXT),
            ("tetrahedron.pdgm", None, FileType.PDGM),
            ("bin.png", None, FileType.UNKNOWN),
        ],
    )
    def test_estimate(self, datadir, path, typestr, expected):
        assert FileType.estimate(os.path.join(datadir, path), typestr) == expected


class TestPDGM(object):
    @pytest.mark.parametrize(
        "degree, expected",
        [
            (0, [0, 0, 0]),
            (1, [14, 15.25, 16]),
            (2, [19.6]),
        ],
    )
    def test_births(self, tetrahedron_reader, degree, expected):
        pdgm = PDGM(tetrahedron_reader, degree)
        assert np.allclose(pdgm.births, expected)

    @pytest.mark.parametrize(
        "degree, expected",
        [
            (0, [11.25, 13.25, 14.0]),
            (1, [17.175925925925927, 18.922240802675585, 19.0625]),
            (2, [21.0695]),
        ],
    )
    def test_deaths(self, tetrahedron_reader, degree, expected):
        pdgm = PDGM(tetrahedron_reader, degree)
        assert np.allclose(pdgm.deaths, expected)

    @pytest.mark.parametrize("degree, expected", [(0, [0]), (1, []), (2, [])])
    def test_essential_births(self, tetrahedron_reader, degree, expected):
        pdgm = PDGM(tetrahedron_reader, degree)
        assert len(pdgm.essential_births) == len(expected)
        assert np.allclose(pdgm.essential_births, expected)

    def test_birth_indices(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 2)
        assert np.allclose(pdgm.birth_indices, [13])

    def test_death_indices(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 2)
        assert np.allclose(pdgm.death_indices, [14])

    def test_essential_birth_indices(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 0)
        assert np.allclose(pdgm.essential_birth_indices, [0])

    def test_sign_flipped(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 0)
        assert not pdgm.sign_flipped

    @pytest.mark.parametrize(
        "array, expected",
        [
            (np.array([[1]], dtype=float), [[0]]),
            (np.array([[3, 4, 0], [2, -1, -3]], dtype=float), [[4, 5, 2], [3, 1, 0]]),
        ],
    )
    def test_index_bitmap(self, tmpdir, array, expected):
        path = str(tmpdir.join("bitmap.pdgm"))
        with open(path, "wb") as f:
            bitmap = Bitmap(array, save_boundary_map=True)
            bitmap.build_bitmap_filtration().compute_pdgm(f)
        pdgm = PDGM(PDGMReader.open(path), 0)
        assert np.allclose(pdgm.indexed_bitmap, expected)

    def test_minmax_of_birthdeath_time(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 1)
        assert pdgm.minmax_of_birthdeath_time() == (14.0, 19.0625)

    @pytest.mark.parametrize(
        "args, expected",
        [
            ((13, 15.5, 16, 20), 2),
            ((13, 15.5, 20, 16), 2),
            ((15.5, 13, 20, 16), 2),
            ((13, 17, 16, 20), 3),
            ((17, 13, 20, 16), 3),
        ],
    )
    def test_count_pairs_in_rectangle(self, tetrahedron_reader, args, expected):
        pdgm = PDGM(tetrahedron_reader, 1)
        assert pdgm.count_pairs_in_rectangle(*args) == expected

    @pytest.mark.parametrize("degree", [0, 1, 2, 3])
    def test_degree(self, tetrahedron_reader, degree):
        pdgm = PDGM(tetrahedron_reader, degree)
        assert pdgm.degree == degree

    def test_path(self, tetrahedron_reader, tetrahedron_path):
        pdgm = PDGM(tetrahedron_reader, 0)
        assert pdgm.path == tetrahedron_path

    def test_input_dim(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 0)
        assert pdgm.input_dim == 3

    def test_alpha_coord_resolver(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 0)
        resolver = pdgm.alpha_coord_resolver
        assert isinstance(resolver.vertices, list)
        assert np.array(resolver.vertices).shape == (4, 3)

    def test_alpha_symbol_resolver(self, tetrahedron_reader):
        pdgm = PDGM(tetrahedron_reader, 0)
        resolver = pdgm.alpha_symbol_resolver
        assert resolver.vertices == ["0", "1", "2", "3"]

    def test_abstract_resolver(self, tmpdir):
        path = str(tmpdir.join("foo.pdgm"))
        with open(path, "wb") as f:
            AbstractFiltration.load(io.StringIO(CODE2), True).compute_pdgm(f)
        pdgm = PDGM(PDGMReader.open(path), 0)
        resolver = pdgm.abstract_geometry_resolver
        assert resolver.index_to_symbol == ["v0", "v1", "e0"]

    def test_cubical_resolver(self, tmpdir):
        path = str(tmpdir.join("foo.pdgm"))
        with open(path, "wb") as f:
            bitmap = Bitmap(np.random.uniform(size=(3, 7)), save_boundary_map=True)
            bitmap.build_cubical_filtration().compute_pdgm(f)
        pdgm = PDGM(PDGMReader.open(path), 0)
        resolver = pdgm.cubical_geometry_resolver
        assert resolver.shape == [3, 7]
        assert resolver.index_to_cube

    class Test_get_geometry_resolver:
        @pytest.mark.parametrize("type", ["default", "coordinates"])
        def test_alpha_coord(self, tetrahedron_reader, type):
            pdgm = PDGM(tetrahedron_reader, 1)
            resolver = pdgm.get_geometry_resolver(type)
            assert np.array(resolver.vertices).shape == (4, 3)

        def test_alpha_symbol(self, tetrahedron_reader):
            pdgm = PDGM(tetrahedron_reader, 1)
            resolver = pdgm.get_geometry_resolver("symbols")
            assert resolver.vertices == ["0", "1", "2", "3"]

        @pytest.mark.parametrize("type", ["vindexes", "vertex_indexes"])
        def test_alpha_vindex(self, tetrahedron_reader, type):
            pdgm = PDGM(tetrahedron_reader, 1)
            resolver = pdgm.get_geometry_resolver(type)
            assert resolver.vertices == [0, 1, 2, 3]

    @pytest.mark.parametrize(
        "dmatrix",
        [
            np.array([[0, 1, 1.4], [1, 0, 1.2], [1.4, 1.2, 0]]),
            np.array(
                [
                    [0, 1, 1.4, 1.6],
                    [1, 0, 1.2, 1.3],
                    [1.4, 1.2, 0, 1.1],
                    [1.6, 1.3, 1.1, 0],
                ]
            ),
        ],
    )
    def test_graph_adjacent_matrix(self, dmatrix, tmpdir):
        path = str(tmpdir.join("foo.pdgm"))
        with open(path, "wb") as f:
            DistanceMatrix(dmatrix, 1).build_rips_filtration(True).compute_pdgm(f)
        pdgm = PDGM(PDGMReader.open(path), 1)
        assert np.all(pdgm.graph_adjacent_matrix == dmatrix.astype(np.float32))

    class Test_alpha_weighted(object):
        def test_for_tetrahedron(self, tetrahedron_reader):
            pdgm = PDGM(tetrahedron_reader, 0)
            assert not pdgm.alpha_weighted

        def test_for_tetrahedron_weighted(self, datadir):
            path = os.path.join(datadir, "tetrahedron-with-weight.pdgm")
            with PDGM(PDGMReader.open(path), 0) as pdgm:
                assert pdgm.alpha_weighted

    class Test_pdgm_id:
        def test_format_ver2(self, tetrahedron_reader):
            assert PDGM(tetrahedron_reader, 1).pdgm_id == "d70488ebefd140f6b832f6ccfdfdd884"

        def test_old_file(self, tetrahedron_format_ver1_path):
            with PDGMReader.open(tetrahedron_format_ver1_path) as reader:
                assert PDGM(reader, 1).pdgm_id is None


def test_Ruler_create_xy_rulers(tetrahedron_reader):
    pdgm = PDGM(tetrahedron_reader, 1)
    x_ruler, y_ruler = Ruler.create_xy_rulers(None, 64, None, None, pdgm)
    assert x_ruler.min() == 14
    assert x_ruler.max() == 19.0625
    assert x_ruler.bins == 64
    assert y_ruler.min() == 14
    assert y_ruler.max() == 19.0625
    assert y_ruler.bins == 64


def test_Histogram(tetrahedron_reader):
    pdgm = PDGM(tetrahedron_reader, 1)
    hist = PDHistogram(pdgm, Ruler((14, 20), 64), Ruler((14, 20), 64))
    assert np.sum(hist.values) == 3
