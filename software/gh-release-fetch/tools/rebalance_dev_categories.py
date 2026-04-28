#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 apps/windows/12-开发.json 拆出数据库 / 云原生 / 可观测 / 编辑器 四个分类文件。"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIN = os.path.join(SCRIPT_DIR, "apps", "windows")
DEV = os.path.join(WIN, "12-开发.json")

MOVES = [
    ("23-数据库.json", "数据库", ["dbeaver", "beekeeper", "duckdb_cli", "cockroach", "pocketbase", "supabase_cli"]),
    (
        "24-云原生.json",
        "云原生",
        [
            "kubectl",
            "helm",
            "minikube",
            "k9s",
            "skaffold",
            "kompose",
            "tilt",
            "lens",
            "podman_desktop",
            "rancher_desktop",
            "lazydocker",
            "kind",
            "nomad",
            "consul",
            "packer",
            "terraform",
        ],
    ),
    ("25-可观测.json", "可观测", ["grafana", "prometheus", "jaeger"]),
    (
        "26-编辑器.json",
        "编辑器",
        [
            "vscodium",
            "vscode",
            "notepadplusplus",
            "notepad_minusminus",
            "skylark",
            "zed",
            "lapce",
            "helix_editor",
            "sublime_merge",
            "fork",
            "winmerge",
            "neovim",
            "gitextensions",
            "imhex",
        ],
    ),
]


def main():
    with open(DEV, encoding="utf-8") as f:
        dev = json.load(f)
    by_id = {a["id"]: a for a in dev}
    pull_ids = set()
    for _fn, _cat, ids in MOVES:
        for i in ids:
            if i not in by_id:
                raise SystemExit("missing id in 12-开发.json: %r" % i)
            pull_ids.add(i)

    for fn, cat, ids in MOVES:
        chunk = []
        for i in ids:
            app = dict(by_id[i])
            app["分类"] = cat
            chunk.append(app)
        path = os.path.join(WIN, fn)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", fn, len(chunk))

    remain = [a for a in dev if a["id"] not in pull_ids]
    with open(DEV, "w", encoding="utf-8") as f:
        json.dump(remain, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("updated 12-开发.json", len(remain))


if __name__ == "__main__":
    main()
