#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""跨分类补全：SnapX/XerahS、系统/云原生/多媒体/备份/写作等 + linux/darwin 缺口。"""
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


def _entry(plat: str, shard: str, *, id: str, 简介: str, 分类: str, repo: str, **cfg):
    _add(plat, shard, [{"id": id, "简介": 简介, "分类": 分类, **_b(**cfg), **_repo(repo)}])


# --- 13 效率：SnapX / XerahS ---
_snapx = "SnapXL/SnapX"
_snapx_note = "SnapX（ShareX 跨平台分支；pinned v0.3.0，latest 多为 flatpak）"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["SnapX-Avalonia-Release-", "Windows-X64.zip"],
                     href_exclude_substrings=["ARM64", "Linux", "macOS"], installer_extensions=[".zip"],
                     download_names=["SnapX-Avalonia-Release-{ver}-Windows-X64.zip"],
                     save_name="SnapX-Avalonia-Release-{ver}-Windows-X64.zip")),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["SnapX-Avalonia-Release-", "Linux-X64.tar.zst"],
                   href_exclude_substrings=["ARM64", "Windows", "macOS"], installer_extensions=[".zst"],
                   use_download_filename=True, save_name="SnapX-Linux-X64.tar.zst")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["SnapX-Avalonia-Release-", "macOS-ARM64.zip"],
                    href_exclude_substrings=["X64.zip", "Linux", "Windows"], installer_extensions=[".zip"],
                    use_download_filename=True, save_name="SnapX-macOS-ARM64.zip")),
):
    _entry(plat, "13-效率.json", id="snapx", 简介=_snapx_note, 分类="效率", repo=_snapx,
           pinned_release_tag="v0.3.0", **spec)

_xs = "KovaForge/XerahS"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["XerahS-", "-win-x64.exe"],
                     href_exclude_substrings=["arm64", ".msi", "flatpak", ".deb", ".rpm", "mac-"],
                     download_names=["XerahS-{ver}-win-x64.exe"], save_name="XerahS-{ver}-win-x64.exe")),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["XerahS-", "linux-x64.flatpak"],
                   href_exclude_substrings=["arm64", "win-", "mac-", ".deb", ".rpm", ".exe"],
                   installer_extensions=[".flatpak"], use_download_filename=True,
                   save_name="XerahS-linux-x64.flatpak")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["XerahS-", "-mac-x64.tar.gz"],
                    href_exclude_substrings=["arm64", "win-", "linux-", "flatpak"],
                    installer_extensions=[".tar.gz"], use_download_filename=True,
                    save_name="XerahS-mac-x64.tar.gz")),
):
    _entry(plat, "13-效率.json", id="xerahs", 简介="XerahS（ShareX 风格跨平台截图/上传）", 分类="效率", repo=_xs, **spec)
_add("darwin", "13-效率.json", [{
    "id": "xerahs_darwin_arm64", "简介": "XerahS（macOS Apple Silicon tar.gz）", "分类": "效率",
    **_b(installer_markers_match_all=True, installer_markers=["XerahS-", "-mac-arm64.tar.gz"],
         href_exclude_substrings=["x64", "win-", "linux-"], installer_extensions=[".tar.gz"],
         use_download_filename=True, save_name="XerahS-mac-arm64.tar.gz"),
    **_repo(_xs),
}])

# --- 17 终端：WindTerm ---
_wt = "kingToolbox/WindTerm"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["WindTerm_", "Windows_Portable_x86_64.zip"],
                     href_exclude_substrings=["x86_32", "Linux", "Mac"], installer_extensions=[".zip"],
                     use_download_filename=True, save_name="WindTerm-Windows-x64.zip")),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["WindTerm_", "Linux_Portable_x86_64.zip"],
                   href_exclude_substrings=["Windows", "Mac"], installer_extensions=[".zip"],
                   use_download_filename=True, save_name="WindTerm-Linux-x64.zip")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["WindTerm_", "Mac_Portable_x86_64.dmg"],
                    href_exclude_substrings=["Windows", "Linux"], installer_extensions=[".dmg"],
                    use_download_filename=True, save_name="WindTerm-Mac-x64.dmg")),
):
    _entry(plat, "17-终端.json", id="windterm", 简介="WindTerm（SSH/SFTP/终端，便携版）", 分类="终端", repo=_wt, **spec)

