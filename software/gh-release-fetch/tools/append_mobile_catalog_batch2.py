#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""apps-mobile batch2：v2rayNG、SmsForwarder（Android APK）。"""
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


def _apk(id, shard, 分类, repo, 简介, markers, exclude=None, **extra):
    _add(shard, [{
        "id": id,
        "简介": 简介,
        "分类": 分类,
        **_b(
            installer_markers_match_all=True,
            installer_markers=markers,
            href_exclude_substrings=(exclude or [])
            + [".aab", "debug", "test", "unsigned", "sources", ".json", ".txt"],
            use_download_filename=True,
            save_name=f"{id}.apk",
            **extra,
        ),
        **_repo(repo),
    }])


_apk(
    "v2rayng",
    "30-代理与隧道.json",
    "代理与隧道",
    "2dust/v2rayNG",
    "v2rayNG（Android 代理客户端，VLESS/Reality 等）",
    ["v2rayNG_", "universal", ".apk"],
    ["fdroid", "arm64-v8a", "armeabi", "x86_64", "x86."],
)
_apk(
    "smsforwarder",
    "09-通讯.json",
    "通讯",
    "pppscn/SmsForwarder",
    "SmsForwarder（短信/来电/通知转发与自动化）",
    ["SmsF_", "universal", "release.apk"],
    ["armeabi", "arm64-v8a", "x86_64", "x86_"],
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
