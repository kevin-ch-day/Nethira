:: filename: run_app.bat
:: Description: Launch the Nethira CLI application
:: Usage: Double-click or run from Command Prompt

@echo off
setlocal ENABLEEXTENSIONS
title Nethira - Android Recon Toolkit Launcher

:: Check if main.py exists
if not exist "main.py" (
    echo [!] Error: main.py not found in the current directory.
    echo     Please run this script from the root of the Nethira project.
    echo.
    pause
    goto :EOF
)

:: Launch application
python main.py

:: End
echo.
echo [*] Application closed.
pause
