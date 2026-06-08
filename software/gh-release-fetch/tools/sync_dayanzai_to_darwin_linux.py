#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""将 Windows 侧 dayanzai 条目同步到 darwin / linux 对应分类分片。"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")

_spec = importlib.util.spec_from_file_location(
    "split_dayanzai",
    os.path.join(ROOT, "tools", "split_dayanzai_unmatched.py"),
)
_split = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_split)
ASSIGN: dict[str, tuple[str, str]] = _split.ASSIGN


def _load_catalog(plat: str) -> tuple[set[str], set[str]]:
    ids: set[str] = set()
    repos: set[str] = set()
    for fn in os.listdir(os.path.join(APPS, plat)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(APPS, plat, fn), encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("id"):
                ids.add(item["id"].strip())
            if item.get("repo_path"):
                repos.add(item["repo_path"].strip().lower())
    return ids, repos


def _collect_dayanzai_windows() -> list[dict]:
    items: list[dict] = []
    for fn in os.listdir(os.path.join(APPS, "windows")):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(APPS, "windows", fn), encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if isinstance(item, dict) and "dayanzai" in (item.get("简介") or ""):
                items.append(item)
    return items


def _clean_intro(text: str) -> str:
    return text.replace("（来源：dayanzai）", "").strip()


def _make_entry(plat: str, win: dict, category: str) -> dict:
    intro = _clean_intro(win.get("简介") or win["id"])
    base = {
        "id": win["id"],
        "简介": intro,
        "分类": category,
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "releases_url": win["releases_url"],
        "repo_path": win["repo_path"],
        "windows_installer": False,
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
        "url_hint": win.get("url_hint") or win["id"],
    }
    if plat == "darwin":
        base.update(
            {
                "installer_extensions": [".dmg", ".pkg", ".zip"],
                "href_exclude_substrings": [
                    "windows",
                    "win64",
                    "win32",
                    "win-",
                    "linux",
                    ".AppImage",
                    ".deb",
                    ".rpm",
                    ".exe",
                    ".msi",
                    "arm64",
                ],
            }
        )
    else:
        base.update(
            {
                "installer_extensions": [".AppImage", ".tar.gz", ".deb", ".rpm", ".zip"],
                "href_exclude_substrings": [
                    "windows",
                    "win64",
                    "win32",
                    "darwin",
                    "macos",
                    ".dmg",
                    ".pkg",
                    ".exe",
                    ".msi",
                ],
            }
        )
    return base


def _merge_into_shards(plat: str, by_shard: dict[str, list[dict]], dry: bool) -> int:
    added = 0
    plat_dir = os.path.join(APPS, plat)
    for shard, apps in sorted(by_shard.items()):
        path = os.path.join(plat_dir, shard)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        seen_id = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
        seen_repo = {(a.get("repo_path") or "").strip().lower() for a in data if isinstance(a, dict)}
        n = 0
        for app in apps:
            aid = app["id"]
            rp = app["repo_path"].lower()
            if aid in seen_id or rp in seen_repo:
                continue
            data.append(app)
            seen_id.add(aid)
            seen_repo.add(rp)
            n += 1
            added += 1
        print(f"  {plat}/{shard}: +{n} (total {len(data)})")
        if not dry:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
    return added


def main():
    dry = "--dry-run" in sys.argv
    windows = _collect_dayanzai_windows()
    print(f"dayanzai windows entries: {len(windows)}")

    unmapped = [w["id"] for w in windows if w["id"] not in ASSIGN]
    if unmapped:
        print("missing ASSIGN:", unmapped)
        raise SystemExit(1)

    for plat in ("darwin", "linux"):
        ids, repos = _load_catalog(plat)
        by_shard: dict[str, list[dict]] = {}
        skip = 0
        for win in windows:
            if win["id"] in ids or win["repo_path"].lower() in repos:
                skip += 1
                continue
            shard, cat = ASSIGN[win["id"]]
            by_shard.setdefault(shard, []).append(_make_entry(plat, win, cat))
        print(f"\n{plat}: skip existing {skip}, to add {sum(len(v) for v in by_shard.values())}")
        _merge_into_shards(plat, by_shard, dry)

    if dry:
        print("\ndry-run only")
    else:
        print("\ndone")


if __name__ == "__main__":
    main()
