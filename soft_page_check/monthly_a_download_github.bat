@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo A 类月度 · 下载本月 GitHub 变化（只下载不安装）
echo ========================================
echo apps: win11_debloat_scavin
echo 会先清空再下载到 software\gh-release-fetch\windows\（gitignore）
echo.
python github_fetch_on_changes.py --scope a
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (echo 完成。包在 windows\ 目录，请手工覆盖到 software\) else (echo [错误] 见上方输出)
pause
exit /b %RC%
