from typing import Iterable, Optional, Union


class DeviceNotFoundError(KeyError):
    def __init__(
        self,
        *,
        device_id: Optional[Union[int, Iterable[int]]] = None,
        device_name: Optional[Union[str, Iterable[str]]] = None,
    ) -> None:
        if device_id is not None and device_name is not None:
            raise ValueError("Only one of device_id or device_name can be provided.")
        if device_id is not None:
            message = f"Device(s) with id(s) {device_id} does not exist."
            args = (message,)
        elif device_name is not None:
            message = f"Device(s) with name(s) '{device_name}' does not exist."
            args = (message,)
        else:
            message = "Device(s) not found."
            args = (message,)
        super().__init__(*args)
