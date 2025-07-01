# analysis/device_info_fetcher.py

import subprocess
import os
from models.device_info import DeviceInfo

ADB_PATH = os.path.join("platform_tools", "adb.exe")


def get_connected_devices() -> list[str]:
    """Returns a list of serial numbers for currently connected ADB devices."""
    try:
        result = subprocess.run(
            [ADB_PATH, "devices"],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().splitlines()[1:]  # Skip the header
        return [
            line.split()[0]
            for line in lines
            if "device" in line and not line.startswith("*")
        ]
    except subprocess.CalledProcessError:
        return []


def adb_shell(serial: str, cmd: str) -> str:
    """Runs an ADB shell command for a specific device serial."""
    try:
        result = subprocess.run(
            [ADB_PATH, "-s", serial, "shell", cmd],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "N/A"


def get_device_info(serial: str) -> DeviceInfo:
    """Gathers detailed information for a specific connected device."""
    return DeviceInfo(
        serial=serial,
        model=adb_shell(serial, "getprop ro.product.model"),
        manufacturer=adb_shell(serial, "getprop ro.product.manufacturer"),
        android_version=adb_shell(serial, "getprop ro.build.version.release"),
        sdk_version=adb_shell(serial, "getprop ro.build.version.sdk"),
        device_name=adb_shell(serial, "getprop ro.product.device"),
    )


def fetch_all_device_info() -> list[DeviceInfo]:
    """Returns a list of DeviceInfo objects for all connected devices."""
    serials = get_connected_devices()
    return [get_device_info(serial) for serial in serials]

