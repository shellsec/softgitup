# -*- coding: utf-8 -*-
"""
Generate Random String
Generate random string of specified length (letters, digits, special characters)
"""

import random
import string

def generate_random_string():
    """Generate random string"""
    # Get length
    length_input = notepad.prompt(
        "Enter string length:",
        "Generate Random String",
        "16"
    )
    
    if length_input is None:
        return
    
    try:
        length = int(length_input)
        if length <= 0:
            notepad.messageBox("Length must be greater than 0", "Error", 0)
            return
    except ValueError:
        notepad.messageBox("Please enter a valid number", "Error", 0)
        return
    
    # Select character set
    choice = notepad.prompt(
        "Select character set:\n1.Letters 2.Digits 3.Letters+Digits 4.All",
        "Generate Random String",
        "3"
    )
    
    if choice is None:
        return
    
    if choice == "1":
        chars = string.ascii_letters
    elif choice == "2":
        chars = string.digits
    elif choice == "3":
        chars = string.ascii_letters + string.digits
    elif choice == "4":
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        notepad.messageBox("Invalid choice, using default: Letters+Digits", "Info", 0)
        chars = string.ascii_letters + string.digits
    
    # Generate random string
    random_string = ''.join(random.choice(chars) for _ in range(length))
    
    # Copy to clipboard (multiple methods)
    copied = False
    error_msg = ""
    
    # Method 1: win32clipboard
    try:
        import win32clipboard
        import win32con
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, random_string)
        win32clipboard.CloseClipboard()
        copied = True
    except Exception as e:
        error_msg = str(e)
        # Method 2: tkinter
        try:
            import tkinter
            root = tkinter.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(random_string)
            root.update()
            root.destroy()
            copied = True
        except Exception as e2:
            error_msg += "\n" + str(e2)
            # Method 3: Notepad++ copy function
            try:
                current_pos = editor.getCurrentPos()
                editor.insertText(current_pos, random_string)
                editor.setSelectionStart(current_pos)
                editor.setSelectionEnd(current_pos + len(random_string))
                editor.copy()
                editor.deleteRange(current_pos, len(random_string))
                copied = True
            except Exception as e3:
                error_msg += "\n" + str(e3)
    
    if copied:
        notepad.messageBox("Generated and copied to clipboard!", "Generate Random String", 0)
    else:
        notepad.messageBox(
            "Generation complete!\n\nFailed to copy to clipboard\n\nResult: {}\n\nPlease copy manually".format(random_string),
            "Generate Random String",
            0
        )

generate_random_string()

