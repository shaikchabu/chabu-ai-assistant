@echo off
title Chabu AI - Voice Terminal
color 0A
cd /d "%~dp0"

echo ========================================
echo   CHABU VOICE ONLY (this window = mic)
echo ========================================
echo.
echo 1. Say: harry potter
echo 2. Then: hello / open google / show notes
echo.

if not exist "venv\Scripts\python.exe" (
    echo ERROR: venv not found. Run start_chabu.bat once after setup.
    pause
    exit /b 1
)

venv\Scripts\python.exe cli_assistant\main.py
pause
