@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo software/ 开源包 · 只下载不安装
echo ========================================
echo apps: win_memory_cleaner everything_cli ditto win11_debloat win11_debloat_scavin lx_music_desktop notepadplusplus notepad_minusminus 7zip
echo 映射: gh_soft_map.json （只读引用 gh-release-fetch）
echo 会先清空再下载到 software\gh-release-fetch\windows\（gitignore，不入库）
echo.
python github_fetch_on_changes.py --soft-map
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (echo 完成。包在 software\gh-release-fetch\windows\ ，请手工覆盖到 software\) else (echo [错误] 见上方输出)
pause
exit /b %RC%
