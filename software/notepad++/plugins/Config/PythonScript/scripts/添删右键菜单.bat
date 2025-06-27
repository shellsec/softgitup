@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 脚本标题
title Notepad++右键菜单管理

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠ 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

:: 查找Notepad++.exe路径
set "exe_path=D:\Program Files\notepad\notepad++.exe"

if not exist "%exe_path%" (
    echo ❌ 错误：未找到 Notepad++.exe
    echo 预期路径: %exe_path%
    echo 请确认Notepad++已正确安装
    pause
    exit /b 1
)

echo ✅ 找到Notepad++.exe: %exe_path%

:: 主菜单
:menu
cls
echo ==============================
echo    Notepad++ 右键菜单管理
echo ==============================
echo 1. 添加右键菜单
echo 2. 删除右键菜单
echo 3. 退出
echo ==============================
set /p choice=请选择操作[1-3]:

if "%choice%"=="1" goto add_menu
if "%choice%"=="2" goto del_menu
if "%choice%"=="3" exit /b
goto menu

:: 添加右键菜单
:add_menu
reg add "HKCR\*\shell\Notepad++" /ve /d "用 Notepad++ 打开" /f
reg add "HKCR\*\shell\Notepad++" /v "Icon" /d "\"%exe_path%\"" /f
reg add "HKCR\*\shell\Notepad++\command" /ve /d "\"%exe_path%\" \"%%1\"" /f
echo ✅ 右键菜单添加成功！
pause
goto menu

:: 删除右键菜单
:del_menu
reg delete "HKCR\*\shell\Notepad++" /f
echo ✅ 右键菜单删除成功！
pause
goto menu