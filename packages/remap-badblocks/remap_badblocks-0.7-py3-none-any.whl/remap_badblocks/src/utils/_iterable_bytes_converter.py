from typing import Iterable


def iterable_to_bytes(iterable: Iterable[int], length: int = 4) -> bytes:
    """
    Convert an iterable of integers to bytes.
    """
    return b"".join(i.to_bytes(length, "big") for i in iterable)


def iterable_from_bytes(data: bytes, length: int = 4) -> Iterable[int]:
    """
    Convert bytes to an iterable of integers.
    """
    if len(data) % length != 0:
        raise ValueError(f"Data length must be a multiple of {length} bytes.")
    return (
        int.from_bytes(data[i : i + length], "big") for i in range(0, len(data), length)
    )
