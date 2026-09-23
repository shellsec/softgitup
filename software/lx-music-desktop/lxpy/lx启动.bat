@echo off
REM 默认同时开网页遥控 + 局域网 MCP。只要手机页：lx启动.bat --no-mcp  或  set LX_MCP=0
cd /d "%~dp0"
chcp 65001 >nul

if not defined LX_API_HOST set "LX_API_HOST=127.0.0.1"

set "PY="
where python >nul 2>&1
if not errorlevel 1 set "PY=python"
if not defined PY (
  where py >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo 未找到 Python。请先安装 Python 3，并勾选 Add python.exe to PATH，或确保 py 启动器可用。
  pause
  exit /b 1
)

%PY% -c "import segno" >nul 2>&1
if errorlevel 1 (
  echo 正在安装二维码依赖 segno …
  %PY% -m pip install -r "%~dp0requirements.txt"
  if errorlevel 1 (
    echo 安装 segno 失败时仍会启动遥控，但控制台可能没有二维码。
  )
)

%PY% -u lx_control.py --web %*
if errorlevel 1 (
  echo.
  pause
)
