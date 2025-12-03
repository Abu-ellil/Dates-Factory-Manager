@echo off
title Date Factory Manager - Quick Start

echo Starting Date Factory Manager...
echo Please wait...

REM Navigate to the project directory and start the server
cd /d "%~dp0"
python src/app.py
