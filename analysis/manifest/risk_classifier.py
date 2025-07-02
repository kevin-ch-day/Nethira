"""Classify apps based on their CVSS score."""

from __future__ import annotations


class RiskClassifier:
    """Simple LOW/MEDIUM/HIGH classifier."""

    def classify(self, score: float) -> str:
        print(f"[RiskClassifier] Classifying score: {score}")
        if score >= 7.0:
            level = "HIGH"
        elif score >= 4.0:
            level = "MEDIUM"
        else:
            level = "LOW"
        print(f"[RiskClassifier] Level: {level}")
        return level
