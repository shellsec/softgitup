#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""将 apps/windows/99-未匹配-windows分片.json 按分类拆入各分片。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIN = os.path.join(ROOT, "apps", "windows")
SRC = os.path.join(WIN, "99-未匹配-windows分片.json")

# id -> (shard_file, 分类名)
ASSIGN: dict[str, tuple[str, str]] = {
    # 02 下载
    "qbittorrent_enhanced_edition": ("02-下载.json", "下载"),
    "downzemall": ("02-下载.json", "下载"),
    "hitomi_downloader": ("02-下载.json", "下载"),
    "ydl_ui": ("02-下载.json", "下载"),
    "liii_bittorrent_client": ("02-下载.json", "下载"),
    "file_centipede": ("02-下载.json", "下载"),
    "m3u8_downloader": ("02-下载.json", "下载"),
    "youtube_downloader_gui": ("02-下载.json", "下载"),
    "persepolis_download_manager": ("02-下载.json", "下载"),
    # 03 写作
    "sigil": ("03-写作.json", "写作"),
    "koodo_reader": ("03-写作.json", "写作"),
    "thorium_reader": ("03-写作.json", "写作"),
    "boostnote": ("03-写作.json", "写作"),
    # 04 办公
    "office_tool_plus": ("04-办公.json", "办公"),
    # 08 多媒体
    "xmanager": ("08-多媒体.json", "多媒体"),
    "ffmpeg_batch_av_converter": ("08-多媒体.json", "多媒体"),
    "tag_editor": ("08-多媒体.json", "多媒体"),
    "fastflix": ("08-多媒体.json", "多媒体"),
    "spek": ("08-多媒体.json", "多媒体"),
    "mpc_be": ("08-多媒体.json", "多媒体"),
    "qmplay2": ("08-多媒体.json", "多媒体"),
    "mixxx": ("08-多媒体.json", "多媒体"),
    "notenoughav1encodes": ("08-多媒体.json", "多媒体"),
    "volumey": ("08-多媒体.json", "多媒体"),
    "musicplayer2": ("08-多媒体.json", "多媒体"),
    "cine_encoder": ("08-多媒体.json", "多媒体"),
    "batchencoder": ("08-多媒体.json", "多媒体"),
    # 09 多媒体与设计
    "mrv2": ("09-多媒体与设计.json", "多媒体与设计"),
    "upscayl": ("09-多媒体与设计.json", "多媒体与设计"),
    "makehuman": ("09-多媒体与设计.json", "多媒体与设计"),
    "waifu2x_gui": ("09-多媒体与设计.json", "多媒体与设计"),
    "waifu2x_extension_gui": ("09-多媒体与设计.json", "多媒体与设计"),
    "superpng": ("09-多媒体与设计.json", "多媒体与设计"),
    # 10 安全
    "tinywall": ("10-安全.json", "安全"),
    "fort_firewall": ("10-安全.json", "安全"),
    "passliss": ("10-安全.json", "安全"),
    "keeweb": ("10-安全.json", "安全"),
    "buttercup": ("10-安全.json", "安全"),
    # 11 工具
    "flyphotos": ("11-工具.json", "工具"),
    "oncepower": ("11-工具.json", "工具"),
    "nanazip": ("11-工具.json", "工具"),
    "colorpicker": ("11-工具.json", "工具"),
    "imagine_compression": ("11-工具.json", "工具"),
    "openhashtab": ("11-工具.json", "工具"),
    "hashing": ("11-工具.json", "工具"),
    "quick_picture_viewer": ("11-工具.json", "工具"),
    "pineapple_picture": ("11-工具.json", "工具"),
    # 12 开发
    "jpexs_flash_decompiler": ("12-开发.json", "开发"),
    "ultimate_packer_for_executables": ("12-开发.json", "开发"),
    "pe_bear": ("12-开发.json", "开发"),
    "dnspy": ("12-开发.json", "开发"),
    "codeblocks": ("12-开发.json", "开发"),
    "net_reactor_slayer": ("12-开发.json", "开发"),
    # 13 效率
    "powertoys_2": ("13-效率.json", "效率"),
    "maye": ("13-效率.json", "效率"),
    "copytranslator": ("13-效率.json", "效率"),
    "quickclipboard": ("13-效率.json", "效率"),
    "flameshot": ("13-效率.json", "效率"),
    "ksnip": ("13-效率.json", "效率"),
    "screenote": ("13-效率.json", "效率"),
    "blinkmind": ("13-效率.json", "效率"),
    # 14 游戏
    "dosbox_x": ("14-游戏.json", "游戏"),
    "ruffle": ("14-游戏.json", "游戏"),
    "sudokusolver": ("14-游戏.json", "游戏"),
    "visualboyadvance_m": ("14-游戏.json", "游戏"),
    "ryujinx_2": ("14-游戏.json", "游戏"),
    "punes": ("14-游戏.json", "游戏"),
    "my_nes": ("14-游戏.json", "游戏"),
    # 15 笔记
    "cherrytree": ("15-笔记.json", "笔记"),
    "trilium_notes": ("15-笔记.json", "笔记"),
    "notesnook": ("15-笔记.json", "笔记"),
    "beaver_notes": ("15-笔记.json", "笔记"),
    "pinny_notes": ("15-笔记.json", "笔记"),
    "desktopnote": ("15-笔记.json", "笔记"),
    "crypto_notepad": ("15-笔记.json", "笔记"),
    # 16 系统
    "sucrose_wallpaper_engine": ("16-系统.json", "系统"),
    "fan_control": ("16-系统.json", "系统"),
    "optimizerduck": ("16-系统.json", "系统"),
    "nwinfo": ("16-系统.json", "系统"),
    "lightbulb": ("16-系统.json", "系统"),
    "efi_boot_editor": ("16-系统.json", "系统"),
    "fedora_media_writer": ("16-系统.json", "系统"),
    "wsl_manager": ("16-系统.json", "系统"),
    "winslop": ("16-系统.json", "系统"),
    "auto_dark_mode": ("16-系统.json", "系统"),
    "whynotwin11": ("16-系统.json", "系统"),
    "lively_wallpaper": ("16-系统.json", "系统"),
    "windynamicdesktop": ("16-系统.json", "系统"),
    "total_registry": ("16-系统.json", "系统"),
    "optimizer": ("16-系统.json", "系统"),
    "sophiapp": ("16-系统.json", "系统"),
    "context_menu_manager": ("16-系统.json", "系统"),
    "dreamscene2": ("16-系统.json", "系统"),
    "pid_key_checker": ("16-系统.json", "系统"),
    "nsudo": ("16-系统.json", "系统"),
    # 17 终端
    "putty": ("17-终端.json", "终端"),
    "xterminal": ("17-终端.json", "终端"),
    "nxshell": ("17-终端.json", "终端"),
    # 18 网络
    "internettest": ("18-网络.json", "网络"),
    "opentrace": ("18-网络.json", "网络"),
    # 20 网络与通讯
    "thunderbird_2": ("20-网络与通讯.json", "网络与通讯"),
    # 21 远程与协作
    "escrcpy": ("21-远程与协作.json", "远程与协作"),
    # 22 音视频
    "screen_to_gif": ("22-音视频.json", "音视频"),
    "simple_screen_recorder": ("22-音视频.json", "音视频"),
    "quickcut": ("22-音视频.json", "音视频"),
    # 23 数据库
    "sqlitestudio": ("23-数据库.json", "数据库"),
    # 26 编辑器
    "notepad_next": ("26-编辑器.json", "编辑器"),
    "akelpad": ("26-编辑器.json", "编辑器"),
    "cudatext": ("26-编辑器.json", "编辑器"),
    "atom_editor": ("26-编辑器.json", "编辑器"),
    # 29 局域网文件共享
    "nocab_desktop": ("29-局域网文件共享.json", "局域网文件共享"),
    "synctrayzor": ("29-局域网文件共享.json", "局域网文件共享"),
}


