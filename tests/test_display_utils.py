import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import display_utils


def test_format_key_values_basic():
    data = {"a": "1", "bb": "2"}
    out = display_utils.format_key_values(data)
    lines = out.splitlines()
    assert lines[0] == "a  : 1"
    assert lines[1] == "bb : 2"


def test_format_key_values_empty():
    assert display_utils.format_key_values({}) == ""


def test_message_helpers_no_color(capsys):
    orig = display_utils.USE_COLORS
    display_utils.USE_COLORS = False
    try:
        display_utils.print_error("bad")
        display_utils.print_warning("warn")
        display_utils.print_success("ok")
        display_utils.print_info("info")
    finally:
        display_utils.USE_COLORS = orig
    out = [line.strip() for line in capsys.readouterr().out.splitlines()]
    assert out == [
        "[ERROR] bad",
        "[WARN ] warn",
        "[ OK  ] ok",
        "[INFO ] info",
    ]


def test_color_detection_env(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert display_utils.detect_color_support() is False
    monkeypatch.delenv("NO_COLOR")
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert display_utils.detect_color_support() is True


def test_strip_ansi():
    colored = "\x1b[91mhello\x1b[0m"
    assert display_utils.strip_ansi(colored) == "hello"
