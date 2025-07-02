"""Pull APK files from a device and compute hashes."""

from __future__ import annotations

import csv
import hashlib
import os
from typing import Dict, List

from utils.adb_utils import run_adb


class APKExtractor:
    """Helper for pulling APKs from a device."""

    def __init__(self,
                 output_dir: str = "output/app_static_profiles",
                 log_file: str = "output/apk_pull_log.csv") -> None:
        self.output_dir = output_dir
        self.log_file = log_file
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        print(f"[APKExtractor] Output directory: {self.output_dir}")
        print(f"[APKExtractor] Log file: {self.log_file}")

    def _write_log(self, row: List[str]) -> None:
        write_header = not os.path.exists(self.log_file)
        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["package", "remote_path", "local_path", "sha256"])
                print(f"[APKExtractor] Writing header to log")
            print(f"[APKExtractor] Logging row: {row}")
            writer.writerow(row)

    def pull_apk(self, serial: str, package: str) -> Dict[str, str] | None:
        """Pull the APK for ``package`` from ``serial`` and return metadata."""
        print(f"[APKExtractor] Pulling {package} from {serial}")
        try:
            result = run_adb(["-s", serial, "shell", "pm", "path", package])
            for line in result.stdout.splitlines():
                if line.startswith("package:"):
                    remote_path = line.replace("package:", "").strip()
                    break
            else:
                print(f"[APKExtractor] Failed to find path for {package}")
                return None

            pkg_dir = os.path.join(self.output_dir, package)
            os.makedirs(pkg_dir, exist_ok=True)
            local_path = os.path.join(pkg_dir, os.path.basename(remote_path))
            print(f"[APKExtractor] Pulling from {remote_path} to {local_path}")
            run_adb(["-s", serial, "pull", remote_path, local_path])

            with open(local_path, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
            print(f"[APKExtractor] SHA256 for {package}: {sha256}")

            self._write_log([package, remote_path, local_path, sha256])
            return {
                "package": package,
                "remote_path": remote_path,
                "local_path": local_path,
                "sha256": sha256,
            }
        except Exception as exc:
            print(f"[APKExtractor] Error pulling {package}: {exc}")
            return None

    def pull_and_record(self, serial: str, package: str,
                         analyzer: "ManifestAnalyzer" | None = None,
                         tracker: "VersionTracker" | None = None) -> Dict[str, str] | None:
        """Pull an APK and optionally record its version history."""
        print(f"[APKExtractor] pull_and_record called for {package}")
        meta = self.pull_apk(serial, package)
        if not meta or not analyzer or not tracker:
            return meta
        manifest = analyzer.parse(meta["local_path"])
        if manifest:
            info = analyzer.get_package_info(manifest)
            print(
                f"[APKExtractor] Recording version {info.get('version_code', '')} "
                f"for {package}"
            )
            tracker.record(package, info.get("version_code", ""), meta["sha256"])
        return meta