def main():
    dry = "--dry-run" in sys.argv
    with open(SRC, encoding="utf-8") as f:
        items = json.load(f)

    by_shard: dict[str, list] = {}
    leftover: list = []
    missing_map: list[str] = []

    for app in items:
        aid = app.get("id", "")
        if aid in ASSIGN:
            shard, cat = ASSIGN[aid]
            entry = dict(app)
            entry["分类"] = cat
            by_shard.setdefault(shard, []).append(entry)
        else:
            missing_map.append(aid)
            leftover.append(app)

    if missing_map:
        print("未映射 id:", missing_map)
        raise SystemExit(1)

    for shard, apps in sorted(by_shard.items()):
        path = os.path.join(WIN, shard)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        seen = {(a.get("id") or "").strip() for a in data}
        add = 0
        for app in apps:
            if app["id"] in seen:
                print("skip duplicate", app["id"], "in", shard)
                continue
            data.append(app)
            add += 1
        print(f"{shard}: +{add} (total {len(data)})")
        if not dry:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")

    if not dry:
        with open(SRC, "w", encoding="utf-8") as f:
            json.dump(leftover, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"cleared {SRC}, leftover {len(leftover)}")
    else:
        print(f"dry-run: would move {sum(len(v) for v in by_shard.values())}, leftover {len(leftover)}")


if __name__ == "__main__":
    main()
