#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""apps-mobile batch6：Android / iOS 尽量全覆盖（薄分类加厚 + 分类占位）。"""
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


def _ios(id, name, repo, url, 分类="占位"):
    _add("99-占位-AppStore.json", [{
        "id": id,
        "简介": f"{name}（iOS · App Store；勿启用 auto_update）",
        "分类": 分类,
        "enabled": False,
        "prefer_api_assets": False,
        "releases_url": url,
        "repo_path": repo,
        "run_installer": False,
        "url_hint": name.lower().split()[0],
    }])


# ========== Android ==========

# 01-AI — pocketpal/mlc/maid 已有

# 04-办公
_apk("libreoffice_viewer", "04-办公.json", "办公", "TéléchargementsLibreOffice/libo-android-config",
     "LibreOffice Viewer（Android 文档查看）",
     ["LibreOffice", "Viewer", ".apk"], ["debug"])

# 04-多媒体（移动分片）
_apk("jellyfin_android", "04-多媒体.json", "多媒体", "jellyfin/jellyfin-android",
     "Jellyfin（Android 客户端）",
     ["jellyfin", "release.apk"], ["debug", "beta"])
_apk("finamp", "04-多媒体.json", "多媒体", "jmshrv/finamp",
     "Finamp（Jellyfin 音乐客户端）",
     ["finamp-", "release.apk"], ["debug"])

# 06-命令行
_apk("android_terminal", "06-命令行.json", "命令行", "JackPal/Android-Terminal-Emulator",
     "Android Terminal Emulator（本地 Shell）",
     ["TerminalEmulator", ".apk"], ["debug"])

# 07-笔记
_apk("standard_notes", "07-笔记.json", "笔记", "standardnotes/mobile",
     "Standard Notes（加密笔记）",
     ["StandardNotes", "release.apk"], ["debug", "beta"])

# 08-输入
_apk("florisboard", "08-输入.json", "输入", "florisboard/florisboard",
     "FlorisBoard（开源键盘）",
     ["FlorisBoard-", "release.apk"], ["debug", "beta"])
_apk("simple_keyboard", "08-输入.json", "输入", "SimpleMobileTools/Simple-Keyboard",
     "Simple Keyboard（SimpleMobileTools 键盘）",
     ["keyboard-fdroid-release", ".apk"], ["debug"])

# 10-浏览器 — fenix 已有；仅补 cromite
_apk("cromite", "10-浏览器.json", "浏览器", "uazo/cromite",
     "Cromite（Chromium 去 Google 化浏览器）",
     ["Cromite", "arm64", ".apk"], ["x86", "armeabi", "debug"])

# 11-工具
_apk("binary_eye", "11-工具.json", "工具", "markusfisch/BinaryEye",
     "Binary Eye（二维码扫描）",
     ["BinaryEye-", "release.apk"], ["debug"])
_apk("fossify_calculator", "11-工具.json", "工具", "FossifyOrg/Calculator",
     "Fossify Calculator（计算器）",
     ["calculator-", "release.apk"], ["debug"])
_apk("fossify_clock", "11-工具.json", "工具", "FossifyOrg/Clock",
     "Fossify Clock（时钟/闹钟）",
     ["clock-", "release.apk"], ["debug"])
_apk("fossify_messages", "11-工具.json", "工具", "FossifyOrg/Messages",
     "Fossify Messages（短信）",
     ["messages-", "release.apk"], ["debug"])

# 12-开发
_apk("mgit", "12-开发.json", "开发", "maksim-korotkov/MGit",
     "MGit（Android Git 客户端）",
     ["MGit-", "release.apk"], ["debug"])

# 14-游戏
_apk("lemuroid", "14-游戏.json", "游戏", "Swordfish90/Lemuroid",
     "Lemuroid（模拟器前端）",
     ["lemuroid-", "release.apk"], ["debug"])
_apk("scummvm", "14-游戏.json", "游戏", "scummvm/scummvm",
     "ScummVM（经典游戏引擎）",
     ["scummvm", "android", ".apk"], ["debug", "win", "linux", "macos"])

# 16-系统
_apk("insular", "16-系统.json", "系统", "oberon/Insular",
     "Insular（工作资料隔离）",
     ["Insular-", "release.apk"], ["debug"])
