@echo off
chcp 65001 >nul
setlocal
set "BASE_DIR=%~dp0"
set "BASE_DIR=%BASE_DIR:~0,-1%"

echo ========================================
echo SoftGitUp - 仅生成软件列表
echo ========================================
echo.

if exist "%BASE_DIR%\Lastb_soft_version.txt" (
    echo 正在更新 Lastb_soft_version.txt 到 software\system_good ...
    copy /Y "%BASE_DIR%\Lastb_soft_version.txt" "%BASE_DIR%\software\system_good\Lastb_soft_version.txt" >nul
    if %errorlevel% equ 0 (
        echo [OK] Lastb_soft_version.txt 已更新
    ) else (
        echo [WARN] 复制 Lastb_soft_version.txt 失败
    )
    echo.
) else (
    echo [INFO] 根目录未找到 Lastb_soft_version.txt，跳过
    echo.
)

echo 正在生成软件列表...
python soft_manager.py --generate-only

if %errorlevel% equ 0 (
    echo.
    echo 软件列表生成成功！
    echo 正在刷新 README.md 中的 software 体积统计...
    python update_readme_size.py
    echo [OK] 请运行 push_git.bat 提交并推送.
    echo.
    echo 操作完成！
) else (
    echo.
    echo 操作失败，请检查错误信息
)

echo.

push_git.bat

