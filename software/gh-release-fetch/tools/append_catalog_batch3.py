#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补全 linux/darwin 缺失分片（19/22/25）及跨平台实用条目。同 id 不重复追加。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")

BATCH: dict[tuple[str, str], list] = {}


def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


def _base(**kw):
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


MISSING_SHARDS = (
    ("linux", "19-网络与协作.json"),
    ("linux", "22-音视频.json"),
    ("linux", "25-可观测.json"),
    ("darwin", "19-网络与协作.json"),
    ("darwin", "22-音视频.json"),
    ("darwin", "25-可观测.json"),
)

# --- 02 motrix / gopeed ---
_motrix = {
    "简介": "Motrix（全能下载工具：HTTP/FTP/BT/磁力链）",
    "分类": "下载",
    "releases_url": "https://bgithub.xyz/agalwood/Motrix/releases",
    "repo_path": "agalwood/Motrix",
}
_add("linux", "02-下载.json", [{
    **_motrix,
    "id": "motrix",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Motrix-", "x64.AppImage"],
        href_exclude_substrings=["dmg", "exe", "arm64", "yml", "blockmap"],
        installer_extensions=[".AppImage"],
        use_download_filename=True,
        save_name="Motrix.AppImage",
    ),
}])
_add("darwin", "02-下载.json", [{
    **_motrix,
    "id": "motrix",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Motrix-", ".dmg"],
        href_exclude_substrings=["AppImage", "exe", "yml", "blockmap", "arm64"],
        installer_extensions=[".dmg"],
        use_download_filename=True,
        save_name="Motrix.dmg",
    ),
}])
_gopeed = {
    "简介": "Gopeed（HTTP/BT 等，现代下载器）",
    "分类": "下载",
    "releases_url": "https://bgithub.xyz/GopeedLab/gopeed/releases",
    "repo_path": "GopeedLab/gopeed",
}
_add("linux", "02-下载.json", [{
    **_gopeed,
    "id": "gopeed",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Gopeed-v", "linux-amd64.zip"],
        href_exclude_substrings=["windows", "macos", "qnap", "arm64", "ia32", "blockmap", ".deb"],
        installer_extensions=[".zip"],
        download_names=["Gopeed-v{ver}-linux-amd64.zip"],
        save_name="Gopeed-v{ver}-linux-amd64.zip",
    ),
}])
_add("darwin", "02-下载.json", [{
    **_gopeed,
    "id": "gopeed",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Gopeed-v", "macos-amd64.dmg"],
        href_exclude_substrings=["windows", "linux", "qnap", "arm64", "blockmap"],
        installer_extensions=[".dmg"],
        download_names=["Gopeed-v{ver}-macos-amd64.dmg"],
        save_name="Gopeed-v{ver}-macos-amd64.dmg",
    ),
}])

# --- 19 网络与协作 ---
_collab = [
    ("mattermost_desktop", "mattermost/desktop", "Mattermost 桌面客户端",
     {"win": ("win.exe", ["mac", "linux"]), "linux": ("linux-x64.tar.gz", ["win", "mac", "arm64"]),
      "darwin": ("mac-x64.dmg", ["win", "linux", "arm64"])}),
    ("zulip_desktop", "zulip/zulip-desktop", "Zulip 桌面客户端",
     {"win": None, "linux": ("x86_64.AppImage", ["win", "mac", "arm64"]),
      "darwin": ("arm64.dmg", ["win", "linux", "x86"])}),
    ("rocketchat_desktop", "RocketChat/Rocket.Chat.Electron", "Rocket.Chat 桌面客户端",
     {"linux": ("linux-x64.deb", ["win", "mac", "arm64", "appx"]),
      "darwin": ("mac.dmg", ["win", "linux", "arm64"])}),
    ("ferdium", "ferdium/ferdium-app", "Ferdium（聚合 Slack/Discord 等）",
     {"linux": ("Ferdium-linux-x64", ".AppImage", ["mac", "win", "arm64"]),
      "darwin": ("Ferdium-mac-arm64", ".dmg", ["linux", "win", "x86"])}),
]
for aid, repo, desc, plats in _collab:
    owner_repo = repo
    for plat, spec in plats.items():
        if spec is None or plat == "win":
            continue
        if len(spec) == 2:
            marker_suffix, excl = spec
            markers = [marker_suffix]
            match_all = False
        else:
            m1, m2, excl = spec
            markers = [m1, m2]
            match_all = True
        _add(plat, "19-网络与协作.json", [{
            "id": aid,
            "简介": desc,
            "分类": "网络与协作",
            "releases_url": f"https://bgithub.xyz/{owner_repo}/releases",
            "repo_path": owner_repo,
            **_base(
                installer_markers=markers,
                installer_markers_match_all=match_all,
                href_exclude_substrings=excl,
                use_download_filename=True,
            ),
        }])

