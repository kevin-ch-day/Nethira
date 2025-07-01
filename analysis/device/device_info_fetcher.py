# analysis/device_info_fetcher.py

from models.device_info import DeviceInfo
from utils import adb_shell, list_connected_devices


def get_connected_devices() -> list[str]:
    """Returns a list of serial numbers for currently connected ADB devices."""
    return list_connected_devices()




def get_device_info(serial: str) -> DeviceInfo:
    """Gathers detailed information for a specific connected device."""
    return DeviceInfo(
        serial=serial,
        model=adb_shell(serial, "getprop ro.product.model"),
        manufacturer=adb_shell(serial, "getprop ro.product.manufacturer"),
        android_version=adb_shell(serial, "getprop ro.build.version.release"),
        sdk_version=adb_shell(serial, "getprop ro.build.version.sdk"),
        device_name=adb_shell(serial, "getprop ro.product.device"),
        build_number=adb_shell(serial, "getprop ro.build.display.id"),
        security_patch=adb_shell(serial, "getprop ro.build.version.security_patch"),
        fingerprint=adb_shell(serial, "getprop ro.build.fingerprint"),
        bootloader=adb_shell(serial, "getprop ro.bootloader"),
        cpu_abi=adb_shell(serial, "getprop ro.product.cpu.abi"),
    )


def fetch_all_device_info() -> list[DeviceInfo]:
    """Returns a list of DeviceInfo objects for all connected devices."""
    serials = get_connected_devices()
    return [get_device_info(serial) for serial in serials]
