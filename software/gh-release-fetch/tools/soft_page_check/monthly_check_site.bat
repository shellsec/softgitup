@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "SITE=%~1"
if "%SITE%"=="" goto usage

if /i "%SITE%"=="423down" goto site_423down
if /i "%SITE%"=="7xiazai" goto site_7xiazai
if /i "%SITE%"=="hybase" goto site_hybase
if /i "%SITE%"=="dayanzai" goto site_dayanzai
if /i "%SITE%"=="down66" goto site_down66

echo 未知站点: %SITE%
goto usage

:site_423down
echo === 423down digest 快检 ===
call refresh_urls.bat 423down nopause || goto fail
python fetch_titles.py --scope 423down --compare || goto fail
call :summary changed_423down_urls.txt last_diff_423down.json 423down
goto finish

:site_7xiazai
echo === 7xiazai 快检（系统+移动）===
call refresh_urls.bat 7xiazai nopause || goto fail
python fetch_titles.py --scope 7xiazai_system --compare || goto fail
call :summary changed_7xiazai_system_urls.txt last_diff_7xiazai_system.json 7xiazai系统
python fetch_titles.py --scope 7xiazai_mobile --compare || goto fail
call :summary changed_7xiazai_mobile_urls.txt last_diff_7xiazai_mobile.json 7xiazai移动
goto finish

:site_hybase
echo === hybase 快检（系统+移动）===
python fetch_titles.py --scope hybase_system --compare || goto fail
call :summary changed_hybase_system_urls.txt last_diff_hybase_system.json hybase系统
python fetch_titles.py --scope hybase_mobile --compare || goto fail
call :summary changed_hybase_mobile_urls.txt last_diff_hybase_mobile.json hybase移动
goto finish

:site_dayanzai
echo === dayanzai 快检（系统+移动）===
python fetch_titles.py --scope dayanzai_system --compare || goto fail
call :summary changed_dayanzai_system_urls.txt last_diff_dayanzai_system.json dayanzai系统
python fetch_titles.py --scope dayanzai_mobile --compare || goto fail
call :summary changed_dayanzai_mobile_urls.txt last_diff_dayanzai_mobile.json dayanzai移动
goto finish

:site_down66
echo === down66 快检（系统+移动）===
python fetch_titles.py --scope down66_system --compare || goto fail
call :summary changed_down66_system_urls.txt last_diff_down66_system.json down66系统
python fetch_titles.py --scope down66_mobile --compare || goto fail
call :summary changed_down66_mobile_urls.txt last_diff_down66_mobile.json down66移动
goto finish

:summary
if not exist "reports\%~2" (
    echo   [%~3] 首次运行，已建基线。再跑一遍才有比对。
    goto :eof
)
if exist "%~1" (
    call :count "%~1"
    echo   [%~3] 标题变化: %N% 个
) else (
    echo   [%~3] 无比对变化
)
goto :eof

:count
set "N=0"
for /f "usebackq delims=" %%L in ("%~1") do set /a N+=1
exit /b 0

:finish
if exist "reports\index.html" if /i not "%~2"=="nopause" if not defined SOFT_PAGE_CHECK_NO_PAUSE start "" "%~dp0reports\index.html"
if /i not "%~2"=="nopause" if not defined SOFT_PAGE_CHECK_NO_PAUSE pause
exit /b 0

:fail
echo [错误] 快检中断
pause
exit /b 1

:usage
echo 用法: monthly_check_site.bat ^<站点^>
echo   423down  7xiazai  hybase  dayanzai  down66
echo.
echo 多站连跑: monthly_check_list.bat
echo 全量:     monthly_check_full.bat
pause
exit /b 1
