# -*- coding: utf-8 -*-
"""
JSON Formatter
Format JSON text to make it more readable
"""

import json

def format_json():
    """Format JSON"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        # If no selected text, format entire document
        selected_text = editor.getText()
        start_pos = 0
        end_pos = len(selected_text)
    else:
        start_pos = editor.getSelectionStart()
        end_pos = editor.getSelectionEnd()
    
    if not selected_text.strip():
        notepad.messageBox("No content to format", "JSON Formatter", 0)
        return
    
    editor.beginUndoAction()
    try:
        try:
            # Parse JSON
            json_obj = json.loads(selected_text)
            # Format output (4 spaces indent)
            formatted = json.dumps(json_obj, ensure_ascii=False, indent=4)
            
            # Replace text
            editor.setSelection(start_pos, end_pos)
            editor.replaceSel(formatted)
            notepad.messageBox("JSON formatted successfully", "JSON Formatter", 0)
        except json.JSONDecodeError as e:
            notepad.messageBox(
                "JSON format error: {}".format(str(e)),
                "Error",
                0
            )
        except Exception as e:
            notepad.messageBox(
                "Format failed: {}".format(str(e)),
                "Error",
                0
            )
    finally:
        editor.endUndoAction()

format_json()

