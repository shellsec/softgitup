#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补全截图/贴图/OCR 类工具：Snipaste、SunnyCapturer、Flameshot/ksnip/ScreenToGif 实装等。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")

UPSERT: dict[tuple[str, str], list] = {}
BATCH: dict[tuple[str, str], list] = {}


def _upsert(plat: str, shard: str, apps: list):
    UPSERT.setdefault((plat, shard), []).extend(apps)


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


_snip = "https://zh.snipaste.com/download.html"
_snip_repo = "snipaste-cn/desktop"
_snip_old = ["Beta", "Snipaste-1.", "Snipaste-2.10", "Snipaste-2.9", "Snipaste-2.8", "Snipaste-2.7"]
_snip_win_excl = ["-x86.zip", "arm64", "AppImage", ".dmg"] + _snip_old
_snip_linux_excl = ["-x86.zip", "arm64", ".dmg", "-x64.zip"] + _snip_old
_snip_darwin_excl = ["-x86.zip", "arm64", "AppImage", "-x64.zip", "arm64.zip"] + _snip_old

_add("windows", "13-效率.json", [{
    "id": "snipaste",
    "简介": "Snipaste（截图/贴图/OCR；官方 CDN download.snipaste.com）",
    "分类": "效率",
    "releases_url": _snip,
    "repo_path": _snip_repo,
    **_b(
        prefer_api_assets=False,
        installer_markers_match_all=True,
        installer_markers=["Snipaste-", "-x64.zip"],
        href_exclude_substrings=_snip_win_excl,
        download_url_templates=["https://download.snipaste.com/archives/Snipaste-{ver_plain}-x64.zip"],
        download_names=["Snipaste-{ver}-x64.zip"],
        save_name="Snipaste-{ver}-x64.zip",
        url_hint="Snipaste",
    ),
}])
_add("linux", "13-效率.json", [{
    "id": "snipaste",
    "简介": "Snipaste（Linux x86_64 AppImage，官方 archives CDN）",
    "分类": "效率",
    "releases_url": _snip,
    "repo_path": _snip_repo,
    **_b(
        prefer_api_assets=False,
        installer_markers_match_all=True,
        installer_markers=["Snipaste-", "x86_64.AppImage"],
        href_exclude_substrings=_snip_linux_excl,
        download_url_templates=["https://download.snipaste.com/archives/Snipaste-{ver_plain}-x86_64.AppImage"],
        installer_extensions=[".AppImage"],
        download_names=["Snipaste-{ver}-x86_64.AppImage"],
        save_name="Snipaste-{ver}-x86_64.AppImage",
        url_hint="Snipaste",
    ),
}])
_add("darwin", "13-效率.json", [{
    "id": "snipaste",
    "简介": "Snipaste（macOS dmg，官方 archives CDN）",
    "分类": "效率",
    "releases_url": _snip,
    "repo_path": _snip_repo,
    **_b(
        prefer_api_assets=False,
        installer_markers_match_all=True,
        installer_markers=["Snipaste-", ".dmg"],
        href_exclude_substrings=_snip_darwin_excl,
        download_url_templates=["https://download.snipaste.com/archives/Snipaste-{ver_plain}.dmg"],
        installer_extensions=[".dmg"],
        download_names=["Snipaste-{ver}.dmg"],
        save_name="Snipaste-{ver}.dmg",
        url_hint="Snipaste",
    ),
}])

_add("windows", "13-效率.json", [{
    "id": "sunny_capturer",
    "简介": "SunnyCapturer（跨平台截图/OCR/贴图/翻译，XMuli 开源）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["SunnyCapturer_setup_", ".exe"],
        href_exclude_substrings=["portable", "ocr_cpu", "ocr_gpu", "7z", "checksums"],
        windows_installer=True,
        download_names=["SunnyCapturer_setup_{ver}.exe"],
        save_name="SunnyCapturer_setup_{ver}.exe",
        run_installer=True,
    ),
    **_repo("XMuli/SunnyCapturer"),
}])

_fs = "flameshot-org/flameshot"
_upsert("windows", "13-效率.json", [{
    "id": "flameshot",
    "简介": "Flameshot（开源截图/标注）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["Flameshot-", "win64.msi"],
        href_exclude_substrings=["sha256", ".zip", "macos", "artifact", "appimage"],
        windows_installer=True,
        installer_extensions=[".msi"],
        download_names=["Flameshot-{ver}-win64.msi"],
        save_name="Flameshot-{ver}-win64.msi",
        run_installer=True,
        process_name="flameshot.exe",
    ),
    **_repo(_fs),
}])
_upsert("linux", "13-效率.json", [{
    "id": "flameshot",
    "简介": "Flameshot（Linux AppImage 打包 zip）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["artifact-appimage-x86_64.zip"],
        href_exclude_substrings=["sha256", "arm64", "armhf", "debian", "fedora", "flatpak", "snap", "ubuntu", "win64", "macos"],
        installer_extensions=[".zip"],
        use_download_filename=True,
        save_name="flameshot-appimage-x86_64.zip",
    ),
    **_repo(_fs),
}])
_upsert("darwin", "13-效率.json", [{
    "id": "flameshot",
    "简介": "Flameshot（macOS Apple Silicon dmg）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["Flameshot-", "macos-arm64.dmg"],
        href_exclude_substrings=["sha256", "intel", "win64", "artifact", "zip"],
        installer_extensions=[".dmg"],
        use_download_filename=True,
        save_name="Flameshot-macos-arm64.dmg",
    ),
    **_repo(_fs),
}])
_add("darwin", "13-效率.json", [{
    "id": "flameshot_darwin_intel",
    "简介": "Flameshot（macOS Intel dmg）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["Flameshot-", "macos-intel.dmg"],
        href_exclude_substrings=["sha256", "arm64", "win64", "artifact"],
        installer_extensions=[".dmg"],
        use_download_filename=True,
        save_name="Flameshot-macos-intel.dmg",
    ),
    **_repo(_fs),
}])

