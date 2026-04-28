# -*- coding: utf-8 -*-
"""
大纲缩进：每行统一增加或减少 2 个前导空格（制表符先按 4 列展开）。0 Token、不联网。

运行后输入 1 = 增加缩进，2 = 减少缩进（只动行首空格）。
有选中则处理选中，否则处理全文；可 Ctrl+Z 撤销。
"""

TAB_WIDTH = 4


def _shift_line(line, delta):
    e = line.expandtabs(TAB_WIDTH)
    if delta > 0:
        return (" " * delta) + e
    lead = len(e) - len(e.lstrip(" "))
    rem = min(-delta, lead)
    return e[rem:]


def outline_indent():
    choice = notepad.prompt(
        "1 = 每行前加 2 个空格\n2 = 每行最多去掉 2 个前导空格",
        "大纲缩进",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice == "1":
        delta = 2
    elif choice == "2":
        delta = -2
    else:
        notepad.messageBox("请输入 1 或 2。", "大纲缩进", 0)
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
        notepad.messageBox("没有文本。", "大纲缩进", 0)
        return

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = "\n".join(_shift_line(ln, delta) for ln in lines)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "大纲缩进", 0)


outline_indent()
