@echo off
chcp 65001 >nul
cd /d "%~dp0"

python monthly_a_board.py
if errorlevel 1 (
    echo [错误] 生成失败
    pause
    exit /b 1
)

if exist "reports\monthly_a.html" (
    start "" "%~dp0reports\monthly_a.html"
) else (
    echo 未找到 reports\monthly_a.html
    pause
    exit /b 1
)
exit /b 0
