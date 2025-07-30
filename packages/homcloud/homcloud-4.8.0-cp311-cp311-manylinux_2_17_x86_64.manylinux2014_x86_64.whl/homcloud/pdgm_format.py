import msgpack
import math
import struct
from pathlib import Path
import uuid

from cached_property import cached_property
import numpy as np

MAGIC_HEADER = (b"HomCloud .pdgm format" + b"\0" * 24)[0:24]
MAGIC_HEADER_LENGTH = len(MAGIC_HEADER)
HEADER_LENGTH = MAGIC_HEADER_LENGTH + 8
FORMAT_VERSION = 2


class PDChunk(object):
    def __init__(self, chunktype, degree, births, deaths, ess_births):
        self.chunktype = chunktype
        self.degree = degree
        self.births = births
        self.deaths = deaths
        self.ess_births = ess_births

    @cached_property
    def binary(self):
        return msgpack.packb(
            {
                "chunktype": self.chunktype,
                "degree": self.degree,
                "births": self.births,
                "deaths": self.deaths,
                "essential_births": self.ess_births,
            },
            use_bin_type=True,
        )

    def metadata(self, start):
        return {"chunktype": self.chunktype, "degree": self.degree, "start": start, "length": len(self.binary)}


class SimpleChunk(object):
    def __init__(self, chunktype, data):
        self.chunktype = chunktype
        self.data = data

    @cached_property
    def binary(self):
        return msgpack.packb({"chunktype": self.chunktype, "data": self.data}, use_bin_type=True)

    def metadata(self, start):
        return {"chunktype": self.chunktype, "start": start, "length": len(self.binary)}


class BinaryChunk(object):
    def __init__(self, chunktype, binary):
        self.chunktype = chunktype
        self.binary = binary

    def metadata(self, start):
        return {"chunktype": self.chunktype, "start": start, "length": len(self.binary)}


class AllPairsChunk(object):
    def __init__(self, degree, pairs):
        self.degree = degree
        self.pairs = pairs

    @cached_property
    def binary(self):
        return msgpack.packb({"chunktype": "allpairs", "degree": self.degree, "data": self.pairs})

    def metadata(self, start):
        return {"chunktype": "allpairs", "degree": self.degree, "start": start, "length": len(self.binary)}


class SimpleDegreeChunk(object):
    def __init__(self, chunktype, degree, data):
        self.chunktype = chunktype
        self.degree = degree
        self.data = data

    @cached_property
    def binary(self):
        return msgpack.packb({"chunktype": self.chunktype, "degree": self.degree, "data": self.data})

    def metadata(self, start):
        return {"chunktype": self.chunktype, "degree": self.degree, "start": start, "length": len(self.binary)}


class BitmapInformationChunk(object):
    def __init__(self, shape, periodicity):
        self.shape = shape
        self.periodicity = periodicity

    @cached_property
    def binary(self):
        return msgpack.packb(
            {
                "chunktype": "bitmap_information",
                "shape": self.shape,
                "periodicity": self.periodicity,
            }
        )

    def metadata(self, start):
        return {"chunktype": "bitmap_information", "start": start, "length": len(self.binary)}


class AlphaInformationChunk(object):
    def __init__(self, num_vertices, periodicity, weighted, squared):
        self.num_vertices = num_vertices
        self.periodicity = periodicity
        self.weighted = weighted
        self.squared = squared

    @cached_property
    def binary(self):
        return msgpack.packb(
            {
                "chunktype": "alpha_information",
                "num_vertices": self.num_vertices,
                "periodicity": self.periodicity,
                "weighted": self.weighted,
                "squared": self.squared,
            }
        )

    def metadata(self, start):
        return {"chunktype": "alpha_information", "start": start, "length": len(self.binary)}


class RipsInformationChunk(object):
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices

    @cached_property
    def binary(self):
        return msgpack.packb({"chunktype": "rips_information", "num_vertices": self.num_vertices})

    def metadata(self, start):
        return {"chunktype": "rips_information", "start": start, "length": len(self.binary)}


class BoundaryMapChunk(object):
    def __init__(self, type, map):
        self.type = type
        self.map = map

    @cached_property
    def binary(self):
        return msgpack.packb({"chunktype": "boundary_map", "type": self.type, "map": self.map})

    def metadata(self, start):
        return {"chunktype": "boundary_map", "start": start, "length": len(self.binary)}


class GraphWeightsChunk(object):
    def __init__(self, matrix):
        assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
        self.matrix = matrix

    @cached_property
    def binary(self):
        return msgpack.packb(
            {
                "chunktype": "graph_weights",
                "num_vertices": self.num_vertices,
                "weights": self.graph_weights(),
            }
        )

    def graph_weights(self):
        return self.matrix[np.triu_indices(self.num_vertices, 1)].tolist()

    @property
    def num_vertices(self):
        return self.matrix.shape[0]

    def metadata(self, start):
        return {"chunktype": "graph_weights", "start": start, "length": len(self.binary)}


