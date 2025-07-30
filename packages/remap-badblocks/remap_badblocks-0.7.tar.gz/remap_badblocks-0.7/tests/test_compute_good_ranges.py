import random
from itertools import tee
from typing import Iterable, Iterator

import pytest

from remap_badblocks.src.badblocks._compute_good_ranges import (
    compute_good_ranges, reserve_space_from_good_ranges)
from remap_badblocks.src.remappers._generate_dm_table import generate_dm_table
from remap_badblocks.src.test_utils import (count_sectors_in_ranges,
                                            iter_to_shuffled_generator)


@pytest.mark.parametrize(
    "bad_sectors, available_range, expected_ranges",
    [
        # Basic functionality
        ([2, 3, 5], (0, 9), [(0, 2), (4, 5), (6, 9)]),
        # No bad sectors
        ([], (0, 9), [(0, 9)]),
        ([], (3, 10), [(3, 10)]),
        # All sectors are bad
        (range(10), (0, 10), []),
        # Bad sectors at the beginning and end
        ([0, 1, 8, 9], (0, 10), [(2, 8)]),
        # Ephemeral shuffled iterable
        (iter_to_shuffled_generator(range(10)), (0, 10), []),
        # No broken extremes
        ([2, 3, 5], (0, 10), [(0, 2), (4, 5), (6, 10)]),
        # Uncomplete device
        ([2, 3, 5], (3, 11), [(4, 5), (6, 11)]),
        ([7, 8, 9], (3, 11), [(3, 7), (10, 11)]),
    ],
)
def test_compute_good_ranges(
    bad_sectors: Iterable[int],
    available_range: tuple[int, int],
    expected_ranges: list[tuple[int, int]],
):
    result = list(compute_good_ranges(bad_sectors, available_range=available_range))
    assert result == expected_ranges


@pytest.mark.parametrize(
    "good_ranges, spare_sectors",
    [
        # Test case 1: Basic functionality
        ([(0, 2), (4, 5), (6, 10)], 2),
        # Test case 2: No good ranges
        ([], 2),
        # Test case 3: All good sectors reserved
        ([(0, 10)], 10),
        # Test case 4: Spare sectors exceed available good sectors
        ([(0, 2), (4, 5), (6, 10)], 10),
        # Test case 5: Ephemeral shuffled iterable
        (iter_to_shuffled_generator([(0, 2), (4, 5), (6, 10)]), 10),
        # Test case 6: Ephemeral shuffled iterable
        (iter_to_shuffled_generator([(0, 2), (4, 5), (6, 10)]), 2),
        # Test case 7: Unsorted list
        ([(4, 5), (6, 10), (0, 2)], 2),
        # Test case 8: Real case
        (
            [
                (0, 464992),
                (464994, 825480),
                (825488, 2384152),
                (2384160, 6702752),
                (6702760, 6702768),
                (6702776, 6702816),
                (6702824, 18360728),
                (18360736, 18449304),
                (18449305, 18456312),
                (18456320, 18456328),
                (18456336, 18456344),
                (18456352, 25501304),
                (25501312, 34432448),
                (34432454, 43016120),
                (43016136, 235886992),
                (235886994, 653916408),
                (653916416, 766445288),
                (766445289, 796938504),
                (796938512, 976773168),
            ],
            1048576,
        ),
    ],
)
def test_reserve_space_from_good_ranges(
    good_ranges: Iterator[tuple[int, int]], spare_sectors: int
):
    good_ranges, good_ranges_copy = tee(good_ranges, 2)

    result = list(reserve_space_from_good_ranges(good_ranges, spare_sectors))

    n_original_sectors = count_sectors_in_ranges(good_ranges_copy)
    n_sectors_in_result = count_sectors_in_ranges(result)

    if n_original_sectors >= spare_sectors:
        assert n_original_sectors - n_sectors_in_result == spare_sectors
    else:
        assert n_sectors_in_result == 0


SAMPLE_MAPPING = [
    (1335566, 2384160, 4318592),
    (24452653, 25501312, 8931136),
    (33383789, 34432454, 8583666),
    (795889812, 796938512, 179834656),
    (17407701, 18456352, 7044952),
    (17400678, 18449305, 7007),
    (5654166, 6702776, 40),
    (5654158, 6702760, 8),
    (17407685, 18456320, 8),
    (17407693, 18456336, 8),
    (41967455, 43016136, 192870856),
    (652867725, 653916416, 112528872),
    (765396597, 766445289, 30493215),
    (5654206, 6702824, 11657904),
    (234838311, 235886994, 418029414),
    (17312110, 18360736, 88568),
    (0, 1048586, 1335566),
]


@pytest.mark.parametrize(
    "seed",
    range(10),
)
def test_generate_dm_table_is_sorted(seed: int):
    last_start = -1
    random.seed(seed)
    random.shuffle(SAMPLE_MAPPING)
    for row in generate_dm_table("/dev/test_path", SAMPLE_MAPPING, 512):
        if row:
            row_virtual_start = int(row.split(" ")[0].strip())
            assert row_virtual_start > last_start
            last_start = row_virtual_start
