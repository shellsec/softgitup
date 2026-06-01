@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo down66 快检（系统 + 移动 分开比对）
echo ========================================
echo.

echo --- 系统 (PC，清单为空则跳过) ---
python fetch_titles.py --scope down66_system --compare
if errorlevel 1 goto fail
call :show down66_system changed_down66_system_urls.txt

echo.
echo --- 移动 (Android app) ---
python fetch_titles.py --scope down66_mobile --compare
if errorlevel 1 goto fail
call :show down66_mobile changed_down66_mobile_urls.txt

if exist "reports\index.html" start "" "%~dp0reports\index.html"
pause
exit /b 0

:show
findstr /C:"\"compared_at\"" "reports\last_diff_%~1.json" >nul 2>&1
if errorlevel 1 (
    echo   [首次] %~1 已建基线或已跳过
    goto :eof
)
if exist "%~2" (
    call :count "%~2"
    echo   [%~1] 标题变化: %N% 个
) else (
    echo   [%~1] 无比对变化
)
goto :eof

:count
set "N=0"
for /f "usebackq delims=" %%L in ("%~1") do set /a N+=1
exit /b 0

:fail
pause
exit /b 1
