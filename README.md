# Nethira

**Nethira** is a lightweight Android reconnaissance toolkit written in Python. It communicates with connected devices via ADB and provides an interactive interface for examining device information and installed applications.

## Features

- Detects and lists all Android devices accessible via ADB
- Displays detailed metadata such as serial, model, manufacturer, build number, security patch level and more
- Categorises installed apps using predefined keyword lists
- Detects presence of major social media apps (Facebook, Twitter, Instagram, Parler, TikTok)
- Generates JSON reports containing device info and categorized apps
- Performs static manifest analysis of installed APKs
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

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
