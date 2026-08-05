# -*- coding: utf-8 -*-
"""插入昨天的中文长串日期（单行；规则见 time_stamp_fmt.format_cn）。"""
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

try:
    from time_stamp_fmt import format_cn, shift_days
except ImportError:
    from datetime import datetime, timedelta

    def shift_days(days, now=None):
        n = now if now is not None else datetime.now()
        return n + timedelta(days=days)

    def format_cn(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y%m%d")


editor.insertText(editor.getCurrentPos(), format_cn(shift_days(-1)))