_apk("app_ops", "16-系统.json", "系统", "RikkaApps/App-Ops-reborn",
     "App Ops（权限/Ops 管理）",
     ["AppOps", "release.apk"], ["debug"])

# 17-终端
_apk("termux_widget", "17-终端.json", "终端", "termux/termux-widget",
     "Termux:Widget（终端小部件）",
     ["termux-widget", ".apk"], ["debug"])

# 08-多媒体
_apk("innertune", "08-多媒体.json", "多媒体", "z-huang/InnerTune",
     "InnerTune（YouTube Music 第三方）",
     ["InnerTune-", "release.apk"], ["debug"])
_apk("antennapod", "08-多媒体.json", "多媒体", "AntennaPod/AntennaPod",
     "AntennaPod（播客客户端）",
     ["AntennaPod-", "release.apk"], ["debug", "free"])
_apk("musicolet", "08-多媒体.json", "多媒体", "krosbits/Musicolet",
     "Musicolet（离线音乐播放器）",
     ["Musicolet", ".apk"], ["debug"])

# 18-网络
_apk("mattermost", "18-网络.json", "网络", "mattermost/mattermost-mobile",
     "Mattermost（团队聊天）",
     ["Mattermost", "release.apk"], ["debug"])
_apk("rocketchat", "18-网络.json", "网络", "RocketChat/Rocket.Chat.ReactNative",
     "Rocket.Chat（团队聊天）",
     ["Rocket.Chat", "release.apk"], ["debug"])

# 19-网络与协作
_apk("davx5", "19-网络与协作.json", "网络与协作", "bitfireAT/davx5",
     "DAVx5（CalDAV/CardDAV 同步）",
     ["davx5-", "release.apk"], ["debug"])

# 21-远程 — rustdesk / hop_to_desk 已有

# 22-音视频 — libretube 已有

# 23-数据库
_apk("andotp", "23-数据库.json", "数据库", "andOTP/andOTP",
     "andOTP（2FA · 含备份导出）",
     ["andOTP-", "release.apk"], ["debug"])

# 24-云原生
_apk("netbird", "24-云原生.json", "云原生", "netbirdio/netbird",
     "NetBird（WireGuard 组网 · 含 Android 客户端）",
     ["netbird", "android", ".apk"], ["linux", "windows", "darwin", "debug"])

# 25-可观测
_apk("netx", "25-可观测.json", "可观测", "ryochan7/NetX",
     "NetX（网络扫描/诊断）",
     ["NetX-", "release.apk"], ["debug"])

# 26-编辑器
_apk("helio_editor", "26-编辑器.json", "编辑器", "helio-editor/HelioEditor",
     "Helio Editor（音乐创作）",
     ["Helio", "release.apk"], ["debug"])

# 27-金融
_apk("green_wallet", "27-金融与股票.json", "金融与股票", "Blockstream/green_android",
     "Green（Blockstream 比特币钱包）",
     ["green", "release.apk"], ["debug"])

# 28-加密货币
_apk("monerujo", "28-加密货币.json", "加密货币", "monerujo-io/monerujo",
     "Monerujo（Monero 钱包）",
     ["monerujo", "release.apk"], ["debug"])
_apk("schildbach_wallet", "28-加密货币.json", "加密货币", "bitcoin-wallet/bitcoin-wallet",
     "Bitcoin Wallet（Schildbach）",
     ["bitcoin-wallet", "release.apk"], ["debug"])

# 29-局域网 — localsend 已有

# 30-代理
_apk("nekobox", "30-代理与隧道.json", "代理与隧道", "MatsuriDayo/NekoBoxForAndroid",
     "NekoBox（sing-box 系 Android 客户端）",
     ["NekoBox", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])
_apk("clash_for_android", "30-代理与隧道.json", "代理与隧道", "Kr328/ClashForAndroid",
     "Clash for Android（已归档 · 仍可下载历史 Release）",
     ["cfa-", "arm64-v8a", ".apk"], ["x86", "armeabi", "debug"])

# 02-下载
_apk("upgradeall", "02-下载.json", "下载", "DUpdate/UpgradeAll",
     "UpgradeAll（多源应用更新追踪）",
     ["UpgradeAll-", "release.apk"], ["debug"])

