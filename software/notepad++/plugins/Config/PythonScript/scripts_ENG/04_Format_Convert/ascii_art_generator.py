# -*- coding: utf-8 -*-
"""
ASCII Art Generator
Open online ASCII Art generator website
Website: http://patorjk.com/software/taag/
"""

import webbrowser
import urllib.parse

def ascii_art_generator():
    """Open ASCII Art generator website"""
    # Online ASCII Art generator website
    base_url = "http://patorjk.com/software/taag/"
    
    # Get selected text
    selected_text = editor.getSelText()
    
    # If there's selected text, copy it to clipboard
    if selected_text:
        try:
            import win32clipboard
            import win32con
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, selected_text)
            win32clipboard.CloseClipboard()
        except:
            # Try tkinter as fallback
            try:
                import tkinter
                root = tkinter.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(selected_text)
                root.update()
                root.destroy()
            except:
                pass
    
    try:
        # Open browser
        webbrowser.open(base_url)
    except Exception as e:
        notepad.messageBox(
            "Failed to open website: {}\n\nPlease visit manually:\n{}".format(str(e), base_url),
            "Error",
            0
        )

ascii_art_generator()

