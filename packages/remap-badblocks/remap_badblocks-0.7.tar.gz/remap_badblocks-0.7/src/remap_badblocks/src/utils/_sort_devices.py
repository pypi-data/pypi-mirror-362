from typing import Collection, Iterable

from remap_badblocks.src.devices.devices_config import DeviceConfig


def sort_devices_by_dependencies(
    devices: Collection[DeviceConfig],
    already_applied_devices: Iterable[DeviceConfig] = set(),
) -> Iterable[DeviceConfig]:
    devices = list(devices)
    sorted_devices: list[DeviceConfig] = []
    already_sorted_ids: set[int] = set(map(lambda x: x.id, already_applied_devices))

    while devices:
        for device in devices:
            if all(dep in already_sorted_ids for dep in device.depends_on):
                sorted_devices.append(device)
                already_sorted_ids.add(device.id)
                devices.remove(device)
                break
        else:
            raise ValueError(
                "Circular dependency detected or no device can be applied."
            )

    return sorted_devices
