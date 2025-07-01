# Nethira

**Nethira** is a lightweight Android reconnaissance toolkit written in Python. It communicates with connected devices via ADB and provides an interactive interface for examining device information and installed applications.

## Features

- Detects and lists all Android devices accessible via ADB
- Displays detailed metadata such as serial, model, manufacturer and Android version
- Categorises installed apps using predefined keyword lists
- Works on Windows, macOS and Linux (uses the bundled ADB if available)

## Project Layout

```
main.py          # entry script
nethira/         # Python package with CLI and analysis modules
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
