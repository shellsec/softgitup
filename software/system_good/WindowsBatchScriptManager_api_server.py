# -*- coding: utf-8 -*-
"""
经测试，本 API 脚本不要加入到 exe 任务列表中，需单独运行；否则由管理器做「全部重启」时，
被一起停止后再拉起会失败（如 python.exe 报 0xc0000142），远程重启会起不来。
若已加入任务列表：以下接口会自动跳过 API 服务（白名单），避免接口先挂：
  /shutdown、/reboot、/restart-all
手动「全部停止」仍会停 API；需要时可单独控制。

通知配置-最好关掉异常通知

API 服务：通过 HTTP 调用主程序的 CLI（优先 exe，无则 main.py），供另一台机器远程启停、添加脚本等。
同一进程提供 MCP（POST /mcp），供 Cursor / Claude 等客户端接入。
也可在 GUI 面板「API: 启动API / 停止API / 重启API」独立管理，无需加入任务列表。

使用方式：
  python WindowsBatchScriptManager_api_server.py [--port 8765] [--host 0.0.0.0]
  python WindowsBatchScriptManager_api_server.py --no-auth --port 8765   # 关闭鉴权，无需 X-API-Key
  python WindowsBatchScriptManager_api_server.py --docs                  # 开启 HTML 接入说明（默认已开）
  python WindowsBatchScriptManager_api_server.py --no-docs               # 根路径 / 只返回 JSON

默认监听 0.0.0.0，可被本机及局域网/外网访问；仅本机访问可加 --host 127.0.0.1。

Python 安装（仅 API 脚本需要；主程序 exe 不需要 Python）：
  官方下载:     https://www.python.org/downloads/
  Windows 页:   https://www.python.org/downloads/windows/
  安装时勾选「Add python.exe to PATH」
  验证:         python --version
  依赖安装:     pip install fastapi uvicorn
                或 pip install fastapi "uvicorn[standard]"

可选 GET /exec 命令执行（默认关闭，高危）：
  见下方「ENABLE_GET_CMD_EXEC」：去掉该行行首 # 后重启本脚本即可启用
  示例: GET /exec?cmd=ipconfig%20/all
  务必开启鉴权（不要用 --no-auth）、修改 API_KEY，勿暴露到公网

接口示例：
  GET  /list          - 列表（需鉴权时加请求头 X-API-Key）
  GET  /status?id=1   - 状态
  POST /start?id=1    - 启动
  POST /stop?id=1     - 停止
  GET  /start?id=1    - 启动（支持 GET）
  GET  /stop?id=1     - 停止（支持 GET）
  GET  /restart?id=1  - 重启（支持 GET）
  POST /update?id=1   - 更新一条（可选 name, path, work_dir, group, script_type, interpreter, args, env_vars, auto_restart, log_output, schedule_*）
  GET  /update?id=1   - 同上（支持 GET）
  GET  /start-all     - 全部启动（支持 GET，便于浏览器/curl 直接访问）
  GET  /stop-all      - 全部停止（支持 GET）
  GET  /restart-all   - 全部重启（支持 GET）
  POST /start-all     - 全部启动
  POST /stop-all      - 全部停止
  POST /restart-all   - 全部重启
  POST /shutdown      - 全部停止后关机（可选 ?force=true）
  GET  /shutdown      - 同上（支持 GET）
  POST /reboot        - 全部停止后重启系统（可选 ?force=true）
  GET  /reboot        - 同上（支持 GET）
  GET  /config-path   - 配置路径
  POST /add?path=...  - 添加（path 必填；可选 args, env_vars, schedule_* 等）
  DELETE /delete?id=  - 删除
  GET  /export        - 导出配置
  POST /import        - 导入配置
  GET  /health        - 健康检查 JSON
  POST /mcp           - MCP（Streamable HTTP）
  GET  /exec?cmd=...  - 执行 cmd 命令（默认未启用，见 ENABLE_GET_CMD_EXEC）
浏览器访问 http://当前IP:8765/ 查看 API / MCP 接入说明与调用示例（不自动打开页面）。
使用 --no-auth 时可不带 X-API-Key，直接请求，例如：
  curl "http://主机:8765/restart?id=1"
  curl "http://主机:8765/start-all"
  curl "http://主机:8765/stop-all"
  curl "http://主机:8765/restart-all"
"""
import json
import os
import socket
import subprocess
import sys
import uuid
from pathlib import Path

try:
    from version import __version__
except ImportError:
    __version__ = "1.1.0"

ROOT = Path(__file__).resolve().parent
# 主程序：Windows 打包后主要为 exe；无 exe 时（开发环境或 Mac/Linux）用 main.py
MAIN_EXE = ROOT / "WindowsBatchScriptManager.exe"
MAIN_SCRIPT = ROOT / "main.py"
API_KEY = os.environ.get("API_KEY", "change-me-in-production")
# 是否关闭鉴权（默认开启鉴权；仅 --no-auth 时设为 True）
DISABLE_AUTH = False
# 是否开启根路径 HTML 接入说明（默认开启；--no-docs 关闭）
ENABLE_DOCS = True

# ---------------------------------------------------------------------------
# 可选：GET /exec 远程执行 cmd 命令（默认关闭）
# 启用方式：去掉下一行行首的 # 后保存并重启 API 服务
# 警告：等同远程 shell；务必鉴权（勿 --no-auth）、强 API_KEY、仅内网使用
# ENABLE_GET_CMD_EXEC = True
try:
    ENABLE_GET_CMD_EXEC
except NameError:
    ENABLE_GET_CMD_EXEC = False

_CMD_EXEC_TIMEOUT = 60
_CMD_EXEC_MAX_OUTPUT = 65536


