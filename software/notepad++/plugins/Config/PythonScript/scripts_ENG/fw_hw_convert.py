# -*- coding: utf-8 -*-
"""
Fullwidth <-> halfwidth for common digits, Latin letters, punctuation, ideographic space.
Prompt: 1 = to halfwidth, 2 = to fullwidth. 0 tokens, no AI.
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
        "1 = To halfwidth\n2 = To fullwidth (mapped set only)",
        "Full/half width",
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
        notepad.messageBox("Enter 1 or 2.", "Full/half width", 0)
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
        notepad.messageBox("No text.", "Full/half width", 0)
        return

    out = raw.translate(table)

    editor.beginUndoAction()
    try:
        editor.setSelection(start, end)
        editor.replaceSel(out)
    finally:
        editor.endUndoAction()

    notepad.messageBox("Done.", "Full/half width", 0)


fw_hw_convert()
