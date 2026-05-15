@echo off
cd /d "%~dp0"
set "PS1=%~dp0Clear-PythonScriptScripts.ps1"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS_EXE%" set "PS_EXE=powershell.exe"
echo Clearing scripts, scripts_ENG, scripts_CHS if present...
"%PS_EXE%" -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
if errorlevel 1 pause
