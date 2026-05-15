# -*- coding: utf-8 -*-
"""
Notepad++ 在 CRLF 文档里用 insertText 只塞 \\n 时，有时整段会挤成一行。
用本模块按系统换行拼接后再插入。
"""
import sys


def template_block(lines, leading_newline=True):
    nl = "\r\n" if sys.platform == "win32" else "\n"
    body = nl.join(lines)
    if leading_newline:
        return nl + body
    return body
