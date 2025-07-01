:: filename: scripts\clean_up_project.bat
:: Description: Recursively delete all .pyc files and __pycache__ folders from the project
:: Usage: Run from the root of the Nethira project directory (e.g., D:\Dev\Github\Nethira)

@echo off
setlocal ENABLEEXTENSIONS
title Nethira Cleanup Utility

echo ============================================================
echo   NETHIRA CLEANUP UTILITY - Remove .pyc and __pycache__
echo ============================================================
echo.

:: Verify we are in the project root by checking for main.py
if not exist "main.py" (
    echo [!] Error: This script must be run from the root of the Nethira project.
    echo     File "main.py" not found in the current directory.
    echo.
    pause
    goto :EOF
)

:: Confirm cleanup
set /p confirm=Are you sure you want to clean the project? [Y/N]: 
if /I not "%confirm%"=="Y" (
    echo.
    echo [*] Cleanup canceled by user.
    goto :EOF
)

echo.
echo [*] Deleting all .pyc files...
for /r %%i in (*.pyc) do (
    if exist "%%i" (
        echo   - Deleting: %%i
        del /f /q "%%i"
    )
)

echo.
echo [*] Removing all __pycache__ folders...
for /d /r %%d in (*) do (
    if /i "%%~nxd"=="__pycache__" (
        echo   - Removing: %%d
        rmdir /s /q "%%d"
    )
)

echo.
echo [*] Cleanup complete.
pause
