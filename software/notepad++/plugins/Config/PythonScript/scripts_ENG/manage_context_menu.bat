@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Script title
title Notepad++ Context Menu Manager

:: Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Warning: Please run this script as administrator!
    pause
    exit /b 1
)

:: Find Notepad++.exe path
set "exe_path=D:\Program Files\notepad\notepad++.exe"

if not exist "%exe_path%" (
    echo Error: Notepad++.exe not found
    echo Expected path: %exe_path%
    echo Please confirm Notepad++ is installed correctly
    pause
    exit /b 1
)

echo Found Notepad++.exe: %exe_path%

:: Main menu
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

:: Add context menu
:add_menu
reg add "HKCR\*\shell\Notepad++" /ve /d "Open with Notepad++" /f
reg add "HKCR\*\shell\Notepad++" /v "Icon" /d "\"%exe_path%\"" /f
reg add "HKCR\*\shell\Notepad++\command" /ve /d "\"%exe_path%\" \"%%1\"" /f
echo Context menu added successfully!
pause
goto menu

:: Remove context menu
:del_menu
reg delete "HKCR\*\shell\Notepad++" /f
echo Context menu removed successfully!
pause
goto menu

