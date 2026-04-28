@echo off
REM 仅在 VibeCodingToolsDown 目录内；通过 vibe_update.py 调用上级 auto_update.py
cd /d "%~dp0"

echo ===== VibeCodingToolsDown 一键更新 =====
echo.

echo [INFO] Checking Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python。
    pause
    exit /b 1
)

echo [INFO] Installing dependencies...
pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

echo [INFO] Building manifest...
python "%~dp0scripts\build_manifest.py"
if %errorlevel% neq 0 (
    echo [WARN] build_manifest 有告警；若 manifest.json 已存在则继续。
)

echo [INFO] Running vibe_update.py ...
python "%~dp0vibe_update.py"
if %errorlevel% neq 0 (
    echo [ERROR] 更新失败，见仓库根目录 update_log.txt。
    pause
    exit /b 1
)

echo [INFO] Done.
pause
