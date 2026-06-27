#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""跨平台缺口大补：将 Windows 已有、Linux/macOS 缺失的跨平台条目批量实装。"""
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


def _repo(repo: str) -> dict:
    return {
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
    }


def _entry(plat, shard, *, id, 简介, 分类, repo, **cfg):
    _add(plat, shard, [{"id": id, "简介": 简介, "分类": 分类, **_b(**cfg), **_repo(repo)}])


def _cli_zip(id, shard, 分类, repo, 简介, prefix, ver_in_name=True):
    """{prefix}{ver}_linux_amd64.zip 类 Hashicorp/Anchore 命名。"""
    for plat, token, excl in (
        ("linux", "linux_amd64", ["windows", "darwin", "386", "arm"]),
        ("darwin", "darwin_amd64", ["windows", "linux", "386", "arm"]),
    ):
        if ver_in_name:
            dn = [f"{prefix}{{ver}}_{token}.zip"]
            sn = f"{prefix}{{ver}}_{token}.zip"
        else:
            dn = [f"{prefix}{token}.zip"]
            sn = f"{prefix}{token}.zip"
        _entry(
            plat, shard, id=id, 简介=简介, 分类=分类, repo=repo,
            installer_markers_match_all=True,
            installer_markers=[prefix, token],
            href_exclude_substrings=excl,
            installer_extensions=[".zip"],
            download_names=dn,
            save_name=sn,
        )


def _cli_plain(id, shard, 分类, repo, 简介, marker, excl_linux, excl_darwin, ext=""):
    _entry("linux", shard, id=id, 简介=简介, 分类=分类, repo=repo,
           installer_markers=[marker], href_exclude_substrings=excl_linux,
           use_download_filename=True, save_name=f"{id}-linux{ext}")
    _entry("darwin", shard, id=id, 简介=简介, 分类=分类, repo=repo,
           installer_markers=[marker.replace("linux", "darwin").replace("Linux", "Darwin")],
           href_exclude_substrings=excl_darwin,
           use_download_filename=True, save_name=f"{id}-darwin{ext}")


# --- 06 命令行 ---
for plat, spec in (
    ("linux", dict(installer_markers=["micro-", "linux64"], href_exclude_substrings=["win", "mac", "darwin"],
                   use_download_filename=True, save_name="micro-linux64.zip")),
    ("darwin", dict(installer_markers=["micro-", "darwin"], href_exclude_substrings=["win", "linux"],
                    use_download_filename=True, save_name="micro-darwin.zip")),
):
    _entry(plat, "06-命令行.json", id="micro", 简介="micro（终端编辑器）", 分类="命令行",
           repo="zyedidia/micro", **spec)
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["nu-", "x86_64-unknown-linux-gnu"],
                   href_exclude_substrings=["windows", "darwin", "musl"], installer_extensions=[".tar.gz"],
                   use_download_filename=True, save_name="nu-linux-x86_64.tar.gz")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["nu-", "aarch64-apple-darwin"],
                    href_exclude_substrings=["windows", "linux", "x86_64"], installer_extensions=[".tar.gz"],
                    use_download_filename=True, save_name="nu-darwin-arm64.tar.gz")),
):
    _entry(plat, "06-命令行.json", id="nushell", 简介="Nushell（结构化 Shell）", 分类="命令行",
           repo="nushell/nushell", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["lsd_", "x86_64-unknown-linux-gnu"], href_exclude_substrings=["windows", "apple"],
                   use_download_filename=True, save_name="lsd-linux-x86_64")),
    ("darwin", dict(installer_markers=["lsd_", "aarch64-apple-darwin"], href_exclude_substrings=["windows", "linux-gnu"],
                    use_download_filename=True, save_name="lsd-darwin-arm64")),
):
    _entry(plat, "06-命令行.json", id="lsd", 简介="lsd（彩色 ls）", 分类="命令行", repo="lsd-rs/lsd", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["ripgrep_all-v", "x86_64-unknown-linux-musl"],
                   href_exclude_substrings=["windows", "apple", "gnu"], use_download_filename=True,
                   save_name="ripgrep_all-linux-musl")),
    ("darwin", dict(installer_markers=["ripgrep_all-v", "aarch64-apple-darwin"],
                    href_exclude_substrings=["windows", "linux"], use_download_filename=True,
                    save_name="ripgrep_all-darwin-arm64")),
):
    _entry(plat, "06-命令行.json", id="ripgrep_all", 简介="ripgrep-all（PDF/Office 内 ripgrep）", 分类="命令行",
           repo="phiresky/ripgrep-all", **spec)

