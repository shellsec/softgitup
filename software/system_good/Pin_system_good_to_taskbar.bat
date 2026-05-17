@echo off
chcp 65001 >nul
setlocal

title 一键固定到任务栏 (Win10/Win11)

echo ========================================
echo    一键固定到任务栏 (Win10 / Win11)
echo ========================================
echo.
echo 默认固定: system_good 五件套 + Notepad++/Everything 等同级常用软件
echo 路径自适应: D:\Program Files\system_good -^> 同级 D:\Program Files\*
echo.
echo 可选: -IncludeOptional  -IncludeMaintenance  -RestartExplorer  -PinMode FolderOnly
echo.

set "PS1=%~dp0Pin_system_good_to_taskbar.ps1"
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
