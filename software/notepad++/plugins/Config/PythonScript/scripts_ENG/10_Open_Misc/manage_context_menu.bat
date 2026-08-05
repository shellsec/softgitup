@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

title Notepad++ Context Menu Manager

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Warning: Please run this script as administrator!
    pause
    exit /b 1
)

set "exe_path="
for %%P in (
    "D:\Program Files\notepad++\notepad++.exe"
    "C:\Program Files\Notepad++\notepad++.exe"
    "C:\Program Files (x86)\Notepad++\notepad++.exe"
) do (
    if exist %%~P (
        set "exe_path=%%~P"
        goto :found
    )
)

echo Error: notepad++.exe not found in common install paths.
echo Edit this bat and set exe_path manually if needed.
pause
exit /b 1

:found
echo Found Notepad++.exe: %exe_path%

:menu
cls
echo ==============================
echo    Notepad++ Context Menu Manager
echo ==============================
echo 1. Add context menu
echo 2. Remove context menu
echo 3. Exit
echo ==============================
set /p choice=Please select operation [1-3]:

if "%choice%"=="1" goto add_menu
if "%choice%"=="2" goto del_menu
if "%choice%"=="3" exit /b
goto menu

:add_menu
reg add "HKCR\*\shell\Notepad++" /ve /d "Open with Notepad++" /f
reg add "HKCR\*\shell\Notepad++" /v "Icon" /d "\"%exe_path%\"" /f
reg add "HKCR\*\shell\Notepad++\command" /ve /d "\"%exe_path%\" \"%%1\"" /f
echo Context menu added successfully!
pause
goto menu

:del_menu
reg delete "HKCR\*\shell\Notepad++" /f
echo Context menu removed successfully!
pause
goto menu
