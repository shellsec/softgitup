#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第三批跨平台补全：安全 CLI、编辑器、游戏、备份、AI、多媒体等剩余缺口。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
BATCH: dict[tuple[str, str], list] = {}


def _add(plat, shard, apps):
    BATCH.setdefault((plat, shard), []).extend(apps)


def _b(**kw):
    d = {"enabled": False, "prefer_api_assets": True, "version_tag_as_on_github": True,
         "windows_installer": False, "process_name": "", "kill_before_install": False, "run_installer": False}
    d.update(kw)
    return d


def _repo(repo):
    return {"releases_url": f"https://bgithub.xyz/{repo}/releases", "repo_path": repo}


def _e(plat, shard, id, 简介, 分类, repo, **cfg):
    _add(plat, shard, [{"id": id, "简介": 简介, "分类": 分类, **_b(**cfg), **_repo(repo)}])


def _cli_zip(id, shard, 分类, repo, 简介, prefix):
    for plat, token, excl in (("linux", "linux_amd64", ["windows", "darwin", "386"]),
                               ("darwin", "darwin_amd64", ["windows", "linux", "386"])):
        _e(plat, shard, id, 简介, 分类, repo, installer_markers_match_all=True,
           installer_markers=[prefix, token], href_exclude_substrings=excl + ["arm"],
           installer_extensions=[".zip"], download_names=[f"{prefix}{{ver}}_{token}.zip"],
           save_name=f"{prefix}{{ver}}_{token}.zip")


# --- 10 安全 ---
_cli_zip("httpx_pd", "10-安全.json", "安全", "projectdiscovery/httpx", "httpx（HTTP 探测）", "httpx_")
_cli_zip("fossa_cli", "10-安全.json", "安全", "fossas/fossa-cli", "FOSSA CLI", "fossa_")
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["kubescape_", "linux_amd64"],
                   href_exclude_substrings=["windows", "darwin", "sbom"], use_download_filename=True,
                   save_name="kubescape-linux-amd64")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["kubescape_", "darwin_amd64"],
                    href_exclude_substrings=["windows", "linux", "sbom"], use_download_filename=True,
                    save_name="kubescape-darwin-amd64")),
):
    _e(plat, "10-安全.json", "kubescape", "Kubescape（K8s 安全扫描）", "安全", "kubescape/kubescape", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["slsa-verifier-linux-amd64"], href_exclude_substrings=["windows", "darwin"],
                   use_download_filename=True, save_name="slsa-verifier-linux-amd64")),
    ("darwin", dict(installer_markers=["slsa-verifier-darwin-amd64"], href_exclude_substrings=["windows", "linux"],
                    use_download_filename=True, save_name="slsa-verifier-darwin-amd64")),
):
    _e(plat, "10-安全.json", "slsa_verifier", "slsa-verifier", "安全", "slsa-framework/slsa-verifier", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["rekor-cli-linux-amd64"], href_exclude_substrings=["windows", "darwin", "sbom"],
                   use_download_filename=True, save_name="rekor-cli-linux-amd64")),
    ("darwin", dict(installer_markers=["rekor-cli-darwin-amd64"], href_exclude_substrings=["windows", "linux", "sbom"],
                    use_download_filename=True, save_name="rekor-cli-darwin-amd64")),
):
    _e(plat, "10-安全.json", "rekor_cli", "Rekor CLI", "安全", "sigstore/rekor", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["kubeaudit_", "linux_amd64.tar.gz"], href_exclude_substrings=["windows", "darwin"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="kubeaudit-linux.tar.gz")),
    ("darwin", dict(installer_markers=["kubeaudit_", "darwin_amd64.tar.gz"], href_exclude_substrings=["windows", "linux"],
                    installer_extensions=[".tar.gz"], use_download_filename=True, save_name="kubeaudit-darwin.tar.gz")),
):
    _e(plat, "10-安全.json", "kubeaudit", "kubeaudit", "安全", "shopify/kubeaudit", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["crowdsec_", "linux_amd64.tar.gz"], href_exclude_substrings=["windows", "darwin", "msi"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="crowdsec-linux.tar.gz")),
    ("darwin", dict(installer_markers=["crowdsec_", "darwin_amd64.tar.gz"], href_exclude_substrings=["windows", "linux", "msi"],
                    installer_extensions=[".tar.gz"], use_download_filename=True, save_name="crowdsec-darwin.tar.gz")),
):
    _e(plat, "10-安全.json", "crowdsec", "CrowdSec", "安全", "crowdsecurity/crowdsec", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["osquery_", "linux_x86_64.tar.gz"], href_exclude_substrings=["windows", "darwin", "deb"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="osquery-linux.tar.gz")),
    ("darwin", dict(installer_markers=["osquery-", "darwin.pkg"], href_exclude_substrings=["windows", "linux", "deb"],
                    installer_extensions=[".pkg"], use_download_filename=True, save_name="osquery-darwin.pkg")),
):
    _e(plat, "10-安全.json", "osquery", "osquery", "安全", "osquery/osquery", **spec)
