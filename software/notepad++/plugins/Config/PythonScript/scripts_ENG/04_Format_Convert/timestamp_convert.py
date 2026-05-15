# -*- coding: utf-8 -*-
"""
Timestamp Converter
Convert between timestamp and datetime
"""

from datetime import datetime

def timestamp_convert():
    """Timestamp converter"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        # If no selected text, prompt for input
        input_text = notepad.prompt(
            "Enter timestamp or date:\nExample: 1699123456 or 2023-11-04 12:34:56",
            "Timestamp Converter",
            ""
        )
        if input_text is None or not input_text.strip():
            return
        selected_text = input_text.strip()
        insert_result = True
    else:
        insert_result = False
    
    editor.beginUndoAction()
    try:
        # Try to determine if it's timestamp or datetime
        try:
            # Try as timestamp
            timestamp = float(selected_text.strip())
            # Check if it's seconds or milliseconds
            if timestamp > 1e12:
                timestamp = timestamp / 1000  # Convert milliseconds to seconds
            
            dt = datetime.fromtimestamp(timestamp)
            result = dt.strftime("%Y-%m-%d %H:%M:%S")
            result_type = "DateTime"
        except ValueError:
            # Try as datetime
            try:
                # Try multiple date formats
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%Y/%m/%d %H:%M:%S",
                    "%Y/%m/%d"
                ]
                
                dt = None
                for fmt in formats:
                    try:
                        dt = datetime.strptime(selected_text.strip(), fmt)
                        break
                    except ValueError:
                        continue
                
                if dt is None:
                    raise ValueError("Cannot parse date format")
                
                result = str(int(dt.timestamp()))
                result_type = "Timestamp (seconds)"
            except ValueError:
                notepad.messageBox(
                    "Cannot recognize timestamp or date format",
                    "Error",
                    0
                )
                return
        
        # Copy to clipboard (multiple methods)
        copied = False
        # Method 1: win32clipboard
        try:
            import win32clipboard
            import win32con
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, result)
            win32clipboard.CloseClipboard()
            copied = True
        except:
            # Method 2: tkinter
            try:
                import tkinter
                root = tkinter.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(result)
                root.update()
                root.destroy()
                copied = True
            except:
                # Method 3: Notepad++ copy function
                try:
                    doc_length = editor.getLength()
                    editor.insertText(doc_length, "\n" + result)
                    editor.setSelectionStart(doc_length + 1)
                    editor.setSelectionEnd(editor.getLength())
                    editor.copy()
                    editor.setSelectionStart(doc_length)
                    editor.setSelectionEnd(editor.getLength())
                    editor.replaceSel("")
                    copied = True
                except:
                    pass
        
        if copied:
            notepad.messageBox("Result: {}\n\nCopied to clipboard!".format(result), "Timestamp Converter - {}".format(result_type), 0)
        else:
            notepad.messageBox("Result: {}\n\n(Failed to copy to clipboard)".format(result), "Timestamp Converter - {}".format(result_type), 0)
    finally:
        editor.endUndoAction()

timestamp_convert()

