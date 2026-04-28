# -*- coding: utf-8 -*-
"""
统计中英文混合 Token — 剪贴板仅五项统计；弹窗含完整说明。
优先 tiktoken（cl100k_base / o200k_base）；未安装时用近似算法。
无选中则统计全文。
"""

import re
import sys


def _copy_to_clipboard_ctypes_unicode(text):
    """Windows：以 CF_UNICODETEXT（UTF-16 LE）写入剪贴板，避免 clip 按 ANSI/错误编码解码导致乱码。"""
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
        return sel, "选中区域"
    return editor.getText(), "全文"


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
        notepad.messageBox("没有可统计的内容。", "Token 统计（剪贴板）", 0)
        return

    try:
        n = _count_with_tiktoken(text, "cl100k_base")
        method = "tiktoken"
        encoding_used = "cl100k_base（GPT-3.5 / GPT-4 系）"
    except Exception:
        try:
            n = _count_with_tiktoken(text, "o200k_base")
            method = "tiktoken"
            encoding_used = "o200k_base（GPT-4o 系）"
        except Exception:
            n = _approx_tokens(text)
            method = "近似估算"
            encoding_used = "启发式（安装 tiktoken 可得到与 API 一致的精确值）"

    chars = len(text)
    utf8_bytes = len(text.encode("utf-8"))
    lines = text.count("\n") + 1 if text else 0

    report_brief = (
        "范围：{scope}\n"
        "字符数：{chars}\n"
        "UTF-8 字节：{utf8}\n"
        "行数（按换行）：{lines}\n"
        "Token 数：{n}"
    ).format(
        scope=scope,
        chars=chars,
        utf8=utf8_bytes,
        lines=lines,
        n=n,
    )

    report_popup = (
        "{brief}\n\n"
        "方式：{method}\n"
        "编码：{enc}\n\n"
        "说明：英文与中文使用同一分词器统计；"
        "cl100k / o200k 与 OpenAI 接口计费粒度一致。"
    ).format(
        brief=report_brief,
        method=method,
        enc=encoding_used,
    )

    if method == "近似估算":
        report_popup += "\n\n安装：pip install tiktoken（需对 PythonScript 所用的 Python 执行）。"

    clip_ok = _copy_to_clipboard(report_brief)
    if clip_ok:
        report_popup += "\n\n（已将上述五项统计复制到剪贴板。）"
    else:
        report_popup += "\n\n（剪贴板复制失败。）"

    notepad.messageBox(report_popup, "Token 统计（剪贴板）", 0)


count_tokens_to_clipboard()
