"""Utility helpers to locate the adb executable."""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import List


def get_adb_path() -> str:
    """Return the path to the adb executable.

    This first checks for a bundled binary in ``platform_tools``. If not found,
    it falls back to whatever ``adb`` is available on the system ``PATH``.
    """
    exe = "adb.exe" if os.name == "nt" else "adb"
    bundled = os.path.join("platform_tools", exe)
    if os.path.isfile(bundled):
        return bundled

    found = shutil.which(exe)
    return found or bundled


def run_adb(args: List[str]) -> subprocess.CompletedProcess:
    """Run an adb command and return the CompletedProcess."""
    try:
        return subprocess.run(
            [get_adb_path(), *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as err:
        raise RuntimeError(
            "ADB executable not found. Ensure it is installed or bundled."
        ) from err


def adb_shell(serial: str, cmd: str) -> str:
    """Execute an adb shell command for a specific device."""
    try:
        result = run_adb(["-s", serial, "shell", cmd])
        return result.stdout.strip()
    except (subprocess.CalledProcessError, RuntimeError):
        return "N/A"


def list_packages(serial: str, flags: List[str] | None = None) -> List[str]:
    """Return a list of package names from `pm list packages`."""
    args = ["-s", serial, "shell", "pm", "list", "packages"]
    if flags:
        args.extend(flags)
    try:
        result = run_adb(args)
        return [
            line.replace("package:", "").strip()
            for line in result.stdout.strip().splitlines()
            if line.strip()
        ]
    except (subprocess.CalledProcessError, RuntimeError):
        return []


def list_connected_devices() -> List[str]:
    """Return the serial numbers of all attached devices."""
    try:
        result = run_adb(["devices"])
        lines = result.stdout.strip().splitlines()[1:]
        return [
            line.split()[0]
            for line in lines
            if "device" in line and not line.startswith("*")
        ]
    except (subprocess.CalledProcessError, RuntimeError):
        return []
