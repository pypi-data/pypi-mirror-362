from argparse import Namespace
from typing import Optional, TypedDict

from remap_badblocks.src.devices.devices_config import DevicesConfig


class RemoveArgs(TypedDict):
    id: Optional[int]
    name: Optional[str]


def parse_args(args: Namespace) -> RemoveArgs:
    return {
        "id": args.id,
        "name": args.name,
    }


def get_device_id_from_args(dc: DevicesConfig, args: RemoveArgs) -> int:
    id: Optional[int] = args["id"]
    name: Optional[str] = args["name"]

    if id is not None and name is not None:
        raise ValueError(
            "Only one of --id or --name can be provided to remove a device from the database."
        )
    elif id is None and name is None:
        raise ValueError(
            "Either --id or --name must be provided to remove a device from the database."
        )
    elif id is not None:
        return id
    else:
        assert name is not None
        return dc.get_device(name=name).id


def remove(dc: DevicesConfig, _args: Namespace) -> None:
    """
    Remove the configuration of a device from the database.
    """
    args = parse_args(_args)
    id = get_device_id_from_args(dc, args)

    dc.remove_device(id)
