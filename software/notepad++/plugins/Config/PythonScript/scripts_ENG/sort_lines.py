# -*- coding: utf-8 -*-
"""
Sort or dedupe lines in selection or whole document. 0 tokens, no AI.

1 = sort A–Z case-insensitive
2 = natural sort (numbers inside lines)
3 = unique lines, keep first occurrence (order preserved)
"""

import re


def _natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def sort_lines():
    choice = notepad.prompt(
        "1 = Sort (case-insensitive)\n2 = Natural sort (digits)\n3 = Unique lines (keep order)",
        "Sort lines",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2", "3"):
        notepad.messageBox("Enter 1, 2, or 3.", "Sort lines", 0)
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
        notepad.messageBox("No text.", "Sort lines", 0)
        return

    ends_nl = raw.endswith("\n") or raw.endswith("\r\n")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    if choice == "1":
        lines.sort(key=lambda s: s.lower())
    elif choice == "2":
        lines.sort(key=_natural_key)
    else:
        seen = set()
        out = []
        for ln in lines:
            if ln not in seen:
                seen.add(ln)
                out.append(ln)
        lines = out

    body = "\n".join(lines)
    if ends_nl and body and not body.endswith("\n"):
        body += "\n"

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(body)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done.", "Sort lines", 0)


sort_lines()
