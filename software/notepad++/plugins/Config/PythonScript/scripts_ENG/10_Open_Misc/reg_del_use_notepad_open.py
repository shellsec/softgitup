# -*- coding: utf-8 -*-
import winreg  # Python 3 uses winreg instead of _winreg
import os
import sys

import re

def get_notepad_path():
    """Automatically get Notepad++.exe path"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up 3 levels to Notepad++ installation directory
    base_dir = os.path.abspath(os.path.join(script_dir, "..","..", "..", ".."))
    exe_path = os.path.join(base_dir, "notepad++.exe")
    
    if not os.path.exists(exe_path):
        raise Exception(f"Cannot find Notepad++.exe\nExpected path: {exe_path}")
    return exe_path

def update_batch_script(exe_path):
    """Update exe path in batch script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_path = os.path.join(script_dir, "manage_context_menu.bat")
    
    if not os.path.exists(batch_path):
        raise Exception("Batch script not found")
    
    with open(batch_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace exe path (escape backslashes in path)
    batch_escaped_path = exe_path.replace("\\", "\\\\")
    new_content = re.sub(
        r'set "exe_path=.*"',
        f'set "exe_path={batch_escaped_path}"',
        content
    )
    
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def run_batch_script():
    """Run batch script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_path = os.path.join(script_dir, "manage_context_menu.bat")
    
    if not os.path.exists(batch_path):
        raise Exception("Batch script not found")
    
    try:
        os.startfile(batch_path)
    except Exception as e:
        raise Exception(f"Failed to run batch script: {e}")

if __name__ == "__main__":
    try:
        # Get Notepad++ path
        exe_path = get_notepad_path()
        print(f"Found Notepad++.exe: {exe_path}")
        
        # Update path in batch script
        update_batch_script(exe_path)
        
        # Run batch script
        run_batch_script()
    except Exception as e:
        print(f"Error: {e}")
