import random

import pytest

from remap_badblocks.src.devices.devices_config import DeviceConfig
from remap_badblocks.src.utils._sort_devices import \
    sort_devices_by_dependencies

DEVICES_SAMPLE = [
    DeviceConfig(
        id=1,
        depends_on=[],
        name="dev1",
        path="/dev/sda",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=2,
        depends_on=[3],
        name="dev2",
        path="/dev/sdb",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=3,
        depends_on=[1],
        name="dev3",
        path="/dev/sdc",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=3,
        depends_on=[1, 2, 3],
        name="dev4",
        path="/dev/sdd",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
]

DEVICES_SAMPLE_NO_DEPS = [
    DeviceConfig(
        id=1,
        depends_on=[],
        name="dev1",
        path="/dev/sda",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=2,
        depends_on=[],
        name="dev2",
        path="/dev/sdb",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=3,
        depends_on=[],
        name="dev3",
        path="/dev/sdc",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=3,
        depends_on=[],
        name="dev4",
        path="/dev/sdd",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
]

DEVICES_SAMPLE_CIRCULAR_DEP = [
    DeviceConfig(
        id=1,
        depends_on=[],
        name="dev1",
        path="/dev/sda",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=2,
        depends_on=[3],
        name="dev2",
        path="/dev/sdb",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=3,
        depends_on=[2],
        name="dev3",
        path="/dev/sdc",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
    DeviceConfig(
        id=4,
        depends_on=[],
        name="dev4",
        path="/dev/sdd",
        sector_size=512,
        badblocks=[],
        logical_range=(0, 1000),
    ),
]


def test_sort_devices__empty_input():
    devices: list[DeviceConfig] = []
    sorted_devices = list(sort_devices_by_dependencies(devices))
    assert sorted_devices == []


def test_sort_devices__single_device():
    devices = DEVICES_SAMPLE[:1]
    sorted_devices = list(sort_devices_by_dependencies(devices))
    assert sorted_devices == devices


def test_sort_devices__no_dependencies():
    sorted_devices = list(sort_devices_by_dependencies(DEVICES_SAMPLE_NO_DEPS))
    for dev in DEVICES_SAMPLE_NO_DEPS:
        assert dev in sorted_devices
    assert len(sorted_devices) == len(DEVICES_SAMPLE_NO_DEPS)


def test_sort_devices__circular_dependency():
    with pytest.raises(ValueError, match=r"[Cc]ircular [Dd]ependency"):
        list(sort_devices_by_dependencies(DEVICES_SAMPLE_CIRCULAR_DEP))


@pytest.mark.parametrize(
    "seed",
    range(10),
)
def test_sort_devices(seed: int):
    random.seed(seed)
    CURRENT_SAMPLE = DEVICES_SAMPLE.copy()
    random.shuffle(CURRENT_SAMPLE)

    sorted_devices = list(sort_devices_by_dependencies(CURRENT_SAMPLE))

    # Check that all devices are present
    for dev in CURRENT_SAMPLE:
        assert dev in sorted_devices

    # Check that dependencies are respected
    already_there_ids: set[int] = set()

    for dev in sorted_devices:
        assert set(dev.depends_on).issubset(already_there_ids)
        already_there_ids.add(dev.id)
