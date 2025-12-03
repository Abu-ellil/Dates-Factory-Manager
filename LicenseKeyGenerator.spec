# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bin\\license_keygen_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('src/license_manager.py', '.')],
    hiddenimports=['uuid', 'platform', 'hashlib', 'hmac', 'base64', 'json', 'openpyxl', 'openpyxl.cell._writer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='LicenseKeyGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
