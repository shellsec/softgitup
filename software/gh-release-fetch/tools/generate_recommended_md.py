#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 apps/<platform> 分片生成各平台 RECOMMENDED*.md。"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
SHARD_RE = re.compile(r"^(\d+)-(.+)\.json$", re.UNICODE)
PLATFORMS = ("windows", "darwin", "linux")

OUTPUT_NAMES: dict[str, tuple[str, str]] = {
    "windows": ("RECOMMENDED.zh-CN.md", "RECOMMENDED.md"),
    "darwin": ("RECOMMENDED.darwin.zh-CN.md", "RECOMMENDED.darwin.md"),
    "linux": ("RECOMMENDED.linux.zh-CN.md", "RECOMMENDED.linux.md"),
}

PLATFORM_LABEL: dict[str, str] = {
    "windows": "Windows",
    "darwin": "macOS",
    "linux": "Linux",
}


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
        head = re.split(r"[，,。]", intro)[0].strip()
        head = re.sub(r"\s+v?\d+[\d.]*.*$", "", head)
        if 4 <= len(head) <= 48:
            return head
    return row["id"].replace("_", " ")


def _platform_nav(platform: str) -> str:
    links = []
    for plat in PLATFORMS:
        if plat == platform:
            continue
        zh_name = OUTPUT_NAMES[plat][0]
        links.append("[%s](%s)" % (PLATFORM_LABEL[plat], zh_name))
    return " · ".join(links)


def _lookup_cmd(platform: str, app_id: str) -> str:
    if platform == "windows":
        return "lookup_app.bat --platform windows %s" % app_id
    return "python lookup_app.py --platform %s %s" % (platform, app_id)


def build_zh(platform: str = "windows") -> str:
    by_cat = collect(platform)
    total = sum(len(v) for v in by_cat.values())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    label = PLATFORM_LABEL[platform]
    nav = _platform_nav(platform)
    lines = [
        "# 推荐开源软件（%s · 全分类导读）" % label,
        "",
        "> 由 `python tools/generate_recommended_md.py` 根据 [`apps/%s/`](apps/%s/) 自动生成，"
        "生成日期：**%s**。条目 **%d** 个（%s 平台）。"
        % (platform, platform, now, total, platform),
        "> 其它平台导读：%s。" % nav,
        "> 技术索引与分片统计见 [`CATALOG.md`](CATALOG.md)。启用/更新：lookup → `run_saved_apps`（Windows 可用 `run_saved_apps.bat`）。",
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
            lines.append("- 查找：`%s`" % _lookup_cmd(platform, row["id"]))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_en(platform: str = "windows") -> str:
    by_cat = collect(platform)
    total = sum(len(v) for v in by_cat.values())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    label = PLATFORM_LABEL[platform]
    zh_name = OUTPUT_NAMES[platform][0]
    nav = _platform_nav(platform)
    lines = [
        "# Recommended apps (%s · full catalog guide)" % label,
        "",
        "> Auto-generated from [`apps/%s/`](apps/%s/) on **%s**. **%d** entries."
        % (platform, platform, now, total),
        "> Chinese guide: [`%s`](%s). Other platforms: %s. Index: [`CATALOG.md`](CATALOG.md)."
        % (zh_name, zh_name, nav),
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


def write_platform(platform: str) -> tuple[str, str]:
    zh_name, en_name = OUTPUT_NAMES[platform]
    zh_path = os.path.join(ROOT, zh_name)
    en_path = os.path.join(ROOT, en_name)
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(build_zh(platform))
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(build_en(platform))
    return zh_path, en_path


def main() -> None:
    ap = argparse.ArgumentParser(
        description="从 apps/<platform> 生成 RECOMMENDED*.md（默认三平台全量）"
    )
    ap.add_argument(
        "platforms",
        nargs="*",
        metavar="PLATFORM",
        help="指定平台 windows / darwin / linux；省略则三平台全量",
    )
    args = ap.parse_args()
    targets = list(args.platforms) if args.platforms else list(PLATFORMS)
    bad = [p for p in targets if p not in PLATFORMS]
    if bad:
        ap.error("未知平台: %s（可选: %s）" % (", ".join(bad), ", ".join(PLATFORMS)))
    for plat in targets:
        zh_path, en_path = write_platform(plat)
        print("Wrote", zh_path)
        print("Wrote", en_path)


if __name__ == "__main__":
    main()
