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

if "%~1"=="" (
    echo 用法: lookup_app.bat ^<关键词^> [更多关键词...]
    echo 示例: lookup_app.bat drawio
    echo       lookup_app.bat --platform windows cherrytree
    echo 加入更新列表后一键更新: run_saved_apps.bat windows
    echo 更多选项: python lookup_app.py --help
    pause
    exit /b 1
)

python lookup_app.py %*
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
