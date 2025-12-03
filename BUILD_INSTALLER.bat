@echo off
chcp 65001 >nul
title Building Date Factory Manager Installer
color 0B

echo.
echo ═══════════════════════════════════════════════════════════
echo    🏭 Date Factory Manager - Installer Builder
echo ═══════════════════════════════════════════════════════════
echo.
echo 🚀 Starting automated build process...
echo.

python build_tools/create_installer.py

echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
