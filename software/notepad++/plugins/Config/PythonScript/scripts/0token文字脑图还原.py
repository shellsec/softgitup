# -*- coding: utf-8 -*-
"""
文字脑图还原：由 ├─ └─ │ 树形还原为缩进大纲（与「0token文字脑图生成」互逆）。0 Token、不联网。

识别规则（与生成脚本一致）：
- 行首可重复「│  」或「   」（各 3 个字符）表示祖先层级
- 接着「├─」或「└─」与正文

首行非空若不符合上述分支格式，则视为根标题；若首行就是分支行，则输出仅大纲、无单独根行。

有选中则替换选中；无选中则替换全文。
"""

TAB_WIDTH = 4
_TRIPLET_PIPE = "\u2502  "
_TRIPLET_SPACE = "   "
_BRANCH1 = "\u251c\u2500"
_BRANCH2 = "\u2514\u2500"


def _parse_tree_row(line):
    s = line.rstrip()
    if not s:
        return None, None
    s = s.expandtabs(TAB_WIDTH)
    pos = 0
    depth_units = 0
    while pos + 3 <= len(s):
        chunk = s[pos : pos + 3]
        if chunk == _TRIPLET_PIPE or chunk == _TRIPLET_SPACE:
            depth_units += 1
            pos += 3
        else:
            break
    if pos + 2 <= len(s):
        br = s[pos : pos + 2]
        if br == _BRANCH1 or br == _BRANCH2:
            text = s[pos + 2 :].lstrip()
            return depth_units, text
    return None, None


def _restore_mindmap(lines):
    stripped = [ln.rstrip() for ln in lines]
    first_idx = None
    for i, ln in enumerate(stripped):
        if ln.strip():
            first_idx = i
            break
    if first_idx is None:
        return None, 0

    items = []
    skipped = 0
    for i in range(first_idx, len(stripped)):
        ln = stripped[i]
        if not ln.strip():
            continue
        expanded = ln.expandtabs(TAB_WIDTH)
        du, tx = _parse_tree_row(expanded)
        if du is None:
            if i == first_idx:
                items.append(("root", expanded.strip()))
            else:
                skipped += 1
        else:
            items.append(("node", du, tx))

    if not items:
        return None, skipped

    out = []
    if items[0][0] == "root":
        out.append(items[0][1])
        for it in items[1:]:
            if it[0] != "node":
                continue
            _, du, tx = it
            out.append((" " * (du * 2)) + tx)
    else:
        for it in items:
            if it[0] != "node":
                continue
            _, du, tx = it
            out.append((" " * (du * 2)) + tx)

    return "\n".join(out), skipped


def text_mindmap_restore():
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
    result = _restore_mindmap(lines)
    if result is None or result[0] is None:
        notepad.messageBox("未识别到脑图或根标题。", "文字脑图还原", 0)
        return

    output, skipped = result
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    msg = "已还原为缩进大纲。"
    if skipped:
        msg += "\n有 {} 行无法识别，已跳过。".format(skipped)
    notepad.messageBox(msg, "文字脑图还原", 0)


text_mindmap_restore()
