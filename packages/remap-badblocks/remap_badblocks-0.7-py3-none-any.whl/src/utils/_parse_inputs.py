import re
from typing import Optional


def parse_string_with_unit_to_bytes(txt: str, unit_multiplier: int) -> int:
    return round(float(txt) * unit_multiplier)


def parse_bytes_to_sectors(_input: int, sector_size: int) -> int:
    if _input % sector_size != 0:
        raise ValueError(
            f"{_input}B is not a multiple of the sector size {sector_size}B."
        )
    return int(_input / sector_size)


def parse_memory_number_to_bytes(txt: str, sector_size: int) -> int:
    """
    Parses a memory value (a sector number or a space size) and outputs a sector number.
    """
    txt = txt.strip()

    try:
        return parse_string_with_unit_to_bytes(txt, sector_size)
    except ValueError:
        pass
    try:
        if txt.endswith("MB"):
            return parse_string_with_unit_to_bytes(txt[:-2], 1024**2)
        elif txt.endswith("GB"):
            return parse_string_with_unit_to_bytes(txt[:-2], 1024**3)
        elif txt.endswith("KB"):
            return parse_string_with_unit_to_bytes(txt[:-2], 1024)
        elif txt.endswith("B"):
            return parse_string_with_unit_to_bytes(txt[:-1], 1)
        else:
            raise ValueError(f"Invalid format: {txt}")
    except ValueError as e:
        raise ValueError(f"Failed to parse memory space from '{txt}': {e}") from e


def parse_memory_range_to_bytes(
    txt: str, sector_size: int
) -> tuple[Optional[int], Optional[int]]:
    """
    Parse a memory space range from a string and check the format is valid. Returns a sector range.
    I.e. checks that the format is 'start-end', where each can be omitted, and start <= end.
    """
    txt = txt.strip()

    m = re.match(
        r"^(?P<start>\d+(\.\d+)?(?:[KMGT]?B)?)?-(?P<end>\d+(\.\d+)?(?:[KMGT]?B)?)?$",
        txt,
    )
    if m is None:
        raise ValueError(
            f"Invalid format: {txt}. Expected format: 'start-end', where each can be omitted."
        )
    groups: dict[str, str | None] = {key: m.group(key) for key in ("start", "end")}
    values: dict[str, int] = {
        key: parse_memory_number_to_bytes(value, sector_size)
        for key, value in groups.items()
        if value is not None
    }

    start, end = values.get("start"), values.get("end")

    if start is not None and end is not None and (end < start):
        raise ValueError(f"End {end} must be greater than or equal to start {start}.")

    return start, end


def parse_memory_range_to_sectors(
    txt: str, sector_size: int
) -> tuple[Optional[int], Optional[int]]:
    start, end = parse_memory_range_to_bytes(txt, sector_size)

    if start is not None:
        start = parse_bytes_to_sectors(start, sector_size)
    if end is not None:
        end = parse_bytes_to_sectors(end, sector_size)

    return start, end
