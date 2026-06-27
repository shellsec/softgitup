#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""apps-mobile batch5：Android 薄分类大补 + iOS App Store 占位扩展（幂等 append）。"""
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


def _apk(id, shard, 分类, repo, 简介, markers, exclude=None, match_all=True, **extra):
    base = {
        "installer_markers_match_all": match_all,
        "installer_markers": markers,
        "href_exclude_substrings": (exclude or [])
        + [".aab", "debug", "test", "unsigned", "sources", ".json", ".txt"],
        "use_download_filename": True,
        "save_name": f"{id}.apk",
    }
    base.update(extra)
    _add(shard, [{
        "id": id,
        "简介": 简介,
        "分类": 分类,
        **_b(**base),
        **_repo(repo),
    }])


def _ios(id, name, repo, app_store_url, 分类="占位"):
    _add("99-占位-AppStore.json", [{
        "id": id,
        "简介": f"{name}（iOS · App Store；无 GitHub 安装包，勿启用 auto_update）",
        "分类": 分类,
        "enabled": False,
        "prefer_api_assets": False,
        "releases_url": app_store_url,
        "repo_path": repo,
        "run_installer": False,
        "url_hint": name.lower().split()[0],
    }])


# --- Android ---
_apk("uhabits", "13-效率.json", "效率", "iSoron/uhabits",
     "Loop Habit Tracker（习惯养成）",
     ["uhabits-", "release.apk"], ["debug"])

_apk("ppsspp", "14-游戏.json", "游戏", "hrydgard/ppsspp",
     "PPSSPP（PSP 模拟器）",
     ["PPSSPP", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])
_apk("dolphin", "14-游戏.json", "游戏", "dolphinemu/dolphin",
     "Dolphin Emulator（GameCube/Wii 模拟器）",
     ["dolphin-master", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])
_apk("retroarch_android", "14-游戏.json", "游戏", "libretro/RetroArch",
     "RetroArch（模拟器前端，Android）",
     ["RetroArch", "arm64-v8a", "apk"], ["x86", "armeabi", "debug", "ra32"])

_apk("briar", "20-网络与通讯.json", "网络与通讯", "briar/briar",
     "Briar（离线 P2P 加密通讯）",
     ["briar-", "release.apk"], ["debug"])
_apk("conversations", "20-网络与通讯.json", "网络与通讯", "Conversations/Conversations",
     "Conversations（XMPP 客户端）",
     ["Conversations-", "release.apk"], ["debug", "beta"])

_apk("jitsi_meet", "19-网络与协作.json", "网络与协作", "jitsi/jitsi-meet",
     "Jitsi Meet（视频会议）",
     ["jitsi-meet", "release.apk"], ["debug", "sdk"])
_apk("zulip", "19-网络与协作.json", "网络与协作", "zulip/zulip-flutter",
     "Zulip（团队聊天）",
     ["zulip-", "release.apk"], ["debug"])

_apk("hop_to_desk", "21-远程与协作.json", "远程与协作", "HopToDesk/HopToDesk",
     "HopToDesk（远程桌面）",
     ["HopToDesk", "Android", ".apk"], ["debug", "x86"])

_apk("transistor", "22-音视频.json", "音视频", "rockstormorg/transistor-app",
     "Transistor（网络电台）",
     ["transistor-", "release.apk"], ["debug"])
_apk("voice", "22-音视频.json", "音视频", "PaulWoitaschek/Voice",
     "Voice（有声书播放器）",
     ["voice-", "release.apk"], ["debug"])

_apk("plume", "03-写作.json", "写作", "Plume-Org/Plume",
     "Plume（ActivityPub 微博客）",
     ["Plume-", "release.apk"], ["debug"])
_apk("readera", "03-写作.json", "写作", "readera/Readera",
     "ReadEra（电子书阅读）",
     ["readera", "release.apk"], ["debug", "premium"])

_apk("domoticz", "11-智能家居.json", "智能家居", "domoticz/domoticz-android",
     "Domoticz（智能家居 Android 客户端）",
     ["domoticz", "release.apk"], ["debug"])

_apk("blokada", "10-安全.json", "安全", "blokadaorg/blokada-apps-android",
     "Blokada（广告/追踪拦截）",
     ["blokada", "release.apk"], ["debug", "legacy"])
_apk("wasted", "10-安全.json", "安全", "x13a/Wasted",
     "Wasted（紧急自毁/反取证）",
     ["wasted-", "release.apk"], ["debug"])

_apk("fossify_gallery", "09-多媒体与设计.json", "多媒体与设计", "FossifyOrg/Gallery",
     "Fossify Gallery（开源相册）",
     ["gallery-", "release.apk"], ["debug"])
_apk("fossify_calendar", "09-多媒体与设计.json", "多媒体与设计", "FossifyOrg/Calendar",
     "Fossify Calendar（开源日历）",
     ["calendar-", "release.apk"], ["debug"])

