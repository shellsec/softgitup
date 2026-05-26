@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "URL_FILE=%~dp0changed_7xiazai_urls.txt"
if not exist "%URL_FILE%" (
    echo 找不到 changed_7xiazai_urls.txt
    echo 请先运行 monthly_check_7xiazai.bat（需跑两次才有比对）
    pause
    exit /b 1
)

echo 打开 7xiazai 有标题变化的页面
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

if !n! equ 0 (echo 列表为空。) else (echo. & echo 已打开 !n! 个页面。)
pause