# --- 12 开发 ---
_cli_zip("glab", "12-开发.json", "开发", "gitlab-org/cli", "glab（GitLab CLI）", "glab_")
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["gitea-", "linux-amd64"],
                   href_exclude_substrings=["windows", "darwin", "arm", "386"], use_download_filename=True,
                   save_name="gitea-linux-amd64")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["gitea-", "darwin-amd64"],
                    href_exclude_substrings=["windows", "linux", "arm"], use_download_filename=True,
                    save_name="gitea-darwin-amd64")),
):
    _entry(plat, "12-开发.json", id="gitea", 简介="Gitea（轻量 Git 服务二进制）", 分类="开发",
           repo="go-gitea/gitea", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["fnm-linux.zip"], href_exclude_substrings=["windows", "mac"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="fnm-linux.zip")),
    ("darwin", dict(installer_markers=["fnm-macos.zip"], href_exclude_substrings=["windows", "linux"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="fnm-macos.zip")),
):
    _entry(plat, "12-开发.json", id="fnm", 简介="fnm（Fast Node Manager）", 分类="开发", repo="Schniz/fnm", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["ninja-linux.zip"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="ninja-linux.zip")),
    ("darwin", dict(installer_markers=["ninja-mac.zip"], href_exclude_substrings=["win", "linux"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="ninja-mac.zip")),
):
    _entry(plat, "12-开发.json", id="ninja", 简介="Ninja（构建系统）", 分类="开发", repo="ninja-build/ninja", **spec)
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["hugo_extended_", "linux-amd64"],
                   href_exclude_substrings=["windows", "darwin", "arm"], installer_extensions=[".zip"],
                   download_names=["hugo_extended_{ver}_linux-amd64.zip"], save_name="hugo_extended_{ver}_linux-amd64.zip")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["hugo_extended_", "darwin-universal"],
                    href_exclude_substrings=["windows", "linux", "arm"], installer_extensions=[".zip"],
                    download_names=["hugo_extended_{ver}_darwin-universal.zip"],
                    save_name="hugo_extended_{ver}_darwin-universal.zip")),
):
    _entry(plat, "12-开发.json", id="hugo_extended", 简介="Hugo Extended（静态站点）", 分类="开发",
           repo="gohugoio/hugo", **spec)
_cli_zip("astgrep", "12-开发.json", "开发", "ast-grep/ast-grep", "ast-grep（AST 代码搜索）", "ast-grep-")
for plat, spec in (
    ("linux", dict(installer_markers=["dprint-x86_64-unknown-linux-gnu.zip"], href_exclude_substrings=["windows", "apple"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="dprint-linux-x64.zip")),
    ("darwin", dict(installer_markers=["dprint-aarch64-apple-darwin.zip"], href_exclude_substrings=["windows", "linux-gnu"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="dprint-darwin-arm64.zip")),
):
    _entry(plat, "12-开发.json", id="dprint", 简介="dprint（代码格式化）", 分类="开发", repo="dprint/dprint", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["hurl-", "x86_64-unknown-linux-gnu"], href_exclude_substrings=["windows", "apple"],
                   use_download_filename=True, save_name="hurl-linux-x64")),
    ("darwin", dict(installer_markers=["hurl-", "aarch64-apple-darwin"], href_exclude_substrings=["windows", "linux-gnu"],
                    use_download_filename=True, save_name="hurl-darwin-arm64")),
):
    _entry(plat, "12-开发.json", id="hurl", 简介="Hurl（HTTP 测试 CLI）", 分类="开发", repo="Orange-OpenSource/hurl", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["netron-", "Linux-x64.zip"], href_exclude_substrings=["Windows", "Darwin"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="netron-Linux-x64.zip")),
    ("darwin", dict(installer_markers=["netron-", "Darwin-x64.zip"], href_exclude_substrings=["Windows", "Linux"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="netron-Darwin-x64.zip")),
):
    _entry(plat, "12-开发.json", id="netron", 简介="Netron（模型可视化）", 分类="开发", repo="lutzroeder/netron", **spec)

