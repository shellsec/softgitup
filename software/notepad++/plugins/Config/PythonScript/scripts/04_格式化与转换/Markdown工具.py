# -*- coding: utf-8 -*-
"""Markdown 小工具：标题升降级、代码块包裹、表格对齐、YAML front matter。"""
import re
from datetime import datetime


def _sel_or_warn():
    text = editor.getSelText()
    if not text:
        notepad.messageBox("请先选中要处理的文本。", "Markdown工具", 0)
        return None
    return text


def _replace_sel(new_text):
    editor.beginUndoAction()
    try:
        editor.replaceSel(new_text)
    finally:
        editor.endUndoAction()


def _split_keep_nl(text):
    """Split into (line_without_nl, nl) pairs; last nl may be ''."""
    parts = []
    i = 0
    n = len(text)
    while i < n:
        j = i
        while j < n and text[j] not in "\r\n":
            j += 1
        line = text[i:j]
        nl = ""
        if j < n:
            if text[j] == "\r" and j + 1 < n and text[j + 1] == "\n":
                nl = "\r\n"
                j += 2
            else:
                nl = text[j]
                j += 1
        parts.append((line, nl))
        i = j
    return parts


def heading_shift(delta):
    """delta +1 → more # (smaller heading); -1 → fewer # (larger)."""
    text = _sel_or_warn()
    if text is None:
        return
    out = []
    for line, nl in _split_keep_nl(text):
        m = re.match(r"^(#{1,6})(\s+)(.*)$", line)
        if not m:
            out.append(line + nl)
            continue
        level = max(1, min(6, len(m.group(1)) + delta))
        out.append("#" * level + m.group(2) + m.group(3) + nl)
    _replace_sel("".join(out))


def wrap_codeblock():
    text = _sel_or_warn()
    if text is None:
        return
    lang = notepad.prompt("代码语言（可空）：", "Markdown工具 · 代码块", "")
    if lang is None:
        return
    lang = (lang or "").strip()
    body = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    block = "```{}\r\n{}\r\n```".format(lang, body.replace("\n", "\r\n"))
    _replace_sel(block)


def align_table():
    text = _sel_or_warn()
    if text is None:
        return
    lines = [ln.rstrip("\r\n") for ln in text.replace("\r\n", "\n").split("\n")]
    rows = []
    for ln in lines:
        if not ln.strip():
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 1:
        notepad.messageBox("未识别到表格行。", "Markdown工具", 0)
        return
    if len(rows) >= 2 and all(re.match(r"^:?-+:?$", c or "-") for c in rows[1]):
        rows.pop(1)
    width = max(len(r) for r in rows)
    for r in rows:
        while len(r) < width:
            r.append("")
    cols = [max(len(rows[i][j]) for i in range(len(rows))) for j in range(width)]
    cols = [max(3, w) for w in cols]

    def fmt_row(cells):
        parts = [cells[j].ljust(cols[j]) for j in range(width)]
        return "| " + " | ".join(parts) + " |"

    sep = "| " + " | ".join("-" * cols[j] for j in range(width)) + " |"
    out_lines = [fmt_row(rows[0]), sep] + [fmt_row(r) for r in rows[1:]]
    _replace_sel("\r\n".join(out_lines))


def insert_front_matter():
    title = notepad.prompt("标题（可空）：", "Markdown工具 · front matter", "")
    if title is None:
        return
    tags = notepad.prompt("标签（逗号分隔，可空）：", "Markdown工具 · front matter", "")
    if tags is None:
        return
    day = datetime.now().strftime("%Y-%m-%d")
    tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
    tags_yaml = "[" + ", ".join(tag_list) + "]" if tag_list else "[]"
    fm = (
        "---\r\n"
        "title: {}\r\n"
        "date: {}\r\n"
        "tags: {}\r\n"
        "---\r\n\r\n"
    ).format((title or "").strip() or "untitled", day, tags_yaml)
    editor.insertText(0, fm)


def main():
    r = notepad.prompt(
        "选择功能：\n"
        "1 — 标题变小（增加 #，最多 6 级）\n"
        "2 — 标题变大（减少 #，最少 1 级）\n"
        "3 — 选区包代码块\n"
        "4 — Markdown 表格对齐\n"
        "5 — 文档开头插入 YAML front matter\n",
        "Markdown工具",
        "3",
    )
    if r is None:
        return
    r = (r or "").strip()
    if r == "1":
        heading_shift(+1)
    elif r == "2":
        heading_shift(-1)
    elif r == "3":
        wrap_codeblock()
    elif r == "4":
        align_table()
    elif r == "5":
        insert_front_matter()
    else:
        notepad.messageBox("请输入 1–5。", "Markdown工具", 0)


main()
