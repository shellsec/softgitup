@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

if not exist "%~dp0catalog.html" (
    echo [ERROR] 未找到 catalog.html
    echo   完整仓库可先运行: python tools\generate_catalog_html.py
    pause
    exit /b 1
)

echo 正在打开分类展示页 catalog.html ...
start "" "%~dp0catalog.html"
exit /b 0
