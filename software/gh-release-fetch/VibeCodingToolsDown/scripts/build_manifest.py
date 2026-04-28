#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
聚合各官网 / 官方 API 的下载直链，生成 VibeCodingToolsDown/dist/vibecoding/manifest.json。
供 GitHub Pages 发布；auto_update.py 通过 resolve_via=github_pages_manifest 读取。

仅依赖 requests、beautifulsoup4（与仓库 requirements.txt 一致）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import requests

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html;q=0.9,*/*;q=0.8",
}
GH_ACCEPT = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}


def _github_api_headers() -> dict[str, str]:
    h = dict(GH_ACCEPT)
    tok = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def _session():
    s = requests.Session()
    s.headers.update(UA)
    return s


def _item(
    item_id: str,
    version: str,
    downloads: dict[str, dict[str, str] | None],
    notes: str | None = None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "version": version.lstrip("v"),
        "version_tag": version if version.startswith("v") else f"v{version}",
        "downloads": downloads,
        "notes": notes,
    }


def fetch_cursor(s: requests.Session) -> dict[str, Any]:
    r = s.get(
        "https://api.github.com/repos/accesstechnology-mike/cursor-downloads/releases/latest",
        headers=_github_api_headers(),
        timeout=40,
    )
    r.raise_for_status()
    j = r.json()
    tag = (j.get("tag_name") or "").strip() or "unknown"
    ver = tag.lstrip("v")
    body = j.get("body") or ""
    urls = re.findall(r"\((https://downloads\.cursor\.com[^)]+)\)", body)
    win = next((u for u in urls if "UserSetup-x64" in u and u.lower().endswith(".exe")), None)
    mac_u = next((u for u in urls if "darwin-universal" in u and u.lower().endswith(".zip")), None)
    mac_a = next((u for u in urls if "darwin-arm64" in u and u.lower().endswith(".zip")), None)
    mac_i = next((u for u in urls if "darwin-x64" in u and u.lower().endswith(".zip")), None)
    lin = next(
        (
            u
            for u in urls
            if "linux" in u and "x86_64" in u and u.lower().endswith(".appimage") and ".zsync" not in u.lower()
        ),
        None,
    )
    return _item(
        "cursor",
        ver,
        {
            "windows": {"url": win, "filename": os.path.basename(win) if win else ""} if win else None,
            "darwin": {"url": mac_u or mac_a, "filename": os.path.basename(mac_u or mac_a or "")}
            if (mac_u or mac_a)
            else None,
            "linux": {"url": lin, "filename": os.path.basename(lin) if lin else ""} if lin else None,
        },
        notes="索引自 accesstechnology-mike/cursor-downloads Release 正文中的官方 CDN 链。",
    )


def _vscode_redirect(s: requests.Session, path_suffix: str) -> str:
    """使用微软官方 update 通道解析最终下载 URL（GET + stream，避免部分网络/代理对 HEAD 不跟随）。"""
    u = "https://update.code.visualstudio.com/" + path_suffix.lstrip("/")
    with s.get(u, allow_redirects=True, timeout=40, stream=True) as r:
        r.raise_for_status()
        return r.url


def fetch_vscode(s: requests.Session) -> dict[str, Any]:
    r = s.get(
        "https://api.github.com/repos/microsoft/vscode/releases/latest",
        headers=_github_api_headers(),
        timeout=40,
    )
    r.raise_for_status()
    j = r.json()
    tag = (j.get("tag_name") or "").strip()
    ver = tag.lstrip("v")
    win_u = _vscode_redirect(s, "latest/win32-x64/stable")
    mac_u = _vscode_redirect(s, "latest/darwin-arm64/stable")
    lin_u = _vscode_redirect(s, "latest/linux-x64/stable")
    downloads = {
        "windows": {"url": win_u, "filename": os.path.basename(win_u.split("?", 1)[0])},
        "darwin": {"url": mac_u, "filename": os.path.basename(mac_u.split("?", 1)[0])},
        "linux": {"url": lin_u, "filename": os.path.basename(lin_u.split("?", 1)[0])},
    }
    return _item(
        "vscode",
        ver,
        downloads,
        notes="版本 tag 来自 GitHub API；安装包 URL 来自 update.code.visualstudio.com GET 重定向链末端（微软官方 CDN）。",
    )


def _collect_trae_install_urls(s: requests.Session, page_urls: tuple[str, ...]) -> list[str]:
    """从官网 HTML 中提取 Trae 稳定包直链（历史页为 lf-trae.toscdn.com；新 CDN 为 lf-cdn.trae.*）。"""
    pat = re.compile(
        r"https://lf-(?:trae\.toscdn\.com|cdn\.trae\.(?:ai|com\.cn))[^\s\"'<>)]*?\.(?:exe|dmg|zip|AppImage)\b",
        re.I,
    )
    seen: set[str] = set()
    for page in page_urls:
        try:
            r = s.get(page, timeout=40)
            r.raise_for_status()
            for u in pat.findall(r.text):
                seen.add(u.split("?", 1)[0])
        except Exception:
            continue
    return sorted(seen)


def fetch_vscodium(s: requests.Session) -> dict[str, Any]:
    r = s.get(
        "https://api.github.com/repos/VSCodium/vscodium/releases/latest",
        headers=_github_api_headers(),
        timeout=40,
    )
    r.raise_for_status()
    j = r.json()
    tag = (j.get("tag_name") or "").strip()
    ver = tag.lstrip("v")
    assets = {a.get("name", ""): a.get("browser_download_url", "") for a in (j.get("assets") or [])}

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: n.startswith("VSCodiumUserSetup-x64-") and n.endswith(".exe"))
    mac = pick(lambda n: n.startswith("VSCodium-darwin-arm64-") and n.endswith(".zip"))
    lin = pick(lambda n: n.startswith("VSCodium-linux-x64-") and n.endswith(".tar.gz"))
    return _item("vscodium", ver, {"windows": win, "darwin": mac, "linux": lin}, notes="GitHub API latest assets。")


def _trae_item_from_urls(item_id: str, urls: list[str], notes: str) -> dict[str, Any]:
    if not urls:
        raise RuntimeError("未解析到 Trae 安装包直链")
    # 多页合并时各平台 stable 段可能不一致，取 URL 中出现的最大稳定段，避免 win/mac 错配旧包。
    segs = [m.group(1) for u in urls for m in [re.search(r"/releases/stable/([^/]+)/", u)] if m]

    def _seg_key(seg: str) -> tuple[int, ...]:
        parts = []
        for p in seg.split("."):
            if p.isdigit():
                parts.append(int(p))
            else:
                parts.append(0)
        return tuple(parts)

    ver = max(segs, key=_seg_key) if segs else "unknown"

    def pick(sub: str):
        cand = [u for u in urls if sub in u and f"/releases/stable/{ver}/" in u]
        pool = cand if cand else [u for u in urls if sub in u]
        for u in pool:
            return {"url": u, "filename": os.path.basename(u.split("?", 1)[0])}
        return None

    win = pick("Trae-Setup-x64") or pick("win32")
    mac = pick("darwin-universal") or pick("darwin-arm64") or pick("darwin-x64")
    lin = pick("linux-x64") or pick("linux")
    return _item(
        item_id,
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes=notes,
    )


def _trae_icube_pick_region(entries: list[Any], region_order: tuple[str, ...]) -> dict[str, Any] | None:
    if not isinstance(entries, list):
        return None
    by_reg: dict[str, dict[str, Any]] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        reg = (e.get("region") or "").strip()
        if reg:
            by_reg[reg] = e
    for reg in region_order:
        if reg in by_reg:
            return by_reg[reg]
    for e in entries:
        if isinstance(e, dict):
            return e
    return None


def _fetch_trae_from_icube_api(
    s: requests.Session,
    *,
    item_id: str,
    api_url: str,
    region_order: tuple[str, ...],
    notes: str,
    data_key: str = "manifest",
) -> dict[str, Any] | None:
    """官方 icube native 接口：data.manifest 为 Trae IDE；data.solo 为 TRAE_SOLO（与 https://solo.trae.cn/ 对应）。"""
    try:
        r = s.get(api_url, timeout=40)
        r.raise_for_status()
        j = r.json()
    except Exception:
        return None
    if not isinstance(j, dict) or not j.get("success"):
        return None
    data = j.get("data")
    if not isinstance(data, dict):
        return None
    branch = data.get(data_key)
    if not isinstance(branch, dict):
        return None

    win_blk = branch.get("win32")
    dar_blk = branch.get("darwin")
    lin_blk = branch.get("linux")
    ver = "unknown"
    if isinstance(win_blk, dict) and (win_blk.get("version") or "").strip():
        ver = str(win_blk["version"]).strip()
    elif isinstance(dar_blk, dict) and (dar_blk.get("version") or "").strip():
        ver = str(dar_blk["version"]).strip()
    elif isinstance(lin_blk, dict) and (lin_blk.get("version") or "").strip():
        ver = str(lin_blk["version"]).strip()

    win = mac = lin = None
    if isinstance(win_blk, dict):
        ent = _trae_icube_pick_region(win_blk.get("download") or [], region_order)
        if ent:
            u = ent.get("x64") or ent.get("x86")
            if isinstance(u, str) and u.startswith("http"):
                win = {"url": u.split("?", 1)[0], "filename": os.path.basename(u.split("?", 1)[0])}
    if isinstance(dar_blk, dict):
        ent = _trae_icube_pick_region(dar_blk.get("download") or [], region_order)
        if ent:
            u = ent.get("apple") or ent.get("arm64") or ent.get("intel") or ent.get("x64")
            if isinstance(u, str) and u.startswith("http"):
                mac = {"url": u.split("?", 1)[0], "filename": os.path.basename(u.split("?", 1)[0])}
    if isinstance(lin_blk, dict):
        ent = _trae_icube_pick_region(lin_blk.get("download") or [], region_order)
        if ent:
            u = (
                ent.get("x64.tar.gz")
                or ent.get("x64.tar")
                or ent.get("amd64.tar.gz")
                or ent.get("x64.AppImage")
            )
            if isinstance(u, str) and u.startswith("http"):
                lin = {"url": u.split("?", 1)[0], "filename": os.path.basename(u.split("?", 1)[0])}

    if not win and not mac and not lin:
        return None
    return _item(item_id, ver, {"windows": win, "darwin": mac, "linux": lin}, notes=notes)


def fetch_trae(s: requests.Session) -> dict[str, Any]:
    item = _fetch_trae_from_icube_api(
        s,
        item_id="trae",
        api_url="https://api.trae.ai/icube/api/v1/native/version/trae/latest",
        region_order=("va", "sg", "usttp", "cn"),
        data_key="manifest",
        notes=(
            "优先 api.trae.ai/icube/.../trae/latest（manifest）；下载链优先 region=va，失败则 sg/usttp/cn。"
            " version 为接口返回的稳定构建号（与 URL 路径一致）；应用内「关于」若显示 3.x 等为另一口径，以本构建号为准。"
        ),
    )
    if item is not None:
        return item
    pages = (
        "https://www.trae.ai/download",
        "https://traeide.com/download",
    )
    urls = _collect_trae_install_urls(s, pages)
    return _trae_item_from_urls(
        "trae",
        urls,
        notes="API 不可用时回退：扫描下载页 HTML 中的 lf-trae / lf-cdn 直链（多源合并，按 stable 段取较新）。",
    )


def fetch_trae_cn(s: requests.Session) -> dict[str, Any]:
    item = _fetch_trae_from_icube_api(
        s,
        item_id="trae_cn",
        api_url="https://api.trae.cn/icube/api/v1/native/version/trae/latest",
        region_order=("cn", "va", "sg", "usttp"),
        data_key="manifest",
        notes=(
            "优先 api.trae.cn/icube/.../trae/latest；下载链优先 region=cn。"
            " version 为接口稳定构建号；与海外 manifest 分支可能不同步。"
        ),
    )
    if item is not None:
        return item
    pages = (
        "https://www.trae.cn/ide/download",
        "https://www.trae.ai/download",
        "https://traeide.com/download",
    )
    urls = _collect_trae_install_urls(s, pages)
    return _trae_item_from_urls(
        "trae_cn",
        urls,
        notes="API 不可用时回退：扫描 trae.cn / trae.ai / traeide 下载页 HTML 直链。",
    )


def fetch_trae_solo(s: requests.Session) -> dict[str, Any]:
    """TRAE_SOLO：与 https://solo.trae.cn/ 对应；icube 的 data.solo 当前多为 darwin dmg，Windows 安装包见官网。"""
    item = _fetch_trae_from_icube_api(
        s,
        item_id="trae_solo",
        api_url="https://api.trae.ai/icube/api/v1/native/version/trae/latest",
        region_order=("va", "sg", "usttp", "cn"),
        data_key="solo",
        notes=(
            "api.trae.ai icube latest 的 data.solo（与 TRAE SOLO 安装包一致）。"
            " 官网：https://solo.trae.cn/ 、https://www.trae.cn/solo 。"
            " 当前接口多为 macOS dmg；windows/linux 常为 null 时请从官网获取。"
        ),
    )
    if item is not None:
        return item
    return _item(
        "trae_solo",
        "0",
        {"windows": None, "darwin": None, "linux": None},
        notes="未能从 icube 解析 TRAE_SOLO；请打开 https://solo.trae.cn/ 或 https://www.trae.cn/solo 手动下载。",
    )


def fetch_antigravity(s: requests.Session) -> dict[str, Any]:
    """从 antigravity.google/download 引用 main-*.js，再在 bundle 内提取 edgedl.me.gvt1.com 直链。"""
    r = s.get("https://antigravity.google/download", timeout=40)
    r.raise_for_status()
    html = r.text
    m = re.search(r'src="(main-[A-Z0-9]+\.js)"', html)
    if not m:
        raise RuntimeError("Antigravity 下载页未找到 main-*.js")
    bundle_url = "https://antigravity.google/" + m.group(1)
    br = s.get(bundle_url, timeout=60)
    br.raise_for_status()
    body = br.text
    pat = re.compile(
        r"https://edgedl\.me\.gvt1\.com/edgedl/release2/[a-z0-9]+/antigravity/stable/"
        r"\d+\.\d+\.\d+-\d+/[^\"'\\\s<>)]+\.(?:exe|dmg|tar\.gz)\b",
        re.I,
    )
    urls = sorted(set(pat.findall(body)))
    if not urls:
        raise RuntimeError("Antigravity main bundle 中未匹配到 edgedl 安装包 URL")

    def pick(pred):
        for u in urls:
            if pred(u):
                return {"url": u, "filename": os.path.basename(u.split("?", 1)[0])}
        return None

    win = pick(lambda u: "windows-x64" in u and u.lower().endswith(".exe"))
    mac = pick(lambda u: "darwin-arm" in u and u.lower().endswith(".dmg")) or pick(
        lambda u: "darwin-x64" in u and u.lower().endswith(".dmg")
    )
    lin = pick(lambda u: "linux-x64" in u and u.lower().endswith(".tar.gz"))
    ver_m = re.search(r"/stable/(\d+\.\d+\.\d+)-\d+/", urls[0])
    ver = ver_m.group(1) if ver_m else "unknown"
    return _item(
        "antigravity",
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes=f"自 {bundle_url} 解析 Google CDN（edgedl.me.gvt1.com）。",
    )


def _gh_latest_assets(s: requests.Session, owner: str, repo: str) -> tuple[str, dict[str, str]]:
    """GitHub releases/latest：返回 tag_name 与 name→browser_download_url 映射。"""
    r = s.get(
        f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
        headers=_github_api_headers(),
        timeout=40,
    )
    r.raise_for_status()
    j = r.json()
    tag = (j.get("tag_name") or "").strip() or "unknown"
    assets = {
        (a.get("name") or ""): (a.get("browser_download_url") or "")
        for a in (j.get("assets") or [])
        if a.get("name")
    }
    return tag, assets


def fetch_restic(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "restic", "restic")
    ver = tag.lstrip("v") if tag.startswith("v") else tag

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: "windows_amd64" in n and n.endswith(".zip"))
    mac = pick(lambda n: "darwin_arm64" in n and n.endswith(".bz2")) or pick(
        lambda n: "darwin_amd64" in n and n.endswith(".bz2")
    )
    lin = pick(lambda n: "linux_amd64" in n and n.endswith(".bz2"))
    return _item(
        "restic",
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes="GitHub restic/restic latest；Windows zip；macOS 优先 arm64 .bz2 否则 amd64；Linux 为 amd64 .bz2（arm64 请用发行版或主仓库 apps 分架构项）。",
    )


def fetch_syncthing(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "syncthing", "syncthing")
    ver = tag.lstrip("v") if tag.startswith("v") else tag

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: n.startswith("syncthing-windows-amd64-") and n.endswith(".zip"))
    mac = pick(lambda n: "syncthing-macos-universal-" in n and n.endswith(".zip"))
    lin = pick(lambda n: n.startswith("syncthing-linux-amd64-") and n.endswith(".tar.gz"))
    return _item(
        "syncthing",
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes="GitHub syncthing/syncthing latest；仅核心压缩包，不含安装器。",
    )


def fetch_sqlitebrowser(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "sqlitebrowser", "sqlitebrowser")
    ver = tag.lstrip("v") if tag.startswith("v") else tag

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: "DB.Browser.for.SQLite-" in n and n.endswith("-win64.msi"))
    mac = pick(lambda n: n.startswith("DB.Browser.for.SQLite-") and n.endswith(".dmg") and "arm64" not in n)
    lin = pick(lambda n: "x86.64" in n and n.endswith(".AppImage"))
    return _item(
        "sqlitebrowser",
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes="GitHub sqlitebrowser/sqlitebrowser latest；Linux 为 x86_64 AppImage（文件名含 x86.64）。",
    )


def fetch_caesium(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "Lymphatus", "caesium-image-compressor")
    ver = tag.lstrip("v") if tag.startswith("v") else tag

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: "win-setup.exe" in n and n.endswith(".exe"))
    mac = pick(lambda n: "-macos.dmg" in n and n.endswith(".dmg"))
    return _item(
        "caesium",
        ver,
        {"windows": win, "darwin": mac, "linux": None},
        notes="GitHub Lymphatus/caesium-image-compressor latest；Linux 无 Release 通用包（见主仓库 apps/linux/11-工具 说明）。",
    )


def fetch_cc_switch(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "farion1231", "cc-switch")
    ver = tag.lstrip("v") if tag.startswith("v") else tag

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: n.startswith("CC-Switch-") and n.endswith("-Windows.msi"))
    mac = pick(lambda n: n.startswith("CC-Switch-") and n.endswith("-macOS.dmg"))
    lin = pick(lambda n: "Linux-x86_64.AppImage" in n and n.endswith(".AppImage"))
    return _item(
        "cc_switch",
        ver,
        {"windows": win, "darwin": mac, "linux": lin},
        notes="GitHub farion1231/cc-switch（CC Switch）；Windows MSI、macOS dmg、Linux x86_64 AppImage。",
    )


def fetch_aria2(s: requests.Session) -> dict[str, Any]:
    tag, assets = _gh_latest_assets(s, "aria2", "aria2")
    m = re.match(r"(?:release-)?(\d+\.\d+\.\d+)\b", tag)
    ver = m.group(1) if m else tag.replace("release-", "").lstrip("v")

    def pick(pred):
        for name, u in assets.items():
            if pred(name):
                return {"url": u, "filename": name}
        return None

    win = pick(lambda n: "win-64bit" in n and n.endswith(".zip"))
    return _item(
        "aria2",
        ver,
        {"windows": win, "darwin": None, "linux": None},
        notes="GitHub aria2/aria2 latest；仅 Windows 64 位 zip。macOS/Linux 请用 brew / 发行版包或源码编译。",
    )


def fetch_kiro(s: requests.Session) -> dict[str, Any]:
    r = s.get("https://prod.download.cli.kiro.dev/stable/latest/manifest.json", timeout=40)
    r.raise_for_status()
    j = r.json()
    ver = str(j.get("version") or "unknown")
    base_latest = "https://prod.download.cli.kiro.dev/stable/latest/"
    packages = j.get("packages") or []

    def pick_pkg(**kw):
        for p in packages:
            if not all(p.get(k) == v for k, v in kw.items()):
                continue
            rel = p.get("download") or ""
            fname = rel.split("/")[-1]
            if not fname:
                continue
            url = base_latest + quote(fname, safe="")
            return {"url": url, "filename": fname}
        return None

    return _item(
        "kiro",
        ver,
        {
            "windows": pick_pkg(
                os="windows", fileType="msi", variant="full", architecture="x86_64"
            ),
            "darwin": pick_pkg(
                os="macos", fileType="dmg", variant="full", architecture="universal"
            ),
            "linux": pick_pkg(
                os="linux", fileType="appImage", variant="full", architecture="x86_64"
            )
            or pick_pkg(os="linux", fileType="deb", variant="full", architecture="x86_64"),
        },
        notes="Kiro CLI 官方 manifest（含 Windows MSI / macOS dmg / Linux AppImage 等）。",
    )


def _qoder_alicdn_version_sort_key(v: str) -> tuple[int, ...]:
    out: list[int] = []
    for p in v.split("."):
        if p.isdigit():
            out.append(int(p))
        else:
            nums = "".join(c for c in p if c.isdigit())
            out.append(int(nums) if nums else 0)
    return tuple(out)


def _qoder_install_urls_from_chunks(s: requests.Session, html: str) -> tuple[str, list[str]]:
    """从 qoder.com 下载页 HTML 解析 alicdn 版本号并扫描 _next/static/chunks 下的 JS 直链。"""
    vers = sorted(
        set(re.findall(r"g\.alicdn\.com/Qoder/qoder-web/([\d.]+)/", html)),
        key=_qoder_alicdn_version_sort_key,
    )
    if not vers:
        return "unknown", []
    ver = vers[-1]
    base = f"https://g.alicdn.com/Qoder/qoder-web/{ver}/"
    js_paths = sorted(
        set(
            re.findall(
                rf"https://g\.alicdn\.com/Qoder/qoder-web/{re.escape(ver)}/_next/static/chunks/[^\"']+\.js",
                html,
            )
        )
    )
    if not js_paths:
        # 协议相对 URL
        rel = sorted(
            set(
                re.findall(
                    rf"//g\.alicdn\.com/Qoder/qoder-web/{re.escape(ver)}/_next/static/chunks/[^\"']+\.js",
                    html,
                )
            )
        )
        js_paths = ["https:" + u if u.startswith("//") else u for u in rel]

    inst_pat = re.compile(
        r"https://[a-zA-Z0-9./_?=&%-]{12,500}\.(?:exe|dmg|deb|rpm|AppImage)\b",
        re.I,
    )
    found: set[str] = set()
    for ju in js_paths[:45]:
        try:
            jr = s.get(ju, timeout=40)
            jr.raise_for_status()
            body = jr.text.replace("\\/", "/")
            for u in inst_pat.findall(body):
                if "${" in u or "{" in u:
                    continue
                found.add(u.split("?", 1)[0])
        except Exception:
            continue
    return ver, sorted(found)


def _pick_qoder_installers(hits: list[str]) -> tuple[str | None, str | None, str | None]:
    """优先选 Qoder IDE 包，避免误选 QoderWork 独立应用（若仅有 Work 包则回退）。"""

    def is_work(u: str) -> bool:
        x = u.lower()
        return "qoderwork" in x or "qoder-work" in x or "qoder_work" in x

    win = next((h for h in hits if h.lower().endswith(".exe") and not is_work(h)), None) or next(
        (h for h in hits if h.lower().endswith(".exe")), None
    )
    mac = next((h for h in hits if h.lower().endswith(".dmg") and not is_work(h)), None) or next(
        (h for h in hits if h.lower().endswith(".dmg")), None
    )
    lin = next((h for h in hits if h.lower().endswith((".deb", ".rpm", ".appimage"))), None)
    return win, mac, lin


def _pick_qoderwork_installers(hits: list[str]) -> tuple[str | None, str | None, str | None]:
    """仅选 QoderWork 独立桌面包（与 Qoder IDE 区分）。"""

    def is_work(u: str) -> bool:
        x = u.lower()
        return "qoderwork" in x or "qoder-work" in x or "qoder_work" in x

    win = next((h for h in hits if h.lower().endswith(".exe") and is_work(h)), None)
    mac = next((h for h in hits if h.lower().endswith(".dmg") and is_work(h)), None)
    lin = next((h for h in hits if is_work(h) and h.lower().endswith((".deb", ".rpm", ".appimage"))), None)
    return win, mac, lin


def fetch_qoder(s: requests.Session) -> dict[str, Any]:
    """新版官网为 Next.js：扫描 alicdn chunks；仍兼容旧版 download/page-*.js 分片。"""
    notes: list[str] = []
    try:
        for page in ("https://qoder.com/zh/download", "https://qoder.com/en/download"):
            r = s.get(page, timeout=40)
            r.raise_for_status()
            html = r.text
            ver, hits = _qoder_install_urls_from_chunks(s, html)
            win, mac, lin = _pick_qoder_installers(hits)
            if win or mac or lin:
                return _item(
                    "qoder",
                    ver,
                    {
                        "windows": {"url": win, "filename": os.path.basename(win.split("?", 1)[0])}
                        if win
                        else None,
                        "darwin": {"url": mac, "filename": os.path.basename(mac.split("?", 1)[0])}
                        if mac
                        else None,
                        "linux": {"url": lin, "filename": os.path.basename(lin.split("?", 1)[0])}
                        if lin
                        else None,
                    },
                    notes=f"自 {page} 的 g.alicdn.com Qoder Next chunks 解析。",
                )
            # 旧版 page 分片
            chunks = re.findall(
                r"https://g\.alicdn\.com/Qoder/qoder-web/[^\"']+/download/page-[a-z0-9]+\.js",
                html,
            ) or re.findall(
                r"https://g\.alicdn\.com/Qoder/qoder-web/[^\"']+/%5Blang%5D/download/page-[a-z0-9]+\.js",
                html,
            )
            if chunks:
                ju = chunks[0].replace("\\u002F", "/")
                jr = s.get(ju, timeout=40)
                jr.raise_for_status()
                body = jr.text.replace("\\/", "/")
                hits2 = sorted(
                    set(
                        re.findall(
                            r"https://[a-zA-Z0-9./_?=&%-]{12,400}\.(?:exe|dmg|deb|rpm|AppImage)\b",
                            body,
                            flags=re.I,
                        )
                    )
                )
                win, mac, lin = _pick_qoder_installers(hits2)
                if win or mac or lin:
                    vm = re.search(r"Qoder[-_]?(\d+\.\d+\.\d+)", body, re.I)
                    ver2 = vm.group(1) if vm else ver
                    return _item(
                        "qoder",
                        ver2,
                        {
                            "windows": {"url": win, "filename": os.path.basename(win.split("?", 1)[0])}
                            if win
                            else None,
                            "darwin": {"url": mac, "filename": os.path.basename(mac.split("?", 1)[0])}
                            if mac
                            else None,
                            "linux": {"url": lin, "filename": os.path.basename(lin.split("?", 1)[0])}
                            if lin
                            else None,
                        },
                        notes=f"自 {page} 旧版 download/page JS 解析。",
                    )
    except Exception as e:
        notes.append(str(e))
    return _item(
        "qoder",
        "0",
        {"windows": None, "darwin": None, "linux": None},
        notes="; ".join(notes) or "未能解析 Qoder 安装包，请从 https://qoder.com/download 手动下载。",
    )


def fetch_qoderwork(s: requests.Session) -> dict[str, Any]:
    """QoderWork 桌面应用：官网 https://qoder.com/zh/qoderwork ；与 Qoder IDE 分包名不同（qoder-work / QoderWork）。"""
    notes: list[str] = []
    pages = (
        "https://qoder.com/zh/qoderwork",
        "https://qoder.com/en/qoderwork",
        "https://qoder.com/zh/download",
        "https://qoder.com/en/download",
    )
    try:
        for page in pages:
            r = s.get(page, timeout=40)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            html = r.text
            ver, hits = _qoder_install_urls_from_chunks(s, html)
            win, mac, lin = _pick_qoderwork_installers(hits)
            if win or mac or lin:
                return _item(
                    "qoderwork",
                    ver,
                    {
                        "windows": {"url": win, "filename": os.path.basename(win.split("?", 1)[0])}
                        if win
                        else None,
                        "darwin": {"url": mac, "filename": os.path.basename(mac.split("?", 1)[0])}
                        if mac
                        else None,
                        "linux": {"url": lin, "filename": os.path.basename(lin.split("?", 1)[0])}
                        if lin
                        else None,
                    },
                    notes=(
                        f"自 {page} 的 g.alicdn.com Qoder Next chunks 解析（仅 QoderWork 包名）。"
                        " 产品页 https://qoder.com/zh/qoderwork ；亦可能出现在 qoder.com/*/download 与 IDE 同源 chunks。"
                    ),
                )
    except Exception as e:
        notes.append(str(e))
    return _item(
        "qoderwork",
        "0",
        {"windows": None, "darwin": None, "linux": None},
        notes="; ".join(notes)
        or "未能解析 QoderWork 安装包，请从 https://qoder.com/zh/qoderwork 手动下载。",
    )


