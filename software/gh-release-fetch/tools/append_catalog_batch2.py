#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性向 apps/<platform>/*.json 追加条目（同平台 id 不可重复）。运行后勿重复执行。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
PLATFORMS = ("windows", "darwin", "linux")

# (platform, shard_file) -> list of app dicts
BATCH: dict[tuple[str, str], list] = {}

def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


# --- 02 下载 ---
_qbt = {
    "简介": "qBittorrent（BT/磁力）",
    "分类": "下载",
    "enabled": False,
    "prefer_api_assets": True,
    "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/qbittorrent/qBittorrent/releases",
    "repo_path": "qbittorrent/qBittorrent",
}
_add("windows", "02-下载.json", [{**_qbt, "id": "qbittorrent", "installer_markers_match_all": True, "installer_markers": ["qbittorrent_", "_x64_setup.exe"], "href_exclude_substrings": ["_lt20_", ".asc", "arm64", "x86"], "windows_installer": True, "download_names": ["qbittorrent_{ver}_x64_setup.exe"], "save_name": "qbittorrent_{ver}_x64_setup.exe", "process_name": "qbittorrent.exe", "kill_before_install": True, "run_installer": True}])
_add("linux", "02-下载.json", [{**_qbt, "id": "qbittorrent", "installer_markers_match_all": True, "installer_markers": ["qbittorrent_", "_x86_64.AppImage"], "href_exclude_substrings": ["Windows", "Darwin", "arm64", ".asc"], "windows_installer": False, "installer_extensions": [".AppImage"], "use_download_filename": True, "save_name": "qbittorrent.AppImage", "process_name": "", "kill_before_install": False, "run_installer": False}])
_add("darwin", "02-下载.json", [{**_qbt, "id": "qbittorrent", "installer_markers_match_all": True, "installer_markers": ["qbittorrent_", "_dmg"], "href_exclude_substrings": ["Windows", "Linux", ".asc"], "windows_installer": False, "installer_extensions": [".dmg"], "use_download_filename": True, "save_name": "qbittorrent.dmg", "process_name": "", "kill_before_install": False, "run_installer": False}])

_trans = {
    "简介": "Transmission（BT 客户端）",
    "分类": "下载",
    "enabled": False,
    "prefer_api_assets": True,
    "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/transmission/transmission/releases",
    "repo_path": "transmission/transmission",
}
_add("linux", "02-下载.json", [{**_trans, "id": "transmission", "installer_markers_match_all": True, "installer_markers": ["transmission-", "-x64.AppImage"], "href_exclude_substrings": ["qt5", "pdb", "dsym", "windows", "darwin"], "windows_installer": False, "installer_extensions": [".AppImage"], "download_names": ["transmission-{ver}-x64.AppImage"], "save_name": "transmission-{ver}-x64.AppImage", "process_name": "", "kill_before_install": False, "run_installer": False}])
_add("darwin", "02-下载.json", [{**_trans, "id": "transmission", "installer_markers_match_all": True, "installer_markers": ["Transmission-", "-.dmg"], "href_exclude_substrings": ["windows", "linux", "pdb"], "windows_installer": False, "installer_extensions": [".dmg"], "download_names": ["Transmission-{ver}.dmg"], "save_name": "Transmission-{ver}.dmg", "process_name": "", "kill_before_install": False, "run_installer": False}])

