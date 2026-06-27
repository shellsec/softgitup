#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""初始化 apps-mobile：Android APK 条目 + iOS App Store 占位。"""
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


# --- Android ---
_apk("termux", "01-工具.json", "工具", "termux/termux-app",
     "Termux（Android 终端 / 包管理）",
     ["termux-app_", "universal", ".apk"],
     ["bootstrap", "armeabi", "x86_64-only"])
_apk("obtainium", "01-工具.json", "工具", "ImranR98/Obtainium",
     "Obtainium（从 GitHub 等源追踪并更新 APK）",
     ["Obtainium", "universal", ".apk"],
     ["arm64-v8a", "armeabi", "x86_64"])
_apk("material_files", "01-工具.json", "工具", "zhanghai/MaterialFiles",
     "Material Files（开源文件管理器）",
     ["app-release", ".apk"],
     ["debug", "lite"])
_apk("aurora_store", "02-下载.json", "下载", "whyGitHub/AuroraStore",
     "Aurora Store（Play 商店客户端，开源）",
     ["AuroraStore", "universal", ".apk"],
     ["vanilla", "nightly"])
_apk("fdroid", "02-下载.json", "下载", "fdroid/fdroidclient",
     "F-Droid（开源应用商店客户端）",
     ["F-Droid_", "unsigned.apk"],
     ["test", "privileged"])
_apk("newpipe", "04-多媒体.json", "多媒体", "TeamNewPipe/NewPipe",
     "NewPipe（YouTube 第三方客户端）",
     ["NewPipe_", ".apk"],
     ["debug"])
_apk("vlc_android", "04-多媒体.json", "多媒体", "videolan/vlc-android",
     "VLC for Android",
     ["VLC-Android-", ".apk"],
     ["debug", "neon"])
_apk("osmand", "04-多媒体.json", "多媒体", "osmandapp/OsmAnd",
     "OsmAnd（离线地图 / 导航）",
     ["Osmand-", "universal", ".apk"],
     ["nightly", "debug"])
_apk("markor", "07-笔记.json", "笔记", "gsantner/markor",
     "Markor（Markdown 笔记，离线优先）",
     ["markor-", "flavor", "release.apk"],
     ["debug"])
_apk("orgzly", "07-笔记.json", "笔记", "orgzly/orgzly-android",
     "Orgzly（Org mode 笔记）",
     ["orgzly-", ".apk"],
     ["debug"])
_apk("openboard", "08-输入.json", "输入", "openboard-team/openboard",
     "OpenBoard（开源 Gboard 替代键盘）",
     ["OpenBoard_", ".apk"],
     ["debug", "test"])
_apk("syncthing_android", "06-网络.json", "网络", "syncthing/syncthing-android",
     "Syncthing（Android 客户端）",
     ["syncthing-android-", "universal", ".apk"],
     ["debug"])
_apk("tailscale_android", "06-网络.json", "网络", "tailscale/tailscale-android",
     "Tailscale（Android VPN/组网）",
     ["tailscale-android-", ".apk"],
     ["debug", "fdroid-only"])
_apk("immich_android", "06-网络.json", "网络", "immich-app/immich",
     "Immich（自托管相册 Android 客户端）",
     ["immich-", "release.apk"],
     ["debug", "ios", "server"])
_apk("kdeconnect", "06-网络.json", "网络", "KDE/kdeconnect-kde",
     "KDE Connect（手机与桌面互联）",
     ["KDEConnect-", ".apk"],
     ["debug"])
_apk("thunderbird_android", "09-通讯.json", "通讯", "thunderbird/thunderbird-android",
     "Thunderbird for Android（原 K-9 Mail）",
     ["thunderbird-", "release.apk"],
     ["beta", "debug"])
_apk("fenix", "10-浏览器.json", "浏览器", "mozilla-mobile/fenix",
     "Firefox for Android（Fenix）",
     ["fenix-", "arm64-v8a", ".apk"],
     ["x86", "debug", "beta"])
_apk("duckduckgo_android", "10-浏览器.json", "浏览器", "duckduckgo/Android",
     "DuckDuckGo Privacy Browser",
     ["duckduckgo-", "release.apk"],
     ["debug", "play"])
_apk("home_assistant", "11-智能家居.json", "智能家居", "home-assistant/android",
     "Home Assistant Companion",
     ["app-full-release.apk", "home-assistant"],
     ["debug", "minimal"])
_apk("bitwarden_android", "05-安全.json", "安全", "bitwarden/android",
     "Bitwarden（Android 客户端）",
     ["com.x8bit.bitwarden", ".apk"],
     ["debug", "fdroid"])

# --- iOS 占位（勿启用）---
_ios_store = [
    ("firefox_ios", "Firefox", "mozilla-mobile/firefox-ios", "https://apps.apple.com/app/firefox-private-safe-browser/id989804926"),
    ("bitwarden_ios", "Bitwarden", "bitwarden/ios", "https://apps.apple.com/app/bitwarden-password-manager/id1137397744"),
    ("signal_ios", "Signal", "signalapp/Signal-iOS", "https://apps.apple.com/app/signal-private-messenger/id874139669"),
    ("protonvpn_ios", "Proton VPN", "ProtonVPN/ios-mac-app", "https://apps.apple.com/app/proton-vpn-fast-secure/id1437005085"),
    ("immich_ios", "Immich", "immich-app/immich", "https://apps.apple.com/app/immich/id1613940772"),
]
for iid, name, repo, url in _ios_store:
    _add("99-占位-AppStore.json", [{
        "id": iid,
        "简介": f"{name}（iOS · App Store 分发，无 GitHub 安装包；勿启用 auto_update）",
        "分类": "占位",
        "enabled": False,
        "prefer_api_assets": False,
        "releases_url": url,
        "repo_path": repo,
        "run_installer": False,
        "url_hint": name.lower(),
    }])


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for shard, apps in sorted(BATCH.items()):
        plat_dir = "android" if not shard.startswith("99-") else "ios"
        path = os.path.join(MOBILE, plat_dir, shard)
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
