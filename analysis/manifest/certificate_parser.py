"""Extract signing certificate details from an APK."""

from __future__ import annotations

from typing import Dict, List

import apkutils2


class CertificateParser:
    """Parse certificate information from APKs."""

    def parse(self, apk_path: str) -> List[Dict[str, str]]:
        """Return certificate subjects and MD5 digests."""
        print(f"[CertificateParser] Parsing certificates from {apk_path}")
        try:
            apk = apkutils2.APK(apk_path)
            certs = apk.get_certs() or []
            results: List[Dict[str, str]] = []
            for subject, md5 in certs:
                results.append({"subject": subject, "md5": md5})
            print(f"[CertificateParser] Found {len(results)} certificates")
            return results
        except Exception as exc:
            print(f"[CertificateParser] Failed to parse certificates: {exc}")
            return []
