import itertools
from typing import Iterable, Iterator, Optional, Union

from remap_badblocks.src.devices.devices_config import Mapping


def remap_badblocks(
    mapping: Iterable[tuple[int, int, int]],
    badblocks: Iterable[int],
    spare_sectors: Iterator[int],
) -> Iterable[tuple[int, int, int]]:
    sorted_badblocks = sorted(badblocks)

    for start_virtual, start_real, length in mapping:
        end_real = start_real + length - 1
        sorted_to_remap: list[int] = []
        sorted_to_remap_virtual: list[int] = []
        for badblock in sorted_badblocks:
            if start_real <= badblock <= end_real:
                sorted_to_remap.append(badblock)
        if not sorted_to_remap:
            # nothing to remap
            yield start_virtual, start_real, length
        else:
            current_start_virtual = start_virtual
            current_start_real = start_real
            for badblock in sorted_to_remap:
                if current_start_real < badblock:
                    # pieces to keep
                    yield current_start_virtual, current_start_real, badblock - current_start_real
                step = badblock - current_start_real + 1
                current_start_virtual += step
                current_start_real += step
                sorted_to_remap_virtual.append(current_start_virtual - 1)
            if current_start_real < end_real:
                # pieces to keep
                yield current_start_virtual, current_start_real, end_real - current_start_real + 1
            for virt_to_remap in sorted_to_remap_virtual:
                try:
                    while (spare_sector := next(spare_sectors)) in badblocks:
                        pass
                except StopIteration:
                    raise RuntimeError
                # remap
                yield virt_to_remap, spare_sector, 1


def identify_simplifiable_couple_in_mapping(
    mapping: list[tuple[int, int, int]],
) -> Optional[tuple[int, int]]:
    for i, (start_virtual_0, start_real_0, length_0) in enumerate(mapping[:-1]):
        end_virtual_0 = start_virtual_0 + length_0
        end_real_0 = start_real_0 + length_0
        for _j, (start_virtual_1, start_real_1, length_1) in enumerate(
            mapping[i + 1 :]
        ):
            j = _j + i + 1
            end_virtual_1 = start_virtual_1 + length_1
            end_real_1 = start_real_1 + length_1
            if (start_virtual_0 == end_virtual_1) and (start_real_0 == end_real_1):
                return j, i
            if (start_virtual_1 == end_virtual_0) and (start_real_1 == end_real_0):
                return i, j
    return None


def simplify_mapping(
    mapping: list[tuple[int, int, int]],
) -> Iterable[tuple[int, int, int]]:
    while (to_simplify := identify_simplifiable_couple_in_mapping(mapping)) is not None:
        i, j = to_simplify
        element_i = mapping[i]
        element_j = mapping[j]

        simplified_element = element_i[0], element_i[1], element_i[2] + element_j[2]

        _i = min(i, j)
        _j = max(i, j)

        mapping = (
            mapping[:_i]
            + mapping[_i + 1 : _j]
            + mapping[_j + 1 :]
            + [simplified_element]
        )

    return mapping


def iter_all_spare_sectors(
    n_spare_sectors: int, first_spare_sector: int
) -> Iterator[int]:
    return iter(range(first_spare_sector, first_spare_sector + n_spare_sectors))


def iter_free_spare_sectors(
    spare_sectors: Iterable[int], n_used_spare_sectors: int
) -> Iterator[int]:
    return itertools.islice(spare_sectors, n_used_spare_sectors, None)


def count_used_spare_sectors(
    mapping: Union[Iterable[tuple[int, int, int]], Mapping],
    spare_sectors: Iterable[int],
) -> int:
    spare_sectors = set(spare_sectors)
    used = 0
    for _, start, length in mapping:
        end = start + length
        for s in spare_sectors:
            if start <= s < end:
                used += 1

    return used
