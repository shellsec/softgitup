# -*- coding: utf-8 -*-
import sys


def template_block(lines, leading_newline=True):
    nl = "\r\n" if sys.platform == "win32" else "\n"
    body = nl.join(lines)
    if leading_newline:
        return nl + body
    return body
