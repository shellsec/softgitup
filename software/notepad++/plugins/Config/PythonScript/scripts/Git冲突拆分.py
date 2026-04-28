# -*- coding: utf-8 -*-
"""
将 Git 冲突标记 <<<<<<< … ======= … >>>>>>> 拆成 OURS / THEIRS 分段（多块按序输出）。0 Token。
"""


def _extract_blocks(text):
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = []
    pos = 0
    while True:
        a = t.find("<<<<<<<", pos)
        if a < 0:
            break
        nl0 = t.find("\n", a)
        if nl0 < 0:
            break
        sep = "\n=======\n"
        b = t.find(sep, nl0)
        if b < 0:
            break
        ours = t[nl0 + 1 : b]
        c = t.find("\n>>>>>>>", b)
        if c < 0:
            break
        theirs = t[b + len(sep) : c]
        blocks.append((ours, theirs))
        nl1 = t.find("\n", c)
        pos = nl1 + 1 if nl1 >= 0 else len(t)
    return blocks


def git_conflict_split():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    if not raw.strip():
        notepad.messageBox("没有文本。", "Git 冲突拆分", 0)
        return

    blocks = _extract_blocks(raw)
    if not blocks:
        notepad.messageBox("未找到 <<<<<<< … ======= … >>>>>>> 块。", "Git 冲突拆分", 0)
        return

    parts = []
    for i, (ours, theirs) in enumerate(blocks, 1):
        parts.append("========== 当前(OURS) #{} ==========".format(i))
        parts.append(ours.rstrip("\n"))
        parts.append("")
        parts.append("========== 对方(THEIRS) #{} ==========".format(i))
        parts.append(theirs.rstrip("\n"))
        parts.append("")
    out = "\n".join(parts).rstrip() + "\n"

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已拆分 {} 处冲突块。".format(len(blocks)), "Git 冲突拆分", 0)


git_conflict_split()
