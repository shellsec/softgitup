#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A 类 GitHub 监控列表补全：soft_page_check 中尚未入库的 owner/repo。"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
MOBILE = os.path.join(ROOT, "apps-mobile")

BATCH: dict[tuple[str, str], list] = {}
MOBILE_BATCH: dict[str, list] = {}


def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


def _madd(shard: str, apps: list):
    MOBILE_BATCH.setdefault(shard, []).extend(apps)


def _b(**kw):
    d = {
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "windows_installer": False,
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
        "use_download_filename": True,
        "href_exclude_substrings": [
            "source", "src.", "-src", "symbols", "debug", "pdb",
            "sha256", ".sig", ".json", ".txt", ".md", "checksum",
        ],
    }
    d.update(kw)
    return d


def _repo(repo: str) -> dict:
    return {
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
    }


def _slug(repo: str) -> str:
    name = repo.split("/")[-1]
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()
    return s or "app"


def _desk(
    repo: str,
    shard: str,
    分类: str,
    简介: str,
    *,
    id: str | None = None,
    plats=("windows", "linux", "darwin"),
    **cfg,
):
    aid = id or _slug(repo)
    for p in plats:
        _add(p, shard, [{"id": aid, "简介": 简介, "分类": 分类, **_b(**cfg), **_repo(repo)}])


def _win(repo, shard, 分类, 简介, **cfg):
    _desk(repo, shard, 分类, 简介, plats=("windows",), **cfg)


def _apk(repo, shard, 分类, 简介, markers, exclude=None, **cfg):
    _madd(shard, [{
        "id": _slug(repo),
        "简介": 简介,
        "分类": 分类,
        **_b(
            installer_markers_match_all=True,
            installer_markers=markers,
            href_exclude_substrings=(exclude or [])
            + [".aab", "debug", "test", "unsigned", "sources"],
            installer_extensions=[".apk"],
            save_name=f"{_slug(repo)}.apk",
            **cfg,
        ),
        **_repo(repo),
    }])


# --- 多媒体 / 下载 ---
_win(
    "youhunwl/TVAPP", "08-多媒体.json", "多媒体",
    "TVAPP（Android TV 应用聚合/安装器）",
    installer_extensions=[".apk"],
)
_win(
    "gyc-12/Cymusic", "08-多媒体.json", "多媒体",
    "Cymusic（第三方音乐客户端）",
)
_desk(
    "lyswhut/lx-music-desktop", "08-多媒体.json", "多媒体",
    "洛雪音乐助手（桌面版）",
    id="lx_music_desktop",
    installer_markers_match_all=True,
    installer_markers=["win_x64"],
    href_exclude_substrings=["arm", "macos", "linux", "ia32", "source"],
    installer_extensions=[".7z", ".exe"],
)
_apk(
    "lyswhut/lx-music-mobile", "08-多媒体.json", "多媒体",
    "洛雪音乐（Android）",
    ["lx-music-mobile", "arm64", ".apk"],
    ["x86", "universal"],
)
_desk(
    "listen1/listen1_desktop", "08-多媒体.json", "多媒体",
    "Listen 1（聚合音乐播放器）",
    id="listen1_desktop",
)
_win(
    "listen1/listen1_chrome_extension", "08-多媒体.json", "多媒体",
    "Listen 1（Chrome 扩展 crx 包，仅下载）",
    id="listen1_chrome_ext",
    installer_extensions=[".crx", ".zip"],
)
_apk(
    "listen1/listen1_mobile", "08-多媒体.json", "多媒体",
    "Listen 1（Android）",
    ["listen1", ".apk"],
)
_win(
    "XiaoYouChR/Ghost-Downloader-3", "02-下载.json", "下载",
    "Ghost Downloader 3（多线程下载器）",
    id="ghost_downloader_3",
)
_win(
    "neatgz/PotPlayer_OneKey_Tool", "08-多媒体.json", "多媒体",
    "PotPlayer 一键配置工具",
    id="potplayer_onekey",
)
_win(
    "hooke007/mpv_PlayKit", "08-多媒体.json", "多媒体",
    "mpv PlayKit（PotPlayer/MPV 脚本套件）",
    id="mpv_playkit",
    installer_extensions=[".zip", ".7z"],
)
_desk(
    "koel/player", "08-多媒体.json", "多媒体",
    "Koel（自托管音乐播放器）",
    plats=("linux", "darwin"),
)
_win(
    "Richasy/Bili.Copilot", "08-多媒体.json", "多媒体",
    "Bili Copilot（B 站助手）",
    id="bili_copilot",
)
_win(
    "sjshb57/NewLcgR", "08-多媒体.json", "多媒体",
    "NewLcgR",
)

