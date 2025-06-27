#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将Python程序打包成单个可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller安装成功")
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败")
        return False
    return True

def build_exe(script_name, exe_name):
    """构建可执行文件"""
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口
        "--name", exe_name,
        "--add-data", "config.json;.",  # 包含配置文件
        script_name
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"{exe_name}.exe 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def main():
    """主函数"""
    print("开始构建SoftGitUp可执行文件...")
    
    # 检查PyInstaller
    if not install_pyinstaller():
        return
    
    # 构建管理工具
    print("构建管理工具...")
    if build_exe("soft_manager.py", "SoftGitUp_Manager"):
        print("管理工具构建完成")
    
    # 构建同步工具
    print("构建同步工具...")
    if build_exe("soft_sync.py", "SoftGitUp_Sync"):
        print("同步工具构建完成")
    
    print("所有可执行文件构建完成！")
    print("生成的文件在 dist/ 目录中")

if __name__ == "__main__":
    main() 