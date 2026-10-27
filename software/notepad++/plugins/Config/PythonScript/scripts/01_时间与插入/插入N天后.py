# -*- coding: utf-8 -*-
"""弹出输入天数，插入偏移后的中文长串日期（单行；规则见 time_stamp_fmt.format_cn）。"""
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
    from time_stamp_fmt import format_cn, parse_day_offset, shift_days
except ImportError:
    from datetime import datetime, timedelta

    def shift_days(days, now=None):
        n = now if now is not None else datetime.now()
        return n + timedelta(days=days)

    def format_cn(now=None):
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
        "多少天之后？（整数）\n0 = 今天，1 = 明天，2 = 后天，负数 = 之前",
        "插入N天后",
        "1",
    )
    if raw is None:
        return
    try:
        days = parse_day_offset(raw)
    except ValueError:
        notepad.messageBox("请输入整数天数，例如 0、1、2 或 -1。", "插入N天后", 0)
        return
    editor.insertText(editor.getCurrentPos(), format_cn(shift_days(days)))


main()