# --- 22 音视频（含 batch2 未写入的 openshot linux）---
_av = [
    ("losslesscut", "mifi/lossless-cut", "LosslessCut（无损裁剪/合并）",
     "linux", ["LosslessCut-linux", "AppImage"], ["win", "dmg"],
     ".AppImage", "LosslessCut-linux-x86_64.AppImage"),
    ("losslesscut", "mifi/lossless-cut", "LosslessCut（macOS dmg）",
     "darwin", ["LosslessCut-mac", ".dmg"], ["win", "linux", "AppImage"],
     ".dmg", "LosslessCut-mac-x64.dmg"),
    ("vidcutter", "ozmartian/vidcutter", "VidCutter（视频剪切/合并）",
     "linux", ["VidCutter-", "x86_64.AppImage"], ["win", "macOS"],
     ".AppImage", "VidCutter-{ver}-x86_64.AppImage"),
    ("vidcutter", "ozmartian/vidcutter", "VidCutter（macOS dmg）",
     "darwin", ["VidCutter-", "macOS.dmg"], ["win", "AppImage"],
     ".dmg", "VidCutter-{ver}-macOS.dmg"),
    ("syncplay", "Syncplay/syncplay", "Syncplay（异地同步播放）",
     "linux", ["Syncplay-", "x86_64.AppImage"], ["Setup.exe", "dmg", "Portable"],
     ".AppImage", "Syncplay-{ver}-x86_64.AppImage"),
    ("syncplay", "Syncplay/syncplay", "Syncplay（macOS dmg）",
     "darwin", ["Syncplay-", ".dmg"], ["Setup.exe", "AppImage", "Portable", "deb"],
     ".dmg", "Syncplay-{ver}.dmg"),
    ("openshot", "OpenShot/openshot-qt", "OpenShot 视频编辑器（AppImage）",
     "linux", ["OpenShot", "x86_64.AppImage"], ["exe", "dmg"],
     ".AppImage", "OpenShot-v{ver}-x86_64.AppImage"),
    ("openshot", "OpenShot/openshot-qt", "OpenShot 视频编辑器（macOS dmg）",
     "darwin", ["OpenShot", "x86_64.dmg"], ["exe", "AppImage", "arm64"],
     ".dmg", "OpenShot-v{ver}-x86_64.dmg"),
]
for aid, repo, desc, plat, markers, excl, ext, save in _av:
    entry = {
        "id": aid,
        "简介": desc,
        "分类": "音视频",
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
        **_base(
            installer_markers_match_all=True,
            installer_markers=markers,
            href_exclude_substrings=excl,
            installer_extensions=[ext],
            download_names=[save] if "{ver}" in save else None,
            save_name=save,
        ),
    }
    if entry.get("download_names") is None:
        entry.pop("download_names", None)
    _add(plat, "22-音视频.json", [entry])

