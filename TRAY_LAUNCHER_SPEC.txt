# INSTRUCTIONS:
# Copy this content to: build_tools\app_tray.spec
# Then build with: python -m PyInstaller --clean --noconfirm build_tools\app_tray.spec

# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Paths relative to build_tools/
src_path = '../src'
docs_path = '../docs'

# Collect all template and static files
added_files = [
    (os.path.join(src_path, 'templates'), 'templates'),
    (os.path.join(src_path, 'static'), 'static'),
    (os.path.join(src_path, '*.db'), '.'),
    (os.path.join(docs_path, '*.md'), 'docs'),
]

a = Analysis(
    [os.path.join(src_path, 'tray_launcher.py')],  # Use tray launcher
    pathex=[os.path.abspath(src_path)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask',
        'xlsxwriter',
        'apscheduler',
        'telegram',
        'telegram.ext',
        'database',
        'export',
        'generate_sheet',
        'backup_scheduler',
        'cloud_upload',
        'license_manager',
        'flask_login',
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DateFactoryManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ← NO CONSOLE WINDOW!
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DateFactoryPortable',
)
