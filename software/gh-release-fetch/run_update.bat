@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

echo ===== GH Release Fetch - on-demand download / update =====
echo.

if exist "%~dp0auto_update.exe" goto run_exe

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python 或 auto_update.exe。请安装 Python 3 或运行 tools\build_exe.ps1。
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python detected.
echo.

echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)
echo [INFO] Dependencies OK.
echo.

echo [INFO] Running auto_update.py...
python auto_update.py
if %errorlevel% neq 0 (
    echo [ERROR] Update failed. See update_log.txt for details.
    pause
    exit /b 1
)
goto done

:run_exe
echo [INFO] Running auto_update.exe...
"%~dp0auto_update.exe"
if %errorlevel% neq 0 (
    echo [ERROR] Update failed. See update_log.txt for details.
    pause
    exit /b 1
)

:done
echo.
echo [INFO] Done.
