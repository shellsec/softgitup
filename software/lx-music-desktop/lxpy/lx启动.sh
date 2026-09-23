#!/usr/bin/env bash
# macOS / Linux 一键启动网页遥控（默认同时开局域网 MCP）。Windows 请用 lx启动.bat。
# 只要手机页：./lx启动.sh --no-mcp  或  LX_MCP=0 ./lx启动.sh
set -euo pipefail
cd "$(dirname "$0")"

# 默认认为洛雪桌面端就在这台电脑上。要连另一台机器上的洛雪：
#   LX_API_HOST=192.168.x.x ./启动.sh
export LX_API_HOST="${LX_API_HOST:-127.0.0.1}"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "未找到 Python 3。请先安装 python3，再执行: chmod +x 启动.sh && ./启动.sh" >&2
  exit 1
fi

if ! "$PY" -c "import segno" >/dev/null 2>&1; then
  echo "正在安装二维码依赖 segno …"
  "$PY" -m pip install -r "$(dirname "$0")/requirements.txt" || echo "安装 segno 失败时仍会启动遥控，但可能没有二维码。" >&2
fi

exec "$PY" -u lx_control.py --web "$@"
