# -*- coding: utf-8 -*-
"""
Count tokens (EN/CJK mixed) — insert 5-line stats at cursor; dialog shows full notes.
Uses tiktoken cl100k_base / o200k_base when available; else heuristic.
No selection = entire document.
"""

import re


def _get_scope_text():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        return sel, "selection"
    return editor.getText(), "full document"


def _approx_tokens(text):
    if not text:
        return 0
    cjk = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]", text))
    non_cjk = max(0, len(text) - cjk)
    return int(non_cjk / 4.0 + cjk / 1.5 + 0.999)


def _count_with_tiktoken(text, encoding_name):
    import tiktoken

    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


def count_tokens_insert():
    text, scope = _get_scope_text()
    if not text:
        notepad.messageBox("No text to count.", "Token count (insert)", 0)
        return

    try:
        n = _count_with_tiktoken(text, "cl100k_base")
        method = "tiktoken"
        encoding_used = "cl100k_base (GPT-3.5 / GPT-4 class)"
    except Exception:
        try:
            n = _count_with_tiktoken(text, "o200k_base")
            method = "tiktoken"
            encoding_used = "o200k_base (GPT-4o class)"
        except Exception:
            n = _approx_tokens(text)
            method = "approximate"
            encoding_used = "heuristic (install tiktoken for accurate counts)"

    chars = len(text)
    utf8_bytes = len(text.encode("utf-8"))
    lines = text.count("\n") + 1 if text else 0

    report_brief = (
        "Scope: {scope}\n"
        "Characters: {chars}\n"
        "UTF-8 bytes: {utf8}\n"
        "Lines (by newline): {lines}\n"
        "Tokens: {n}"
    ).format(
        scope=scope,
        chars=chars,
        utf8=utf8_bytes,
        lines=lines,
        n=n,
    )

    report_popup = (
        "{brief}\n\n"
        "Method: {method}\n"
        "Encoding: {enc}\n\n"
        "Note: English and Chinese use the same tokenizer; "
        "cl100k/o200k match OpenAI API tokenization."
    ).format(
        brief=report_brief,
        method=method,
        enc=encoding_used,
    )

    if method == "approximate":
        report_popup += "\n\nInstall: pip install tiktoken (use the same Python as PythonScript)."

    pos = editor.getCurrentPos()
    prefix = "\n" if pos > 0 else ""
    block = prefix + report_brief + "\n"
    editor.beginUndoAction()
    try:
        editor.insertText(pos, block)
    finally:
        editor.endUndoAction()

    report_popup += "\n\n(Inserted the 5-line summary at the cursor.)"
    notepad.messageBox(report_popup, "Token count (insert)", 0)


count_tokens_insert()