_e("linux", "10-安全.json", "clamav", "ClamAV（Linux deb）", "安全", "Cisco-Talos/clamav",
   installer_markers=["clamav_", "amd64.deb"], href_exclude_substrings=["win", "mac"], installer_extensions=[".deb"],
   use_download_filename=True, save_name="clamav-linux.deb")

# --- 26 编辑器 ---
for plat, spec in (
    ("linux", dict(installer_markers=["code-", "linux-x64.tar.gz"], href_exclude_substrings=["win32", "darwin", "arm"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="vscode-linux-x64.tar.gz")),
    ("darwin", dict(installer_markers=["VSCode-darwin-universal.zip"], href_exclude_substrings=["linux", "win32"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="vscode-darwin-universal.zip")),
):
    _e(plat, "26-编辑器.json", "vscode", "Visual Studio Code", "编辑器", "microsoft/vscode", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["sublime_merge_build", "_x64.deb"], href_exclude_substrings=["win", "osx", "arm"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="sublime_merge.deb")),
    ("darwin", dict(installer_markers=["sublime_merge_build", "_mac.zip"], href_exclude_substrings=["win", "deb"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="sublime_merge_mac.zip")),
):
    _e(plat, "26-编辑器.json", "sublime_merge", "Sublime Merge", "编辑器", "sublimehq/sublime_merge", **spec)
_e("darwin", "26-编辑器.json", "fork", "Fork（Git 客户端，macOS）", "编辑器", "fork-dev/fork",
   installer_markers=["Fork-", ".dmg"], href_exclude_substrings=["win", "exe"], installer_extensions=[".dmg"],
   use_download_filename=True, save_name="Fork.dmg")

# --- 07 备份 ---
for plat, spec in (
    ("linux", dict(installer_markers=["duplicacy_linux_x64_"], href_exclude_substrings=["win", "osx", "freebsd"],
                   use_download_filename=True, save_name="duplicacy-linux-x64")),
    ("darwin", dict(installer_markers=["duplicacy_osx_x64_"], href_exclude_substrings=["win", "linux", "freebsd"],
                    use_download_filename=True, save_name="duplicacy-osx-x64")),
):
    _e(plat, "07-备份.json", "duplicacy", "Duplicacy", "备份", "gilbertchen/duplicacy", **spec)
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["rustic-v", "x86_64-unknown-linux-gnu"],
                   href_exclude_substrings=["windows", "darwin", "musl"], installer_extensions=[".tar.gz"],
                   use_download_filename=True, save_name="rustic-linux-gnu.tar.gz")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["rustic-v", "aarch64-apple-darwin"],
                    href_exclude_substrings=["windows", "linux", "x86_64"], installer_extensions=[".tar.gz"],
                    use_download_filename=True, save_name="rustic-darwin-arm64.tar.gz")),
):
    _e(plat, "07-备份.json", "rustic", "rustic（restic 兼容）", "备份", "rustic-rs/rustic", **spec)

