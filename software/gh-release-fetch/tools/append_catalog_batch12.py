#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mpv：修正官方 Release 匹配规则，补 shinchiro Win 构建与 macOS Intel；Linux 注明无二进制。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
BATCH: dict[tuple[str, str], list] = {}
UPSERT: dict[tuple[str, str], list] = {}


def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


def _upsert(plat: str, shard: str, apps: list):
    UPSERT.setdefault((plat, shard), []).extend(apps)


def _b(**kw):
    d = {
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "windows_installer": False,
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
    }
    d.update(kw)
    return d


def _repo(repo: str) -> dict:
    return {
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
    }


def _entry(plat, shard, *, id, 简介, 分类, repo, **cfg):
    _add(plat, shard, [{"id": id, "简介": 简介, "分类": 分类, **_b(**cfg), **_repo(repo)}])


# --- 修正既有 mpv（官方 mpv-player/mpv）---
_upsert("windows", "08-多媒体.json", [{
    "id": "mpv",
    "简介": "mpv（Windows x64 官方 zip；安装说明 https://mpv.io/installation/）",
    "分类": "多媒体",
    "installer_markers_match_all": True,
    "installer_markers": ["mpv-", "x86_64", "w64-mingw32"],
    "href_exclude_substrings": ["aarch64", "i686", "macos", "msvc"],
    "installer_extensions": [".zip"],
    "download_names": ["mpv-{ver}-x86_64-w64-mingw32.zip"],
    "save_name": "mpv-{ver}-x86_64-w64-mingw32.zip",
    "url_hint": "mpv",
}])

_upsert("darwin", "08-多媒体.json", [{
    "id": "mpv",
    "简介": "mpv（macOS Apple Silicon 官方 zip，仅下载）",
    "分类": "多媒体",
    "installer_markers_match_all": True,
    "installer_markers": ["mpv-", "macos", "-arm"],
    "href_exclude_substrings": ["intel", "windows", "i686", "mingw"],
    "installer_extensions": [".zip"],
    "use_download_filename": True,
    "save_name": "mpv-macos-arm.zip",
    "url_hint": "mpv",
}])

_upsert("linux", "08-多媒体.json", [{
    "id": "mpv",
    "简介": "mpv（Linux：官方 GitHub Release 无预编译包，请用发行版包管理器或 https://mpv.io/installation/）",
    "分类": "多媒体",
    "prefer_api_assets": False,
    "run_installer": False,
}])

_entry(
    "darwin", "08-多媒体.json",
    id="mpv_macos_intel",
    简介="mpv（macOS Intel 官方 zip，仅下载）",
    分类="多媒体",
    repo="mpv-player/mpv",
    installer_markers_match_all=True,
    installer_markers=["mpv-", "macos", "intel"],
    href_exclude_substrings=["-arm", "windows", "i686", "mingw"],
    installer_extensions=[".zip"],
    use_download_filename=True,
    save_name="mpv-macos-intel.zip",
    url_hint="mpv",
)

# mpv.io 推荐的 Windows 第三方 git 构建
_entry(
    "windows", "08-多媒体.json",
    id="mpv_shinchiro",
    简介="mpv（Windows x64 git 构建，shinchiro；见 mpv.io/installation/）",
    分类="多媒体",
    repo="shinchiro/mpv-winbuild-cmake",
    version_tag_as_on_github=False,
    installer_markers_match_all=True,
    installer_markers=["mpv-x86_64-", ".7z"],
    href_exclude_substrings=["dev", "i686", "aarch64", "ffmpeg", "-v3-", "debug"],
    installer_extensions=[".7z"],
    use_download_filename=True,
    save_name="mpv-shinchiro-x64.7z",
)

_entry(
    "windows", "08-多媒体.json",
    id="mpv_zhongfly",
    简介="mpv（Windows x64 git 构建，zhongfly；见 mpv.io/installation/）",
    分类="多媒体",
    repo="zhongfly/mpv-winbuild",
    version_tag_as_on_github=False,
    installer_markers_match_all=True,
    installer_markers=["mpv-x86_64-", ".7z"],
    href_exclude_substrings=["dev", "debug", "i686", "aarch64", "ffmpeg", "lgpl", "-v3-"],
    installer_extensions=[".7z"],
    use_download_filename=True,
    save_name="mpv-zhongfly-x64.7z",
)


def _apply_upsert(data: list, apps: list) -> int:
    n = 0
    index_by_id: dict[str, int] = {}
    for i, a in enumerate(data):
        if isinstance(a, dict) and a.get("id"):
            index_by_id[a["id"]] = i
    for app in apps:
        aid = (app.get("id") or "").strip()
        if not aid:
            continue
        if aid in index_by_id:
            merged = dict(data[index_by_id[aid]])
            merged.update(app)
            data[index_by_id[aid]] = merged
        else:
            data.append(app)
            index_by_id[aid] = len(data) - 1
        n += 1
    return n


def merge_all(dry_run: bool = False) -> tuple[int, int, int]:
    upserted = added = skipped = 0
    for mapping, is_upsert in ((UPSERT, True), (BATCH, False)):
        for (plat, shard), apps in sorted(mapping.items()):
            path = os.path.join(APPS, plat, shard)
            if not os.path.isfile(path):
                print("SKIP missing", path)
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                continue
            if is_upsert:
                upserted += _apply_upsert(data, apps)
            else:
                seen = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
                for app in apps:
                    aid = (app.get("id") or "").strip()
                    if not aid or aid in seen:
                        skipped += 1
                        continue
                    data.append(app)
                    seen.add(aid)
                    added += 1
            if not dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write("\n")
    return upserted, added, skipped


def main():
    dry = "--dry-run" in sys.argv
    u, a, s = merge_all(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: upserted {u}, added {a}, skipped duplicate {s}")


if __name__ == "__main__":
    main()
