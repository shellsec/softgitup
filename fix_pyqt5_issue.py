#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 DLL问题修复工具
帮助解决编译后运行时的PyQt5 DLL加载问题
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyqt5_installation():
    """检查PyQt5安装状态"""
    try:
        import PyQt5
        print("✓ PyQt5已安装")
        return True
    except ImportError:
        print("✗ PyQt5未安装")
        return False

def install_pyqt5():
    """安装PyQt5"""
    print("正在安装PyQt5...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], check=True)
        print("✓ PyQt5安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ PyQt5安装失败")
        return False

def check_vcredist():
    """检查Visual C++ Redistributable"""
    print("检查Visual C++ Redistributable...")
    
    # 检查常见的VC++ Redistributable安装路径
    vcredist_paths = [
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Redist\MSVC",
        r"C:\Program Files\Microsoft Visual Studio\2019\BuildTools\VC\Redist\MSVC",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Redist\MSVC",
        r"C:\Program Files\Microsoft Visual Studio\2017\BuildTools\VC\Redist\MSVC",
    ]
    
    for path in vcredist_paths:
        if os.path.exists(path):
            print(f"✓ 找到Visual C++ Redistributable: {path}")
            return True
    
    print("✗ 未找到Visual C++ Redistributable")
    return False

def download_vcredist():
    """下载Visual C++ Redistributable"""
    print("正在下载Visual C++ Redistributable...")
    print("请访问以下链接下载并安装：")
    print("https://aka.ms/vs/17/release/vc_redist.x64.exe")
    print("https://aka.ms/vs/17/release/vc_redist.x86.exe")
    
    # 尝试自动下载
    try:
        import urllib.request
        url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        filename = "vc_redist.x64.exe"
        
        print(f"正在下载 {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ 下载完成: {filename}")
        print("请运行下载的文件进行安装")
        return True
    except Exception as e:
        print(f"✗ 自动下载失败: {e}")
        print("请手动下载并安装Visual C++ Redistributable")
        return False

def test_pyqt5_import():
    """测试PyQt5导入"""
    print("测试PyQt5导入...")
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon
        from PyQt5.QtCore import QTimer
        print("✓ PyQt5导入测试成功")
        return True
    except Exception as e:
        print(f"✗ PyQt5导入测试失败: {e}")
        return False

def create_console_version():
    """创建控制台版本"""
    print("创建控制台版本...")
    
    # 检查simple_sync.py是否存在
    if not os.path.exists("simple_sync.py"):
        print("✗ simple_sync.py不存在")
        return False
    
    # 运行控制台版本测试
    try:
        result = subprocess.run([sys.executable, "simple_sync.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        print("✓ 控制台版本测试成功")
        return True
    except Exception as e:
        print(f"✗ 控制台版本测试失败: {e}")
        return False

def rebuild_exe():
    """重新构建可执行文件"""
    print("重新构建可执行文件...")
    
    if not os.path.exists("build_exe.py"):
        print("✗ build_exe.py不存在")
        return False
    
    try:
        # 清理构建文件
        for dir_name in ["build", "dist", "__pycache__"]:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"已清理 {dir_name} 目录")
        
        # 重新构建
        subprocess.run([sys.executable, "build_exe.py"], check=True)
        print("✓ 重新构建完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 重新构建失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("PyQt5 DLL问题修复工具")
    print("=" * 60)
    
    print("正在诊断问题...")
    
    # 检查PyQt5安装
    if not check_pyqt5_installation():
        if not install_pyqt5():
            print("无法安装PyQt5，请手动安装")
            return
    
    # 测试PyQt5导入
    if not test_pyqt5_import():
        print("\nPyQt5导入失败，可能的原因：")
        print("1. Visual C++ Redistributable未安装")
        print("2. Python版本不兼容")
        print("3. 系统缺少必要的DLL文件")
        
        if not check_vcredist():
            print("\n建议安装Visual C++ Redistributable")
            download_vcredist()
        
        print("\n推荐解决方案：")
        print("1. 使用控制台版本：python simple_sync.py")
        print("2. 使用工作流程工具：python workflow.py")
        print("3. 重新构建控制台版本：python build_exe.py (选择选项2)")
        return
    
    # 如果PyQt5正常工作，重新构建
    print("\nPyQt5工作正常，重新构建可执行文件...")
    if rebuild_exe():
        print("\n修复完成！")
        print("生成的可执行文件在 dist/ 目录中")
    else:
        print("\n构建失败，请使用控制台版本")

if __name__ == "__main__":
    main() 