class PDGMWriter(object):
    def __init__(self, out, filtration_type, dim=None, pdgm_id=None):
        self.out = out
        self.filtration_type = filtration_type
        self.sign_flipped = False
        self.dim = dim
        self.chunks = []
        self.pdgm_id = pdgm_id or self.generate_pdgm_id()

    @staticmethod
    def generate_pdgm_id():
        return uuid.uuid4().hex

    def append_chunk(self, chunk):
        self.chunks.append(chunk)

    def extend_chunks(self, chunks):
        self.chunks.extend(chunks)

    def append_simple_chunk(self, chunktype, data, degree=None):
        if degree is None:
            self.chunks.append(SimpleChunk(chunktype, data))
        else:
            self.chunks.append(SimpleDegreeChunk(chunktype, degree, data))

    def write(self):
        self.write_magic_header()
        self.write_metadata()
        self.write_chunks()

    def write_magic_header(self):
        self.out.write(MAGIC_HEADER)

    def write_metadata(self):
        metadata_binary = msgpack.packb(self.metadata(), use_bin_type=True)
        self.out.write(struct.pack("q", len(metadata_binary)))
        self.out.write(metadata_binary)

    def write_chunks(self):
        for chunk in self.chunks:
            self.out.write(chunk.binary)

    def metadata(self):
        return {
            "format_version": FORMAT_VERSION,
            "filtration_type": self.filtration_type,
            "sign_flipped": self.sign_flipped,
            "dim": self.dim,
            "pdgm_id": self.pdgm_id,
            "chunks": self.chunk_metadata_list(),
        }

    def chunk_metadata_list(self):
        start = 0
        metadata_list = []
        for chunk in self.chunks:
            metadata = chunk.metadata(start)
            start += metadata["length"]
            metadata_list.append(metadata)

        return metadata_list

    def save_pairs(self, pairs, index_to_levels, save_index_info=True):
        indexed_pds = [IndexedPD(d, index_to_levels) for d in range(self.dim + 1)]
        for d, birth, death in pairs:
            if d > self.dim:
                continue
            indexed_pds[d].append(birth, death)

        self.chunks.extend(indexed_pd.to_unindexed_chunk() for indexed_pd in indexed_pds)

        if not save_index_info:
            return

        self.chunks.extend(indexed_pd.to_chunk() for indexed_pd in indexed_pds)
        self.chunks.extend(indexed_pd.to_allpairs_chunk() for indexed_pd in indexed_pds)


class IndexedPD(object):
    def __init__(self, degree, index_to_levels):
        self.degree = degree
        self.birth_indices = []
        self.death_indices = []
        self.ess_birth_indices = []
        self.births = []
        self.deaths = []
        self.ess_births = []
        self.pairs = []
        self.index_to_levels = index_to_levels

    def append(self, birth, death):
        self.pairs.append((birth, death))
        birth_level = self.level(birth)
        death_level = self.level(death)

        if birth_level == -math.inf:
            pass
        elif birth_level == death_level:
            pass
        elif death is None or math.isinf(death_level):
            self.ess_birth_indices.append(birth)
            self.ess_births.append(birth_level)
        else:
            self.birth_indices.append(birth)
            self.births.append(birth_level)
            self.death_indices.append(death)
            self.deaths.append(death_level)

    def level(self, index):
        return self.index_to_levels[index] if index is not None else None

    def to_chunk(self):
        return PDChunk("indexed_pd", self.degree, self.birth_indices, self.death_indices, self.ess_birth_indices)

    def to_unindexed_chunk(self):
        return PDChunk("pd", self.degree, self.births, self.deaths, self.ess_births)

    def to_allpairs_chunk(self):
        return AllPairsChunk(self.degree, self.pairs)


class PDGMReader(object):
    def __init__(self, infile, path=None):
        self.infile = infile
        self.path = path
        self.scan_magic_header()
        self.load_metadata()

    @staticmethod
    def open(path):
        return PDGMReader(open(path, "rb"), path)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def scan_magic_header(self):
        if self.infile.read(MAGIC_HEADER_LENGTH) != MAGIC_HEADER:
            raise RuntimeError("HomCloud .pdgm format magic header not found")

    def load_metadata(self):
        (metadata_length,) = struct.unpack("q", self.infile.read(8))
        self.metadata = msgpack.unpackb(self.infile.read(metadata_length), raw=False)
        self.pos_first_chunk = HEADER_LENGTH + metadata_length

    @property
    def filtration_type(self):
        return self.metadata["filtration_type"]

    @property
    def pdgm_id(self):
        return self.metadata.get("pdgm_id")

    def unpack_chunk(self, chunk_metadata):
        return msgpack.unpackb(self.read_chunk_bytes(chunk_metadata), raw=False)

    def read_chunk_bytes(self, chunk_metadata):
        self.infile.seek(self.pos_first_chunk + chunk_metadata["start"])
        return self.infile.read(chunk_metadata["length"])

    def load_pd_chunk(self, chunktype, degree):
        chunk = self.load_chunk(chunktype, degree)
        if chunk:
            return chunk["births"], chunk["deaths"], chunk["essential_births"]
        else:
            return (None, None, None)

    def load_simple_chunk(self, chunktype, degree=None):
        chunk = self.load_chunk(chunktype, degree)
        if chunk:
            return chunk["data"]
        else:
            return None

    def load_boundary_map_chunk(self):
        return self.load_chunk("boundary_map")

    def load_chunk(self, chunktype, degree=None):
        chunk_metadata = self.find_chunk_metadata(chunktype, degree)
        if not chunk_metadata:
            return None
        return self.unpack_chunk(chunk_metadata)

    def load_chunk_bytes(self, chunktype, degree=None):
        chunk_metadata = self.find_chunk_metadata(chunktype, degree)
        if not chunk_metadata:
            return None
        return self.read_chunk_bytes(chunk_metadata)

    def find_chunk_metadata(self, chunktype, degree=None):
        def cond(chunk):
            return (chunk["chunktype"] == chunktype) and ((degree is None) or (chunk["degree"] == degree))

        return next(filter(cond, self.metadata["chunks"]), None)

    def load_bitmap_information_chunk(self):
        chunk = self.load_chunk("bitmap_information")
        if chunk:
            return BitmapInformationChunk(chunk["shape"], chunk["periodicity"])
        else:
            return None

    def close(self):
        self.infile.close()


def ispdgm(path):
    return Path(path).suffix == ".pdgm"
