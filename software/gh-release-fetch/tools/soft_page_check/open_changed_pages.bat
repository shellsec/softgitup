@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "MODE=%~1"
set "URL_FILE="

if /i "%MODE%"=="all" (
    set "URL_FILE=%~dp0changed_pages_urls.txt"
    echo 打开全部有变化的页面
) else (
    if exist "%~dp0changed_tier_a_urls.txt" (
        set "URL_FILE=%~dp0changed_tier_a_urls.txt"
        echo 打开 A 类有变化的页面（推荐）
    ) else if exist "%~dp0changed_pages_urls.txt" (
        set "URL_FILE=%~dp0changed_pages_urls.txt"
        echo 打开全部有变化的页面
    ) else (
        echo 找不到 changed_tier_a_urls.txt / changed_pages_urls.txt
        echo 请先运行 monthly_check.bat
        pause
        exit /b 1
    )
)

echo 列表: %URL_FILE%
echo.

set /a n=0
for /f "usebackq delims=" %%u in ("%URL_FILE%") do (
    set "line=%%u"
    if not "!line!"=="" (
        set /a n+=1
        echo [!n!] !line!
        start "" "!line!"
        timeout /t 1 /nobreak >nul
    )
)

if !n! equ 0 (
    echo 列表为空，当前无需打开。
) else (
    echo.
    echo 已打开 !n! 个待核查页面。
    echo 确认要更新后: 手工下载 -^> 替换 software/ -^> generate_and_push.bat
)
pause