# --- 25 可观测（含 netdata linux）---
_obs_tools = [
    ("grafana", "grafana/grafana", "Grafana 可观测性仪表盘",
     "grafana_", {"linux": "linux-amd64.tar.gz", "darwin": "darwin-amd64.tar.gz"}),
    ("prometheus", "prometheus/prometheus", "Prometheus 监控",
     "prometheus-", {"linux": "linux-amd64.tar.gz", "darwin": "darwin-amd64.tar.gz"}),
    ("jaeger", "jaegertracing/jaeger", "Jaeger 分布式链路追踪",
     "jaeger-", {"linux": "linux-amd64.tar.gz", "darwin": "darwin-amd64.tar.gz"}),
    ("loki", "grafana/loki", "Grafana Loki 日志聚合",
     "loki-", {"linux": "linux-amd64.zip", "darwin": "darwin-amd64.zip"}),
    ("tempo", "grafana/tempo", "Grafana Tempo 追踪后端",
     "tempo_", {"linux": "linux_amd64.tar.gz", "darwin": "darwin_amd64.tar.gz"}),
    ("vector", "vectordotdev/vector", "Vector 日志/指标采集",
     "vector-", {"linux": "x86_64-unknown-linux-gnu.tar.gz", "darwin": "aarch64-apple-darwin.tar.gz"}),
    ("grafana_alloy", "grafana/alloy", "Grafana Alloy（OTel Collector 发行版）",
     "alloy-", {"linux": "linux-amd64.zip", "darwin": "darwin-amd64.zip"}),
]
for aid, repo, desc, prefix, suffixes in _obs_tools:
    for plat, suffix in suffixes.items():
        excl = ["windows"] + (["darwin", "linux"] if plat == "linux" else ["linux", "windows"])
        if plat == "linux":
            excl = ["windows", "darwin", "arm", "freebsd"]
        else:
            excl = ["windows", "linux", "x86_64-unknown-linux"]
        _add(plat, "25-可观测.json", [{
            "id": aid,
            "简介": desc,
            "分类": "可观测",
            "releases_url": f"https://bgithub.xyz/{repo}/releases",
            "repo_path": repo,
            **_base(
                installer_markers_match_all=True,
                installer_markers=[prefix, suffix],
                href_exclude_substrings=excl,
                use_download_filename=True,
            ),
        }])

_add("linux", "25-可观测.json", [{
    "id": "netdata",
    "简介": "Netdata（监控 Agent，Linux 静态二进制）",
    "分类": "可观测",
    "releases_url": "https://bgithub.xyz/netdata/netdata/releases",
    "repo_path": "netdata/netdata",
    **_base(
        installer_markers=["netdata-", "x86_64.gz"],
        href_exclude_substrings=["arm", "ppc", "s390", "windows", "darwin"],
        installer_extensions=[".gz"],
    ),
}])
_add("darwin", "25-可观测.json", [{
    "id": "netdata",
    "简介": "Netdata（macOS 静态二进制）",
    "分类": "可观测",
    "releases_url": "https://bgithub.xyz/netdata/netdata/releases",
    "repo_path": "netdata/netdata",
    **_base(
        installer_markers=["netdata-", "darwin-x86_64.gz"],
        href_exclude_substrings=["linux", "windows", "arm", "ppc"],
        installer_extensions=[".gz"],
    ),
}])

# --- batch2 仅 windows 的条目补 darwin/linux ---
_add("darwin", "29-局域网文件共享.json", [{
    "id": "alist",
    "简介": "AList（macOS arm64 tar.gz）",
    "分类": "局域网文件共享",
    "releases_url": "https://bgithub.xyz/AlistGo/alist/releases",
    "repo_path": "AlistGo/alist",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["darwin-arm64", ".tar.gz"],
        href_exclude_substrings=["windows", "linux", "amd64", "386"],
        installer_extensions=[".tar.gz"],
        download_names=["alist-darwin-arm64-{ver}.tar.gz"],
        save_name="alist-darwin-arm64-{ver}.tar.gz",
    ),
}])
_add("darwin", "10-安全.json", [{
    "id": "owasp_zap",
    "简介": "OWASP ZAP（macOS 包）",
    "分类": "安全",
    "releases_url": "https://bgithub.xyz/zaproxy/zaproxy/releases",
    "repo_path": "zaproxy/zaproxy",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["ZAP_", "_Mac.dmg"],
        href_exclude_substrings=["Windows", "Linux", "CrossPlatform"],
        installer_extensions=[".dmg"],
        download_names=["ZAP_{ver}_Mac.dmg"],
        save_name="ZAP_{ver}_Mac.dmg",
    ),
}])
_add("darwin", "12-开发.json", [{
    "id": "forgejo",
    "简介": "Forgejo（macOS amd64）",
    "分类": "开发",
    "releases_url": "https://bgithub.xyz/forgejo/forgejo/releases",
    "repo_path": "forgejo/forgejo",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["forgejo-", "darwin-4.0-amd64.zip"],
        href_exclude_substrings=["windows", "linux", "arm64", ".asc"],
        installer_extensions=[".zip"],
        download_names=["forgejo-{ver}-darwin-4.0-amd64.zip"],
        save_name="forgejo-{ver}-darwin-4.0-amd64.zip",
    ),
}])
for plat, suffix, excl in (
    ("linux", "linux-x64.zip", ["win64", "mac"]),
    ("darwin", "mac-arm64.zip", ["win64", "linux"]),
):
    _add(plat, "12-开发.json", [{
        "id": "playwright_cli",
        "简介": f"Playwright CLI（{plat} zip）",
        "分类": "开发",
        "releases_url": "https://bgithub.xyz/microsoft/playwright/releases",
        "repo_path": "microsoft/playwright",
        **_base(
            installer_markers=["playwright-", suffix],
            href_exclude_substrings=excl,
            installer_extensions=[".zip"],
            download_names=[f"playwright-{{ver}}-{suffix}"],
            save_name=f"playwright-{{ver}}-{suffix}",
        ),
    }])
