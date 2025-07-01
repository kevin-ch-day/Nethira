# filename: utils/display_utils.py

import os
from typing import List
from nethira.models.device_info import DeviceInfo

def clear_screen():
    """
    Clears the terminal screen based on the operating system.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """
    Displays the Nethira banner header with a clean border.
    """
    clear_screen()
    banner_width = 60
    print("=" * banner_width)
    print("               NETHIRA - Android Recon Toolkit")
    print("=" * banner_width)
    print()


def print_device_table(devices_info: List[DeviceInfo]):
    """
    Displays a formatted table of connected Android devices.

    Args:
        devices_info (List[DeviceInfo]): List of connected device info objects.
    """
    if not devices_info:
        print("[*] No devices to display.\n")
        return

    header_format = "{:<3} {:<16} {:<25} {:<15} {:<13} {:<9} {:<15}"
    row_format = header_format

    print(header_format.format(
        "No", "Serial", "Model", "Manufacturer", "Android Ver", "SDK", "Device Name"
    ))
    print("-" * 100)

    for idx, device in enumerate(devices_info, start=1):
        print(row_format.format(
            idx,
            device.serial,
            device.model[:24],
            device.manufacturer[:14],
            device.android_version,
            device.sdk_version,
            device.device_name[:14]
        ))

    print()
