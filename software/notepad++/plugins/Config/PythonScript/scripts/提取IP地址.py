# -*- coding: utf-8 -*-
"""
Extract IP Addresses Script
Function: Extract all IPv4 and IPv6 addresses from document or selected text
"""

import re

def extract_ip_addresses():
    """Extract IPv4 and IPv6 addresses"""
    selected_text = editor.getSelText()
    
    if selected_text:
        text = selected_text
        text_type = "selected text"
    else:
        text = editor.getText()
        text_type = "entire document"
    
    # Extract IPv4 addresses (valid ones only)
    ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ipv4_addresses = re.findall(ipv4_pattern, text)
    
    # Extract IPv6 addresses (simplified but accurate pattern)
    ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b|\b(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}\b|\b(?:[0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}\b|\b(?:[0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}\b|\b[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})\b|\b:((:[0-9a-fA-F]{1,4}){1,7}|:)\b|\bfe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}\b|\b::(ffff(?::0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\b|\b(?:[0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\b'
    ipv6_addresses = re.findall(ipv6_pattern, text)
    
    # Build result
    result_lines = []
    result_lines.append("Extracted from {}:\n".format(text_type))
    
    if ipv4_addresses:
        result_lines.append("\nIPv4 Addresses ({} total):\n".format(len(ipv4_addresses)))
        for i, ip in enumerate(ipv4_addresses, 1):
            result_lines.append("{}. {}\n".format(i, ip))
    else:
        result_lines.append("\nNo IPv4 addresses found\n")
    
    if ipv6_addresses:
        result_lines.append("\nIPv6 Addresses ({} total):\n".format(len(ipv6_addresses)))
        for i, ip in enumerate(ipv6_addresses, 1):
            result_lines.append("{}. {}\n".format(i, ip))
    else:
        result_lines.append("\nNo IPv6 addresses found\n")
    
    result_text = ''.join(result_lines)
    
    # Display result
    if ipv4_addresses or ipv6_addresses:
        summary = "Extraction complete!\n\nIPv4: {} \nIPv6: {} \n\nResults copied to clipboard".format(len(ipv4_addresses), len(ipv6_addresses))
        notepad.messageBox(summary, "Extract IP Addresses", 0)
    else:
        notepad.messageBox("No IP addresses found", "Extract IP Addresses", 0)
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

extract_ip_addresses()

