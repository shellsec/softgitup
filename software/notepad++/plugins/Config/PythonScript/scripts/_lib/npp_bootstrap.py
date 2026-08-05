# -*- coding: utf-8 -*-
"""Locate scripts/_lib (or scripts_ENG/_lib) and put it on sys.path."""
import os
import sys


def ensure_lib_path(start=None, marker="time_stamp_fmt.py"):
    """
    Walk parents from `start` (default: caller file dir) until `_lib/<marker>`
    is found; insert that `_lib` at sys.path[0]. Returns the lib dir or "".
    """
    if start is None:
        # Caller's directory if possible
        try:
            import inspect

            frame = inspect.stack()[1]
            start = os.path.dirname(os.path.abspath(frame.filename))
        except Exception:
            start = os.path.dirname(os.path.abspath(__file__))
    _d = start
    for __ in range(10):
        _lib = os.path.join(_d, "_lib")
        if os.path.isfile(os.path.join(_lib, marker)):
            if _lib not in sys.path:
                sys.path.insert(0, _lib)
            return _lib
        _p = os.path.dirname(_d)
        if _p == _d:
            break
        _d = _p
    return ""
