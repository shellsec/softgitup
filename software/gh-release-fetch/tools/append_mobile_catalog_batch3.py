#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""apps-mobile batch3：按桌面 30 分类大补 Android APK（幂等 append）。"""
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


# --- 01-AI ---
_apk("pocketpal", "01-AI.json", "AI", "AIRetrofit/PocketPal-Android",
     "PocketPal（本地 LLM 聊天，Android）",
     ["PocketPal", "universal", ".apk"],
     ["armeabi", "x86", "debug"])
_apk("mlc_chat", "01-AI.json", "AI", "mlc-ai/mlc-chat-android",
     "MLC Chat（设备端 LLM，Android）",
     ["MLCChat", "android", ".apk"],
     ["x86", "debug"])

# --- 01-工具（扩充既有分片）---
_apk("appmanager", "01-工具.json", "工具", "MuntashirAkon/AppManager",
     "App Manager（应用/权限/组件管理）",
     ["AppManager_v", ".apk"], ["debug"])
_apk("amaze", "01-工具.json", "工具", "TeamAmaze/AmazeFileManager",
     "Amaze File Manager（开源文件管理器）",
     ["app-fdroid-release", ".apk"], ["debug", "lite"])
_apk("droidify", "01-工具.json", "工具", "Droid-ify/client",
     "Droid-ify（F-Droid 客户端）",
     ["app-release", ".apk"], ["debug"])
_apk("neo_store", "01-工具.json", "工具", "NeoApplications/Neo-Store",
     "Neo Store（F-Droid 客户端）",
     ["Neo_Store_", "release.apk"], ["debug"])
_apk("breezy_weather", "01-工具.json", "工具", "breezy-weather/breezy-weather",
     "Breezy Weather（开源天气）",
     ["breezy-weather", "arm64-v8a", "standard.apk"],
     ["armeabi", "x86", "debug", "freenet"])

# --- 03-写作 ---
_apk("gitjournal", "03-写作.json", "写作", "GitJournal/GitJournal",
     "GitJournal（Git 同步日记/写作）",
     ["GitJournal-android", ".apk"], ["debug"])

# --- 04-办公 ---
_apk("wikipedia", "04-办公.json", "办公", "wikimedia/apps-android-wikipedia",
     "Wikipedia（维基百科 Android）",
     ["app-alpha-universal", "release.apk"],
     ["beta", "debug", "test"])
_apk("streetcomplete", "04-办公.json", "办公", "streetcomplete/StreetComplete",
     "StreetComplete（OpenStreetMap 众包编辑）",
     ["StreetComplete-v", ".apk"], ["debug"])

# --- 05-办公与设计 ---
_apk("simple_gallery", "05-办公与设计.json", "办公与设计", "IacobIonut01/Gallery",
     "Gallery（开源相册，ReFra）",
     ["universal-release.apk"], ["offline", "ML", "debug", "armeabi", "x86"])
_apk("simple_calendar", "05-办公与设计.json", "办公与设计", "SimpleMobileTools/Simple-Calendar",
     "Simple Calendar（开源日历）",
     ["calendar-fdroid-release", ".apk"], ["debug", "proprietary"])
_apk("graphene_camera", "05-办公与设计.json", "办公与设计", "GrapheneOS/Camera",
     "GrapheneOS Camera（开源相机）",
     ["Camera-", ".apk"], ["debug"])

# --- 06-命令行 ---
_apk("termux_api", "06-命令行.json", "命令行", "termux/termux-api",
     "Termux:API（Termux 扩展）",
     ["termux-api-app_", ".apk"], ["bootstrap", "debug"])
_apk("termux_widget", "06-命令行.json", "命令行", "termux/termux-widget",
     "Termux:Widget（Termux 桌面小部件）",
     ["termux-widget", ".apk"], ["debug"])

# --- 07-备份 ---
_apk("ente_photos", "07-备份.json", "备份", "ente-io/ente",
     "Ente Photos（端到端加密相册备份）",
     ["ente-", ".apk"], ["locker", "debug"])
