# -*- coding: utf-8 -*-
"""
Base64 encode/decode on selection or whole document. Stdlib only, 0 tokens.

Prompt: 1 = encode (UTF-8 -> Base64 ASCII), 2 = decode (whitespace stripped).
"""

import base64
import re


def _get_range():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        return sel, editor.getSelectionStart(), editor.getSelectionEnd()
    return editor.getText(), 0, editor.getLength()


def _decode_b64(raw):
    s = re.sub(r"\s+", "", raw)
    if not s:
        raise ValueError("empty input")
    pad = (-len(s)) % 4
    if pad:
        s += "=" * pad
    data = base64.b64decode(s)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def base64_selection():
    choice = notepad.prompt(
        "1 = Encode (UTF-8 text to Base64)\n2 = Decode (Base64 to text)",
        "Base64",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice not in ("1", "2"):
        notepad.messageBox("Enter 1 or 2.", "Base64", 0)
        return

    raw, start, end = _get_range()
    if not raw:
        notepad.messageBox("No text.", "Base64", 0)
        return

    try:
        if choice == "1":
            out = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        else:
            out = _decode_b64(raw)
    except Exception as e:
        notepad.messageBox("Failed:\n{}".format(e), "Base64", 0)
        return

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done.", "Base64", 0)


base64_selection()
