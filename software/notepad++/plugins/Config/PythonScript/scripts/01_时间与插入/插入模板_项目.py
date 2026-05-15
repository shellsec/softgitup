# -*- coding: utf-8 -*-
"""项目 · 换行按 CRLF（仅当前文档）。"""
import os
import sys

_d = os.path.dirname(os.path.abspath(__file__))
for __ in range(10):
    _lib = os.path.join(_d, "_lib")
    if os.path.isfile(os.path.join(_lib, "time_stamp_fmt.py")):
        if _lib not in sys.path:
            sys.path.insert(0, _lib)
        break
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p

from datetime import datetime

try:
    from time_stamp_fmt import format_cn
except ImportError:
    def format_cn(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y%m%d")

try:
    from npp_eol import template_block
except ImportError:
    def template_block(lines, leading_newline=True):
        nl = "\r\n" if sys.platform == "win32" else "\n"
        body = nl.join(lines)
        return (nl + body) if leading_newline else body


ts = format_cn(datetime.now())
editor.insertText(
    editor.getCurrentPos(),
    template_block(
        [
            ts,
            "项目今天：（一句话：做啥、到哪了）",
            "",
            "当前进度：（阶段或百分比随意）",
            "",
            "依赖或风险：（人/事/写「无」）",
            "",
            "下一步：（一个动作）",
            "",
            "---",
        ]
    ),
)
