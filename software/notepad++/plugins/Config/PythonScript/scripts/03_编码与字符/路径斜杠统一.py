# -*- coding: utf-8 -*-
"""
路径斜杠统一：选中或全文。1 = 正斜杠 /，2 = 反斜杠 \\。0 Token、不联网。
"""


def path_normalize():
    choice = notepad.prompt(
        "1 = 统一为正斜杠 /\n2 = 统一为反斜杠 \\",
        "路径斜杠",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("请输入 1 或 2。", "路径斜杠", 0)
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
        notepad.messageBox("没有文本。", "路径斜杠", 0)
        return

    if choice == "2":
        out = raw.replace("/", "\\")
    else:
        out = raw.replace("\\", "/")

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "路径斜杠", 0)


path_normalize()
