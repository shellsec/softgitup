@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

echo ===== GH Release Fetch - on-demand download / update =====
echo.

python --version >nul 2>&1
if not errorlevel 1 goto run_py

if exist "%~dp0auto_update.exe" goto run_exe

echo [ERROR] 未找到 Python 或 auto_update.exe
echo   有 Python: 安装 Python 3 后直接运行本 bat
echo   无 Python: powershell -File tools\build_exe.ps1 后复制 dist\exe\auto_update.exe 到本目录
pause
exit /b 1

:run_py
echo [INFO] Python detected.
echo.
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)
echo [INFO] Dependencies OK.
echo.
echo [INFO] Running auto_update.py...
python auto_update.py %*
if %errorlevel% neq 0 (
    echo [ERROR] Update failed. See update_log.txt for details.
    pause
    exit /b 1
)
goto done

:run_exe
echo [INFO] Running auto_update.exe...
"%~dp0auto_update.exe" %*
if %errorlevel% neq 0 (
    echo [ERROR] Update failed. See update_log.txt for details.
    pause
    exit /b 1
)

:done
echo.
echo [INFO] Done.
