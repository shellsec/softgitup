#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 工作流程工具
方便更新单个软件并同步
"""

import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("SoftGitUp 工作流程工具")
    print("=" * 60)
    print("请选择操作:")
    print("1. 更新单个软件并生成列表")
    print("2. 同步单个软件")
    print("3. 同步所有软件")
    print("4. 生成完整软件列表")
    print("5. 退出")
    print("=" * 60)
    
    while True:
        try:
            choice = input("请输入选择 (1-5): ").strip()
            
            if choice == "1":
                # 更新单个软件并生成列表
                software_name = input("请输入软件名称 (如: everything): ").strip()
                if software_name:
                    print(f"\n开始更新软件: {software_name}")
                    # 这里可以添加更新软件的逻辑
                    print("请手动更新软件文件到 software/ 目录下")
                    
                    print(f"\n生成软件列表: {software_name}")
                    os.system(f"python -c \"from soft_manager import SoftManager; SoftManager().generate_list_file('{software_name}')\"")
                    
                    print(f"\n推送到GitHub")
                    os.system("python -c \"from soft_manager import SoftManager; SoftManager().git_commit_and_push()\"")
                    
                    print(f"软件 {software_name} 更新完成！")
                break
                
            elif choice == "2":
                # 同步单个软件
                software_name = input("请输入软件名称 (如: everything): ").strip()
                if software_name:
                    print(f"\n开始同步软件: {software_name}")
                    os.system(f"python simple_sync.py {software_name}")
                break
                
            elif choice == "3":
                # 同步所有软件
                print("\n开始同步所有软件")
                os.system("python simple_sync.py")
                break
                
            elif choice == "4":
                # 生成完整软件列表
                print("\n开始生成完整软件列表")
                os.system("python soft_manager.py")
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
    
    print("\n操作完成！")

if __name__ == "__main__":
    main() 