@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python，请先安装 Python 3。
    pause
    exit /b 1
)

python tools\apply_enabled_snapshot.py %*
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
