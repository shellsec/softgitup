#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证同步功能
"""

import json
import os
from pathlib import Path

def test_config():
    """测试配置文件"""
    print("=== 测试配置文件 ===")
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ 配置文件加载成功")
        print(f"  GitHub仓库: {config['github_repo']}")
        print(f"  同步时间: {config['sync_time']}")
        print(f"  软件数量: {len(config['software_dirs'])}")
        return True
    except Exception as e:
        print(f"✗ 配置文件加载失败: {e}")
        return False

def test_list_file():
    """测试列表文件"""
    print("\n=== 测试列表文件 ===")
    try:
        with open("list.txt", 'r', encoding='utf-8') as f:
            list_data = json.load(f)
        print("✓ 列表文件加载成功")
        print(f"  生成时间: {list_data['generated_at']}")
        print(f"  软件数量: {list_data['total_software']}")
        print(f"  文件总数: {list_data['total_files']}")
        
        for software_name, software_info in list_data['software'].items():
            print(f"  - {software_name}: {software_info['total_files']} 个文件")
        return True
    except Exception as e:
        print(f"✗ 列表文件加载失败: {e}")
        return False

def test_software_dirs():
    """测试软件目录"""
    print("\n=== 测试软件目录 ===")
    software_path = Path("software")
    if not software_path.exists():
        print("✗ software目录不存在")
        return False
        
    config = json.load(open("config.json", 'r', encoding='utf-8'))
    all_exist = True
    
    for software_name in config['software_dirs']:
        software_dir = software_path / software_name
        if software_dir.exists():
            file_count = len(list(software_dir.rglob("*")))
            print(f"✓ {software_name}: {file_count} 个文件")
        else:
            print(f"✗ {software_name}: 目录不存在")
            all_exist = False
            
    return all_exist

def test_logs():
    """测试日志文件"""
    print("\n=== 测试日志文件 ===")
    log_dir = Path("logs")
    if log_dir.exists():
        log_files = list(log_dir.glob("*.log"))
        if log_files:
            print("✓ 日志文件存在:")
            for log_file in log_files:
                size = log_file.stat().st_size
                print(f"  - {log_file.name}: {size} 字节")
        else:
            print("✗ 没有找到日志文件")
            return False
    else:
        print("✗ logs目录不存在")
        return False
    return True

def main():
    """主测试函数"""
    print("SoftGitUp 功能测试")
    print("=" * 50)
    
    tests = [
        test_config,
        test_list_file,
        test_software_dirs,
        test_logs
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！系统配置正确。")
    else:
        print("✗ 部分测试失败，请检查配置。")

if __name__ == "__main__":
    main() 