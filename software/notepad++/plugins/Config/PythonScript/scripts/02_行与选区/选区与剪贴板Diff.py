# -*- coding: utf-8 -*-
"""对比选区与剪贴板（行级：仅左/仅右/相同），结果插入光标处或新文档。"""
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
        notepad.messageBox("请先选中作为「左侧/选区」的文本。", "选区与剪贴板Diff", 0)
        return
    right = _clipboard_text()
    if not right:
        notepad.messageBox("剪贴板为空。", "选区与剪贴板Diff", 0)
        return
    a = left.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    b = right.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    diff = list(
        difflib.unified_diff(a, b, fromfile="selection", tofile="clipboard", lineterm="")
    )
    if not diff:
        notepad.messageBox("选区与剪贴板相同（按行比较）。", "选区与剪贴板Diff", 0)
        return
    body = "\r\n".join(diff) + "\r\n"
    r = notepad.prompt(
        "1 — 插入到当前光标\n"
        "2 — 打开为新文档\n",
        "选区与剪贴板Diff",
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
        notepad.messageBox("请输入 1 或 2。", "选区与剪贴板Diff", 0)


main()