# --- 24 云原生 ---
_cli_zip("terraform", "24-云原生.json", "云原生", "hashicorp/terraform", "Terraform", "terraform_")
_cli_zip("packer", "24-云原生.json", "云原生", "hashicorp/packer", "Packer", "packer_")
_cli_zip("nomad", "24-云原生.json", "云原生", "hashicorp/nomad", "Nomad", "nomad_")
for plat, spec in (
    ("linux", dict(installer_markers=["minikube-linux-amd64"], href_exclude_substrings=["windows", "darwin", "arm"],
                   use_download_filename=True, save_name="minikube-linux-amd64")),
    ("darwin", dict(installer_markers=["minikube-darwin-amd64"], href_exclude_substrings=["windows", "linux", "arm"],
                    use_download_filename=True, save_name="minikube-darwin-amd64")),
):
    _entry(plat, "24-云原生.json", id="minikube", 简介="minikube（本地 K8s）", 分类="云原生",
           repo="kubernetes/minikube", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["kind-linux-amd64"], href_exclude_substrings=["windows", "darwin", ".sha256"],
                   use_download_filename=True, save_name="kind-linux-amd64")),
    ("darwin", dict(installer_markers=["kind-darwin-amd64"], href_exclude_substrings=["windows", "linux", ".sha256"],
                    use_download_filename=True, save_name="kind-darwin-amd64")),
):
    _entry(plat, "24-云原生.json", id="kind", 简介="kind（K8s in Docker）", 分类="云原生",
           repo="kubernetes-sigs/kind", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["devspace-linux-amd64"], href_exclude_substrings=["windows", "darwin", "arm"],
                   use_download_filename=True, save_name="devspace-linux-amd64")),
    ("darwin", dict(installer_markers=["devspace-darwin-amd64"], href_exclude_substrings=["windows", "linux", "arm"],
                    use_download_filename=True, save_name="devspace-darwin-amd64")),
):
    _entry(plat, "24-云原生.json", id="devspace", 简介="DevSpace（K8s 开发工具）", 分类="云原生",
           repo="devspace-sh/devspace", **spec)

# --- 26 编辑器 ---
for plat, spec in (
    ("linux", dict(installer_markers=["helix-", "x86_64-linux.tar.xz"], href_exclude_substrings=["windows", "macos", "aarch64"],
                   installer_extensions=[".xz"], use_download_filename=True, save_name="helix-linux-x64.tar.xz")),
    ("darwin", dict(installer_markers=["helix-", "aarch64-macos.tar.xz"], href_exclude_substrings=["windows", "linux", "x86_64"],
                    installer_extensions=[".xz"], use_download_filename=True, save_name="helix-macos-arm64.tar.xz")),
):
    _entry(plat, "26-编辑器.json", id="helix", 简介="Helix（modal 编辑器）", 分类="编辑器",
           repo="helix-editor/helix", **spec)

# --- 10 安全 ---
_cli_zip("grype", "10-安全.json", "安全", "anchore/grype", "Grype（镜像漏洞扫描）", "grype_")
_cli_zip("syft", "10-安全.json", "安全", "anchore/syft", "Syft（SBOM）", "syft_")
_cli_zip("nuclei", "10-安全.json", "安全", "projectdiscovery/nuclei", "Nuclei（漏洞模板扫描）", "nuclei_")
for plat, spec in (
    ("linux", dict(installer_markers=["cosign-linux-amd64"], href_exclude_substrings=["windows", "darwin", "arm"],
                   use_download_filename=True, save_name="cosign-linux-amd64")),
    ("darwin", dict(installer_markers=["cosign-darwin-amd64"], href_exclude_substrings=["windows", "linux", "arm"],
                    use_download_filename=True, save_name="cosign-darwin-amd64")),
):
    _entry(plat, "10-安全.json", id="cosign", 简介="cosign（容器签名）", 分类="安全", repo="sigstore/cosign", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["amass_Linux_amd64.zip"], href_exclude_substrings=["windows", "darwin", "checksums"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="amass-linux-amd64.zip")),
    ("darwin", dict(installer_markers=["amass_Darwin_amd64.zip"], href_exclude_substrings=["windows", "linux", "checksums"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="amass-darwin-amd64.zip")),
):
    _entry(plat, "10-安全.json", id="amass", 简介="OWASP Amass（子域枚举）", 分类="安全",
           repo="owasp-amass/amass", **spec)

# --- 23 数据库 ---
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["cockroach-v", ".linux-amd64"],
                   href_exclude_substrings=["windows", "darwin", "src"], installer_extensions=[".tgz", ".tar.gz", ".zip"],
                   use_download_filename=True, save_name="cockroach-linux-amd64.tgz")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["cockroach-v", ".darwin"],
                    href_exclude_substrings=["windows", "linux", "src"], use_download_filename=True,
                    save_name="cockroach-darwin.tgz")),
):
    _entry(plat, "23-数据库.json", id="cockroach", 简介="CockroachDB（Linux/macOS 二进制）", 分类="数据库",
           repo="cockroachdb/cockroach", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["dolt-linux-amd64.zip"], href_exclude_substrings=["windows", "darwin", "arm"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="dolt-linux-amd64.zip")),
    ("darwin", dict(installer_markers=["dolt-darwin-amd64.zip"], href_exclude_substrings=["windows", "linux", "arm"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="dolt-darwin-amd64.zip")),
):
    _entry(plat, "23-数据库.json", id="dolt", 简介="Dolt（Git 语义数据库）", 分类="数据库", repo="dolthub/dolt", **spec)
