@echo off
title GhostTrackerPro - Windows Build Tool
echo.
echo  ============================================
echo       GhostTrackerPro - Windows Build
echo       Professional OSINT Toolkit v2.0
echo  ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [*] Python found: 
python --version

:: Install dependencies
echo.
echo [*] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

:: Clean previous build
echo.
echo [*] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: Build executable
echo.
echo [*] Building GhostTrackerPro.exe...
python -m PyInstaller --clean --noconfirm ^
    --name GhostTrackerPro ^
    --onefile ^
    --add-data "web/static;web/static" ^
    --add-data "web/templates;web/templates" ^
    --hidden-import requests ^
    --hidden-import phonenumbers ^
    --hidden-import phonenumbers.carrier ^
    --hidden-import phonenumbers.geocoder ^
    --hidden-import phonenumbers.timezone ^
    --hidden-import flask ^
    --hidden-import concurrent.futures ^
    --exclude-module tkinter ^
    --exclude-module test ^
    --exclude-module unittest ^
    --icon images\Logo.jpg ^
    GhostTrackerPro.py

if %errorlevel% equ 0 (
    echo.
    echo  ============================================
    echo       BUILD SUCCESSFUL!
    echo  ============================================
    echo.
    echo   Output: dist\GhostTrackerPro.exe
    echo.
    dir /a-d dist\GhostTrackerPro.exe
    echo.
    echo   Run: dist\GhostTrackerPro.exe --help
    echo   Or:  dist\GhostTrackerPro.exe
) else (
    echo.
    echo  ============================================
    echo       BUILD FAILED!
    echo  ============================================
    echo.
    echo   Check the error messages above.
)
echo.
pause
