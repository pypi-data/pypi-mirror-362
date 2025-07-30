import collections
import homcloud.optimal_one_cycle_ext as optimal_one_cycle_ext


def vertices(boundary_map, birth):
    return [index for (index, (dim, boundary)) in enumerate(boundary_map["map"][:birth]) if dim == 0]


def edges(boundary_map, birth):
    return [(index, boundary) for (index, (dim, boundary)) in enumerate(boundary_map["map"][:birth]) if dim == 1]


def adjacent_vertices(boundary_map, birth):
    adjacent_vertices = {vertex: [] for vertex in vertices(boundary_map, birth)}
    for e, (x, y) in edges(boundary_map, birth):
        adjacent_vertices[x].append((e, x, y))
        adjacent_vertices[y].append((e, y, x))

    return adjacent_vertices


def path(visited, start, end):
    v = end
    result = []

    while True:
        (edge, v) = visited[v]
        result.append(edge)
        if v is None:
            return result


def search(boundary_map, birth):
    adjacents = adjacent_vertices(boundary_map, birth)
    start, end = boundary_map["map"][birth][1]

    queue = collections.deque([(birth, None, start)])
    visited = {}

    while True:
        if len(queue) == 0:
            return None

        (e, v, other) = queue.popleft()
        if other in visited:
            continue
        visited[other] = (e, v)
        if other == end:
            return path(visited, start, end)

        queue.extend(adjacents[other])


def search_on_chunk_bytes(boundary_map_chunk_bytes, birth):
    return optimal_one_cycle_ext.search(boundary_map_chunk_bytes, birth)