def _codebuddy_from_update_api(
    s: requests.Session,
    api_origin: str,
    referer: str,
) -> tuple[str, dict[str, dict[str, str] | None]]:
    """调用 CodeBuddy 官方 /v2/update?platform=ide-* 返回各端安装包 URL。"""
    headers = {"Referer": referer, "Accept": "application/json"}
    base = api_origin.rstrip("/")

    def one(platform: str) -> dict[str, Any]:
        r = s.get(
            f"{base}/v2/update",
            params={"platform": platform},
            headers=headers,
            timeout=40,
        )
        r.raise_for_status()
        return r.json()

    win_j = one("ide-win32-x64-user")
    ver = str(win_j.get("productVersion") or win_j.get("version") or "unknown")
    win_url = (win_j.get("url") or "").strip()
    mac_arm = (one("ide-darwin-arm64").get("url") or "").strip()
    mac_x64 = (one("ide-darwin-x64").get("url") or "").strip()
    mac_url = mac_arm or mac_x64
    downloads: dict[str, dict[str, str] | None] = {
        "windows": {"url": win_url, "filename": os.path.basename(win_url.split("?", 1)[0])}
        if win_url
        else None,
        "darwin": {"url": mac_url, "filename": os.path.basename(mac_url.split("?", 1)[0])}
        if mac_url
        else None,
        "linux": None,
    }
    return ver, downloads


