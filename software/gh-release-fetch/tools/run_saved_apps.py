#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按根目录 saved_apps_<platform>.json 批量开启 enabled 并执行 auto_update。

用法：
  python tools/run_saved_apps.py
  python tools/run_saved_apps.py windows
  python tools/run_saved_apps.py saved_apps_windows.json
  python tools/run_saved_apps.py --list my_apps_windows.json --skip-enable
  python tools/run_saved_apps.py --dry-run windows
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from tools.app_list import (  # noqa: E402
    PLATFORMS,
    default_list_basename,
    load_list,
    resolve_list_path,
)


def detect_platform() -> str:
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "darwin"
    return "linux"


def infer_platform(data: dict, fallback: str) -> str:
    plat = (data.get("platform") or "").strip().lower()
    if plat in PLATFORMS:
        return plat
    items = data.get("items") or []
    plats = {(r.get("platform") or "").lower() for r in items if r.get("platform")}
    plats.discard("")
    if len(plats) == 1:
        return next(iter(plats))
    return fallback


def main() -> int:
    ap = argparse.ArgumentParser(description="按 saved_apps_*.json 批量更新应用")
    ap.add_argument(
        "target",
        nargs="?",
        default="",
        help="平台名 windows|darwin|linux，或列表文件路径（默认当前系统 + saved_apps_<平台>.json）",
    )
    ap.add_argument("--list", dest="list_path", default="", help="显式指定列表 JSON 路径")
    ap.add_argument("--platform", default="", help="传给 auto_update 的平台")
    ap.add_argument("--skip-enable", action="store_true", help="不写入 enabled，仅按 id 更新")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不修改 JSON、不下载")
    ap.add_argument("--insecure", action="store_true", help="传给 auto_update.py")
    ap.add_argument("--apps-dir", default="", help="传给 auto_update / apply 的配置目录")
    args = ap.parse_args()

    default_plat = args.platform or detect_platform()
    list_arg = args.list_path or args.target
    list_path = resolve_list_path(SCRIPT_DIR, list_arg or None, default_plat)

    if not os.path.isfile(list_path):
        hint = default_list_basename(default_plat)
        print("[ERROR] 未找到列表文件: %s" % list_path, file=sys.stderr)
        print("请先用 lookup_app 保存，或指定列表路径:", file=sys.stderr)
        print("  lookup_app.bat --platform %s --save 关键词" % default_plat, file=sys.stderr)
        print("  run_saved_apps.bat my_list.json", file=sys.stderr)
        print("  set SAVED_APPS_LIST=my_list.json  再 run_saved_apps.bat", file=sys.stderr)
        print("默认（未指定时）: %s（相对仓库根）" % hint, file=sys.stderr)
        return 1

    try:
        data = load_list(list_path)
    except (OSError, ValueError) as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 1

    items = [r for r in (data.get("items") or []) if (r.get("id") or "").strip()]
    if not items:
        print("列表为空，无需处理。")
        return 0

    platform = infer_platform(data, default_plat)
    ids = sorted({(r.get("id") or "").strip() for r in items})
    rel_list = os.path.relpath(list_path, SCRIPT_DIR)
    print("列表: %s（%d 条，平台 %s）" % (rel_list, len(ids), platform))
    print("应用 id:", ", ".join(ids))

    if args.dry_run:
        print("（dry-run：将 apply enabled + auto_update --platform %s %d 个 id）" % (platform, len(ids)))
        return 0

    py = sys.executable
    if not args.skip_enable:
        snap_arg = list_path
        try:
            if os.path.commonpath([SCRIPT_DIR, list_path]) == SCRIPT_DIR:
                snap_arg = os.path.relpath(list_path, SCRIPT_DIR)
        except ValueError:
            pass  # 不同盘符等：保留绝对路径
        apply_cmd = [
            py,
            os.path.join(SCRIPT_DIR, "tools", "apply_enabled_snapshot.py"),
            "--root",
            SCRIPT_DIR,
            "--snapshot-path",
            snap_arg,
        ]
        print("\n[1/2] 开启 enabled …")
        r = subprocess.run(apply_cmd, cwd=SCRIPT_DIR)
        if r.returncode != 0:
            return r.returncode

    upd = [py, os.path.join(SCRIPT_DIR, "auto_update.py"), "--platform", platform, *ids]
    if args.insecure:
        upd.append("--insecure")
    if args.apps_dir:
        upd.extend(["--apps-dir", args.apps_dir])

    print("\n[2/2] 执行更新 …")
    r = subprocess.run(upd, cwd=SCRIPT_DIR)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
