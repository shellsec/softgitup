# -*- coding: utf-8 -*-
"""
Text Format Converter
Convert text to camelCase, snake_case, kebab-case, etc.
"""

import re

def text_format_convert():
    """Text format converter"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to convert",
            "Text Format Converter",
            0
        )
        return
    
    # Select conversion type
    choice = notepad.prompt(
        "Select conversion type:\n1.Camel 2.Pascal 3.Snake\n4.Kebab 5.Constant 6.Space",
        "Text Format Converter",
        "1"
    )
    
    if choice is None:
        return
    
    # Extract number
    match = re.search(r'\d+', str(choice))
    if match:
        choice = match.group()
    else:
        choice = str(choice).strip()
    
    editor.beginUndoAction()
    try:
        # Normalize: convert separators to spaces, then split words
        text = selected_text.strip()
        # Convert underscores, hyphens, spaces to spaces
        text = re.sub(r'[_\-\s]+', ' ', text)
        # Detect camelCase (insert space before uppercase)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        # Split words
        words = [w.strip() for w in text.split() if w.strip()]
        
        if not words:
            notepad.messageBox("Cannot recognize word format", "Error", 0)
            return
        
        # Convert to lowercase word list
        words_lower = [w.lower() for w in words]
        
        if choice == "1":
            # camelCase: first word lowercase, rest capitalized
            result = words_lower[0] + ''.join(w.capitalize() for w in words_lower[1:])
        elif choice == "2":
            # PascalCase: all words capitalized
            result = ''.join(w.capitalize() for w in words_lower)
        elif choice == "3":
            # snake_case: all lowercase, underscore separated
            result = '_'.join(words_lower)
        elif choice == "4":
            # kebab-case: all lowercase, hyphen separated
            result = '-'.join(words_lower)
        elif choice == "5":
            # UPPER_SNAKE_CASE: all uppercase, underscore separated
            result = '_'.join(w.upper() for w in words_lower)
        elif choice == "6":
            # Space separated, each word capitalized
            result = ' '.join(w.capitalize() for w in words_lower)
        else:
            notepad.messageBox("Invalid choice, using default: camelCase", "Info", 0)
            result = words_lower[0] + ''.join(w.capitalize() for w in words_lower[1:])
        
        editor.replaceSel(result)
        notepad.messageBox("Conversion complete", "Text Format Converter", 0)
    finally:
        editor.endUndoAction()

text_format_convert()

