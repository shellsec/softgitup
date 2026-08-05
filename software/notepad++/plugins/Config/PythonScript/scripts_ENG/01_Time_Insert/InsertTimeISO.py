# -*- coding: utf-8 -*-
"""Insert local ISO time YYYY-MM-DDTHH:MM:SS."""
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
    from time_stamp_fmt import format_iso
except ImportError:
    def format_iso(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y-%m-%dT%H:%M:%S")


editor.insertText(editor.getCurrentPos(), format_iso())
