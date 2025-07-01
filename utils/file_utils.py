"""Basic helpers for working with log files."""

import os
from datetime import datetime


def ensure_logs_dir() -> None:
    """Create the ``logs`` directory if missing."""
    if not os.path.exists("logs"):
        os.makedirs("logs")


def get_timestamped_log_path(prefix: str = "session") -> str:
    """Return a log file path containing a timestamp."""
    ensure_logs_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("logs", f"{prefix}_{timestamp}.log")


def save_text_to_file(filepath: str, text: str) -> None:
    """Write ``text`` to ``filepath`` using UTF-8 encoding."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
