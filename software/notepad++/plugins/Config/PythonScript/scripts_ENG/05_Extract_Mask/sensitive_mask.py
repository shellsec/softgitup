# -*- coding: utf-8 -*-
"""
Mask common sensitive patterns in selection or whole document. 0 tokens, no AI.

Covers: emails, China mobile, China ID (18 digits), OpenAI-style sk- keys, AWS AKIA keys.
Replaces with [MASKED:type] tags.
"""

import re

_REPLACEMENT = "[MASKED:{0}]"

_PATTERNS = (
    ("email", re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")),
    ("mobile_cn", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("id_cn", re.compile(r"\b\d{17}[\dXx]\b")),
    ("openai_sk", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws_ak", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


def sensitive_mask():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    if not raw:
        notepad.messageBox("No text.", "Sensitive mask", 0)
        return

    text = raw
    counts = {}
    for name, rx in _PATTERNS:

        def repl(_m, n=name):
            counts[n] = counts.get(n, 0) + 1
            return _REPLACEMENT.format(n)

        text = rx.sub(repl, text)

    if text == raw:
        notepad.messageBox("No matching patterns found.", "Sensitive mask", 0)
        return

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(text)
    finally:
        editor.endUndoAction()

    parts = ["Masked:"]
    for k in sorted(counts.keys()):
        parts.append("  {}: {}".format(k, counts[k]))
    notepad.messageBox("\n".join(parts), "Sensitive mask", 0)


sensitive_mask()
