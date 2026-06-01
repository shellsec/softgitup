# -*- coding: utf-8 -*-
"""
经测试，本 API 脚本不要加入到 exe 任务列表中，需单独运行；否则由管理器做「全部重启」时，
被一起停止后再拉起会失败（如 python.exe 报 0xc0000142），远程重启会起不来。
若已加入任务列表：以下接口会自动跳过 API 服务（白名单），避免接口先挂：
  /shutdown、/reboot、/restart-all
手动「全部停止」仍会停 API；需要时可单独控制。

通知配置-最好关掉异常通知

API 服务：通过 HTTP 调用主程序的 CLI（优先 exe，无则 main.py），供另一台机器远程启停、添加脚本等。
也可在 GUI 面板「API: 启动API / 停止API / 重启API」独立管理，无需加入任务列表。

使用方式：
  python WindowsBatchScriptManager_api_server.py [--port 8765] [--host 0.0.0.0]
  python WindowsBatchScriptManager_api_server.py --no-auth --port 8765   # 关闭鉴权，无需 X-API-Key
  python WindowsBatchScriptManager_api_server.py --no-auth --docs        # 关闭鉴权 + 开启 HTML 文档页面

默认监听 0.0.0.0，可被本机及局域网/外网访问；仅本机访问可加 --host 127.0.0.1。
依赖：pip install fastapi uvicorn

接口示例：
  GET  /list          - 列表（需鉴权时加请求头 X-API-Key）
  GET  /status?id=1   - 状态
  POST /start?id=1    - 启动
  POST /stop?id=1     - 停止
  GET  /start?id=1    - 启动（支持 GET）
  GET  /stop?id=1     - 停止（支持 GET）
  GET  /restart?id=1  - 重启（支持 GET）
  POST /update?id=1   - 更新一条（可选 name, path, work_dir, group, script_type, interpreter, auto_restart, log_output）
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
  POST /add           - 添加脚本
  DELETE /delete?id=  - 删除
  GET  /export        - 导出配置
  POST /import        - 导入配置
使用 --no-auth 时可不带 X-API-Key，直接请求，例如：
  curl "http://主机:8765/restart?id=1"
  curl "http://主机:8765/start-all"
  curl "http://主机:8765/stop-all"
  curl "http://主机:8765/restart-all"
"""
import os
import subprocess
import sys
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
# 是否关闭鉴权（--no-auth 时设为 True，默认关闭鉴权方便使用；去掉 --no-auth 即开启鉴权）
DISABLE_AUTH = True
# 是否开启根路径 HTML 文档页面（--docs 时设为 True）
ENABLE_DOCS = False


def get_cli_cmd():
    if MAIN_EXE.exists():
        return [str(MAIN_EXE)]
    return [sys.executable, str(MAIN_SCRIPT)]


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
    from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


def require_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if DISABLE_AUTH:
        return
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


def create_app():
    app = FastAPI(title="Batch Script Manager API", version=__version__)

    @app.get("/")
    def root(request: Request):
        if not ENABLE_DOCS:
            return {"status": "ok", "version": __version__}
        base = str(request.base_url).rstrip("/")
        auth_note = ""
        if not DISABLE_AUTH:
            auth_note = '<p style="color:#e67e22;margin:4px 0">🔐 Auth enabled — add header <code>X-API-Key: YOUR_KEY</code></p>'
        html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Batch Script Manager API</title>
