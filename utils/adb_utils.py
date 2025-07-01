"""Utility helpers to locate the adb executable."""

from __future__ import annotations

import os
import shutil


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

