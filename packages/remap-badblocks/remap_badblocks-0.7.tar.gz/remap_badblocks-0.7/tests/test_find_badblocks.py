import tempfile
from typing import Optional

import pytest

from remap_badblocks.src.badblocks._find_badblocks import (
    build_badblocks_command, parse_badblocks, read_known_badblocks)

test_params: list[tuple[list[str], set[int]]] = [
    (["12345\n", "67890\n", "54321\n"], {12345, 67890, 54321}),  # Normal case
    ([""], set()),  # Empty input
    (["12345\n", "abcde\n", "67890\n"], {12345, 67890}),  # Input with non-numeric lines
    (
        ["   12345   \n", "67890\n   "],
        {12345, 67890},
    ),  # Input with leading/trailing whitespace
]


@pytest.mark.parametrize(
    "input_data, expected_output",
    test_params,
)
def test_parse_badblocks(input_data: list[str], expected_output: set[int]):
    assert set(parse_badblocks(input_data)) == expected_output


@pytest.mark.parametrize(
    "device, mode, known_badblocks_file, sector_size, blocks_range, expected_command",
    [
        # Test case 1: Read mode without known badblocks file
        (
            "/dev/sda",
            "read",
            None,
            512,
            None,
            ["badblocks", "-sv", "-b", "512", "/dev/sda"],
        ),
        # Test case 2: Write mode with known badblocks file
        (
            "/dev/sda",
            "write",
            "/path/to/known_badblocks.txt",
            512,
            None,
            [
                "badblocks",
                "-wsv",
                "-b",
                "512",
                "-i",
                "/path/to/known_badblocks.txt",
                "/dev/sda",
            ],
        ),
        # Test case 3: Different sector size
        (
            "/dev/sda",
            "write",
            "/path/to/known_badblocks.txt",
            1024,
            None,
            [
                "badblocks",
                "-wsv",
                "-b",
                "1024",
                "-i",
                "/path/to/known_badblocks.txt",
                "/dev/sda",
            ],
        ),
        # Test case 4: None path to known badblocks file
        (
            "/dev/sda",
            "write",
            None,
            512,
            None,
            ["badblocks", "-wsv", "-b", "512", "/dev/sda"],
        ),
        # Test case 5: Block range specified
        (
            "/dev/sda",
            "read",
            None,
            512,
            (0, 1000),
            ["badblocks", "-sv", "-b", "512", "/dev/sda", "1000", "0"],
        ),
        # Test case 6: Block range and known badblocks specified
        (
            "/dev/sda",
            "read",
            "/path/to/known_badblocks.txt",
            512,
            (0, 1000),
            [
                "badblocks",
                "-sv",
                "-b",
                "512",
                "-i",
                "/path/to/known_badblocks.txt",
                "/dev/sda",
                "1000",
                "0",
            ],
        ),
    ],
)
def test_build_badblocks_command(
    device: str,
    mode: str,
    known_badblocks_file: Optional[str],
    sector_size: int,
    blocks_range: Optional[tuple[int, int]],
    expected_command: list[str],
):
    assert (
        build_badblocks_command(
            device, sector_size, mode, known_badblocks_file, blocks_range
        )
        == expected_command
    )


def test_build_badblocks_command_error():
    with pytest.raises(ValueError):
        build_badblocks_command("/dev/sda", 512, "invalid_mode", None, None)


def test_read_known_badblocks():
    old_badblocks_file_content = "54321\n67890\n"
    expected_output = {67890, 54321}

    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(delete=True) as temp_known_badblocks_file:
        temp_known_badblocks_file.write(old_badblocks_file_content.encode("utf-8"))
        temp_known_badblocks_file.flush()

        assert (
            set(read_known_badblocks(temp_known_badblocks_file.name)) == expected_output
        )
