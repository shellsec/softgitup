@echo off
chcp 65001 >nul
echo ========================================
echo SoftGitUp 软件自动更新工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 检查Python脚本是否存在
if not exist "sync_software.py" (
    echo 错误: 找不到 sync_software.py 文件
    echo.
    pause
    exit /b 1
)

REM 检查配置文件是否存在
if not exist "config.json" (
    echo 错误: 找不到 config.json 配置文件
    echo.
    pause
    exit /b 1
)

echo 开始执行软件同步...
echo 执行时间: %date% %time%
echo.

REM 执行Python脚本
python sync_software.py

REM 检查执行结果
if %errorlevel% equ 0 (
    echo.
    echo ✓ 软件同步完成！
) else (
    echo.
    echo ✗ 软件同步失败，错误代码: %errorlevel%
)

echo.
echo 执行完成时间: %date% %time%
echo ========================================
echo.
pause