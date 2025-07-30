import numpy as np

import homcloud.maximal_0_component as maximal_0_component


class PH0Components(object):
    def __init__(self, pair, epsilon):
        self.pair = pair
        self.graph = maximal_0_component.Graph(pair.diagram.pd, pair.birth_index, pair.death_index, epsilon)

    @property
    def _symbol_resolver(self):
        return self.pair.diagram.pd.alpha_symbol_resolver

    @property
    def _coord_resolver(self):
        return self.pair.diagram.pd.alpha_coord_resolver

    @property
    def birth_component(self):
        return np.array([self._coord_resolver.vertices[i] for i in self.graph.birth_component])

    @property
    def elder_component(self):
        return np.array([self._coord_resolver.vertices[i] for i in self.graph.elder_component])

    @property
    def birth_component_symbols(self):
        return [self._symbol_resolver.vertices[i] for i in self.graph.birth_component]

    @property
    def elder_component_symbols(self):
        return [self._symbol_resolver.vertices[i] for i in self.graph.elder_component]