def run_shell_command(cmd: str, timeout: int = _CMD_EXEC_TIMEOUT):
    """经 cmd.exe /c 执行一条命令，返回 (stdout, stderr, returncode)。"""
    cmd = (cmd or "").strip()
    if not cmd:
        return "", "empty command", -1
    if timeout <= 0 or timeout > 300:
        timeout = _CMD_EXEC_TIMEOUT
    try:
        r = subprocess.run(
            ["cmd.exe", "/c", cmd],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        out = (r.stdout or "")[:_CMD_EXEC_MAX_OUTPUT]
        err = (r.stderr or "")[:_CMD_EXEC_MAX_OUTPUT]
        return out, err, r.returncode
    except subprocess.TimeoutExpired:
        return "", "command timeout (%ss)" % timeout, -1
    except Exception as e:
        return "", str(e), -1


def get_cli_cmd():
    if MAIN_EXE.exists():
        return [str(MAIN_EXE)]
    return [sys.executable, str(MAIN_SCRIPT)]


def _append_optional_cli_args(cmd_args, **kw):
    """将可选字段转为 CLI 参数（仅传入非 None 的项）。"""
    if kw.get("script_args") is not None:
        cmd_args += ["--args", str(kw["script_args"])]
    if kw.get("env_vars") is not None:
        cmd_args += ["--env-vars", str(kw["env_vars"])]
    if kw.get("depends_on") is not None:
        cmd_args += ["--depends-on", str(kw["depends_on"])]
    if kw.get("delay_after_dep") is not None:
        cmd_args += ["--delay-after-dep", str(int(kw["delay_after_dep"]))]
    if kw.get("schedule_enabled") is not None:
        cmd_args += ["--schedule-enabled", "true" if kw["schedule_enabled"] else "false"]
    if kw.get("schedule_action") is not None:
        cmd_args += ["--schedule-action", str(kw["schedule_action"])]
    if kw.get("schedule_type") is not None:
        cmd_args += ["--schedule-type", str(kw["schedule_type"])]
    if kw.get("schedule_time") is not None:
        cmd_args += ["--schedule-time", str(kw["schedule_time"])]
    if kw.get("schedule_interval") is not None:
        cmd_args += ["--schedule-interval", str(int(kw["schedule_interval"]))]
    if kw.get("schedule_weekday") is not None:
        cmd_args += ["--schedule-weekday", str(int(kw["schedule_weekday"]))]
    if kw.get("schedule_day") is not None:
        cmd_args += ["--schedule-day", str(int(kw["schedule_day"]))]
    if kw.get("schedule_once_date") is not None:
        cmd_args += ["--schedule-once-date", str(kw["schedule_once_date"])]
    return cmd_args


def run_cli(*args, json_out=True):
    cmd = get_cli_cmd() + list(args)
    if json_out:
        cmd.append("--json")
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
        return (r.stdout or "").strip(), (r.stderr or "").strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "CLI timeout (120s)", -1
    except Exception as e:
        return "", str(e), -1


try:
    from fastapi import FastAPI, Header, HTTPException, Query, Body, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse, Response, StreamingResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    HTTPException = Exception


def get_lan_ip(timeout: float = 2.0) -> str:
    """探测当前局域网 IPv4，失败返回空字符串。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        infos = socket.gethostbyname_ex(hostname)[2]
        for item in infos:
            if item and not item.startswith("127."):
                return item
    except Exception:
        pass
    return ""


def get_machine_hostname() -> str:
    try:
        return (socket.gethostname() or "").strip()
    except Exception:
        return ""


MCP_PROTOCOL_VERSION = "2025-03-26"
MCP_PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
MCP_TOOLS = [
    {
        "name": "list_scripts",
        "description": "列出所有脚本任务（id、名称、路径、是否运行、PID）。",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "script_status",
        "description": "查询一条脚本的运行状态。id 可以是数字 ID 或名称（支持子串匹配）。",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "脚本 ID 或名称，如 1 或 backup"}},
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "start_script",
        "description": "启动一条脚本。id 可以是数字 ID 或名称。",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "脚本 ID 或名称"}},
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "stop_script",
        "description": "停止一条脚本。id 可以是数字 ID 或名称。",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "脚本 ID 或名称"}},
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "restart_script",
        "description": "重启一条脚本。id 可以是数字 ID 或名称。",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "脚本 ID 或名称"}},
            "required": ["id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "start_all",
        "description": "启动列表中全部脚本。",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "stop_all",
        "description": "停止列表中全部脚本。",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


def _mcp_ok(id_, result):
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def _mcp_err(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def _cli_to_text(out, err, code):
    if code == 0:
        text = (out or "").strip() or '{"ok": true}'
        return text, False
    text = (err or out or "failed").strip()
    return text, True


def execute_mcp_tool(name, arguments):
    """执行 MCP 工具，返回 (text, is_error)。"""
    arguments = arguments or {}
    sid = str(arguments.get("id") or arguments.get("id_or_name") or "").strip()
    if name == "list_scripts":
        return _cli_to_text(*run_cli("--list"))
    if name == "script_status":
        if not sid:
            return "missing id", True
        return _cli_to_text(*run_cli("--status", sid))
    if name == "start_script":
        if not sid:
            return "missing id", True
        return _cli_to_text(*run_cli("--start", sid))
    if name == "stop_script":
        if not sid:
            return "missing id", True
        return _cli_to_text(*run_cli("--stop", sid))
    if name == "restart_script":
        if not sid:
            return "missing id", True
        return _cli_to_text(*run_cli("--restart", sid))
    if name == "start_all":
        return _cli_to_text(*run_cli("--start-all"))
    if name == "stop_all":
        return _cli_to_text(*run_cli("--stop-all"))
    return "Unknown tool: %s" % name, True


def handle_mcp_message(msg):
    """处理一条 JSON-RPC 消息。通知返回 None。"""
    if not isinstance(msg, dict):
        return _mcp_err(None, -32600, "Invalid Request")
    method = msg.get("method")
    if not method:
        return _mcp_err(msg.get("id"), -32600, "Invalid Request")
    if "id" not in msg or str(method).startswith("notifications/"):
        return None
    id_ = msg.get("id")
    params = msg.get("params") or {}
    if not isinstance(params, dict):
        params = {}
    if method == "initialize":
        client_ver = params.get("protocolVersion") or MCP_PROTOCOL_VERSION
        version = client_ver if client_ver in MCP_PROTOCOL_VERSIONS else MCP_PROTOCOL_VERSION
        return _mcp_ok(id_, {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "WindowsBatchScriptManager", "version": __version__},
            "instructions": "管理本机脚本任务。可用工具：list_scripts、script_status、start_script、stop_script、restart_script、start_all、stop_all。id 为数字或名称。",
        })
    if method == "ping":
        return _mcp_ok(id_, {})
    if method == "tools/list":
        return _mcp_ok(id_, {"tools": MCP_TOOLS})
    if method == "tools/call":
        name = str(params.get("name") or "")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            arguments = {}
        text, is_error = execute_mcp_tool(name, arguments)
        return _mcp_ok(id_, {
            "content": [{"type": "text", "text": text}],
            "isError": bool(is_error),
        })
    return _mcp_err(id_, -32601, "Method not found: %s" % method)


def _request_port(request) -> int:
    host = request.headers.get("host") or ""
    if host.startswith("[") and "]:" in host:
        try:
            return int(host.rsplit(":", 1)[1])
        except ValueError:
            pass
    elif host.count(":") == 1:
        try:
            return int(host.split(":")[1])
        except ValueError:
            pass
    return int(request.url.port or 8765)


def _request_api_key(request, x_api_key=None) -> str:
    if x_api_key and str(x_api_key).strip():
        return str(x_api_key).strip()
    auth = (request.headers.get("authorization") or "").strip()
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    q = request.query_params.get("api_key") or request.query_params.get("key")
    return (q or "").strip()


def require_mcp_auth(request, x_api_key=None):
    if DISABLE_AUTH:
        return
    key = _request_api_key(request, x_api_key)
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


def build_docs_html(request) -> str:
    """接入说明页：API + MCP 示例，按当前访问地址 / 局域网 IP / 计算机名生成。"""
    port = _request_port(request)
    lan_ip = get_lan_ip()
    hostname = get_machine_hostname()
    cfg = {
        "version": __version__,
        "port": port,
        "lanIp": lan_ip,
        "hostname": hostname,
        "authEnabled": (not DISABLE_AUTH),
        "apiKey": "" if DISABLE_AUTH else API_KEY,
        "mcpPath": "/mcp",
    }
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
    return DOCS_HTML.replace("__CFG_JSON__", cfg_json)


DOCS_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Batch Script Manager · API / MCP</title>
<style>
  :root{--bg:#1a1a2e;--card:#16213e;--line:#2a2a4a;--text:#e0e0e0;--muted:#9aa4b2;--accent:#00d2ff;--ok:#7fdbca;--warn:#e67e22;--code:#f8b400}
  *{box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Microsoft YaHei",sans-serif;max-width:980px;margin:0 auto;padding:20px;background:var(--bg);color:var(--text)}
  h1{color:var(--accent);border-bottom:2px solid var(--accent);padding-bottom:8px;margin:0 0 8px;font-size:26px}
  h2{color:var(--ok);margin:28px 0 10px;border-left:3px solid var(--ok);padding-left:10px;font-size:18px}
  p,li{line-height:1.55;color:var(--text)}
  .sub{color:var(--muted);margin:0 0 18px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin:10px 0}
  .row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
  .addr{font-family:ui-monospace,Consolas,monospace;color:var(--code);word-break:break-all}
  .btn{background:#0f3460;color:#fff;border:1px solid var(--accent);border-radius:6px;padding:6px 12px;cursor:pointer;font-size:13px}
  .btn:hover{background:#16487c}
  table{width:100%;border-collapse:collapse;margin:8px 0 16px}
  th{background:var(--card);color:var(--accent);text-align:left;padding:8px 12px;border:1px solid var(--line)}
  td{padding:8px 12px;border:1px solid var(--line);vertical-align:top}
  tr:nth-child(even){background:#12182b}
  code{background:var(--card);padding:2px 6px;border-radius:3px;color:var(--code);font-size:13px}
  .method{font-weight:bold;padding:2px 8px;border-radius:3px;font-size:12px;display:inline-block;min-width:50px;text-align:center}
  .get{background:#27ae60;color:#fff}
  .post{background:#2980b9;color:#fff}
  .delete{background:#c0392b;color:#fff}
  .example{background:#0f3460;border:1px solid var(--line);border-radius:6px;padding:12px;margin:6px 0 10px;font-family:ui-monospace,Consolas,monospace;white-space:pre-wrap;font-size:13px;color:#a8e6cf;word-break:break-all}
  .note{color:var(--warn);margin:6px 0}
  .hint{color:var(--muted);font-size:13px}
  a{color:var(--accent)}
</style></head><body>
<h1>Batch Script Manager · API / MCP</h1>
<p class="sub">局域网接入说明。服务不会自动打开本页；用浏览器访问当前 IP 的 <code>/</code> 即可。IP 变了后打开新地址，本页示例会跟着变。</p>
<p id="authNote" class="note"></p>

<h2>接入地址</h2>
<div class="card">
  <div>当前访问：<span class="addr" id="originAddr"></span></div>
  <div>局域网 IP（默认复制这项）：<span class="addr" id="lanAddr"></span></div>
  <div>计算机名（IP 变了优先用）：<span class="addr" id="hostAddr"></span></div>
  <div>本机：<span class="addr" id="localAddr"></span></div>
  <p class="hint">MCP 与 API 共用同一端口。Cursor 里已保存的配置不会自己改 IP；局域网请优先计算机名，或换 IP 后回到本页重新复制。</p>
</div>

<h2>MCP 一键接入</h2>
<div class="card">
  <p>复制 JSON，粘贴到 Cursor <code>Settings → MCP</code>，或项目 <code>.cursor/mcp.json</code> / Claude Desktop 配置。客户端连的是下面的 <code>/mcp</code>。</p>
  <div class="row">
    <button class="btn" type="button" onclick="copyMcp('lan')">复制 MCP（当前 IP）</button>
    <button class="btn" type="button" onclick="copyMcp('hostname')">复制 MCP（计算机名）</button>
    <button class="btn" type="button" onclick="copyMcp('origin')">复制 MCP（当前访问）</button>
    <span id="mcpCopied" class="hint"></span>
  </div>
  <div class="example" id="mcpPreview"></div>
  <p class="hint">MCP 工具：list_scripts、script_status、start_script、stop_script、restart_script、start_all、stop_all。不含关机 / 重启 / exec。</p>
</div>

<h2>API 一键接入</h2>
<div class="card">
  <div class="row">
    <button class="btn" type="button" onclick="copyText(curlExample(), 'apiCopied')">复制 curl</button>
    <button class="btn" type="button" onclick="copyText(pythonExample(), 'apiCopied')">复制 Python</button>
    <button class="btn" type="button" onclick="copyText(jsExample(), 'apiCopied')">复制 fetch</button>
    <span id="apiCopied" class="hint"></span>
  </div>
  <div class="example" id="apiPreview"></div>
</div>

<h2>API 接口</h2>
<table>
  <tr><th>Method</th><th>路径</th><th>说明</th></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/health</code></td><td>健康检查</td></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/list</code></td><td>列出脚本</td></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/status?id=1</code></td><td>查询状态（id 或名称）</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/start?id=1</code></td><td>启动</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/stop?id=1</code></td><td>停止</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/restart?id=1</code></td><td>重启</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/start-all</code></td><td>全部启动</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/stop-all</code></td><td>全部停止</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/restart-all</code></td><td>全部重启</td></tr>
  <tr><td><span class="method post">POST</span></td><td><code>/add?path=...&name=...</code></td><td>添加</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/update?id=1</code></td><td>更新字段</td></tr>
  <tr><td><span class="method delete">DELETE</span></td><td><code>/delete?id=1</code></td><td>删除</td></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/export</code></td><td>导出配置</td></tr>
  <tr><td><span class="method post">POST</span></td><td><code>/import</code></td><td>导入 Body: {"items":[...]}</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/shutdown</code> <code>/reboot</code></td><td>停止托管脚本后关机/重启系统</td></tr>
  <tr><td><span class="method post">POST</span></td><td><code>/mcp</code></td><td>MCP Streamable HTTP</td></tr>
</table>
<p class="hint">鉴权开启时，HTTP 请求加头 <code>X-API-Key</code>。MCP 配置里同样放在 <code>headers</code>。</p>
<script>
const CFG = __CFG_JSON__;
function port(){return CFG.port || 8765}
function lanBase(){return CFG.lanIp ? ("http://"+CFG.lanIp+":"+port()) : ""}
function hostBase(){return CFG.hostname ? ("http://"+CFG.hostname+":"+port()) : ""}
function localBase(){return "http://127.0.0.1:"+port()}
function originBase(){return window.location.origin.replace(/\/$/,"")}
function defaultBase(){return lanBase() || originBase()}
function authHeadersObj(){
  if(!CFG.authEnabled || !CFG.apiKey) return {};
  return {"X-API-Key": CFG.apiKey};
}
function mcpJson(base){
  const server = {url: base + CFG.mcpPath};
  const headers = authHeadersObj();
  if(Object.keys(headers).length) server.headers = headers;
  return JSON.stringify({mcpServers:{"script-manager": server}}, null, 2);
}
function curlExample(){
  const b = defaultBase();
  const h = CFG.authEnabled ? ('-H "X-API-Key: '+CFG.apiKey+'" ') : "";
  return [
    "curl "+h+'"'+b+'/list"',
    "curl -X POST "+h+'"'+b+'/start?id=1"',
    "curl -X POST "+h+'"'+b+'/stop?id=1"',
    "curl -X POST "+h+'"'+b+'/restart?id=1"',
    "curl "+h+'"'+b+'/status?id=1"',
    "curl -X POST "+h+'"'+b+'/start-all"',
    "curl -X POST "+h+'"'+b+'/stop-all"'
  ].join("\n");
}
function pythonExample(){
  const b = defaultBase();
  const keyLine = CFG.authEnabled ? ('headers = {"X-API-Key": '+JSON.stringify(CFG.apiKey)+'}\n') : "headers = {}\n";
  return "import urllib.request, json\n"+keyLine+"req = urllib.request.Request("+JSON.stringify(b+"/list")+", headers=headers)\nprint(json.load(urllib.request.urlopen(req)))";
}
function jsExample(){
  const b = defaultBase();
  const headers = CFG.authEnabled ? ('{ "X-API-Key": '+JSON.stringify(CFG.apiKey)+' }') : "{}";
  return "const r = await fetch("+JSON.stringify(b+"/list")+", { headers: "+headers+" });\nconst data = await r.json();\nconsole.log(data);";
}
function copyText(text, hintId){
  const done = function(){ const el=document.getElementById(hintId); if(el){ el.textContent="已复制"; setTimeout(function(){el.textContent="";}, 1600);} };
  if(navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(text).then(done).catch(function(){ fallbackCopy(text, done); });
  } else fallbackCopy(text, done);
}
function fallbackCopy(text, done){
  const ta=document.createElement("textarea"); ta.value=text; document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); done(); } catch(e) {}
  document.body.removeChild(ta);
}
function copyMcp(kind){
  const base = kind==="hostname" ? hostBase() : (kind==="origin" ? originBase() : defaultBase());
  if(!base){ document.getElementById("mcpCopied").textContent="没有可用地址"; return; }
  copyText(mcpJson(base), "mcpCopied");
  document.getElementById("mcpPreview").textContent = mcpJson(base);
}
function render(){
  document.getElementById("originAddr").textContent = originBase();
  document.getElementById("lanAddr").textContent = lanBase() || "（未探测到）";
  document.getElementById("hostAddr").textContent = hostBase() || "（无计算机名）";
  document.getElementById("localAddr").textContent = localBase();
  document.getElementById("mcpPreview").textContent = mcpJson(defaultBase() || originBase());
  document.getElementById("apiPreview").textContent = curlExample();
  const note = document.getElementById("authNote");
  if(CFG.authEnabled){
    note.textContent = "鉴权已开启，请求头 X-API-Key: " + CFG.apiKey;
  } else {
    note.textContent = "鉴权已关闭（--no-auth）。";
    note.style.color = "#7fdbca";
  }
}
render();
</script>
</body></html>
"""


def require_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if DISABLE_AUTH:
        return
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


def create_app():
    app = FastAPI(title="Batch Script Manager API", version=__version__)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "MCP-Protocol-Version"],
    )

    @app.get("/")
    def root(request: Request):
        if not ENABLE_DOCS:
            return {"status": "ok", "version": __version__}
        return HTMLResponse(content=build_docs_html(request))

    @app.get("/health")
    def api_health():
        return {"status": "ok", "version": __version__, "mcp": "/mcp"}

    def _mcp_headers(session_id=None, extra=None):
        headers = {
            "MCP-Protocol-Version": MCP_PROTOCOL_VERSION,
            "Cache-Control": "no-cache",
        }
        if session_id:
            headers["Mcp-Session-Id"] = session_id
        if extra:
            headers.update(extra)
        return headers

    @app.post("/mcp")
    async def mcp_post(request: Request, x_api_key: str = Header(None, alias="X-API-Key")):
        require_mcp_auth(request, x_api_key)
        try:
            body = await request.json()
        except Exception:
            return JSONResponse(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}},
                status_code=400,
            )
        session_id = request.headers.get("mcp-session-id") or str(uuid.uuid4())
        headers = _mcp_headers(session_id)

        def _dispatch(item):
            return handle_mcp_message(item)

        if isinstance(body, list):
            results = [r for r in (_dispatch(item) for item in body) if r is not None]
            if not results:
                return Response(status_code=202, headers=headers)
            payload = results
        else:
            payload = _dispatch(body)
            if payload is None:
                return Response(status_code=202, headers=headers)

        accept = (request.headers.get("accept") or "").lower()
        if "text/event-stream" in accept and "application/json" not in accept:
            data = json.dumps(payload, ensure_ascii=False)

            async def _sse():
                yield "event: message\ndata: %s\n\n" % data

            return StreamingResponse(_sse(), media_type="text/event-stream", headers=headers)
        return JSONResponse(content=payload, headers=headers)

    @app.get("/mcp")
    async def mcp_get(request: Request, x_api_key: str = Header(None, alias="X-API-Key")):
        require_mcp_auth(request, x_api_key)
        session_id = request.headers.get("mcp-session-id") or str(uuid.uuid4())
        headers = _mcp_headers(session_id)

        async def _sse():
            yield ": connected\n\n"

        return StreamingResponse(_sse(), media_type="text/event-stream", headers=headers)

    @app.delete("/mcp")
    async def mcp_delete(request: Request, x_api_key: str = Header(None, alias="X-API-Key")):
        require_mcp_auth(request, x_api_key)
        return Response(status_code=204)

    @app.get("/config-path")
    def api_config_path(x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--config-path", json_out=False)
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        return PlainTextResponse(out)

    @app.get("/list")
    def api_list(x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--list")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/status")
    def api_status(id_or_name: str = Query(None), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        args = ["--status"] if not id_or_name else ["--status", id_or_name]
        out, err, code = run_cli(*args)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/start")
    def api_start(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--start", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/stop")
    def api_stop(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--stop", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/start")
    def api_start_get(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式启动指定脚本。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--start", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/stop")
    def api_stop_get(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式停止指定脚本。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--stop", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/restart")
    def api_restart(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--restart", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/restart")
    def api_restart_get(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式重启指定脚本，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--restart", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/start-all")
    def api_start_all(x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--start-all")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/stop-all")
    def api_stop_all(x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--stop-all")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/start-all")
    def api_start_all_get(x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式全部启动，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--start-all")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/stop-all")
    def api_stop_all_get(x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式全部停止，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--stop-all")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/restart-all")
    def api_restart_all(x_api_key: str = Header(None, alias="X-API-Key")):
        """全部重启：先 stop-all 再 start-all。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--restart-all")
        if code != 0:
            msg = err or out or "failed"
            import sys as _sys
            print("[restart-all] CLI exit %s stderr: %s" % (code, err), file=_sys.stderr)
            if out:
                print("[restart-all] stdout: %s" % out[:500], file=_sys.stderr)
            raise HTTPException(status_code=500, detail=msg)
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/restart-all")
    def api_restart_all_get(x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式全部重启，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        out, err, code = run_cli("--restart-all")
        if code != 0:
            msg = err or out or "failed"
            import sys as _sys
            print("[restart-all] CLI exit %s stderr: %s" % (code, err), file=_sys.stderr)
            if out:
                print("[restart-all] stdout: %s" % out[:500], file=_sys.stderr)
            raise HTTPException(status_code=500, detail=msg)
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    def _do_power_action(action: str, force: bool = False):
        args = ["--shutdown" if action == "shutdown" else "--reboot"]
        if force:
            args.append("--force")
        out, err, code = run_cli(*args)
        if code != 0:
            raise HTTPException(status_code=500, detail=err or out or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out or action)

    @app.post("/shutdown")
    def api_shutdown(force: bool = Query(False), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        return _do_power_action("shutdown", force=force)

    @app.get("/shutdown")
    def api_shutdown_get(force: bool = Query(False), x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式关机，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        return _do_power_action("shutdown", force=force)

    @app.post("/reboot")
    def api_reboot(force: bool = Query(False), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        return _do_power_action("reboot", force=force)

    @app.get("/reboot")
    def api_reboot_get(force: bool = Query(False), x_api_key: str = Header(None, alias="X-API-Key")):
        """GET 方式重启系统，便于浏览器或 curl 直接访问。"""
        require_api_key(x_api_key)
        return _do_power_action("reboot", force=force)

    @app.post("/add")
    def api_add(
        name: str = Query(""),
        path: str = Query(..., alias="path"),
        work_dir: str = Query(""),
        group: str = Query(""),
        script_type: str = Query(""),
        interpreter: str = Query(""),
        script_args: str = Query("", alias="args"),
        env_vars: str = Query(""),
        auto_restart: bool = Query(False),
        log_output: bool = Query(False),
        schedule_enabled: bool = Query(None),
        schedule_action: str = Query(None),
        schedule_type: str = Query(None),
        schedule_time: str = Query(None),
        schedule_interval: int = Query(None),
        schedule_weekday: int = Query(None),
        schedule_day: int = Query(None),
        schedule_once_date: str = Query(None),
        depends_on: str = Query(""),
        delay_after_dep: int = Query(None),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        cmd_args = ["--add", "--path", path]
        if name:
            cmd_args += ["--name", name]
        if work_dir:
            cmd_args += ["--work-dir", work_dir]
        if group:
            cmd_args += ["--group", group]
        if script_type:
            cmd_args += ["--script-type", script_type]
        if interpreter:
            cmd_args += ["--interpreter", interpreter]
        if auto_restart:
            cmd_args += ["--auto-restart"]
        if log_output:
            cmd_args += ["--log-output"]
        if depends_on:
            cmd_args += ["--depends-on", depends_on]
        _append_optional_cli_args(
            cmd_args,
            script_args=script_args or None,
            env_vars=env_vars or None,
            delay_after_dep=delay_after_dep,
            schedule_enabled=schedule_enabled,
            schedule_action=schedule_action,
            schedule_type=schedule_type,
            schedule_time=schedule_time,
            schedule_interval=schedule_interval,
            schedule_weekday=schedule_weekday,
            schedule_day=schedule_day,
            schedule_once_date=schedule_once_date,
        )
        out, err, code = run_cli(*cmd_args)
        if code != 0:
            raise HTTPException(status_code=400 if "path" in err.lower() else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.delete("/delete")
    def api_delete(id_or_name: str = Query(..., alias="id"), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--delete", id_or_name)
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        return {"ok": True, "message": out or "deleted"}

    def _do_update(
        id_or_name: str,
        name=None,
        path=None,
        work_dir=None,
        group=None,
        script_type=None,
        interpreter=None,
        script_args=None,
        env_vars=None,
        auto_restart=None,
        log_output=None,
        schedule_enabled=None,
        schedule_action=None,
        schedule_type=None,
        schedule_time=None,
        schedule_interval=None,
        schedule_weekday=None,
        schedule_day=None,
        schedule_once_date=None,
        depends_on=None,
        delay_after_dep=None,
    ):
        cmd_args = ["--update", id_or_name]
        if name is not None:
            cmd_args += ["--name", str(name)]
        if path is not None:
            cmd_args += ["--path", str(path)]
        if work_dir is not None:
            cmd_args += ["--work-dir", str(work_dir)]
        if group is not None:
            cmd_args += ["--group", str(group)]
        if script_type is not None:
            cmd_args += ["--script-type", str(script_type)]
        if interpreter is not None:
            cmd_args += ["--interpreter", str(interpreter)]
        if auto_restart is True:
            cmd_args += ["--auto-restart"]
        if auto_restart is False:
            cmd_args += ["--no-auto-restart"]
        if log_output is True:
            cmd_args += ["--log-output"]
        if log_output is False:
            cmd_args += ["--no-log-output"]
        _append_optional_cli_args(
            cmd_args,
            script_args=script_args,
            env_vars=env_vars,
            depends_on=depends_on,
            delay_after_dep=delay_after_dep,
            schedule_enabled=schedule_enabled,
            schedule_action=schedule_action,
            schedule_type=schedule_type,
            schedule_time=schedule_time,
            schedule_interval=schedule_interval,
            schedule_weekday=schedule_weekday,
            schedule_day=schedule_day,
            schedule_once_date=schedule_once_date,
        )
        return run_cli(*cmd_args)

    @app.post("/update")
    def api_update(
        id_or_name: str = Query(..., alias="id"),
        name: str = Query(None),
        path: str = Query(None),
        work_dir: str = Query(None),
        group: str = Query(None),
        script_type: str = Query(None),
        interpreter: str = Query(None),
        script_args: str = Query(None, alias="args"),
        env_vars: str = Query(None),
        auto_restart: bool = Query(None),
        log_output: bool = Query(None),
        schedule_enabled: bool = Query(None),
        schedule_action: str = Query(None),
        schedule_type: str = Query(None),
        schedule_time: str = Query(None),
        schedule_interval: int = Query(None),
        schedule_weekday: int = Query(None),
        schedule_day: int = Query(None),
        schedule_once_date: str = Query(None),
        depends_on: str = Query(None),
        delay_after_dep: int = Query(None),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        out, err, code = _do_update(
            id_or_name,
            name=name,
            path=path,
            work_dir=work_dir,
            group=group,
            script_type=script_type,
            interpreter=interpreter,
            script_args=script_args,
            env_vars=env_vars,
            auto_restart=auto_restart,
            log_output=log_output,
            schedule_enabled=schedule_enabled,
            schedule_action=schedule_action,
            schedule_type=schedule_type,
            schedule_time=schedule_time,
            schedule_interval=schedule_interval,
            schedule_weekday=schedule_weekday,
            schedule_day=schedule_day,
            schedule_once_date=schedule_once_date,
            depends_on=depends_on,
            delay_after_dep=delay_after_dep,
        )
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/update")
    def api_update_get(
        id_or_name: str = Query(..., alias="id"),
        name: str = Query(None),
        path: str = Query(None),
        work_dir: str = Query(None),
        group: str = Query(None),
        script_type: str = Query(None),
        interpreter: str = Query(None),
        script_args: str = Query(None, alias="args"),
        env_vars: str = Query(None),
        auto_restart: bool = Query(None),
        log_output: bool = Query(None),
        schedule_enabled: bool = Query(None),
        schedule_action: str = Query(None),
        schedule_type: str = Query(None),
        schedule_time: str = Query(None),
        schedule_interval: int = Query(None),
        schedule_weekday: int = Query(None),
        schedule_day: int = Query(None),
        schedule_once_date: str = Query(None),
        depends_on: str = Query(None),
        delay_after_dep: int = Query(None),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        out, err, code = _do_update(
            id_or_name,
            name=name,
            path=path,
            work_dir=work_dir,
            group=group,
            script_type=script_type,
            interpreter=interpreter,
            script_args=script_args,
            env_vars=env_vars,
            auto_restart=auto_restart,
            log_output=log_output,
            schedule_enabled=schedule_enabled,
            schedule_action=schedule_action,
            schedule_type=schedule_type,
            schedule_time=schedule_time,
            schedule_interval=schedule_interval,
            schedule_weekday=schedule_weekday,
            schedule_day=schedule_day,
            schedule_once_date=schedule_once_date,
            depends_on=depends_on,
            delay_after_dep=delay_after_dep,
        )
        if code != 0:
            raise HTTPException(status_code=404 if "Not found" in err else 500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.get("/export")
    def api_export(x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        out, err, code = run_cli("--export")
        if code != 0:
            raise HTTPException(status_code=500, detail=err or "failed")
        try:
            return JSONResponse(content=__import__("json").loads(out))
        except Exception:
            return PlainTextResponse(out)

    @app.post("/import")
    def api_import(body: dict = Body(None), replace: bool = Query(False), x_api_key: str = Header(None, alias="X-API-Key")):
        require_api_key(x_api_key)
        if not body or "items" not in body:
            raise HTTPException(status_code=400, detail="Body must be { items: [...] }")
        import tempfile
        import json as _json
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            _json.dump(body, f, ensure_ascii=False, indent=2)
            path = f.name
        try:
            args = ["--import", path]
            if replace:
                args.append("--replace")
            out, err, code = run_cli(*args)
            if code != 0:
                raise HTTPException(status_code=500, detail=err or "failed")
            return {"ok": True, "message": out or "imported"}
        finally:
            try:
                os.unlink(path)
            except Exception:
                pass

    if ENABLE_GET_CMD_EXEC:

        @app.get("/exec")
        def api_exec_get(
            cmd: str = Query(..., description="要执行的命令，如 ipconfig /all"),
            timeout: int = Query(None, ge=1, le=300, description="超时秒数，默认 60"),
            x_api_key: str = Header(None, alias="X-API-Key"),
        ):
            """GET 执行 cmd 命令（需 ENABLE_GET_CMD_EXEC=True）。返回 stdout/stderr/returncode。"""
            require_api_key(x_api_key)
            tout = timeout if timeout is not None else _CMD_EXEC_TIMEOUT
            out, err, code = run_shell_command(cmd, timeout=tout)
            return {
                "ok": code == 0,
                "returncode": code,
                "stdout": out,
                "stderr": err,
                "cmd": cmd,
            }

    return app


def main():
    import argparse
    p = argparse.ArgumentParser(description="Batch Script Manager API Server")
    p.add_argument("--host", default="0.0.0.0", help="Bind host (default 0.0.0.0=all interfaces for external access; use 127.0.0.1 for local only)")
    p.add_argument("--port", type=int, default=8765, help="Port")
    p.add_argument("--api-key", default=None, help="API key (override env API_KEY)")
    p.add_argument("--no-auth", action="store_true", help="Disable authentication; all endpoints (list/start/stop/etc.) can be called without X-API-Key")
    p.add_argument("--docs", action="store_true", help="Enable HTML API/MCP docs page at / (default: on)")
    p.add_argument("--no-docs", action="store_true", help="Disable HTML docs page; / returns JSON only")
    a = p.parse_args()
    if a.api_key:
        global API_KEY
        API_KEY = a.api_key
    if a.no_auth:
        global DISABLE_AUTH
        DISABLE_AUTH = True
    global ENABLE_DOCS
    if a.no_docs:
        ENABLE_DOCS = False
    elif a.docs:
        ENABLE_DOCS = True
    if not HAS_FASTAPI:
        print("Please install: pip install fastapi uvicorn[standard]", file=sys.stderr)
        sys.exit(1)
    import uvicorn
    if DISABLE_AUTH:
        print("Auth: disabled (--no-auth)")
        if a.host == "0.0.0.0":
            print("WARNING: Auth disabled and listening on 0.0.0.0 — do not expose to untrusted networks", file=sys.stderr)
    else:
        print("Auth: enabled, API key (X-API-Key):", API_KEY)
        if API_KEY == "change-me-in-production":
            print("WARNING: Using default API_KEY — set --api-key or env API_KEY before production use", file=sys.stderr)
    if a.host == "0.0.0.0" and API_KEY == "change-me-in-production":
        print("WARNING: Listening on all interfaces with default API key", file=sys.stderr)
    if ENABLE_DOCS:
        print("Docs: enabled, open http://<LAN-IP>:%s/ in a browser (not opened automatically)" % a.port)
        print("MCP:  POST http://<LAN-IP>:%s/mcp" % a.port)
    lan_ip = get_lan_ip()
    hostname = get_machine_hostname()
    if lan_ip:
        print("LAN IP:", "http://%s:%s/" % (lan_ip, a.port))
    if hostname:
        print("Hostname:", "http://%s:%s/" % (hostname, a.port))
    if ENABLE_GET_CMD_EXEC:
        print("WARNING: GET /exec enabled — remote cmd execution; use strong API_KEY, do not use --no-auth on untrusted networks")
        if DISABLE_AUTH:
            print("ERROR: GET /exec cannot run with --no-auth. Remove --no-auth or disable ENABLE_GET_CMD_EXEC.", file=sys.stderr)
            sys.exit(1)
        if a.host == "0.0.0.0" and API_KEY == "change-me-in-production":
            print("ERROR: GET /exec on 0.0.0.0 requires a non-default API_KEY.", file=sys.stderr)
            sys.exit(1)
    print("Listen:", a.host, "port", a.port)
    print()
    print("=" * 60)
    print("  启动参数说明 / Launch Options")
    print("=" * 60)
    print("""  默认:    鉴权开启；根路径 / 为 API/MCP 接入说明页（不会自动打开浏览器）
           MCP 地址 POST /mcp ；健康检查 GET /health

  --no-auth      关闭鉴权，无需 Key 即可调用（方便本地/内网使用）
  --docs         开启 HTML 接入说明（默认已开）
  --no-docs      关闭说明页，/ 只返回 JSON
  --api-key KEY  自定义 API Key
                 默认从环境变量 API_KEY 读取，fallback 为 change-me-in-production

  组合示例:
    python WindowsBatchScriptManager_api_server.py
    python WindowsBatchScriptManager_api_server.py --no-auth
    python WindowsBatchScriptManager_api_server.py --api-key my-secret-key""")
    print()
    print("=" * 60)
    print("  接口示例 / API Endpoints")
    print("=" * 60)
    base = f"http://{a.host}:{a.port}"
    if a.host == "0.0.0.0":
        base = f"http://localhost:{a.port}"
    auth_hint = "（需鉴权时加请求头 X-API-Key）" if not DISABLE_AUTH else ""
    print(f"""  GET  /list          - 列表{auth_hint}
  GET  /status?id=1   - 状态
  POST /start?id=1    - 启动
  POST /stop?id=1     - 停止
  GET  /start?id=1    - 启动（支持 GET）
  GET  /stop?id=1     - 停止（支持 GET）
  GET  /restart?id=1  - 重启（支持 GET）
  POST /update?id=1   - 更新（可选 name, path, work_dir, group, script_type, interpreter, args, env_vars, auto_restart, log_output, schedule_*）
  GET  /update?id=1   - 同上（支持 GET）
  POST /add?path=...  - 添加（path 必填；可选 args, env_vars, schedule_* 等）
  GET  /start-all     - 全部启动（支持 GET，便于浏览器/curl 直接访问）
  GET  /stop-all      - 全部停止（支持 GET）
  GET  /restart-all   - 全部重启（支持 GET）
  POST /start-all     - 全部启动
  POST /stop-all      - 全部停止
  POST /restart-all   - 全部重启
  POST /shutdown      - 全部停止后关机（可选 ?force=true）
  GET  /shutdown      - 同上（支持 GET）
  POST /reboot        - 全部停止后重启系统（可选 ?force=true）
  GET  /reboot        - 同上（支持 GET）
  GET  /config-path   - 配置路径
  DELETE /delete?id=  - 删除
  GET  /export        - 导出配置
  POST /import        - 导入配置
  GET  /health        - 健康检查
  POST /mcp           - MCP（Cursor / Claude 一键接入）
  GET  /exec?cmd=...  - 执行 cmd（默认关闭；去掉脚本内 # ENABLE_GET_CMD_EXEC = True 的 # 后启用）""")
    print()
    print("  curl 示例:")
    if not DISABLE_AUTH:
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/list"')
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/start?id=1"')
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/stop-all"')
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/restart-all"')
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/shutdown"')
        print(f'    curl -H "X-API-Key: {API_KEY}" "{base}/reboot"')
    else:
        print(f'    curl "{base}/list"')
        print(f'    curl "{base}/start?id=1"')
        print(f'    curl "{base}/stop-all"')
        print(f'    curl "{base}/restart-all"')
        print(f'    curl "{base}/shutdown"')
        print(f'    curl "{base}/reboot"')
        print(f'    curl "{base}/start-all"')
        print(f'    curl "{base}/add?path=C:\\\\test.bat&name=Test"')
    print()
    print("=" * 60)
    print()
    uvicorn.run(create_app(), host=a.host, port=a.port)


if __name__ == "__main__":
    main()
