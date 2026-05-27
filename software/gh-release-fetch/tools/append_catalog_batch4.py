#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补全常用跨平台条目（linux/darwin）。同 id 不重复追加。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
BATCH: dict[tuple[str, str], list] = {}


def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


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


# (id, shard, repo, desc, linux_cfg, darwin_cfg)
_ITEMS = [
    ("dbeaver", "23-数据库.json", "dbeaver/dbeaver", "DBeaver CE 数据库客户端",
     _b(分类="数据库", installer_markers_match_all=True, installer_markers=["dbeaver-ce-", "linux.gtk.x86_64.tar.gz"],
        href_exclude_substrings=["windows", "macos", "aarch64", "sha256"], installer_extensions=[".tar.gz"],
        download_names=["dbeaver-ce-{ver}-linux.gtk.x86_64.tar.gz"], save_name="dbeaver-ce-{ver}-linux.gtk.x86_64.tar.gz"),
     _b(分类="数据库", installer_markers_match_all=True, installer_markers=["dbeaver-ce-", "macos-x86_64.dmg"],
        href_exclude_substrings=["windows", "linux", "aarch64"], installer_extensions=[".dmg"],
        download_names=["dbeaver-ce-{ver}-macos-x86_64.dmg"], save_name="dbeaver-ce-{ver}-macos-x86_64.dmg")),
    ("espanso", "13-效率.json", "espanso/espanso", "Espanso 文本扩展",
     _b(分类="效率", installer_markers=["Espanso-Linux-x86_64"], href_exclude_substrings=["Win", "Mac", "Portable"],
        use_download_filename=True),
     _b(分类="效率", installer_markers=["Espanso-mac-x86_64"], href_exclude_substrings=["Win", "Linux", "Portable"],
        use_download_filename=True)),
    ("barrier", "21-远程与协作.json", "debauchee/barrier", "Barrier 开源 KVM",
     _b(分类="远程与协作", installer_markers_match_all=True, installer_markers=["Barrier-", "Linux-x86_64.deb"],
        href_exclude_substrings=["exe", "dmg", "sha256"], installer_extensions=[".deb"], use_download_filename=True),
     _b(分类="远程与协作", installer_markers_match_all=True, installer_markers=["Barrier-", "Release.dmg"],
        href_exclude_substrings=["exe", "deb", "sha256"], installer_extensions=[".dmg"], use_download_filename=True)),
    ("appflowy", "15-笔记.json", "AppFlowy-IO/AppFlowy", "AppFlowy 开源 Notion 类",
     _b(分类="笔记", installer_markers_match_all=True, installer_markers=["AppFlowy-", "linux-x86_64.tar.gz"],
        href_exclude_substrings=["windows", "macos", "android", "arm64"], installer_extensions=[".tar.gz"],
        download_names=["AppFlowy-{ver}-linux-x86_64.tar.gz"], save_name="AppFlowy-{ver}-linux-x86_64.tar.gz"),
     _b(分类="笔记", installer_markers_match_all=True, installer_markers=["AppFlowy-", "macos-x86_64.dmg"],
        href_exclude_substrings=["windows", "linux", "android"], installer_extensions=[".dmg"],
        download_names=["AppFlowy-{ver}-macos-x86_64.dmg"], save_name="AppFlowy-{ver}-macos-x86_64.dmg")),
    ("affine", "04-办公.json", "toeverything/AFFiNE", "AFFiNE 知识库/文档/白板",
     _b(分类="办公", installer_markers_match_all=True, installer_markers=["affine-", "stable-linux-x64"],
        href_exclude_substrings=["windows", "darwin", "arm64", "blockmap"], use_download_filename=True),
     _b(分类="办公", installer_markers_match_all=True, installer_markers=["affine-", "stable-macos-x64"],
        href_exclude_substrings=["windows", "linux", "arm64", "blockmap"], use_download_filename=True)),
    ("electerm", "17-终端.json", "electerm/electerm", "electerm 终端/SSH/SFTP",
     _b(分类="终端", installer_markers=["electerm-", "linux-x64.tar.gz"], href_exclude_substrings=["win", "mac", "arm64"],
        installer_extensions=[".tar.gz"], download_names=["electerm-{ver}-linux-x64-portable.tar.gz"],
        save_name="electerm-{ver}-linux-x64-portable.tar.gz", url_hint="electerm"),
     _b(分类="终端", installer_markers=["electerm-", "mac-arm64.dmg"], href_exclude_substrings=["win", "linux", "x64"],
        installer_extensions=[".dmg"], download_names=["electerm-{ver}-mac-arm64-portable.dmg"],
        save_name="electerm-{ver}-mac-arm64-portable.dmg", url_hint="electerm")),
    ("copyq", "13-效率.json", "hluk/CopyQ", "CopyQ 剪贴板管理",
     _b(分类="效率", installer_markers_match_all=True, installer_markers=["copyq-", "linux-x86_64.tar.gz"],
        href_exclude_substrings=["setup.exe", "macos", "checksum"], installer_extensions=[".tar.gz"],
        download_names=["copyq-{ver}-linux-x86_64.tar.gz"], save_name="copyq-{ver}-linux-x86_64.tar.gz"),
     _b(分类="效率", installer_markers_match_all=True, installer_markers=["copyq-", "macos.dmg"],
        href_exclude_substrings=["setup.exe", "linux", "checksum"], installer_extensions=[".dmg"],
        download_names=["copyq-{ver}-macos.dmg"], save_name="copyq-{ver}-macos.dmg")),
    ("cmake", "12-开发.json", "Kitware/CMake", "CMake 构建系统",
     _b(分类="开发", installer_markers=["cmake-", "linux-x86_64.tar.gz"], href_exclude_substrings=["windows", "Darwin", "arm"],
        installer_extensions=[".tar.gz"], download_names=["cmake-{ver}-linux-x86_64.tar.gz"],
        save_name="cmake-{ver}-linux-x86_64.tar.gz"),
     _b(分类="开发", installer_markers=["cmake-", "macos-universal.tar.gz"], href_exclude_substrings=["windows", "Linux", "arm64-only"],
        installer_extensions=[".tar.gz"], download_names=["cmake-{ver}-macos-universal.tar.gz"],
        save_name="cmake-{ver}-macos-universal.tar.gz")),
    ("etcd", "12-开发.json", "etcd-io/etcd", "etcd 分布式键值",
     _b(分类="开发", installer_markers=["etcd-v", "linux-amd64.tar.gz"], href_exclude_substrings=["windows", "darwin", "arm"],
        installer_extensions=[".tar.gz"], download_names=["etcd-v{ver}-linux-amd64.tar.gz"],
        save_name="etcd-v{ver}-linux-amd64.tar.gz"),
     _b(分类="开发", installer_markers=["etcd-v", "darwin-amd64.zip"], href_exclude_substrings=["windows", "linux", "arm"],
        installer_extensions=[".zip"], download_names=["etcd-v{ver}-darwin-amd64.zip"],
        save_name="etcd-v{ver}-darwin-amd64.zip")),
    ("consul", "24-云原生.json", "hashicorp/consul", "Consul 服务发现",
     _b(分类="云原生", installer_markers=["consul_", "linux_amd64.zip"], href_exclude_substrings=["windows", "darwin"],
        installer_extensions=[".zip"], download_names=["consul_{ver}_linux_amd64.zip"],
        save_name="consul_{ver}_linux_amd64.zip"),
     _b(分类="云原生", installer_markers=["consul_", "darwin_amd64.zip"], href_exclude_substrings=["windows", "linux"],
        installer_extensions=[".zip"], download_names=["consul_{ver}_darwin_amd64.zip"],
        save_name="consul_{ver}_darwin_amd64.zip")),
    ("duf", "16-系统.json", "muesli/duf", "duf 磁盘空间概览",
     _b(分类="系统", installer_markers=["duf_", "Linux_x86_64.tar.gz"], href_exclude_substrings=["Windows", "Darwin", "arm"],
        installer_extensions=[".tar.gz"], download_names=["duf_{ver}_Linux_x86_64.tar.gz"],
        save_name="duf_{ver}_Linux_x86_64.tar.gz"),
     _b(分类="系统", installer_markers=["duf_", "Darwin_x86_64.tar.gz"], href_exclude_substrings=["Windows", "Linux", "arm"],
        installer_extensions=[".tar.gz"], download_names=["duf_{ver}_Darwin_x86_64.tar.gz"],
        save_name="duf_{ver}_Darwin_x86_64.tar.gz")),
    ("dive", "10-安全.json", "wagoodman/dive", "dive Docker 镜像层分析",
     _b(分类="安全", installer_markers_match_all=True, installer_markers=["dive_", "linux_amd64.tar.gz"],
        href_exclude_substrings=["windows", "darwin", "deb", "rpm"], installer_extensions=[".tar.gz"],
        download_names=["dive_{ver}_linux_amd64.tar.gz"], save_name="dive_{ver}_linux_amd64.tar.gz"),
     _b(分类="安全", installer_markers_match_all=True, installer_markers=["dive_", "darwin_amd64.tar.gz"],
        href_exclude_substrings=["windows", "linux", "deb", "rpm"], installer_extensions=[".tar.gz"],
        download_names=["dive_{ver}_darwin_amd64.tar.gz"], save_name="dive_{ver}_darwin_amd64.tar.gz")),
]

for aid, shard, repo, desc, lcfg, dcfg in _ITEMS:
    for plat, cfg in (("linux", lcfg), ("darwin", dcfg)):
        entry = {
            "id": aid,
            "简介": desc if plat == "linux" else desc,
            "releases_url": f"https://bgithub.xyz/{repo}/releases",
            "repo_path": repo,
            **cfg,
        }
        _add(plat, shard, [entry])


def merge_batch(dry_run: bool = False):
    added = skipped = 0
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            print("SKIP missing", path)
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
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
    return added, skipped


def main():
    dry = "--dry-run" in sys.argv
    added, skipped = merge_batch(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: added {added}, skipped {skipped}")


if __name__ == "__main__":
    main()
