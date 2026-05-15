# -*- coding: utf-8 -*-
"""
Base64：选中或全文。1 = UTF-8 文本编码为 Base64；2 = Base64 解码为文本（忽略空白）。
标准库，0 Token、不联网。
"""

import base64
import re


def _get_range():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        return sel, editor.getSelectionStart(), editor.getSelectionEnd()
    return editor.getText(), 0, editor.getLength()


def _decode_b64(raw):
    s = re.sub(r"\s+", "", raw)
    if not s:
        raise ValueError("无有效输入")
    pad = (-len(s)) % 4
    if pad:
        s += "=" * pad
    data = base64.b64decode(s)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def base64_selection():
    choice = notepad.prompt(
        "1 = 编码（UTF-8 文本 → Base64）\n2 = 解码（Base64 → 文本）",
        "Base64",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("请输入 1 或 2。", "Base64", 0)
        return

    raw, start, end = _get_range()
    if not raw:
        notepad.messageBox("没有文本。", "Base64", 0)
        return

    try:
        if choice == "1":
            out = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        else:
            out = _decode_b64(raw)
    except Exception as e:
        notepad.messageBox("处理失败：\n{}".format(e), "Base64", 0)
        return

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "Base64", 0)


base64_selection()
