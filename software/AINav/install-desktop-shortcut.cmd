@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist "%~dp0index.html" (
  echo [ERROR] index.html not found next to this script.
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
  echo PowerShell step failed.
  pause
  exit /b 1
)

echo.
echo Done. Desktop shortcut: AI-Navigator.url  (English name avoids garbled Chinese labels)
echo If Desktop failed, see AI-Navigator.url next to index.html.
echo If the page did not open, double-click the .url file.
exit