# --- 笔记 / 写作 ---
_desk(
    "codexu/note-gen", "15-笔记.json", "笔记",
    "NoteGen（AI 笔记生成）",
    id="note_gen",
)
_desk(
    "drl990114/MarkFlowy", "15-笔记.json", "笔记",
    "MarkFlowy（Markdown 笔记）",
    id="markflowy",
)
_desk(
    "flyhunterl/flymd", "03-写作.json", "写作",
    "flymd（Markdown 编辑器）",
    id="flymd",
)
_desk(
    "doocs/md", "03-写作.json", "写作",
    "doocs/md（Markdown 编辑器）",
    id="doocs_md",
)
_desk(
    "KDE/ghostwriter", "03-写作.json", "写作",
    "ghostwriter（KDE Markdown 编辑器）",
    id="ghostwriter",
    plats=("linux", "darwin"),
)
_desk(
    "vnotex/vnote", "15-笔记.json", "笔记",
    "VNote（Markdown 笔记）",
    id="vnote",
)
_win(
    "windingwind/zotero-better-notes", "15-笔记.json", "笔记",
    "Zotero Better Notes（插件 Release）",
    id="zotero_better_notes",
    installer_extensions=[".xpi", ".zip"],
)

# --- 编辑器 ---
_desk(
    "zufuliu/notepad4", "26-编辑器.json", "编辑器",
    "Notepad4（Notepad2 分支）",
    id="notepad4",
    plats=("windows",),
)
_desk(
    "markdown-it/markdown-it", "26-编辑器.json", "编辑器",
    "markdown-it（JS 库 Release，非安装包）",
    id="markdown_it",
    prefer_api_assets=True,
    installer_extensions=[".tgz", ".zip"],
)

# --- 输入法 ---
_win(
    "rime/weasel", "26-编辑器.json", "编辑器",
    "小狼毫 Weasel（Windows Rime 输入法）",
    id="weasel",
    installer_markers_match_all=True,
    installer_markers=["weasel", "installer"],
    installer_extensions=[".exe"],
    windows_installer=True,
    run_installer=True,
)
_win(
    "studyzy/imewlconverter", "11-工具.json", "工具",
    "imewlconverter（词库转换）",
    id="imewlconverter",
)
_win(
    "iDvel/rime-ice", "11-工具.json", "工具",
    "rime-ice（雾凇拼音词库，Release 资源包）",
    id="rime_ice",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "huanfeng/WindInput", "26-编辑器.json", "编辑器",
    "WindInput（Windows 输入法）",
    id="wind_input",
)

# --- 数据库 ---
_win(
    "HeidiSQL/HeidiSQL", "23-数据库.json", "数据库",
    "HeidiSQL（MySQL/MariaDB 客户端）",
    id="heidisql",
    installer_markers=["HeidiSQL_", "Setup.exe"],
    installer_extensions=[".exe"],
    windows_installer=True,
    run_installer=True,
)
_win(
    "tiny-craft/tiny-rdm", "23-数据库.json", "数据库",
    "Tiny RDM（Redis 桌面客户端）",
    id="tiny_rdm",
)
_win(
    "lework/RedisDesktopManager-Windows", "23-数据库.json", "数据库",
    "RedisDesktopManager-Windows",
    id="redis_desktop_manager_win",
)
_win(
    "moshowgame/dbeaver-driver-all", "23-数据库.json", "数据库",
    "DBeaver 全量驱动包",
    id="dbeaver_driver_all",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "wgzhao/dbeaver-agent", "23-数据库.json", "数据库",
    "dbeaver-agent（DBeaver 插件包）",
    id="dbeaver_agent",
    installer_extensions=[".jar", ".zip"],
)
_win(
    "shellsec/navicat_for_mac_reset", "23-数据库.json", "数据库",
    "navicat_for_mac_reset（脚本/工具 Release）",
    id="navicat_mac_reset",
    installer_extensions=[".zip", ".sh", ".command"],
)

