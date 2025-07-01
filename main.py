# filename: nethira/main.py
# Description: Command line interface for the Nethira Android Recon Toolkit

import sys

from analysis.device import device_enumeration, device_reporter
from analysis.apps import list_installed_apps, social_media_detector
from models.device_info import DeviceInfo
from utils import display_utils


def show_main_menu() -> None:
    """Display the main menu options."""
    print("============================================================")
    print("                 NETHIRA - ANDROID RECON TOOLKIT          ")
    print("============================================================")
    print(" [1] Show connected devices")
    print(" [2] List installed apps by category")
    print(" [3] Detect social media apps")
    print(" [4] Generate device report")
    print(" [0] Exit")
    print("============================================================\n")


def prompt_device_selection(devices: list[DeviceInfo]) -> DeviceInfo | None:
    """
    Prompt the user to select a device from the connected list.
    Returns None if selection is invalid or cancelled.
    """
    if not devices:
        print("[!] No devices available for selection.\n")
        return None

    print("\nSelect a device:")
    for idx, device in enumerate(devices, start=1):
        print(f" [{idx}] {device.serial} - {device.model}")

    choice = input("\nEnter device number: ").strip()
    if not choice.isdigit():
        print("[!] Please enter a valid number.\n")
        return None

    index = int(choice)
    if 1 <= index <= len(devices):
        return devices[index - 1]
    else:
        print("[!] Invalid selection.\n")
        return None


def handle_app_listing(devices: list[DeviceInfo]):
    """Allow the user to pick a device and show categorized app info."""
    selected_device = prompt_device_selection(devices)
    if not selected_device:
        return

    apps = list_installed_apps.categorize_installed_apps(
        selected_device.serial,
        selected_device.manufacturer
    )

    print("============================================================")
    print(f" APP LISTING FOR DEVICE: {selected_device.model} ({selected_device.serial})")
    print("============================================================\n")

    for category, app_list in apps.items():
        if not app_list:
            continue
        print(f"=== {category.upper()} APPS ({len(app_list)}) ===")
        for idx, pkg in enumerate(app_list, 1):
            print(f" [{idx}] {pkg}")
        print()


def handle_social_media_scan(devices: list[DeviceInfo]) -> None:
    """Scan for well-known social media apps on a selected device."""
    selected_device = prompt_device_selection(devices)
    if not selected_device:
        return

    results = social_media_detector.detect_social_media_apps(selected_device.serial)
    print("============================================================")
    print(
        f" SOCIAL MEDIA APPS ON: {selected_device.model} ({selected_device.serial})"
    )
    print("============================================================\n")

    if not results:
        print("No major social media apps found.\n")
        return

    for name, packages in results.items():
        print(f"=== {name.upper()} ({len(packages)}) ===")
        for pkg in packages:
            print(f" - {pkg}")
        print()


def handle_device_report(devices: list[DeviceInfo]) -> None:
    """Generate and save a detailed report for a chosen device."""
    selected_device = prompt_device_selection(devices)
    if not selected_device:
        return

    path = device_reporter.save_report(
        selected_device.serial, selected_device.manufacturer
    )
    print(f"\nReport saved to {path}\n")


def main():
    display_utils.print_banner()

    while True:
        show_main_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            _ = device_enumeration.enumerate_and_display_devices()

        elif choice == "2":
            devices = device_enumeration.enumerate_and_display_devices()
            if devices:
                handle_app_listing(devices)

        elif choice == "3":
            devices = device_enumeration.enumerate_and_display_devices()
            if devices:
                handle_social_media_scan(devices)

        elif choice == "4":
            devices = device_enumeration.enumerate_and_display_devices()
            if devices:
                handle_device_report(devices)

        elif choice == "0":
            print("\nExiting Nethira.\n")
            break

        else:
            print("[!] Invalid input. Please enter a valid option.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...\n")
        sys.exit(0)
