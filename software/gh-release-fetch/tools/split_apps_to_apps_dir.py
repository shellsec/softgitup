#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性：将根目录 apps.json 拆分为 apps/root.json + apps/windows/*.json + apps/darwin.json + apps/linux.json"""

import json
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONOLITH = os.path.join(SCRIPT_DIR, "apps.json")
APPS_DIR = os.path.join(SCRIPT_DIR, "apps")


def safe_filename(name: str) -> str:
    name = (name or "未分类").strip() or "未分类"
    for c in r'\/:*?"<>|':
        name = name.replace(c, "_")
    return name


def main():
    if not os.path.isfile(MONOLITH):
        raise SystemExit(f"找不到 {MONOLITH}")
    with open(MONOLITH, encoding="utf-8") as f:
        cfg = json.load(f)
    platforms = cfg.get("platforms") or {}
    if not isinstance(platforms, dict):
        raise SystemExit("platforms 必须是对象")

    root = {k: v for k, v in cfg.items() if k != "platforms"}
    desc = root.get("_说明")
    if isinstance(desc, dict):
        desc = dict(desc)
        desc["多文件布局"] = (
            "配置在 apps/ 目录：root.json 放全局项；windows/ 下按「分类」拆成多个 .json 数组；"
            "darwin.json、linux.json 各一个数组。auto_update.py 会按文件名排序合并 windows 分片。"
        )
        root["_说明"] = desc

    os.makedirs(os.path.join(APPS_DIR, "windows"), exist_ok=True)

    windows = platforms.get("windows") or []
    by_cat = {}
    for app in windows:
        c = (app.get("分类") or "未分类").strip() or "未分类"
        by_cat.setdefault(c, []).append(app)

    sorted_cats = sorted(by_cat.keys(), key=lambda x: (x == "未分类", x))
    for i, cat in enumerate(sorted_cats, start=1):
        fn = f"{i:02d}-{safe_filename(cat)}.json"
        path = os.path.join(APPS_DIR, "windows", fn)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(by_cat[cat], f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(by_cat[cat]), "apps")

    for plat in ("darwin", "linux"):
        arr = platforms.get(plat) or []
        path = os.path.join(APPS_DIR, f"{plat}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(arr), "items")

    with open(os.path.join(APPS_DIR, "root.json"), "w", encoding="utf-8") as f:
        json.dump(root, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", os.path.join(APPS_DIR, "root.json"))

    bak = MONOLITH + ".monolith.bak"
    shutil.move(MONOLITH, bak)
    print("moved", MONOLITH, "->", bak)


if __name__ == "__main__":
    main()
