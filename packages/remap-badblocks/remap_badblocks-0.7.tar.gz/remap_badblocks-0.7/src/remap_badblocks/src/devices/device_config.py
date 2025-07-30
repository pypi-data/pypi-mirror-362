from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Union

from remap_badblocks.src.badblocks.badblocks import Badblocks
from remap_badblocks.src.mapping import Mapping


@dataclass
class DeviceConfig:
    id: int
    path: Path
    name: str
    sector_size: int
    badblocks: Badblocks
    depends_on: set[int]
    logical_range: tuple[int, int]
    apply_at_startup: bool = False
    spare_sectors: Optional[int] = None
    mapping: Optional[Mapping] = None

    def __init__(
        self,
        id: int,
        path: Union[Path, str],
        name: str,
        sector_size: int,
        badblocks: Iterable[int],
        logical_range: tuple[int, int],
        apply_at_startup: bool = False,
        depends_on: Iterable[int] = set(),
        spare_sectors: Optional[int] = None,
        mapping: Optional[Mapping] = None,
    ):
        if isinstance(path, str):
            path = Path(path)
        self.id = id
        self.path = path
        self.name = name
        self.sector_size = sector_size
        self.badblocks = Badblocks(badblocks)
        self.mapping = mapping if mapping is not None else None
        self.spare_sectors = spare_sectors
        self.depends_on = set(depends_on)
        self.logical_range = logical_range
        self.apply_at_startup = apply_at_startup

    def __str__(self) -> str:
        return (
            "DeviceConfig("
            f"   id={self.id}, path={self.path}, name={self.name},"
            f"   sector_size={self.sector_size}, badblocks={len(self.badblocks)}, spare_sectors={self.spare_sectors},"
            f"   mapping={'Undefined' if self.mapping is None else 'Defined'},"
            f"   depends_on={self.depends_on}, logical_range={self.logical_range}"
            ")"
        )

    def get_applied_path(self) -> Path:
        return Path("/dev/mapper/", self.name)

    def __hash__(self) -> int:
        return self.id
