import enum
import os

import numpy as np
from cached_property import cached_property

import homcloud.geometry_resolver as geom_resolver
from homcloud.pdgm_format import PDGMReader, MAGIC_HEADER, MAGIC_HEADER_LENGTH


def empty_pd(degree=0, sign_flipped=False):
    empty_array = np.zeros((0,))
    return SimplePDGM(degree, empty_array, empty_array, empty_array, sign_flipped)


class PDGMBase(object):
    def minmax_of_birthdeath_time(self):
        return (min(self.births.min(), self.deaths.min()), max(self.births.max(), self.deaths.max()))

    def count_pairs_in_rectangle(self, birth1, birth2, death1, death2):
        birth_min = min([birth1, birth2])
        birth_max = max([birth1, birth2])
        death_min = min([death1, death2])
        death_max = max([death1, death2])
        return np.sum(
            (self.births >= birth_min)
            & (self.births <= birth_max)
            & (self.deaths >= death_min)
            & (self.deaths <= death_max)
        )

    @property
    def num_pairs(self):
        return len(self.births)


class SimplePDGM(PDGMBase):
    def __init__(self, degree, births, deaths, ess_births=np.array([]), sign_flipped=False):
        self.degree = degree
        self.births = births
        self.deaths = deaths
        self.essential_births = ess_births
        self.sign_flipped = sign_flipped

    @staticmethod
    def load_from_textfile(path, degree=None, sign_flipped=False):
        with open(path) as f:
            return SimplePDGM.load_from_text(f, degree, sign_flipped)

    @staticmethod
    def load_from_text(infile, degree=None, sign_flipped=False):
        """Create a PD object from text file

        Args:
        infile -- io-like object
        """
        births = []
        deaths = []
        essbirths = []
        for line in infile:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            birth, death = line.split()
            if death == "Inf":
                essbirths.append(float(birth))
            elif birth == "-Inf":
                essbirths.append(float(death))
            else:
                births.append(float(birth))
                deaths.append(float(death))

        return SimplePDGM(degree, np.array(births), np.array(deaths), np.array(essbirths), sign_flipped)


