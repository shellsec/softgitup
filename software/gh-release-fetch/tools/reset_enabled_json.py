#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将所有应用配置 JSON 里的 enabled 一律写为 false（改磁盘文件）。

重置前默认把当前所有 enabled=true 的条目写入
  tools/last_enabled_before_reset.json
便于重置/更新后按路径与 id 回到对应 JSON 里手动改回 true。

支持布局：
  - apps/windows/*.json（数组）
  - apps/darwin/*.json、apps/linux/*.json（数组分片）；若无分片则仍支持 apps/darwin.json、apps/linux.json
  - 根目录 apps.json（单文件，含 platforms.windows|darwin|linux）

用法：
  python tools/reset_enabled_json.py
  python tools/reset_enabled_json.py --dry-run
  python tools/reset_enabled_json.py --no-snapshot
  python tools/reset_enabled_json.py --snapshot-path my_enabled.json
  python tools/reset_enabled_json.py --apps-dir VibeCodingToolsDown
  （--apps-dir 为相对 --root 的配置根；非默认 apps 时不再处理根目录 apps.json，
  快照默认写到 <该目录>/tools/last_enabled_before_reset.json，避免覆盖主清单快照）

恢复开启状态：python tools/apply_enabled_snapshot.py（读取默认同名快照）
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _dump(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _discover_split_json_files(apps_dir):
    """与 process_apps_dir 相同的分片 JSON 列表（绝对路径）。"""
    files = []
    win = os.path.join(apps_dir, "windows")
    if os.path.isdir(win):
        for name in sorted(os.listdir(win)):
            if name.endswith(".json"):
                files.append(os.path.join(win, name))
    for plat in ("darwin", "linux"):
        sub = os.path.join(apps_dir, plat)
        used_dir = False
        if os.path.isdir(sub):
            names = [n for n in sorted(os.listdir(sub)) if n.endswith(".json")]
            if names:
                for name in names:
                    files.append(os.path.join(sub, name))
                used_dir = True
        if not used_dir:
            p = os.path.join(apps_dir, "%s.json" % plat)
            if os.path.isfile(p):
                files.append(p)
    return files


def _append_enabled_from_app_list(items, rel_path, bucket, platform=None):
    if not isinstance(items, list):
        return
    for app in items:
        if not isinstance(app, dict):
            continue
        if app.get("enabled") is not True:
            continue
        row = {
            "path": rel_path,
            "id": app.get("id", ""),
            "分类": app.get("分类", ""),
            "简介": app.get("简介", ""),
        }
        if platform is not None:
            row["platform"] = platform
        bucket.append(row)


def collect_enabled_from_file(abspath, rel_path, bucket):
    """从单个 JSON 文件收集 enabled=true 的条目，rel_path 使用正斜杠。"""
    rel_path = rel_path.replace("\\", "/")
    with open(abspath, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "apps" in data:
        inner = data["apps"]
        if isinstance(inner, list):
            _append_enabled_from_app_list(inner, rel_path, bucket)
    elif isinstance(data, list):
        _append_enabled_from_app_list(data, rel_path, bucket)
    elif isinstance(data, dict):
        platforms = data.get("platforms")
        if isinstance(platforms, dict):
            for plat in ("windows", "darwin", "linux"):
                block = platforms.get(plat)
                if isinstance(block, list):
                    _append_enabled_from_app_list(
                        block, rel_path, bucket, platform=plat
                    )
        legacy = data.get("apps")
        if isinstance(legacy, list):
            _append_enabled_from_app_list(
                legacy, rel_path, bucket, platform="legacy"
            )


def build_snapshot_payload(root, items):
    by_category = {}
    for row in items:
        cat = row.get("分类") or "(未填分类)"
        by_category.setdefault(cat, []).append(row.get("id", ""))
    for cat in by_category:
        by_category[cat] = sorted(
            [x for x in by_category[cat] if x],
            key=lambda s: s.lower(),
        )
    return {
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "root": root.replace("\\", "/"),
        "count": len(items),
        "items": sorted(items, key=lambda r: (r["path"], r.get("id") or "")),
        "by_category": dict(sorted(by_category.items(), key=lambda kv: kv[0])),
    }


def write_enabled_snapshot(root, snapshot_path, dry_run, apps_dir, scan_monolith):
    """扫描并写入快照；dry_run 时仍会写入（记录执行 dry-run 当时的开启状态）。"""
    monolith = os.path.join(root, "apps.json")
    bucket = []

    if os.path.isfile(os.path.join(apps_dir, "root.json")):
        for abspath in _discover_split_json_files(apps_dir):
            collect_enabled_from_file(
                abspath, os.path.relpath(abspath, root), bucket
            )

    if scan_monolith and os.path.isfile(monolith):
        collect_enabled_from_file(monolith, os.path.relpath(monolith, root), bucket)

    payload = build_snapshot_payload(root, bucket)
    payload["dry_run"] = dry_run

    _dump(snapshot_path, payload)
    print(
        "已写入开启项快照 (%s 条): %s"
        % (payload["count"], os.path.relpath(snapshot_path, root))
    )


def reset_app_list(items):
    """返回本列表内被改写的条目数。"""
    n = 0
    if not isinstance(items, list):
        return n
    for app in items:
        if isinstance(app, dict):
            app["enabled"] = False
            n += 1
    return n


def process_apps_dir(apps_dir, dry_run):
    total = 0
    files = _discover_split_json_files(apps_dir)

    for path in files:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "apps" in data:
            inner = data["apps"]
            if not isinstance(inner, list):
                print("跳过（非数组）:", path, file=sys.stderr)
                continue
            n = reset_app_list(inner)
            total += n
            print("%s %s 条%s" % (path, n, "（未写入）" if dry_run else ""))
            if not dry_run:
                _dump(path, data)
        elif isinstance(data, list):
            n = reset_app_list(data)
            total += n
            print("%s %s 条%s" % (path, n, "（未写入）" if dry_run else ""))
            if not dry_run:
                _dump(path, data)
        else:
            print("跳过（格式不符）:", path, file=sys.stderr)
    return total


def process_monolith(path, dry_run):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    total = 0
    platforms = cfg.get("platforms")
    if isinstance(platforms, dict):
        for plat in ("windows", "darwin", "linux"):
            block = platforms.get(plat)
            if isinstance(block, list):
                total += reset_app_list(block)
    legacy = cfg.get("apps")
    if isinstance(legacy, list):
        total += reset_app_list(legacy)
    print("%s 合计 %s 条%s" % (path, total, "（未写入）" if dry_run else ""))
    if not dry_run and total:
        _dump(path, cfg)
    return total


def main():
    ap = argparse.ArgumentParser(description="将所有应用条目的 enabled 写回 false")
    ap.add_argument(
        "--root",
        default=SCRIPT_DIR,
        help="仓库根目录（默认：本脚本所在仓库根，即 tools 的上级的上级）",
    )
    ap.add_argument(
        "--apps-dir",
        default="apps",
        metavar="REL",
        help="配置根相对 --root（默认 apps）；如 VibeCodingToolsDown。仅当该路径为默认 apps 时才同时处理根目录 apps.json",
    )
    ap.add_argument("--dry-run", action="store_true", help="只统计，不写文件")
    ap.add_argument(
        "--no-snapshot",
        action="store_true",
        help="不写入开启项快照（默认写入 tools/last_enabled_before_reset.json）",
    )
    ap.add_argument(
        "--snapshot-path",
        default="",
        help="快照 JSON 路径（相对 --root 或绝对路径；默认 tools/last_enabled_before_reset.json）",
    )
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    apps_rel = args.apps_dir.strip().replace("\\", "/").strip("/")
    if not apps_rel:
        print("--apps-dir 不能为空", file=sys.stderr)
        sys.exit(1)
    apps_dir = os.path.join(root, apps_rel.replace("/", os.sep))
    monolith = os.path.join(root, "apps.json")
    scan_monolith = os.path.normpath(apps_dir) == os.path.normpath(
        os.path.join(root, "apps")
    )

    if args.snapshot_path:
        sp = args.snapshot_path
        snapshot_path = sp if os.path.isabs(sp) else os.path.join(root, sp)
    elif scan_monolith:
        snapshot_path = os.path.join(root, "tools", "last_enabled_before_reset.json")
    else:
        snapshot_path = os.path.join(
            apps_dir, "tools", "last_enabled_before_reset.json"
        )

    if not args.no_snapshot:
        snap_dir = os.path.dirname(snapshot_path)
        if snap_dir and not os.path.isdir(snap_dir):
            os.makedirs(snap_dir, exist_ok=True)
        write_enabled_snapshot(
            root, snapshot_path, args.dry_run, apps_dir, scan_monolith
        )

    grand = 0
    has_split = os.path.isfile(os.path.join(apps_dir, "root.json"))
    if has_split:
        grand += process_apps_dir(apps_dir, args.dry_run)
    if scan_monolith and os.path.isfile(monolith):
        grand += process_monolith(monolith, args.dry_run)

    if grand == 0 and not has_split and not (scan_monolith and os.path.isfile(monolith)):
        print("未找到可处理配置（%s 下无 root.json，且未处理 apps.json）" % apps_rel, file=sys.stderr)
        sys.exit(1)

    print("共计处理条目数:", grand)
    if args.dry_run:
        print("（dry-run，未修改任何文件）")


if __name__ == "__main__":
    main()
