import os
from argparse import Namespace
from pathlib import Path
from typing import Optional, TypedDict

from remap_badblocks.src.devices.devices_config import DevicesConfig
from remap_badblocks.src.utils._get_device_info import (
    get_disk_block_size, get_disk_number_of_blocks, resolve_device_name)
from remap_badblocks.src.utils._parse_inputs import \
    parse_memory_range_to_sectors


class AddArgs(TypedDict):
    wwn: Optional[str]
    path: Optional[Path]
    name: str
    depends_on_id: set[int]
    depends_on: set[str]
    logical_sector_range: str


def parse_args(args: Namespace) -> AddArgs:
    return {
        "wwn": args.wwn,
        "path": args.path,
        "name": args.name,
        "depends_on_id": set(args.depends_on_id),
        "depends_on": set(args.depends_on),
        "logical_sector_range": args.logical_sector_range.strip(),
    }


def get_path_from_args(args: AddArgs) -> Path:
    wwn = args["wwn"]
    path = args["path"]

    if wwn is not None and path is not None:
        raise ValueError("Only one of --wwn or --path can be provided, not both.")

    if path is not None:
        if isinstance(path, str):
            path = Path(path)
        return path
    elif wwn is not None:
        if not wwn.startswith("/dev/disk/by-id/"):
            wwn = os.path.join("/dev/disk/by-id/", wwn)
        return Path(wwn)
    else:
        raise ValueError("Either --wwn or --path must be provided.")


def get_device_dependencies_from_args(dc: DevicesConfig, args: AddArgs) -> set[int]:
    return args["depends_on_id"] | {
        dc.get_device(name=dep).id for dep in args["depends_on"] if dep
    }


def get_logical_block_range_from_args(
    args: AddArgs, sector_size: int, total_sectors: int
) -> tuple[int, int]:
    logical_start_block, logical_end_block = parse_memory_range_to_sectors(
        args["logical_sector_range"], sector_size
    )

    if logical_start_block is None:
        logical_start_block = 0
    if logical_end_block is None:
        logical_end_block = total_sectors

    return logical_start_block, logical_end_block


def add(dc: DevicesConfig, _args: Namespace) -> None:
    """
    Add a new device to the database.
    """
    args = parse_args(_args)
    path: Path = get_path_from_args(args)

    sector_size = get_disk_block_size(resolve_device_name(path))
    total_sectors = get_disk_number_of_blocks(resolve_device_name(path))

    dc.add_device(
        path=path,
        name=args["name"],
        sector_size=sector_size,
        depends_on=get_device_dependencies_from_args(dc, args),
        logical_range=get_logical_block_range_from_args(
            args, sector_size, total_sectors
        ),
    )
