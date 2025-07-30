from random import shuffle
from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def iter_to_shuffled_generator(_iter: Iterable[T]) -> Generator[T, None, None]:
    _iter_list = list(_iter)
    shuffle(_iter_list)
    for v in _iter_list:
        yield v


def count_sectors_in_ranges(ranges: Iterable[tuple[int, int]]):
    n_sectors = 0
    for start, end in ranges:
        n_sectors += end - start
    return n_sectors
