@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

if exist "%~dp0lookup_app.exe" goto run_exe

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python 或 lookup_app.exe，请先安装 Python 3 或运行 tools\build_exe.ps1 生成 exe。
    pause
    exit /b 1
)
if not "%~1"=="" goto run_py_args
goto prompt_query

:run_exe
if not "%~1"=="" (
    "%~dp0lookup_app.exe" %*
    goto finish
)
:prompt_query
echo.
echo 用法: lookup_app.bat [选项与关键词...]
echo 示例: lookup_app.bat drawio
echo       lookup_app.bat --platform android termux
echo 交互选条目后: 1=立刻下载  2=加入并下载  3=加入列表  4=启用
echo 直接下载: lookup_app.bat -y --download drawio
echo 加入列表后批量更新: run_saved_apps.bat windows
if exist "%~dp0lookup_app.exe" (
    echo 运行: lookup_app.exe
) else (
    echo 更多选项: python lookup_app.py --help
)
echo.
set /p "QUERY=请输入关键词（可含 --platform android 等）: "
if "%QUERY%"=="" (
    echo 未输入，已退出。
    exit /b 0
)
if exist "%~dp0lookup_app.exe" (
    "%~dp0lookup_app.exe" %QUERY%
) else (
    python lookup_app.py %QUERY%
)
goto finish

:run_py_args
python lookup_app.py %*

:finish
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
