from typing import Iterable

from remap_badblocks.src.devices.device_config import DeviceConfig


def filter_applied_devices(devices: Iterable[DeviceConfig]):
    def check_applied(device: DeviceConfig) -> bool:
        return device.get_applied_path().is_block_device()

    return filter(check_applied, devices)
