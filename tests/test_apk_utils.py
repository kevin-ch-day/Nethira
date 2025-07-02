import zipfile
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import apk_utils


def create_sample_apk(path: Path) -> None:
    manifest_data = b"<manifest></manifest>"
    cert_data = b"dummy-cert"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("AndroidManifest.xml", manifest_data)
        z.writestr("META-INF/CERT.RSA", cert_data)


def test_extract_manifest_and_certificate(tmp_path):
    apk_path = tmp_path / "sample.apk"
    create_sample_apk(apk_path)

    manifest = apk_utils.extract_manifest(str(apk_path))
    assert manifest == b"<manifest></manifest>"

    cert = apk_utils.extract_certificate(str(apk_path))
    assert cert == b"dummy-cert"


def test_extract_manifest_xml(tmp_path, monkeypatch):
    apk_path = tmp_path / "sample.apk"
    create_sample_apk(apk_path)

    class DummyAXML:
        def __init__(self, data: bytes) -> None:
            self.data = data

        def get_xml(self) -> str:
            return "<manifest></manifest>"

    monkeypatch.setattr(apk_utils, "AXML", DummyAXML)
    xml = apk_utils.extract_manifest_xml(str(apk_path))
    assert xml == "<manifest></manifest>"


def test_missing_files_return_none(tmp_path):
    missing = tmp_path / "missing.apk"
    assert apk_utils.extract_manifest(str(missing)) is None
    assert apk_utils.extract_certificate(str(missing)) is None
    assert apk_utils.extract_manifest_xml(str(missing)) is None


def test_extract_certificate_not_present(tmp_path):
    apk_path = tmp_path / "no_cert.apk"
    with zipfile.ZipFile(apk_path, "w") as z:
        z.writestr("AndroidManifest.xml", b"<manifest></manifest>")
    assert apk_utils.extract_certificate(str(apk_path)) is None


def test_extract_manifest_xml_no_axml(tmp_path, monkeypatch):
    apk_path = tmp_path / "sample.apk"
    create_sample_apk(apk_path)
    monkeypatch.setattr(apk_utils, "AXML", None)
    assert apk_utils.extract_manifest_xml(str(apk_path)) is None


def test_extract_manifest_xml_decode_error(tmp_path, monkeypatch):
    apk_path = tmp_path / "sample.apk"
    create_sample_apk(apk_path)

    class BrokenAXML:
        def __init__(self, data: bytes) -> None:
            pass

        def get_xml(self) -> str:
            raise ValueError("bad")

    monkeypatch.setattr(apk_utils, "AXML", BrokenAXML)
    assert apk_utils.extract_manifest_xml(str(apk_path)) is None

