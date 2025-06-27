@echo off
chcp 65001 >nul
echo ========================================
echo           SoftGitUp 快速开始
echo ========================================
echo.
echo 请选择要执行的操作：
echo.
echo 1. 运行系统测试
echo 2. 启动管理工具（生成软件列表）
echo 3. 启动同步工具（后台运行）
echo 4. 安装Python依赖
echo 5. 打包成可执行文件
echo 6. 查看使用说明
echo 7. 退出
echo.
set /p choice=请输入选择 (1-7): 

if "%choice%"=="1" (
    echo.
    echo 运行系统测试...
    python test_sync.py
    pause
    goto :eof
)

if "%choice%"=="2" (
    echo.
    echo 启动管理工具...
    python soft_manager.py
    pause
    goto :eof
)

if "%choice%"=="3" (
    echo.
    echo 启动同步工具...
    echo 注意：同步工具将在后台运行，请查看系统托盘图标
    python soft_sync.py
    goto :eof
)

if "%choice%"=="4" (
    echo.
    echo 安装Python依赖...
    pip install -r requirements.txt
    pause
    goto :eof
)

if "%choice%"=="5" (
    echo.
    echo 打包成可执行文件...
    python build_exe.py
    pause
    goto :eof
)

if "%choice%"=="6" (
    echo.
    echo 打开使用说明...
    start 使用说明.md
    goto :eof
)

if "%choice%"=="7" (
    echo.
    echo 退出程序
    goto :eof
)

echo.
echo 无效选择，请重新运行脚本
pause 