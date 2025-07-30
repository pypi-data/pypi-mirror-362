import os
import re
from pathlib import Path


def resolve_device_name(device: Path) -> str:
    resolved = device.resolve()
    if not resolved.is_block_device():
        raise ValueError(f"{device} is not a valid block device.")
    _resolved = str(resolved)
    m = re.match(r"^/dev/([a-zA-Z0-9\-]+)$", _resolved)
    if not m:
        raise RuntimeError(f"Could not parse '{_resolved}'.")
    return m.group(1)


def get_disk_block_size(device_name: str) -> int:
    """Get the block size of the disk."""
    path = os.path.join("/sys/block/", device_name, "queue/physical_block_size")
    try:
        with open(path, "r") as f:
            block_size = f.read()
            return int(block_size.strip())
    except Exception as e:
        raise RuntimeError(f"Could not read block size for {device_name}: {e}") from e


def get_disk_number_of_blocks(device_name: str) -> int:
    """Get the number of blocks on the disk."""
    block_size = get_disk_block_size(device_name)
    path = os.path.join("/sys/block/", device_name, "size")
    try:
        with open(path, "r") as f:
            txt = f.read()
        size_in_blocks = int(txt.strip()) * 512 / block_size
        assert (
            size_in_blocks.is_integer()
        ), f"Size in blocks is not an integer: {size_in_blocks}"
        return int(size_in_blocks)
    except Exception as e:
        raise RuntimeError(
            f"Could not read size in physical blocks for {device_name}: {e}"
        ) from e
