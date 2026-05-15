# -*- coding: utf-8 -*-
"""
敏感信息遮罩：在选中或全文中替换常见敏感模式。0 Token、不联网。

覆盖：邮箱、中国手机号、18 位身份证、OpenAI 风格 sk- 密钥、AWS AKIA 密钥。
替换为 [已遮罩:类型] 占位（英文脚本为 [MASKED:type]）。
"""

import re

_REPLACEMENT = "[已遮罩:{0}]"

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
        notepad.messageBox("没有文本。", "敏感信息遮罩", 0)
        return

    text = raw
    counts = {}
    for name, rx in _PATTERNS:

        def repl(_m, n=name):
            counts[n] = counts.get(n, 0) + 1
            return _REPLACEMENT.format(n)

        text = rx.sub(repl, text)

    if text == raw:
        notepad.messageBox("未发现匹配的模式。", "敏感信息遮罩", 0)
        return

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(text)
    finally:
        editor.endUndoAction()

    parts = ["已遮罩："]
    for k in sorted(counts.keys()):
        parts.append("  {}：{} 处".format(k, counts[k]))
    notepad.messageBox("\n".join(parts), "敏感信息遮罩", 0)


sensitive_mask()
