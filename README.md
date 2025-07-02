# Nethira

**Nethira** is a lightweight Android reconnaissance toolkit written in Python. It communicates with connected devices via ADB and provides an interactive interface for examining device information and installed applications.

## Features

- Detects and lists all Android devices accessible via ADB
- Displays detailed metadata such as serial, model, manufacturer, build number, security patch level and more
- Categorises installed apps using predefined keyword lists
- Detects presence of major social media apps (Facebook, Twitter, Instagram, Parler, TikTok)
- Generates JSON reports containing device info and categorized apps
- Performs static analysis of APK files to inspect manifest metadata and requested permissions
- Saves analysis results as timestamped JSON files in the `logs/` directory
- Works on Windows, macOS and Linux (uses the bundled ADB if available)

## Project Layout

```
main.py          # entry script
analysis/        # device and app analysis modules
models/          # dataclass definitions
utils/           # helper utilities
platform_tools/  # optional ADB binaries for Windows users
run_app.bat      # helper script for launching on Windows
```

## Quick Start

1. Ensure the `platform_tools` folder is present or that ADB is installed and on your PATH.
2. Run the application from the project root:

```bash
python main.py
```

Windows users may double-click `run_app.bat` instead.

### Static APK Analysis

Static analysis requires the optional [`androguard`](https://pypi.org/project/androguard/) package to parse APK
files. Once installed you can analyze an APK by providing the path when launching the
tool:

```bash
python main.py /path/to/app.apk
```

Analysis results will be written as JSON files inside `logs/` with a timestamped
name such as `apk_<package>_20240101_120000.log`.

Some features also rely on the [`apkutils2`](https://pypi.org/project/apkutils2/) library.
If it is not installed the manifest analysis modules will be disabled but the
rest of the toolkit will still operate.

### Display Utilities

Nethira includes helper functions for consistent terminal output.
See `tools/display_messages.py` for a demonstration of formatted
info, warning and error messages as well as titles and key/value blocks.
Colors are automatically enabled when the output is a TTY but can be
forced on or off using the `FORCE_COLOR` and `NO_COLOR` environment
variables. Utility functions are provided to check or change this
behaviour at runtime.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
