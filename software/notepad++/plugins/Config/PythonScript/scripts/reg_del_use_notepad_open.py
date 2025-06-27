# -*- coding: utf-8 -*-
import winreg  # Python 3 使用winreg而不是_winreg
import os
import sys

import re

def get_notepad_path():
    """自动获取Notepad++.exe路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 上溯3级目录到Notepad++安装目录
    base_dir = os.path.abspath(os.path.join(script_dir, "..","..", "..", ".."))
    exe_path = os.path.join(base_dir, "notepad++.exe")
    
    if not os.path.exists(exe_path):
        raise Exception(f"无法找到Notepad++.exe\n预期路径: {exe_path}")
    return exe_path

def update_batch_script(exe_path):
    """更新批处理脚本中的exe路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_path = os.path.join(script_dir, "添删右键菜单.bat")
    
    if not os.path.exists(batch_path):
        raise Exception("未找到批处理脚本")
    
    with open(batch_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换exe路径（对路径中的反斜杠进行转义）
    escaped_path = re.escape(exe_path)
    new_content = re.sub(
        r'set "exe_path=.*"',
        f'set "exe_path={exe_path.replace("\\", "\\\\")}"',
        content
    )
    
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def run_batch_script():
    """运行批处理脚本"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    batch_path = os.path.join(script_dir, "添删右键菜单.bat")
    
    if not os.path.exists(batch_path):
        raise Exception("未找到批处理脚本")
    
    try:
        os.startfile(batch_path)
    except Exception as e:
        raise Exception(f"运行批处理脚本失败: {e}")

if __name__ == "__main__":
    try:
        # 获取Notepad++路径
        exe_path = get_notepad_path()
        print(f"✅ 找到Notepad++.exe: {exe_path}")
        
        # 更新批处理脚本中的路径
        update_batch_script(exe_path)
        
        # 运行批处理脚本
        run_batch_script()
    except Exception as e:
        print(f"❌ 错误: {e}")