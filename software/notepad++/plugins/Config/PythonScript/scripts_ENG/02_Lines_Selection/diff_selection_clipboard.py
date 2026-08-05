# -*- coding: utf-8 -*-
"""Diff selection vs clipboard (unified); insert at cursor or new doc."""
import difflib


def _clipboard_text():
    try:
        import tkinter as tk

        r = tk.Tk()
        r.withdraw()
        try:
            r.attributes("-topmost", True)
        except Exception:
            pass
        r.update()
        try:
            t = r.clipboard_get()
        except Exception:
            t = ""
        r.destroy()
        return t or ""
    except Exception:
        return ""


def main():
    left = editor.getSelText()
    if not left:
        notepad.messageBox("Select text first (left / selection).", "Diff selection↔clipboard", 0)
        return
    right = _clipboard_text()
    if not right:
        notepad.messageBox("Clipboard is empty.", "Diff selection↔clipboard", 0)
        return
    a = left.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    b = right.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    diff = list(
        difflib.unified_diff(a, b, fromfile="selection", tofile="clipboard", lineterm="")
    )
    if not diff:
        notepad.messageBox("Selection and clipboard are identical (line-wise).", "Diff selection↔clipboard", 0)
        return
    body = "\r\n".join(diff) + "\r\n"
    r = notepad.prompt(
        "1 — Insert at cursor\n"
        "2 — Open as new document\n",
        "Diff selection↔clipboard",
        "1",
    )
    if r is None:
        return
    r = (r or "").strip()
    if r == "2":
        notepad.new()
        editor.setText(body)
    elif r == "1":
        editor.insertText(editor.getCurrentPos(), "\r\n" + body)
    else:
        notepad.messageBox("Enter 1 or 2.", "Diff selection↔clipboard", 0)


main()
