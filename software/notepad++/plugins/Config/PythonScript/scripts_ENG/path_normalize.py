# -*- coding: utf-8 -*-
"""
Normalize path slashes in selection or document. 0 tokens, no AI.

Prompt: 1 = forward slashes /, 2 = backslashes \\ (Windows style).
"""

def path_normalize():
    choice = notepad.prompt(
        "1 = Use forward slashes /\n2 = Use backslashes \\\\",
        "Path normalize",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("Enter 1 or 2.", "Path normalize", 0)
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
        notepad.messageBox("No text.", "Path normalize", 0)
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

    notepad.messageBox("Done.", "Path normalize", 0)


path_normalize()
