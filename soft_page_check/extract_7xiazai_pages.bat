@echo off
chcp 65001 >nul
cd /d "%~dp0"
python extract_7xiazai_pages.py
if %errorlevel% neq 0 pause & exit /b 1
pause
