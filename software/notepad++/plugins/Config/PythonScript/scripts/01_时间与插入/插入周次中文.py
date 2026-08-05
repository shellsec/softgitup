# -*- coding: utf-8 -*-
"""插入周次信息，如 2026-W32 · 第32周 · 周三。"""
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
    from time_stamp_fmt import format_week_cn
except ImportError:
    def format_week_cn(now=None):
        n = now if now is not None else datetime.now()
        return "W{}".format(n.isocalendar()[1])


editor.insertText(editor.getCurrentPos(), format_week_cn())