# --- 06 命令行：Oh My Posh（实装，替换 99 占位）---
_omp = "JanDeDobbeleer/oh-my-posh"
_omp_cfg = [
    ("windows", dict(installer_markers_match_all=True, installer_markers=["install-x64.msi"],
                     href_exclude_substrings=["arm64", "msix", "arm.", "delta"], windows_installer=True,
                     installer_extensions=[".msi"], download_names=["install-x64.msi"], save_name="oh-my-posh-install-x64.msi",
                     run_installer=True)),
    ("linux", dict(installer_markers=["posh-linux-amd64"], href_exclude_substrings=["arm", "darwin", "windows", "deb", "rpm"],
                   use_download_filename=True, save_name="posh-linux-amd64")),
    ("darwin", dict(installer_markers=["posh-darwin-arm64"], href_exclude_substrings=["amd64", "linux", "windows"],
                   use_download_filename=True, save_name="posh-darwin-arm64")),
]
for plat, cfg in _omp_cfg:
    _upsert(plat, "06-命令行.json", [{"id": "oh_my_posh", "简介": "Oh My Posh（终端提示符主题引擎）", "分类": "命令行", **_b(**cfg), **_repo(_omp)}])
_add("darwin", "06-命令行.json", [{
    "id": "oh_my_posh_darwin_intel", "简介": "Oh My Posh（macOS Intel 二进制）", "分类": "命令行",
    **_b(installer_markers=["posh-darwin-amd64"], href_exclude_substrings=["arm64", "linux", "windows"],
         use_download_filename=True, save_name="posh-darwin-amd64"),
    **_repo(_omp),
}])

# --- 16 系统：balenaEtcher ---
_be = "balena-io/etcher"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["balenaEtcher-", ".Setup.exe"],
                     href_exclude_substrings=["darwin", "linux", "arm64.dmg"], windows_installer=True,
                     installer_extensions=[".exe"], use_download_filename=True, save_name="balenaEtcher-Setup.exe",
                     run_installer=True)),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["balenaEtcher-linux-x64-", ".zip"],
                   href_exclude_substrings=["Setup.exe", "darwin", "deb", "rpm"], installer_extensions=[".zip"],
                   use_download_filename=True, save_name="balenaEtcher-linux-x64.zip")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["balenaEtcher-", "-arm64.dmg"],
                    href_exclude_substrings=["x64.dmg", "Setup.exe", "linux"], installer_extensions=[".dmg"],
                    use_download_filename=True, save_name="balenaEtcher-arm64.dmg")),
):
    _entry(plat, "16-系统.json", id="balena_etcher", 简介="balenaEtcher（USB 启动盘写入）", 分类="系统", repo=_be, **spec)
_add("darwin", "16-系统.json", [{
    "id": "balena_etcher_darwin_intel", "简介": "balenaEtcher（macOS Intel dmg）", "分类": "系统",
    **_b(installer_markers_match_all=True, installer_markers=["balenaEtcher-", "-x64.dmg"],
         href_exclude_substrings=["arm64", "Setup.exe", "linux"], installer_extensions=[".dmg"],
         use_download_filename=True, save_name="balenaEtcher-x64.dmg"),
    **_repo(_be),
}])

# --- 24 云原生：Podman / Portainer ---
_pd = "containers/podman"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["podman-installer-windows-amd64.msi"],
                     href_exclude_substrings=["arm64", "darwin", "linux", "remote"], windows_installer=True,
                     installer_extensions=[".msi"], use_download_filename=True, save_name="podman-installer-windows-amd64.msi",
                     run_installer=True)),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["podman-remote-static-linux_amd64.tar.gz"],
                   href_exclude_substrings=["arm64", "windows", "darwin"], installer_extensions=[".tar.gz"],
                   use_download_filename=True, save_name="podman-remote-linux-amd64.tar.gz")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["podman-installer-macos-arm64.pkg"],
                    href_exclude_substrings=["windows", "linux", "amd64"], installer_extensions=[".pkg"],
                    use_download_filename=True, save_name="podman-installer-macos-arm64.pkg")),
):
    _entry(plat, "24-云原生.json", id="podman", 简介="Podman（无守护进程容器，Desktop/CLI）", 分类="云原生", repo=_pd, **spec)

_pt = "portainer/portainer"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["portainer-", "windows1809-amd64.tar.gz"],
                     href_exclude_substrings=["checksum", "linux", "arm", "ltsc2022"], installer_extensions=[".tar.gz"],
                     use_download_filename=True, save_name="portainer-windows-amd64.tar.gz")),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["portainer-", "linux-amd64.tar.gz"],
                   href_exclude_substrings=["checksum", "windows", "arm"], installer_extensions=[".tar.gz"],
                   use_download_filename=True, save_name="portainer-linux-amd64.tar.gz")),
):
    _entry(plat, "24-云原生.json", id="portainer", 简介="Portainer（容器管理 UI 服务端包）", 分类="云原生", repo=_pt, **spec)

