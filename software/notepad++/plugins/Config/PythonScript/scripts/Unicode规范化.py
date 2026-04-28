# -*- coding: utf-8 -*-
"""
Unicode 规范化（unicodedata.normalize）。1=NFC 2=NFD 3=NFKC 4=NFKD。0 Token。
"""

import unicodedata


def unicode_normalize():
    choice = notepad.prompt(
        "1 = NFC（组合）\n2 = NFD（分解）\n3 = NFKC\n4 = NFKD",
        "Unicode 规范化",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    modes = {"1": "NFC", "2": "NFD", "3": "NFKC", "4": "NFKD"}
    if choice not in modes:
        notepad.messageBox("请输入 1～4。", "Unicode 规范化", 0)
        return
    mode = modes[choice]

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
        notepad.messageBox("没有文本。", "Unicode 规范化", 0)
        return

    out = unicodedata.normalize(mode, raw)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已应用 {}。".format(mode), "Unicode 规范化", 0)


unicode_normalize()
