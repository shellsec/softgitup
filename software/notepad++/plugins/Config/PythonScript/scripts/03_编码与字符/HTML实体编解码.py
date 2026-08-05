# -*- coding: utf-8 -*-
"""选区 HTML 实体编码 / 解码。"""
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
        notepad.messageBox("请先选中文本。", "HTML实体编解码", 0)
        return
    r = notepad.prompt(
        "1 — 编码（& < > \" '）\n"
        "2 — 解码\n",
        "HTML实体编解码",
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
                raise RuntimeError("无 html / xml.sax 模块")
        elif r == "2":
            if html is not None:
                out = html.unescape(text)
            elif unescape is not None:
                out = unescape(text, {"&quot;": '"', "&#39;": "'"})
            else:
                raise RuntimeError("无 html / xml.sax 模块")
        else:
            notepad.messageBox("请输入 1–2。", "HTML实体编解码", 0)
            return
    except Exception as e:
        notepad.messageBox("失败：\n{}".format(e), "HTML实体编解码", 0)
        return
    editor.beginUndoAction()
    try:
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()


main()
