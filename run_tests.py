#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 测试运行器
提供多种测试选项来验证同步功能
"""

import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("SoftGitUp 同步测试工具")
    print("=" * 60)
    print("请选择测试类型:")
    print("1. 简单同步测试 (只同步 everything 软件)")
    print("2. 完整同步测试 (同步所有软件)")
    print("3. 基础同步测试 (使用 test_sync.py)")
    print("4. 生成软件列表 (使用 soft_manager.py)")
    print("5. 退出")
    print("=" * 60)
    
    while True:
        try:
            choice = input("请输入选择 (1-5): ").strip()
            
            if choice == "1":
                print("\n开始简单同步测试...")
                os.system("python test_simple_sync.py")
                break
            elif choice == "2":
                print("\n开始完整同步测试...")
                os.system("python test_complete_sync.py")
                break
            elif choice == "3":
                print("\n开始基础同步测试...")
                os.system("python test_sync.py")
                break
            elif choice == "4":
                print("\n开始生成软件列表...")
                os.system("python soft_manager.py")
                break
            elif choice == "5":
                print("退出测试")
                break
            else:
                print("无效选择，请输入 1-5")
                
        except KeyboardInterrupt:
            print("\n\n用户中断，退出测试")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break
    
    print("\n测试完成！")
    print("日志文件保存在 logs/ 目录下:")
    print("- simple_sync.log: 简单同步测试日志")
    print("- complete_sync.log: 完整同步测试日志")
    print("- test_sync.log: 基础同步测试日志")
    print("- manager.log: 软件管理工具日志")

if __name__ == "__main__":
    main() 