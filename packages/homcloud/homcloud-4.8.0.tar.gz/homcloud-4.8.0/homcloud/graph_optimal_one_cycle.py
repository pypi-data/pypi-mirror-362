from collections import deque
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def search(adj_matrix, birth, weighted=False):
    if weighted:
        return search_for_weighted_graph(adj_matrix, birth)
    else:
        return Finder(adj_matrix, birth).search()


TERM = -1


def search_starting_edge(matrix, birth):
    xs, ys = np.nonzero(matrix == birth)
    if xs.size == 0:
        raise RuntimeError("Invalid birth time")
    if xs.size > 2:
        raise RuntimeError("Pairs with the same birth time")
    return sorted([int(xs[0]), int(ys[0])])


def path(predecessors, start, end):
    result = [end]
    at = end
    while at != start:
        at = predecessors[at]
        result.append(at)
    return result


def search_for_weighted_graph(adjacent_matrix, birth):
    start, end = search_starting_edge(adjacent_matrix, birth)
    matrix = adjacent_matrix.copy()
    matrix[matrix >= birth] = 0.0
    graph = csr_matrix(matrix)
    dist_matrix, predecessors = dijkstra(graph, False, start, True)
    return path(predecessors, start, end)


def search_with_cocycle(adjacent_matrix, cocycle, birth, torelance, weighted):
    def edge(e):
        v1 = e[0]
        v2 = e[1]
        if v1 < v2:
            return (v1, v2)
        else:
            return (v2, v1)

    cocycle_edges = set(edge(e) for e in cocycle)
    matrix = adjacent_matrix.copy()
    matrix[matrix >= birth + torelance] = 0.0
    for e in cocycle_edges:
        matrix[e[0], e[1]] = 0.0
        matrix[e[1], e[0]] = 0.0
    graph = csr_matrix(matrix)

    # TODO: 最短距離計算を重複して計算しているので，効率化のためには保存しておくとよい
    predecessors = None
    min_loop_length = np.inf
    min_edge = None
    for e in cocycle_edges:
        if birth + torelance < adjacent_matrix[e[0], e[1]]:
            continue
        dist_matrix, another_predecessors = dijkstra(graph, False, e[0], True, not weighted)
        loop_length = dist_matrix[e[1]] + adjacent_matrix[e[0], e[1]]
        if min_loop_length > loop_length:
            min_loop_length = loop_length
            predecessors = another_predecessors
            min_edge = e
    return path(predecessors, min_edge[0], min_edge[1])


class Finder(object):
    def __init__(self, adjacent_matrix, birth):
        self.matrix = adjacent_matrix
        self.birth = birth
        self.visited = set()
        self.prev = dict()

    def search(self):
        start, end = search_starting_edge(self.matrix, self.birth)
        g = self.matrix < self.birth
        queue = deque([start])
        self.visited.add(start)
        self.prev[start] = TERM

        while queue:
            v = queue.popleft()
            if v == end:
                return self.path(end)
            for n in range(self.num_points):
                if not g[n, v]:
                    continue
                if n in self.visited:
                    continue

                self.visited.add(n)
                self.prev[n] = v
                queue.append(n)

        raise RuntimeError("No loop containing birth")

    def path(self, end):
        v = end
        path = []
        while True:
            path.append(v)
            v = self.prev[v]
            if v == TERM:
                return path

    @property
    def num_points(self):
        return self.matrix.shape[0]
