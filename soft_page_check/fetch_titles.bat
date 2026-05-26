@echo off
chcp 65001 >nul
cd /d "%~dp0"
python fetch_titles.py --scope a --compare
pause
