@echo off
echo ===== GH Release Fetch - on-demand download / update =====
echo.

rm *.html

REM Check Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install Python 3.6 or newer.
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detected.
echo.

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)
echo [INFO] Dependencies OK.
echo.

REM Run updater
echo [INFO] Running auto_update.py...
python auto_update.py
if %errorlevel% neq 0 (
    echo [ERROR] Update failed. See update_log.txt for details.
    pause
    exit /b 1
)

echo.
echo [INFO] Done.