_add("darwin", "26-编辑器.json", [{
    "id": "pulsar",
    "简介": "Pulsar（Atom 继任，macOS zip）",
    "分类": "编辑器",
    "releases_url": "https://bgithub.xyz/pulsar-edit/pulsar/releases",
    "repo_path": "pulsar-edit/pulsar",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Pulsar-", "mac.zip"],
        href_exclude_substrings=["win", "linux", "arm64", "blockmap"],
        installer_extensions=[".zip"],
        use_download_filename=True,
        save_name="Pulsar-mac.zip",
    ),
}])
_add("linux", "26-编辑器.json", [{
    "id": "pulsar",
    "简介": "Pulsar（Linux x64 tar.gz）",
    "分类": "编辑器",
    "releases_url": "https://bgithub.xyz/pulsar-edit/pulsar/releases",
    "repo_path": "pulsar-edit/pulsar",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Pulsar-", "linux-x64.tar.gz"],
        href_exclude_substrings=["win", "mac", "arm64"],
        installer_extensions=[".tar.gz"],
        use_download_filename=True,
        save_name="Pulsar-linux-x64.tar.gz",
    ),
}])
_add("darwin", "26-编辑器.json", [{
    "id": "lite_xl",
    "简介": "Lite XL（macOS tar.gz）",
    "分类": "编辑器",
    "releases_url": "https://bgithub.xyz/lite-xl/lite-xl/releases",
    "repo_path": "lite-xl/lite-xl",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["lite-xl-", "macos-aarch64.tar.gz"],
        href_exclude_substrings=["windows", "linux", "x86"],
        installer_extensions=[".tar.gz"],
        download_names=["lite-xl-{ver}-macos-aarch64.tar.gz"],
        save_name="lite-xl-{ver}-macos-aarch64.tar.gz",
    ),
}])
_add("darwin", "01-AI.json", [{
    "id": "aider",
    "简介": "aider（macOS arm64 tar.gz）",
    "分类": "AI",
    "releases_url": "https://bgithub.xyz/Aider-AI/aider/releases",
    "repo_path": "Aider-AI/aider",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["aider-", "darwin-arm64.tar.gz"],
        href_exclude_substrings=["windows", "linux", "x86", ".sha256"],
        installer_extensions=[".tar.gz"],
        download_names=["aider-{ver}-darwin-arm64.tar.gz"],
        save_name="aider-{ver}-darwin-arm64.tar.gz",
    ),
}])
for plat, marker, excl, ext in (
    ("linux", "Redis-Insight-linux-amd64.deb", ["win", "darwin", "arm64"], ".deb"),
    ("darwin", "Redis-Insight-mac-arm64.dmg", ["win", "linux", "blockmap"], ".dmg"),
):
    _add(plat, "23-数据库.json", [{
        "id": "redis_insight",
        "简介": f"Redis Insight（{plat}）",
        "分类": "数据库",
        "releases_url": "https://bgithub.xyz/RedisInsight/RedisInsight/releases",
        "repo_path": "RedisInsight/RedisInsight",
        **_base(
            installer_markers_match_all=True,
            installer_markers=[marker.split(".")[0].replace("-amd64", ""), ext],
            href_exclude_substrings=excl,
            installer_extensions=[ext],
            use_download_filename=True,
            save_name=marker if "{" not in marker else marker,
        ),
    }])
