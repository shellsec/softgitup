# -*- coding: utf-8 -*-
"""
从缩进大纲生成 Mermaid mindmap 代码块（规则与「0token文字脑图生成」相同）。不联网、不调用 AI。

首行非空为根，后续用行首空格/Tab 表示层级；输出用 ```mermaid ... ``` 包裹。
有选中则替换选中，否则替换全文。
"""

TAB_WIDTH = 4


class _Node(object):
    __slots__ = ("text", "children")

    def __init__(self, text):
        self.text = text
        self.children = []


def _leading_space_count(line):
    e = line.expandtabs(TAB_WIDTH)
    n = 0
    for ch in e:
        if ch == " ":
            n += 1
        else:
            break
    return n


def _parse_outline(body_lines):
    stripped = [ln.rstrip() for ln in body_lines]
    first_i = None
    for i, ln in enumerate(stripped):
        if ln.strip():
            first_i = i
            break
    if first_i is None:
        return None
    root_text = stripped[first_i].strip()
    root = _Node(root_text)
    stack = [(root, -1)]

    for ln in stripped[first_i + 1 :]:
        if not ln.strip():
            continue
        indent = _leading_space_count(ln)
        text = ln.expandtabs(TAB_WIDTH).strip()
        if not text:
            continue
        node = _Node(text)
        while stack[-1][1] >= indent:
            stack.pop()
        stack[-1][0].children.append(node)
        stack.append((node, indent))
    return root


def _mermaid_label(s):
    if any(c in s for c in "#:()[]{}|\"\n\r\t"):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def _emit(node, col, lines):
    lines.append(" " * col + _mermaid_label(node.text))
    for ch in node.children:
        _emit(ch, col + 2, lines)


def _build_mermaid(root):
    lines = ["```mermaid", "mindmap", "  " + _mermaid_label(root.text)]
    for ch in root.children:
        _emit(ch, 4, lines)
    lines.append("```")
    return "\n".join(lines)


def mermaid_mindmap():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    root = _parse_outline(lines)
    if root is None:
        notepad.messageBox("没有可转换的大纲内容。", "Mermaid 脑图", 0)
        return

    output = _build_mermaid(root)
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。可粘贴到支持 Mermaid 的 Markdown 预览中查看。", "Mermaid 脑图", 0)


mermaid_mindmap()
