"""Simple CVSS-like scoring for mobile app risks."""

from __future__ import annotations

from typing import Dict, Any


class CVSSScorer:
    """Assign a crude severity score from component scan results."""

    def score(self, scan_results: Dict[str, Any]) -> float:
        """Return a score between 0.0 and 10.0."""
        risky_perms = scan_results.get("risky_permissions", [])
        exported = scan_results.get("exported_components", [])
        actions = scan_results.get("intent_actions", [])
        print(
            f"[CVSSScorer] perms={len(risky_perms)} exported={len(exported)}"
            f" actions={len(actions)}"
        )
        score = (
            len(risky_perms) * 1.0
            + len(exported) * 0.5
            + len(actions) * 0.2
        )
        final = min(10.0, score)
        print(f"[CVSSScorer] Score: {final}")
        return final
