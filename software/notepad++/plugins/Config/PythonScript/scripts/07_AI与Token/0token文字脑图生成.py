# -*- coding: utf-8 -*-
"""
文字脑图（ASCII 树）：缩进大纲 -> ├─ └─ │ 树形，0 Token、不调用 AI。

规则：
- 第一段非空行 = 根标题（如「TOKEN即真理」）。
- 后续非空行：行首空格/制表符表示层级（制表符按 4 列宽展开）。
- 建议每加深一级加 **2 个空格**（只要子级缩进严格大于父级即可）。

有选中内容则替换选中部分为脑图；无选中则替换全文。

互逆脚本：0token文字脑图还原.py / 0token_text_mindmap_restore.py
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
        notepad.messageBox("没有可转换的大纲内容。", "文字脑图", 0)
        return

    output = _render_tree(root)
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。根节点下共 {} 个一级分支。".format(len(root.children)), "文字脑图", 0)


text_mindmap()
