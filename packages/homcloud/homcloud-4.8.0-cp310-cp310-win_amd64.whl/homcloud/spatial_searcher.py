import numpy as np


# TODO: Use KDTree or something
class SpatialSearcher(object):
    def __init__(self, pairs, births, deaths):
        self.pairs = pairs
        self.births = births
        self.deaths = deaths

    def nearest_pair(self, birth, death):
        distances = (self.births - birth) ** 2 + (self.deaths - death) ** 2
        return self.pairs[np.argmin(distances)]

    def in_rectangle(self, xmin, xmax, ymin, ymax):
        def is_pair_in_rectangle(birth, death):
            return (xmin <= birth <= xmax) and (ymin <= death <= ymax) and (birth != death)

        return [self.pairs[k] for k in range(len(self.pairs)) if is_pair_in_rectangle(self.births[k], self.deaths[k])]
