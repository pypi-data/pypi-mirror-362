from typing import Iterable

import pytest

from remap_badblocks.src.badblocks._remap_badblocks import (
    count_used_spare_sectors, iter_all_spare_sectors, remap_badblocks,
    simplify_mapping)


@pytest.mark.parametrize(
    "mapping_in, mapping_out_expected",
    [
        [[(0, 0, 5), (5, 5, 13)], [(0, 0, 18)]],
        [
            [
                (5, 9, 13),
                (0, 4, 5),
            ],
            [
                (0, 4, 18),
            ],
        ],
        [[(0, 0, 500)], [(0, 0, 500)]],
        [
            [
                (15, 3, 1),
                (16, 4, 1),
                (17, 5, 1),
                (18, 6, 2),
                (20, 8, 100),
                (4592, 347, 10),
                (4602, 357, 4),
            ],
            [
                (15, 3, 105),
                (4592, 347, 14),
            ],
        ],
    ],
)
def test_simplify_mapping(
    mapping_in: list[tuple[int, int, int]],
    mapping_out_expected: Iterable[tuple[int, int, int]],
):
    mapping_out = simplify_mapping(mapping_in)

    assert set(mapping_out) == set(mapping_out_expected)


@pytest.mark.parametrize("spare_sectors_n", [10, 20, 100])
@pytest.mark.parametrize(
    "mapping, badblocks",
    [
        ([(0, 1024, 1024), (1024, 3000, 1000)], [0, 1025, 2050, 2800, 1026]),
        ([(0, 1024, 1024)], [1, 1024, 1025, 1026, 1027, 1028]),
    ],
)
def test_remap_badblocks__no_badblocks_in_output(
    mapping: Iterable[tuple[int, int, int]],
    badblocks: Iterable[int],
    spare_sectors_n: int,
):
    spare_sectors = iter(range(spare_sectors_n))
    remapped = list(remap_badblocks(mapping, badblocks, spare_sectors))

    for _, start, length in remapped:
        for badblock in badblocks:
            assert not (start <= badblock < start + length)


@pytest.mark.parametrize(
    "mapping, badblocks, spare_sectors_n, is_enough",
    [
        (
            [(0, 1024, 1024)],
            list(range(1024, 1035)),
            10,
            False,
        ),
        (
            [(0, 1024, 1024)],
            list(range(1024, 1034)),
            10,
            True,
        ),
        (
            [(0, 1024, 1024)],
            [],
            10,
            True,
        ),
        [
            [(0, 1024, 1024)],
            list(range(10)) + [2047],
            10,
            False,
        ],
        [
            [(0, 1024, 1024)],
            list(range(10)) + [2048],
            10,
            True,
        ],
    ],
)
def test_remap_badblocks__not_enough_spares(
    mapping: Iterable[tuple[int, int, int]],
    badblocks: Iterable[int],
    spare_sectors_n: int,
    is_enough: bool,
):
    spare_sectors = iter(range(spare_sectors_n))

    if is_enough:
        list(remap_badblocks(mapping, badblocks, spare_sectors))
    else:
        with pytest.raises(RuntimeError):
            list(remap_badblocks(mapping, badblocks, spare_sectors))


@pytest.mark.parametrize("spare_sectors_n", [10, 20, 100])
@pytest.mark.parametrize(
    "mapping, badblocks",
    [
        ([(0, 1024, 1024), (1024, 3000, 1000)], [0, 1025, 2050, 2800, 1026]),
        ([(0, 1024, 1024)], [1, 1024, 1025, 1026, 1027, 1028]),
        ([(0, 1024, 1024)], [3, 1024, 1025, 1026, 1027, 1028, 2046, 2047, 2048]),
        ([(0, 1024, 1024)], [5, 1024, 1025, 1026, 1027, 1028, 2046, 2047]),
    ],
)
def test_remap_badblocks__is_keeping_good_ranges_constant(
    mapping: Iterable[tuple[int, int, int]],
    badblocks: Iterable[int],
    spare_sectors_n: int,
):
    spare_sectors = iter(range(spare_sectors_n))
    remapped = list(remap_badblocks(mapping, badblocks, spare_sectors))

    old_maps_to_keep: set[tuple[int, int]] = set()

    for start_virt_old, start_real_old, length_old in mapping:
        for virt_old, real_old in zip(
            range(start_virt_old, start_virt_old + length_old),
            range(start_real_old, start_real_old + length_old),
        ):
            if real_old not in badblocks:
                old_maps_to_keep.add((virt_old, real_old))

    new_maps: set[tuple[int, int]] = set()
    for start_virt_new, start_real_new, length_new in remapped:
        for virt_new, real_new in zip(
            range(start_virt_new, start_virt_new + length_new),
            range(start_real_new, start_real_new + length_new),
        ):
            new_maps.add((virt_new, real_new))

    assert old_maps_to_keep.issubset(new_maps)


@pytest.mark.parametrize(
    "mapping, n_spare_sectors, answer",
    [
        (
            [(0, 10, 5), (5, 17, 8)],
            10,
            0,
        ),
        (
            [(0, 10, 5), (5, 0, 2), (7, 17, 8)],
            10,
            2,
        ),
        (
            [(0, 10, 5), (5, 0, 2), (7, 17, 8), (15, 2, 4)],
            10,
            6,
        ),
    ],
)
def test_count_used_spare_sectors(
    mapping: Iterable[tuple[int, int, int]], n_spare_sectors: int, answer: int
):
    spare_sectors = iter_all_spare_sectors(n_spare_sectors, 0)
    assert answer == count_used_spare_sectors(mapping, spare_sectors)
