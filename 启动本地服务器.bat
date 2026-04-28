@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title SoftGitUp 本地文件服务器

echo ========================================
echo SoftGitUp 本地文件服务器
echo ========================================
echo.

:: 设置服务器端口（默认8000）
set "PORT=8000"

:: 检查端口参数
if not "%~1"=="" set "PORT=%~1"

:: 获取当前目录
set "BASE_DIR=%~dp0"

echo 服务器目录: %BASE_DIR%
echo 服务器端口: %PORT%
echo.
echo 访问地址: http://localhost:%PORT%/
echo 软件列表: http://localhost:%PORT%/software/list.txt
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python
    echo.
    pause
    exit /b 1
)

:: 启动 Python HTTP 服务器
cd /d "%BASE_DIR%"
python -m http.server %PORT%

pause

