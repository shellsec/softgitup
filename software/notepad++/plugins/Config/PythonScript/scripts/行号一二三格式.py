# -*- coding: utf-8 -*-
"""
多行自动编号
在选中的多行文字前面自动添加 1、 2、 3、 格式的编号
"""

def add_line_numbers():
    """在选中每行前面加上 1、 2、 3、"""
    start_pos = editor.getSelectionStart()
    end_pos = editor.getSelectionEnd()

    # 没有选中时，提示用户
    if start_pos == end_pos:
        notepad.messageBox(
            "请先选中需要编号的多行文字，再运行本脚本。",
            "多行自动编号",
            0
        )
        return

    selected_text = editor.getSelText()
    if not selected_text:
        return

    # 检测并保留原文换行符
    if "\r\n" in selected_text:
        newline = "\r\n"
    elif "\r" in selected_text:
        newline = "\r"
    else:
        newline = "\n"

    # 按行分割
    lines = selected_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    # 为每一行前面加上 "序号、"
    numbered_lines = []
    for i, line in enumerate(lines, start=1):
        numbered_lines.append("{0}、{1}".format(i, line))

    # 用原来的换行符拼回去
    new_text = newline.join(numbered_lines)

    editor.beginUndoAction()
    try:
        editor.setSelectionStart(start_pos)
        editor.setSelectionEnd(end_pos)
        editor.replaceSel(new_text)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已为 {} 行添加编号。".format(len(lines)), "多行自动编号", 0)


add_line_numbers()