# --- 远程 / 终端 ---
_desk(
    "rustdesk/rustdesk-server", "21-远程与协作.json", "远程与协作",
    "RustDesk Server（hbbs/hbbr）",
    id="rustdesk_server",
    installer_markers_match_all=True,
    installer_markers=["rustdesk-server"],
    href_exclude_substrings=["client", "android", "ios"],
)
_win(
    "GMYXDS/MstscManager", "21-远程与协作.json", "远程与协作",
    "MstscManager（远程桌面管理）",
    id="mstsc_manager",
)
_desk(
    "TermoraDev/termora", "17-终端.json", "终端",
    "Termora（终端/SSH 客户端）",
    id="termora",
)
_win(
    "TheBlindM/T-Shell", "17-终端.json", "终端",
    "T-Shell（Windows 终端工具）",
    id="t_shell",
)
_win(
    "wzsx150/MobaXterm_CN", "21-远程与协作.json", "远程与协作",
    "MobaXterm 中文语言包",
    id="mobaxterm_cn",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "RipplePiam/MobaXterm-Chinese-Simplified", "21-远程与协作.json", "远程与协作",
    "MobaXterm 简体中文补丁",
    id="mobaxterm_zh_patch",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "zarfadev/MobaXterm-Keygen", "21-远程与协作.json", "远程与协作",
    "MobaXterm-Keygen",
    id="mobaxterm_keygen",
)

# --- 系统 ---
_win(
    "IgorMundstein/WinMemoryCleaner", "16-系统.json", "系统",
    "WinMemoryCleaner（内存清理）",
    id="win_memory_cleaner",
)
_win(
    "memstechtips/Winhance", "16-系统.json", "系统",
    "Winhance（Windows 优化脚本套件）",
    id="winhance",
    installer_markers=["Get.ps1", ".ps1"],
    installer_extensions=[".ps1", ".zip"],
)
_win(
    "henrypp/memreduct", "16-系统.json", "系统",
    "Mem Reduct（内存优化）",
    id="memreduct",
    installer_markers=["memreduct", "setup"],
    installer_extensions=[".exe"],
)
_win(
    "Raphire/Win11Debloat", "16-系统.json", "系统",
    "Win11Debloat（系统精简脚本，Release 为 Get.ps1）",
    id="win11_debloat",
    installer_markers=["Get.ps1"],
    installer_extensions=[".ps1", ".zip"],
)
_win(
    "scavin/Win11Debloat", "16-系统.json", "系统",
    "Win11Debloat（scavin  fork）",
    id="win11_debloat_scavin",
    installer_markers=["Get.ps1"],
    installer_extensions=[".ps1", ".zip"],
)
_win(
    "ionuttbara/windows-defender-remover", "16-系统.json", "系统",
    "Windows Defender Remover",
    id="defender_remover",
    installer_extensions=[".exe", ".zip", ".7z"],
)
_win(
    "choyy/VirtualDesktopSwitcher", "16-系统.json", "系统",
    "VirtualDesktopSwitcher（虚拟桌面切换）",
    id="virtual_desktop_switcher",
)
_win(
    "Runixe786/MD3-Windows", "16-系统.json", "系统",
    "MD3-Windows（Material Design 3 主题/工具）",
    id="md3_windows",
)
_win(
    "NixaVulpi/MonitorBrightnessAdjuster", "16-系统.json", "系统",
    "MonitorBrightnessAdjuster",
    id="monitor_brightness_adjuster",
)
_desk(
    "anfragment/zen", "16-系统.json", "系统",
    "Zen Browser（旧仓库 anfragment/zen；新上游 irbis-sh/zen-desktop）",
    id="zen_browser_legacy",
    plats=("windows", "linux", "darwin"),
)

