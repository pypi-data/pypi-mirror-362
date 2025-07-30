from typing import Generator, Iterable


def compute_good_ranges(
    bad_sectors: Iterable[int], available_range: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    """
    Compute good sector ranges, excluding bad sectors.
    available_range is expected to be a range that is right-open
    result is a range that is right-open
    """
    bad_sectors = sorted(set(bad_sectors))  # Ensure bad_sectors is sorted and unique
    current_start = available_range[0]
    last_sector = available_range[1] - 1

    for bad_sector in bad_sectors:
        if bad_sector > last_sector:
            break
        if current_start < bad_sector:
            yield (current_start, bad_sector)
        current_start = bad_sector + 1

    if current_start <= last_sector:
        yield (current_start, last_sector + 1)


def reserve_space_from_good_ranges(
    good_ranges: Iterable[tuple[int, int]], spare_sectors: int
) -> Generator[tuple[int, int], None, None]:
    """
    Return good sector ranges, skipping the first `spare_sectors` good sectors as reserved space.
    Both input and output ranges are right-open.
    """
    to_reserve = spare_sectors
    for start, end in good_ranges:
        length = end - start
        if to_reserve >= length:
            to_reserve -= length
            continue
        elif to_reserve > 0:
            start += to_reserve
            to_reserve = 0
        yield (start, end)
