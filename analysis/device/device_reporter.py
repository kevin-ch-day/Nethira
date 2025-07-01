"""Generate and save comprehensive device reports."""

from __future__ import annotations

import json

from models.device_info import DeviceInfo
from analysis.apps import list_installed_apps, social_media_detector
from utils import file_utils
from . import device_info_fetcher


def build_report(serial: str, manufacturer: str) -> dict:
    """Collect device info, app categories and social apps."""
    info: DeviceInfo = device_info_fetcher.get_device_info(serial)
    apps = list_installed_apps.categorize_installed_apps(serial, manufacturer)
    social = social_media_detector.detect_social_media_apps(serial)
    return {
        "device_info": info.to_dict(),
        "app_categories": apps,
        "social_media": social,
    }


def save_report(serial: str, manufacturer: str, path: str | None = None) -> str:
    """Save a JSON device report and return the file path."""
    report = build_report(serial, manufacturer)
    filepath = path or file_utils.get_timestamped_log_path(f"report_{serial}")
    file_utils.save_text_to_file(filepath, json.dumps(report, indent=2))
    return filepath
