#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 apps/<platform> 分片生成 RECOMMENDED.zh-CN.md / RECOMMENDED.md。"""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
SHARD_RE = re.compile(r"^(\d+)-(.+)\.json$", re.UNICODE)
PLATFORMS = ("windows", "darwin", "linux")


def _load_shard(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [a for a in data if isinstance(a, dict)]


def collect(platform: str) -> dict[str, list[dict]]:
    plat_dir = os.path.join(APPS, platform)
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for name in sorted(os.listdir(plat_dir)):
        if not name.endswith(".json") or name.startswith("99-"):
            continue
        m = SHARD_RE.match(name)
        shard_cat = m.group(2) if m else name.replace(".json", "")
        path = os.path.join(plat_dir, name)
        for app in _load_shard(path):
            cat = (app.get("分类") or "").strip() or shard_cat
            row = {
                "id": (app.get("id") or "").strip(),
                "简介": (app.get("简介") or "").strip(),
                "repo_path": (app.get("repo_path") or "").strip(),
                "shard": name,
                "platform": platform,
                "has_rules": bool(app.get("installer_markers") or app.get("download_names")),
                "run_installer": app.get("run_installer") is True,
            }
            if row["id"]:
                by_cat[cat].append(row)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda r: r["id"].lower())
    return dict(sorted(by_cat.items(), key=lambda kv: kv[0]))


def _clean_intro(text: str) -> str:
    return text.replace("（来源：dayanzai）", "").strip()


def _rule_badge(row: dict) -> str:
    if row["run_installer"] and row["has_rules"]:
        return "规则较完整"
    if row["has_rules"]:
        return "已配匹配规则"
    return "基础条目（试跑前建议补规则）"


def _title_from_row(row: dict) -> str:
    intro = _clean_intro(row["简介"])
    if intro:
        # 取简介第一句/逗号前，去掉版本号尾巴
        head = re.split(r"[，,。]", intro)[0].strip()
        head = re.sub(r"\s+v?\d+[\d.]*.*$", "", head)
        if 4 <= len(head) <= 48:
            return head
    return row["id"].replace("_", " ")


def build_zh(platform: str = "windows") -> str:
    by_cat = collect(platform)
    total = sum(len(v) for v in by_cat.values())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# 推荐开源软件（全分类导读）",
        "",
        "> 由 `python tools/generate_recommended_md.py` 根据 [`apps/%s/`](apps/%s/) 自动生成，"
        "生成日期：**%s**。条目 **%d** 个（%s 平台）。"
        % (platform, platform, now, total, platform),
        "> 技术索引与分片统计见 [`CATALOG.md`](CATALOG.md)。启用/更新：`lookup_app.bat <id>` → `run_saved_apps.bat`。",
        "",
        "---",
        "",
    ]
    for cat, rows in by_cat.items():
        lines.append("## %s（%d）" % (cat, len(rows)))
        lines.append("")
        for row in rows:
            title = _title_from_row(row)
            intro = _clean_intro(row["简介"]) or "（见仓库 Release 说明）"
            badge = _rule_badge(row)
            lines.append("### %s · `%s`" % (title, row["id"]))
            lines.append("")
            lines.append(intro)
            lines.append("")
            meta = []
            if row["repo_path"]:
                meta.append("仓库：`%s`" % row["repo_path"])
            meta.append("分片：`apps/%s/%s`" % (platform, row["shard"]))
            meta.append("配置：%s" % badge)
            lines.append("- " + " · ".join(meta))
            lines.append("- 查找：`lookup_app.bat --platform %s %s`" % (platform, row["id"]))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_en(platform: str = "windows") -> str:
    by_cat = collect(platform)
    total = sum(len(v) for v in by_cat.values())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Recommended apps (full catalog guide)",
        "",
        "> Auto-generated from [`apps/%s/`](apps/%s/) on **%s**. **%d** entries."
        % (platform, platform, now, total),
        "> Details: [`RECOMMENDED.zh-CN.md`](RECOMMENDED.zh-CN.md). Index: [`CATALOG.md`](CATALOG.md).",
        "",
    ]
    for cat, rows in by_cat.items():
        lines.append("## %s (%d)" % (cat, len(rows)))
        lines.append("")
        lines.append("| id | Intro | repo |")
        lines.append("|----|-------|------|")
        for row in rows:
            intro = _clean_intro(row["简介"]).replace("|", "\\|")
            if len(intro) > 80:
                intro = intro[:77] + "..."
            repo = row["repo_path"] or "-"
            lines.append("| `%s` | %s | `%s` |" % (row["id"], intro or "-", repo))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    import sys

    plat = "windows"
    if len(sys.argv) > 1:
        plat = sys.argv[1]
    zh_path = os.path.join(ROOT, "RECOMMENDED.zh-CN.md")
    en_path = os.path.join(ROOT, "RECOMMENDED.md")
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(build_zh(plat))
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(build_en(plat))
    print("Wrote", zh_path)
    print("Wrote", en_path)


if __name__ == "__main__":
    main()
