import numpy as np
import pytest

from homcloud.cubical_ext import CubicalFiltrationExt, CubeEncoder


class TestCubicalFiltrationExt(object):
    def test_init(self):
        cubical_filtration = CubicalFiltrationExt(np.zeros((2, 3)), [False] * 2, False)
        assert cubical_filtration.required_bits == [2, 3]

    def test_encode_cube_and_decode_cube(self):
        cubical_filtration = CubicalFiltrationExt(np.zeros((4, 7)), [False] * 2, False)
        assert cubical_filtration.encode_cube((0, 0), (0, 0)) == 0
        assert cubical_filtration.decode_cube(0) == ([0, 0], [0, 0])

        cubeint = cubical_filtration.encode_cube((2, 5), [1, 1])
        assert isinstance(cubeint, int)
        assert cubical_filtration.decode_cube(cubeint) == ([2, 5], [1, 1])

        cubeint = cubical_filtration.encode_cube((2, 5), [1, 0])
        assert isinstance(cubeint, int)
        assert cubical_filtration.decode_cube(cubeint) == ([2, 5], [1, 0])

        cubeint = cubical_filtration.encode_cube((1, 5), [0, 1])
        assert isinstance(cubeint, int)
        assert cubical_filtration.decode_cube(cubeint) == ([1, 5], [0, 1])

    def test_cube_dim(self):
        filt = CubicalFiltrationExt(np.zeros((4, 7)), [False] * 2, False)
        assert filt.cube_dim(filt.encode_cube([3, 6], [0, 0])) == 0
        assert filt.cube_dim(filt.encode_cube([3, 5], [0, 1])) == 1
        assert filt.cube_dim(filt.encode_cube([2, 5], [1, 0])) == 1
        assert filt.cube_dim(filt.encode_cube([2, 5], [1, 1])) == 2

    class Test_boundary(object):
        def test_for_nonperiodic(self):
            filt = CubicalFiltrationExt(np.zeros((4, 7)), [False] * 2, False)
            assert filt.boundary(filt.encode_cube([1, 4], [0, 0])) == ([], [])
            assert filt.boundary(filt.encode_cube([1, 4], [1, 0])) == (
                [filt.encode_cube([2, 4], [0, 0]), filt.encode_cube([1, 4], [0, 0])],
                [1, -1],
            )
            assert filt.boundary(filt.encode_cube([1, 4], [0, 1])) == (
                [filt.encode_cube([1, 5], [0, 0]), filt.encode_cube([1, 4], [0, 0])],
                [1, -1],
            )
            assert filt.boundary(filt.encode_cube([1, 4], [1, 1])) == (
                [
                    filt.encode_cube([2, 4], [0, 1]),
                    filt.encode_cube([1, 4], [0, 1]),
                    filt.encode_cube([1, 5], [1, 0]),
                    filt.encode_cube([1, 4], [1, 0]),
                ],
                [1, -1, -1, 1],
            )

        def test_for_periodic(self):
            filt = CubicalFiltrationExt(np.zeros((4, 7)), [True] * 2, False)
            assert filt.boundary(filt.encode_cube([3, 4], [0, 0])) == ([], [])

            assert filt.boundary(filt.encode_cube([3, 4], [1, 0])) == (
                [filt.encode_cube([0, 4], [0, 0]), filt.encode_cube([3, 4], [0, 0])],
                [1, -1],
            )
            assert filt.boundary(filt.encode_cube([3, 6], [1, 1])) == (
                [
                    filt.encode_cube([0, 6], [0, 1]),
                    filt.encode_cube([3, 6], [0, 1]),
                    filt.encode_cube([3, 0], [1, 0]),
                    filt.encode_cube([3, 6], [1, 0]),
                ],
                [1, -1, -1, 1],
            )

    class Test_value_at(object):
        def test_for_nonperiodic(self):
            filt = CubicalFiltrationExt(np.arange(28).reshape((4, 7)).astype(float), [False] * 2, False)
            assert filt.value_at(filt.encode_cube([0, 0], [0, 0])) == 0
            assert filt.value_at(filt.encode_cube([3, 6], [0, 0])) == 27
            assert filt.value_at(filt.encode_cube([0, 0], [1, 0])) == 7
            assert filt.value_at(filt.encode_cube([0, 0], [0, 1])) == 1
            assert filt.value_at(filt.encode_cube([0, 0], [1, 1])) == 8
            assert filt.value_at(filt.encode_cube([1, 2], [0, 0])) == 9
            assert filt.value_at(filt.encode_cube([1, 2], [1, 0])) == 16
            assert filt.value_at(filt.encode_cube([1, 2], [0, 1])) == 10
            assert filt.value_at(filt.encode_cube([1, 2], [1, 1])) == 17

        def test_for_periodic(self):
            bitmap = np.arange(28, dtype=float).reshape((4, 7))
            bitmap[0, 0] = 30
            filt = CubicalFiltrationExt(bitmap, [True] * 2, False)
            assert filt.value_at(filt.encode_cube([3, 0], [1, 1])) == 30
            assert filt.value_at(filt.encode_cube([3, 1], [1, 1])) == 23
            assert filt.value_at(filt.encode_cube([3, 6], [1, 1])) == 30
            assert filt.value_at(filt.encode_cube([0, 6], [0, 1])) == 30

    class Test_all_cubes(object):
        def test_for_nonperiodic(self):
            filt = CubicalFiltrationExt(np.zeros((2, 3), dtype=float), [False] * 2, False)
            c = filt.encode_cube
            assert sorted(filt.all_cubes()) == sorted(
                [c([x, y], [0, 0]) for x in range(2) for y in range(3)]
                + [c([0, y], [1, 0]) for y in range(3)]
                + [c([x, y], [0, 1]) for x in range(2) for y in range(2)]
                + [c([0, 0], [1, 1]), c([0, 1], [1, 1])]
            )

        def test_for_periodic_one_direction(self):
            filt = CubicalFiltrationExt(np.zeros((2, 3), dtype=float), [False, True], False)
            c = filt.encode_cube
            assert sorted(filt.all_cubes()) == sorted(
                [c([x, y], [0, 0]) for x in range(2) for y in range(3)]
                + [c([0, y], [1, 0]) for y in range(3)]
                + [c([x, y], [0, 1]) for x in range(2) for y in range(3)]
                + [c([0, 0], [1, 1]), c([0, 1], [1, 1]), c([0, 2], [1, 1])]
            )

        def test_for_periodic_two_direction(self):
            filt = CubicalFiltrationExt(np.zeros((2, 3), dtype=float), [True, True], False)
            c = filt.encode_cube
            assert sorted(filt.all_cubes()) == sorted(
                [c([x, y], [0, 0]) for x in range(2) for y in range(3)]
                + [c([x, y], [1, 0]) for x in range(2) for y in range(3)]
                + [c([x, y], [0, 1]) for x in range(2) for y in range(3)]
                + [c([x, y], [1, 1]) for x in range(2) for y in range(3)]
            )

        def test_with_inf_cubes(self):
            ary = np.array(
                [
                    [0, 1, np.inf],
                    [3, 72, 0],
                ],
                dtype=float,
            )
            filt = CubicalFiltrationExt(ary, [False, False], False)
            c = filt.encode_cube
            assert sorted(filt.all_cubes()) == sorted(
                [
                    c([0, 0], [0, 0]),
                    c([0, 1], [0, 0]),
                    c([1, 0], [0, 0]),
                    c([1, 1], [0, 0]),
                    c([1, 2], [0, 0]),
                    c([0, 0], [0, 1]),
                    c([1, 0], [0, 1]),
                    c([1, 1], [0, 1]),
                    c([0, 0], [1, 0]),
                    c([0, 1], [1, 0]),
                    c([0, 0], [1, 1]),
                ]
            )


class TestCubeEncoder(object):
    def test_cube_dim(self):
        encoder = CubeEncoder([4, 7])
        assert encoder.cube_dim(encoder.encode_cube([3, 6], [0, 0])) == 0
        assert encoder.cube_dim(encoder.encode_cube([3, 5], [0, 1])) == 1
        assert encoder.cube_dim(encoder.encode_cube([2, 5], [1, 0])) == 1
        assert encoder.cube_dim(encoder.encode_cube([2, 5], [1, 1])) == 2

    @pytest.mark.parametrize(
        "coord, non_deg, cubeid",
        [
            ((0, 0), (0, 0), 0),
            ((2, 5), (1, 1), None),
            ((2, 5), (1, 0), None),
            ((2, 5), (0, 1), None),
        ],
    )
    def test_encode_cube_and_decode_cube(self, coord, non_deg, cubeid):
        encoder = CubeEncoder([4, 7])
        if cubeid is not None:
            assert encoder.encode_cube(coord, non_deg) == cubeid
        cubeint = encoder.encode_cube(coord, non_deg)
        assert isinstance(cubeint, int)
        assert encoder.decode_cube(cubeint) == (list(coord), list(non_deg))