_apk("floccus", "07-备份.json", "备份", "floccusaddon/floccus",
     "floccus（浏览器书签同步到 WebDAV/Nextcloud）",
     ["floccus-build-v", ".apk"], ["debug"])

# --- 08-多媒体（桌面同名分片）---
_apk("spotube", "08-多媒体.json", "多媒体", "KRTirtho/spotube",
     "Spotube（跨平台 Spotify 客户端）",
     ["Spotube-android", ".apk"], ["x86", "debug"])
_apk("seal", "08-多媒体.json", "多媒体", "JunkFood02/Seal",
     "Seal（yt-dlp 系 Android 下载器）",
     ["Seal-", "universal", "release.apk"],
     ["armeabi", "arm64-v8a-only", "x86", "debug"])
_apk("smarttube", "08-多媒体.json", "多媒体", "yuliskov/SmartTubeNext",
     "SmartTube（YouTube 第三方 TV/手机客户端）",
     ["SmartTube_stable", "arm64-v8a", ".apk"],
     ["x86", "armeabi", "beta"])
_apk("aniyomi", "08-多媒体.json", "多媒体", "aniyomiorg/aniyomi",
     "Aniyomi（Tachiyomi 系漫画阅读器）",
     ["aniyomi", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])
_apk("mihon", "08-多媒体.json", "多媒体", "mihonapp/mihon",
     "Mihon（Tachiyomi 系漫画阅读器）",
     ["mihon", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])
_apk("organicmaps", "08-多媒体.json", "多媒体", "organicmaps/organicmaps",
     "Organic Maps（离线地图）",
     ["OrganicMaps-", "release.apk"], ["debug", "beta"])

# --- 09-多媒体与设计 ---
_apk("simple_gallery_smt", "09-多媒体与设计.json", "多媒体与设计",
     "SimpleMobileTools/Simple-Gallery",
     "Simple Gallery（SimpleMobileTools 相册）",
     ["gallery-", "foss-release.apk"], ["proprietary", "debug"])

# --- 05-安全（移动既有分片，继续补）---
_apk("signal", "05-安全.json", "安全", "signalapp/Signal-Android",
     "Signal（端到端加密通讯）",
     ["Signal-Android", "universal", "release", ".apk"],
     ["play", "debug", "armeabi", "x86"])
_apk("mullvad", "05-安全.json", "安全", "mullvad/mullvadvpn-app",
     "Mullvad VPN（Android）",
     ["MullvadVPN-", ".apk"], ["debug", "fdroid"])
_apk("proton_mail", "05-安全.json", "安全", "ProtonMail/proton-mail-android",
     "Proton Mail（Android）",
     ["ProtonMail-", ".apk"], ["debug", "beta"])
_apk("proton_vpn", "05-安全.json", "安全", "ProtonVPN/android-app",
     "Proton VPN（Android）",
     ["ProtonVPN-", "production", "release.apk"],
     ["beta", "debug", "fdroid"])
_apk("keepass2android", "05-安全.json", "安全", "PhilippC/keepass2android",
     "KeePass2Android（KeePass 客户端）",
     ["keepass2android", ".apk"], ["debug", "beta"])
_apk("aegis", "05-安全.json", "安全", "AegisAuthenticator/Aegis",
     "Aegis（2FA 验证器）",
     ["Aegis", "release.apk"], ["debug", "fdroid"])
_apk("open_keychain", "05-安全.json", "安全", "open-keychain/open-keychain",
     "OpenKeychain（OpenPGP 密钥管理）",
     ["OpenKeychain", ".apk"], ["debug", "beta"])
_apk("fair_email", "05-安全.json", "安全", "M66B/FairEmail",
     "FairEmail（隐私向邮件客户端）",
     ["FairEmail-v", "github-release.apk"], ["large", "debug"])

# --- 10-安全（桌面同名分片）---
_apk("netguard", "10-安全.json", "安全", "M66B/NetGuard",
     "NetGuard（无 root 防火墙 / 网络监控）",
     ["NetGuard-", "release.apk"], ["debug", "play"])

