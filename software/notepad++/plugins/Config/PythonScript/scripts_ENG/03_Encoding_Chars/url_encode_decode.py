# -*- coding: utf-8 -*-
"""URL-encode / decode selection (UTF-8)."""
try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote


def main():
    text = editor.getSelText()
    if not text:
        notepad.messageBox("Select text first.", "URL encode/decode", 0)
        return
    r = notepad.prompt(
        "1 — Encode (quote, keep /)\n"
        "2 — Encode (quote, including /)\n"
        "3 — Decode (unquote)\n",
        "URL encode/decode",
        "1",
    )
    if r is None:
        return
    r = (r or "").strip()
    try:
        if r == "1":
            out = quote(text, safe="/")
        elif r == "2":
            out = quote(text, safe="")
        elif r == "3":
            out = unquote(text)
        else:
            notepad.messageBox("Enter 1–3.", "URL encode/decode", 0)
            return
    except Exception as e:
        notepad.messageBox("Failed:\n{}".format(e), "URL encode/decode", 0)
        return
    editor.beginUndoAction()
    try:
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()


main()