_apk("helium", "08-输入.json", "输入", "Helium314/Helium",
     "Helium（开源键盘）",
     ["helium-", "release.apk"], ["debug"])

_apk("maid", "01-AI.json", "AI", "Mobile-Artificial-Intelligence/maid",
     "maid（Mobile AI 本地聊天）",
     ["maid-", "release.apk"], ["debug"])

_apk("github_mobile", "12-开发.json", "开发", "github/github",
     "GitHub Mobile（官方 Android 客户端）",
     ["github", "release.apk"], ["debug", "beta"])

_apk("seedvault", "07-备份.json", "备份", "seedvault-app/seedvault",
     "Seedvault（Android 备份）",
     ["Seedvault-", "release.apk"], ["debug"])
_apk("wallabag", "07-备份.json", "备份", "wallabag/android-app",
     "wallabag（稍后阅读）",
     ["wallabag", "release.apk"], ["debug"])

_apk("fedilab", "18-网络.json", "网络", "stom79/Fedilab",
     "Fedilab（Mastodon 客户端）",
     ["fedilab-", "release.apk"], ["debug"])
_apk("tusky", "18-网络.json", "网络", "tuskyapp/Tusky",
     "Tusky（Mastodon 客户端）",
     ["Tusky-", "release.apk"], ["debug"])

_apk("accrescent", "02-下载.json", "下载", "accrescent/accrescent",
     "Accrescent（开源应用商店）",
     ["accrescent", "release.apk"], ["debug"])

_apk("bluewallet", "28-加密货币.json", "加密货币", "BlueWallet/BlueWallet",
     "BlueWallet（Bitcoin Lightning 钱包）",
     ["BlueWallet-", "release.apk"], ["debug"])

_apk("cgeo_db", "23-数据库.json", "数据库", "cgeo/cgeo",
     "c:geo（Geocaching · 含离线数据库）",
     ["cgeo-foss-release", ".apk"], ["google", "debug"])

_apk("simple_dialer", "09-通讯.json", "通讯", "FossifyOrg/Dialer",
     "Fossify Dialer（开源拨号）",
     ["dialer-", "release.apk"], ["debug"])

# --- iOS App Store 占位 ---
_ios("nextcloud_ios", "Nextcloud", "nextcloud/ios",
     "https://apps.apple.com/app/nextcloud/id1125420102", "网络")
_ios("element_ios", "Element", "element-hq/element-x-ios",
     "https://apps.apple.com/app/element-messenger/id1083446067", "网络")
_ios("joplin_ios", "Joplin", "laurent22/joplin",
     "https://apps.apple.com/app/joplin/id1315599797", "笔记")
_ios("syncthing_ios", "Syncthing", "syncthing/syncthing",
     "https://apps.apple.com/app/syncthing/id1434949272", "网络")
_ios("tailscale_ios", "Tailscale", "tailscale/tailscale",
     "https://apps.apple.com/app/tailscale/id1470499037", "网络")
_ios("vlc_ios", "VLC", "videolan/vlc",
     "https://apps.apple.com/app/vlc-for-mobile/id650377962", "多媒体")
_ios("protonmail_ios", "Proton Mail", "ProtonMail/proton-mail-ios",
     "https://apps.apple.com/app/proton-mail-encrypted-email/id979659905", "安全")
_ios("mullvad_ios", "Mullvad VPN", "mullvad/mullvadvpn-app",
     "https://apps.apple.com/app/mullvad-vpn/id1484208628", "安全")
_ios("rustdesk_ios", "RustDesk", "rustdesk/rustdesk",
     "https://apps.apple.com/app/rustdesk-remote-desktop/id1581225015", "远程与协作")
_ios("home_assistant_ios", "Home Assistant", "home-assistant/iOS",
     "https://apps.apple.com/app/home-assistant/id1099568401", "智能家居")
_ios("duckduckgo_ios", "DuckDuckGo", "duckduckgo/iOS",
     "https://apps.apple.com/app/duckduckgo-privacy-browser/id663592361", "浏览器")
_ios("thunderbird_ios", "Thunderbird", "thunderbird/thunderbird-ios",
     "https://apps.apple.com/app/thunderbird-email/id6450994832", "通讯")
_ios("obsidian_ios", "Obsidian", "obsidianmd/obsidian-releases",
     "https://apps.apple.com/app/obsidian/id1559035448", "笔记")
_ios("keepass_ios", "KeePassium", "keepassium/KeePassium",
     "https://apps.apple.com/app/keepassium-keepass-password-manager/id1435127111", "安全")
_ios("mastodon_ios", "Mastodon", "mastodon/mastodon",
     "https://apps.apple.com/app/mastodon/id1574080888", "网络")


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for shard, apps in sorted(BATCH.items()):
        plat_dir = "ios" if shard.startswith("99-") else "android"
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
