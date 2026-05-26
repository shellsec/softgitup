@echo off
chcp 65001 >nul
cd /d "%~dp0"
python build_watchlist.py
if %errorlevel% neq 0 pause & exit /b 1
pause
