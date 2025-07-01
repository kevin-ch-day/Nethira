"App analysis utilities."

from .list_installed_apps import categorize_installed_apps
from .social_media_detector import detect_social_media_apps

__all__ = [
    "categorize_installed_apps",
    "detect_social_media_apps",
]
