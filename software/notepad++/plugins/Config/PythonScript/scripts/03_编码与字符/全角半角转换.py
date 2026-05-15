# -*- coding: utf-8 -*-
"""
全角/半角：常见数字、英文字母、标点与全角空格。1 = 转半角，2 = 转全角（仅映射表内）。0 Token。
"""

_PAIRS = (
    "０0１1２2３3４4５5６6７7８8９9"
    "ＡAＢBＣCＤDＥEＦFＧGＨHＩIＪJＫKＬLＭMＮNＯOＰPＱQＲRＳSＴTＵUＶVＷWＸXＹYＺZ"
    "ａaｂbｃcｄdｅeｆfｇgｈhｉiｊjｋkｌlｍmｎnｏoｐpｑqｒrｓsｔtｕuｖvｗwｘxｙyｚz"
    "，,。.、,；;：:？?（(）)［[］]｛{｝}　 "
)
_FULL = _PAIRS[0::2]
_HALF = _PAIRS[1::2]
_TO_HALF = str.maketrans(_FULL, _HALF)
_TO_FULL = str.maketrans(_HALF, _FULL)


def fw_hw_convert():
    choice = notepad.prompt(
        "1 = 转为半角\n2 = 转为全角（仅映射表内字符）",
        "全角半角",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice == "1":
        table = _TO_HALF
    elif choice == "2":
        table = _TO_FULL
    else:
        notepad.messageBox("请输入 1 或 2。", "全角半角", 0)
        return

    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()
    else:
        raw = editor.getText()
        start = 0
        end = editor.getLength()

    if not raw:
        notepad.messageBox("没有文本。", "全角半角", 0)
        return

    out = raw.translate(table)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("已完成。", "全角半角", 0)


fw_hw_convert()
