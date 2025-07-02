from unittest.mock import patch
import sys
from pathlib import Path
import importlib.util
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

def _load_module(name: str, path: Path, package: str):
    spec = importlib.util.spec_from_file_location(f"{package}.{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[f"{package}.{name}"] = module
    spec.loader.exec_module(module)
    return module

sys.modules.setdefault("analysis", types.ModuleType("analysis"))
manifest_pkg = types.ModuleType("analysis.manifest")
manifest_pkg.__path__ = [str(ROOT / "analysis/manifest")]
sys.modules.setdefault("analysis.manifest", manifest_pkg)
sys.modules["analysis"].manifest = manifest_pkg

pipeline = _load_module("pipeline", ROOT / "analysis/manifest/pipeline.py", "analysis.manifest")
scanner = _load_module("scanner", ROOT / "analysis/manifest/scanner.py", "analysis.manifest")


def test_format_results():
    results = [
        {"package": "com.example", "suspicious": ["READ_SMS"]},
        {"package": "com.safe", "suspicious": []},
    ]
    output = pipeline.format_results(results).splitlines()
    assert output[0] == "com.example: READ_SMS"
    assert output[1] == "com.safe: no suspicious permissions"


def test_scan_app_parses_permissions():
    adb_output = """
        package: com.example
        permission: android.permission.READ_SMS
        permission: android.permission.WRITE_CONTACTS
    """
    with patch("analysis.manifest.scanner.adb_shell", return_value=adb_output):
        result = scanner.scan_app("serial", "com.example")
    assert result["package"] == "com.example"
    assert "android.permission.READ_SMS" in result["permissions"]
    assert "android.permission.WRITE_CONTACTS" in result["permissions"]
    assert "android.permission.READ_SMS" in result["suspicious"]
    assert "android.permission.WRITE_CONTACTS" not in result["suspicious"]


def test_scan_app_no_permissions():
    with patch("analysis.manifest.scanner.adb_shell", return_value=""):
        result = scanner.scan_app("serial", "pkg")
    assert result == {"package": "pkg", "permissions": [], "suspicious": []}


def test_scan_packages_calls_scan_app(monkeypatch):
    calls = []

    def fake_scan_app(serial: str, pkg: str):
        calls.append(pkg)
        return {"package": pkg, "permissions": [], "suspicious": []}

    monkeypatch.setattr(scanner, "scan_app", fake_scan_app)
    results = scanner.scan_packages("serial", ["a", "b"])

    assert calls == ["a", "b"]
    assert len(results) == 2


def test_analyze_packages_pipeline(monkeypatch, tmp_path):
    fake_results = [{"package": "pkg", "permissions": [], "suspicious": []}]

    monkeypatch.setattr(pipeline, "scan_packages", lambda s, p: fake_results)
    json_called = []
    csv_called = []

    def fake_json(results):
        json_called.append(results)
        return str(tmp_path / "out.json")

    def fake_csv(results):
        csv_called.append(results)
        return str(tmp_path / "out.csv")

    monkeypatch.setattr(pipeline, "write_json_report", fake_json)
    monkeypatch.setattr(pipeline, "write_csv_report", fake_csv)

    json_path, csv_path, results = pipeline.analyze_packages("serial", ["pkg"])

    assert json_path.endswith("out.json")
    assert csv_path.endswith("out.csv")
    assert results == fake_results
    assert json_called == [fake_results]
    assert csv_called == [fake_results]

