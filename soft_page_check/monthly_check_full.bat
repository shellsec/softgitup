@echo off
chcp 65001 >nul
cd /d "%~dp0"

type "%~dp0full_check_intro.txt"
echo.

python extract_pages.py
if errorlevel 1 goto fail
python build_watchlist.py
if errorlevel 1 goto fail

echo ========== 1/4 A 类 - config.json 同步软件 ==========
python fetch_titles.py --scope a --compare
if errorlevel 1 goto fail
call :summary changed_tier_a_urls.txt last_diff_a.json A类

echo.
echo ========== 2/4 装机区 - 指南之前全部页面 ==========
python fetch_titles.py --scope all --compare
if errorlevel 1 goto fail
call :summary changed_pages_urls.txt last_diff_all.json 装机区

echo.
echo ========== 3/4 423down digest ==========
python extract_423down_digest.py
if errorlevel 1 goto fail
python fetch_titles.py --scope 423down --compare
if errorlevel 1 goto fail
call :summary changed_423down_urls.txt last_diff_423down.json 423down

echo.
echo ========== 4/4 7xiazai 列表 ==========
python extract_7xiazai_pages.py
if errorlevel 1 goto fail
python fetch_titles.py --scope 7xiazai --compare
if errorlevel 1 goto fail
call :summary changed_7xiazai_urls.txt last_diff_7xiazai.json 7xiazai

echo.
echo ============================================================
echo  全量快检完成 - 报告页四个分区均已刷新
echo ============================================================
echo  打开变化页:
echo    A类      open_changed_pages.bat
echo    装机区   open_changed_pages.bat all
echo    423down  open_changed_423down.bat
echo    7xiazai  open_changed_7xiazai.bat
echo.
if exist "reports\index.html" start "" "%~dp0reports\index.html"
pause
exit /b 0

:summary
set "CHG_FILE=%~1"
set "DIFF_JSON=%~2"
set "LABEL=%~3"
if not exist "reports\%DIFF_JSON%" (
    echo   [%LABEL%] 首次运行，已建基线。再跑一遍全量 bat 才有比对。
    goto :eof
)
call :count_lines "%CHG_FILE%"
if %CHG% gtr 0 (
    echo   [%LABEL%] 标题变化: %CHG% 个
) else (
    echo   [%LABEL%] 无比对变化
)
goto :eof

:count_lines
set "CHG=0"
if not exist "%~1" exit /b 0
for /f "usebackq delims=" %%L in ("%~1") do set /a CHG+=1
exit /b 0

:fail
echo.
echo [错误] 全量快检中断，请查看上方 Python 输出。
pause
exit /b 1
