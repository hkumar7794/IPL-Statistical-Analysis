@echo off
title IPL Statistical Analysis
cd /d "%~dp0"

echo ==========================================
echo       IPL STATISTICAL ANALYSIS
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo Installing/updating required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed.
    echo Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Starting IPL website...
python -m streamlit run app.py

pause
