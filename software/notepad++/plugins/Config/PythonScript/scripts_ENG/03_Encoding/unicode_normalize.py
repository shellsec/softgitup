# -*- coding: utf-8 -*-
"""
Unicode normalization (unicodedata.normalize). 0 tokens, no AI.

Prompt: 1 = NFC, 2 = NFD, 3 = NFKC, 4 = NFKD
"""

import unicodedata


def unicode_normalize():
    choice = notepad.prompt(
        "1 = NFC (composed)\n2 = NFD (decomposed)\n3 = NFKC\n4 = NFKD",
        "Unicode normalize",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    modes = {"1": "NFC", "2": "NFD", "3": "NFKC", "4": "NFKD"}
    if choice not in modes:
        notepad.messageBox("Enter 1–4.", "Unicode normalize", 0)
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
        notepad.messageBox("No text.", "Unicode normalize", 0)
        return

    out = unicodedata.normalize(mode, raw)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Applied {}.".format(mode), "Unicode normalize", 0)


unicode_normalize()
