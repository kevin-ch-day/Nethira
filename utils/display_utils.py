# filename: utils/display_utils.py

import os
import sys
import subprocess
from typing import List, Mapping

from models.device_info import DeviceInfo


def detect_color_support() -> bool:
    """Return True if colored output should be used."""
    if os.getenv("FORCE_COLOR"):
        return True
    if os.getenv("NO_COLOR"):
        return False
    return sys.stdout.isatty() and os.getenv("TERM") != "dumb"


USE_COLORS = detect_color_support()
_RED = "\033[91m"
_YELLOW = "\033[93m"
_GREEN = "\033[92m"
_RESET = "\033[0m"


def _color(text: str, code: str) -> str:
    return f"{code}{text}{_RESET}" if USE_COLORS else text


def set_color_enabled(enabled: bool) -> None:
    """Toggle colored output at runtime."""
    global USE_COLORS
    USE_COLORS = enabled


def strip_ansi(text: str) -> str:
    """Remove ANSI color codes from a string."""
    import re

    ansi_re = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_re.sub("", text)


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
        print_warning("No devices to display.")
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


def format_key_values(data: Mapping[str, str]) -> str:
    """Return key-value pairs formatted as aligned lines."""
    if not data:
        return ""
    width = max(len(key) for key in data)
    return "\n".join(f"{key:<{width}} : {value}" for key, value in data.items())


def print_key_values(title: str, data: Mapping[str, str]) -> None:
    """Print a titled block of key-value pairs uniformly."""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    if data:
        print(format_key_values(data))
    else:
        print("<no data>")
    print("=" * 60)
    print()


def print_title(title: str) -> None:
    """Print a formatted section title."""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_error(msg: str) -> None:
    """Display an error message in red if colors are enabled."""
    print(_color(f"[ERROR] {msg}", _RED))


def print_warning(msg: str) -> None:
    """Display a warning message in yellow if colors are enabled."""
    print(_color(f"[WARN ] {msg}", _YELLOW))


def print_success(msg: str) -> None:
    """Display a success message in green if colors are enabled."""
    print(_color(f"[ OK  ] {msg}", _GREEN))


def print_info(msg: str) -> None:
    """Display an informational message without coloring."""
    print(f"[INFO ] {msg}")
