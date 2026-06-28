@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "SITE=%~1"
if "%SITE%"=="" goto usage

if /i "%SITE%"=="a" (
    call :open_one "changed_tier_a_urls.txt" "A类"
    goto done
)
if /i "%SITE%"=="all" (
    call :open_one "changed_pages_urls.txt" "装机区全量"
    goto done
)
if /i "%SITE%"=="423down" (
    call :open_one "changed_423down_urls.txt" "423down"
    goto done
)
if /i "%SITE%"=="gamer520" (
    call :open_one "changed_gamer520_urls.txt" "gamer520"
    goto done
)
if /i "%SITE%"=="hybase" (
    call :open_one "changed_hybase_system_urls.txt" "hybase系统"
    call :open_one "changed_hybase_mobile_urls.txt" "hybase移动"
    goto done
)
if /i "%SITE%"=="dayanzai" (
    call :open_one "changed_dayanzai_system_urls.txt" "dayanzai系统"
    call :open_one "changed_dayanzai_mobile_urls.txt" "dayanzai移动"
    goto done
)
if /i "%SITE%"=="down66" (
    call :open_one "changed_down66_system_urls.txt" "down66系统"
    call :open_one "changed_down66_mobile_urls.txt" "down66移动"
    goto done
)
if /i "%SITE%"=="7xiazai" (
    call :open_one "changed_7xiazai_system_urls.txt" "7xiazai系统"
    call :open_one "changed_7xiazai_mobile_urls.txt" "7xiazai移动"
    goto done
)

echo 未知站点: %SITE%
goto usage

:open_one
set "F=%~dp0%~1"
if not exist "%F%" (
    echo [跳过] %~2 — 无 %~1
    goto :eof
)
set /a n=0
for /f "usebackq delims=" %%u in ("%F%") do (
    set "line=%%u"
    if not "!line!"=="" (
        set /a n+=1
        echo [!n!][%~2] !line!
        start "" "!line!"
        timeout /t 1 /nobreak >nul
    )
)
if !n! equ 0 echo [%~2] 列表为空
goto :eof

:done
pause
exit /b 0

:usage
echo 用法: open_changed_site.bat ^<站点^>
echo   a 423down gamer520 hybase dayanzai down66 7xiazai all
echo.
echo A 类变化仍可用: open_changed_pages.bat
pause
exit /b 1
