@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0"

echo ============================================================
echo  GH Release Fetch — Windows 便携包一键打包
echo  1. 编译 exe  2. 复制到仓库根  3. 生成 dist\release\*.zip
echo ============================================================
echo.

echo [1/3] 编译 exe （tools\build_exe.ps1）...
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\build_exe.ps1"
if errorlevel 1 goto fail

echo.
echo [2/3] 复制 dist\exe\*.exe 到仓库根...
if not exist "dist\exe\lookup_app.exe" (
    echo [ERROR] 未找到 dist\exe\*.exe，编译可能失败。
    goto fail
)
copy /Y "dist\exe\*.exe" . >nul
echo     已更新: lookup_app run_saved_apps search_soft_pages search_games auto_update

echo.
echo [3/3] 打包 Release （tools\pack_windows_release.ps1 -SkipBuild）...
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\pack_windows_release.ps1" -SkipBuild %*
if errorlevel 1 goto fail

echo.
echo ============================================================
echo  完成。请上传: dist\release\gh-release-fetch-windows-*.zip
echo  本地试跑:   dist\release\gh-release-fetch-windows-*\
echo ============================================================
echo.
echo 可选: pack_windows_release.bat -Version 1.0.0
echo 仅重打 zip（不编译）: powershell -File tools\pack_windows_release.ps1 -SkipBuild
pause
exit /b 0

:fail
echo.
echo [失败] 打包中断。
pause
exit /b 1
