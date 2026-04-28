@echo off
chcp 65001 >nul
REM GiteeExploreHot 一键：依赖 → 同步 catalog → 生成 hot_repos.json / gitee_downloads.json
REM 可选：run_sync_gitee.bat windows   在同步后再下载 Windows 附件（需索引里已有 URL）
cd /d "%~dp0"

echo ===== GiteeExploreHot 一键同步 =====
echo.

echo [INFO] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python。
    pause
    exit /b 1
)

set "ROOT_REQ=%~dp0..\requirements.txt"
if not exist "%ROOT_REQ%" (
    echo [ERROR] 找不到仓库根 requirements.txt: "%ROOT_REQ%"
    pause
    exit /b 1
)

echo [INFO] Installing dependencies ^(仓库根 requirements.txt^)...
pip install -r "%ROOT_REQ%"
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

echo [INFO] Syncing Gitee catalog ^(catalog/*.json → data/*.json^)...
python "%~dp0scripts\fetch_explore_hot.py" --sleep 0.8
if %errorlevel% neq 0 (
    echo [ERROR] fetch_explore_hot.py 失败。
    pause
    exit /b 1
)

if /i "%~1"=="" goto :done

echo [INFO] Downloading platform: %~1 ...
python "%~dp0scripts\gitee_download.py" --platform "%~1"
if %errorlevel% neq 0 (
    echo [WARN] gitee_download 结束码非 0（可能部分条目无该平台 URL）。
)

:done
echo [INFO] Done. 输出: data\hot_repos.json 、 data\gitee_downloads.json
if /i "%~1"=="" (
    echo       可选: 拖入参数以同步后下载，例如: run_sync_gitee.bat windows
    echo       支持: windows  darwin  linux
)
pause
