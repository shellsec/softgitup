#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""apps-mobile batch4：NipaPlay-Reload、NextPlayer、mpv-android（Android APK）。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOBILE = os.path.join(ROOT, "apps-mobile")
BATCH: dict[str, list] = {}


def _add(shard: str, apps: list):
    BATCH.setdefault(shard, []).extend(apps)


def _b(**kw):
    d = {
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "run_installer": False,
        "kill_before_install": False,
        "windows_installer": False,
        "process_name": "",
        "installer_extensions": [".apk"],
    }
    d.update(kw)
    return d


def _repo(repo: str) -> dict:
    return {
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
    }


def _apk(id, shard, 分类, repo, 简介, markers, exclude=None, match_all=True, **extra):
    base = {
        "installer_markers_match_all": match_all,
        "installer_markers": markers,
        "href_exclude_substrings": (exclude or [])
        + [".aab", "debug", "test", "unsigned", "sources", ".json", ".txt"],
        "use_download_filename": True,
        "save_name": f"{id}.apk",
    }
    base.update(extra)
    _add(shard, [{
        "id": id,
        "简介": 简介,
        "分类": 分类,
        **_b(**base),
        **_repo(repo),
    }])


_apk(
    "nipaplay",
    "08-多媒体.json",
    "多媒体",
    "MCDFsteve/NipaPlay-Reload",
    "NipaPlay-Reload（跨平台媒体播放 / 动画追番，Android）",
    ["NipaPlay-", "Android-universal", ".apk"],
    [
        "arm64-v8a",
        "armeabi",
        "x86_64",
        "Linux",
        "Windows",
        "macOS",
        "AppImage",
        ".deb",
        ".rpm",
        ".msix",
        ".zip",
        ".dmg",
    ],
)

_apk(
    "nextplayer",
    "08-多媒体.json",
    "多媒体",
    "anilbeesetti/nextplayer",
    "Next Player（Android 原生本地视频播放器）",
    ["nextplayer-v", "universal", ".apk"],
    ["arm64-v8a", "armeabi", "x86_64", "x86."],
)

_apk(
    "mpv_android",
    "08-多媒体.json",
    "多媒体",
    "mpv-android/mpv-android",
    "mpv for Android（mpv-android 官方构建；亦见 https://mpv.io/installation/）",
    ["app-default-universal", "release.apk"],
    ["debug", "arm64-v8a", "armeabi", "x86", "api29"],
)


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for shard, apps in sorted(BATCH.items()):
        path = os.path.join(MOBILE, "android", shard)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        existing = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                existing = json.load(f)
        seen = {(a.get("id") or "").strip() for a in existing if isinstance(a, dict)}
        for app in apps:
            aid = (app.get("id") or "").strip()
            if aid in seen:
                continue
            existing.append(app)
            seen.add(aid)
            total += 1
        if not dry:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print("Wrote", path, "count", len(existing))
    print(f"{'dry-run' if dry else 'done'}: added {total} new entries")


if __name__ == "__main__":
    main()
