import sqlite3
from dataclasses import dataclass
from typing import Collection, Iterator

from remap_badblocks.src.utils._iterable_bytes_converter import (
    iterable_from_bytes, iterable_to_bytes)

DEFAULT_INT_LENGTH = 8


@dataclass
class MappingElement:
    start_id_virtual: int
    start_id_real: int
    length: int

    INT_LENGTH: int = DEFAULT_INT_LENGTH
    BYTES_LENGTH: int = 3 * INT_LENGTH

    def __bytes__(self) -> bytes:
        """
        Convert the MappingElement to bytes for storage.
        """
        return iterable_to_bytes(
            (
                self.start_id_virtual,
                self.start_id_real,
                self.length,
            ),
            length=self.INT_LENGTH,
        )

    def __index__(self) -> int:
        """
        Convert the MappingElement to an integer for storage.
        """
        return int.from_bytes(self.__bytes__(), "big")

    @classmethod
    def from_bytes(cls, data: bytes) -> "MappingElement":
        """
        Create a MappingElement from bytes.
        """
        if len(data) != cls.BYTES_LENGTH:
            raise ValueError(f"Data must be exactly {cls.BYTES_LENGTH} bytes long.")
        start_id_virtual, start_id_real, length = iterable_from_bytes(
            data, length=cls.INT_LENGTH
        )
        return cls(start_id_virtual, start_id_real, length)

    def __hash__(self) -> int:
        """
        Hash the MappingElement for use in sets or dictionaries.
        """
        return self.__index__()

    @classmethod
    def from_tuple(cls, _tuple: tuple[int, int, int]) -> "MappingElement":
        """
        Create a MappingElement from a tuple.
        """
        if len(_tuple) != 3:
            raise ValueError("Tuple must contain exactly three elements.")
        return cls(
            start_id_virtual=_tuple[0], start_id_real=_tuple[1], length=_tuple[2]
        )

    def to_tuple(self) -> tuple[int, int, int]:
        return self.start_id_virtual, self.start_id_real, self.length

    def __iter__(self) -> Iterator[int]:
        return iter(self.to_tuple())


@dataclass
class Mapping:
    elements: Collection[MappingElement]

    def __bytes__(self) -> bytes:
        """
        Convert the Mapping to bytes for storage.
        """
        return b"".join(bytes(element) for element in self.elements)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Mapping":
        """
        Create a Mapping from bytes.
        """
        if len(data) % MappingElement.BYTES_LENGTH != 0:
            raise ValueError(
                "Data length is not a multiple of {} bytes.",
                MappingElement.BYTES_LENGTH,
            )
        elements: list[MappingElement] = []
        for i in range(0, len(data), MappingElement.BYTES_LENGTH):
            elements.append(
                MappingElement.from_bytes(data[i : i + MappingElement.BYTES_LENGTH])
            )
        return cls(elements)

    def to_sql_binary(self) -> sqlite3.Binary:
        """
        Convert the Mapping to a binary format suitable for SQLite storage.
        """
        return sqlite3.Binary(bytes(self))

    def __iter__(self) -> Iterator[MappingElement]:
        return iter(self.elements)
