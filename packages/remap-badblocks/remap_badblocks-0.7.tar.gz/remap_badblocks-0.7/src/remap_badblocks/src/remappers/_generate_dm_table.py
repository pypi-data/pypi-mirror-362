from pathlib import Path
from typing import Generator, Iterable, TypeVar, Union

from remap_badblocks.src.devices.devices_config import Mapping


def generate_dm_table(
    device: Union[Path, str],
    mapping: Union[Iterable[tuple[int, int, int]], Mapping],
    block_size: int,
) -> Generator[str, None, None]:
    """Generate a device-mapper linear mapping table from good ranges."""
    block_size_multiplier = block_size / 512
    assert block_size_multiplier.is_integer(), "Block size must be a multiple of 512"
    block_size_multiplier = int(block_size_multiplier)

    T = TypeVar("T")

    def get_first(iterable: Iterable[T]) -> T:
        return next(iter(iterable))

    for start_virtual, start_real, length in sorted(mapping, key=get_first):
        start_virtual *= block_size_multiplier
        start_real *= block_size_multiplier
        length *= block_size_multiplier

        yield f"{start_virtual} {length} linear {device} {start_real}"
