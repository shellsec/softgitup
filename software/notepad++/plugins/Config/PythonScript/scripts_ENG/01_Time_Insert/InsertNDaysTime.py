# -*- coding: utf-8 -*-
"""Prompt for a day offset, then insert the English long date (format_en)."""
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
    from time_stamp_fmt import format_en, parse_day_offset, shift_days
except ImportError:
    from datetime import datetime, timedelta

    def shift_days(days, now=None):
        n = now if now is not None else datetime.now()
        return n + timedelta(days=days)

    def format_en(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y%m%d")

    def parse_day_offset(text):
        if text is None:
            raise ValueError("day offset required")
        s = str(text).strip()
        if not s:
            raise ValueError("day offset required")
        body = s[1:] if s[0] in "+-" else s
        if not body.isdigit():
            raise ValueError("day offset must be an integer")
        return int(s)


def main():
    raw = notepad.prompt(
        "Days from today (integer)\n0 = today, 1 = tomorrow, 2 = in two days, negative = earlier",
        "Insert N days",
        "1",
    )
    if raw is None:
        return
    try:
        days = parse_day_offset(raw)
    except ValueError:
        notepad.messageBox("Enter an integer number of days, for example 0, 1, 2, or -1.", "Insert N days", 0)
        return
    editor.insertText(editor.getCurrentPos(), format_en(shift_days(days)))


main()
