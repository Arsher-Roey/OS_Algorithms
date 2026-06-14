@echo off
title OS Disk Scheduling Setup
echo ==========================================
echo Starting OS Project Environment Setup...
echo ==========================================
echo.

if exist "venv\Scripts\activate" (
    echo [OK] Virtual environment already exists.
) else (
    echo [+] Creating new virtual environment...
    python -m venv venv
)

echo [+] Activating environment...
call venv\Scripts\activate

echo [+] Installing requirements (CustomTkinter, Matplotlib, etc.)...
pip install -r requirements.txt --quiet

echo.
echo ==========================================
echo Setup Complete! Launching Application...
echo ==========================================
echo.

python main.py

pause