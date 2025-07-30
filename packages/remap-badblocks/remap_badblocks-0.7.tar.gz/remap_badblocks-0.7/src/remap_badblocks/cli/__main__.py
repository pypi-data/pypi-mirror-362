from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from remap_badblocks.cli.commands import (add, apply, get, remove, update,
                                          version)
from remap_badblocks.src.devices.devices_config import DevicesConfig
from remap_badblocks.src.devices_config_constants import \
    DEFAULT_DEVICES_CONFIG_PATH

argparse = ArgumentParser(
    description="Badblocks remapper for block devices.",
)

argparse.add_argument(
    "-P",
    "--db-path",
    type=Path,
    default=DEFAULT_DEVICES_CONFIG_PATH,
    help="Path to the devices configuration database.",
)

subparser = argparse.add_subparsers(
    title="Actions",
    description="Available actions for the badblocks remapper.",
    dest="action",
    help="Action to perform",
    required=True,
)

add_new_device_parser = subparser.add_parser(
    "add",
    help="Add a new device to the database.",
)

add_new_device_parser.add_argument(
    "name", type=str, help="The name of the output device."
)
add_new_device_parser.add_argument(
    "--wwn",
    type=str,
    help="The WWN of the device to add.",
)
add_new_device_parser.add_argument(
    "--path",
    type=Path,
    help="The path to the device to add.",
)
add_new_device_parser.add_argument(
    "--depends-on",
    type=str,
    default=[],
    action="append",
    help=(
        "The name of a device that this device depends on. Can be specified multiple times to add multiple"
        " dependencies. This is used to ensure that devices are applied in the correct order."
    ),
)
add_new_device_parser.add_argument(
    "--depends-on-id",
    type=int,
    default=[],
    action="append",
    help=(
        "The ID of a device that this device depends on. Can be specified multiple times to add multiple"
        " dependencies. This is used to ensure that devices are applied in the correct order."
    ),
)
add_new_device_parser.add_argument(
    "--logical-sector-range",
    type=str,
    default="-",
    help=(
        "Logical sector range to assign to the device. Format: 'start-end', where 'end' can be omitted to mean"
        " 'till the end of the device'. Both start and end can be specified as sector numbers or as byte offsets."
        " In case of byte offsets, they must be multiples of the sector size. If not specified, the whole device"
        " will be used. Note that end is not included in the range."
    ),
)


get_devices_parser = subparser.add_parser(
    "get",
    help="Get the existing device(s) in the database.",
)
get_devices_parser.add_argument(
    "--id",
    type=int,
    default=None,
    help="The ID of the device to get. If neither --id or --name are provided, all devices will be returned.",
)
get_devices_parser.add_argument(
    "--name",
    type=str,
    default=None,
    help="The name of the device to get. If neither --id or --name are provided, all devices will be returned.",
)

remove_devices_parser = subparser.add_parser(
    "remove",
    help="Remove an existing device in the database.",
)
remove_devices_parser.add_argument(
    "--id",
    type=int,
    default=None,
    help="The ID of the device to remove. If neither --id or --name are provided, an error will be raised.",
)
remove_devices_parser.add_argument(
    "--name",
    type=str,
    default=None,
    help="The name of the device to remove. If neither --id or --name are provided, an error will be raised.",
)

update_mapping_parser = subparser.add_parser(
    "update",
    help=(
        "Update the mapping of a device in the database. More specifically: compute/update the device's badblocks and"
        " store them in the database, compute the new mapping of a device; if the mapping has changed, the user will"
        " be prompted to confirm the changes."
    ),
)
update_mapping_parser.add_argument(
    "--id",
    type=int,
    default=None,
    help="The ID of the device to update.",
)
update_mapping_parser.add_argument(
    "--name",
    type=str,
    default=None,
    help="The name of the device to update.",
)
update_mapping_parser.add_argument(
    "--mode",
    type=str,
    choices=["read", "write", "skip"],
    default="read",
    help="Mode for computing badblocks",
)
update_mapping_parser.add_argument(
    "--known-badblocks-file",
    type=Path,
    default=None,
    help=(
        "Path to file with known badblocks (a sector number for each line) that will be merged to those found so far."
        " Take care the sector size is the same as configured into remap_badblocks"
    ),
)
update_mapping_parser.add_argument(
    "--block-range",
    type=str,
    help=(
        "Block range to check (e.g., 0-1000, or 1573-), omitted start and end means the whole logical range. Note"
        " that the end is not included in the range"
    ),
    default="-",
)
update_mapping_parser.add_argument(
    "--output",
    type=Path,
    default=None,
    help="Badblocks are stored internally. If provided, they will also be copied to this file.",
)
update_mapping_parser.add_argument(
    "--spare-space",
    type=str,
    default=None,
    help="Number of spare sectors to reserve from the good ranges. Cannot be changed after first time",
)
update_mapping_parser.add_argument(
    "--reset-mapping",
    action="store_true",
    help=(
        "If specified, will ignore existing mapping and build a new mapping from scratch."
        " DANGER: this might lead to data loss, handle with care"
    ),
)

apply_devices_parser = subparser.add_parser(
    "apply",
    help="Apply a remapping that's already existing in the database.",
)
apply_devices_parser.add_argument(
    "--id",
    type=int,
    default=None,
    help="The ID of the device to apply. If neither --id or --name are provided, all devices will be applied.",
)
apply_devices_parser.add_argument(
    "--name",
    type=str,
    default=None,
    help="The name of the device to apply. If neither --id or --name are provided, all devices will be applied.",
)
apply_devices_parser.add_argument(
    "--method",
    type=str,
    default="device-mapper",
    choices=["device-mapper"],
    help="Method to apply the mapping. Only device-mapper is available",
)

version_parser = subparser.add_parser("version")


def main() -> None:
    args = argparse.parse_args()
    db_path: Path = args.db_path

    actions: dict[str, Callable[[DevicesConfig, Namespace], None]] = {
        "add": add,
        "apply": apply,
        "get": get,
        "remove": remove,
        "update": update,
    }

    static_actions: dict[str, Callable[[], None]] = {
        "version": version,
    }

    if args.action in actions:
        if db_path.is_dir():
            raise ValueError("The provided path must not be a directory.")
        devices_config = DevicesConfig(db_path)
        actions[args.action](devices_config, args)
    elif args.action in static_actions:
        static_actions[args.action]()
    else:
        raise ValueError(
            f"Unknown action: {args.action}. Please use one of {tuple(actions.keys()) + tuple(static_actions.keys())}."
        )


if __name__ == "__main__":
    main()
