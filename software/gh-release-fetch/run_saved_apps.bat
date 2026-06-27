@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

if exist "%~dp0run_saved_apps.exe" (
    "%~dp0run_saved_apps.exe" %*
    set EXITCODE=%ERRORLEVEL%
    if %EXITCODE% neq 0 pause
    exit /b %EXITCODE%
)

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python 或 run_saved_apps.exe，请先安装 Python 3 或运行 tools\build_exe.ps1。
    pause
    exit /b 1
)

REM 用法:
REM   run_saved_apps.bat
REM   run_saved_apps.bat windows
REM   run_saved_apps.bat my_list.json
REM   set SAVED_APPS_LIST=my_list.json
REM 列表 JSON 可在任意位置；未指定时默认仓库根 saved_apps_<平台>.json
python tools\run_saved_apps.py %*
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
