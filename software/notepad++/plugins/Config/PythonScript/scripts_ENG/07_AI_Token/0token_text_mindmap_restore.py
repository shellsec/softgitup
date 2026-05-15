# -*- coding: utf-8 -*-
"""
Restore indented outline from ASCII mind map (├─ └─ │). Inverse of 0token_text_mindmap.py.
0 tokens, no AI.

Recognizes lines produced by the generator:
- Prefix: zero or more of "│  " (vertical + 2 spaces) or "   " (3 spaces) per ancestor level
- Then "├─" or "└─" (box-drawing), then node text

First non-empty line without that pattern = root title.
If the first non-empty line is already a branch line, output outline only (no root line).

Selection replaces selection; no selection replaces whole document.
"""

TAB_WIDTH = 4
_TRIPLET_PIPE = "\u2502  "  # │ + two spaces
_TRIPLET_SPACE = "   "
_BRANCH1 = "\u251c\u2500"  # ├─
_BRANCH2 = "\u2514\u2500"  # └─


def _parse_tree_row(line):
    """Return (depth_units, content) or (None, None) if not a tree row."""
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
        notepad.messageBox("No mind map / root found to restore.", "Text mind map restore", 0)
        return

    output, skipped = result
    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(output)
    finally:
        editor.endUndoAction()

    msg = "Restored to outline."
    if skipped:
        msg += "\nSkipped {} unrecognized line(s).".format(skipped)
    notepad.messageBox(msg, "Text mind map restore", 0)


text_mindmap_restore()
