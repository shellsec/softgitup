#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 apps-mobile/ 生成根目录 CATALOG.mobile.md。"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOBILE = os.path.join(ROOT, "apps-mobile")
OUT = os.path.join(ROOT, "CATALOG.mobile.md")
PLATFORMS = ("android", "ios")
SKIP_PREFIX = "99-"


def _label(fn: str) -> str:
    m = re.match(r"^\d+-(.+)\.json$", fn.replace(".json", "") + ".json")
    base = fn.replace(".json", "")
    m = re.match(r"^\d+-(.+)$", base)
    return m.group(1) if m else base


def collect():
    rows = {}
    totals = {p: {"apps": 0, "enabled": 0, "shards": 0} for p in PLATFORMS}
    shard_names = set()
    for plat in PLATFORMS:
        plat_dir = os.path.join(MOBILE, plat)
        if not os.path.isdir(plat_dir):
            continue
        shards = {}
        for fn in sorted(os.listdir(plat_dir)):
            if not fn.endswith(".json"):
                continue
            if plat == "android" and fn.startswith(SKIP_PREFIX):
                continue
            path = os.path.join(plat_dir, fn)
            with open(path, encoding="utf-8") as f:
                apps = json.load(f)
            if not isinstance(apps, list):
                continue
            shards[fn] = apps
        totals[plat]["shards"] = len(shards)
        for fn, apps in shards.items():
            shard_names.add(fn)
            if fn not in rows:
                rows[fn] = {"label": _label(fn), "counts": {p: 0 for p in PLATFORMS}}
            for app in apps:
                if not isinstance(app, dict):
                    continue
                rows[fn]["counts"][plat] += 1
                totals[plat]["apps"] += 1
                if app.get("enabled") is True:
                    totals[plat]["enabled"] += 1
    return rows, totals, sorted(shard_names)


def render(rows, totals, order) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# 移动端软件清单索引（apps-mobile）",
        "",
        f"> 自动生成：`python tools/generate_mobile_catalog_index.py`。生成时间：**{now}**",
        "",
        "与桌面 [`apps/`](apps/) 分离。Android 走 GitHub Release APK；iOS 多为 App Store 占位。",
        "",
        "## 规模概览",
        "",
        "| 平台 | 条目数 | 已启用 | 分片数 |",
        "|------|--------|--------|--------|",
    ]
    for plat in PLATFORMS:
        t = totals[plat]
        lines.append(f"| {plat} | {t['apps']} | {t['enabled']} | {t['shards']} |")
    lines += [
        "",
        "## 常用命令",
        "",
        "```bat",
        "python lookup_app.py --apps-dir apps-mobile --platform android termux",
        "python auto_update.py --apps-dir apps-mobile --platform android termux",
        "```",
        "",
        "下载目录默认：`./android/`（`download_subdir_by_platform: true`）。**仅下载 APK，不自动安装。**",
        "",
        "## 分片一览",
        "",
        "| 分片 | 分类 | Android | iOS |",
        "|------|------|---------|-----|",
    ]
    for fn in order:
        r = rows.get(fn)
        if not r:
            continue
        c = r["counts"]
        lines.append(f"| `{fn}` | {r['label']} | {c['android']} | {c['ios']} |")
    lines += [
        "",
        "## 维护脚本",
        "",
        "- `tools/append_mobile_catalog_batch1.py` — 首批 Android + iOS 占位",
        "- `tools/append_mobile_catalog_batch2.py` — v2rayNG、SmsForwarder",
        "- `tools/append_mobile_catalog_batch3.py` — 按桌面 30 分类大补 Android",
        "- `tools/append_mobile_catalog_batch4.py` — NipaPlay-Reload、NextPlayer、mpv-android",
        "- `tools/append_mobile_catalog_batch5.py` — Android 薄分类 + iOS 占位扩展",
        "- `tools/append_mobile_catalog_batch6.py` — Android / iOS 尽量全覆盖",
        "",
    ]
    return "\n".join(lines)


def main():
    rows, totals, order = collect()
    content = render(rows, totals, order)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
        f.write("\n")
    print(f"Wrote {OUT}")
    for plat in PLATFORMS:
        t = totals[plat]
        print(f"  {plat}: {t['apps']} apps, {t['enabled']} enabled")


if __name__ == "__main__":
    main()
