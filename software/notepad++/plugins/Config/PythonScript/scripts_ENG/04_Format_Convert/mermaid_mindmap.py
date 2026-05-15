# -*- coding: utf-8 -*-
"""
Build a Mermaid mindmap code block from the same indented outline as 0token_text_mindmap.py.
0 tokens, no AI.

First non-empty line = root; following lines use leading spaces/tabs for depth (tab = 4).
Output replaces selection or whole document; wrapped in ```mermaid ... ```.
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
        notepad.messageBox("No outline to convert.", "Mermaid mindmap", 0)
        return

    output = _build_mermaid(root)
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done. Paste into Markdown viewers that support Mermaid.", "Mermaid mindmap", 0)


mermaid_mindmap()
