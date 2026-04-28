# -*- coding: utf-8 -*-
"""
选择「含 TXT 的目录」与「保存 MD 的目录」，递归将所有 .txt 转为 .md（UTF-8）。
保持相对路径。无需 pip。

优先 tkinter；若无 tkinter，在 Windows 下用 PowerShell + WinForms（需同目录 folder_dialog_win.py）。
"""

import os
import sys

_sd = os.path.dirname(os.path.abspath(__file__))
if _sd not in sys.path:
    sys.path.insert(0, _sd)

try:
    from folder_dialog_win import ask_directory
except ImportError:
    ask_directory = None


def _read_text(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fp:
                return fp.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as fp:
        return fp.read()


def _pick_folders():
    if ask_directory is None:
        notepad.messageBox(
            "未找到与本脚本同目录的 folder_dialog_win.py。",
            "批量 TXT 转 Markdown",
            0,
        )
        return None, None
    inp = ask_directory("选择包含 TXT 的目录")
    if not inp:
        return None, None
    outp = ask_directory("选择保存 Markdown 的目录")
    if not outp:
        return None, None
    return os.path.normpath(inp), os.path.normpath(outp)


def batch_txt_to_md():
    inp, outp = _pick_folders()
    if inp is None:
        return

    inp = os.path.normpath(os.path.expanduser(str(inp).strip()))
    outp = os.path.normpath(os.path.expanduser(str(outp).strip()))
    if not os.path.isdir(inp):
        notepad.messageBox(
            "输入路径不是有效文件夹：\n{}".format(inp),
            "批量 TXT 转 Markdown",
            0,
        )
        return

    if os.path.normcase(os.path.normpath(inp)) == os.path.normcase(os.path.normpath(outp)):
        notepad.messageBox("输入目录与输出目录不能相同。", "批量 TXT 转 Markdown", 0)
        return

    ok = 0
    errors = []

    for base, _dirs, files in os.walk(inp):
        for name in files:
            if not name.lower().endswith(".txt"):
                continue
            src = os.path.join(base, name)
            rel = os.path.relpath(src, inp)
            dst_rel = os.path.splitext(rel)[0] + ".md"
            dst = os.path.join(outp, dst_rel)
            try:
                text = _read_text(src)
                parent = os.path.dirname(dst)
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent, exist_ok=True)
                with open(dst, "w", encoding="utf-8", newline="\n") as fp:
                    fp.write(text)
                ok += 1
            except Exception as e:
                errors.append("{}: {}".format(rel, e))

    msg = "已转换 {} 个 .txt 为 .md。".format(ok)
    if errors:
        msg += "\n\n失败（{} 处）：\n".format(len(errors))
        msg += "\n".join(errors[:15])
        if len(errors) > 15:
            msg += "\n..."
    if ok == 0 and not errors:
        msg = (
            "在所选输入目录（含子文件夹）下未发现扩展名为 .txt 的文件。\n\n"
            "已扫描的根目录：\n{}\n\n"
            "请核对：\n"
            "· 是否选对了「含 TXT 的根文件夹」（不是上一级或空文件夹）；\n"
            "· 资源管理器若隐藏已知扩展名，列出的「xxx.txt」可能是别的类型，"
            "请在「查看」中勾选「文件扩展名」后确认真实后缀；\n"
            "· 仅匹配 .txt / .TXT，不含 .text、.log、无扩展名等。"
        ).format(inp)

    notepad.messageBox(msg, "批量 TXT 转 Markdown", 0)


batch_txt_to_md()