# --- 01 AI ---
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["Langflow_", "amd64.deb"],
                   href_exclude_substrings=["win", "mac", "msi"], installer_extensions=[".deb"],
                   use_download_filename=True, save_name="Langflow-linux.deb")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["Langflow_", "universal.dmg"],
                    href_exclude_substrings=["win", "linux", "msi"], installer_extensions=[".dmg"],
                    use_download_filename=True, save_name="Langflow-universal.dmg")),
):
    _e(plat, "01-AI.json", "langflow", "Langflow", "AI", "langflow-ai/langflow", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Goose-linux-x64", ".zip"], href_exclude_substrings=["win32", "darwin"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="Goose-linux-x64.zip")),
    ("darwin", dict(installer_markers=["Goose-darwin-x64", ".zip"], href_exclude_substrings=["win32", "linux"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="Goose-darwin-x64.zip")),
):
    _e(plat, "01-AI.json", "goose_desktop", "Goose 桌面版", "AI", "block/goose", **spec)

# --- 09 多媒体与设计 ---
for plat, spec in (
    ("linux", dict(installer_markers=["RawTherapee_", "AppImage"], href_exclude_substrings=["win", "osx"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="RawTherapee.AppImage")),
    ("darwin", dict(installer_markers=["RawTherapee_", "osx64.dmg"], href_exclude_substrings=["win", "appimage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="RawTherapee.dmg")),
):
    _e(plat, "09-多媒体与设计.json", "rawtherapee", "RawTherapee", "多媒体与设计", "Beep6581/RawTherapee", **spec)
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["ente-", "x86_64.AppImage"],
                   href_exclude_substrings=["win", "mac", "exe"], installer_extensions=[".AppImage"],
                   use_download_filename=True, save_name="ente-photos.AppImage")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["ente-", "universal.dmg"],
                    href_exclude_substrings=["win", "linux", "exe"], installer_extensions=[".dmg"],
                    use_download_filename=True, save_name="ente-photos.dmg")),
):
    _e(plat, "09-多媒体与设计.json", "ente_photos", "Ente Photos", "多媒体与设计", "ente-io/photos-desktop", **spec)

# --- 14 游戏 ---
for plat, spec in (
    ("linux", dict(installer_markers=["OpenRA-", "linux-x64.tar.gz"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="OpenRA-linux.tar.gz")),
    ("darwin", dict(installer_markers=["OpenRA-", "macos.dmg"], href_exclude_substrings=["win", "linux"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="OpenRA-macos.dmg")),
):
    _e(plat, "14-游戏.json", "openra", "OpenRA", "游戏", "OpenRA/OpenRA", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["OpenRCT2-", "linux-x86_64.tar.gz"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="OpenRCT2-linux.tar.gz")),
    ("darwin", dict(installer_markers=["OpenRCT2-", "macos-universal.dmg"], href_exclude_substrings=["win", "linux"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="OpenRCT2-macos.dmg")),
):
    _e(plat, "14-游戏.json", "openrct2", "OpenRCT2", "游戏", "OpenRCT2/OpenRCT2", **spec)
_e("linux", "14-游戏.json", "playnite", "Playnite（Linux AppImage）", "游戏", "JosefNemec/Playnite",
   installer_markers=["Playnite-", "Linux-x64.AppImage"], href_exclude_substrings=["win", "mac"],
   installer_extensions=[".AppImage"], use_download_filename=True, save_name="Playnite.AppImage")
for plat, spec in (
    ("linux", dict(installer_markers=["warzone2100_", "linux"], href_exclude_substrings=["win", "mac"], use_download_filename=True,
                   save_name="warzone2100-linux")),
    ("darwin", dict(installer_markers=["warzone2100_", "macos"], href_exclude_substrings=["win", "linux"], use_download_filename=True,
                    save_name="warzone2100-macos.dmg")),
):
    _e(plat, "14-游戏.json", "warzone2100", "Warzone 2100", "游戏", "Warzone2100/warzone2100", **spec)
_e("linux", "14-游戏.json", "xemu", "Xemu（Xbox 模拟器 AppImage）", "游戏", "xemu-project/xemu",
   installer_markers=["xemu-v", "AppImage"], href_exclude_substrings=["win", "mac"], installer_extensions=[".AppImage"],
   use_download_filename=True, save_name="xemu.AppImage")

# --- 27 金融 ---
for plat, spec in (
    ("linux", dict(installer_markers=["go-stock-linux-amd64"], href_exclude_substrings=["win", "darwin"],
                   use_download_filename=True, save_name="go-stock-linux-amd64")),
    ("darwin", dict(installer_markers=["go-stock-darwin-amd64"], href_exclude_substrings=["win", "linux"],
                    use_download_filename=True, save_name="go-stock-darwin-amd64")),
):
    _e(plat, "27-金融与股票.json", "go_stock", "go-stock", "金融与股票", "ArvinLovegood/go-stock", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["ta-lib-", "linux-x86_64.tar.gz"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="ta-lib-linux.tar.gz")),
    ("darwin", dict(installer_markers=["ta-lib-", "darwin-x86_64.tar.gz"], href_exclude_substrings=["win", "linux"],
                    installer_extensions=[".tar.gz"], use_download_filename=True, save_name="ta-lib-darwin.tar.gz")),
):
    _e(plat, "27-金融与股票.json", "ta_lib", "TA-Lib", "金融与股票", "ta-lib/ta-lib", **spec)

# --- 28 加密货币 ---
for plat, spec in (
    ("linux", dict(installer_markers=["feather-", "linux-x64.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="feather.AppImage")),
    ("darwin", dict(installer_markers=["feather-", "macos.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="feather.dmg")),
):
    _e(plat, "28-加密货币.json", "feather_wallet", "Feather Wallet", "加密货币", "feather-wallet/feather", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["specter-desktop-", "linux-x64.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="specter.AppImage")),
    ("darwin", dict(installer_markers=["specter-desktop-", "macos.dmg"], href_exclude_substrings=["win", "linux"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="specter.dmg")),
):
    _e(plat, "28-加密货币.json", "specter_desktop", "Specter Desktop", "加密货币", "cryptoadvance/specter-desktop", **spec)
_e("linux", "28-加密货币.json", "lnd", "LND（Lightning 节点 Linux）", "加密货币", "lightningnetwork/lnd",
   installer_markers=["lnd-linux-amd64-v", ".tar.gz"], href_exclude_substrings=["win", "mac", "arm"],
   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="lnd-linux-amd64.tar.gz")

# --- 13 效率 rambox ---
for plat, spec in (
    ("linux", dict(installer_markers=["Rambox-", "linux-x64.deb"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Rambox-linux.deb")),
    ("darwin", dict(installer_markers=["Rambox-", "mac-universal.dmg"], href_exclude_substrings=["win", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Rambox.dmg")),
):
    _e(plat, "13-效率.json", "rambox", "Rambox（多账号 Web 应用）", "效率", "ramboxapp/community-edition", **spec)

# --- 24 portainer darwin? skip - no official ---

# --- 22 obs darwin (gap was 1) ---
_e("darwin", "22-音视频.json", "obs", "OBS Studio（macOS Apple Silicon dmg）", "音视频", "obsproject/obs-studio",
   installer_markers_match_all=True, installer_markers=["OBS-Studio-", "macOS-Apple.dmg"],
   href_exclude_substrings=["Windows", "Linux", "Intel"], installer_extensions=[".dmg"],
   download_names=["OBS-Studio-{ver}-macOS-Apple.dmg"], save_name="OBS-Studio-{ver}-macOS-Apple.dmg", url_hint="OBS-Studio")


def merge_all(dry_run=False):
    added = skipped = 0
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            print("SKIP", path)
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


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    a, s = merge_all(dry)
    print(f"{'dry-run' if dry else 'written'}: added {a}, skipped {s}")
