import collections

import numpy as np

from homcloud.paraview_interface import LinesDrawer


def search(bitmap, birth_level, start):
    ndim = bitmap.ndim
    shape = bitmap.shape
    queue = collections.deque()
    memo = np.full_like(bitmap, None, dtype=object)

    def backward_list(at):
        lst = [at]
        while memo[at]:
            _, next_pos = memo[at]
            lst.append(next_pos)
            at = next_pos
        return lst

    def next_from(at):
        for i in range(ndim):
            for sign in [-1, +1]:
                n = list(at)
                n[i] += sign
                next_pos = tuple(n)
                if next_pos[i] < 0 or next_pos[i] >= shape[i]:
                    continue
                if bitmap[next_pos] < birth_level:
                    yield next_pos

    def step_from(head_name, at):
        for next_pos in next_from(at):
            next_step = memo[next_pos]
            if next_step:
                next_head_name, next_backward = next_step
                if next_head_name == head_name:
                    continue
                else:
                    return list(reversed(backward_list(at))) + backward_list(next_pos)
            else:
                memo[next_pos] = (head_name, at)
                queue.append((head_name, next_pos))

    def initialize():
        for head_name, pos in enumerate(next_from(start)):
            memo[pos] = (head_name, start)
            queue.append((head_name, pos))

    initialize()

    while True:
        if not len(queue):
            return None
        head_name, at = queue.popleft()
        result = step_from(head_name, at)
        if result:
            return result


class Finder(object):
    def __init__(self, pdgm):
        assert pdgm.filtration_type == "bitmap"
        self.pdgm = pdgm

    def query_pair(self, birth, death):
        path = search(self.bitmap, birth, self.start_pixel(birth))
        return Result(self.pdgm.index_to_level[birth], self.pdgm.index_to_level[death], path)

    @property
    def bitmap(self):
        return self.pdgm.indexed_bitmap

    def start_pixel(self, birth):
        return tuple(self.pdgm.index_to_pixel[birth])


class Result(object):
    def __init__(self, birth_time, death_time, path):
        self.birth_time = birth_time
        self.death_time = death_time
        self.path = path

    def to_jsondict(self):
        return {
            "birth-time": self.birth_time,
            "death-time": self.death_time,
            "path": list(map(list, self.path)),
            "boundary-points": list(map(list, self.boundary_points())),
        }

    def boundary_points(self):
        return set(self.path)

    def draw(self, drawer, color, index):
        drawer.draw_loop(self.path, color, index=index)


def prepare_drawer_for_paraview(n_colors):
    return LinesDrawer(n_colors, {"index": None, "isboundary": "1"})
