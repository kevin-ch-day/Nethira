"""Parse AndroidManifest.xml from an APK."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import apkutils2


class ManifestAnalyzer:
    """Extract and parse manifest information."""

    def parse(self, apk_path: str) -> apkutils2.Manifest | None:
        """Return a ``Manifest`` object for ``apk_path`` if possible."""
        if not os.path.isfile(apk_path):
            print(f"[ManifestAnalyzer] APK not found: {apk_path}")
            return None
        try:
            print(f"[ManifestAnalyzer] Parsing manifest from {apk_path}")
            apk = apkutils2.APK(apk_path)
            xml = apk.get_org_manifest()
            if not xml:
                print("[ManifestAnalyzer] get_org_manifest returned no data")
                return None
            return apkutils2.Manifest(xml)
        except Exception as exc:
            print(f"[ManifestAnalyzer] Error parsing manifest: {exc}")
            return None

    def to_dict(self, manifest: apkutils2.Manifest) -> Dict[str, Any]:
        """Convert a Manifest object to a dictionary."""
        try:
            data = manifest.json() or {}
            print(f"[ManifestAnalyzer] Manifest dictionary keys: {list(data.keys())}")
            return data
        except Exception as exc:
            print(f"[ManifestAnalyzer] Failed to convert manifest to dict: {exc}")
            return {}

    def get_package_info(self, manifest: apkutils2.Manifest) -> Dict[str, str]:
        """Return basic package metadata."""
        info = {
            "package": manifest.package_name or "",
            "version_code": str(manifest.version_code or ""),
            "version_name": manifest.version_name or "",
            "main_activity": manifest.main_activity or "",
        }
        print(f"[ManifestAnalyzer] Package info: {info}")
        return info

    def get_permissions(self, manifest: apkutils2.Manifest) -> List[str]:
        """Return all permissions requested by the app."""
        try:
            perms = list(manifest.permissions)
            print(f"[ManifestAnalyzer] Permissions: {perms}")
            return perms
        except Exception as exc:
            print(f"[ManifestAnalyzer] Failed to get permissions: {exc}")
            return []

    def get_sdk_info(self, manifest: apkutils2.Manifest) -> Dict[str, str]:
        """Return ``minSdk`` and ``targetSdk`` levels if declared."""
        data = self.to_dict(manifest)
        uses_sdk = data.get("uses-sdk", {})
        if isinstance(uses_sdk, list):
            uses_sdk = uses_sdk[0] if uses_sdk else {}
        info = {
            "min_sdk": uses_sdk.get("@android:minSdkVersion", ""),
            "target_sdk": uses_sdk.get("@android:targetSdkVersion", ""),
        }
        print(f"[ManifestAnalyzer] SDK info: {info}")
        return info
