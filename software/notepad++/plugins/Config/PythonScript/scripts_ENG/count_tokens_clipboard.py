# -*- coding: utf-8 -*-
"""
Count tokens (EN/CJK mixed) — clipboard gets 5-line stats; dialog shows full notes.
Uses tiktoken cl100k_base / o200k_base when available; else heuristic.
No selection = entire document.
"""

import re
import sys


def _copy_to_clipboard_ctypes_unicode(text):
    """Windows: write CF_UNICODETEXT (UTF-16 LE). Avoids clip.exe ANSI/UTF-8 mojibake."""
    import ctypes
    from ctypes import wintypes

    if not isinstance(text, str):
        text = text.decode("utf-8", errors="replace") if isinstance(text, bytes) else str(text)

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002

    if not user32.OpenClipboard(None):
        return False
    try:
        if not user32.EmptyClipboard():
            return False
        raw = text.encode("utf-16-le") + b"\x00\x00"
        n = len(raw)
        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, n)
        if not h_mem:
            return False
        p = kernel32.GlobalLock(h_mem)
        if not p:
            kernel32.GlobalFree(h_mem)
            return False
        try:
            ctypes.memmove(p, raw, n)
        finally:
            kernel32.GlobalUnlock(h_mem)
        if not user32.SetClipboardData(CF_UNICODETEXT, h_mem):
            kernel32.GlobalFree(h_mem)
            return False
        return True
    finally:
        user32.CloseClipboard()


def _copy_to_clipboard(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")

    if sys.platform == "win32":
        try:
            if _copy_to_clipboard_ctypes_unicode(text):
                return True
        except Exception:
            pass
        try:
            import win32clipboard

            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                if hasattr(win32clipboard, "SetClipboardText"):
                    win32clipboard.SetClipboardText(text)
                else:
                    import win32con

                    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
                return True
            finally:
                win32clipboard.CloseClipboard()
        except Exception:
            pass

    try:
        import tkinter

        r = tkinter.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()
        return True
    except Exception:
        pass

    return False


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


def count_tokens_to_clipboard():
    text, scope = _get_scope_text()
    if not text:
        notepad.messageBox("No text to count.", "Token count (clipboard)", 0)
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

    clip_ok = _copy_to_clipboard(report_brief)
    if clip_ok:
        report_popup += "\n\n(Copied the 5-line summary to clipboard.)"
    else:
        report_popup += "\n\n(Clipboard copy failed.)"

    notepad.messageBox(report_popup, "Token count (clipboard)", 0)


count_tokens_to_clipboard()
