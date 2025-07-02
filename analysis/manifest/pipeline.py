# filename: analysis/manifest/pipeline.py
"""High level manifest analysis workflow."""

from __future__ import annotations

from typing import List, Tuple, Dict

from .scanner import scan_packages
from .report_writer import write_json_report, write_csv_report


def analyze_packages(serial: str, packages: List[str]) -> Tuple[str, str, List[Dict[str, List[str]]]]:
    """Scan packages and output JSON and CSV reports.

    Returns:
        Tuple[str, str]: Paths to the JSON and CSV reports.
    """
    print(f"[DEBUG] Starting manifest scan on {serial} for {len(packages)} packages")
    results = scan_packages(serial, packages)
    print(f"[DEBUG] Finished scanning. Generating reports...")
    json_path = write_json_report(results)
    csv_path = write_csv_report(results)
    print(f"[DEBUG] Reports written: JSON -> {json_path}, CSV -> {csv_path}")
    return json_path, csv_path, results


def format_results(results: List[Dict[str, List[str]]]) -> str:
    """Return a readable summary of manifest scan results."""
    lines = []
    for item in results:
        pkg = item.get("package", "")
        suspicious = item.get("suspicious", [])
        if suspicious:
            lines.append(f"{pkg}: {', '.join(suspicious)}")
        else:
            lines.append(f"{pkg}: no suspicious permissions")
    return "\n".join(lines)
