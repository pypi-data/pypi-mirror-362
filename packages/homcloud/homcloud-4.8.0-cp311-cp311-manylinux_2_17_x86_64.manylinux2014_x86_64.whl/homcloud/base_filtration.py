import math
import re

import numpy as np

import homcloud.dipha as dipha
import homcloud.homccube as homccube


class Filtration(object):
    """Super class of AlphaFiltration, BitmapFiltration and CubicalFiltration"""

    def compute_pdgm_and_save(self, path, algorithm=None, save_suppl_info=True):
        with open(path, "wb") as f:
            self.compute_pdgm(f, algorithm, save_suppl_info)

    def compute_pairs(self, algorithm=None, parallels=1, upper_dim=None, upper_value=None):
        def compute_pairs_by_phat():
            matrix = self.build_phat_matrix()
            matrix.reduce(algorithm)
            return matrix.birth_death_pairs(), matrix.boundary_map_byte_sequence()

        def format_pair(pair):
            d, birth, death = pair
            return (d, int(birth), (None if death == math.inf else int(death)))

        def compute_pairs_by_dipha():
            return [format_pair(pair) for pair in dipha.pairs_from_filtration(self)]

        def compute_pairs_by_homccube():
            return homccube.compute_pd(
                self.index_bitmap.astype(np.int32), self.periodicity, self.parse_homccube_algorithm(algorithm)
            )

        algorithm = algorithm or self.favorite_algorithm()

        if algorithm.startswith("phat-"):
            return compute_pairs_by_phat()
        if algorithm.startswith("dipha"):
            return compute_pairs_by_dipha(), None
        if algorithm.startswith("homccube-"):
            return compute_pairs_by_homccube(), None

        raise NotImplementedError("unknown alogrithm: {}".format(algorithm))

    @staticmethod
    def parse_homccube_algorithm(algorithm):
        return int(re.match(r"homccube-(\d+)", algorithm).group(1))
