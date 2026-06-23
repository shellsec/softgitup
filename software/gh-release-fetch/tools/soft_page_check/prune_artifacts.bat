@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 清理可再生的历史快照、旧 report_*.txt、__pycache__ …
python prune_artifacts.py %*
pause
