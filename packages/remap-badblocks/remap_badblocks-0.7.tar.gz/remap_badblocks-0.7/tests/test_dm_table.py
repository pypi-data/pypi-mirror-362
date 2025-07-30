from typing import Iterable

import pytest

from remap_badblocks.src.badblocks._mapping_generation import generate_mapping
from remap_badblocks.src.remappers._generate_dm_table import generate_dm_table


@pytest.mark.parametrize(
    "ranges, block_size, expected_output",
    [
        ([(0, 6), (10, 16)], 512, ["0 6 linear /dev/sda 0", "6 6 linear /dev/sda 10"]),
        (
            iter([(0, 6), (10, 16)]),
            512,
            ["0 6 linear /dev/sda 0", "6 6 linear /dev/sda 10"],
        ),
        (
            iter([(10, 16), (0, 6)]),
            512,
            ["0 6 linear /dev/sda 10", "6 6 linear /dev/sda 0"],
        ),
        (
            [(0, 6), (10, 16)],
            1024,
            ["0 12 linear /dev/sda 0", "12 12 linear /dev/sda 20"],
        ),
    ],
)
def test_generate_dm_table(
    ranges: Iterable[tuple[int, int]], block_size: int, expected_output: list[str]
):
    device = "/dev/sda"

    mapping = generate_mapping(ranges)
    result = list(generate_dm_table(device, mapping, block_size))

    assert len(result) == len(expected_output)

    assert set(result) == set(
        expected_output
    ), f"Expected {expected_output}, but got {result}"
