# filename: analysis/list_installed_apps.py
# Description: Categorize Android apps into various groups including
# manufacturer, android core, google, major social media platforms,
# vendor related apps, user installed, system, and uncategorized

from typing import Dict, List

from analysis.apps import app_category_keywords
from utils import list_packages

def _matches_any(pkg: str, keywords: List[str]) -> bool:
    """Return True if the package name starts with any of the given keywords."""
    pkg_lower = pkg.lower()
    return any(pkg_lower.startswith(keyword.lower()) for keyword in keywords)

def categorize_installed_apps(serial: str, manufacturer: str) -> Dict[str, List[str]]:
    """
    Categorize installed Android apps into known groups based on package prefixes.
    Priority order: manufacturer -> android -> google -> facebook -> tiktok -> twitter -> instagram -> parler -> reddit -> vendor -> user -> system -> uncategorized
    """
    print("\n[*] Scanning installed apps on device:", serial)
    print("[*] Please wait...\n")

    all_apps = set(list_packages(serial))
    system_apps = set(list_packages(serial, ["-s"]))
    user_apps = set(list_packages(serial, ["-3"]))

    categorized: Dict[str, List[str]] = {
        "manufacturer": [],
        "android": [],
        "google": [],
        "facebook": [],
        "tiktok": [],
        "twitter": [],
        "instagram": [],
        "parler": [],
        "reddit": [],
        "vendor": [],
        "user": [],
        "system": [],
        "uncategorized": []
    }

    assigned = set()

    # Manufacturer apps (first priority)
    for pkg in sorted(all_apps):
        if manufacturer.lower() in pkg.lower() or pkg.startswith(f"com.{manufacturer.lower()}"):
            categorized["manufacturer"].append(pkg)
            assigned.add(pkg)

    # Android core packages
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.ANDROID_PACKAGES):
            categorized["android"].append(pkg)
            assigned.add(pkg)

    # Google packages
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.GOOGLE_PACKAGES):
            categorized["google"].append(pkg)
            assigned.add(pkg)

    # Facebook apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.FACEBOOK_PACKAGES):
            categorized["facebook"].append(pkg)
            assigned.add(pkg)

    # TikTok apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.TIKTOK_PACKAGES):
            categorized["tiktok"].append(pkg)
            assigned.add(pkg)

    # Twitter apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.TWITTER_PACKAGES):
            categorized["twitter"].append(pkg)
            assigned.add(pkg)

    # Instagram apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.INSTAGRAM_PACKAGES):
            categorized["instagram"].append(pkg)
            assigned.add(pkg)

    # Parler apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.PARLER_PACKAGES):
            categorized["parler"].append(pkg)
            assigned.add(pkg)

    # Reddit apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.REDDIT_PACKAGES):
            categorized["reddit"].append(pkg)
            assigned.add(pkg)

    # Vendor-related apps
    for pkg in sorted(all_apps - assigned):
        if _matches_any(pkg, app_category_keywords.VENDOR_KEYWORDS):
            categorized["vendor"].append(pkg)
            assigned.add(pkg)

    # User-installed apps
    for pkg in sorted(all_apps - assigned):
        if pkg in user_apps:
            categorized["user"].append(pkg)
            assigned.add(pkg)

    # Remaining system apps
    for pkg in sorted(all_apps - assigned):
        if pkg in system_apps:
            categorized["system"].append(pkg)
            assigned.add(pkg)

    # Any remaining go to uncategorized
    for pkg in sorted(all_apps - assigned):
        categorized["uncategorized"].append(pkg)

    # Sort all lists alphabetically before returning
    for key in categorized:
        categorized[key] = sorted(categorized[key])

    _print_app_summary(categorized)
    return categorized

def _print_app_summary(apps_by_category: Dict[str, List[str]]) -> None:
    """Print app category summary with ASCII-only formatting, skipping empty categories."""
    print("============================================================")
    print("                APP CATEGORY SUMMARY")
    print("============================================================")
    for label in [
        "manufacturer",
        "android",
        "google",
        "facebook",
        "tiktok",
        "twitter",
        "instagram",
        "parler",
        "reddit",
        "vendor",
        "user",
        "system",
        "uncategorized",
    ]:
        apps = apps_by_category.get(label, [])
        if apps:
            print(f" [{label.capitalize():<13}] {len(apps)} apps")
    print("============================================================\n")