# 05-安全
_apk("rethink_dns", "05-安全.json", "安全", "rethinkhealth/rethink-app",
     "Rethink DNS + Firewall（DNS/防火墙）",
     ["rethink", "release.apk"], ["debug"])

# 10-安全
_apk("dns66", "10-安全.json", "安全", "julian-klode/dns66",
     "DNS66（ hosts 广告拦截 · 项目已归档）",
     ["dns66", ".apk"], ["debug"])

# 05-办公与设计
_apk("fossify_music", "05-办公与设计.json", "办公与设计", "FossifyOrg/Music-Player",
     "Fossify Music Player（音乐播放器）",
     ["music-", "release.apk"], ["debug"])

# 06-网络
_apk("wireguard_android", "06-网络.json", "网络", "WireGuard/wireguard-android",
     "WireGuard（Android VPN 客户端）",
     ["wireguard", "release.apk"], ["debug"])

# 09-通讯 — deltachat 见 20-网络与通讯

# 11-智能家居 — home_assistant / domoticz 已有

# 01-工具

# 15-笔记 — siyuan 见 12-开发

# 20-网络与通讯 — simplex 见 18-网络

# 03-写作
_apk("einkbro", "03-写作.json", "写作", "plateaukao/einkbro",
     "EinkBro（轻量浏览器/阅读）",
     ["EinkBro-", "release.apk"], ["debug"])

# 07-备份
_apk("proton_drive", "07-备份.json", "备份", "ProtonMail/proton-drive-android",
     "Proton Drive（端到端加密云盘 Android）",
     ["ProtonDrive", "release.apk"], ["debug"])

# 13-效率
_apk("habitica", "13-效率.json", "效率", "HabitRPG/habitica-android",
     "Habitica（习惯 RPG 待办）",
     ["Habitica", "release.apk"], ["debug"])

# 15-笔记
_apk("notally", "15-笔记.json", "笔记", "c0de517/notally",
     "Notally（极简笔记）",
     ["Notally-", "release.apk"], ["debug"])

# 21-远程与协作
_apk("unified_remote", "21-远程与协作.json", "远程与协作", "UnifiedRemote/Droid",
     "Unified Remote（通用远程控制）",
     ["UnifiedRemote", "release.apk"], ["debug"])

# 22-音视频
_apk("skytube", "22-音视频.json", "音视频", "SkyTubeApp/SkyTube",
     "SkyTube（YouTube 客户端 · 开源）",
     ["SkyTube", "release.apk"], ["debug"])

# 01-工具
_apk("datamonitor", "01-工具.json", "工具", "itsdrill/DataMonitor",
     "DataMonitor（流量监控）",
     ["DataMonitor-", "release.apk"], ["debug"])

# ========== iOS App Store 占位（按分类尽量对齐）==========
_ios("chatgpt_ios", "ChatGPT", "openai/chatgpt-ios",
     "https://apps.apple.com/app/openai-chatgpt/id6448311069", "AI")
_ios("github_ios", "GitHub", "github/github",
     "https://apps.apple.com/app/github/id1477622338", "开发")
_ios("gitlab_ios", "GitLab", "gitlabhq/gitlabhq",
     "https://apps.apple.com/app/gitlab/id1274972321", "开发")
_ios("notion_ios", "Notion", "makenotion/notion",
     "https://apps.apple.com/app/notion/id1232780281", "笔记")
_ios("organic_maps_ios", "Organic Maps", "organicmaps/organicmaps",
     "https://apps.apple.com/app/organic-maps-offline-hiking/id1567431693", "多媒体")
_ios("osmand_ios", "OsmAnd", "osmandapp/OsmAnd",
     "https://apps.apple.com/app/osmand-maps-travel/id934488856", "多媒体")
_ios("outline_ios", "Outline", "Jigsaw-Code/outline-apps",
     "https://apps.apple.com/app/outline-secure-internet-access/id1356176944", "代理与隧道")
_ios("wireguard_ios", "WireGuard", "WireGuard/wireguard-apple",
     "https://apps.apple.com/app/wireguard/id1441195209", "网络")
_ios("localsend_ios", "LocalSend", "localsend/localsend",
     "https://apps.apple.com/app/localsend/id1661733228", "局域网文件共享")
