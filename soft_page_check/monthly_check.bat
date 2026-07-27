@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 月度快检 · A 类（同步目录相关页面）
echo ========================================
echo.
echo 原则: 不更 software/ 也完全可用；本工具只发现「标题可能变了」的页
echo 破解/423down 下载仍须手工；有变化再 open_changed_pages.bat
echo.

echo [1/3] 刷新 URL 与 A 类监控清单 ...
python extract_pages.py
python build_watchlist.py
echo.

echo [2/3] 抓取 A 类页面标题并比对历史 ...
python fetch_titles.py --scope a --compare
echo.

echo [3/3] 结果
findstr /C:"\"compared_at\"" "reports\last_diff_a.json" >nul 2>&1
if errorlevel 1 (
    echo   [首次运行] 已建立 A 类基线。请再运行本 bat 一次才有标题变化比对。
    goto after_result
)
if exist "changed_tier_a_urls.txt" (
    call :count_lines "changed_tier_a_urls.txt"
    echo   [有变化] A 类 %CHG% 个 -^> 报告页或 open_changed_pages.bat
) else (
    echo   [无比对变化] A 类页面标题与上次一致，本月通常无需更新。
)
:after_result
echo.
echo 月度工作台: open_monthly_a.bat  （旧版本→新版本 · 开源可直下）
echo 季度全量: monthly_check_full.bat  （A+装机+423down+7xiazai）
echo 全量打开:   open_soft_pages.bat
echo 报告页面:   open_report.bat  或  reports\index.html
echo.
python monthly_a_board.py >nul 2>&1
if exist "reports\monthly_a.html" (
    start "" "%~dp0reports\monthly_a.html"
) else if exist "reports\index.html" (
    start "" "%~dp0reports\index.html"
)
echo.
pause
exit /b 0

:count_lines
set "CHG=0"
if not exist "%~1" exit /b 0
for /f "usebackq delims=" %%L in ("%~1") do set /a CHG+=1
exit /b 0
