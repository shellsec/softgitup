# -*- coding: utf-8 -*-
"""
Shift outline indent by 2 spaces per line (tabs expanded first). 0 tokens, no AI.

Prompt: 1 = indent (+2), 2 = outdent (-2, only leading spaces).
Selection or whole document; supports undo.
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
        "1 = Add 2 leading spaces per line\n2 = Remove up to 2 leading spaces per line",
        "Outline indent",
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
        notepad.messageBox('Enter 1 or 2 only.', "Outline indent", 0)
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
        notepad.messageBox("No text.", "Outline indent", 0)
        return

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = "\n".join(_shift_line(ln, delta) for ln in lines)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done.", "Outline indent", 0)


outline_indent()
