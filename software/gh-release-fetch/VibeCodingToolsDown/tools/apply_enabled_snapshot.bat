@echo off
set "REPO_ROOT=%~dp0..\.."
cd /d "%REPO_ROOT%"
python tools\apply_enabled_snapshot.py --snapshot-path VibeCodingToolsDown/tools/last_enabled_before_reset.json %*