class PDGM(PDGMBase):
    def __init__(self, reader, degree, load_indexed_pairs=True):
        self.pdgmreader = reader
        self.degree = degree
        self.load_pd()
        if load_indexed_pairs:
            self.load_indexed_pd()

    def load_pd(self):
        births, deaths, ess_births = self.pdgmreader.load_pd_chunk("pd", self.degree)
        self.births = np.array(births)
        self.deaths = np.array(deaths)
        self.essential_births = np.array(ess_births)

    def load_indexed_pd(self):
        births, deaths, ess_births = self.pdgmreader.load_pd_chunk("indexed_pd", self.degree)
        if births is None:
            return
        self.birth_indices = np.array(births, dtype=int)
        self.death_indices = np.array(deaths, dtype=int)
        self.essential_birth_indices = np.array(ess_births, dtype=int)

    def has_chunk(self, chunktype, degree=None):
        return self.pdgmreader.find_chunk_metadata(chunktype, degree) is not None

    @staticmethod
    def open(path, degree, load_indexed_pairs=True):
        return PDGM(PDGMReader.open(path), degree, load_indexed_pairs)

    def close(self):
        self.pdgmreader.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @property
    def sign_flipped(self):
        return self.pdgmreader.metadata["sign_flipped"]

    @property
    def filtration_type(self):
        return self.pdgmreader.metadata["filtration_type"]

    @property
    def input_dim(self):
        return self.pdgmreader.metadata["dim"]

    @property
    def pdgm_id(self):
        return self.pdgmreader.pdgm_id

    @property
    def death_index_to_pair_number(self):
        return dict(zip(self.death_indices, range(self.num_pairs)))

    @property
    def death_index_to_birth_index(self):
        return dict(zip(self.death_indices, self.birth_indices))

    @cached_property
    def index_to_level(self):
        return self.pdgmreader.load_simple_chunk("index_to_level")

    @cached_property
    def index_to_pixel(self):
        return self.pdgmreader.load_simple_chunk("index_to_pixel")

    @cached_property
    def bitmap_information(self):
        return self.pdgmreader.load_bitmap_information_chunk()

    @cached_property
    def indexed_bitmap(self):
        assert self.filtration_type == "bitmap"
        shape = self.bitmap_information.shape
        bitmap = np.empty(shape, dtype=int)
        for index, pixel in enumerate(self.index_to_pixel):
            bitmap[tuple(pixel)] = index
        return bitmap

    @property
    def index_to_simplex(self):
        return self.pdgmreader.load_simple_chunk("index_to_simplex")

    @cached_property
    def boundary_map_chunk(self):
        return self.pdgmreader.load_boundary_map_chunk()

    def load_boundary_map(self):
        return self.boundary_map_chunk

    @property
    def boundary_map_bytes(self):
        return self.pdgmreader.load_chunk_bytes("boundary_map")

    def default_vertex_symbols(self):
        return [str(k) for k in range(self.num_vertices)]

    @cached_property
    def num_vertices(self):
        if self.filtration_type == "alpha":
            return self.pdgmreader.load_chunk("alpha_information")["num_vertices"]
        if self.filtration_type == "rips":
            return self.pdgmreader.load_chunk("rips_information")["num_vertices"]

    @cached_property
    def simplicial_symbol_resolver(self):
        assert self.filtration_type in ["alpha", "simplicial"]

        return geom_resolver.SimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            self.pdgmreader.load_simple_chunk("vertex_symbols") or self.default_vertex_symbols(),
            self.boundary_map,
        )

    @property
    def alpha_symbol_resolver(self):
        return self.simplicial_symbol_resolver

    @cached_property
    def vertex_index_resolver(self):
        assert self.filtration_type in ["alpha", "simplicial"]

        return geom_resolver.SimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            list(range(self.num_vertices)),
            self.boundary_map,
        )

    @cached_property
    def alpha_coord_resolver(self):
        assert self.filtration_type == "alpha"

        return geom_resolver.SimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            self.pdgmreader.load_simple_chunk("vertex_coordintes"),
            self.boundary_map,
        )

    def periodic_alpha_coord_resolver(self, pbc_ratio):
        assert self.filtration_type == "alpha"
        assert self.alpha_information["periodicity"]

        return geom_resolver.PeriodicSimplicialResolver(
            self.pdgmreader.load_simple_chunk("index_to_simplex"),
            self.pdgmreader.load_simple_chunk("vertex_coordintes"),
            self.boundary_map,
            self.alpha_information["periodicity"],
            pbc_ratio,
        )

    @cached_property
    def cubical_geometry_resolver(self):
        assert self.filtration_type == "cubical"

        return geom_resolver.CubicalResolver(
            self.pdgmreader.load_chunk("bitmap_information")["shape"],
            self.pdgmreader.load_simple_chunk("index_to_cube"),
            self.boundary_map,
        )

    @cached_property
    def bitmap_geometry_resolver(self):
        assert self.filtration_type == "bitmap"

        return geom_resolver.BitmapResolver(self.index_to_pixel)

    @cached_property
    def abstract_geometry_resolver(self):
        assert self.filtration_type == "abstract"

        return geom_resolver.AbstractResolver(self.pdgmreader.load_simple_chunk("index_to_symbol"), self.boundary_map)

    @cached_property
    def rips_geometry_resolver(self):
        assert self.filtration_type == "rips"

        return geom_resolver.RipsResolver(
            self.pdgmreader.load_simple_chunk("vertex_symbols") or self.default_vertex_symbols()
        )

    def get_geometry_resolver(self, resolver_type="default", pbc_ratio=None):
        match (self.filtration_type, resolver_type):
            case ("alpha", "symbols"):
                return self.alpha_symbol_resolver
            case ("alpha", "default" | "coordinates") if pbc_ratio is not None:
                return self.periodic_alpha_coord_resolver(pbc_ratio)
            case ("alpha", "default" | "coordinates"):
                return self.alpha_coord_resolver
            case ("alpha" | "simplicial", "vertex_indexes" | "vindexes"):
                return self.vertex_index_resolver
            case ("simplicial", "default"):
                return self.simplicial_symbol_resolver
            case ("cubical", "default"):
                return self.cubical_geometry_resolver
            case ("bitmap", "default"):
                return self.bitmap_geometry_resolver
            case ("abstract", "default"):
                return self.abstract_geometry_resolver
            case ("rips", "default" | "symbols"):
                return self.rips_geometry_resolver
            case _:
                raise RuntimeError(f"Geometry resolver is unavailable for {self.filtration_type}, {resolver_type}")

    def boundary_map(self, cell_index):
        return self.boundary_map_chunk["map"][cell_index][1]

    @property
    def path(self):
        return self.pdgmreader.path

    @cached_property
    def birth_positions(self):
        return self.get_geometry_resolver().resolve_cells(self.birth_indices)

    @cached_property
    def death_positions(self):
        return self.get_geometry_resolver().resolve_cells(self.death_indices)

    @cached_property
    def essential_birth_positions(self):
        return self.get_geometry_resolver().resolve_cells(self.essential_birth_indices)

    def pairs_positions(self):
        return zip(self.births, self.deaths, self.birth_positions, self.death_positions)

    @cached_property
    def alpha_information(self):
        return self.pdgmreader.load_chunk("alpha_information")

    @property
    def alpha_weighted(self):
        return self.alpha_information["weighted"]

    @property
    def alpha_radii_squared(self):
        return self.alpha_information["squared"]

    @property
    def graph_adjacent_matrix(self):
        chunk = self.pdgmreader.load_chunk("graph_weights")
        if chunk is None:
            return None
        num_vertices = chunk["num_vertices"]
        matrix = np.zeros((num_vertices, num_vertices), dtype=float)
        xs, ys = np.triu_indices(num_vertices, 1)
        matrix[(xs, ys)] = chunk["weights"]
        matrix[(ys, xs)] = chunk["weights"]
        return matrix

    def representative_cocycle(self, d, nth):
        return self.pdgmreader.load_simple_chunk("cocycles", d)[nth]


