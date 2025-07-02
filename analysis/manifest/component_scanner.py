"""Identify exported components and risky permissions."""

from __future__ import annotations

from typing import Any, Dict, List

import apkutils2


class ComponentScanner:
    """Scan manifest data for potential risks."""

    RISKY_PERMISSIONS = {
        "android.permission.RECORD_AUDIO",
        "android.permission.CAMERA",
        "android.permission.READ_SMS",
        "android.permission.SEND_SMS",
        "android.permission.RECEIVE_SMS",
        "android.permission.READ_CALL_LOG",
        "android.permission.WRITE_CALL_LOG",
        "android.permission.READ_CONTACTS",
        "android.permission.WRITE_CONTACTS",
        "android.permission.WRITE_SETTINGS",
        "android.permission.REQUEST_INSTALL_PACKAGES",
        "android.permission.SYSTEM_ALERT_WINDOW",
    }

    def scan(self, manifest: apkutils2.Manifest) -> Dict[str, Any]:
        """Return exported components, intents and risky permissions."""
        print("[ComponentScanner] Scanning manifest")
        data = manifest.json() or {}
        exported: List[Dict[str, str]] = []
        intent_actions: List[str] = []
        app = data.get("application", {})
        for comp_type in ["activity", "provider", "receiver", "service"]:
            comps = app.get(comp_type, [])
            if isinstance(comps, dict):
                comps = [comps]
            for comp in comps:
                exported_flag = comp.get("@android:exported") == "true"
                name = comp.get("@android:name")
                filters = comp.get("intent-filter", [])
                if isinstance(filters, dict):
                    filters = [filters]
                actions = []
                for flt in filters:
                    acts = flt.get("action", [])
                    if isinstance(acts, dict):
                        acts = [acts]
                    for a in acts:
                        act_name = a.get("@android:name")
                        if act_name:
                            actions.append(act_name)
                if exported_flag:
                    exported.append({"type": comp_type, "name": name})
                intent_actions.extend(actions)
        perms = [p for p in manifest.permissions if p in self.RISKY_PERMISSIONS]
        print(f"[ComponentScanner] Exported components: {exported}")
        print(f"[ComponentScanner] Risky permissions: {perms}")
        print(f"[ComponentScanner] Intent actions: {intent_actions}")
        return {
            "exported_components": exported,
            "risky_permissions": perms,
            "intent_actions": list(set(intent_actions)),
        }
