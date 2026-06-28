@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=core"
set "NOPAUSE=%~2"

if /i "%TARGET%"=="core" goto core
if /i "%TARGET%"=="pages" goto pages_only
if /i "%TARGET%"=="watchlist" goto watchlist_only
if /i "%TARGET%"=="423down" goto digest_only
if /i "%TARGET%"=="gamer520" goto gamer520_only
if /i "%TARGET%"=="7xiazai" goto xiazai_only
if /i "%TARGET%"=="all" goto all_targets
goto usage

:all_targets
call :run_pages || goto fail
call :run_watchlist || goto fail
call :run_423down || goto fail
call :run_7xiazai || goto fail
goto finish

:core
call :run_pages || goto fail
call :run_watchlist || goto fail
goto finish

:pages_only
call :run_pages || goto fail
goto finish

:watchlist_only
call :run_watchlist || goto fail
goto finish

:digest_only
call :run_423down || goto fail
goto finish

:gamer520_only
call :run_gamer520 || goto fail
goto finish

:xiazai_only
call :run_7xiazai || goto fail
goto finish

:run_pages
echo [refresh] extract_pages.py
python extract_pages.py
exit /b %errorlevel%

:run_watchlist
echo [refresh] build_watchlist.py
python build_watchlist.py
exit /b %errorlevel%

:run_423down
echo [refresh] extract_423down_digest.py
python extract_423down_digest.py
exit /b %errorlevel%

:run_gamer520
echo [refresh] extract_gamer520_urls.py --pages 50
python extract_gamer520_urls.py --pages 50
exit /b %errorlevel%

:run_7xiazai
echo [refresh] extract_7xiazai_pages.py
python extract_7xiazai_pages.py
exit /b %errorlevel%

:finish
if /i not "%NOPAUSE%"=="nopause" pause
exit /b 0

:fail
if /i not "%NOPAUSE%"=="nopause" pause
exit /b 1

:usage
echo 用法: refresh_urls.bat [目标] [nopause]
echo   core      装机区 URL + A/B 分级（默认，月度快检用）
echo   all       core + 423down digest + 7xiazai 列表
echo   pages     仅 extract_pages
echo   watchlist 仅 build_watchlist（需先有 soft_pages_urls.txt）
echo   423down   仅 digest 区 423down 链接
echo   gamer520  仅 gamer520 近期文章列表（首页分页）
echo   7xiazai   仅 7xiazai 软件页列表
pause
exit /b 1
