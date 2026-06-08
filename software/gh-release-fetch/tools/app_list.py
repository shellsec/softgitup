#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""根目录应用列表 saved_apps_<platform>.json 的读写与合并。"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

PLATFORMS = ("windows", "darwin", "linux")


def _dump(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def default_list_basename(platform: str) -> str:
    plat = (platform or "windows").strip().lower()
    if plat not in PLATFORMS:
        plat = "windows"
    return "saved_apps_%s.json" % plat


def default_list_path(root: str, platform: str) -> str:
    return os.path.join(root, default_list_basename(platform))


def hit_to_item(hit: dict, apps_dir: str) -> dict:
    """lookup_app 命中项 → 快照条目（path 相对仓库根，供 apply_enabled_snapshot 使用）。"""
    rel = (hit.get("path") or "").replace("\\", "/")
    apps_prefix = os.path.relpath(apps_dir, os.path.dirname(apps_dir)).replace("\\", "/")
    if apps_prefix == ".":
        apps_prefix = "apps"
    if not rel.startswith(apps_prefix + "/"):
        rel = "%s/%s" % (apps_prefix, rel)
    return {
        "platform": hit.get("platform"),
        "path": rel,
        "id": hit.get("id") or "",
        "分类": hit.get("分类") or "",
        "简介": hit.get("简介") or "",
    }


def build_payload(
    platform: str,
    items: list[dict],
    *,
    list_file: str | None = None,
) -> dict:
    """root 固定为 '.'，表示条目 path 相对「运行 bat/脚本的仓库根」而非本机绝对路径。"""
    by_cat: dict[str, list[str]] = {}
    for row in items:
        cat = row.get("分类") or "(未填分类)"
        by_cat.setdefault(cat, []).append(row.get("id") or "")
    for cat in by_cat:
        by_cat[cat] = sorted(x for x in by_cat[cat] if x)
    payload = {
        "platform": platform,
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "root": ".",
        "count": len(items),
        "items": sorted(items, key=lambda r: (r.get("path") or "", r.get("id") or "")),
        "by_category": dict(sorted(by_cat.items(), key=lambda kv: kv[0])),
    }
    if list_file:
        payload["list_file"] = list_file.replace("\\", "/")
    return payload


def merge_items(existing: list[dict], new_items: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for row in existing + new_items:
        key = ((row.get("platform") or "").lower(), (row.get("id") or "").strip())
        if not key[1] or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def load_list(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError("%s：缺少 items 数组" % path)
    return data


def save_hits(
    path: str,
    hits: list[dict],
    apps_dir: str,
    root: str,
    merge: bool = True,
) -> int:
    """将 lookup 命中写入列表文件，返回写入后总条数。"""
    if not hits:
        return 0
    new_rows = [hit_to_item(h, apps_dir) for h in hits]
    platform = hits[0].get("platform") or "windows"
    if any(h.get("platform") != platform for h in hits):
        platform = "mixed"

    items = new_rows
    if merge and os.path.isfile(path):
        try:
            old = load_list(path)
            items = merge_items(old.get("items") or [], new_rows)
            if old.get("platform") and old.get("platform") != "mixed":
                platform = old["platform"]
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    list_rel = os.path.relpath(os.path.abspath(path), os.path.abspath(root)).replace("\\", "/")
    payload = build_payload(platform, items, list_file=list_rel)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    _dump(path, payload)
    return len(items)


def save_hits_by_platform(
    root: str,
    hits: list[dict],
    apps_dir: str,
    merge: bool = True,
    explicit_path: str | None = None,
) -> list[str]:
    """按平台拆分保存；若指定 explicit_path 则只写该文件。"""
    if explicit_path:
        n = save_hits(explicit_path, hits, apps_dir, root, merge=merge)
        print("已保存 %d 条 → %s" % (n, os.path.relpath(explicit_path, root)))
        return [explicit_path]

    by_plat: dict[str, list[dict]] = {}
    for h in hits:
        by_plat.setdefault(h.get("platform") or "windows", []).append(h)

    written: list[str] = []
    for plat, chunk in sorted(by_plat.items()):
        p = default_list_path(root, plat)
        n = save_hits(p, chunk, apps_dir, root, merge=merge)
        print("已保存 %d 条 → %s" % (n, os.path.relpath(p, root)))
        written.append(p)
    return written


def resolve_list_path(root: str, arg: str | None, default_platform: str | None = None) -> str:
    """
    解析列表 JSON 路径。优先级：显式参数 > 环境变量 SAVED_APPS_LIST > 默认 saved_apps_<平台>.json。
    路径可为绝对路径，或相对仓库根（run_saved_apps.bat 所在目录）。
    """
    env = (os.environ.get("SAVED_APPS_LIST") or "").strip()
    if not arg and env:
        arg = env
    if not arg:
        return default_list_path(root, default_platform or "windows")
    arg = arg.strip()
    if os.path.isfile(arg):
        return os.path.abspath(arg)
    under_root = os.path.join(root, arg)
    if os.path.isfile(under_root):
        return os.path.abspath(under_root)
    if arg in PLATFORMS:
        return default_list_path(root, arg)
    return os.path.abspath(under_root)
