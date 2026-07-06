#!/usr/bin/env python3
"""
GhostTrackerPro - Windows Executable Builder

Builds a standalone Windows .exe using PyInstaller.
Run on Windows:
    python build_exe.py

Or cross-compile on Linux (requires pyinstaller + wine):
    python build_exe.py --linux  (builds Linux binary instead)
"""

import os
import sys
import shutil
import subprocess
import platform

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')

BANNER = """
  ╔══════════════════════════════════════════════╗
  ║        GhostTrackerPro - Build Tool          ║
  ║        Professional OSINT Toolkit v2.0       ║
  ╚══════════════════════════════════════════════╝
"""


def clean():
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            print(f"  Cleaning {d}...")
            shutil.rmtree(d)
    # Also clean .spec if left over
    spec_file = os.path.join(PROJECT_DIR, 'GhostTrackerPro.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)


def check_dependencies():
    print("  Checking dependencies...")
    missing = []
    try:
        import requests
    except ImportError:
        missing.append('requests')
    try:
        import phonenumbers
    except ImportError:
        missing.append('phonenumbers')
    try:
        import flask
    except ImportError:
        missing.append('flask')
    try:
        import PyInstaller
    except ImportError:
        missing.append('pyinstaller')

    if missing:
        print(f"  ERROR: Missing packages: {', '.join(missing)}")
        print(f"  Install: pip install {' '.join(missing)}")
        sys.exit(1)

    # Check for UPX (optional, for smaller exe)
    upx = shutil.which('upx')
    if upx:
        print(f"  UPX found: {upx}")
    else:
        print("  UPX not found (optional, exe will be larger)")


def build_windows():
    print("  Building Windows executable...")
    spec_path = os.path.join(PROJECT_DIR, 'GhostTrackerPro.spec')
    
    if not os.path.exists(spec_path):
        print("  ERROR: GhostTrackerPro.spec not found!")
        sys.exit(1)

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        spec_path,
    ]
    
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_DIR)
    
    if result.returncode != 0:
        print(f"  ERROR: Build failed with code {result.returncode}")
        sys.exit(1)
    
    exe_path = os.path.join(DIST_DIR, 'GhostTrackerPro.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n  SUCCESS: {exe_path} ({size_mb:.1f} MB)")
    else:
        print("\n  Build completed. Check the dist/ folder.")


def build_linux():
    print("  Building Linux executable...")
    from PyInstaller.__main__ import run as pyi_run
    
    args = [
        'GhostTrackerPro.py',
        '--name=GhostTrackerPro',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--add-data', f'web/static{os.pathsep}web/static',
        '--add-data', f'web/templates{os.pathsep}web/templates',
        '--hidden-import=requests',
        '--hidden-import=phonenumbers',
        '--hidden-import=phonenumbers.carrier',
        '--hidden-import=phonenumbers.geocoder',
        '--hidden-import=phonenumbers.timezone',
        '--hidden-import=flask',
        '--hidden-import=concurrent.futures',
        '--exclude-module=tkinter',
        '--exclude-module=test',
        '--exclude-module=unittest',
    ]
    
    # Try to find logo icon
    logo = os.path.join(PROJECT_DIR, 'images', 'Logo.jpg')
    if os.path.exists(logo):
        args.extend(['--icon', logo])
    
    print(f"  Running PyInstaller with args: {' '.join(args)}")
    pyi_run(args)
    
    exe_name = 'GhostTrackerPro' if platform.system() == 'Windows' else 'GhostTrackerPro'
    exe_path = os.path.join(DIST_DIR, exe_name)
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n  SUCCESS: {exe_path} ({size_mb:.1f} MB)")
    else:
        # Try with extension
        for f in os.listdir(DIST_DIR):
            print(f"  Output: {os.path.join(DIST_DIR, f)}")


def zip_build():
    """Create a portable zip of the dist folder."""
    zip_name = os.path.join(PROJECT_DIR, 'dist', 'GhostTrackerPro_Portable.zip')
    print(f"  Creating {zip_name}...")
    shutil.make_archive(
        zip_name.replace('.zip', ''),
        'zip',
        DIST_DIR
    )
    size_mb = os.path.getsize(zip_name) / (1024 * 1024)
    print(f"  Created: {zip_name} ({size_mb:.1f} MB)")


def main():
    print(BANNER)

    is_windows = platform.system() == 'Windows'
    
    if len(sys.argv) > 1 and sys.argv[1] == '--linux':
        build_linux()
    elif is_windows:
        print(f"  OS: Windows ({platform.release()})")
        print(f"  Python: {sys.version.split()[0]}\n")
        check_dependencies()
        build_windows()
        print(f"\n  Output in: {DIST_DIR}")
        print("  Run: dist\\GhostTrackerPro.exe")
    else:
        print(f"  OS: {platform.system()} ({platform.release()})")
        print(f"  Python: {sys.version.split()[0]}\n")
        print("  NOTE: Cross-compiling for Windows requires Windows.")
        print("  Building Linux binary instead.")
        print("  For Windows exe, run this script on a Windows machine.\n")
        check_dependencies()
        build_linux()
        print(f"\n  Output in: {DIST_DIR}")
        print("  Run: ./dist/GhostTrackerPro")


if __name__ == '__main__':
    main()
