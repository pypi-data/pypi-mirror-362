import math

import pytest
import numpy as np

from homcloud.pdgm_format import IndexedPD, GraphWeightsChunk

INDEX_TO_LEVELS = [-math.inf, -math.inf, 0.0, 1.0, 1.0, 2.0, math.inf, math.inf]


class TestIndexedPD(object):
    @pytest.mark.parametrize(
        "pair, expected_births, expected_birth_indices,"
        "expected_deaths, expected_death_indices,"
        "expected_ess_births, expected_ess_birth_indices",
        [
            ((2, 3), [0.0], [2], [1.0], [3], [], []),
            ((3, 4), [], [], [], [], [], []),  # birth == death != inf
            ((0, None), [], [], [], [], [], []),
            ((0, 6), [], [], [], [], [], []),  # birth == -inf, death == inf
            ((3, None), [], [], [], [], [1.0], [3]),
            ((3, 6), [], [], [], [], [1.0], [3]),  # deah == inf
            ((6, 7), [], [], [], [], [], []),  # birth == death == inf
        ],
    )
    def test_append(
        self,
        pair,
        expected_births,
        expected_birth_indices,
        expected_deaths,
        expected_death_indices,
        expected_ess_births,
        expected_ess_birth_indices,
    ):
        indexed_pd = IndexedPD(1, INDEX_TO_LEVELS)
        indexed_pd.append(*pair)
        assert indexed_pd.pairs == [pair]
        assert indexed_pd.births == expected_births
        assert indexed_pd.deaths == expected_deaths
        assert indexed_pd.ess_births == expected_ess_births
        assert indexed_pd.birth_indices == expected_birth_indices
        assert indexed_pd.death_indices == expected_death_indices
        assert indexed_pd.ess_birth_indices == expected_ess_birth_indices


class TestGraphWeightsChunk(object):
    def test_graph_weights(self):
        dmatrix = np.array(
            [
                [0, 1, 1.2],
                [1, 0, 1.4],
                [1.2, 1.4, 0],
            ]
        )
        assert GraphWeightsChunk(dmatrix).graph_weights() == [1.0, 1.2, 1.4]
