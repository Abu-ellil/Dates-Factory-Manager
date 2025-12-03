"""
Build script to create executable for License Generator GUI
"""
import os
import sys
from PyInstaller.__main__ import run as pyinstaller_run

def build_executable():
    # Change to the src directory
    os.chdir('src')

    # PyInstaller arguments
    args = [
        '--onefile',
        '--windowed',  # No console window
        '--icon=build_tools/icon.ico',  # Use existing icon
        '--name=LicenseGeneratorGUI',
        '--clean',
        'generate_license_gui.py'
    ]

    print("Building License Generator GUI executable...")
    print(f"Command: pyinstaller {' '.join(args)}")

    try:
        # Run PyInstaller
        pyinstaller_run(args)

        # Check if the executable was created (check in root dist directory)
        if os.path.exists('../dist/LicenseGeneratorGUI.exe'):
            print("✓ Executable created successfully!")
            print(f"Executable location: {os.path.abspath('../dist/LicenseGeneratorGUI.exe')}")
        else:
            print("✗ Failed to create executable")

    except Exception as e:
        print(f"Error building executable: {e}")

if __name__ == "__main__":
    build_executable()
