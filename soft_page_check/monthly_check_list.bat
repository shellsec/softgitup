@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo list 四站快检（hybase/dayanzai/down66/7xiazai · 系统/移动）
echo ========================================
echo.
echo 刷新 URL 清单（7xiazai + dayanzai/down66 系统区）...
python extract_7xiazai_pages.py
if errorlevel 1 goto fail
python extract_list_system_urls.py
if errorlevel 1 goto fail
echo.

for %%S in (hybase_system hybase_mobile dayanzai_system dayanzai_mobile down66_system down66_mobile 7xiazai_system 7xiazai_mobile) do (
    echo ========== %%S ==========
    python fetch_titles.py --scope %%S --compare
    if errorlevel 1 goto fail
    echo.
)

echo ============================================================
echo  完成 - 报告页按站点分组，系统/移动变化分开显示
echo ============================================================
if exist "reports\index.html" start "" "%~dp0reports\index.html"
pause
exit /b 0

:fail
echo [错误] 快检中断
pause
exit /b 1
