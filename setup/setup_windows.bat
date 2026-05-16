@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

cd /d "%PROJECT_DIR%"

echo ========================================
echo Breitling AeroSpace Evo Clock - Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or later.
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/3] Installing dependencies...
call venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [3/3] Setup complete!
echo.
echo To run the watch:
echo   venv\Scripts\python main.py
echo.
echo Or create a shortcut with:
echo   Target: %CD%\venv\Scripts\python.exe "%CD%\main.py"
echo.
pause