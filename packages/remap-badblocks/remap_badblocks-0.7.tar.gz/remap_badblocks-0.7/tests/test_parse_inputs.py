from typing import Optional

import pytest

from remap_badblocks.src.utils._parse_inputs import (
    parse_bytes_to_sectors, parse_memory_number_to_bytes,
    parse_memory_range_to_bytes)


@pytest.mark.parametrize(
    "sector_size",
    [512, 1024, 4096],
)
@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("0B", 0),
        ("1B", 1),
        ("1024B", 1024),
        ("1KB", 1024),
        ("1MB", 1024 * 1024),
        ("1GB", 1024 * 1024 * 1024),
        ("10MB", 10 * 1024 * 1024),
        ("10GB", 10 * 1024 * 1024 * 1024),
    ],
)
def test_parse_memory_number_to_bytes__no_sectors(
    input_str: str, expected_output: int, sector_size: int
):
    """
    Test the parse_memory_space function with various inputs.
    """
    result = parse_memory_number_to_bytes(input_str, sector_size=sector_size)
    assert result == expected_output, f"Expected {expected_output} but got {result}"


@pytest.mark.parametrize(
    "input_str, sector_size, expected_output",
    [
        ("0", 512, 0),
        ("1", 512, 512),
        ("1", 1024, 1024),
        ("1", 4096, 4096),
        ("1024", 1, 1024),
        ("10", 4096, 40960),
        ("3000000", 1024, 3000000 * 1024),
        ("30000000", 512, 30000000 * 512),
    ],
)
def test_parse_memory_space_sectors(
    input_str: str, sector_size: int, expected_output: int
):
    result = parse_memory_number_to_bytes(input_str, sector_size=sector_size)
    assert result == expected_output, f"Expected {expected_output} but got {result}"


@pytest.mark.parametrize(
    "input_str, sector_size, expected_output",
    [
        ("1-2", 512, (512, 1024)),
        ("1-3", 1024, (1024, 3072)),
        ("1-4", 4096, (4096, 16384)),
        ("1000-2000", 512, (512000, 1024000)),
        ("5MB-6MB", 512, (5 * 1024**2, 6 * 1024**2)),
        ("1000-", 512, (512000, None)),
        ("0-", 512, (0, None)),
        ("-2000", 512, (None, 1024000)),
        ("-2000B", 512, (None, 2000)),
        ("-", 512, (None, None)),
        ("1000-2000KB", 512, (512000, 2048000)),
        ("1000B-2000B", 512, (1000, 2000)),
        ("1.5KB-", 512, (1024 + 512, None)),
    ],
)
def test_parse_memory_range_to_bytes(
    input_str: str, sector_size: int, expected_output: tuple[int, Optional[int]]
):
    """
    Test the parse_memory_range_to_bytes function with various inputs.
    """
    start, end = parse_memory_range_to_bytes(input_str, sector_size=sector_size)
    assert (
        start,
        end,
    ) == expected_output, f"Expected {expected_output} but got {(start, end)}"


@pytest.mark.parametrize(
    "sector_size",
    [512, 1024, 4096],
)
@pytest.mark.parametrize(
    "input_str",
    [
        "",
        "invalid",
        "1-2-3",
        "1-2-3-4",
        "13WB-",
        "-13WB",
        "5-4",
        "5MB-4MB",
        "MB-",
        "MB-MB",
    ],
)
def test_parse_memory_range_to_bytes_breaks(input_str: str, sector_size: int):
    """
    Test the parse_memory_range_to_bytes function breaks with wrong inputs.
    """
    with pytest.raises(ValueError):
        parse_memory_range_to_bytes(input_str, sector_size=sector_size)


@pytest.mark.parametrize(
    "_bytes, sector_size, expected_output",
    [
        (1024, 512, 2),
        (0, 512, 0),
        (512, 512, 1),
    ],
)
def test_parse_bytes_to_sectors(_bytes: int, sector_size: int, expected_output: int):
    assert parse_bytes_to_sectors(_bytes, sector_size) == expected_output


@pytest.mark.parametrize(
    "_bytes, sector_size",
    [
        (1023, 512),
        (1, 512),
        (513, 512),
    ],
)
def test_parse_bytes_to_sectors_errors(_bytes: int, sector_size: int):
    with pytest.raises(ValueError):
        parse_bytes_to_sectors(_bytes, sector_size)
