"""Functions for retrieving manifest and signing info from APKs."""

from __future__ import annotations

from typing import Dict, Optional

from utils import apk_utils, hash_utils


def get_manifest_bytes(apk_path: str) -> Optional[bytes]:
    """Return the raw manifest bytes from the APK."""
    print(f"[manifest_info] get_manifest_bytes: {apk_path}")
    data = apk_utils.extract_manifest(apk_path)
    if data:
        print(f"[manifest_info] Retrieved {len(data)} bytes")
    else:
        print("[manifest_info] No manifest bytes found")
    return data


def get_manifest_xml(apk_path: str) -> Optional[str]:
    """Return the decoded manifest XML string."""
    print(f"[manifest_info] get_manifest_xml: {apk_path}")
    xml = apk_utils.extract_manifest_xml(apk_path)
    if xml:
        print(f"[manifest_info] XML length: {len(xml)}")
    else:
        print("[manifest_info] XML not found")
    return xml


def get_certificate_fingerprints(apk_path: str) -> Dict[str, str]:
    """Return SHA-256, SHA-1 and MD5 fingerprints for the APK certificate."""
    print(f"[manifest_info] get_certificate_fingerprints: {apk_path}")
    cert = apk_utils.extract_certificate(apk_path)
    if not cert:
        print("[manifest_info] Certificate not found")
        return {}
    fingerprints = {
        "sha256": hash_utils.sha256_digest(cert),
        "sha1": hash_utils.sha1_digest(cert),
        "md5": hash_utils.md5_digest(cert),
    }
    print(f"[manifest_info] Fingerprints: {fingerprints}")
    return fingerprints

