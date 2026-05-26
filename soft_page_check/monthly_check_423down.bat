@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 423down digest 全量快检（可选，非默认）
echo ========================================
echo.
echo 范围: Lastb_soft_version.txt 中 digest 区
echo 数量: 约 350+ 条去重链接，预计 1-2 分钟
echo 说明: 噪声较多，建议季度运行；日常请用 monthly_check.bat
echo.

echo [1/2] 提取 digest 区 423down 链接 ...
python extract_423down_digest.py
echo.

echo [2/2] 抓取标题并比对历史 ...
python fetch_titles.py --scope 423down --compare
echo.

if exist "changed_423down_urls.txt" (
    call :count_lines "changed_423down_urls.txt"
    echo [有变化] %CHG% 个 -^> open_changed_423down.bat
    goto after_result
)
findstr /C:"\"compared_at\"" "reports\last_diff_423down.json" >nul 2>&1
if errorlevel 1 (
    echo [首次运行] 已建立 digest 基线。请再运行本 bat 一次才有比对结果。
) else (
    echo [无比对变化] digest 标题与上次一致。
)
:after_result
echo.
if exist "reports\index.html" start "" "%~dp0reports\index.html"
echo.
pause
exit /b 0

:count_lines
set "CHG=0"
if not exist "%~1" exit /b 0
for /f "usebackq delims=" %%L in ("%~1") do set /a CHG+=1
exit /b 0
