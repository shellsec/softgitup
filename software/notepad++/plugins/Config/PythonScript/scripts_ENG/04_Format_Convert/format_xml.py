# -*- coding: utf-8 -*-
"""
XML Formatter
Format XML text to make it more readable
"""

import xml.dom.minidom
import re

def format_xml():
    """Format XML"""
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
        notepad.messageBox("No content to format", "XML Formatter", 0)
        return
    
    editor.beginUndoAction()
    try:
        try:
            # Parse XML
            dom = xml.dom.minidom.parseString(selected_text)
            # Format output (2 spaces indent)
            formatted = dom.toprettyxml(indent="  ")
            
            # Remove empty line after XML declaration
            formatted = re.sub(r'<\?xml[^>]*>\s*\n\s*\n', '<?xml version="1.0" ?>\n', formatted)
            
            # Replace text
            editor.setSelection(start_pos, end_pos)
            editor.replaceSel(formatted)
            notepad.messageBox("XML formatted successfully", "XML Formatter", 0)
        except xml.parsers.expat.ExpatError as e:
            notepad.messageBox(
                "XML format error: {}".format(str(e)),
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

format_xml()

