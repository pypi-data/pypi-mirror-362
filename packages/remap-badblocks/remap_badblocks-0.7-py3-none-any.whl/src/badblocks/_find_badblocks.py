from itertools import chain
from pathlib import Path
from typing import Iterable, Optional, Union

from remap_badblocks.src.utils._run_command import run_command_realtime


def parse_badblocks(lines: Iterable[str]) -> Iterable[int]:
    """Parse badblocks output and return a set of bad sector numbers."""
    lines = map(lambda line: line.strip(), lines)
    lines = filter(lambda line: line.isdigit(), lines)
    return map(int, lines)


def read_known_badblocks(known_badblocks_file: Union[Path, str]) -> Iterable[int]:
    """Merge badblocks with known badblocks from a file."""
    with open(known_badblocks_file, "r") as f:
        known_badblocks = parse_badblocks(f.readlines())
    return known_badblocks


def build_badblocks_command(
    device: Union[Path, str],
    sector_size: int,
    mode: str,
    known_badblocks_file: Optional[Union[Path, str]],
    blocks_range: Optional[tuple[int, int]],
) -> list[str]:
    """
    Build the badblocks command based on the mode and optional known badblocks file.
    blocks_range is a right-open interval
    """
    if mode == "read":
        cmd = ["badblocks", "-sv"]
    elif mode == "write":
        cmd = ["badblocks", "-wsv"]
    else:
        raise ValueError("Invalid mode. Use 'read' or 'write'.")

    cmd += ["-b", str(sector_size)]

    if known_badblocks_file:
        cmd += ["-i", str(known_badblocks_file)]

    cmd += [str(device)]

    if blocks_range:
        start_block, end_block = blocks_range
        cmd += [str(end_block), str(start_block)]

    return cmd


def get_all_badblocks(
    device: Path,
    sector_size: int,
    mode: str = "read",
    known_badblocks_file: Optional[Path] = None,
    block_range: Optional[tuple[int, int]] = None,
) -> Iterable[int]:
    """
    Run badblocks on a device and return the results as a set of bad sectors.
    block_range is a right-open interval
    """
    badblocks: Iterable[int] = set()

    if known_badblocks_file:
        badblocks = read_known_badblocks(known_badblocks_file)

    cmd = build_badblocks_command(
        device, sector_size, mode, known_badblocks_file, block_range
    )
    badblocks_lines = run_command_realtime(cmd)
    badblocks = chain(badblocks, parse_badblocks(badblocks_lines))

    return badblocks
