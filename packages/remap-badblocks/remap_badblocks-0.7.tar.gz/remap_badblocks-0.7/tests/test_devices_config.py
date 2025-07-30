from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable, Optional

import pytest

from remap_badblocks.src.devices.devices_config import DevicesConfig
from remap_badblocks.src.mapping import Mapping, MappingElement
from remap_badblocks.src.utils._iterable_bytes_converter import (
    iterable_from_bytes, iterable_to_bytes)

BADBLOCKS_SAMPLES: list[Optional[set[int]]] = [
    None,
    set(),
    {1, 2, 3},
    {100, 200, 300},
    {
        0,
        10 * (1024**3) * 2,
    },  # Edge cases for memory limits (test 10TB badblock for 512-bytes block size)
]


@pytest.mark.parametrize(
    "start_id_virtual, start_id_real, length",
    [
        (0, 0, 0),
        (1, 2, 3),
        (12345678, 87654321, 1000),
        (4294967295, 4294967295, 4294967295),
    ],
)
def test_mapping_element_bytes(start_id_virtual: int, start_id_real: int, length: int):
    """
    Test the conversion of MappingElement to and from bytes.
    """
    element = MappingElement(start_id_virtual, start_id_real, length)
    data = bytes(element)
    restored_element = MappingElement.from_bytes(data)

    assert restored_element.start_id_virtual == start_id_virtual
    assert restored_element.start_id_real == start_id_real
    assert restored_element.length == length
    assert isinstance(data, bytes)
    assert len(data) == MappingElement.BYTES_LENGTH


@pytest.mark.parametrize(
    "elements",
    [
        [MappingElement(0, 0, 0)],
        [MappingElement(1, 2, 3), MappingElement(4, 5, 6)],
        [MappingElement(12345678, 87654321, 1000)],
        [MappingElement(4294967295, 4294967295, 4294967295)],
    ],
)
def test_mapping_bytes(elements: list[MappingElement]):
    """
    Test the conversion of Mapping to and from bytes.
    """
    mapping = Mapping(elements)
    data = bytes(mapping)
    restored_mapping = Mapping.from_bytes(data)

    original_elements = set(mapping.elements)
    restored_elements = set(restored_mapping.elements)

    assert original_elements == restored_elements
    assert isinstance(data, bytes)
    assert isinstance(restored_mapping, Mapping)
    assert len(data) % MappingElement.BYTES_LENGTH == 0


def test_devices_config_init():
    """
    Test the initialization of DevicesConfig with an empty database.
    """
    with NamedTemporaryFile() as temp_db:
        devices_config = DevicesConfig(path=temp_db.name)
        assert devices_config.get_devices() == []

        with pytest.raises(KeyError):
            devices_config.get_device(id=1)

        assert len(devices_config) == 0


@pytest.mark.parametrize(
    "length",
    [4, 8, 16],
)
@pytest.mark.parametrize(
    "iterable",
    [
        [],
        [1, 2, 3],
        {100, 400, 600},
    ],
)
def test_iterable_to_bytes(length: int, iterable: Iterable[int]):
    assert set(iterable) == set(
        iterable_from_bytes(iterable_to_bytes(iterable, length=length), length=length)
    )


@pytest.mark.parametrize(
    "sector_size",
    [512, 1024, 2048],
)
@pytest.mark.parametrize(
    "badblocks",
    BADBLOCKS_SAMPLES,
)
def test_devices_config_add_device(badblocks: Optional[set[int]], sector_size: int):
    """
    Test adding a device to DevicesConfig.
    """
    with NamedTemporaryFile() as temp_block_file:
        with NamedTemporaryFile() as temp_db:
            devices_config = DevicesConfig(path=temp_db.name)

            if badblocks is None:
                devices_config.add_device(
                    name="name1",
                    path=temp_block_file.name,
                    sector_size=sector_size,
                    logical_range=(0, int(1e10)),
                )
            else:
                devices_config.add_device(
                    name="name1",
                    path=temp_block_file.name,
                    badblocks=badblocks,
                    sector_size=sector_size,
                    logical_range=(0, int(1e10)),
                )

            assert len(devices_config) == 1

            devices = list(devices_config.get_devices())

            device = devices[0]
            assert device.path == Path(temp_block_file.name)
            if badblocks is not None:
                assert len(device.badblocks) == len(badblocks)
                assert set(device.badblocks) == set(badblocks)
            assert device.mapping is None

            devices_config.add_device(
                name="name2",
                path=temp_block_file.name,
                sector_size=sector_size,
                logical_range=(0, int(1e10)),
            )

            assert len(devices_config) == 2

            with pytest.raises(Exception):
                devices_config.add_device(
                    name="name2",
                    path=temp_block_file.name,
                    sector_size=sector_size,
                    logical_range=(0, int(1e10)),
                )


@pytest.mark.parametrize(
    "sector_size",
    [512, 1024, 2048],
)
def test_devices_config_remove_device(sector_size: int):
    """
    Test removing a device from DevicesConfig.
    """
    with NamedTemporaryFile() as temp_block_file:
        with NamedTemporaryFile() as temp_db:
            devices_config = DevicesConfig(path=temp_db.name)

            devices_config.add_device(
                name="name1",
                path=temp_block_file.name,
                sector_size=sector_size,
                logical_range=(0, int(1e10)),
            )
            devices_config.add_device(
                name="name2",
                path=temp_block_file.name,
                sector_size=sector_size,
                logical_range=(0, int(1e10)),
            )
            assert len(devices_config) == 2

            devices = list(devices_config.get_devices())
            device_to_remove_id = devices[0].id
            device_to_keep_id = devices[1].id

            assert device_to_remove_id != device_to_keep_id

            devices_config.remove_device(id=device_to_remove_id)
            assert len(devices_config) == 1

            with pytest.raises(KeyError):
                devices_config.get_device(id=device_to_remove_id)

            devices_config.get_device(id=device_to_keep_id)


def test_devices_config_update_device():
    """
    Test updating a device in DevicesConfig.
    """
    with (
        NamedTemporaryFile() as temp_block_file1,
        NamedTemporaryFile() as temp_block_file2,
    ):
        with NamedTemporaryFile() as temp_db:
            devices_config = DevicesConfig(path=temp_db.name)

            devices_config.add_device(
                name="name",
                path=temp_block_file1.name,
                sector_size=512,
                logical_range=(0, int(1e10)),
            )
            assert len(devices_config) == 1

            devices = list(devices_config.get_devices())
            device_id = devices[0].id

            new_path = Path(temp_block_file2.name)
            devices_config.update_device(id=device_id, path=new_path)

            updated_device = devices_config.get_device(id=device_id)
            assert updated_device.path == new_path

            new_badblocks = {1, 2, 3}
            devices_config.update_device(id=device_id, badblocks=new_badblocks)

            updated_device = devices_config.get_device(id=device_id)
            assert set(updated_device.badblocks) == new_badblocks
