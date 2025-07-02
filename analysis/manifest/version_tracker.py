"""Track version information for APKs over time."""

from __future__ import annotations

import csv
import os
from datetime import datetime
from typing import List, Tuple


class VersionTracker:
    """Append version and hash details to a timeline CSV."""

    def __init__(self, timeline_file: str = "output/update_timeline.csv") -> None:
        self.timeline_file = timeline_file
        os.makedirs(os.path.dirname(self.timeline_file), exist_ok=True)
        print(f"[VersionTracker] Timeline file: {self.timeline_file}")

    def record(self, package: str, version: str, sha256: str) -> None:
        """Add an entry for the given package version."""
        write_header = not os.path.exists(self.timeline_file)
        with open(self.timeline_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["timestamp", "package", "version", "sha256"])
                print("[VersionTracker] Writing header to timeline")
            print(
                f"[VersionTracker] Recording {package} version {version} sha256 {sha256}"
            )
            writer.writerow([
                datetime.utcnow().isoformat(timespec="seconds"),
                package,
                version,
                sha256,
            ])

    def history(self, package: str) -> List[Tuple[str, str, str, str]]:
        """Return timeline rows for ``package``."""
        if not os.path.exists(self.timeline_file):
            return []
        rows: List[Tuple[str, str, str, str]] = []
        with open(self.timeline_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) == 4 and row[1] == package:
                    rows.append(tuple(row))
        print(f"[VersionTracker] History for {package}: {len(rows)} entries")
        return rows
