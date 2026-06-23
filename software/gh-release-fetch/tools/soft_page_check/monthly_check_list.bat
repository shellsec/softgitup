@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo list 三站 + 7xiazai 快检（系统/移动）
echo ========================================
echo.

set "SOFT_PAGE_CHECK_NO_PAUSE=1"
for %%S in (7xiazai hybase dayanzai down66) do (
    echo.
    call "%~dp0monthly_check_site.bat" %%S nopause
    if errorlevel 1 goto fail
)
set "SOFT_PAGE_CHECK_NO_PAUSE="

echo ============================================================
echo  完成 - 报告页按站点分组，系统/移动变化分开显示
echo ============================================================
if exist "reports\index.html" start "" "%~dp0reports\index.html"
pause
exit /b 0

:fail
set "SOFT_PAGE_CHECK_NO_PAUSE="
echo [错误] 快检中断
pause
exit /b 1
