# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GhostTrackerPro.py'],
    pathex=[],
    binaries=[],
    datas=[('web/static', 'web/static'), ('web/templates', 'web/templates')],
    hiddenimports=['requests', 'phonenumbers', 'phonenumbers.carrier', 'phonenumbers.geocoder', 'phonenumbers.timezone', 'flask', 'concurrent.futures'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'unittest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
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
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/workspaces/GhostTrackerPro/images/Logo.jpg'],
)
