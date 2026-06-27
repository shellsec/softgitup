#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 apps/ 分片生成根目录 CATALOG.md（人类可读索引，勿手改）。"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
OUT = os.path.join(ROOT, "CATALOG.md")
PLATFORMS = ("windows", "darwin", "linux")
SKIP_SHARD_PREFIX = "99-"


def _shard_label(filename: str) -> str:
    base = filename.replace(".json", "")
    m = re.match(r"^\d+-(.+)$", base)
    return m.group(1) if m else base


def _load_shards(platform: str) -> dict[str, list]:
    d: dict[str, list] = {}
    plat_dir = os.path.join(APPS, platform)
    if not os.path.isdir(plat_dir):
        return d
    for fn in sorted(os.listdir(plat_dir)):
        if not fn.endswith(".json") or fn.startswith(SKIP_SHARD_PREFIX):
            continue
        path = os.path.join(plat_dir, fn)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            d[fn] = data
    return d


def collect():
    rows: dict[str, dict] = {}
    totals = {p: {"apps": 0, "enabled": 0, "shards": 0} for p in PLATFORMS}
    all_shard_names: set[str] = set()

    for plat in PLATFORMS:
        shards = _load_shards(plat)
        totals[plat]["shards"] = len(shards)
        for fn, apps in shards.items():
            all_shard_names.add(fn)
            if fn not in rows:
                rows[fn] = {"label": _shard_label(fn), "counts": {p: 0 for p in PLATFORMS}}
            for app in apps:
                if not isinstance(app, dict):
                    continue
                rows[fn]["counts"][plat] += 1
                totals[plat]["apps"] += 1
                if app.get("enabled") is True:
                    totals[plat]["enabled"] += 1

    return rows, totals, sorted(all_shard_names)


def render(rows, totals, shard_order) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# apps 软件清单索引",
        "",
        f"> 自动生成：运行 `python tools/generate_catalog_index.py` 刷新。生成时间：**{now}**",
        "",
        "主清单数据在 [`apps/`](apps/)（`windows` / `darwin` / `linux` 各 30 个分类分片）。本文件只做**概览与导航**，不替代 JSON 配置。",
        "",
        "## 规模概览",
        "",
        "| 平台 | 条目数 | 已启用 (`enabled: true`) | 分类分片 |",
        "|------|--------|--------------------------|----------|",
    ]
    for plat in PLATFORMS:
        t = totals[plat]
        lines.append(
            f"| {plat} | {t['apps']} | {t['enabled']} | {t['shards']} |"
        )
    lines += [
        "",
        "不含 `99-未匹配-windows分片.json`（占位/待归类条目）。精确数以运行 `python auto_update.py` 时日志「已从 apps/ 目录合并配置」为准。",
        "",
        "## 分片一览（按文件名）",
        "",
        "| 分片文件 | 分类 | Windows | Darwin | Linux |",
        "|----------|------|---------|--------|-------|",
    ]
    for fn in shard_order:
        r = rows.get(fn)
        if not r:
            continue
        c = r["counts"]
        lines.append(
            f"| `{fn}` | {r['label']} | {c['windows']} | {c['darwin']} | {c['linux']} |"
        )
    lines += [
        "",
        "## 常用操作",
        "",
        "| 目的 | 命令 |",
        "|------|------|",
        "| 模糊查找应用、开启条目 | `lookup_app.bat <关键词>` 或 `python lookup_app.py <关键词>` |",
        "| 批量下载已启用条目 | `python auto_update.py`（可选 `--platform windows\\|darwin\\|linux`） |",
        "| 全部关闭 enabled | 根目录 `reset_enabled_json.bat` 或 `python tools/reset_enabled_json.py` |",
        "| 字段说明与分类参考 | [`apps/root.json`](apps/root.json) 内 `_说明` |",
        "| 刷新本索引 | `python tools/generate_catalog_index.py` |",
        "",
        "## 其它清单（与 apps/ 独立）",
        "",
        "| 目录 | 用途 |",
        "|------|------|",
        "| [`VibeCodingToolsDown/`](VibeCodingToolsDown/) | AI 编程 IDE 等，manifest 由脚本生成 |",
        "| [`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/) | Gitee 仓库分类与 Release 附件索引 |",
        "",
        "## 批量维护脚本（追加条目，幂等）",
        "",
        "- `tools/append_catalog_batch2.py` … `append_catalog_batch4.py` — 早期跨平台批",
        "- `tools/append_catalog_batch5.py` — AI IDE 生态",
        "- `tools/append_catalog_batch6.py` — AI 编程 / Copilot 类",
        "- `tools/append_catalog_batch7.py` — 截图/贴图/OCR（Snipaste、OhMyShot 等）",
        "- `tools/append_catalog_batch8.py` — SnapX/XerahS、系统/云原生/多媒体等",
        "- `tools/append_catalog_batch9.py` — 跨平台缺口大补（命令行/安全/游戏等）",
        "- `tools/append_catalog_batch10.py` — 安全 CLI、编辑器、备份、AI 等",
        "- `tools/append_catalog_batch11.py` — Vault/Trivy/Terrascan 等",
        "",
    ]
    return "\n".join(lines)


def main():
    rows, totals, shard_order = collect()
    content = render(rows, totals, shard_order)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
        f.write("\n")
    print(f"Wrote {OUT}")
    for plat in PLATFORMS:
        t = totals[plat]
        print(f"  {plat}: {t['apps']} apps, {t['enabled']} enabled, {t['shards']} shards")


if __name__ == "__main__":
    main()
