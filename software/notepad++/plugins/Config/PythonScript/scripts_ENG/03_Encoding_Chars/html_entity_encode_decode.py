# -*- coding: utf-8 -*-
"""HTML-entity encode / decode selection."""
try:
    import html
except ImportError:
    html = None
    try:
        from xml.sax.saxutils import escape, unescape
    except ImportError:
        escape = unescape = None


def main():
    text = editor.getSelText()
    if not text:
        notepad.messageBox("Select text first.", "HTML entities", 0)
        return
    r = notepad.prompt(
        "1 — Encode (& < > \" ')\n"
        "2 — Decode\n",
        "HTML entities",
        "1",
    )
    if r is None:
        return
    r = (r or "").strip()
    try:
        if r == "1":
            if html is not None:
                out = html.escape(text, quote=True)
            elif escape is not None:
                out = escape(text, {'"': "&quot;", "'": "&#39;"})
            else:
                raise RuntimeError("html / xml.sax unavailable")
        elif r == "2":
            if html is not None:
                out = html.unescape(text)
            elif unescape is not None:
                out = unescape(text, {"&quot;": '"', "&#39;": "'"})
            else:
                raise RuntimeError("html / xml.sax unavailable")
        else:
            notepad.messageBox("Enter 1–2.", "HTML entities", 0)
            return
    except Exception as e:
        notepad.messageBox("Failed:\n{}".format(e), "HTML entities", 0)
        return
    editor.beginUndoAction()
    try:
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()


main()
