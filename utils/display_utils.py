# filename: utils/display_utils.py

import os
import subprocess
from typing import List

from models.device_info import DeviceInfo


def clear_screen() -> None:
    """Clear the terminal without invoking the shell."""
    try:
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"], check=False)
        else:
            subprocess.run(["clear"], check=False)
    except Exception:
        print("\033c", end="")


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

    header_format = (
        "{:<3} {:<16} {:<20} {:<12} {:<13} {:<9} {:<12} {:<10}"
    )
    row_format = header_format

    print(
        header_format.format(
            "No",
            "Serial",
            "Model",
            "Manufacturer",
            "Android Ver",
            "SDK",
            "Build No",
            "Security",
        )
    )
    print("-" * 100)

    for idx, device in enumerate(devices_info, start=1):
        print(row_format.format(
            idx,
            device.serial,
            device.model[:24],
            device.manufacturer[:14],
            device.android_version,
            device.sdk_version,
            device.build_number[:11],
            device.security_patch[:9]
        ))

    print()


def print_device_details(device: DeviceInfo) -> None:
    """Display all available fields for a single device."""
    print("=" * 60)
    print(f"  DETAILS FOR DEVICE: {device.model} ({device.serial})")
    print("=" * 60)
    print(device)
    print("=" * 60)
    print()