_ks = "ksnip/ksnip"
_upsert("windows", "13-效率.json", [{
    "id": "ksnip",
    "简介": "ksnip（开源截图/标注，Windows zip）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["ksnip-", "-windows.zip"],
        href_exclude_substrings=["AppImage", "deb", "rpm", "dmg", "msi"],
        installer_extensions=[".zip"],
        download_names=["ksnip-{ver}-windows.zip"],
        save_name="ksnip-{ver}-windows.zip",
    ),
    **_repo(_ks),
}])
_upsert("linux", "13-效率.json", [{
    "id": "ksnip",
    "简介": "ksnip（Linux x86_64 AppImage）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["ksnip-", "x86_64.AppImage"],
        href_exclude_substrings=["windows", "deb", "rpm", "dmg"],
        installer_extensions=[".AppImage"],
        download_names=["ksnip-{ver}-x86_64.AppImage"],
        save_name="ksnip-{ver}-x86_64.AppImage",
    ),
    **_repo(_ks),
}])
_upsert("darwin", "13-效率.json", [{
    "id": "ksnip",
    "简介": "ksnip（macOS dmg）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["ksnip-", ".dmg"],
        href_exclude_substrings=["windows", "AppImage", "deb", "rpm"],
        installer_extensions=[".dmg"],
        download_names=["ksnip-{ver}.dmg"],
        save_name="ksnip-{ver}.dmg",
    ),
    **_repo(_ks),
}])

_stg = "NickeManarin/ScreenToGif"
_upsert("windows", "22-音视频.json", [{
    "id": "screen_to_gif",
    "简介": "ScreenToGif（GIF/录屏，Windows x64 安装包）",
    "分类": "音视频",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["ScreenToGif.", "Light.Setup.x64.msi"],
        href_exclude_substrings=["Portable", "Arm64", "x86.", "Package", "msix"],
        windows_installer=True,
        installer_extensions=[".msi"],
        download_names=["ScreenToGif.{ver}.Light.Setup.x64.msi"],
        save_name="ScreenToGif.{ver}.Light.Setup.x64.msi",
        run_installer=True,
        process_name="ScreenToGif.exe",
    ),
    **_repo(_stg),
}])

_add("windows", "13-效率.json", [{
    "id": "greenshot_portable",
    "简介": "Greenshot 便携版（Windows zip）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["Greenshot-PORTABLE-", "-RELEASE.zip"],
        href_exclude_substrings=["INSTALLER"],
        installer_extensions=[".zip"],
        download_names=["Greenshot-PORTABLE-{ver}-RELEASE.zip"],
        save_name="Greenshot-PORTABLE-{ver}-RELEASE.zip",
    ),
    **_repo("greenshot/greenshot"),
}])

for plat in ("windows", "darwin", "linux"):
    _add(plat, "13-效率.json", [{
        "id": "picpick",
        "简介": "PicPick（截图/取色/标尺；官网 picpick.app 分发，GitHub 无安装包；勿启用）",
        "分类": "效率",
        "releases_url": "https://picpick.app/en/download",
        "repo_path": "picpick/picpick",
        "prefer_api_assets": False,
        "url_hint": "picpick",
        **_b(),
    }])

_upsert("windows", "13-效率.json", [{
    "id": "snipaste",
    "href_exclude_substrings": _snip_win_excl,
}])
_upsert("linux", "13-效率.json", [{
    "id": "snipaste",
    "href_exclude_substrings": _snip_linux_excl,
}])
_upsert("darwin", "13-效率.json", [{
    "id": "snipaste",
    "href_exclude_substrings": _snip_darwin_excl,
}])

