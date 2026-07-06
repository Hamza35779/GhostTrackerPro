# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for GhostTrackerPro Windows executable.
Build: pyinstaller GhostTrackerPro.spec
"""

import os
import sys

block_cipher = None

PROJECT_DIR = os.getcwd()
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
PKG_DIR = os.path.join(SRC_DIR, 'ghosttrackerpro')
STATIC_DIR = os.path.join(PKG_DIR, 'web', 'static')
TEMPLATES_DIR = os.path.join(PKG_DIR, 'web', 'templates')
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')
ICON_PATH = os.path.join(IMAGES_DIR, 'Logo.jpg')

a = Analysis(
    ['GhostTrackerPro.py'],
    pathex=[SRC_DIR, PROJECT_DIR],
    binaries=[],
    datas=[
        (STATIC_DIR, 'ghosttrackerpro/web/static'),
        (TEMPLATES_DIR, 'ghosttrackerpro/web/templates'),
    ],
    hiddenimports=[
        'requests',
        'phonenumbers',
        'phonenumbers.carrier',
        'phonenumbers.geocoder',
        'phonenumbers.timezone',
        'phonenumbers.phonenumberutil',
        'flask',
        'json',
        'socket',
        'ssl',
        'concurrent.futures',
        'urllib.parse',
        'ghosttrackerpro',
        'ghosttrackerpro.core',
        'ghosttrackerpro.cli',
        'ghosttrackerpro.app',
        'ghosttrackerpro.web',
        'ghosttrackerpro.web.server',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'test',
        'unittest',
        'email',
        'http.server',
        'xml',
        'pydoc',
        'doctest',
        'pickle',
        'lib2to3',
        'distutils',
        'setuptools',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GhostTrackerPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_tracedefaults=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
)