_ios("brave_ios", "Brave", "brave/brave-ios",
     "https://apps.apple.com/app/brave-private-web-browser-vpn/id1052879175", "浏览器")
_ios("telegram_ios", "Telegram", "TelegramMessenger/Telegram-iOS",
     "https://apps.apple.com/app/telegram-messenger/id686449807", "通讯")
_ios("delta_chat_ios", "Delta Chat", "deltachat/deltachat-ios",
     "https://apps.apple.com/app/delta-chat/id971034419", "通讯")
_ios("tutanota_ios", "Tuta Mail", "tutao/tutanota",
     "https://apps.apple.com/app/tuta-mail/id922558369", "安全")
_ios("protonpass_ios", "Proton Pass", "ProtonMail/proton-pass-ios",
     "https://apps.apple.com/app/proton-pass-password-manager/id6443492969", "安全")
_ios("working_copy_ios", "Working Copy", "WorkingCopyApp/WorkingCopy",
     "https://apps.apple.com/app/working-copy-git-client/id896694807", "开发")
_ios("infuse_ios", "Infuse", "firecore/infuse",
     "https://apps.apple.com/app/infuse/id550519732", "多媒体")
_ios("spotify_ios", "Spotify", "spotify/ios",
     "https://apps.apple.com/app/spotify-music-and-podcasts/id324684580", "多媒体")
_ios("1password_ios", "1Password", "1Password/1Password",
     "https://apps.apple.com/app/1password-password-manager/id1511601750", "安全")
_ios("microsoft_rd_ios", "Microsoft Remote Desktop", "microsoft/remote-desktop",
     "https://apps.apple.com/app/microsoft-remote-desktop/id714464147", "远程与协作")
_ios("mattermost_ios", "Mattermost", "mattermost/mattermost-mobile",
     "https://apps.apple.com/app/mattermost/id1252497129", "网络与协作")
_ios("jitsi_ios", "Jitsi Meet", "jitsi/jitsi-meet",
     "https://apps.apple.com/app/jitsi-meet/id1165103905", "网络与协作")
_ios("standard_notes_ios", "Standard Notes", "standardnotes/mobile",
     "https://apps.apple.com/app/standard-notes/id1533652021", "笔记")
_ios("ente_ios", "Ente Photos", "ente-io/ente",
     "https://apps.apple.com/app/ente-photos/id1542026908", "备份")
_ios("bluewallet_ios", "BlueWallet", "BlueWallet/BlueWallet",
     "https://apps.apple.com/app/bluewallet-bitcoin-wallet/id1376878040", "加密货币")
_ios("shadowrocket_ios", "Shadowrocket", "2dust/v2rayNG",
     "https://apps.apple.com/app/shadowrocket/id932747118", "代理与隧道")
_ios("ppsspp_ios", "PPSSPP", "hrydgard/ppsspp",
     "https://apps.apple.com/app/ppsspp-psp-emulator/id407294374", "游戏")
_ios("hop_to_desk_ios", "HopToDesk", "HopToDesk/HopToDesk",
     "https://apps.apple.com/app/hoptodesk/id6449253059", "远程与协作")
_ios("ish_ios", "iSH", "ish-app/ish",
     "https://apps.apple.com/app/ish-shell/id1442740726", "终端")
_ios("altstore_ios", "AltStore", "altstoreio/AltStore",
     "https://apps.apple.com/app/altstore/id1520648649", "下载")
_ios("nextplayer_ios", "Next Player", "anilbeesetti/nextplayer",
     "https://apps.apple.com/app/next-player/id6443565993", "多媒体")
_ios("nipaplay_ios", "NipaPlay", "MCDFsteve/NipaPlay-Reload",
     "https://apps.apple.com/app/nipaplay/id6738942356", "多媒体")
_ios("mpv_ios", "mpv", "mpv-android/mpv-android",
     "https://apps.apple.com/app/mpv/id6443670749", "多媒体")


def main():
    # 去掉无效 iOS 占位
    ios = BATCH.get("99-占位-AppStore.json", [])
    BATCH["99-占位-AppStore.json"] = [
        a for a in ios
        if not a.get("releases_url", "").rstrip("/").endswith("/app")
    ]

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
