# -*- coding: utf-8 -*-
"""
行排序或去重：1=字母序（忽略大小写）2=自然序（数字按数值）3=去重保留首次出现。0 Token。
"""

import re


def _natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def sort_lines():
    choice = notepad.prompt(
        "1 = 排序（忽略大小写）\n2 = 自然排序（行内数字）\n3 = 去重（保留首次出现顺序）",
        "行排序去重",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2", "3"):
        notepad.messageBox("请输入 1、2 或 3。", "行排序去重", 0)
        return

    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    if not raw:
        notepad.messageBox("没有文本。", "行排序去重", 0)
        return

    ends_nl = raw.endswith("\n") or raw.endswith("\r\n")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    if choice == "1":
        lines.sort(key=lambda s: s.lower())
    elif choice == "2":
        lines.sort(key=_natural_key)
    else:
        seen = set()
        out = []
        for ln in lines:
            if ln not in seen:
                seen.add(ln)
                out.append(ln)
        lines = out

    body = "\n".join(lines)
    if ends_nl and body and not body.endswith("\n"):
        body += "\n"

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(body)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "行排序去重", 0)


sort_lines()