# --- 11-工具（桌面同名）---
_apk("tasks", "11-工具.json", "工具", "tasks/tasks",
     "Tasks.org（开源待办/效率）",
     ["tasks-fdroid", ".apk"], ["googleplay", "debug"])
_apk("simple_notes", "11-工具.json", "工具", "SimpleMobileTools/Simple-Notes",
     "Simple Notes（SimpleMobileTools 笔记）",
     ["notes-fdroid-release", ".apk"], ["debug"])
_apk("simple_contacts", "11-工具.json", "工具", "SimpleMobileTools/Simple-Contacts",
     "Simple Contacts（SimpleMobileTools 通讯录）",
     ["contacts-fdroid-release", ".apk"], ["debug"])

# --- 12-开发 ---
_apk("acode", "12-开发.json", "开发", "Acode-Foundation/Acode",
     "Acode（Android 代码编辑器）",
     ["app-fdroid", ".apk"], ["debug", "play"])
_apk("siyuan", "12-开发.json", "开发", "siyuan-note/siyuan",
     "SiYuan（本地优先笔记/知识库）",
     ["siyuan-", ".apk"], ["android-arm", "debug"])
_apk("logseq", "12-开发.json", "开发", "logseq/logseq",
     "Logseq（大纲/双链笔记）",
     ["Logseq-android", ".apk"], ["debug"])

# --- 13-效率 ---
_apk("simple_draw", "13-效率.json", "效率", "SimpleMobileTools/Simple-Draw",
     "Simple Draw（轻量绘图/标注）",
     ["draw-fdroid-release", ".apk"], ["debug", "proprietary"])

# --- 14-游戏 ---
_apk("luanti", "14-游戏.json", "游戏", "minetest/minetest",
     "Luanti / Minetest（开源沙盒游戏）",
     ["luanti-", "arm64-v8a", ".apk"], ["armeabi", "x86", "debug"])

# --- 15-笔记 ---
_apk("appflowy", "15-笔记.json", "笔记", "AppFlowy-IO/AppFlowy",
     "AppFlowy（Notion 类笔记，Android）",
     ["AppFlowy-", "android.apk"], ["ios", "debug"])
_apk("joplin", "15-笔记.json", "笔记", "laurent22/joplin-android",
     "Joplin（Markdown 笔记，Android）",
     ["joplin-v", ".apk"], ["debug", "beta"])

# --- 16-系统 ---
_apk("shelter", "16-系统.json", "系统", "PeterCxy/Shelter",
     "Shelter（工作资料隔离/双开）",
     ["Shelter", ".apk"], ["debug"])
_apk("lawnchair", "16-系统.json", "系统", "LawnchairLauncher/lawnchair",
     "Lawnchair（开源启动器）",
     ["Lawnchair", "release.apk"], ["debug", "nightly", "play"])

# --- 17-终端 ---
_apk("connectbot", "17-终端.json", "终端", "connectbot/connectbot",
     "ConnectBot（SSH 客户端）",
     ["ConnectBot-v", "oss.apk"], ["google", "debug"])

# --- 18-网络 ---
_apk("element_x", "18-网络.json", "网络", "element-hq/element-x-android",
     "Element X（Matrix 客户端）",
     [".apk"],
     ["debug", "test", "sources"],
     match_all=False)
_apk("simplex_chat", "18-网络.json", "网络", "simplex-chat/simplex-chat",
     "SimpleX Chat（端到端加密聊天）",
     ["simplex-aarch64", ".apk"], ["armv7", "x86", "debug"])
_apk("nextcloud", "18-网络.json", "网络", "nextcloud/android",
     "Nextcloud（Android 客户端）",
     ["nextcloud-", ".apk"], ["gplay", "debug", "beta"])

# --- 19-网络与协作 ---
_apk("nextcloud_talk", "19-网络与协作.json", "网络与协作", "nextcloud/talk-android",
     "Nextcloud Talk（音视频会议）",
     ["talk-", "release.apk"], ["debug", "beta"])

