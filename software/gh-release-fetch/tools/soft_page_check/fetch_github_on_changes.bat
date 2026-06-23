@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo soft_page_check · GitHub Release 下载
echo ========================================
echo.
echo 依据快检变化 URL（github.com）引用本仓库 gh-release-fetch 配置下载
echo 配置目录: apps\  （只读，不在此修改工具）
echo.

python github_fetch_on_changes.py %*
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
    echo 完成。安装包/logs 见 gh-release-fetch 下载目录（由 auto_update 配置）
) else (
    echo [错误] 下载失败，见上方输出
)
if /i not "%~1"=="--dry-run" pause
exit /b %RC%
