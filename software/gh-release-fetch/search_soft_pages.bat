@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

python --version >nul 2>&1
if not errorlevel 1 (
    python tools\soft_page_check\search_pages.py %*
    goto finish
)

if exist "%~dp0search_soft_pages.exe" (
    "%~dp0search_soft_pages.exe" %*
    goto finish
)

echo [ERROR] 未找到 Python 或 search_soft_pages.exe
echo   有 Python: 安装 Python 3 后直接运行本 bat
echo   无 Python: powershell -File tools\build_exe.ps1 后复制 dist\exe\search_soft_pages.exe 到本目录
pause
exit /b 1

:finish
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
