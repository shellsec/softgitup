# -*- coding: utf-8 -*-
"""Insert week stamp, e.g. 2026-W32 · Week 32 · Wed."""
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
    from time_stamp_fmt import format_week_en
except ImportError:
    def format_week_en(now=None):
        n = now if now is not None else datetime.now()
        return "W{}".format(n.isocalendar()[1])


editor.insertText(editor.getCurrentPos(), format_week_en())