_upsert("linux", "13-效率.json", [{
    "id": "xerahs",
    "installer_markers": ["XerahS-", "linux-x64.flatpak"],
    "href_exclude_substrings": ["arm64", "win-", "mac-", ".deb", ".rpm", ".exe"],
    "installer_extensions": [".flatpak"],
    "use_download_filename": True,
    "save_name": "XerahS-linux-x64.flatpak",
}])

# k9s / helm linux+darwin
_add("linux", "24-云原生.json", [{
    "id": "k9s", "简介": "K9s（K8s 终端 UI，Linux amd64）", "分类": "云原生",
    **_b(installer_markers=["k9s_Linux_amd64.tar.gz"], href_exclude_substrings=["Windows", "Darwin", "arm", ".sbom"],
         installer_extensions=[".tar.gz"], download_names=["k9s_Linux_amd64.tar.gz"], save_name="k9s_Linux_amd64.tar.gz"),
    **_repo("derailed/k9s"),
}])
_add("darwin", "24-云原生.json", [{
    "id": "k9s", "简介": "K9s（K8s 终端 UI，macOS amd64）", "分类": "云原生",
    **_b(installer_markers=["k9s_Darwin_amd64.tar.gz"], href_exclude_substrings=["Windows", "Linux", "arm", ".sbom"],
         installer_extensions=[".tar.gz"], download_names=["k9s_Darwin_amd64.tar.gz"], save_name="k9s_Darwin_amd64.tar.gz"),
    **_repo("derailed/k9s"),
}])
_add("linux", "24-云原生.json", [{
    "id": "helm", "简介": "Helm（K8s 包管理，Linux amd64）", "分类": "云原生",
    **_b(installer_markers_match_all=True, installer_markers=["helm-v", "linux-amd64.tar.gz"],
         href_exclude_substrings=["windows", "darwin", "arm"], installer_extensions=[".tar.gz"],
         download_names=["helm-v{ver}-linux-amd64.tar.gz"], save_name="helm-v{ver}-linux-amd64.tar.gz"),
    **_repo("helm/helm"),
}])
_add("darwin", "24-云原生.json", [{
    "id": "helm", "简介": "Helm（K8s 包管理，macOS amd64）", "分类": "云原生",
    **_b(installer_markers_match_all=True, installer_markers=["helm-v", "darwin-amd64.tar.gz"],
         href_exclude_substrings=["windows", "linux", "arm"], installer_extensions=[".tar.gz"],
         download_names=["helm-v{ver}-darwin-amd64.tar.gz"], save_name="helm-v{ver}-darwin-amd64.tar.gz"),
    **_repo("helm/helm"),
}])

# --- 12 开发：ddev ---
_dv = "ddev/ddev"
for plat, spec in (
    ("windows", dict(installer_markers_match_all=True, installer_markers=["ddev_windows_amd64_installer.v", ".exe"],
                     href_exclude_substrings=["arm64", "zip", "macos", "linux"], windows_installer=True,
                     installer_extensions=[".exe"], use_download_filename=True, save_name="ddev-installer.exe", run_installer=True)),
    ("linux", dict(installer_markers_match_all=True, installer_markers=["ddev-wsl2_", "_linux_amd64.deb"],
                   href_exclude_substrings=["windows", "macos", "arm64", "rpm"], installer_extensions=[".deb"],
                   use_download_filename=True, save_name="ddev-linux-amd64.deb")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["ddev_macos-arm64.v", ".tar.gz"],
                    href_exclude_substrings=["windows", "linux", "amd64.v"], installer_extensions=[".tar.gz"],
                    use_download_filename=True, save_name="ddev-macos-arm64.tar.gz")),
):
    _entry(plat, "12-开发.json", id="ddev", 简介="DDEV（本地 PHP/Drupal/WordPress 容器开发环境）", 分类="开发", repo=_dv, **spec)

# --- 22 音视频：FFmpeg BtbN 构建 ---
_ff = "BtbN/FFmpeg-Builds"
for plat, spec in (
    ("windows", dict(installer_markers=["ffmpeg-master-latest-win64-gpl.zip"],
                     href_exclude_substrings=["shared", "lgpl", "arm", "linux"], installer_extensions=[".zip"],
                     use_download_filename=True, save_name="ffmpeg-win64-gpl.zip", version_tag_as_on_github=False)),
    ("linux", dict(installer_markers=["ffmpeg-master-latest-linux64-gpl.tar.xz"],
                   href_exclude_substrings=["shared", "lgpl", "win", "arm"], installer_extensions=[".xz"],
                   use_download_filename=True, save_name="ffmpeg-linux64-gpl.tar.xz", version_tag_as_on_github=False)),
):
    _entry(plat, "22-音视频.json", id="ffmpeg_builds", 简介="FFmpeg（BtbN 预编译 master/latest 构建）", 分类="音视频",
           repo=_ff, pinned_release_tag="latest", **spec)

