# -*- coding: utf-8 -*-
"""
将选中或全文中的 CSV/TSV 转为 Markdown 管道表格。0 Token、不联网。
制表符多于逗号则按 Tab 分隔，否则按逗号；使用 csv 模块处理引号。
"""

import csv
import io


def _detect_delim(s):
    return "\t" if s.count("\t") > s.count(",") else ","


def _escape_cell(c):
    return (c or "").replace("|", "\\|").replace("\n", " ")


def _to_md_table(text, delim):
    text = text.lstrip("\ufeff")
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    rows = [r for r in reader if any(x.strip() for x in r)]
    if not rows:
        return None
    width = max(len(r) for r in rows)

    def pad(row):
        r = list(row) + [""] * (width - len(row))
        return r[:width]

    rows = [pad(r) for r in rows]
    header = rows[0]
    lines = [
        "| " + " | ".join(_escape_cell(c) for c in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for r in rows[1:]:
        lines.append("| " + " | ".join(_escape_cell(c) for c in r) + " |")
    return "\n".join(lines)


def csv_to_md():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    if not raw.strip():
        notepad.messageBox("没有 CSV/TSV 内容。", "CSV 转 Markdown", 0)
        return

    delim = _detect_delim(raw)
    md = _to_md_table(raw, delim)
    if md is None:
        notepad.messageBox("无法解析出行。", "CSV 转 Markdown", 0)
        return

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(md)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已使用分隔符：{!r}".format(delim), "CSV 转 Markdown", 0)


csv_to_md()
