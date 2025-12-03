@echo off
REM Quick launcher for License Key Generator GUI
title License Key Generator
cd /d "%~dp0"
python bin\license_keygen_gui.py
pause
