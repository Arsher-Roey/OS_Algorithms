@echo off
title OS Disk Scheduling Setup
echo ==========================================
echo Starting OS Project Environment Setup...
echo ==========================================
echo.

:: Check if the virtual environment folder already exists
if exist "venv\Scripts\activate" (
    echo [OK] Virtual environment already exists.
) else (
    echo [+] Creating new virtual environment...
    python -m venv venv
)

:: Activate the environment
echo [+] Activating environment...
call venv\Scripts\activate

:: Install the required libraries quietly
echo [+] Installing requirements (CustomTkinter, Matplotlib, etc.)...
pip install -r requirements.txt --quiet

echo.
echo ==========================================
echo Setup Complete! Launching Application...
echo ==========================================
echo.

:: Run the main python file (Change 'main.py' if your file is named something else!)
python main.py

pause