# -*- coding: utf-8 -*-
"""选区 URL 编码 / 解码（UTF-8）。"""
try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote


def main():
    text = editor.getSelText()
    if not text:
        notepad.messageBox("请先选中文本。", "URL编解码", 0)
        return
    r = notepad.prompt(
        "1 — 编码（quote，保留 /）\n"
        "2 — 编码（quote，含 /）\n"
        "3 — 解码（unquote）\n",
        "URL编解码",
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
            notepad.messageBox("请输入 1–3。", "URL编解码", 0)
            return
    except Exception as e:
        notepad.messageBox("失败：\n{}".format(e), "URL编解码", 0)
        return
    editor.beginUndoAction()
    try:
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()


main()
