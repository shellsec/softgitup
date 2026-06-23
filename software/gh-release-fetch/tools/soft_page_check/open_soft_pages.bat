@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "URL_FILE=%BASE%soft_pages_urls.txt"
if not exist "%URL_FILE%" (
    echo 找不到 URL 列表，先运行 refresh_urls.bat pages
    pause
    exit /b 1
)

echo.
echo 批量打开软件介绍页面（不含直链下载）
echo 来源: Lastb_soft_version.txt （最终选择指南 之前）
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

echo.
echo 已全部打开，共 !n! 个页面。
pause
