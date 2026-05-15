# -*- coding: utf-8 -*-
"""
Save Selected Text
Save selected text to specified file
"""

import os

def save_selected_text():
    """Save selected text"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to save",
            "Save Selected Text",
            0
        )
        return
    
    # Get save path
    file_path = notepad.prompt(
        "Enter save path:",
        "Save Selected Text",
        ""
    )
    
    if not file_path or file_path.strip() == "":
        return
    
    file_path = file_path.strip()
    
    try:
        # Ensure directory exists
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        # Save file (using UTF-8 encoding)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(selected_text)
        
        notepad.messageBox(
            "Saved to:\n{}\n({} characters)".format(file_path, len(selected_text)),
            "Save Selected Text",
            0
        )
    except Exception as e:
        notepad.messageBox(
            "Failed to save file:\n{}".format(str(e)),
            "Error",
            0
        )

save_selected_text()