def _workbuddy_from_update_api(
    s: requests.Session,
) -> tuple[str, dict[str, dict[str, str] | None]]:
    """WorkBuddy：https://copilot.tencent.com/work/ 对应 copilot.tencent.com/v2/update?platform=workbuddy-* 。"""
    headers = {"Referer": "https://copilot.tencent.com/work/", "Accept": "application/json"}
    base = "https://copilot.tencent.com"

    def one(platform: str) -> dict[str, Any]:
        r = s.get(
            f"{base}/v2/update",
            params={"platform": platform},
            headers=headers,
            timeout=40,
        )
        r.raise_for_status()
        return r.json()

    win_j = one("workbuddy-win32-x64-user")
    ver = str(win_j.get("productVersion") or win_j.get("version") or "unknown")
    win_url = (win_j.get("url") or "").strip()
    mac_arm = (one("workbuddy-darwin-arm64").get("url") or "").strip()
    mac_x64 = (one("workbuddy-darwin-x64").get("url") or "").strip()
    mac_url = mac_arm or mac_x64
    downloads: dict[str, dict[str, str] | None] = {
        "windows": {"url": win_url, "filename": os.path.basename(win_url.split("?", 1)[0])}
        if win_url
        else None,
        "darwin": {"url": mac_url, "filename": os.path.basename(mac_url.split("?", 1)[0])}
        if mac_url
        else None,
        "linux": None,
    }
    return ver, downloads


