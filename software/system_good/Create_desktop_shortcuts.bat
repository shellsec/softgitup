@echo off
chcp 65001 >nul
setlocal

title 一键创建桌面快捷方式

echo ========================================
echo    一键创建桌面快捷方式
echo ========================================
echo.
echo 默认创建与任务栏相同的软件列表（system_good + 同级常用工具）
echo 路径自适应: 脚本在 system_good 内，软件根为其上一级
echo.
echo 可选: -IncludeOptional  -IncludeMaintenance  -DesktopOnly
echo.

set "PS1=%~dp0Create_desktop_shortcuts.ps1"
if not exist "%PS1%" (
    echo [ERROR] 找不到 %PS1%
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
set "RC=%ERRORLEVEL%"

echo.
if %RC% neq 0 (echo [ERROR] 部分失败，错误码 %RC%) else (echo [OK] 执行完成)
echo.
pause
exit /b %RC%
