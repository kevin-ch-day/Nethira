# filename: analysis/manifest/__init__.py
"""Static manifest analysis utilities."""

from __future__ import annotations

from typing import Any

from .apk_extractor import APKExtractor
from .cvss_scorer import CVSSScorer
from .risk_classifier import RiskClassifier
from .version_tracker import VersionTracker
from .scanner import scan_packages
from .report_writer import write_json_report, write_csv_report
from .pipeline import analyze_packages, format_results

ManifestAnalyzer: Any | None
ComponentScanner: Any | None
CertificateParser: Any | None

try:  # pragma: no cover - optional dependency
    from .manifest_analyzer import ManifestAnalyzer
    from .component_scanner import ComponentScanner
    from .certificate_parser import CertificateParser
except Exception as exc:  # noqa: BLE001
    ManifestAnalyzer = None
    ComponentScanner = None
    CertificateParser = None
    print(f"[analysis.manifest] Optional features unavailable: {exc}")

__all__ = [
    "APKExtractor",
    "ManifestAnalyzer",
    "ComponentScanner",
    "CertificateParser",
    "CVSSScorer",
    "RiskClassifier",
    "VersionTracker",
    "scan_packages",
    "write_json_report",
    "write_csv_report",
    "analyze_packages",
    "format_results",
]