def fetch_codebuddy(s: requests.Session) -> dict[str, Any]:
    ver, dl = _codebuddy_from_update_api(
        s, "https://www.codebuddy.ai", "https://www.codebuddy.ai/ide"
    )
    return _item(
        "codebuddy",
        ver,
        dl,
        notes="官方 https://www.codebuddy.ai/v2/update?platform=ide-win32-x64-user / ide-darwin-arm64 等。",
    )


def fetch_codebuddy_cn(s: requests.Session) -> dict[str, Any]:
    ver, dl = _codebuddy_from_update_api(
        s, "https://copilot.tencent.com", "https://copilot.tencent.com/ide/"
    )
    return _item(
        "codebuddy_cn",
        ver,
        dl,
        notes="官方 https://copilot.tencent.com/v2/update（国内 IDE 下载接口）。",
    )


def fetch_workbuddy(s: requests.Session) -> dict[str, Any]:
    """WorkBuddy 办公智能体：官网 https://copilot.tencent.com/work/ ，安装包走 v2/update workbuddy-* 通道。"""
    try:
        ver, dl = _workbuddy_from_update_api(s)
        return _item(
            "workbuddy",
            ver,
            dl,
            notes=(
                "与 https://copilot.tencent.com/work/ 一致：GET copilot.tencent.com/v2/update "
                "?platform=workbuddy-win32-x64-user | workbuddy-darwin-arm64 | workbuddy-darwin-x64 ，"
                " CDN 为 download.codebuddy.cn/workbuddy/… ；mac 当前分发 zip；无 Linux 平台 id。"
            ),
        )
    except Exception as e:
        return _item(
            "workbuddy",
            "0",
            {"windows": None, "darwin": None, "linux": None},
            notes=f"解析失败 ({e})；请从 https://copilot.tencent.com/work/ 手动下载。",
        )


