# -*- coding: utf-8 -*-
"""
经测试，本 API 脚本不要加入到 exe 任务列表中，需单独运行；否则由管理器做「全部重启」时，
被一起停止后再拉起会失败（如 python.exe 报 0xc0000142），远程重启会起不来。

通知配置-最好关掉异常通知

API 服务：通过 HTTP 调用主程序的 CLI（优先 exe，无则 main.py），供另一台机器远程启停、添加脚本等。

使用方式：
  python WindowsBatchScriptManager_api_server.py [--port 8765] [--host 0.0.0.0]
  python WindowsBatchScriptManager_api_server.py --no-auth --port 8765   # 关闭鉴权，无需 X-API-Key

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

ROOT = Path(__file__).resolve().parent
# 主程序：Windows 打包后主要为 exe；无 exe 时（开发环境或 Mac/Linux）用 main.py
MAIN_EXE = ROOT / "WindowsBatchScriptManager.exe"
MAIN_SCRIPT = ROOT / "main.py"
API_KEY = os.environ.get("API_KEY", "change-me-in-production")
# 是否关闭鉴权（--no-auth 时设为 True，无需 X-API-Key 即可调用）
DISABLE_AUTH = True


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
    from fastapi import FastAPI, Header, HTTPException, Query, Body
    from fastapi.responses import PlainTextResponse, JSONResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


def require_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if DISABLE_AUTH:
        return
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


def create_app():
    app = FastAPI(title="Batch Script Manager API", version="1.0")

    @app.get("/")
    def root():
        return {
            "service": "Batch Script Manager API",
            "endpoints": ["/list", "/status", "/start", "/stop", "/restart", "/start-all", "/stop-all", "/restart-all", "/add", "/update", "/delete", "/export", "/import", "/config-path"],
            "note": "restart、start-all、stop-all、restart-all 同时支持 GET 和 POST",
        }

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
    a = p.parse_args()
    if a.api_key:
        global API_KEY
        API_KEY = a.api_key
    if a.no_auth:
        global DISABLE_AUTH
        DISABLE_AUTH = True
    if not HAS_FASTAPI:
        print("Please install: pip install fastapi uvicorn[standard]", file=sys.stderr)
        sys.exit(1)
    import uvicorn
    if DISABLE_AUTH:
        print("Auth: disabled (--no-auth)")
    else:
        print("API key (X-API-Key):", API_KEY)
    print("Listen:", a.host, "port", a.port)
    uvicorn.run(create_app(), host=a.host, port=a.port)


if __name__ == "__main__":
    main()
