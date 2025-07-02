#!/usr/bin/env python3
"""Demonstration script for Nethira display utilities."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import (
    print_banner,
    print_info,
    print_warning,
    print_error,
    print_success,
)


def main() -> None:
    print_banner()
    print_info("This is an info message")
    print_warning("This is a warning")
    print_error("This is an error")
    print_success("All done")


if __name__ == "__main__":
    main()
