# -*- coding: utf-8 -*-
"""
Text mind map (ASCII tree): indented outline -> box-drawing tree.
0 tokens, no AI.

Input rules:
- First non-empty line = root title.
- Each following non-empty line: leading spaces/tabs = depth (tab = 4 spaces).
- Recommended: 2 spaces per level (4, 6, ... also work as long as indent strictly increases per depth).

If text is selected, replace selection with output; otherwise replace entire document.

Inverse: 0token_text_mindmap_restore.py / 0token文字脑图还原.py
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


def _render_lines(node, out, ancestor_prefix, is_last):
    branch = "└─ " if is_last else "├─ "
    out.append(ancestor_prefix + branch + node.text)
    child_prefix = ancestor_prefix + ("   " if is_last else "│  ")
    ch = node.children
    for i, c in enumerate(ch):
        _render_lines(c, out, child_prefix, i == len(ch) - 1)


def _render_tree(root):
    out = [root.text]
    ch = root.children
    for i, c in enumerate(ch):
        _render_lines(c, out, "", i == len(ch) - 1)
    return "\n".join(out)


def text_mindmap():
    selected = editor.getSelText()
    if selected is not None and len(selected) > 0:
        raw = selected
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    root = _parse_outline(lines)
    if root is None:
        notepad.messageBox("No outline to convert.", "Text mind map", 0)
        return

    output = _render_tree(root)
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done. Root + {} top-level branch(es).".format(len(root.children)), "Text mind map", 0)


text_mindmap()
