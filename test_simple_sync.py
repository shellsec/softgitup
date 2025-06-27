#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 简单同步测试
只同步everything软件包进行测试
"""

import os
import json
import hashlib
import datetime
import requests
import time
from pathlib import Path
import logging

class SimpleSyncTest:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.local_path = Path(self.config.get("sync_base_path", "D:/Program Files"))
        self.list_file = self.config["list_file"]
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
        # 尝试多个镜像源
        mirrors = [
            "https://raw.githubusercontent.com/shellsec/softgitup/master",
            "https://ghproxy.com/https://raw.githubusercontent.com/shellsec/softgitup/master",
            "https://raw.fastgit.org/shellsec/softgitup/master",
            "https://hub.fastgit.xyz/shellsec/softgitup/raw/master"
        ]
        
        for mirror in mirrors:
            list_url = f"{mirror}/{self.list_file}"
            try:
                self.logger.info(f"尝试从镜像源获取: {list_url}")
                response = requests.get(list_url, timeout=30)
                response.raise_for_status()
                return json.loads(response.text)
            except Exception as e:
                self.logger.warning(f"镜像源失败: {e}")
                continue
                
        self.logger.error("所有镜像源都失败了")
        return None
        
    def calculate_file_hash(self, file_path):
        """计算文件MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"计算文件哈希失败: {file_path}, 错误: {e}")
            return None
            
    def download_software_file(self, software_name, file_info):
        """下载软件文件"""
        # 尝试多个镜像源
        mirrors = [
            "https://raw.githubusercontent.com/shellsec/softgitup/master",
            "https://ghproxy.com/https://raw.githubusercontent.com/shellsec/softgitup/master",
            "https://raw.fastgit.org/shellsec/softgitup/master",
            "https://hub.fastgit.xyz/shellsec/softgitup/raw/master"
        ]
        
        for mirror in mirrors:
            file_url = f"{mirror}/software/{software_name}/{file_info['path']}"
            local_file_path = self.local_path / software_name / file_info['path']
            
            # 创建目录
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 下载文件
            if self.download_file(file_url, local_file_path):
                # 验证哈希
                local_hash = self.calculate_file_hash(local_file_path)
                if local_hash == file_info['hash']:
                    self.logger.info(f"文件下载成功: {file_info['path']}")
                    return True
                else:
                    self.logger.error(f"文件哈希验证失败: {file_info['path']}")
                    self.logger.error(f"期望哈希: {file_info['hash']}")
                    self.logger.error(f"实际哈希: {local_hash}")
                    local_file_path.unlink()  # 删除损坏的文件
                    continue
            else:
                self.logger.warning(f"从镜像源下载失败: {file_info['path']}")
                continue
                
        self.logger.error(f"所有镜像源都失败了: {file_info['path']}")
        return False
        
    def sync_everything(self):
        """只同步everything软件"""
        self.logger.info("开始同步everything软件")
        
        # 获取远程列表
        remote_list = self.get_remote_list()
        if not remote_list:
            self.logger.error("无法获取远程软件列表")
            return False
            
        # 只同步everything
        if "everything" not in remote_list['software']:
            self.logger.error("远程列表中没有everything软件")
            return False
            
        software_info = remote_list['software']['everything']
        files_info = software_info['files']
        
        software_path = self.local_path / "everything"
        software_path.mkdir(exist_ok=True)
        
        updated_files = 0
        new_files = 0
        
        for file_info in files_info:
            file_path = file_info['path']
            remote_hash = file_info['hash']
            
            local_file_path = software_path / file_path
            local_hash = None
            
            if local_file_path.exists():
                local_hash = self.calculate_file_hash(local_file_path)
                
            # 检查是否需要更新
            if not local_file_path.exists() or local_hash != remote_hash:
                if self.download_software_file("everything", file_info):
                    if not local_file_path.exists():
                        new_files += 1
                    else:
                        updated_files += 1
                        
        self.logger.info(f"everything软件同步完成: 新增 {new_files} 个文件, 更新 {updated_files} 个文件")
        return new_files + updated_files
        
    def run(self):
        """运行简单同步测试"""
        self.logger.info("开始运行简单同步测试")
        success = self.sync_everything()
        if success:
            self.logger.info("简单同步测试完成")
        else:
            self.logger.error("简单同步测试失败")
            
if __name__ == "__main__":
    sync = SimpleSyncTest()
    sync.run() 