# --- 08 多媒体：VLC / OBS linux+darwin ---
_add("linux", "08-多媒体.json", [{
    "id": "vlc", "简介": "VLC 媒体播放器（Linux x86_64 tar.xz）", "分类": "多媒体",
    **_b(installer_markers_match_all=True, installer_markers=["vlc-", "linux64.tar.xz"],
         href_exclude_substrings=["win", "darwin", "arm", ".exe"], installer_extensions=[".xz"],
         download_names=["vlc-{ver}-linux64.tar.xz"], save_name="vlc-{ver}-linux64.tar.xz", url_hint="vlc"),
    **_repo("videolan/vlc"),
}])
_add("darwin", "08-多媒体.json", [{
    "id": "vlc", "简介": "VLC 媒体播放器（macOS dmg）", "分类": "多媒体",
    **_b(installer_markers_match_all=True, installer_markers=["vlc-", "darwin.dmg"],
         href_exclude_substrings=["win", "linux", "arm64"], installer_extensions=[".dmg"],
         download_names=["vlc-{ver}-darwin.dmg"], save_name="vlc-{ver}-darwin.dmg", url_hint="vlc"),
    **_repo("videolan/vlc"),
}])
_add("linux", "08-多媒体.json", [{
    "id": "obs", "简介": "OBS Studio（Linux x86_64 安装包）", "分类": "多媒体",
    **_b(installer_markers_match_all=True, installer_markers=["OBS-Studio-", "Linux-x86_64.tar.gz"],
         href_exclude_substrings=["Windows", "macOS", "arm64", "PDBs"], installer_extensions=[".tar.gz"],
         download_names=["OBS-Studio-{ver}-Linux-x86_64.tar.gz"], save_name="OBS-Studio-{ver}-Linux-x86_64.tar.gz",
         url_hint="OBS-Studio"),
    **_repo("obsproject/obs-studio"),
}])
_add("darwin", "08-多媒体.json", [{
    "id": "obs", "简介": "OBS Studio（macOS Apple Silicon dmg）", "分类": "多媒体",
    **_b(installer_markers_match_all=True, installer_markers=["OBS-Studio-", "macOS-Apple.dmg"],
         href_exclude_substrings=["Windows", "Linux", "Intel", "PDBs"], installer_extensions=[".dmg"],
         download_names=["OBS-Studio-{ver}-macOS-Apple.dmg"], save_name="OBS-Studio-{ver}-macOS-Apple.dmg",
         url_hint="OBS-Studio"),
    **_repo("obsproject/obs-studio"),
}])

# --- 15 笔记：MarkText linux+darwin ---
_add("linux", "15-笔记.json", [{
    "id": "marktext", "简介": "MarkText（Linux AppImage）", "分类": "笔记",
    **_b(installer_markers=["marktext-x64.AppImage"], href_exclude_substrings=["setup.exe", "dmg", "arm"],
         installer_extensions=[".AppImage"], use_download_filename=True, save_name="marktext-x64.AppImage"),
    **_repo("marktext/marktext"),
}])
_add("darwin", "15-笔记.json", [{
    "id": "marktext", "简介": "MarkText（macOS dmg）", "分类": "笔记",
    **_b(installer_markers=["marktext-", "-x64.dmg"], href_exclude_substrings=["setup.exe", "AppImage", "arm"],
         installer_extensions=[".dmg"], use_download_filename=True, save_name="marktext-x64.dmg"),
    **_repo("marktext/marktext"),
}])

# --- 07 备份：restic linux+darwin ---
_add("linux", "07-备份.json", [{
    "id": "restic", "简介": "restic（Linux amd64 二进制 zip）", "分类": "备份",
    **_b(installer_markers_match_all=True, installer_markers=["restic_", "linux_amd64.zip"],
         href_exclude_substrings=["windows", "darwin", "386", "arm", ".bz2"], installer_extensions=[".zip"],
         use_download_filename=True, save_name="restic-linux-amd64.zip"),
    **_repo("restic/restic"),
}])
_add("darwin", "07-备份.json", [{
    "id": "restic", "简介": "restic（macOS amd64 二进制 zip）", "分类": "备份",
    **_b(installer_markers_match_all=True, installer_markers=["restic_", "darwin_amd64.zip"],
         href_exclude_substrings=["windows", "linux", "386", "arm", ".bz2"], installer_extensions=[".zip"],
         use_download_filename=True, save_name="restic-darwin-amd64.zip"),
    **_repo("restic/restic"),
}])

