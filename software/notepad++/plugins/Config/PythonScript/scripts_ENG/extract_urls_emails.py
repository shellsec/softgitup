# -*- coding: utf-8 -*-
"""
Extract URLs and Emails
Extract all URLs and email addresses from document or selected text
"""

import re

def extract_urls_and_emails():
    """Extract URLs and emails"""
    selected_text = editor.getSelText()
    
    if selected_text:
        text = selected_text
        text_type = "selected text"
    else:
        text = editor.getText()
        text_type = "entire document"
    
    # Extract URLs (simple match)
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    
    # Extract emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Build result
    result_lines = []
    result_lines.append("Extracted from {}:\n".format(text_type))
    
    if urls:
        result_lines.append("\nURLs ({} total):\n".format(len(urls)))
        for i, url in enumerate(urls, 1):
            result_lines.append("{}. {}\n".format(i, url))
    else:
        result_lines.append("\nNo URLs found\n")
    
    if emails:
        result_lines.append("\nEmails ({} total):\n".format(len(emails)))
        for i, email in enumerate(emails, 1):
            result_lines.append("{}. {}\n".format(i, email))
    else:
        result_lines.append("\nNo emails found\n")
    
    result_text = ''.join(result_lines)
    
    # Display result
    if urls or emails:
        summary = "Extraction complete!\n\nURLs: {} \nEmails: {} \n\nResults copied to clipboard".format(len(urls), len(emails))
        notepad.messageBox(summary, "Extract URLs and Emails", 0)
    else:
        notepad.messageBox("No URLs or emails found", "Extract URLs and Emails", 0)
        return
    
    # Copy to clipboard (multiple methods)
    copied = False
    # Method 1: win32clipboard
    try:
        import win32clipboard
        import win32con
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, result_text)
        win32clipboard.CloseClipboard()
        copied = True
    except:
        # Method 2: tkinter
        try:
            import tkinter
            root = tkinter.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(result_text)
            root.update()
            root.destroy()
            copied = True
        except:
            # Method 3: Notepad++ copy function
            try:
                doc_length = editor.getLength()
                editor.insertText(doc_length, "\n" + result_text)
                editor.setSelectionStart(doc_length + 1)
                editor.setSelectionEnd(editor.getLength())
                editor.copy()
                editor.setSelectionStart(doc_length)
                editor.setSelectionEnd(editor.getLength())
                editor.replaceSel("")
                copied = True
            except:
                pass

extract_urls_and_emails()

