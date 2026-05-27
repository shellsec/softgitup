@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

python reset_enabled_json.py %*
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
