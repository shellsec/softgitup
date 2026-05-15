# -*- coding: utf-8 -*-
"""
Prepare text before pasting to an LLM: collapse extra blank lines, mask common secrets,
append char count + heuristic token estimate. 0 tokens, no AI call.
"""

import re

_MASK_PATTERNS = (
    ("email", re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")),
    ("mobile_cn", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("id_cn", re.compile(r"\b\d{17}[\dXx]\b")),
    ("openai_sk", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws_ak", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


def _collapse_blanks(text):
    return re.sub(r"\n{3,}", "\n\n", text)


def _mask(text):
    for name, rx in _MASK_PATTERNS:
        text = rx.sub("[MASKED:{}]".format(name), text)
    return text


def _approx_tokens(t):
    if not t:
        return 0
    cjk = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]", t))
    non_cjk = max(0, len(t) - cjk)
    return int(non_cjk / 4.0 + cjk / 1.5 + 0.999)


def prep_for_llm():
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
        notepad.messageBox("No text.", "0token prep for LLM", 0)
        return

    body = _collapse_blanks(raw.rstrip("\n\r"))
    body = _mask(body)
    nchar = len(body)
    nt = _approx_tokens(body)
    footer = "\n\n---\nChars: {}\nApprox tokens (heuristic): {}\n".format(nchar, nt)
    out = body + footer

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox(
        "Collapsed blank lines, masked patterns, appended stats footer.",
        "0token prep for LLM",
        0,
    )


prep_for_llm()
