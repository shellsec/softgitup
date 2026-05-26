@echo off
chcp 65001 >nul
cd /d "%~dp0"
python report_html.py
start "" "%~dp0reports\index.html"
