@echo off
REM 仓库根 = 本目录上两级（VibeCodingToolsDown\tools -> 仓库根）
set "REPO_ROOT=%~dp0..\.."
cd /d "%REPO_ROOT%"
python tools\reset_enabled_json.py --apps-dir VibeCodingToolsDown %*