# fix redis entries with simpler markers
BATCH[("linux", "23-数据库.json")] = [a for a in BATCH.get(("linux", "23-数据库.json"), []) if a.get("id") != "redis_insight"]
BATCH[("darwin", "23-数据库.json")] = [a for a in BATCH.get(("darwin", "23-数据库.json"), []) if a.get("id") != "redis_insight"]
_add("linux", "23-数据库.json", [{
    "id": "redis_insight",
    "简介": "Redis Insight（Linux amd64 deb）",
    "分类": "数据库",
    "releases_url": "https://bgithub.xyz/RedisInsight/RedisInsight/releases",
    "repo_path": "RedisInsight/RedisInsight",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Redis-Insight", "linux-amd64.deb"],
        href_exclude_substrings=["win", "darwin", "arm64"],
        installer_extensions=[".deb"],
        use_download_filename=True,
        save_name="Redis-Insight-linux-amd64.deb",
    ),
}])
_add("darwin", "23-数据库.json", [{
    "id": "redis_insight",
    "简介": "Redis Insight（macOS arm64 dmg）",
    "分类": "数据库",
    "releases_url": "https://bgithub.xyz/RedisInsight/RedisInsight/releases",
    "repo_path": "RedisInsight/RedisInsight",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["Redis-Insight", "mac-arm64.dmg"],
        href_exclude_substrings=["win", "linux", "blockmap"],
        installer_extensions=[".dmg"],
        use_download_filename=True,
        save_name="Redis-Insight-mac-arm64.dmg",
    ),
}])
for plat, marker, save in (
    ("linux", "ryujinx-", "ryujinx-{ver}-linux-x64.tar.gz"),
    ("darwin", "ryujinx-", "ryujinx-{ver}-osx-x64.tar.gz"),
):
    _add(plat, "14-游戏.json", [{
        "id": "ryujinx",
        "简介": f"Ryujinx（Switch 模拟器，{plat}）",
        "分类": "游戏",
        "releases_url": "https://bgithub.xyz/Ryubing/Ryujinx/releases",
        "repo_path": "Ryubing/Ryujinx",
        **_base(
            installer_markers_match_all=True,
            installer_markers=[marker, "x64" if plat == "linux" else "osx"],
            href_exclude_substrings=["win", "arm64", "publish"] if plat == "linux" else ["win", "linux", "arm64"],
            installer_extensions=[".tar.gz"],
            download_names=[save],
            save_name=save,
        ),
    }])
_add("darwin", "11-工具.json", [{
    "id": "7zip",
    "简介": "7-Zip（macOS tar.xz，ip7z/7zip）",
    "分类": "工具",
    "releases_url": "https://bgithub.xyz/ip7z/7zip/releases",
    "repo_path": "ip7z/7zip",
    **_base(
        installer_markers_match_all=True,
        installer_markers=["7z", "mac.tar.xz"],
        href_exclude_substrings=["linux", "win", "extra", "arm"],
        installer_extensions=[".xz"],
        use_download_filename=True,
        save_name="7zip-mac.tar.xz",
    ),
}])


def ensure_shards():
    for plat, shard in MISSING_SHARDS:
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
                f.write("\n")
            print("CREATED", path)


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
            # strip None values
            clean = {k: v for k, v in app.items() if v is not None}
            data.append(clean)
            seen.add(aid)
            added += 1
        if not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
    return added, skipped


def main():
    dry = "--dry-run" in sys.argv
    ensure_shards()
    added, skipped = merge_batch(dry_run=dry)
    mode = "dry-run" if dry else "written"
    print(f"{mode}: added {added}, skipped duplicate id {skipped}")


if __name__ == "__main__":
    main()