_cli_zip("sqlc", "23-数据库.json", "数据库", "sqlc-dev/sqlc", "sqlc", "sqlc_")
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["usql-", "linux-amd64.zip"],
                   href_exclude_substrings=["windows", "darwin", "arm"], installer_extensions=[".zip"],
                   download_names=["usql-{ver}-linux-amd64.zip"], save_name="usql-{ver}-linux-amd64.zip")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["usql-", "darwin-amd64.zip"],
                    href_exclude_substrings=["windows", "linux", "arm"], installer_extensions=[".zip"],
                    download_names=["usql-{ver}-darwin-amd64.zip"], save_name="usql-{ver}-darwin-amd64.zip")),
):
    _entry(plat, "23-数据库.json", id="usql", 简介="usql（通用 SQL CLI）", 分类="数据库", repo="xo/usql", **spec)

# --- 04 办公 ---
for plat, spec in (
    ("linux", dict(installer_markers=["typst-x86_64-unknown-linux-musl"], href_exclude_substrings=["windows", "apple"],
                   installer_extensions=[".tar.xz", ".zip"], use_download_filename=True, save_name="typst-linux-x64")),
    ("darwin", dict(installer_markers=["typst-aarch64-apple-darwin"], href_exclude_substrings=["windows", "linux", "x86_64"],
                    use_download_filename=True, save_name="typst-darwin-arm64")),
):
    _entry(plat, "04-办公.json", id="typst", 简介="Typst（排版系统）", 分类="办公", repo="typst/typst", **spec)
_entry("linux", "04-办公.json", id="pdfarranger", 简介="PDF Arranger（PDF 合并/拆分，Linux）", 分类="办公",
       repo="pdfarranger/pdfarranger",
       installer_markers=["pdfarranger", "fedora"], href_exclude_substrings=["windows", "mac"],
       installer_extensions=[".rpm", ".deb"], use_download_filename=True, save_name="pdfarranger-linux.rpm")