# --- 工具 / 效率 ---
_win(
    "fzxx/FlashErase", "11-工具.json", "工具",
    "FlashErase",
    id="flash_erase",
)
_win(
    "fzxx/FileImgSwap", "11-工具.json", "工具",
    "FileImgSwap",
    id="file_img_swap",
)
_win(
    "fzxx/XiangYue", "11-工具.json", "工具",
    "XiangYue",
    id="xiang_yue",
)
_win(
    "fzxx/NaughtyDamagePack", "14-游戏.json", "游戏",
    "NaughtyDamagePack",
    id="naughty_damage_pack",
)
_desk(
    "bleachbit/bleachbit", "11-工具.json", "工具",
    "BleachBit（系统清理）",
    id="bleachbit",
)
_win(
    "Jeric-X/SyncClipboard", "11-工具.json", "工具",
    "SyncClipboard（剪贴板同步）",
    id="sync_clipboard",
)
_win(
    "sabrogden/Ditto", "11-工具.json", "工具",
    "Ditto（剪贴板管理）",
    id="ditto",
    installer_markers=["Ditto", "bit", ".exe"],
    installer_extensions=[".exe", ".zip"],
)
_desk(
    "crosspaste/crosspaste-desktop", "11-工具.json", "工具",
    "CrossPaste（跨设备剪贴板）",
    id="crosspaste",
)
_win(
    "PasteBar/PasteBarApp", "11-工具.json", "工具",
    "PasteBar（剪贴板历史）",
    id="pastebar",
)
_win(
    "taojy123/KeymouseGo", "11-工具.json", "工具",
    "KeymouseGo（键鼠宏录制）",
    id="keymouse_go",
)
_win(
    "majorworld/MousePlus", "11-工具.json", "工具",
    "MousePlus（鼠标增强）",
    id="mouse_plus",
)
_desk(
    "super-productivity/super-productivity", "13-效率.json", "效率",
    "Super Productivity（任务/番茄钟）",
    id="super_productivity",
)
_desk(
    "Splode/pomotroid", "13-效率.json", "效率",
    "Pomotroid（番茄钟）",
    id="pomotroid",
)
_win(
    "Open-Less/openless", "11-工具.json", "工具",
    "OpenLess",
    id="openless",
)
_win(
    "Qwejay/QphotoRenamer", "11-工具.json", "工具",
    "QphotoRenamer（批量重命名）",
    id="qphoto_renamer",
)
_win(
    "jd1378/otphelper", "11-工具.json", "工具",
    "OTP Helper（2FA 工具）",
    id="otp_helper",
)
_win(
    "LC044/AnnualReport", "11-工具.json", "工具",
    "AnnualReport（年度报告生成）",
    id="annual_report",
)
_win(
    "trustdev-org/calendar-diary", "13-效率.json", "效率",
    "Calendar Diary",
    id="calendar_diary",
)
_desk(
    "anufrievroman/calcure", "13-效率.json", "效率",
    "calcure（TUI 日历/任务）",
    id="calcure",
    plats=("linux", "darwin"),
)
_win(
    "Snouzy/workout-cool", "13-效率.json", "效率",
    "workout-cool",
    id="workout_cool",
)
_win(
    "aoguai/LiYing", "11-工具.json", "工具",
    "LiYing",
    id="li_ying",
)
_win(
    "TNT-Likely/BeeCount", "11-工具.json", "工具",
    "BeeCount",
    id="bee_count",
)

# --- 安全 / 沙箱 / 激活类（监控列表全量入库，默认 disabled）---
_win(
    "sandboxie-plus/Sandboxie", "10-安全.json", "安全",
    "Sandboxie Plus（沙箱）",
    id="sandboxie_plus",
    installer_markers=["Sandboxie-Plus", "win", "x64"],
    installer_extensions=[".exe"],
)
_win(
    "wecooperate/iMonitor", "10-安全.json", "安全",
    "iMonitor（EDR/监控）",
    id="imonitor",
)
_win(
    "zbezj/HEU_KMS_Activator", "10-安全.json", "安全",
    "HEU KMS Activator",
    id="heu_kms",
    installer_extensions=[".zip", ".7z", ".exe"],
)
_win(
    "massgravel/Microsoft-Activation-Scripts", "10-安全.json", "安全",
    "Microsoft Activation Scripts",
    id="mas_scripts",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "QiuChenly/InjectLib", "10-安全.json", "安全",
    "InjectLib",
    id="inject_lib",
    installer_extensions=[".zip", ".7z"],
)
_win(
    "shellsec/RDS_Grace_Period_Reset", "10-安全.json", "安全",
    "RDS Grace Period Reset",
    id="rds_grace_reset",
)

# --- 微信相关 ---
_win(
    "afaa1991/BetterWX-UI", "20-网络与通讯.json", "网络与通讯",
    "BetterWX-UI",
    id="betterwx_ui",
)
_win(
    "huiyadanli/RevokeMsgPatcher", "20-网络与通讯.json", "网络与通讯",
    "RevokeMsgPatcher（防撤回补丁）",
    id="revoke_msg_patcher",
)
_win(
    "TC999/WeChatMsg", "20-网络与通讯.json", "网络与通讯",
    "WeChatMsg（微信聊天记录导出）",
    id="wechat_msg",
)

