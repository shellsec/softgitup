# -*- coding: utf-8 -*-
"""
Markdown 任务列表 [ ] <-> [x] 切换。匹配 - * + 或 1. 开头。0 Token。
"""

import re

_PAT_SPACE = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)\[ \](\s|$)")
_PAT_X = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)\[[xX]\](\s|$)")


def _toggle_line(ln):
    if _PAT_SPACE.match(ln):
        return _PAT_SPACE.sub(r"\1[x]\2", ln, count=1)
    if _PAT_X.match(ln):
        return _PAT_X.sub(r"\1[ ]\2", ln, count=1)
    return ln


def todo_toggle():
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
        notepad.messageBox("没有文本。", "待办切换", 0)
        return

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = "\n".join(_toggle_line(ln) for ln in lines)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "待办切换", 0)


todo_toggle()