# --- 11 工具 ---
_add("linux", "11-工具.json", [{
    "id": "7zip", "简介": "7-Zip（Linux x64 tar.xz，ip7z/7zip）", "分类": "工具", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/ip7z/7zip/releases", "repo_path": "ip7z/7zip",
    "installer_markers_match_all": True, "installer_markers": ["7z", "linux-x64.tar.xz"],
    "href_exclude_substrings": ["arm", "mac", "win", "extra"], "windows_installer": False,
    "installer_extensions": [".xz"], "use_download_filename": True, "save_name": "7zip-linux-x64.tar.xz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 08 多媒体 jellyfin_server ---
_jfs = {"id": "jellyfin_server", "简介": "Jellyfin 媒体服务器（安装见 jellyfin.org；GitHub 主仓常无安装包，勿启用）", "分类": "多媒体", "enabled": False, "releases_url": "https://bgithub.xyz/jellyfin/jellyfin/releases", "repo_path": "jellyfin/jellyfin", "windows_installer": False, "process_name": "", "kill_before_install": False, "run_installer": False, "url_hint": "jellyfin"}
for plat in PLATFORMS:
    _add(plat, "08-多媒体.json", [_jfs.copy()])

# --- 09 godot ---
_godot_base = {"简介": "Godot 游戏引擎", "分类": "多媒体与设计", "enabled": False, "prefer_api_assets": True, "version_tag_as_on_github": True, "releases_url": "https://bgithub.xyz/godotengine/godot/releases", "repo_path": "godotengine/godot", "href_exclude_substrings": ["mono", "android", "web_editor", "debug_symbols"], "windows_installer": False, "process_name": "", "kill_before_install": False, "run_installer": False}
_add("linux", "09-多媒体与设计.json", [{**_godot_base, "id": "godot", "installer_markers_match_all": True, "installer_markers": ["Godot_v", "linux.x86_64.zip"], "href_exclude_substrings": _godot_base["href_exclude_substrings"] + ["win64", "macos", "arm64"], "installer_extensions": [".zip"], "download_names": ["Godot_v{ver}_linux.x86_64.zip"], "save_name": "Godot_v{ver}_linux.x86_64.zip"}])
_add("darwin", "09-多媒体与设计.json", [{**_godot_base, "id": "godot", "installer_markers_match_all": True, "installer_markers": ["Godot_v", "macos.universal.zip"], "href_exclude_substrings": _godot_base["href_exclude_substrings"] + ["linux", "win64"], "installer_extensions": [".zip"], "download_names": ["Godot_v{ver}_macos.universal.zip"], "save_name": "Godot_v{ver}_macos.universal.zip"}])

# --- 29 filebrowser + alist ---
_add("linux", "29-局域网文件共享.json", [{
    "id": "filebrowser", "简介": "FileBrowser（Linux amd64 tar.gz）", "分类": "局域网文件共享", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/filebrowser/filebrowser/releases", "repo_path": "filebrowser/filebrowser",
    "installer_markers_match_all": True, "installer_markers": ["linux-amd64-filebrowser.tar.gz"],
    "href_exclude_substrings": ["windows", "darwin", "386", "arm64"], "windows_installer": False,
    "installer_extensions": [".tar.gz"], "use_download_filename": True, "save_name": "linux-amd64-filebrowser.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("darwin", "29-局域网文件共享.json", [{
    "id": "filebrowser", "简介": "FileBrowser（macOS arm64 tar.gz）", "分类": "局域网文件共享", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/filebrowser/filebrowser/releases", "repo_path": "filebrowser/filebrowser",
    "installer_markers_match_all": True, "installer_markers": ["darwin-arm64-filebrowser.tar.gz"],
    "href_exclude_substrings": ["windows", "linux", "amd64-filebrowser"], "windows_installer": False,
    "installer_extensions": [".tar.gz"], "use_download_filename": True, "save_name": "darwin-arm64-filebrowser.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("windows", "29-局域网文件共享.json", [{
    "id": "alist", "简介": "AList（多网盘挂载，Windows amd64 zip）", "分类": "局域网文件共享", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/AlistGo/alist/releases", "repo_path": "AlistGo/alist",
    "installer_markers_match_all": True, "installer_markers": ["windows-amd64", ".zip"],
    "href_exclude_substrings": ["linux", "darwin", "arm64", "386", ".tar.gz"], "windows_installer": False,
    "installer_extensions": [".zip"], "download_names": ["alist-windows-amd64-{ver}.zip"],
    "save_name": "alist-windows-amd64-{ver}.zip", "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "29-局域网文件共享.json", [{
    "id": "alist", "简介": "AList（Linux amd64 tar.gz）", "分类": "局域网文件共享", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/AlistGo/alist/releases", "repo_path": "AlistGo/alist",
    "installer_markers_match_all": True, "installer_markers": ["linux-amd64", ".tar.gz"],
    "href_exclude_substrings": ["windows", "darwin", "arm64", "386"], "windows_installer": False,
    "installer_extensions": [".tar.gz"], "download_names": ["alist-linux-amd64-{ver}.tar.gz"],
    "save_name": "alist-linux-amd64-{ver}.tar.gz", "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 17 ghostty darwin/linux ---
_add("darwin", "17-终端.json", [{
    "id": "ghostty", "简介": "Ghostty 终端（macOS universal zip）", "分类": "终端", "enabled": False,
    "prefer_api_assets": True, "releases_url": "https://bgithub.xyz/ghostty-org/ghostty/releases", "repo_path": "ghostty-org/ghostty",
    "installer_markers_match_all": True, "installer_markers": ["ghostty-macos-universal.zip"],
    "href_exclude_substrings": ["debug", "source", "linux"], "windows_installer": False,
    "installer_extensions": [".zip"], "use_download_filename": True, "save_name": "ghostty-macos-universal.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "17-终端.json", [{
    "id": "ghostty", "简介": "Ghostty 终端（Linux 构建见官方文档；Release 以 tag 资产为准，优先 tar.gz/zip）", "分类": "终端", "enabled": False,
    "prefer_api_assets": True, "releases_url": "https://bgithub.xyz/ghostty-org/ghostty/releases", "repo_path": "ghostty-org/ghostty",
    "installer_markers": ["ghostty", "linux"], "href_exclude_substrings": ["macos", "source", "debug"],
    "windows_installer": False, "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 30 sing-box / mihomo linux darwin ---
_sb = {"简介": "sing-box 代理内核", "分类": "代理与隧道", "enabled": False, "prefer_api_assets": True, "version_tag_as_on_github": True, "releases_url": "https://bgithub.xyz/SagerNet/sing-box/releases", "repo_path": "SagerNet/sing-box", "windows_installer": False, "process_name": "", "kill_before_install": False, "run_installer": False}
_add("linux", "30-代理与隧道.json", [{**_sb, "id": "sing_box_linux_amd64", "installer_markers_match_all": True, "installer_markers": ["sing-box-", "linux-amd64.tar.gz"], "href_exclude_substrings": ["386", "arm64", "windows", "darwin", "android", "dSYM"], "installer_extensions": [".tar.gz"], "download_names": ["sing-box-{ver}-linux-amd64.tar.gz"], "save_name": "sing-box-{ver}-linux-amd64.tar.gz"}])
_add("darwin", "30-代理与隧道.json", [{**_sb, "id": "sing_box_macos_arm64", "installer_markers_match_all": True, "installer_markers": ["sing-box-", "darwin-arm64.tar.gz"], "href_exclude_substrings": ["386", "amd64-legacy", "windows", "linux", "android"], "installer_extensions": [".tar.gz"], "download_names": ["sing-box-{ver}-darwin-arm64.tar.gz"], "save_name": "sing-box-{ver}-darwin-arm64.tar.gz"}])
_add("linux", "30-代理与隧道.json", [{**_sb, "id": "mihomo_linux_amd64", "简介": "mihomo Clash Meta 内核（Linux amd64 gz）", "installer_markers_match_all": True, "installer_markers": ["mihomo-linux-amd64-v", ".gz"], "href_exclude_substrings": ["go120", "go121", "go122", "go123", "compatible", "arm64", "windows", "darwin", "android", ".deb", ".rpm"], "installer_extensions": [".gz"], "download_names": ["mihomo-linux-amd64-v{ver}.gz"], "save_name": "mihomo-linux-amd64-v{ver}.gz"}])
_add("darwin", "30-代理与隧道.json", [{**_sb, "id": "mihomo_macos_arm64", "简介": "mihomo（macOS arm64 gz）", "installer_markers_match_all": True, "installer_markers": ["mihomo-darwin-arm64-v", ".gz"], "href_exclude_substrings": ["go120", "go121", "compatible", "amd64", "windows", "linux", "android"], "installer_extensions": [".gz"], "download_names": ["mihomo-darwin-arm64-v{ver}.gz"], "save_name": "mihomo-darwin-arm64-v{ver}.gz"}])
_add("darwin", "30-代理与隧道.json", [{
    "id": "hiddify_next", "简介": "Hiddify Next（macOS pkg）", "分类": "代理与隧道", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/hiddify/hiddify-next/releases", "repo_path": "hiddify/hiddify-next",
    "installer_markers_match_all": True, "installer_markers": ["Hiddify-MacOS-Installer.pkg"],
    "href_exclude_substrings": ["dmg", "Windows", "Linux", "Android"], "windows_installer": False,
    "installer_extensions": [".pkg"], "download_names": ["Hiddify-MacOS-Installer.pkg"], "save_name": "Hiddify-MacOS-Installer.pkg",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("darwin", "30-代理与隧道.json", [{
    "id": "flclash_macos_arm64", "简介": "FlClash（macOS arm64 dmg）", "分类": "代理与隧道", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/chen08209/FlClash/releases", "repo_path": "chen08209/FlClash",
    "installer_markers_match_all": True, "installer_markers": ["FlClash-", "macos-arm64.dmg"],
    "href_exclude_substrings": ["windows", "linux", "android", ".sha256"], "windows_installer": False,
    "installer_extensions": [".dmg"], "download_names": ["FlClash-{ver}-macos-arm64.dmg"], "save_name": "FlClash-{ver}-macos-arm64.dmg",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 28 crypto linux/darwin ---
_bc = {"简介": "Bitcoin Core", "分类": "加密货币", "enabled": False, "prefer_api_assets": True, "version_tag_as_on_github": True, "releases_url": "https://bgithub.xyz/bitcoin-core/gui/releases", "repo_path": "bitcoin-core/gui", "installer_markers_match_all": True, "installer_markers": ["bitcoin-", "-setup"], "href_exclude_substrings": [".asc", "linux", "win64-setup.exe"]}
_add("linux", "28-加密货币.json", [{**_bc, "id": "bitcoin_core", "installer_markers": ["bitcoin-", "x86_64-linux-gnu.tar.gz"], "href_exclude_substrings": [".asc", "windows", "osx", "arm64", "setup"], "windows_installer": False, "installer_extensions": [".tar.gz"], "download_names": ["bitcoin-{ver}-x86_64-linux-gnu.tar.gz"], "save_name": "bitcoin-{ver}-x86_64-linux-gnu.tar.gz", "process_name": "", "kill_before_install": False, "run_installer": False}])
_add("darwin", "28-加密货币.json", [{**_bc, "id": "bitcoin_core", "installer_markers": ["bitcoin-", "x86_64-apple-darwin.dmg"], "href_exclude_substrings": [".asc", "windows", "linux", "arm64"], "windows_installer": False, "installer_extensions": [".dmg"], "download_names": ["bitcoin-{ver}-x86_64-apple-darwin.dmg"], "save_name": "bitcoin-{ver}-x86_64-apple-darwin.dmg", "process_name": "", "kill_before_install": False, "run_installer": False}])
_add("linux", "28-加密货币.json", [{
    "id": "electrum", "简介": "Electrum 轻钱包（Linux AppImage）", "分类": "加密货币", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/spesmilo/electrum/releases", "repo_path": "spesmilo/electrum",
    "installer_markers_match_all": True, "installer_markers": ["electrum-", "AppImage"],
    "href_exclude_substrings": [".asc", "windows", "mac", "tar.gz"], "windows_installer": False,
    "installer_extensions": [".AppImage"], "download_names": ["electrum-{ver}-x86_64.AppImage"], "save_name": "electrum-{ver}-x86_64.AppImage",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("darwin", "28-加密货币.json", [{
    "id": "electrum", "简介": "Electrum（macOS dmg）", "分类": "加密货币", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/spesmilo/electrum/releases", "repo_path": "spesmilo/electrum",
    "installer_markers_match_all": True, "installer_markers": ["electrum-", ".dmg"],
    "href_exclude_substrings": [".asc", "windows", "linux", "AppImage"], "windows_installer": False,
    "installer_extensions": [".dmg"], "download_names": ["electrum-{ver}.dmg"], "save_name": "electrum-{ver}.dmg",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 12 开发 实用 ---
_add("windows", "12-开发.json", [{
    "id": "forgejo", "简介": "Forgejo（Git 托管，Windows amd64 zip）", "分类": "开发", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/forgejo/forgejo/releases", "repo_path": "forgejo/forgejo",
    "installer_markers_match_all": True, "installer_markers": ["forgejo-", "windows-4.0-amd64.zip"],
    "href_exclude_substrings": ["linux", "darwin", "arm64", "386", ".asc", "src"], "windows_installer": False,
    "installer_extensions": [".zip"], "download_names": ["forgejo-{ver}-windows-4.0-amd64.zip"], "save_name": "forgejo-{ver}-windows-4.0-amd64.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "12-开发.json", [{
    "id": "forgejo", "enabled": False, "releases_url": "https://bgithub.xyz/forgejo/forgejo/releases", "repo_path": "forgejo/forgejo",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "Forgejo（Linux amd64）", "分类": "开发",
    "installer_markers_match_all": True, "installer_markers": ["forgejo-", "linux-4.0-amd64.zip"],
    "href_exclude_substrings": ["windows", "darwin", "arm64"], "windows_installer": False, "installer_extensions": [".zip"],
    "download_names": ["forgejo-{ver}-linux-4.0-amd64.zip"], "save_name": "forgejo-{ver}-linux-4.0-amd64.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("windows", "12-开发.json", [{
    "id": "playwright_cli", "简介": "Playwright CLI（Node 驱动浏览器自动化，Release zip）", "分类": "开发", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/microsoft/playwright/releases", "repo_path": "microsoft/playwright",
    "installer_markers": ["playwright-", "win64.zip"], "href_exclude_substrings": ["linux", "mac", "arm64"],
    "windows_installer": False, "installer_extensions": [".zip"], "download_names": ["playwright-{ver}-win64.zip"],
    "save_name": "playwright-{ver}-win64.zip", "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("windows", "12-开发.json", [{
    "id": "act", "简介": "act（本地运行 GitHub Actions，Windows x64 zip）", "分类": "开发", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/nektos/act/releases", "repo_path": "nektos/act",
    "installer_markers_match_all": True, "installer_markers": ["act_Windows", "x86_64.zip"],
    "href_exclude_substrings": ["Linux", "Darwin", "arm64", "i386", "checksum"], "windows_installer": False,
    "installer_extensions": [".zip"], "download_names": ["act_Windows_{ver}_x86_64.zip"], "save_name": "act_Windows_{ver}_x86_64.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "12-开发.json", [{
    "id": "act", "enabled": False, "releases_url": "https://bgithub.xyz/nektos/act/releases", "repo_path": "nektos/act",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "act（Linux x64）", "分类": "开发",
    "installer_markers_match_all": True, "installer_markers": ["act_Linux", "x86_64.tar.gz"],
    "href_exclude_substrings": ["Windows", "Darwin", "arm64"], "windows_installer": False, "installer_extensions": [".tar.gz"],
    "download_names": ["act_Linux_{ver}_x86_64.tar.gz"], "save_name": "act_Linux_{ver}_x86_64.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("darwin", "12-开发.json", [{
    "id": "act", "enabled": False, "releases_url": "https://bgithub.xyz/nektos/act/releases", "repo_path": "nektos/act",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "act（macOS arm64）", "分类": "开发",
    "installer_markers_match_all": True, "installer_markers": ["act_Darwin", "arm64.tar.gz"],
    "href_exclude_substrings": ["Windows", "Linux", "x86_64"], "windows_installer": False, "installer_extensions": [".tar.gz"],
    "download_names": ["act_Darwin_{ver}_arm64.tar.gz"], "save_name": "act_Darwin_{ver}_arm64.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 10 安全 OWASP ZAP ---
_add("windows", "10-安全.json", [{
    "id": "owasp_zap", "简介": "OWASP ZAP（Web 安全测试，Windows 安装包）", "分类": "安全", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/zaproxy/zaproxy/releases", "repo_path": "zaproxy/zaproxy",
    "installer_markers_match_all": True, "installer_markers": ["ZAP_", "_Windows.exe"],
    "href_exclude_substrings": ["Linux", "Darwin", "CrossPlatform", ".sha512"], "windows_installer": True,
    "download_names": ["ZAP_{ver}_Windows.exe"], "save_name": "ZAP_{ver}_Windows.exe",
    "process_name": "", "kill_before_install": False, "run_installer": True,
}])
_add("linux", "10-安全.json", [{
    "id": "owasp_zap", "enabled": False, "releases_url": "https://bgithub.xyz/zaproxy/zaproxy/releases", "repo_path": "zaproxy/zaproxy",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "OWASP ZAP（Linux 包）", "分类": "安全",
    "installer_markers_match_all": True, "installer_markers": ["ZAP_", "_Linux.tar.gz"],
    "href_exclude_substrings": ["Windows", "Darwin"], "windows_installer": False, "installer_extensions": [".tar.gz"],
    "download_names": ["ZAP_{ver}_Linux.tar.gz"], "save_name": "ZAP_{ver}_Linux.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 18 网络 ZeroTier ---
_zt = {"id": "zerotier", "简介": "ZeroTier 虚拟组网", "分类": "网络", "enabled": False, "prefer_api_assets": True, "version_tag_as_on_github": True, "releases_url": "https://bgithub.xyz/zerotier/ZeroTierOne/releases", "repo_path": "zerotier/ZeroTierOne", "process_name": "", "kill_before_install": False}
_add("windows", "18-网络.json", [{**_zt, "installer_markers_match_all": True, "installer_markers": ["ZeroTier One", "x64.msi"], "href_exclude_substrings": ["arm64", "x86", ".deb", ".pkg"], "windows_installer": True, "installer_extensions": [".msi"], "download_names": ["ZeroTier One {ver} x64.msi"], "save_name": "ZeroTier One {ver} x64.msi", "run_installer": True}])
_add("linux", "18-网络.json", [{**_zt, "installer_markers_match_all": True, "installer_markers": ["zerotier", "x86_64", ".deb"], "href_exclude_substrings": ["windows", "darwin", "arm64", "386"], "windows_installer": False, "installer_extensions": [".deb"], "use_download_filename": True, "save_name": "zerotier.deb", "run_installer": False}])
_add("darwin", "18-网络.json", [{**_zt, "installer_markers_match_all": True, "installer_markers": ["ZeroTier One", ".pkg"], "href_exclude_substrings": ["windows", "linux", ".deb"], "windows_installer": False, "installer_extensions": [".pkg"], "use_download_filename": True, "save_name": "ZeroTier.pkg", "run_installer": False}])

# --- 22 音视频 OpenShot ---
_add("windows", "22-音视频.json", [{
    "id": "openshot", "简介": "OpenShot 视频编辑器（Windows x64 exe）", "分类": "音视频", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/OpenShot/openshot-qt/releases", "repo_path": "OpenShot/openshot-qt",
    "installer_markers_match_all": True, "installer_markers": ["OpenShot", "x64.exe"],
    "href_exclude_substrings": ["dmg", "AppImage", "arm64", "portable"], "windows_installer": True,
    "download_names": ["OpenShot-v{ver}-x64.exe"], "save_name": "OpenShot-v{ver}-x64.exe",
    "process_name": "", "kill_before_install": False, "run_installer": True,
}])
_add("linux", "22-音视频.json", [{
    "id": "openshot", "enabled": False, "releases_url": "https://bgithub.xyz/OpenShot/openshot-qt/releases", "repo_path": "OpenShot/openshot-qt",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "OpenShot（AppImage）", "分类": "音视频",
    "installer_markers_match_all": True, "installer_markers": ["OpenShot", "x86_64.AppImage"],
    "href_exclude_substrings": ["exe", "dmg"], "windows_installer": False, "installer_extensions": [".AppImage"],
    "download_names": ["OpenShot-v{ver}-x86_64.AppImage"], "save_name": "OpenShot-v{ver}-x86_64.AppImage",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 26 编辑器 Pulsar / Lite XL ---
_add("windows", "26-编辑器.json", [{
    "id": "pulsar", "简介": "Pulsar（Atom 继任编辑器，Windows zip）", "分类": "编辑器", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/pulsar-edit/pulsar/releases", "repo_path": "pulsar-edit/pulsar",
    "installer_markers_match_all": True, "installer_markers": ["Pulsar.Setup.", "x64.exe"],
    "href_exclude_substrings": ["arm64", "mac", "linux", ".blockmap"], "windows_installer": True,
    "download_names": ["Pulsar.Setup.{ver}.x64.exe"], "save_name": "Pulsar.Setup.{ver}.x64.exe",
    "process_name": "", "kill_before_install": False, "run_installer": True,
}])
_add("windows", "26-编辑器.json", [{
    "id": "lite_xl", "简介": "Lite XL（轻量 Lua 编辑器，Windows portable zip）", "分类": "编辑器", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/lite-xl/lite-xl/releases", "repo_path": "lite-xl/lite-xl",
    "installer_markers_match_all": True, "installer_markers": ["lite-xl-", "windows-x86_64.zip"],
    "href_exclude_substrings": ["linux", "macos", "arm64", "installer"], "windows_installer": False,
    "installer_extensions": [".zip"], "download_names": ["lite-xl-{ver}-windows-x86_64.zip"], "save_name": "lite-xl-{ver}-windows-x86_64.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "26-编辑器.json", [{
    "id": "lite_xl", "enabled": False, "releases_url": "https://bgithub.xyz/lite-xl/lite-xl/releases", "repo_path": "lite-xl/lite-xl",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "Lite XL（Linux x86_64 tar.gz）", "分类": "编辑器",
    "installer_markers_match_all": True, "installer_markers": ["lite-xl-", "linux-x86_64.tar.gz"],
    "href_exclude_substrings": ["windows", "macos", "arm64"], "windows_installer": False, "installer_extensions": [".tar.gz"],
    "download_names": ["lite-xl-{ver}-linux-x86_64.tar.gz"], "save_name": "lite-xl-{ver}-linux-x86_64.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 01 AI aider ---
_add("windows", "01-AI.json", [{
    "id": "aider", "简介": "aider（终端 AI 结对编程，Windows exe）", "分类": "AI", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/Aider-AI/aider/releases", "repo_path": "Aider-AI/aider",
    "installer_markers_match_all": True, "installer_markers": ["aider-", "windows-x86_64.exe"],
    "href_exclude_substrings": ["linux", "darwin", "arm64", ".sha256"], "windows_installer": False,
    "installer_extensions": [".exe"], "download_names": ["aider-{ver}-windows-x86_64.exe"], "save_name": "aider-{ver}-windows-x86_64.exe",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])
_add("linux", "01-AI.json", [{
    "id": "aider", "enabled": False, "releases_url": "https://bgithub.xyz/Aider-AI/aider/releases", "repo_path": "Aider-AI/aider",
    "prefer_api_assets": True, "version_tag_as_on_github": True, "简介": "aider（Linux x86_64）", "分类": "AI",
    "installer_markers_match_all": True, "installer_markers": ["aider-", "linux-x86_64.tar.gz"],
    "href_exclude_substrings": ["windows", "darwin", "arm64"], "windows_installer": False, "installer_extensions": [".tar.gz"],
    "download_names": ["aider-{ver}-linux-x86_64.tar.gz"], "save_name": "aider-{ver}-linux-x86_64.tar.gz",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 23 数据库 Redis Insight ---
_add("windows", "23-数据库.json", [{
    "id": "redis_insight", "简介": "Redis Insight（Redis 图形客户端，Windows exe）", "分类": "数据库", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/RedisInsight/RedisInsight/releases", "repo_path": "RedisInsight/RedisInsight",
    "installer_markers_match_all": True, "installer_markers": ["Redis-Insight-win-installer", ".exe"],
    "href_exclude_substrings": ["linux", "darwin", "arm64", ".blockmap"], "windows_installer": True,
    "download_names": ["Redis-Insight-win-installer.{ver}.exe"], "save_name": "Redis-Insight-win-installer.{ver}.exe",
    "process_name": "", "kill_before_install": False, "run_installer": True,
}])

# --- 14 游戏 Ryujinx ---
_add("windows", "14-游戏.json", [{
    "id": "ryujinx", "简介": "Ryujinx（Nintendo Switch 模拟器，Windows x64 便携 zip）", "分类": "游戏", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/Ryubing/Ryujinx/releases", "repo_path": "Ryubing/Ryujinx",
    "installer_markers_match_all": True, "installer_markers": ["ryujinx-", "win-x64.zip"],
    "href_exclude_substrings": ["linux", "osx", "arm64", "publish"], "windows_installer": False,
    "installer_extensions": [".zip"], "download_names": ["ryujinx-{ver}-win-x64.zip"], "save_name": "ryujinx-{ver}-win-x64.zip",
    "process_name": "", "kill_before_install": False, "run_installer": False,
}])

# --- 25 可观测 Netdata ---
_add("linux", "25-可观测.json", [{
    "id": "netdata", "简介": "Netdata（监控 Agent，Linux 静态二进制）", "分类": "可观测", "enabled": False,
    "prefer_api_assets": True, "version_tag_as_on_github": True,
    "releases_url": "https://bgithub.xyz/netdata/netdata/releases", "repo_path": "netdata/netdata",
    "installer_markers": ["netdata-", "x86_64.gz"], "href_exclude_substrings": ["arm", "ppc", "s390", "windows", "darwin"],
    "windows_installer": False, "installer_extensions": [".gz"], "process_name": "", "kill_before_install": False, "run_installer": False,
}])


def merge_batch(dry_run: bool = False):
    added = 0
    skipped = 0
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            print("SKIP missing", path)
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("SKIP not array", path)
            continue
        seen = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
        for app in apps:
            aid = (app.get("id") or "").strip()
            if not aid:
                continue
            if aid in seen:
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
    mode = "dry-run" if dry else "written"
    print(f"{mode}: added {added}, skipped duplicate id {skipped}")


if __name__ == "__main__":
    main()
