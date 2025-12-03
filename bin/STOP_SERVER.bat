@echo off
chcp 65001 >nul
title إيقاف السيرفر - Stop Server
color 0C

echo ═══════════════════════════════════════════════════════
echo    ⛔ إيقاف السيرفر - Stopping Server
echo ═══════════════════════════════════════════════════════
echo.

REM Kill Python processes running app.py
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Date Factory Manager*" 2>nul
taskkill /F /IM app.exe 2>nul

echo.
echo ✅ تم إيقاف السيرفر بنجاح
echo    Server stopped successfully
echo.
pause
