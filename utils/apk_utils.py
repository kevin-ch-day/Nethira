"""Helpers for working with APK files."""

from __future__ import annotations

import os
import zipfile
from typing import Optional

try:
    from apkutils2 import AXML
except Exception:  # pragma: no cover - apkutils2 may not be installed
    AXML = None


def extract_manifest(apk_path: str) -> Optional[bytes]:
    """Return the raw AndroidManifest.xml from the APK or ``None`` if missing."""
    print(f"[apk_utils] extract_manifest: {apk_path}")
    if not os.path.isfile(apk_path):
        print("[apk_utils] File not found")
        return None
    try:
        with zipfile.ZipFile(apk_path, "r") as z:
            with z.open("AndroidManifest.xml") as f:
                data = f.read()
                print(f"[apk_utils] Manifest size: {len(data)} bytes")
                return data
    except Exception as e:
        print(f"[apk_utils] Failed to extract manifest: {e}")
        return None


def extract_certificate(apk_path: str) -> Optional[bytes]:
    """Return the first certificate file from ``META-INF`` or ``None``."""
    print(f"[apk_utils] extract_certificate: {apk_path}")
    if not os.path.isfile(apk_path):
        print("[apk_utils] File not found")
        return None
    try:
        with zipfile.ZipFile(apk_path, "r") as z:
            for name in z.namelist():
                lower = name.lower()
                if lower.startswith("meta-inf/") and lower.endswith((".rsa", ".dsa", ".ec")):
                    with z.open(name) as f:
                        data = f.read()
                        print(f"[apk_utils] Certificate {name} size: {len(data)} bytes")
                        return data
    except Exception as e:
        print(f"[apk_utils] Failed to extract certificate: {e}")
        return None
    print("[apk_utils] Certificate not found")
    return None


def extract_manifest_xml(apk_path: str) -> Optional[str]:
    """Return the decoded manifest XML string or ``None`` if unavailable."""
    print(f"[apk_utils] extract_manifest_xml: {apk_path}")
    raw = extract_manifest(apk_path)
    if not raw:
        print("[apk_utils] No manifest bytes extracted")
        return None
    if AXML is None:
        print("[apk_utils] apkutils2.AXML is unavailable")
        return None
    try:
        xml = AXML(raw).get_xml()
        print(f"[apk_utils] Decoded manifest XML length: {len(xml)}")
        return xml
    except Exception as e:
        print(f"[apk_utils] Failed to decode manifest XML: {e}")
        return None
