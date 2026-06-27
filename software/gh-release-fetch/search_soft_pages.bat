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

if not "%~1"=="" goto run_args

echo.
echo 用法: search_soft_pages.bat [选项与关键词...]
echo 示例: search_soft_pages.bat 7zip
echo       search_soft_pages.bat dayanzai 优化
echo       search_soft_pages.bat --scope a github
echo       search_soft_pages.bat --stats
echo.
echo 搜索 soft_page_check 已抓取的介绍页标题并打开链接。
echo 与 lookup_app.bat（GitHub 清单）互补：后者偏 Releases，前者偏各站介绍页。
echo 建立标题索引: tools\soft_page_check\monthly_check.bat
echo 更多选项: python tools\soft_page_check\search_pages.py --help
echo.
set /p "QUERY=请输入关键词（可含 --scope a 等）: "
if "%QUERY%"=="" (
    echo 未输入，已退出。
    exit /b 0
)
python tools\soft_page_check\search_pages.py %QUERY%
goto finish

:run_args
python tools\soft_page_check\search_pages.py %*

:finish
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% neq 0 pause
exit /b %EXITCODE%