# --- 15 笔记 ---
for plat, spec in (
    ("linux", dict(installer_markers_match_all=True, installer_markers=["siyuan-", "linux-amd64"],
                   href_exclude_substrings=["win", "mac", "apk", "SHA256"], use_download_filename=True,
                   save_name="siyuan-linux-amd64")),
    ("darwin", dict(installer_markers_match_all=True, installer_markers=["siyuan-", "mac.dmg"],
                    href_exclude_substrings=["win", "linux", "apk"], installer_extensions=[".dmg"],
                    use_download_filename=True, save_name="siyuan-mac.dmg")),
):
    _entry(plat, "15-笔记.json", id="siyuan", 简介="思源笔记", 分类="笔记", repo="siyuan-note/siyuan", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["xournalpp-", "Debian-x86_64.deb"], href_exclude_substrings=["Windows", "macOS"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="xournalpp-linux.deb")),
    ("darwin", dict(installer_markers=["xournalpp-", "macOS.dmg"], href_exclude_substrings=["Windows", "Debian", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="xournalpp-macos.dmg")),
):
    _entry(plat, "15-笔记.json", id="xournalpp", 简介="Xournal++（手写/PDF 标注）", 分类="笔记",
           repo="xournalpp/xournalpp", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Yank-Note-linux-x64-", ".deb"], href_exclude_substrings=["win", "mac", "blockmap"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Yank-Note-linux.deb")),
    ("darwin", dict(installer_markers=["Yank-Note-mac-x64-", ".dmg"], href_exclude_substrings=["win", "linux", "blockmap"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Yank-Note-mac.dmg")),
):
    _entry(plat, "15-笔记.json", id="yanknote", 简介="Yank Note（Markdown 笔记）", 分类="笔记", repo="purocean/yn", **spec)

# --- 08 多媒体 ---
for plat, spec in (
    ("linux", dict(installer_markers=["lmms-", "Linux-x86_64.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="lmms.AppImage")),
    ("darwin", dict(installer_markers=["lmms-", ".dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="lmms.dmg")),
):
    _entry(plat, "08-多媒体.json", id="lmms", 简介="LMMS（数字音频工作站）", 分类="多媒体", repo="LMMS/lmms", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["MediaInfo_GUI_", "Ubuntu_amd64.deb"], href_exclude_substrings=["Windows", "Mac"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="MediaInfo_GUI.deb")),
    ("darwin", dict(installer_markers=["MediaInfo_GUI_", "_Mac.dmg"], href_exclude_substrings=["Windows", "Ubuntu", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="MediaInfo_GUI.dmg")),
):
    _entry(plat, "08-多媒体.json", id="mediainfo", 简介="MediaInfo（媒体元数据）", 分类="多媒体",
           repo="MediaArea/MediaInfo", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["spotube-", "linux-x86_64.deb"], href_exclude_substrings=["windows", "mac", "arm"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="spotube-linux.deb")),
    ("darwin", dict(installer_markers=["spotube-", "macos-universal.dmg"], href_exclude_substrings=["windows", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="spotube-macos.dmg")),
):
    _entry(plat, "08-多媒体.json", id="spotube", 简介="Spotube（Spotify 客户端）", 分类="多媒体",
           repo="KRTirtho/spotube", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["avidemux_", "Qt6AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="avidemux.AppImage")),
    ("darwin", dict(installer_markers=["avidemux_", "Qt6_64.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="avidemux.dmg")),
):
    _entry(plat, "08-多媒体.json", id="avidemux", 简介="Avidemux（视频编辑）", 分类="多媒体", repo="meonstal/Avidemux", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["SubtitleEdit-", "Linux.zip"], href_exclude_substrings=["Windows", "Mac"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="SubtitleEdit-Linux.zip")),
    ("darwin", dict(installer_markers=["SubtitleEdit-", "Mac.zip"], href_exclude_substrings=["Windows", "Linux"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="SubtitleEdit-Mac.zip")),
):
    _entry(plat, "08-多媒体.json", id="subtitleedit", 简介="Subtitle Edit（字幕编辑）", 分类="多媒体",
           repo="SubtitleEdit/subtitleedit", **spec)

# --- 14 游戏 ---
for plat, spec in (
    ("linux", dict(installer_markers=["scummvm-", "Linux-x86_64.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="scummvm.AppImage")),
    ("darwin", dict(installer_markers=["scummvm-", "macosx.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="scummvm.dmg")),
):
    _entry(plat, "14-游戏.json", id="scummvm", 简介="ScummVM（经典游戏引擎）", 分类="游戏", repo="scummvm/scummvm", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Sunshine-", "ubuntu-22.04-amd64.deb"], href_exclude_substrings=["windows", "mac", "appimage"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="sunshine-linux.deb")),
    ("darwin", dict(installer_markers=["Sunshine-", "macos.dmg"], href_exclude_substrings=["windows", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="sunshine-macos.dmg")),
):
    _entry(plat, "14-游戏.json", id="sunshine", 简介="Sunshine（Moonlight 串流服务端）", 分类="游戏",
           repo="LizardByte/Sunshine", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["OpenMW-", "linux"], href_exclude_substrings=["win", "mac"], use_download_filename=True,
                   save_name="OpenMW-linux.tar.gz")),
    ("darwin", dict(installer_markers=["OpenMW-", "osx"], href_exclude_substrings=["win", "linux"], use_download_filename=True,
                    save_name="OpenMW-macos.dmg")),
):
    _entry(plat, "14-游戏.json", id="openmw", 简介="OpenMW（上古卷轴 III 引擎）", 分类="游戏", repo="OpenMW/openmw", **spec)
_entry("linux", "14-游戏.json", id="0ad", 简介="0 A.D.（即时战略，Linux deb）", 分类="游戏", repo="0ad/0ad",
       installer_markers=["0ad_", "amd64.deb"], href_exclude_substrings=["win", "mac"], installer_extensions=[".deb"],
       use_download_filename=True, save_name="0ad-linux.deb")
_entry("darwin", "14-游戏.json", id="0ad", 简介="0 A.D.（macOS dmg）", 分类="游戏", repo="0ad/0ad",
       installer_markers=["0ad-", "osx.dmg"], href_exclude_substrings=["win", "linux"], installer_extensions=[".dmg"],
       use_download_filename=True, save_name="0ad-macos.dmg")
_entry("linux", "14-游戏.json", id="rpcs3", 简介="RPCS3（PS3 模拟器 AppImage）", 分类="游戏", repo="RPCS3/rpcs3",
       installer_markers=["rpcs3-v", "Linux64.AppImage"], href_exclude_substrings=["win", "mac"],
       installer_extensions=[".AppImage"], use_download_filename=True, save_name="rpcs3.AppImage")
for plat, spec in (
    ("linux", dict(installer_markers=["dosbox-staging-", "linux"], href_exclude_substrings=["win", "mac"], use_download_filename=True,
                   save_name="dosbox-staging-linux.tar.gz")),
    ("darwin", dict(installer_markers=["dosbox-staging-", "macos"], href_exclude_substrings=["win", "linux"], use_download_filename=True,
                    save_name="dosbox-staging-macos.dmg")),
):
    _entry(plat, "14-游戏.json", id="dosbox_staging", 简介="DOSBox Staging", 分类="游戏", repo="dosbox-staging/dosbox-staging", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Moonlight-", "x64.AppImage"], href_exclude_substrings=["win", "mac"], installer_extensions=[".AppImage"],
                   use_download_filename=True, save_name="moonlight.AppImage")),
    ("darwin", dict(installer_markers=["Moonlight-", "macos.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="moonlight.dmg")),
):
    _entry(plat, "14-游戏.json", id="moonlight_qt", 简介="Moonlight（串流客户端）", 分类="游戏", repo="moonlight-stream/moonlight-qt", **spec)

# --- 16 系统 ---
for plat, spec in (
    ("linux", dict(installer_markers=["gdu-linux-amd64"], href_exclude_substrings=["windows", "darwin", "arm"],
                   use_download_filename=True, save_name="gdu-linux-amd64")),
    ("darwin", dict(installer_markers=["gdu-darwin-amd64"], href_exclude_substrings=["windows", "linux", "arm"],
                    use_download_filename=True, save_name="gdu-darwin-amd64")),
):
    _entry(plat, "16-系统.json", id="gdu", 简介="gdu（磁盘用量分析）", 分类="系统", repo="dundee/gdu", **spec)
_entry("linux", "16-系统.json", id="ventoy", 简介="Ventoy（多系统 USB 启动，Linux 包）", 分类="系统", repo="ventoy/Ventoy",
       installer_markers_match_all=True, installer_markers=["ventoy-", "-linux.tar.gz"],
       href_exclude_substrings=["windows"], installer_extensions=[".tar.gz"],
       download_names=["ventoy-{ver}-linux.tar.gz"], save_name="ventoy-{ver}-linux.tar.gz")

# --- 18 网络 ---
for plat, spec in (
    ("linux", dict(installer_markers=["Nextcloud-", "x86_64.AppImage"], href_exclude_substrings=["win", "mac", "arm"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="Nextcloud.AppImage")),
    ("darwin", dict(installer_markers=["Nextcloud-", "macos.pkg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".pkg"], use_download_filename=True, save_name="Nextcloud.pkg")),
):
    _entry(plat, "18-网络.json", id="nextcloud_desktop", 简介="Nextcloud 桌面客户端", 分类="网络",
           repo="nextcloud/desktop", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["netbird-ui-linux_", "linux_amd64.tar.gz"], href_exclude_substrings=["windows", "darwin"],
                   installer_extensions=[".tar.gz"], use_download_filename=True, save_name="netbird-ui-linux.tar.gz")),
    ("darwin", dict(installer_markers=["netbird-ui-darwin_", "darwin_amd64.tar.gz"], href_exclude_substrings=["windows", "linux"],
                    installer_extensions=[".tar.gz"], use_download_filename=True, save_name="netbird-ui-darwin.tar.gz")),
):
    _entry(plat, "18-网络.json", id="netbird", 简介="NetBird（WireGuard 组网）", 分类="网络", repo="netbirdio/netbird", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["xh-v", "x86_64-unknown-linux-musl"], href_exclude_substrings=["windows", "apple"],
                   use_download_filename=True, save_name="xh-linux-musl")),
    ("darwin", dict(installer_markers=["xh-v", "aarch64-apple-darwin"], href_exclude_substrings=["windows", "linux-gnu"],
                    use_download_filename=True, save_name="xh-darwin-arm64")),
):
    _entry(plat, "18-网络.json", id="xh", 简介="xh（彩色 HTTP 客户端）", 分类="网络", repo="ducaale/xh", **spec)

# --- 30 代理 ---
for plat, spec in (
    ("linux", dict(installer_markers=["mihomo-linux-amd64-v", ".zip"], href_exclude_substrings=["darwin", "windows", "arm"],
                   installer_extensions=[".zip"], use_download_filename=True, save_name="mihomo-linux-amd64.zip")),
    ("darwin", dict(installer_markers=["mihomo-darwin-amd64-v", ".zip"], href_exclude_substrings=["linux", "windows", "arm"],
                    installer_extensions=[".zip"], use_download_filename=True, save_name="mihomo-darwin-amd64.zip")),
):
    _entry(plat, "30-代理与隧道.json", id="mihomo", 简介="mihomo（Clash Meta 内核）", 分类="代理与隧道",
           repo="MetaCubeX/mihomo", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["sing-box-", "linux-amd64"], href_exclude_substrings=["windows", "darwin", "arm"],
                   use_download_filename=True, save_name="sing-box-linux-amd64")),
    ("darwin", dict(installer_markers=["sing-box-", "darwin-amd64"], href_exclude_substrings=["windows", "linux", "arm"],
                    use_download_filename=True, save_name="sing-box-darwin-amd64")),
):
    _entry(plat, "30-代理与隧道.json", id="sing_box", 简介="sing-box（通用代理平台）", 分类="代理与隧道",
           repo="SagerNet/sing-box", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Clash.Verge_", "amd64.deb"], href_exclude_substrings=["windows", "dmg", "arm64", "AppImage"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Clash.Verge.deb")),
    ("darwin", dict(installer_markers=["Clash.Verge_", "aarch64.dmg"], href_exclude_substrings=["windows", "deb", "x64"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Clash.Verge.dmg")),
):
    _entry(plat, "30-代理与隧道.json", id="clash_verge_rev", 简介="Clash Verge Rev（Clash 客户端）", 分类="代理与隧道",
           repo="clash-verge-rev/clash-verge-rev", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["FlClash-", "linux-amd64.deb"], href_exclude_substrings=["windows", "mac", "rpm"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="FlClash-linux.deb")),
    ("darwin", dict(installer_markers=["FlClash-", "macos-arm64.dmg"], href_exclude_substrings=["windows", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="FlClash-macos.dmg")),
):
    _entry(plat, "30-代理与隧道.json", id="flclash", 简介="FlClash（Flutter Clash 客户端）", 分类="代理与隧道",
           repo="chen08209/FlClash", **spec)

# --- 28 加密货币 ---
for plat, spec in (
    ("linux", dict(installer_markers=["Bisq-64bit-", ".deb"], href_exclude_substrings=["win", "mac", "rpm"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Bisq-linux.deb")),
    ("darwin", dict(installer_markers=["Bisq-", ".dmg"], href_exclude_substrings=["win", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Bisq.dmg")),
):
    _entry(plat, "28-加密货币.json", id="bisq", 简介="Bisq（去中心化交易所）", 分类="加密货币", repo="bisq-network/bisq", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Sparrow-", "x86_64.deb"], href_exclude_substrings=["win", "mac", "rpm"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Sparrow-linux.deb")),
    ("darwin", dict(installer_markers=["Sparrow-", "x86_64.dmg"], href_exclude_substrings=["win", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Sparrow.dmg")),
):
    _entry(plat, "28-加密货币.json", id="sparrow_wallet", 简介="Sparrow Wallet（Bitcoin）", 分类="加密货币",
           repo="sparrowwallet/sparrow", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Wasabi-", "linux-x64.deb"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".deb"], use_download_filename=True, save_name="Wasabi-linux.deb")),
    ("darwin", dict(installer_markers=["Wasabi-", "macOS.dmg"], href_exclude_substrings=["win", "linux", "deb"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Wasabi.dmg")),
):
    _entry(plat, "28-加密货币.json", id="wasabi_wallet", 简介="Wasabi Wallet（Bitcoin 隐私）", 分类="加密货币",
           repo="zkSNACKs/WalletWasabi", **spec)

# --- 02 下载 ---
_entry("linux", "02-下载.json", id="gallery_dl", 简介="gallery-dl（图库/B站等批量下载 CLI）", 分类="下载",
       repo="mikf/gallery-dl", installer_markers=["gallery-dl.bin"], href_exclude_substrings=["win", "mac"],
       use_download_filename=True, save_name="gallery-dl.bin")
_entry("darwin", "02-下载.json", id="gallery_dl", 简介="gallery-dl（macOS 二进制）", 分类="下载", repo="mikf/gallery-dl",
       installer_markers=["gallery-dl"], href_exclude_substrings=["win", "linux", ".bin"], use_download_filename=True,
       save_name="gallery-dl")

# --- 20 网络与通讯 ---
for plat, spec in (
    ("linux", dict(installer_markers=["thunderbird-", ".tar.xz"], href_exclude_substrings=["win", "mac"], installer_extensions=[".tar.xz"],
                   use_download_filename=True, save_name="thunderbird-linux.tar.xz")),
    ("darwin", dict(installer_markers=["Thunderbird", ".dmg"], href_exclude_substrings=["win", "linux", "tar.xz"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Thunderbird.dmg")),
):
    _entry(plat, "20-网络与通讯.json", id="thunderbird", 简介="Thunderbird（邮件客户端）", 分类="网络与通讯",
           repo="thunderbird/thunderbird", **spec)

# --- 21 远程 ---
for plat, spec in (
    ("linux", dict(installer_markers=["deskreen-ce-", "Linux.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="deskreen.AppImage")),
    ("darwin", dict(installer_markers=["deskreen-ce-", "macOS.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="deskreen.dmg")),
):
    _entry(plat, "21-远程与协作.json", id="deskreen", 简介="Deskreen（屏幕共享）", 分类="远程与协作", repo="pavlobu/deskreen", **spec)

# --- 17 终端 ---
for plat, spec in (
    ("linux", dict(installer_markers=["rio-", "linux"], href_exclude_substrings=["windows", "darwin", "msi"],
                   use_download_filename=True, save_name="rio-linux")),
    ("darwin", dict(installer_markers=["rio-installer-aarch64", ".dmg"], href_exclude_substrings=["windows", "linux", "msi"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="rio-macos.dmg")),
):
    _entry(plat, "17-终端.json", id="rio", 简介="Rio（GPU 终端）", 分类="终端", repo="raphamorim/rio", **spec)

# --- 05 办公与设计 ---
for plat, spec in (
    ("linux", dict(installer_markers=["rnote-", "linux.flatpak"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".flatpak"], use_download_filename=True, save_name="rnote.flatpak")),
    ("darwin", dict(installer_markers=["rnote-", "macos.dmg"], href_exclude_substrings=["win", "linux", "flatpak"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="rnote.dmg")),
):
    _entry(plat, "05-办公与设计.json", id="rnote", 简介="Rnote（手写笔记）", 分类="办公与设计", repo="flxzt/rnote", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["Stirling-PDF-", "linux-amd64.jar"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".jar"], use_download_filename=True, save_name="Stirling-PDF.jar")),
    ("darwin", dict(installer_markers=["Stirling-PDF-", "macos.dmg"], href_exclude_substrings=["win", "linux", "jar"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Stirling-PDF.dmg")),
):
    _entry(plat, "05-办公与设计.json", id="stirling_pdf", 简介="Stirling-PDF（PDF 工具集）", 分类="办公与设计",
           repo="Stirling-Tools/Stirling-PDF", **spec)

# --- 27 金融 ---
for plat, spec in (
    ("linux", dict(installer_markers=["Actual-", "linux-x64.AppImage"], href_exclude_substrings=["win", "mac"],
                   installer_extensions=[".AppImage"], use_download_filename=True, save_name="Actual.AppImage")),
    ("darwin", dict(installer_markers=["Actual-", "macos.dmg"], href_exclude_substrings=["win", "linux", "AppImage"],
                    installer_extensions=[".dmg"], use_download_filename=True, save_name="Actual.dmg")),
):
    _entry(plat, "27-金融与股票.json", id="actual_budget", 简介="Actual Budget（本地记账）", 分类="金融与股票",
           repo="actualbudget/actual", **spec)
for plat, spec in (
    ("linux", dict(installer_markers=["OpenBB", "linux"], href_exclude_substrings=["win", "mac"], use_download_filename=True,
                   save_name="OpenBB-linux")),
    ("darwin", dict(installer_markers=["OpenBB", "macos"], href_exclude_substrings=["win", "linux"], use_download_filename=True,
                    save_name="OpenBB-macos")),
):
    _entry(plat, "27-金融与股票.json", id="openbb_desktop", 简介="OpenBB Desktop（金融终端）", 分类="金融与股票",
           repo="OpenBB-finance/OpenBB", **spec)

# --- 13 效率 pixpin linux placeholder ---
_entry("linux", "13-效率.json", id="pixpin", 简介="PixPin（官方暂无 Linux 版；占位勿启用）", 分类="效率",
       repo="pixpin-cn/desktop", releases_url="https://pixpin.cn/download/", prefer_api_assets=False, url_hint="pixpin")


def merge_all(dry_run: bool = False) -> tuple[int, int]:
    added = skipped = 0
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            print("SKIP missing", path)
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            continue
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
    a, s = merge_all(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: added {a}, skipped duplicate {s}")


if __name__ == "__main__":
    main()
