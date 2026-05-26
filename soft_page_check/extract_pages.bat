@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 从 Lastb_soft_version.txt 提取页面 URL ...
python extract_pages.py
if %errorlevel% neq 0 pause & exit /b 1
echo 完成。
pause
