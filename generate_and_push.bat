@echo off
chcp 65001 >nul
echo ========================================
echo SoftGitUp - 一键生成和推送工具
echo ========================================
echo.

echo 正在生成软件列表...
python soft_manager.py

if %errorlevel% equ 0 (
    echo.
    echo 软件列表生成成功！
    echo 已自动推送到GitHub
    echo.
    echo 操作完成！
) else (
    echo.
    echo 操作失败，请检查错误信息
)

echo.


pause 