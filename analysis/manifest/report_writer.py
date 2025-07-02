# filename: analysis/manifest/report_writer.py
"""Report writers for manifest scan results."""

from __future__ import annotations

import csv
import json
import os
from typing import List, Dict

from utils import file_utils


def _get_path(prefix: str, ext: str) -> str:
    base = file_utils.get_timestamped_log_path(prefix)
    path = os.path.splitext(base)[0] + f".{ext}"
    print(f"[DEBUG] Generated {ext.upper()} report path: {path}")
    return path


def write_json_report(results: List[Dict[str, List[str]]], prefix: str = "manifest") -> str:
    """Write results to a JSON file and return the path."""
    path = _get_path(prefix, "json")
    file_utils.save_text_to_file(path, json.dumps(results, indent=2))
    print(f"[DEBUG] JSON report saved to {path}")
    return path


def write_csv_report(results: List[Dict[str, List[str]]], prefix: str = "manifest") -> str:
    """Write results to a CSV file and return the path."""
    path = _get_path(prefix, "csv")
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["package", "permissions", "suspicious"])
        for item in results:
            perms = ",".join(item.get("permissions", []))
            suspicious = ",".join(item.get("suspicious", []))
            writer.writerow([item.get("package", ""), perms, suspicious])
    print(f"[DEBUG] CSV report saved to {path}")
    return path
