# -*- coding: utf-8 -*-
"""
在光标处插入 UUID（若有选中则替换选中内容）。可一次插入多行。
1 = 标准带连字符；2 = 32 位十六进制无连字符。标准库，0 Token、不联网。
"""

import uuid


def insert_uuid():
    n_raw = notepad.prompt("要插入几个 UUID？", "插入 UUID", "1")
    if n_raw is None:
        return
    n_raw = (n_raw or "").strip()
    if not n_raw:
        n_raw = "1"
    try:
        n = int(n_raw)
    except ValueError:
        notepad.messageBox("数量无效。", "插入 UUID", 0)
        return
    if n < 1 or n > 500:
        notepad.messageBox("数量须在 1～500 之间。", "插入 UUID", 0)
        return

    mode = notepad.prompt(
        "1 = 标准格式（含连字符）\n2 = 32 位 hex（无连字符）",
        "插入 UUID",
        "1",
    )
    if mode is None:
        return
    mode = mode.strip()
    if mode not in ("1", "2"):
        notepad.messageBox("请输入 1 或 2。", "插入 UUID", 0)
        return

    lines = []
    for _ in range(n):
        u = uuid.uuid4()
        lines.append(str(u) if mode == "1" else u.hex)
    text = "\n".join(lines)

    editor.beginUndoAction()
    try:
        editor.replaceSel(text)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已插入 {} 个 UUID。".format(n), "插入 UUID", 0)


insert_uuid()
