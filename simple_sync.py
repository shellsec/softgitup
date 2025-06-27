#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 简化同步工具
不依赖GUI，提供基本的同步功能
"""

import sys
import os
import json
import requests
import datetime
import time
from pathlib import Path
import logging

class SimpleSync:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.local_path = Path(self.config.get("sync_base_path", "D:/Program Files"))
        self.list_file = "software/" + self.config["list_file"]
        self.github_repo = self.config["github_repo"]
        
        # 创建本地目录
        self.local_path.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_file} 不存在")
            return {}
            
    def setup_logging(self):
        """设置日志"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, self.config.get("log_level", "INFO")),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "simple_sync.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def download_file(self, url, local_path):
        """下载文件"""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            self.logger.error(f"下载文件失败: {url}, 错误: {e}")
            return False
            
    def get_remote_list(self):
        """获取远程列表文件"""
        # 使用配置文件中的gh-proxy.com加速源
        mirrors = self.config.get("git_mirrors", [self.github_repo])
        
        for mirror in mirrors:
            list_url = f"{mirror}/refs/heads/master/{self.list_file}"
            try:
                self.logger.info(f"尝试从镜像源获取: {list_url}")
                response = requests.get(list_url, timeout=30)
                response.raise_for_status()
                return json.loads(response.text)
            except Exception as e:
                self.logger.warning(f"镜像源 {mirror} 失败: {e}")
                continue
                
        self.logger.error("所有镜像源都失败了")
        return None
            
    def get_local_list(self):
        """获取本地列表文件"""
        # 从项目根目录的software文件夹读取list.txt
        local_list_path = Path("software") / self.config["list_file"]
        if local_list_path.exists():
            try:
                with open(local_list_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"读取本地列表失败: {e}")
        return None
        
    def download_software_file(self, software_name, file_info):
        """下载软件文件"""
        # 使用配置文件中的gh-proxy.com加速源
        mirrors = self.config.get("git_mirrors", [self.github_repo])
        
        for mirror in mirrors:
            # 处理Windows路径分隔符
            file_path = file_info['path'].replace('\\', '/')
            file_url = f"{mirror}/refs/heads/master/software/{software_name}/{file_path}"
            local_file_path = self.local_path / software_name / file_info['path']
            
            # 创建目录
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 下载文件
            if self.download_file(file_url, local_file_path):
                self.logger.info(f"文件下载成功: {file_info['path']}")
                return True
            else:
                self.logger.warning(f"从镜像源 {mirror} 下载失败: {file_info['path']}")
                continue
                
        self.logger.error(f"所有镜像源都失败了: {file_info['path']}")
        return False
        
    def sync_software(self, software_name, remote_files):
        """同步单个软件"""
        self.logger.info(f"开始同步软件: {software_name}")
        
        software_path = self.local_path / software_name
        software_path.mkdir(exist_ok=True)
        
        updated_files = 0
        new_files = 0
        
        for file_info in remote_files:
            file_path = file_info['path']
            remote_modified = file_info['modified']
            
            local_file_path = software_path / file_path
            local_modified = None
            
            if local_file_path.exists():
                local_modified = datetime.datetime.fromtimestamp(
                    local_file_path.stat().st_mtime
                ).isoformat()
                
            # 检查是否需要更新（使用修改时间）
            if not local_file_path.exists() or local_modified != remote_modified:
                if self.download_software_file(software_name, file_info):
                    if not local_file_path.exists():
                        new_files += 1
                    else:
                        updated_files += 1
                        
        self.logger.info(f"软件 {software_name} 同步完成: 新增 {new_files} 个文件, 更新 {updated_files} 个文件")
        return new_files + updated_files
        
    def perform_sync(self, software_name=None):
        """执行同步操作"""
        self.logger.info("开始执行同步操作")
        
        # 获取远程列表
        remote_list = self.get_remote_list()
        if not remote_list:
            self.logger.error("无法获取远程软件列表")
            return False
            
        # 获取本地列表
        local_list = self.get_local_list()
        
        total_updated = 0
        
        if software_name:
            # 同步指定软件
            if software_name in remote_list:
                updated = self.sync_software(software_name, remote_list[software_name])
                total_updated += updated
                self.logger.info(f"软件 {software_name} 同步完成，更新了 {updated} 个文件")
            else:
                self.logger.error(f"软件 {software_name} 在远程列表中不存在")
                return False
        else:
            # 同步所有软件
            for software_name, remote_files in remote_list.items():
                updated = self.sync_software(software_name, remote_files)
                total_updated += updated
                
        self.logger.info(f"同步操作完成，总共更新了 {total_updated} 个文件")
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("SoftGitUp 简化同步工具")
    print("=" * 60)
    
    # 检查命令行参数
    software_name = None
    if len(sys.argv) > 1:
        software_name = sys.argv[1]
        print(f"将同步软件: {software_name}")
    else:
        print("将同步所有软件")
    
    print("=" * 60)
    
    # 创建同步器并执行同步
    sync = SimpleSync()
    success = sync.perform_sync(software_name)
    
    if success:
        print("同步操作完成！")
    else:
        print("同步操作失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 