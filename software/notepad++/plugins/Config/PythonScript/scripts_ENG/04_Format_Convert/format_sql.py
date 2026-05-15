# -*- coding: utf-8 -*-
"""
SQL Formatter
Format SQL statements to make them more readable
"""

import re

def format_sql():
    """Format SQL"""
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
        notepad.messageBox("No content to format", "SQL Formatter", 0)
        return
    
    editor.beginUndoAction()
    try:
        # SQL keywords list
        sql_keywords = [
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET',
            'DELETE', 'CREATE', 'TABLE', 'ALTER', 'DROP', 'INDEX', 'VIEW', 'DATABASE',
            'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'BEGIN', 'TRANSACTION',
            'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN', 'IS', 'NULL',
            'ORDER', 'BY', 'GROUP', 'HAVING', 'JOIN', 'INNER', 'LEFT', 'RIGHT',
            'OUTER', 'ON', 'AS', 'DISTINCT', 'UNION', 'ALL', 'EXISTS',
            'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'IF', 'ELSEIF'
        ]
        
        # Convert SQL keywords to uppercase
        formatted = selected_text
        for keyword in sql_keywords:
            # Use word boundary matching to avoid false replacements
            pattern = r'\b' + re.escape(keyword) + r'\b'
            formatted = re.sub(pattern, keyword, formatted, flags=re.IGNORECASE)
        
        # Simple indentation handling
        lines = formatted.split('\n')
        indent_level = 0
        indent_size = 4
        formatted_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Keywords that decrease indentation
            if re.match(r'^\s*(END|ELSE|ELSEIF|ENDIF|END CASE)', stripped, re.IGNORECASE):
                indent_level = max(0, indent_level - 1)
            
            # Add indentation
            indented_line = ' ' * (indent_level * indent_size) + stripped
            formatted_lines.append(indented_line)
            
            # Keywords that increase indentation
            if re.match(r'^\s*(IF|CASE|WHEN|THEN|ELSE|ELSEIF)', stripped, re.IGNORECASE):
                indent_level += 1
            elif re.match(r'^\s*(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|CREATE|ALTER)', stripped, re.IGNORECASE):
                # Check for clauses
                if re.search(r'\b(WHERE|ORDER|GROUP|HAVING|JOIN)\b', stripped, re.IGNORECASE):
                    pass  # Don't increase indentation
                else:
                    indent_level += 1
        
        formatted = '\n'.join(formatted_lines)
        
        # Replace text
        editor.setSelection(start_pos, end_pos)
        editor.replaceSel(formatted)
        notepad.messageBox("SQL formatted successfully", "SQL Formatter", 0)
    except Exception as e:
        notepad.messageBox(
            "Format failed: {}".format(str(e)),
            "Error",
            0
        )
    finally:
        editor.endUndoAction()

format_sql()

