@echo off
echo ============================================================
echo Restarting Date Factory Manager Server
echo ============================================================
echo.

REM Kill any running Python processes for this app
echo Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Date Factory*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting server...
echo.

cd /d "%~dp0"
python src\app.py

pause
