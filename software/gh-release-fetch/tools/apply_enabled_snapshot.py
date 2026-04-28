#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据快照 JSON 批量将对应条目的 enabled 写为 true（与 reset_enabled_json.py 配套）。

默认读取 tools/last_enabled_before_reset.json（由重置脚本生成）。

每条快照需含 path、id；若来自根目录 apps.json 则还需 platform（windows|darwin|linux|legacy）。

用法：
  python tools/apply_enabled_snapshot.py
  python tools/apply_enabled_snapshot.py --dry-run
  python tools/apply_enabled_snapshot.py --snapshot-path my_enabled.json
  python tools/apply_enabled_snapshot.py --snapshot-path VibeCodingToolsDown/tools/last_enabled_before_reset.json
  python tools/apply_enabled_snapshot.py --strict
"""

import argparse
import collections
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _dump(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _enable_ids_in_list(items, ids_wanted):
    """在列表中把 id 属于 ids_wanted 的条目标为 enabled=true。返回 (命中数, 未找到的 id 列表)。"""
    if not isinstance(items, list):
        return 0, sorted(ids_wanted)
    wanted = set(ids_wanted)
    matched = set()
    for app in items:
        if not isinstance(app, dict):
            continue
        aid = app.get("id")
        if aid in wanted:
            app["enabled"] = True
            matched.add(aid)
    return len(matched), sorted(wanted - matched)


def _group_snapshot_by_path(items):
    """path -> platform -> set(ids)；分片 JSON 的 platform 为 None。"""
    by_path = collections.defaultdict(
        lambda: collections.defaultdict(set)
    )
    for row in items:
        if not isinstance(row, dict):
            continue
        rel = (row.get("path") or "").replace("\\", "/").strip()
        _id = (row.get("id") or "").strip()
        if not rel or not _id:
            continue
        plat = row.get("platform")
        by_path[rel][plat].add(_id)
    return by_path


def _apply_one_file(rel_path, plat_map, root, dry_run):
    """
    plat_map: platform -> set(ids)，分片文件只有 key None。
    返回 (命中条目数, 未找到的 id 列表, 是否写盘)。
    """
    abs_path = os.path.join(root, rel_path.replace("/", os.sep))
    if not os.path.isfile(abs_path):
        missing_all = []
        for _plat, ids in plat_map.items():
            missing_all.extend(sorted(ids))
        print("跳过（文件不存在）: %s" % rel_path, file=sys.stderr)
        return 0, missing_all, False

    with open(abs_path, encoding="utf-8") as f:
        data = json.load(f)

    total_hit = 0
    all_missing = []
    dirty = False

    if isinstance(data, dict) and isinstance(data.get("platforms"), dict):
        for plat, ids in plat_map.items():
            if plat is None:
                print(
                    "跳过（%s 为 monolith，快照缺少 platform 字段）"
                    % rel_path,
                    file=sys.stderr,
                )
                all_missing.extend(sorted(ids))
                continue
            if plat == "legacy":
                lst = data.get("apps")
            else:
                lst = (data.get("platforms") or {}).get(plat)
            if not isinstance(lst, list):
                all_missing.extend(sorted(ids))
                continue
            hit, miss = _enable_ids_in_list(lst, ids)
            if hit:
                dirty = True
            total_hit += hit
            all_missing.extend(miss)
    elif isinstance(data, dict) and isinstance(data.get("apps"), list):
        ids = set()
        for _k, s in plat_map.items():
            ids |= s
        hit, miss = _enable_ids_in_list(data["apps"], ids)
        if hit:
            dirty = True
        total_hit += hit
        all_missing.extend(miss)
    elif isinstance(data, list):
        ids = set()
        for _k, s in plat_map.items():
            ids |= s
        hit, miss = _enable_ids_in_list(data, ids)
        if hit:
            dirty = True
        total_hit += hit
        all_missing.extend(miss)
    else:
        print("跳过（格式不符）: %s" % rel_path, file=sys.stderr)
        for _plat, ids in plat_map.items():
            all_missing.extend(sorted(ids))
        return 0, all_missing, False

    wrote = False
    if dirty and not dry_run:
        _dump(abs_path, data)
        wrote = True
    print(
        "%s 命中 %s 条%s"
        % (rel_path, total_hit, "（未写入）" if dry_run else ("，已保存" if wrote else ""))
    )
    return total_hit, all_missing, wrote


def main():
    ap = argparse.ArgumentParser(
        description="按快照批量将应用条目的 enabled 写为 true"
    )
    ap.add_argument(
        "--root",
        default=SCRIPT_DIR,
        help="仓库根目录（默认：本脚本上级目录）",
    )
    ap.add_argument("--dry-run", action="store_true", help="只统计，不写文件")
    ap.add_argument(
        "--snapshot-path",
        default="",
        help="快照路径（相对 --root 或绝对；默认 tools/last_enabled_before_reset.json）",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="若有任意 id 在对应文件中未找到则退出码 1",
    )
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if args.snapshot_path:
        sp = args.snapshot_path
        snap_path = sp if os.path.isabs(sp) else os.path.join(root, sp)
    else:
        snap_path = os.path.join(root, "tools", "last_enabled_before_reset.json")

    if not os.path.isfile(snap_path):
        print("未找到快照文件: %s" % snap_path, file=sys.stderr)
        sys.exit(1)

    with open(snap_path, encoding="utf-8") as f:
        snap = json.load(f)
    items = snap.get("items")
    if not isinstance(items, list):
        print("快照格式错误：缺少 items 数组", file=sys.stderr)
        sys.exit(1)

    if not items:
        print("快照中 items 为空，无需处理。")
        sys.exit(0)

    by_path = _group_snapshot_by_path(items)
    grand_hit = 0
    grand_missing = []

    for rel_path in sorted(by_path.keys()):
        plat_map = by_path[rel_path]
        hit, miss, _wrote = _apply_one_file(rel_path, plat_map, root, args.dry_run)
        grand_hit += hit
        grand_missing.extend(miss)

    if grand_missing:
        print("以下 id 未在对应文件中匹配到:", file=sys.stderr)
        for mid in sorted(set(grand_missing)):
            print("  -", mid, file=sys.stderr)

    print("共计命中并设为 true 的条目数:", grand_hit)
    if args.dry_run:
        print("（dry-run，未修改任何文件）")

    if args.strict and grand_missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
