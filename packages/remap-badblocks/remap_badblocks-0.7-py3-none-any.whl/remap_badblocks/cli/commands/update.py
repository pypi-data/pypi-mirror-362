from argparse import Namespace
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable, Literal, Optional, TypedDict

from remap_badblocks.src.badblocks._compute_good_ranges import (
    compute_good_ranges, reserve_space_from_good_ranges)
from remap_badblocks.src.badblocks._find_badblocks import (
    get_all_badblocks, read_known_badblocks)
from remap_badblocks.src.badblocks._mapping_generation import generate_mapping
from remap_badblocks.src.badblocks._remap_badblocks import (
    count_used_spare_sectors, iter_all_spare_sectors, iter_free_spare_sectors,
    remap_badblocks, simplify_mapping)
from remap_badblocks.src.devices.device_config import DeviceConfig
from remap_badblocks.src.devices.devices_config import DevicesConfig
from remap_badblocks.src.mapping import Mapping, MappingElement
from remap_badblocks.src.utils._parse_inputs import (
    parse_bytes_to_sectors, parse_memory_number_to_bytes,
    parse_memory_range_to_sectors)
from remap_badblocks.src.utils._run_command import pipe_lines_to_file


class UpdateArgs(TypedDict):
    device_id: Optional[int]
    device_name: Optional[str]
    mode: Literal["read", "write", "skip"]
    output: Optional[Path]
    block_range: str
    spare_space: Optional[str]
    reset_mapping: bool
    external_known_badblocks_file: Optional[Path]


def parse_args(args: Namespace) -> UpdateArgs:
    return {
        "device_id": args.id,
        "device_name": args.name,
        "mode": args.mode,
        "output": args.output,
        "block_range": args.block_range,
        "spare_space": (None if args.spare_space is None else args.spare_space.strip()),
        "reset_mapping": args.reset_mapping,
        "external_known_badblocks_file": args.known_badblocks_file,
    }


def get_device_from_args(args: UpdateArgs, dc: DevicesConfig) -> DeviceConfig:
    if args["device_id"] is None:
        if args["device_name"] is not None:
            return dc.get_device(name=args["device_name"])
        else:
            raise ValueError(
                "Either --id or --name must be provided to update a device in the database."
            )

    return dc.get_device(id=args["device_id"])


def get_update_block_range_from_args(
    args: UpdateArgs, device: DeviceConfig
) -> tuple[int, int]:
    start_block, end_block = parse_memory_range_to_sectors(
        args["block_range"],
        sector_size=device.sector_size,
    )

    if (start_block is not None and start_block < device.logical_range[0]) or (
        end_block is not None and end_block > device.logical_range[1]
    ):
        raise ValueError(
            f"Block range {start_block}-{end_block} must be contained"
            f" within the logical range {device.logical_range[0]}-{device.logical_range[1]}."
        )

    if start_block is None:
        start_block = device.logical_range[0]
    if end_block is None:
        end_block = device.logical_range[1]

    return start_block, end_block


def get_n_spare_sectors_from_args(args: UpdateArgs, device: DeviceConfig) -> int:
    sector_size = device.sector_size

    if args["spare_space"] is None:
        spare_blocks = None
    else:
        spare_blocks = parse_bytes_to_sectors(
            parse_memory_number_to_bytes(args["spare_space"], sector_size=sector_size),
            sector_size,
        )

    if spare_blocks is not None:
        return spare_blocks
    else:
        if device.spare_sectors is None:
            raise ValueError(
                "Should specify spare_sectors the first time you map badblocks"
            )
        return device.spare_sectors


def get_starting_badblocks(args: UpdateArgs, device: DeviceConfig) -> set[int]:
    known_badblocks: set[int] = set(device.badblocks)

    # If known badblocks file is passed, merge it into our known_badblocks
    if args["external_known_badblocks_file"]:
        known_badblocks.update(
            read_known_badblocks(
                known_badblocks_file=args["external_known_badblocks_file"]
            )
        )

    return known_badblocks


def get_current_badblocks(
    args: UpdateArgs,
    known_badblocks: set[int],
    device: DeviceConfig,
    block_range: tuple[int, int],
) -> set[int]:
    if args["mode"] == "skip":
        return known_badblocks

    with NamedTemporaryFile() as known_badblocks_file:
        known_badblocks_file.write("\n".join(map(str, known_badblocks)).encode("utf-8"))
        known_badblocks_file.flush()

        badblocks: set[int] = set(
            get_all_badblocks(
                device.path,
                device.sector_size,
                mode=args["mode"],
                known_badblocks_file=Path(known_badblocks_file.name),
                block_range=block_range,
            )
        )

        if args["output"]:
            pipe_lines_to_file(badblocks, args["output"])

        return badblocks


def update_mapping(
    args: UpdateArgs,
    device: DeviceConfig,
    badblocks: Iterable[int],
    n_spare_sectors: int,
) -> Mapping:
    new_mapping: Iterable[tuple[int, int, int]]

    if (device.mapping is None) or (args["reset_mapping"]):
        good_ranges = compute_good_ranges(
            badblocks, available_range=device.logical_range
        )
        good_ranges = reserve_space_from_good_ranges(good_ranges, n_spare_sectors)
        good_ranges = reserve_space_from_good_ranges(
            good_ranges,
            int(100 * 1024 / device.sector_size),
        )
        new_mapping = generate_mapping(
            good_ranges,
        )
    else:
        spare_sectors = iter_all_spare_sectors(n_spare_sectors, device.logical_range[0])
        n_used_spare_sectors = count_used_spare_sectors(device.mapping, spare_sectors)
        current_mapping = map(lambda x: x.to_tuple(), device.mapping)
        new_mapping = remap_badblocks(
            current_mapping,
            badblocks,
            spare_sectors=iter_free_spare_sectors(spare_sectors, n_used_spare_sectors),
        )

    new_mapping = simplify_mapping(list(new_mapping))
    return Mapping(set(map(MappingElement.from_tuple, new_mapping)))


def update(dc: DevicesConfig, _args: Namespace) -> None:
    """
    Update the mapping of a device in the database.
    """
    args = parse_args(_args)

    device: DeviceConfig = get_device_from_args(args, dc)
    block_range = get_update_block_range_from_args(args, device)
    n_spare_sectors = get_n_spare_sectors_from_args(args, device)

    known_badblocks = get_starting_badblocks(args, device)
    badblocks = get_current_badblocks(args, known_badblocks, device, block_range)

    print(
        f"Badblocks computed. Badblocks went from {len(known_badblocks)} to {len(badblocks)}."
    )

    dc.update_device(
        id=device.id,
        badblocks=badblocks,
    )

    print("Badblocks list updated.")

    new_mapping = update_mapping(args, device, badblocks, n_spare_sectors)
    dc.update_device(id=device.id, mapping=new_mapping, spare_sectors=n_spare_sectors)

    print("Mapping updated.")
