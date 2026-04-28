# -*- coding: utf-8 -*-
"""
Insert UUID(s) at cursor (or replace selection). Stdlib only, 0 tokens.

Prompts: count (default 1), then 1 = standard with hyphens, 2 = 32 hex chars (no hyphens).
"""

import uuid


def insert_uuid():
    n_raw = notepad.prompt("How many UUIDs to insert?", "Insert UUID", "1")
    if n_raw is None:
        return
    n_raw = (n_raw or "").strip()
    if not n_raw:
        n_raw = "1"
    try:
        n = int(n_raw)
    except ValueError:
        notepad.messageBox("Invalid count.", "Insert UUID", 0)
        return
    if n < 1 or n > 500:
        notepad.messageBox("Count must be between 1 and 500.", "Insert UUID", 0)
        return

    mode = notepad.prompt(
        "1 = Standard (with hyphens)\n2 = 32 hex characters (no hyphens)",
        "Insert UUID",
        "1",
    )
    if mode is None:
        return
    mode = mode.strip()
    if mode not in ("1", "2"):
        notepad.messageBox("Enter 1 or 2.", "Insert UUID", 0)
        return

    lines = []
    for _ in range(n):
        u = uuid.uuid4()
        lines.append(str(u) if mode == "1" else u.hex)
    text = "\n".join(lines)

    editor.beginUndoAction()
    try:
        editor.replaceSel(text)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Inserted {} UUID(s).".format(n), "Insert UUID", 0)


insert_uuid()
