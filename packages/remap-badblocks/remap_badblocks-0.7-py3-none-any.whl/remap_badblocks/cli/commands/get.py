from argparse import Namespace
from typing import Iterable, Optional

from remap_badblocks.src.devices.device_config import DeviceConfig
from remap_badblocks.src.devices.devices_config import DevicesConfig


def parse_id_from_args(args: Namespace) -> Optional[int]:
    return args.id


def get_devices_to_print(
    dc: DevicesConfig, id: Optional[int]
) -> Iterable[DeviceConfig]:
    if id is not None:
        return (dc.get_device(id=id),)
    else:
        return dc.get_devices()


def get(dc: DevicesConfig, args: Namespace) -> None:
    """
    Get the configuration of a device from the database.
    """
    id: Optional[int] = parse_id_from_args(args)

    for device in get_devices_to_print(dc, id):
        print(str(device))
