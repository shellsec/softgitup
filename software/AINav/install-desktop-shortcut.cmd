@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist "%~dp0index.html" (
  echo [ERROR] index.html not found next to this script.
  pause
  exit /b 1
)
if not exist "%~dp0cr.html" (
  echo [ERROR] cr.html not found next to this script.
  pause
  exit /b 1
)
if not exist "%~dp0install-nav-shortcut.ps1" (
  echo [ERROR] install-nav-shortcut.ps1 not found next to this script.
  pause
  exit /b 1
)

"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-nav-shortcut.ps1" -IndexHtmlPath "%~dp0index.html"
if errorlevel 1 (
  echo.
  echo PowerShell step failed for index.html.
  pause
  exit /b 1
)

"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-nav-shortcut.ps1" -IndexHtmlPath "%~dp0cr.html" -ShortcutName "CR-Navigator.url" -NoOpen
if errorlevel 1 (
  echo.
  echo PowerShell step failed for cr.html.
  pause
  exit /b 1
)

echo.
echo Done. Desktop shortcuts (English names avoid garbled Chinese labels):
echo   AI-Navigator.url
echo   CR-Navigator.url
echo If Desktop failed, see the .url files next to the HTML files.
echo If a page did not open, double-click the .url file.
exit
