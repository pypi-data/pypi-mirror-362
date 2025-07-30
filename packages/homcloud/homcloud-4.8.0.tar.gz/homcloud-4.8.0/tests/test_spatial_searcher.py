import pytest
import numpy as np

from homcloud.spatial_searcher import SpatialSearcher


class TestSpatialSearcher(object):
    @pytest.fixture
    def searcher(self):
        pairs = [(1, 5), (2, 3)]
        births = np.array([11.0, 12.0])
        deaths = np.array([15.0, 13.0])
        return SpatialSearcher(pairs, births, deaths)

    def test_query(self, searcher):
        assert searcher.nearest_pair(11.1, 15.1) == (1, 5)
        assert searcher.nearest_pair(12, 13.5) == (2, 3)
        assert searcher.nearest_pair(11.5, 13.99) == (2, 3)
        assert searcher.nearest_pair(11.5, 14.01) == (1, 5)

    def test_in_rectangle(self, searcher):
        assert sorted(searcher.in_rectangle(10.8, 11.1, 14.8, 15.2)) == [(1, 5)]
        assert sorted(searcher.in_rectangle(10.8, 11.1, 15.2, 15.21)) == []
