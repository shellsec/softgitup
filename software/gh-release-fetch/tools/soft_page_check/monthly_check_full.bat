@echo off
chcp 65001 >nul
cd /d "%~dp0"

type "%~dp0full_check_intro.txt"
echo.

call "%~dp0refresh_urls.bat" all nopause
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
python fetch_titles.py --scope 423down --compare
if errorlevel 1 goto fail
call :summary changed_423down_urls.txt last_diff_423down.json 423down

echo.
echo ========== 4/10 7xiazai 系统 ==========
python fetch_titles.py --scope 7xiazai_system --compare
if errorlevel 1 goto fail
call :summary changed_7xiazai_system_urls.txt last_diff_7xiazai_system.json 7xiazai系统

echo.
echo ========== 5/10 7xiazai 移动 ==========
python fetch_titles.py --scope 7xiazai_mobile --compare
if errorlevel 1 goto fail
call :summary changed_7xiazai_mobile_urls.txt last_diff_7xiazai_mobile.json 7xiazai移动

echo.
echo ========== 6/10 hybase 系统 ==========
python fetch_titles.py --scope hybase_system --compare
if errorlevel 1 goto fail
call :summary changed_hybase_system_urls.txt last_diff_hybase_system.json hybase系统

echo.
echo ========== 7/10 hybase 移动 ==========
python fetch_titles.py --scope hybase_mobile --compare
if errorlevel 1 goto fail
call :summary changed_hybase_mobile_urls.txt last_diff_hybase_mobile.json hybase移动

echo.
echo ========== 8/10 dayanzai 系统 ==========
python fetch_titles.py --scope dayanzai_system --compare
if errorlevel 1 goto fail
call :summary changed_dayanzai_system_urls.txt last_diff_dayanzai_system.json dayanzai系统

echo.
echo ========== 9/10 dayanzai 移动 ==========
python fetch_titles.py --scope dayanzai_mobile --compare
if errorlevel 1 goto fail
call :summary changed_dayanzai_mobile_urls.txt last_diff_dayanzai_mobile.json dayanzai移动

echo.
echo ========== 10/12 down66 系统 ==========
python fetch_titles.py --scope down66_system --compare
if errorlevel 1 goto fail
call :summary changed_down66_system_urls.txt last_diff_down66_system.json down66系统

echo.
echo ========== 11/12 down66 移动 ==========
python fetch_titles.py --scope down66_mobile --compare
if errorlevel 1 goto fail
call :summary changed_down66_mobile_urls.txt last_diff_down66_mobile.json down66移动

echo.
echo ============================================================
echo  全量快检完成 - 报告页核心分区 + list 四站(系统/移动)
echo ============================================================
echo  打开变化页:
echo    A类/装机  open_changed_pages.bat [all]
echo    其它站点  open_changed_site.bat ^<423down^|7xiazai^|hybase^|dayanzai^|down66^>
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
