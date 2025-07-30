import os
import re
import sqlite3 as sqlite
from collections import OrderedDict
from pathlib import Path
from typing import (Any, Collection, Iterable, Literal, Optional, Union,
                    overload)

from remap_badblocks.src.badblocks.badblocks import Badblocks
from remap_badblocks.src.mapping import Mapping
from remap_badblocks.src.utils._iterable_bytes_converter import (
    iterable_from_bytes, iterable_to_bytes)

from .device_config import DeviceConfig
from .exceptions import DeviceNotFoundError

DEFAULT_INT_LENGTH = 8
DEVICE_INFO_COLUMNS_TYPES = OrderedDict(
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "path": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "sector_size": "INTEGER NOT NULL",
        "badblocks": "BLOB NOT NULL",
        "spare_sectors": "INTEGER",
        "mapping": "BLOB",
        "depends_on": "BLOB NOT NULL",
        "logical_range_start": "INTEGER NOT NULL",
        "logical_range_end": "INTEGER NOT NULL",
        "apply_at_startup": "BOOLEAN DEFAULT FALSE NOT NULL",
    }
)


class DevicesConfig:
    _path: Path

    def __init__(self, path: Union[Path, str]):
        if isinstance(path, str):
            path = Path(path)
        assert not path.is_dir(), "The provided path must not be a directory."
        self._path = path
        self.__init_table()

    def __init_table(self) -> None:
        """
        Initialize the devices table in the database.
        """
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with sqlite.connect(self._path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS devices (
                """
                + ",".join(
                    (
                        col_name + " " + col_type
                        for col_name, col_type in DEVICE_INFO_COLUMNS_TYPES.items()
                    )
                )
                + """
                )
                """
            )
            conn.commit()

    def __check_device_in_db(self, conn: sqlite.Connection, id: int) -> bool:
        """
        Check if a device with the given ID exists in the database.
        """
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM devices WHERE id = ? LIMIT 1", (id,))
        val = cursor.fetchone()
        return val is not None

    def _assert_depends_on(
        self, conn: sqlite.Connection, depends_on: Collection[int]
    ) -> None:
        missing: set[int] = set()
        for _id in depends_on:
            if not self.__check_device_in_db(conn, id=_id):
                missing.add(_id)
        if missing:
            raise DeviceNotFoundError(device_id=missing)

    def __parse_device_from_row(
        self,
        id: int,
        path: Union[Path, str],
        name: str,
        sector_size: int,
        badblocks: bytes,
        spare_sectors: Optional[int],
        mapping: Optional[bytes],
        depends_on: bytes,
        logical_range_start: int,
        logical_range_end: int,
        apply_at_startup: bool,
    ) -> DeviceConfig:
        """
        Parse a device configuration from a database row.
        """
        return DeviceConfig(
            id=id,
            path=Path(path),
            name=name,
            sector_size=sector_size,
            badblocks=Badblocks.from_bytes(badblocks),
            spare_sectors=spare_sectors,
            mapping=Mapping.from_bytes(mapping) if mapping is not None else None,
            depends_on=set(iterable_from_bytes(depends_on, length=DEFAULT_INT_LENGTH)),
            logical_range=(logical_range_start, logical_range_end),
            apply_at_startup=apply_at_startup,
        )

    def get_devices(self) -> Iterable[DeviceConfig]:
        """
        Get the devices configuration as a DataFrame.
        """
        with sqlite.connect(self._path) as conn:
            data = conn.execute(
                """SELECT """
                + ",".join(DEVICE_INFO_COLUMNS_TYPES.keys())
                + """ FROM devices"""
            ).fetchall()

        data = [
            self.__parse_device_from_row(
                **dict(zip(DEVICE_INFO_COLUMNS_TYPES.keys(), row))
            )
            for row in data
        ]
        return data

    @overload
    def get_device(self, *, id: int, name: Literal[None] = None) -> DeviceConfig: ...
    @overload
    def get_device(self, *, id: Literal[None] = None, name: str) -> DeviceConfig: ...

    def get_device(
        self, *, id: Optional[int] = None, name: Optional[str] = None
    ) -> DeviceConfig:
        if id is not None and name is not None:
            raise ValueError("Only one of id or name can be provided to get a device.")

        with sqlite.connect(self._path) as conn:
            cursor = conn.cursor()
            QUERY = (
                """SELECT """
                + ",".join(DEVICE_INFO_COLUMNS_TYPES.keys())
                + """ FROM devices"""
            )
            if id is not None:
                cursor.execute(QUERY + " WHERE id = ?", (id,))
            elif name is not None:
                cursor.execute(QUERY + " WHERE name = ?", (name,))
            else:
                raise ValueError("Either id or name must be provided to get a device.")
            row = cursor.fetchone()
            if row is None:
                raise DeviceNotFoundError(device_id=id, device_name=name)

        return self.__parse_device_from_row(
            **dict(zip(DEVICE_INFO_COLUMNS_TYPES.keys(), row))
        )

    def __insert_into_devices_table(self, cursor: sqlite.Cursor, row: dict[str, Any]):
        cols = list(row.keys())
        cursor.execute(
            """INSERT INTO devices
                ("""
            + ",".join(cols)
            + """)
            VALUES ("""
            + ",".join(("?",) * len(cols))
            + """)""",
            tuple(row[col] for col in cols),
        )

    def add_device(
        self,
        path: Union[Path, str],
        name: str,
        logical_range: tuple[int, int],
        *,
        sector_size: Optional[int] = None,
        badblocks: Union[set[int], Badblocks] = set(),
        depends_on: Collection[int] = set(),
    ) -> None:
        _path: Path = Path(path)
        assert _path.exists(), f"The provided device {_path} does not exist."

        assert (
            re.fullmatch(r"[0-9A-Za-z#+\-\.:=@_]+", name) is not None
        ), "Name does not match requirements"

        try:
            existing_dev = self.get_device(name=name)
            raise ValueError(f"Name {name} is used by device {existing_dev.id}.")
        except DeviceNotFoundError:
            pass

        badblocks = Badblocks(badblocks)

        with sqlite.connect(self._path) as conn:
            self._assert_depends_on(conn, depends_on)

            cursor = conn.cursor()
            self.__insert_into_devices_table(
                cursor,
                {
                    "path": str(_path),
                    "name": name,
                    "sector_size": sector_size,
                    "badblocks": sqlite.Binary(bytes(badblocks)),
                    "spare_sectors": None,
                    "mapping": None,
                    "depends_on": iterable_to_bytes(
                        depends_on, length=DEFAULT_INT_LENGTH
                    ),
                    "logical_range_start": logical_range[0],
                    "logical_range_end": logical_range[1],
                },
            )
            conn.commit()

    def remove_device(self, id: int) -> None:
        with sqlite.connect(self._path) as conn:
            if not self.__check_device_in_db(conn, id=id):
                raise DeviceNotFoundError(device_id=id)

            for dev in self.get_devices():
                if id in dev.depends_on:
                    raise KeyError(
                        f"Device {dev.id} depends on device {id}, can't remove the latter."
                    )

            cursor = conn.cursor()
            cursor.execute("DELETE FROM devices WHERE id = ?", (id,))
            conn.commit()

    def update_device(
        self,
        id: int,
        *,
        path: Optional[Union[Path, str]] = None,
        name: Optional[str] = None,
        badblocks: Optional[Iterable[int]] = None,
        mapping: Optional[Mapping] = None,
        spare_sectors: Optional[int] = None,
        depends_on: Optional[Collection[int]] = None,
    ) -> None:
        with sqlite.connect(self._path) as conn:
            if not self.__check_device_in_db(conn, id=id):
                raise DeviceNotFoundError(device_id=id)

            cursor = conn.cursor()
            if path is not None:
                cursor.execute(
                    "UPDATE devices SET path = ? WHERE id = ?", (str(path), id)
                )
            if name is not None:
                cursor.execute("UPDATE devices SET name = ? WHERE id = ?", (name, id))
            if badblocks is not None:
                badblocks = Badblocks(badblocks)
                cursor.execute(
                    "UPDATE devices SET badblocks = ? WHERE id = ?",
                    (sqlite.Binary(bytes(badblocks)), id),
                )
            if mapping is not None:
                cursor.execute(
                    "UPDATE devices SET mapping = ? WHERE id = ?",
                    (sqlite.Binary(bytes(mapping)), id),
                )
            if spare_sectors is not None:
                cursor.execute(
                    "UPDATE devices SET spare_sectors = ? WHERE id = ?",
                    (spare_sectors, id),
                )
            if depends_on is not None:
                self._assert_depends_on(conn, depends_on)
                cursor.execute(
                    "UPDATE devices SET depends_on = ? WHERE id = ?",
                    (
                        iterable_to_bytes(depends_on, length=DEFAULT_INT_LENGTH),
                        id,
                    ),
                )
            conn.commit()

    def __len__(self) -> int:
        """
        Get the number of devices in the database.
        """
        with sqlite.connect(self._path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM devices")
            count = cursor.fetchone()[0]
        return count