# --- 03 写作：pandoc / mdbook / zola linux+darwin ---
_add("linux", "03-写作.json", [{
    "id": "pandoc", "简介": "Pandoc（Linux amd64 deb）", "分类": "写作",
    **_b(installer_markers_match_all=True, installer_markers=["pandoc-", "-1-amd64.deb"],
         href_exclude_substrings=["windows", "mac", "arm", "tar.gz"], installer_extensions=[".deb"],
         use_download_filename=True, save_name="pandoc-linux-amd64.deb"),
    **_repo("jgm/pandoc"),
}])
_add("darwin", "03-写作.json", [{
    "id": "pandoc", "简介": "Pandoc（macOS pkg）", "分类": "写作",
    **_b(installer_markers_match_all=True, installer_markers=["pandoc-", "-macOS.pkg"],
         href_exclude_substrings=["windows", "linux", "arm"], installer_extensions=[".pkg"],
         use_download_filename=True, save_name="pandoc-macOS.pkg"),
    **_repo("jgm/pandoc"),
}])
for plat, spec in (
    ("linux", dict(installer_markers=["mdbook-v", "x86_64-unknown-linux-gnu.tar.gz"],
                   save_name="mdbook-linux-x64.tar.gz")),
    ("darwin", dict(installer_markers=["mdbook-v", "x86_64-apple-darwin.tar.gz"],
                    save_name="mdbook-darwin-x64.tar.gz")),
):
    _entry(plat, "03-写作.json", id="mdbook", 简介="mdBook（Rust 静态书生成器）", 分类="写作", repo="rust-lang/mdBook",
           installer_extensions=[".tar.gz"], use_download_filename=True, **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["zola-v", "x86_64-unknown-linux-gnu.tar.gz"], save_name="zola-linux-x64.tar.gz")),
    ("darwin", dict(installer_markers=["zola-v", "x86_64-apple-darwin.tar.gz"], save_name="zola-darwin-x64.tar.gz")),
):
    _entry(plat, "03-写作.json", id="zola", 简介="Zola（静态站点生成器）", 分类="写作", repo="getzola/zola",
           installer_extensions=[".tar.gz"], use_download_filename=True, **spec)

# --- 25 可观测：Uptime Kuma（源码包，Docker 部署常用）---
_add("linux", "25-可观测.json", [{
    "id": "uptime_kuma", "简介": "Uptime Kuma（监控面板 dist 源码包，非安装程序）", "分类": "可观测",
    **_b(installer_markers=["dist.tar.gz"], href_exclude_substrings=["checksum"], installer_extensions=[".tar.gz"],
         use_download_filename=True, save_name="uptime-kuma-dist.tar.gz"),
    **_repo("louislam/uptime-kuma"),
}])
_add("darwin", "25-可观测.json", [{
    "id": "uptime_kuma", "简介": "Uptime Kuma（监控面板 dist 源码包）", "分类": "可观测",
    **_b(installer_markers=["dist.tar.gz"], installer_extensions=[".tar.gz"], use_download_filename=True,
         save_name="uptime-kuma-dist.tar.gz"),
    **_repo("louislam/uptime-kuma"),
}])
_add("windows", "25-可观测.json", [{
    "id": "uptime_kuma", "简介": "Uptime Kuma（监控面板 dist 源码包）", "分类": "可观测",
    **_b(installer_markers=["dist.tar.gz"], installer_extensions=[".tar.gz"], use_download_filename=True,
         save_name="uptime-kuma-dist.tar.gz"),
    **_repo("louislam/uptime-kuma"),
}])


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


def _strip_ids(path: str, ids: set[str]):
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        return
    new = [a for a in data if not (isinstance(a, dict) and a.get("id") in ids)]
    if len(new) != len(data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(new, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("CLEANED", path, "removed", ids)


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
    if not dry_run:
        for plat in ("linux", "darwin"):
            _strip_ids(os.path.join(APPS, plat, "99-未匹配-windows分片.json"), {"oh_my_posh"})
    return upserted, added, skipped


def main():
    dry = "--dry-run" in sys.argv
    u, a, s = merge_all(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: upserted {u}, added {a}, skipped duplicate {s}")


if __name__ == "__main__":
    main()
