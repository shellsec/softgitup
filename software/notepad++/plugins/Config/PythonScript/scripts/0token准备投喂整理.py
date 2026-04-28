# -*- coding: utf-8 -*-
"""
投喂模型前整理：合并多余空行、遮罩常见敏感信息、文末追加字符数与近似 Token。0 Token、不调模型。
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
        text = rx.sub("[已遮罩:{}]".format(name), text)
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
        notepad.messageBox("没有文本。", "0token 准备投喂整理", 0)
        return

    body = _collapse_blanks(raw.rstrip("\n\r"))
    body = _mask(body)
    nchar = len(body)
    nt = _approx_tokens(body)
    footer = "\n\n---\n字符数：{}\n近似 Token（启发式）：{}\n".format(nchar, nt)
    out = body + footer

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已合并空行、已遮罩、已追加统计页脚。", "0token 准备投喂整理", 0)


prep_for_llm()