# --- 20-网络与通讯 ---
_apk("deltachat", "20-网络与通讯.json", "网络与通讯", "deltachat/deltachat-android",
     "Delta Chat（邮件式加密聊天）",
     ["deltachat", "arm64-v8a", ".apk"], ["armeabi", "x86", "debug"])

# --- 21-远程与协作 ---
_apk("rustdesk", "21-远程与协作.json", "远程与协作", "rustdesk/rustdesk",
     "RustDesk（远程桌面 Android 客户端）",
     ["rustdesk-", "aarch64", "signed.apk"],
     ["x86", "armeabi", "unsigned", "debug"])

# --- 22-音视频 ---
_apk("libretube", "22-音视频.json", "音视频", "libre-tube/LibreTube",
     "LibreTube（YouTube 客户端）",
     ["LibreTube", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])

# --- 23-数据库 ---
_apk("cgeo", "23-数据库.json", "数据库", "cgeo/cgeo",
     "c:geo（Geocaching 客户端，含离线 DB）",
     ["cgeo-foss-release", ".apk"], ["google", "debug"])

# --- 24-云原生 ---
_apk("gotify", "24-云原生.json", "云原生", "gotify/android",
     "Gotify（自托管推送通知 Android 客户端）",
     ["gotify-", ".apk"], ["debug"])

# --- 25-可观测 ---
_apk("openhab", "25-可观测.json", "可观测", "openhab/openhab-android",
     "openHAB（智能家居监控与控制）",
     ["openhab-android", ".apk"], ["debug"])

# --- 26-编辑器 ---
_apk("vimtouch", "26-编辑器.json", "编辑器", "vimtouch/vimtouch",
     "VimTouch（Android 上的 Vim）",
     ["VimTouch", ".apk"], ["debug"])

# --- 27-金融与股票 ---
_apk("unstoppable_wallet", "27-金融与股票.json", "金融与股票",
     "horizontalsystems/unstoppable-wallet-android",
     "Unstoppable Wallet（多链加密货币钱包）",
     ["unstoppable_wallet_github", ".apk"], ["google_play", "debug"])

# --- 28-加密货币 ---
_apk("samourai", "28-加密货币.json", "加密货币", "samourai-wallet/samourai-wallet",
     "Samourai Wallet（比特币隐私钱包）",
     ["Samourai", "release.apk"], ["debug", "test"])

# --- 29-局域网文件共享 ---
_apk("localsend", "29-局域网文件共享.json", "局域网文件共享", "localsend/localsend",
     "LocalSend（局域网跨平台文件传输）",
     ["LocalSend-", "android", "aarch64", ".apk"],
     ["arm32", "x86", "windows", "linux", "macos"])

# --- 30-代理与隧道（扩充）---
_apk("hiddify", "30-代理与隧道.json", "代理与隧道", "hiddify/hiddify-next",
     "Hiddify（代理客户端，Android）",
     ["Hiddify-Android-universal", ".apk"],
     ["fdroid", "arm64", "x86", "debug"])
_apk("flclash", "30-代理与隧道.json", "代理与隧道", "chen08209/FlClash",
     "FlClash（Clash 系 Android 客户端）",
     ["FlClash-", "android", "arm64-v8a", ".apk"],
     ["armeabi", "x86", "debug"])
_apk("clash_meta_android", "30-代理与隧道.json", "代理与隧道", "MetaCubeX/ClashMetaForAndroid",
     "Clash Meta for Android",
     ["cmfa-", "universal", "release.apk"],
     ["arm64", "armeabi", "x86", "debug"])
_apk("sagernet", "30-代理与隧道.json", "代理与隧道", "SagerNet/SagerNet",
     "SagerNet（sing-box 系 Android 客户端）",
     ["SN-", "arm64-v8a", ".apk"], ["armeabi", "x86", "debug"])

# --- 06-网络（扩充）---
_apk("owncloud", "06-网络.json", "网络", "owncloud/android",
     "ownCloud（Android 客户端）",
     ["owncloud_", "original-release.apk"], ["debug", "beta"])


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for shard, apps in sorted(BATCH.items()):
        path = os.path.join(MOBILE, "android", shard)
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
