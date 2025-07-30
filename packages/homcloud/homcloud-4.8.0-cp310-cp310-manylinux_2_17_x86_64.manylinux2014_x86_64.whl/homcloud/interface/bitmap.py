import numpy as np


def volume_range(volume):
    return np.min(volume, axis=0), np.max(volume, axis=0) + 1


def volrange_to_slices(range):
    return tuple(slice(b, e) for (b, e) in zip(*range))


def volume_to_bitmap(volume, range):
    min, max = range
    shape = max - min
    indices = np.ravel_multi_index(np.transpose(volume) - min[:, np.newaxis], shape)
    arr = np.zeros(shape=shape, dtype=bool)
    np.put(arr, indices, True)
    return arr