def main():
    ap = argparse.ArgumentParser(description="生成 VibeCodingToolsDown manifest.json")
    ap.add_argument(
        "--output-dir",
        default="",
        help="输出根目录（默认：本包根下 dist/）",
    )
    args = ap.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 本脚本位于 …/scripts/，输出默认写入包根目录 dist/（与是否在主仓库内无关）
    vibe_root = os.path.normpath(os.path.join(script_dir, ".."))
    out_root = args.output_dir.strip() or os.path.join(vibe_root, "dist")
    out_dir = os.path.join(out_root, "vibecoding")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "manifest.json")

    s = _session()
    items: list[dict[str, Any]] = []
    builders = [
        fetch_cursor,
        fetch_vscode,
        fetch_vscodium,
        fetch_trae,
        fetch_trae_cn,
        fetch_trae_solo,
        fetch_qoder,
        fetch_qoderwork,
        fetch_codebuddy,
        fetch_codebuddy_cn,
        fetch_workbuddy,
        fetch_antigravity,
        fetch_kiro,
        fetch_restic,
        fetch_syncthing,
        fetch_sqlitebrowser,
        fetch_caesium,
        fetch_aria2,
        fetch_cc_switch,
    ]
    errors: list[str] = []
    for fn in builders:
        try:
            items.append(fn(s))
        except Exception as e:
            errors.append(f"{fn.__name__}: {e}")

    doc = {
        "schema": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
        "errors": errors,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("Wrote", out_path, "items", len(items), "errors", len(errors))
    if errors:
        for e in errors:
            print("WARN:", e, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