_oms = "redf0x1/ohmyshot-releases"
for plat, shard, spec in (
    ("windows", "13-效率.json", dict(
        id="ohmyshot",
        简介="OhMyShot（截图美化/标注/滚动截图/GIF；跨平台 GitHub Release）",
        installer_markers=["OhMyShot_", "_x64-setup.exe"],
        href_exclude_substrings=[".sig", ".deb", ".rpm", "AppImage", ".dmg", ".msi", "app.tar"],
        windows_installer=True,
        download_names=["OhMyShot_{ver}_x64-setup.exe"],
        save_name="OhMyShot_{ver}_x64-setup.exe",
        run_installer=True,
    )),
    ("linux", "13-效率.json", dict(
        id="ohmyshot",
        简介="OhMyShot（Linux x86_64 AppImage）",
        installer_markers=["OhMyShot_", "_amd64.AppImage"],
        href_exclude_substrings=[".sig", ".deb", ".rpm", ".dmg", "setup", "app.tar", "aarch64"],
        installer_extensions=[".AppImage"],
        download_names=["OhMyShot_{ver}_amd64.AppImage"],
        save_name="OhMyShot_{ver}_amd64.AppImage",
    )),
    ("darwin", "13-效率.json", dict(
        id="ohmyshot",
        简介="OhMyShot（macOS Apple Silicon dmg）",
        installer_markers=["OhMyShot_", "_aarch64.dmg"],
        href_exclude_substrings=[".sig", "AppImage", "setup", "x64.dmg", "app.tar", ".deb", ".rpm"],
        installer_extensions=[".dmg"],
        download_names=["OhMyShot_{ver}_aarch64.dmg"],
        save_name="OhMyShot_{ver}_aarch64.dmg",
    )),
):
    entry = {"分类": "效率", **_b(**{k: v for k, v in spec.items() if k not in ("id", "简介")}), **_repo(_oms)}
    entry["id"] = spec["id"]
    entry["简介"] = spec["简介"]
    _add(plat, shard, [entry])

_add("darwin", "13-效率.json", [{
    "id": "ohmyshot_darwin_intel",
    "简介": "OhMyShot（macOS Intel dmg）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["OhMyShot_", "_x64.dmg"],
        href_exclude_substrings=[".sig", "aarch64", "AppImage", "setup", "app.tar"],
        installer_extensions=[".dmg"],
        download_names=["OhMyShot_{ver}_x64.dmg"],
        save_name="OhMyShot_{ver}_x64.dmg",
    ),
    **_repo(_oms),
}])

_os = "Tracekit-Dev/openshots"
for plat, shard, spec in (
    ("windows", "13-效率.json", dict(
        id="openshots",
        简介="OpenShots（Tauri 截图美化/标注，跨平台）",
        installer_markers=["OpenShots_", "_x64_en-US.msi"],
        href_exclude_substrings=["cli", "AppImage", ".deb", ".rpm", ".dmg", "aarch64"],
        windows_installer=True,
        installer_extensions=[".msi"],
        download_names=["OpenShots_{ver}_x64_en-US.msi"],
        save_name="OpenShots_{ver}_x64_en-US.msi",
        run_installer=True,
    )),
    ("linux", "13-效率.json", dict(
        id="openshots",
        简介="OpenShots（Linux x86_64 AppImage）",
        installer_markers=["OpenShots_", "_amd64.AppImage"],
        href_exclude_substrings=["cli", ".deb", ".rpm", ".dmg", "aarch64", ".msi"],
        installer_extensions=[".AppImage"],
        download_names=["OpenShots_{ver}_amd64.AppImage"],
        save_name="OpenShots_{ver}_amd64.AppImage",
    )),
    ("darwin", "13-效率.json", dict(
        id="openshots",
        简介="OpenShots（macOS Apple Silicon dmg）",
        installer_markers=["OpenShots_", "_aarch64.dmg"],
        href_exclude_substrings=["cli", "AppImage", ".deb", ".rpm", "_x64", ".msi"],
        installer_extensions=[".dmg"],
        download_names=["OpenShots_{ver}_aarch64.dmg"],
        save_name="OpenShots_{ver}_aarch64.dmg",
    )),
):
    entry = {"分类": "效率", **_b(**{k: v for k, v in spec.items() if k not in ("id", "简介")}), **_repo(_os)}
    entry["id"] = spec["id"]
    entry["简介"] = spec["简介"]
    _add(plat, shard, [entry])

_add("darwin", "13-效率.json", [{
    "id": "openshots_darwin_intel",
    "简介": "OpenShots（macOS Intel dmg）",
    "分类": "效率",
    **_b(
        installer_markers_match_all=True,
        installer_markers=["OpenShots_", "_x64.dmg"],
        href_exclude_substrings=["cli", "AppImage", "aarch64", ".deb", ".msi"],
        installer_extensions=[".dmg"],
        download_names=["OpenShots_{ver}_x64.dmg"],
        save_name="OpenShots_{ver}_x64.dmg",
    ),
    **_repo(_os),
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


def _strip_id_from_shard(path: str, ids: set[str]):
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
            _strip_id_from_shard(
                os.path.join(APPS, plat, "99-未匹配-windows分片.json"),
                {"flameshot"},
            )
    return upserted, added, skipped


def main():
    dry = "--dry-run" in sys.argv
    u, a, s = merge_all(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: upserted {u}, added {a}, skipped duplicate {s}")


if __name__ == "__main__":
    main()
