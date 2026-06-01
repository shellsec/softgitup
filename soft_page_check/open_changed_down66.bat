@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo 打开 down66 标题变化（系统 + 移动）
echo.

call :open_file changed_down66_system_urls.txt "系统"
call :open_file changed_down66_mobile_urls.txt "移动"
pause
exit /b 0

:open_file
set "F=%~dp0%~1"
if not exist "%F%" (
    echo [跳过] %~2 — 无 %~1
    goto :eof
)
set /a n=0
for /f "usebackq delims=" %%u in ("%F%") do (
    set "line=%%u"
    if not "!line!"=="" (
        set /a n+=1
        echo [!n!][%~2] !line!
        start "" "!line!"
        timeout /t 1 /nobreak >nul
    )
)
if !n! equ 0 echo [%~2] 列表为空
goto :eof
