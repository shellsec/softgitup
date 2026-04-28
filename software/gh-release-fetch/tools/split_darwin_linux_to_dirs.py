#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将 apps/darwin.json、apps/linux.json 按与 apps/windows/*.json 相同的分片名拆到
apps/darwin/、apps/linux/ 目录（按 windows 条目的 id 匹配分片）。

运行后若目录下已有分片且非空，会备份并替换单文件为分片；原 darwin.json / linux.json
重命名为 *.json.bak（若仍存在）。

用法（在仓库根目录）:
  python tools/split_darwin_linux_to_dirs.py
"""

import json
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(SCRIPT_DIR, "apps")
WIN = os.path.join(APPS, "windows")


def load_array(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "apps" in data:
        data = data["apps"]
    if not isinstance(data, list):
        raise SystemExit("%s 不是数组" % path)
    return data


def build_id_to_stem():
    id_to_stem = {}
    stems = []
    for name in sorted(os.listdir(WIN)):
        if not name.endswith(".json"):
            continue
        stem = name[:-5]
        stems.append(stem)
        path = os.path.join(WIN, name)
        for app in load_array(path):
            aid = (app.get("id") or "").strip()
            if aid:
                id_to_stem[aid] = stem
    return id_to_stem, stems


def split_platform(plat: str, id_to_stem: dict, stems: list):
    single = os.path.join(APPS, "%s.json" % plat)
    if not os.path.isfile(single):
        print("跳过 %s：无 %s" % (plat, single))
        return
    items = load_array(single)
    out_dir = os.path.join(APPS, plat)
    if os.path.isdir(out_dir):
        bak = out_dir + ".bak"
        if os.path.isdir(bak):
            shutil.rmtree(bak)
        shutil.move(out_dir, bak)
        print("已备份原目录 ->", bak)
    os.makedirs(out_dir, exist_ok=True)

    buckets = {s: [] for s in stems}
    buckets["_未匹配"] = []

    for app in items:
        aid = (app.get("id") or "").strip()
        stem = id_to_stem.get(aid)
        if stem:
            buckets[stem].append(app)
        else:
            buckets["_未匹配"].append(app)

    written = 0
    for stem in stems:
        chunk = buckets.get(stem) or []
        if not chunk:
            continue
        path = os.path.join(out_dir, "%s.json" % stem)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
            f.write("\n")
        written += len(chunk)
        print("wrote", path, len(chunk))

    um = buckets.get("_未匹配") or []
    if um:
        path = os.path.join(out_dir, "99-未匹配-windows分片.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(um, f, ensure_ascii=False, indent=2)
            f.write("\n")
        written += len(um)
        print("wrote", path, len(um), "(id 未出现在任何 windows 分片中)")

    if written != len(items):
        print("警告: 写出条数 %s 与源 %s 不一致" % (written, len(items)), file=sys.stderr)

    bak_single = single + ".bak"
    shutil.move(single, bak_single)
    print("已移动", single, "->", bak_single)


def main():
    if not os.path.isdir(WIN):
        raise SystemExit("缺少 %s" % WIN)
    id_to_stem, stems = build_id_to_stem()
    for plat in ("darwin", "linux"):
        split_platform(plat, id_to_stem, stems)
    print("完成。auto_update 会优先读取 apps/darwin/、apps/linux/ 下分片；单文件已备份为 .bak")


if __name__ == "__main__":
    main()
