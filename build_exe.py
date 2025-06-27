#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将Python程序打包成单个可执行文件
支持多种打包选项
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败")
        return False

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理 {dir_name} 目录")
    
    # 清理.spec文件
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"已删除 {spec_file}")

def build_console_exe(script_name, exe_name):
    """构建控制台版本的可执行文件"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", exe_name,
        "--add-data", "config.json;.",
        script_name
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"{exe_name}.exe (控制台版本) 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def build_gui_exe(script_name, exe_name):
    """构建GUI版本的可执行文件"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", exe_name,
        "--add-data", "config.json;.",
        "--hidden-import", "PyQt5.QtWidgets",
        "--hidden-import", "PyQt5.QtGui", 
        "--hidden-import", "PyQt5.QtCore",
        "--hidden-import", "PyQt5.sip",
        "--collect-all", "PyQt5",
        script_name
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"{exe_name}.exe (GUI版本) 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def build_simple_exe(script_name, exe_name):
    """构建简单版本的可执行文件（无GUI依赖）"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", exe_name,
        "--add-data", "config.json;.",
        "--exclude-module", "PyQt5",
        script_name
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"{exe_name}.exe (简单版本) 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("SoftGitUp 打包工具")
    print("=" * 60)
    print("请选择打包选项:")
    print("1. 构建所有程序 (推荐)")
    print("2. 只构建控制台版本 (无GUI依赖)")
    print("3. 只构建GUI版本")
    print("4. 清理构建文件")
    print("5. 退出")
    print("=" * 60)
    
    while True:
        try:
            choice = input("请输入选择 (1-5): ").strip()
            
            if choice == "1":
                # 构建所有程序
                print("\n开始构建所有程序...")
                
                if not install_pyinstaller():
                    return
                
                clean_build()
                
                # 构建workflow.py (控制台版本)
                print("构建工作流程工具...")
                build_console_exe("workflow.py", "SoftGitUp_Workflow")
                
                # 构建soft_manager.py (GUI版本)
                print("构建管理工具...")
                build_gui_exe("soft_manager.py", "SoftGitUp_Manager")
                
                # 构建soft_sync.py (GUI版本)
                print("构建同步工具...")
                build_gui_exe("soft_sync.py", "SoftGitUp_Sync")
                
                print("\n所有程序构建完成！")
                print("生成的文件在 dist/ 目录中")
                break
                
            elif choice == "2":
                # 只构建控制台版本
                print("\n开始构建控制台版本...")
                
                if not install_pyinstaller():
                    return
                
                clean_build()
                
                # 构建workflow.py
                print("构建工作流程工具...")
                build_console_exe("workflow.py", "SoftGitUp_Workflow")
                
                # 构建简化版本的同步工具
                print("构建简化同步工具...")
                build_simple_exe("soft_sync.py", "SoftGitUp_Sync_Simple")
                
                print("\n控制台版本构建完成！")
                print("生成的文件在 dist/ 目录中")
                break
                
            elif choice == "3":
                # 只构建GUI版本
                print("\n开始构建GUI版本...")
                
                if not install_pyinstaller():
                    return
                
                clean_build()
                
                # 构建GUI版本
                print("构建管理工具...")
                build_gui_exe("soft_manager.py", "SoftGitUp_Manager")
                
                print("构建同步工具...")
                build_gui_exe("soft_sync.py", "SoftGitUp_Sync")
                
                print("\nGUI版本构建完成！")
                print("生成的文件在 dist/ 目录中")
                break
                
            elif choice == "4":
                # 清理构建文件
                print("\n清理构建文件...")
                clean_build()
                print("清理完成！")
                break
                
            elif choice == "5":
                print("退出")
                break
            else:
                print("无效选择，请输入 1-5")
                
        except KeyboardInterrupt:
            print("\n\n用户中断，退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break

if __name__ == "__main__":
    main() 