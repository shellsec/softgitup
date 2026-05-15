# -*- coding: utf-8 -*-
"""
Extract Phone Numbers Script
Function: Extract all phone numbers from document or selected text
Supports: Chinese mobile/landline numbers and international phone numbers
"""

import re

def extract_phone_numbers():
    """Extract phone numbers"""
    selected_text = editor.getSelText()
    
    if selected_text:
        text = selected_text
        text_type = "selected text"
    else:
        text = editor.getText()
        text_type = "entire document"
    
    # Extract Chinese mobile numbers (11 digits starting with 1)
    # Format examples: 13812345678, 138-1234-5678, 138 1234 5678
    chinese_mobile_pattern = r'\b1[3-9]\d{9}\b|\b1[3-9]\d{2}[-\s]\d{4}[-\s]\d{4}\b'
    chinese_mobile_numbers = re.findall(chinese_mobile_pattern, text)
    
    # Extract Chinese landline numbers
    # Format examples: 010-12345678, 021-87654321, 0571-12345678
    chinese_landline_pattern = r'\b0\d{2,3}[-\s]\d{7,8}\b'
    chinese_landline_numbers = re.findall(chinese_landline_pattern, text)
    
    # Extract international phone numbers
    # Format examples: +1-555-123-4567, +44 20 1234 5678, +86 138 1234 5678
    international_pattern = r'\+\d{1,3}[-\s]\d{1,4}[-\s]\d{1,4}[-\s]\d{1,9}\b'
    international_numbers = re.findall(international_pattern, text)
    
    # Build result
    result_lines = []
    result_lines.append("Extracted from {}:\n".format(text_type))
    
    if chinese_mobile_numbers:
        result_lines.append("\nChinese Mobile Numbers ({} total):\n".format(len(chinese_mobile_numbers)))
        for i, number in enumerate(chinese_mobile_numbers, 1):
            result_lines.append("{}. {}\n".format(i, number))
    else:
        result_lines.append("\nNo Chinese mobile numbers found\n")
    
    if chinese_landline_numbers:
        result_lines.append("\nChinese Landline Numbers ({} total):\n".format(len(chinese_landline_numbers)))
        for i, number in enumerate(chinese_landline_numbers, 1):
            result_lines.append("{}. {}\n".format(i, number))
    else:
        result_lines.append("\nNo Chinese landline numbers found\n")
    
    if international_numbers:
        result_lines.append("\nInternational Phone Numbers ({} total):\n".format(len(international_numbers)))
        for i, number in enumerate(international_numbers, 1):
            result_lines.append("{}. {}\n".format(i, number))
    else:
        result_lines.append("\nNo international phone numbers found\n")
    
    result_text = ''.join(result_lines)
    
    # Display result
    if chinese_mobile_numbers or chinese_landline_numbers or international_numbers:
        summary = "Extraction complete!\n\nChinese Mobile: {} \nChinese Landline: {} \nInternational: {} \n\nResults copied to clipboard".format(len(chinese_mobile_numbers), len(chinese_landline_numbers), len(international_numbers))
        notepad.messageBox(summary, "Extract Phone Numbers", 0)
    else:
        notepad.messageBox("No phone numbers found", "Extract Phone Numbers", 0)
        return
    
    # Copy to clipboard
    try:
        # Method 1: Try using win32clipboard (Windows, most reliable)
        try:
            import win32clipboard
            import win32con
            
            # Ensure text is Unicode string
            if isinstance(result_text, bytes):
                result_text = result_text.decode('utf-8')
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            # Use CF_UNICODETEXT format, Windows handles encoding automatically
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, result_text)
            win32clipboard.CloseClipboard()
        except ImportError:
            # Method 2: Use tkinter (cross-platform, but needs tkinter)
            try:
                import tkinter
                root = tkinter.Tk()
                root.withdraw()  # Hide window
                root.clipboard_clear()
                root.clipboard_append(result_text)
                root.update()  # Ensure copy completes
                root.destroy()
            except:
                # Method 3: Use Windows clip command (Windows 10+)
                try:
                    import subprocess
                    import sys
                    # Use UTF-8 encoding
                    if sys.version_info[0] >= 3:
                        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                        process.communicate(input=result_text.encode('utf-8'))
                    else:
                        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                        process.communicate(input=result_text.encode('utf-8'))
                    process.wait()
                except:
                    # Method 4: Use Notepad++ copy function (most reliable, ensures correct encoding)
                    # Save current selection and position
                    old_sel_start = editor.getSelectionStart()
                    old_sel_end = editor.getSelectionEnd()
                    
                    # Insert result at end of document and select
                    doc_length = editor.getLength()
                    editor.beginUndoAction()
                    try:
                        editor.insertText(doc_length, "\n" + result_text)
                        editor.setSelectionStart(doc_length + 1)
                        editor.setSelectionEnd(editor.getLength())
                        
                        # Copy selected content
                        editor.copy()
                        
                        # Restore original document (delete inserted content)
                        editor.setSelectionStart(doc_length)
                        editor.setSelectionEnd(editor.getLength())
                        editor.replaceSel("")
                    finally:
                        editor.endUndoAction()
                    
                    # Restore original selection
                    if old_sel_start != old_sel_end:
                        editor.setSelectionStart(old_sel_start)
                        editor.setSelectionEnd(old_sel_end)
        except Exception as e:
            # If win32clipboard fails, try method 4
            try:
                old_sel_start = editor.getSelectionStart()
                old_sel_end = editor.getSelectionEnd()
                
                doc_length = editor.getLength()
                editor.beginUndoAction()
                try:
                    editor.insertText(doc_length, "\n" + result_text)
                    editor.setSelectionStart(doc_length + 1)
                    editor.setSelectionEnd(editor.getLength())
                    editor.copy()
                    editor.setSelectionStart(doc_length)
                    editor.setSelectionEnd(editor.getLength())
                    editor.replaceSel("")
                finally:
                    editor.endUndoAction()
                
                if old_sel_start != old_sel_end:
                    editor.setSelectionStart(old_sel_start)
                    editor.setSelectionEnd(old_sel_end)
            except Exception as e2:
                notepad.messageBox("Failed to copy to clipboard: {}\n\nPlease try copying manually".format(str(e2)), "Error", 0)
    except Exception as e:
        notepad.messageBox("Failed to copy to clipboard: {}\n\nPlease try copying manually".format(str(e)), "Error", 0)

extract_phone_numbers()