# --- 网络 / 文件共享 ---
_desk(
    "drakkan/sftpgo", "29-局域网文件共享.json", "局域网文件共享",
    "SFTPGo（SFTP/WebDAV 文件服务）",
    id="sftpgo",
)
_desk(
    "MatrixSeven/file-transfer-go", "29-局域网文件共享.json", "局域网文件共享",
    "file-transfer-go",
    id="file_transfer_go",
)
_desk(
    "terreng/simple-web-server", "18-网络.json", "网络",
    "Simple Web Server",
    id="simple_web_server",
)
_desk(
    "9001/copyparty", "29-局域网文件共享.json", "局域网文件共享",
    "copyparty（文件共享 Web UI）",
    id="copyparty",
)

# --- 开发 ---
_desk(
    "xtool-org/xtool", "12-开发.json", "开发",
    "xtool（Xcode 命令行工具链辅助）",
    id="xtool",
    plats=("darwin",),
)
_win(
    "ashi876/Laxuhub", "12-开发.json", "开发",
    "Laxuhub",
    id="laxuhub",
)
_win(
    "shellsec/softgitup", "12-开发.json", "开发",
    "softgitup",
    id="softgitup",
)

# --- 卸载 / 维护 ---
_win(
    "Klocman/Bulk-Crap-Uninstaller", "16-系统.json", "系统",
    "Bulk Crap Uninstaller（BCUninstaller）",
    id="bcuninstaller",
    installer_markers=["BCUninstaller_", "setup"],
    installer_extensions=[".exe"],
)

# --- 网络管理 ---
_desk(
    "BornToBeRoot/NETworkManager", "18-网络.json", "网络",
    "NETworkManager（网络诊断工具集）",
    id="network_manager",
    plats=("windows",),
)

# --- escrcpy fork ---
_win(
    "Mu-L/escrcpy", "21-远程与协作.json", "远程与协作",
    "escrcpy（Mu-L fork；主清单为 viarotel-org/escrcpy）",
    id="escrcpy_mu_l",
)


def _load_existing(plat: str, mobile: bool = False) -> tuple[set[str], set[str]]:
    base = MOBILE if mobile else APPS
    sub = "android" if mobile else plat
    ids: set[str] = set()
    repos: set[str] = set()
    d = os.path.join(base, sub)
    if not os.path.isdir(d):
        return ids, repos
    for fn in os.listdir(d):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(d, fn), encoding="utf-8") as f:
            for item in json.load(f):
                if not isinstance(item, dict):
                    continue
                if item.get("id"):
                    ids.add(item["id"].strip())
                if item.get("repo_path"):
                    repos.add(item["repo_path"].lower())
    return ids, repos


def _merge_desktop(dry: bool) -> tuple[int, int]:
    added = skipped = 0
    plat_cache: dict[str, tuple[set[str], set[str]]] = {}
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        if plat not in plat_cache:
            plat_cache[plat] = _load_existing(plat, mobile=False)
        seen_ids, seen_repos = plat_cache[plat]
        file_ids = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
        for app in apps:
            rp = (app.get("repo_path") or "").lower()
            aid = (app.get("id") or "").strip()
            if rp in seen_repos or aid in seen_ids or aid in file_ids:
                skipped += 1
                continue
            data.append(app)
            seen_ids.add(aid)
            seen_repos.add(rp)
            file_ids.add(aid)
            added += 1
        if not dry:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"Wrote {path} ({len(data)} entries)")
    return added, skipped


def _merge_mobile(dry: bool) -> tuple[int, int]:
    added = skipped = 0
    seen_ids, seen_repos = _load_existing("android", mobile=True)
    for shard, apps in sorted(MOBILE_BATCH.items()):
        path = os.path.join(MOBILE, "android", shard)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        file_ids = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
        for app in apps:
            rp = (app.get("repo_path") or "").lower()
            aid = (app.get("id") or "").strip()
            if rp in seen_repos or aid in seen_ids or aid in file_ids:
                skipped += 1
                continue
            data.append(app)
            seen_ids.add(aid)
            seen_repos.add(rp)
            file_ids.add(aid)
            added += 1
        if not dry:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            print(f"Wrote {path} ({len(data)} entries)")
    return added, skipped


def main():
    dry = "--dry-run" in sys.argv
    a1, s1 = _merge_desktop(dry)
    a2, s2 = _merge_mobile(dry)
    print(f"{'dry-run' if dry else 'done'}: desktop +{a1} skip {s1}, mobile +{a2} skip {s2}")


if __name__ == "__main__":
    main()
