# -*- coding: utf-8 -*-
"""
多行自动编号（多种格式可选）
支持：1. 2. / (1) (2) / ① ② ③ / 01、02、（补零）/ 自定义前缀（如 0x0）
"""

# Unicode 带圈数字 ①～⑳ (1-20)，㉑～㉟ (21-35)
CIRCLED_1_20 = "\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468\u2469\u246a\u246b\u246c\u246d\u246e\u246f\u2470\u2471\u2472\u2473"
CIRCLED_21_35 = "\u3251\u3252\u3253\u3254\u3255\u3256\u3257\u3258\u3259\u325a\u325b\u325c\u325d\u325e\u325f"


def get_number_prefix(style, index, start, padding, custom_prefix):
    """根据格式返回当前行的编号前缀。index 从 0 起，显示为 start + index。"""
    n = start + index
    if style == "1":
        return "{0}. ".format(n)
    if style == "2":
        return "({0}) ".format(n)
    if style == "3":
        if 1 <= n <= 20:
            return CIRCLED_1_20[n - 1] + " "
        if 21 <= n <= 35:
            return CIRCLED_21_35[n - 21] + " "
        return "({0}) ".format(n)
    if style == "4":
        return "{0:0{1}d}、".format(n, padding)
    if style == "5":
        return "{0}{1:0{2}d}".format(custom_prefix, n, padding)
    return "{0}、".format(n)


def add_line_numbers_multi():
    start_pos = editor.getSelectionStart()
    end_pos = editor.getSelectionEnd()

    if start_pos == end_pos:
        notepad.messageBox(
            "请先选中需要编号的多行文字，再运行本脚本。",
            "多行自动编号（多种格式）",
            0
        )
        return

    selected_text = editor.getSelText()
    if not selected_text:
        return

    # 先弹出说明（避免 prompt 框太小看不到上面选项）
    notepad.messageBox(
        "1 = 1. 2. 3.\n"
        "2 = (1) (2) (3)\n"
        "3 = ① ② ③\n"
        "4 = 01、02、03、（补零）\n"
        "5 = 自定义前缀（如 0x0 → 0x01 0x02）\n\n"
        "点击确定后，在下一框输入 1～5 选择格式。",
        "多行自动编号 - 格式说明",
        0
    )

    # 选择格式
    choice = notepad.prompt("请输入编号格式 1～5：", "多行自动编号", "1")
    if choice is None:
        return
    style = choice.strip() or "1"
    if style not in "12345":
        style = "1"

    start_num = 1
    padding = 2
    custom_prefix = ""

    if style in "45":
        start_str = notepad.prompt("起始数字（直接回车默认为 1）：", "起始数字", "1")
        if start_str is not None and start_str.strip() != "":
            try:
                start_num = int(start_str.strip())
            except ValueError:
                pass
        pad_str = notepad.prompt("位数（补零宽度，直接回车默认为 2）：", "补零位数", "2")
        if pad_str is not None and pad_str.strip() != "":
            try:
                padding = max(1, int(pad_str.strip()))
            except ValueError:
                pass
    if style == "5":
        custom_prefix = notepad.prompt("自定义前缀（如 0x0 或 item_）：", "自定义前缀", "0x0")
        if custom_prefix is None:
            custom_prefix = "0x0"
        custom_prefix = custom_prefix.strip() or "0x0"

    if "\r\n" in selected_text:
        newline = "\r\n"
    elif "\r" in selected_text:
        newline = "\r"
    else:
        newline = "\n"

    lines = selected_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    numbered_lines = []
    for i, line in enumerate(lines):
        prefix = get_number_prefix(style, i, start_num, padding, custom_prefix)
        numbered_lines.append(prefix + line)

    new_text = newline.join(numbered_lines)

    editor.beginUndoAction()
    try:
        editor.setSelectionStart(start_pos)
        editor.setSelectionEnd(end_pos)
        editor.replaceSel(new_text)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已为 {} 行添加编号。".format(len(lines)), "多行自动编号", 0)


add_line_numbers_multi()
