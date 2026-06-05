@echo off
title Chabu AI - Dashboard
color 0A
cd /d "%~dp0"

echo ==================================================
echo                STARTING CHABU AI
echo ==================================================
echo.
echo  WINDOW 1 = Voice (mic + speaker)  -- say harry potter
echo  WINDOW 2 = Browser dashboard
echo.

if not exist "venv312\Scripts\python.exe" (
    echo ERROR: venv312 not found.
    pause
    exit /b 1
)

start "Chabu Voice" cmd /k "cd /d %~dp0 && venv312\Scripts\python.exe cli_assistant\main.py"

timeout /t 3 /nobreak >nul

venv312\Scripts\python.exe -m streamlit run web_assistant\app.py

pause
