# filename: analysis/device_enumeration.py

from analysis.device import device_info_fetcher
from models.device_info import DeviceInfo
from utils import display_utils
from typing import List


def enumerate_connected_devices() -> List[DeviceInfo]:
    """
    Detect and return a list of connected Android devices using ADB.

    Returns:
        List[DeviceInfo]: Parsed device metadata for all connected devices.
    """
    return device_info_fetcher.fetch_all_device_info()


def display_enumerated_devices(devices: List[DeviceInfo]) -> None:
    """
    Display a table of connected Android devices.

    Args:
        devices (List[DeviceInfo]): Devices to display.
    """
    if not devices:
        display_utils.print_warning("No devices connected.")
        return

    display_utils.print_title("Connected Devices")
    display_utils.print_device_table(devices)


def enumerate_and_display_devices() -> List[DeviceInfo]:
    """
    Full pipeline to enumerate and display connected Android devices.

    Returns:
        List[DeviceInfo]: Devices detected and displayed.
    """
    devices = enumerate_connected_devices()
    display_enumerated_devices(devices)
    return devices
