from argparse import Namespace
from pathlib import Path
from typing import Iterable, Literal, Optional, TypedDict

from remap_badblocks.src.devices.device_config import DeviceConfig
from remap_badblocks.src.devices.devices_config import DevicesConfig
from remap_badblocks.src.mapping import Mapping
from remap_badblocks.src.remappers._check_applied_devices import \
    filter_applied_devices
from remap_badblocks.src.remappers._generate_dm_table import generate_dm_table
from remap_badblocks.src.utils._run_command import run_command_realtime
from remap_badblocks.src.utils._sort_devices import \
    sort_devices_by_dependencies


class ApplyArgs(TypedDict):
    device_id: Optional[int]
    device_name: Optional[str]
    method: Literal["device-mapper"]


def parse_args(args: Namespace) -> ApplyArgs:
    return {
        "device_id": args.id,
        "device_name": args.name,
        "method": args.method,
    }


def get_user_wanted_device_list(
    dc: DevicesConfig, args: ApplyArgs
) -> Iterable[DeviceConfig]:
    if args["device_id"] is not None:
        return [dc.get_device(id=args["device_id"])]
    elif args["device_name"] is not None:
        return [dc.get_device(name=args["device_name"])]
    else:
        return dc.get_devices()


def plan_apply_devices(
    dc: DevicesConfig, devices: Iterable[DeviceConfig]
) -> Iterable[DeviceConfig]:
    already_applied_devices = set(filter_applied_devices(dc.get_devices()))
    return sort_devices_by_dependencies(
        list(devices), already_applied_devices=already_applied_devices
    )


def apply_device_mapper(device: DeviceConfig):
    mapping: Optional[Mapping] = device.mapping
    sector_size: int = device.sector_size
    device_path: Path = device.path

    assert mapping is not None, "Call ‘remap_badblocks update‘ before applying"

    device_dmtable_identifier = device_path

    dmtable = "\n".join(
        generate_dm_table(device_dmtable_identifier, mapping, sector_size)
    )

    for _ in run_command_realtime(["dmsetup", "create", device.name], stdin=dmtable):
        pass


def apply(dc: DevicesConfig, _args: Namespace):
    args = parse_args(_args)

    devices: Iterable[DeviceConfig] = get_user_wanted_device_list(dc, args)
    devices = plan_apply_devices(dc, devices)

    # TODO: remove already applied devices

    method = args["method"]
    assert (
        method == "device-mapper"
    ), f"Only ‘device-mapper‘ method is available, found ‘{method}‘"

    for device in devices:
        apply_device_mapper(device)
