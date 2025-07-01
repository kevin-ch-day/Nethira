from typing import Dict, List

from . import app_category_keywords
from utils import list_packages


SOCIAL_CATEGORIES = {
    "facebook": app_category_keywords.FACEBOOK_PACKAGES,
    "tiktok": app_category_keywords.TIKTOK_PACKAGES,
    "twitter": app_category_keywords.TWITTER_PACKAGES,
    "instagram": app_category_keywords.INSTAGRAM_PACKAGES,
    "parler": app_category_keywords.PARLER_PACKAGES,
    "reddit": app_category_keywords.REDDIT_PACKAGES,
}


def detect_social_media_apps(serial: str) -> Dict[str, List[str]]:
    """Return detected social media packages present on the device."""
    installed = set(list_packages(serial))
    results: Dict[str, List[str]] = {name: [] for name in SOCIAL_CATEGORIES}
    for name, prefixes in SOCIAL_CATEGORIES.items():
        for pkg in installed:
            if any(pkg.startswith(pref) for pref in prefixes):
                results[name].append(pkg)
    return {k: sorted(v) for k, v in results.items() if v}
