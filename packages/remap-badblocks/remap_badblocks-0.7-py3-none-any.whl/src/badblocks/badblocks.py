from dataclasses import dataclass
from typing import Iterable, Iterator

from remap_badblocks.src.utils._iterable_bytes_converter import (
    iterable_from_bytes, iterable_to_bytes)


@dataclass
class Badblocks(Iterable[int]):
    badblocks: set[int]

    INT_LENGTH: int = 8

    def __init__(self, badblocks: Iterable[int]):
        self.badblocks = set(badblocks)

    def __bytes__(self) -> bytes:
        """
        Convert the Badblocks to bytes for storage.
        """
        return iterable_to_bytes(self.badblocks, length=self.INT_LENGTH)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Badblocks":
        """
        Create a Badblocks instance from bytes.
        """
        return cls(badblocks=set(iterable_from_bytes(data, length=cls.INT_LENGTH)))

    def __len__(self) -> int:
        """
        Get the number of bad blocks.
        """
        return len(self.badblocks)

    def __iter__(self) -> Iterator[int]:
        """
        Iterate over the bad blocks.
        """
        return iter(self.badblocks)
