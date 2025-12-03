@echo off
REM Build License Key Generator GUI to EXE
echo ========================================
echo Building License Key Generator GUI...
echo ========================================
echo.

REM Check if openpyxl is installed
python -c "import openpyxl" 2>nul
if errorlevel 1 (
    echo openpyxl not found. Installing...
    pip install openpyxl
)

REM Build the executable
echo.
echo Building executable...
python -m PyInstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "LicenseKeyGenerator" ^
    --add-data "src/license_manager.py;." ^
    --hidden-import uuid ^
    --hidden-import platform ^
    --hidden-import hashlib ^
    --hidden-import hmac ^
    --hidden-import base64 ^
    --hidden-import json ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.cell._writer ^
    "bin/license_keygen_gui.py"

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\LicenseKeyGenerator.exe
echo.
pause
