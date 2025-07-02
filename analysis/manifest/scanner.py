# filename: analysis/manifest/scanner.py
"""Simple Android manifest scanner using ADB."""

from __future__ import annotations

import re
from typing import List, Dict

from utils import adb_shell

# Basic list of high-risk permissions for demonstration
SUSPICIOUS_KEYWORDS = [
    "READ_SMS",
    "SEND_SMS",
    "RECEIVE_SMS",
    "WRITE_SMS",
    "READ_PHONE_STATE",
    "WRITE_SETTINGS",
    "SYSTEM_ALERT_WINDOW",
]


def scan_app(serial: str, package: str) -> Dict[str, List[str]]:
    """Return permission info for a single package."""
    print(f"[DEBUG] Scanning permissions for {package} on {serial}")
    output = adb_shell(serial, f"dumpsys package {package}")
    perms = sorted(set(re.findall(r"android.permission.[A-Z_\.]+", output)))
    suspicious = [p for p in perms if any(key in p for key in SUSPICIOUS_KEYWORDS)]
    return {
        "package": package,
        "permissions": perms,
        "suspicious": suspicious,
    }


def scan_packages(serial: str, packages: List[str]) -> List[Dict[str, List[str]]]:
    """Scan multiple packages on a device."""
    print(f"[DEBUG] Beginning scan of {len(packages)} package(s)")
    results = []
    for pkg in packages:
        results.append(scan_app(serial, pkg))
    print("[DEBUG] Package scan complete")
    return results
