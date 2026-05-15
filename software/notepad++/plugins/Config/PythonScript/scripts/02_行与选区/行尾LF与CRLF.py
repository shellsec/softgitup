# -*- coding: utf-8 -*-
"""
行尾换行符：选中或全文。1 = 统一为 LF（\\n）；2 = 统一为 CRLF（\\r\\n）。
先将 \\r\\n 与单独 \\r 规范为 \\n，再按需转为 CRLF。0 Token、不联网。
"""


def _normalize_to_lf(s):
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    return s


def _to_crlf(s):
    return _normalize_to_lf(s).replace("\n", "\r\n")


def line_endings_lf_crlf():
    choice = notepad.prompt(
        "1 = 仅 LF（\\n，类 Unix）\n2 = CRLF（\\r\\n，Windows）",
        "行尾换行符",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("请输入 1 或 2。", "行尾换行符", 0)
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
        notepad.messageBox("没有文本。", "行尾换行符", 0)
        return

    out = _normalize_to_lf(raw) if choice == "1" else _to_crlf(raw)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "行尾换行符", 0)


line_endings_lf_crlf()