class FileType(enum.Enum):
    TEXT = 0
    PDGM = 5
    UNKNOWN = -1

    @staticmethod
    def estimate(path, typestr):
        TABLE_TYPESTR = {
            "text": FileType.TEXT,
            "pdgm": FileType.PDGM,
        }
        TABLE_EXTENSION = {
            ".txt": FileType.TEXT,
            ".pdgm": FileType.PDGM,
        }

        def check_file_header(path):
            with open(path, "rb") as f:
                if f.read(MAGIC_HEADER_LENGTH) == MAGIC_HEADER:
                    return FileType.PDGM
                else:
                    return None

        _, ext = os.path.splitext(path)
        return TABLE_TYPESTR.get(typestr) or check_file_header(path) or TABLE_EXTENSION.get(ext) or FileType.UNKNOWN

    def loader(self, degree, sign_flipped):
        if self == FileType.TEXT:
            return lambda path: SimplePDGM.load_from_textfile(path, degree, sign_flipped)
        elif self == FileType.PDGM:
            return lambda path: PDGM.open(path, degree)
        else:
            raise ValueError("Unknown filetype")


def load(path, filetype=None, degree=None, sign_flipped=False):
    filetype = FileType.estimate(path, filetype)
    return filetype.loader(degree, sign_flipped)(path)


def load_merged_diagrams(paths, filetype=None, degree=None, sign_flipped=False):
    def merge_diagrams(diagrams):
        if len(diagrams) == 0:
            return SimplePDGM.empty_pd(degree, sign_flipped)
        births = np.concatenate([pd.births for pd in diagrams])
        deaths = np.concatenate([pd.deaths for pd in diagrams])
        ess_births = np.concatenate([pd.essential_births for pd in diagrams])
        return SimplePDGM(degree, births, deaths, ess_births, sign_flipped)

    filetype = FileType.estimate(paths[0], filetype)
    loader = filetype.loader(degree, sign_flipped)
    diagrams = [loader(path) for path in paths]
    if len(diagrams) == 1:
        return diagrams[0]
    else:
        return merge_diagrams(diagrams)
