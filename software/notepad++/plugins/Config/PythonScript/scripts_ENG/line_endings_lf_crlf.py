# -*- coding: utf-8 -*-
"""
Normalize line endings in selection or whole document. Stdlib only, 0 tokens.

Prompt: 1 = LF only (\\n), 2 = CRLF (\\r\\n). Mixed \\r\\n and lone \\r are normalized first.
"""


def _normalize_to_lf(s):
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    return s


def _to_crlf(s):
    return _normalize_to_lf(s).replace("\n", "\r\n")


def line_endings_lf_crlf():
    choice = notepad.prompt(
        "1 = Use LF only (\\n, Unix style)\n2 = Use CRLF (\\r\\n, Windows style)",
        "Line endings",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("Enter 1 or 2.", "Line endings", 0)
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
        notepad.messageBox("No text.", "Line endings", 0)
        return

    out = _normalize_to_lf(raw) if choice == "1" else _to_crlf(raw)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done.", "Line endings", 0)


line_endings_lf_crlf()
