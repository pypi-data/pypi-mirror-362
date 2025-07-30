from typing import Generator, Iterable


def generate_mapping(
    ranges: Iterable[tuple[int, int]],
) -> Generator[tuple[int, int, int], None, None]:
    """Generate a mapping from good ranges."""
    offset = 0
    for start, end in ranges:
        length = end - start
        yield (offset, start, length)  # (start_id_virtual, start_id_real, length)
        offset += length
