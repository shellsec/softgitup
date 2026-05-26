@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 7xiazai 软件页快检（可选，非默认）
echo ========================================
echo.
echo 范围: 从列表页发现的软件详情页 title（含版本号）
echo 刷新 URL: extract_7xiazai_pages.bat  （改 max_page 见 7xiazai_config.json）
echo.

python extract_7xiazai_pages.py
echo.
python fetch_titles.py --scope 7xiazai --compare
echo.

findstr /C:"\"compared_at\"" "reports\last_diff_7xiazai.json" >nul 2>&1
if errorlevel 1 (
    echo [首次运行] 已建立 7xiazai 基线。请再运行本 bat 一次才有比对结果。
    goto after_result
)
if exist "changed_7xiazai_urls.txt" (
    call :count_lines "changed_7xiazai_urls.txt"
    echo [有变化] %CHG% 个 -^> open_changed_7xiazai.bat
) else (
    echo [无比对变化] 软件页标题与上次一致。
)
:after_result
echo.
if exist "reports\index.html" start "" "%~dp0reports\index.html"
pause
exit /b 0

:count_lines
set "CHG=0"
if not exist "%~1" exit /b 0
for /f "usebackq delims=" %%L in ("%~1") do set /a CHG+=1
exit /b 0
