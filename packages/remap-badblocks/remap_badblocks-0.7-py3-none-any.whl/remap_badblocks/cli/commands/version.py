import os
from tomllib import load


def get_version() -> str:

    pyproject = os.path.join(
        os.path.dirname(os.path.abspath(__name__)), "pyproject.toml"
    )
    with open(pyproject, "rb") as f:
        return load(f)["project"]["version"]


def version():
    print(f"remap-badblocks version v{get_version()}")