<style>
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:900px;margin:0 auto;padding:20px;background:#1a1a2e;color:#e0e0e0}}
  h1{{color:#00d2ff;border-bottom:2px solid #00d2ff;padding-bottom:8px}}
  h2{{color:#7fdbca;margin-top:28px;border-left:3px solid #7fdbca;padding-left:10px}}
  table{{width:100%;border-collapse:collapse;margin:8px 0 16px}}
  th{{background:#16213e;color:#00d2ff;text-align:left;padding:8px 12px;border:1px solid #2a2a4a}}
  td{{padding:8px 12px;border:1px solid #2a2a4a}}
  tr:nth-child(even){{background:#16213e}}
  code{{background:#16213e;padding:2px 6px;border-radius:3px;color:#f8b400;font-size:13px}}
  .method{{font-weight:bold;padding:2px 8px;border-radius:3px;font-size:12px;display:inline-block;min-width:50px;text-align:center}}
  .get{{background:#27ae60;color:#fff}}
  .post{{background:#2980b9;color:#fff}}
  .delete{{background:#c0392b;color:#fff}}
  .example{{background:#0f3460;border:1px solid #2a2a4a;border-radius:6px;padding:12px;margin:6px 0 14px;font-family:monospace;white-space:pre-wrap;font-size:13px;color:#a8e6cf;word-break:break-all}}
  a{{color:#00d2ff}}
</style></head><body>
<h1>🚀 Batch Script Manager API</h1>
{auth_note}

<h2>⚡ 快捷控制 (Quick Control)</h2>
<table>
  <tr><th>Method</th><th>Endpoint</th><th>说明</th></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/start-all</code></td><td>启动所有脚本</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/stop-all</code></td><td>停止所有脚本</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/restart-all</code></td><td>重启所有脚本</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/shutdown</code></td><td>停止所有脚本后关机</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/reboot</code></td><td>停止所有脚本后重启系统</td></tr>
</table>

<h2>🎯 单脚本控制 (Single Script)</h2>
<table>
  <tr><th>Method</th><th>Endpoint</th><th>说明</th></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/start?id=1</code></td><td>启动脚本 (id 或 name)</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/stop?id=1</code></td><td>停止脚本</td></tr>
  <tr><td><span class="method get">GET</span> <span class="method post">POST</span></td><td><code>/restart?id=1</code></td><td>重启脚本</td></tr>
</table>

<h2>📊 查询 & 状态 (Query & Status)</h2>
<table>
  <tr><th>Method</th><th>Endpoint</th><th>说明</th></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/list</code></td><td>列出所有脚本</td></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/status?id=1</code></td><td>查询脚本状态 (id 或 name)</td></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/config-path</code></td><td>获取配置文件路径</td></tr>
</table>

<h2>📝 管理 (Manage)</h2>
<table>
  <tr><th>Method</th><th>Endpoint</th><th>说明</th></tr>
  <tr><td><span class="method post">POST</span></td><td><code>/add?path=C:\\test.bat&name=Test</code></td><td>添加脚本</td></tr>
  <tr><td></td><td><code>&group=&script_type=&interpreter=&auto_restart=&log_output=</code></td><td>可选参数</td></tr>
  <tr><td><span class="method post">POST</span> <span class="method get">GET</span></td><td><code>/update?id=1</code></td><td>更新脚本字段</td></tr>
  <tr><td></td><td><code>&name=&path=&work_dir=&group=&script_type=&interpreter=&auto_restart=&log_output=</code></td><td>可选参数</td></tr>
  <tr><td><span class="method delete">DELETE</span></td><td><code>/delete?id=1</code></td><td>删除脚本</td></tr>
</table>

<h2>📥 导入导出 (Import & Export)</h2>
<table>
  <tr><th>Method</th><th>Endpoint</th><th>说明</th></tr>
  <tr><td><span class="method get">GET</span></td><td><code>/export</code></td><td>导出配置为 JSON</td></tr>
  <tr><td><span class="method post">POST</span></td><td><code>/import</code></td><td>导入配置 Body: {{"items": [...]}}</td></tr>
  <tr><td></td><td><code>?replace=true</code></td><td>替换所有现有项</td></tr>
</table>

<h2>💡 快速示例 (Examples)</h2>
<div class="example">curl "{base}/start-all"
curl "{base}/stop-all"
curl "{base}/restart-all"
curl "{base}/start?id=1"
curl "{base}/stop?id=my-script"
curl "{base}/list"
curl "{base}/status?id=1"
curl "{base}/add?path=C:\\\\test.bat&amp;name=Test"
curl -X DELETE "{base}/delete?id=1"</div>
</body></html>"""
        return HTMLResponse(content=html)

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
        auto_restart: bool = Query(False),
        log_output: bool = Query(False),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        args = ["--add", "--path", path]
        if name:
            args += ["--name", name]
        if work_dir:
            args += ["--work-dir", work_dir]
        if group:
            args += ["--group", group]
        if script_type:
            args += ["--script-type", script_type]
        if interpreter:
            args += ["--interpreter", interpreter]
        if auto_restart:
            args += ["--auto-restart"]
        if log_output:
            args += ["--log-output"]
        out, err, code = run_cli(*args)
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

    def _do_update(id_or_name: str, name=None, path=None, work_dir=None, group=None, script_type=None, interpreter=None, auto_restart=None, log_output=None):
        args = ["--update", id_or_name]
        if name is not None:
            args += ["--name", str(name)]
        if path is not None:
            args += ["--path", str(path)]
        if work_dir is not None:
            args += ["--work-dir", str(work_dir)]
        if group is not None:
            args += ["--group", str(group)]
        if script_type is not None:
            args += ["--script-type", str(script_type)]
        if interpreter is not None:
            args += ["--interpreter", str(interpreter)]
        if auto_restart is True:
            args += ["--auto-restart"]
        if auto_restart is False:
            args += ["--no-auto-restart"]
        if log_output is True:
            args += ["--log-output"]
        if log_output is False:
            args += ["--no-log-output"]
        return run_cli(*args)

    @app.post("/update")
    def api_update(
        id_or_name: str = Query(..., alias="id"),
        name: str = Query(None),
        path: str = Query(None),
        work_dir: str = Query(None),
        group: str = Query(None),
        script_type: str = Query(None),
        interpreter: str = Query(None),
        auto_restart: bool = Query(None),
        log_output: bool = Query(None),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        out, err, code = _do_update(id_or_name, name=name, path=path, work_dir=work_dir, group=group, script_type=script_type, interpreter=interpreter, auto_restart=auto_restart, log_output=log_output)
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
        auto_restart: bool = Query(None),
        log_output: bool = Query(None),
        x_api_key: str = Header(None, alias="X-API-Key"),
    ):
        require_api_key(x_api_key)
        out, err, code = _do_update(id_or_name, name=name, path=path, work_dir=work_dir, group=group, script_type=script_type, interpreter=interpreter, auto_restart=auto_restart, log_output=log_output)
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

    return app


def main():
    import argparse
    p = argparse.ArgumentParser(description="Batch Script Manager API Server")
    p.add_argument("--host", default="0.0.0.0", help="Bind host (default 0.0.0.0=all interfaces for external access; use 127.0.0.1 for local only)")
    p.add_argument("--port", type=int, default=8765, help="Port")
    p.add_argument("--api-key", default=None, help="API key (override env API_KEY)")
    p.add_argument("--no-auth", action="store_true", help="Disable authentication; all endpoints (list/start/stop/etc.) can be called without X-API-Key")
    p.add_argument("--docs", action="store_true", help="Enable HTML API docs page at root path /")
    a = p.parse_args()
    if a.api_key:
        global API_KEY
        API_KEY = a.api_key
    if a.no_auth:
        global DISABLE_AUTH
        DISABLE_AUTH = True
    if a.docs:
        global ENABLE_DOCS
        ENABLE_DOCS = True
    if not HAS_FASTAPI:
        print("Please install: pip install fastapi uvicorn[standard]", file=sys.stderr)
        sys.exit(1)
    import uvicorn
    if DISABLE_AUTH:
        print("Auth: disabled (--no-auth)")
    else:
        print("Auth: enabled, API key (X-API-Key):", API_KEY)
    if ENABLE_DOCS:
        print("Docs: enabled (--docs), visit / for HTML API docs")
    print("Listen:", a.host, "port", a.port)
    print()
    print("=" * 60)
    print("  启动参数说明 / Launch Options")
    print("=" * 60)
    print("""  默认:    鉴权开启，所有接口需带 X-API-Key 请求头
           根路径 / 只返回 {"status":"ok"}，不暴露接口信息

  --no-auth      关闭鉴权，无需 Key 即可调用（方便本地/内网使用）
  --docs         开启 HTML 文档页面，浏览器访问 / 查看接口文档
  --api-key KEY  自定义 API Key
                 默认从环境变量 API_KEY 读取，fallback 为 change-me-in-production

  组合示例:
    python WindowsBatchScriptManager_api_server.py --no-auth
    python WindowsBatchScriptManager_api_server.py --no-auth --docs
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
  POST /update?id=1   - 更新（可选 name, path, work_dir, group, script_type, interpreter, auto_restart, log_output）
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
  POST /add           - 添加脚本
  DELETE /delete?id=  - 删除
  GET  /export        - 导出配置
  POST /import        - 导入配置""")
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
