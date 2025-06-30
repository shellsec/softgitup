#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 完整同步测试
测试所有软件的同步功能
"""

import os
import json
import hashlib
import datetime
import requests
import time
from pathlib import Path
import logging

class CompleteSyncTest:
    def __init__(self, config_file="config_system.json"):
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
                logging.FileHandler(log_dir / "complete_sync.log", encoding='utf-8'),
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
        # 使用gh-proxy.com作为有效的Git加速下载源
        mirrors = [
            "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
        ]
        
        for mirror in mirrors:
            # 构建列表文件URL
            list_url = f"{mirror}/refs/heads/master/{self.list_file}"
                
            try:
                self.logger.info(f"尝试从镜像源获取: {list_url}")
                response = requests.get(list_url, timeout=30)
                response.raise_for_status()
                return json.loads(response.text)
            except Exception as e:
                self.logger.warning(f"镜像源 {mirror} 失败: {e}")
                continue
                
        self.logger.error("镜像源失败了")
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
        # 使用gh-proxy.com作为有效的Git加速下载源
        mirrors = [
            "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
        ]
        
        for mirror in mirrors:
            # 处理Windows路径分隔符
            file_path = file_info['path'].replace('\\', '/')
            
            # 构建文件URL
            file_url = f"{mirror}/refs/heads/master/software/{software_name}/{file_path}"
                
            local_file_path = self.local_path / software_name / file_info['path']
            
            # 创建目录
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 下载文件
            if self.download_file(file_url, local_file_path):
                # 只检查文件是否下载成功，不验证哈希
                self.logger.info(f"文件下载成功: {file_info['path']}")
                return True
            else:
                self.logger.warning(f"从镜像源 {mirror} 下载失败: {file_info['path']}")
                continue
                
        self.logger.error(f"镜像源失败了: {file_info['path']}")
        return False
        
    def sync_software(self, software_name, remote_files, local_files):
        """同步单个软件"""
        self.logger.info(f"开始同步软件: {software_name}")
        
        software_path = self.local_path / software_name
        software_path.mkdir(exist_ok=True)
        
        updated_files = 0
        new_files = 0
        failed_files = 0
        
        for file_info in remote_files:
            file_path = file_info['path']
            remote_modified = file_info['modified']
            
            local_file_path = software_path / file_path
            local_modified = None
            
            if local_file_path.exists():
                local_modified = datetime.datetime.fromtimestamp(
                    local_file_path.stat().st_mtime
                ).isoformat()
                
            # 检查是否需要更新（使用修改时间而不是哈希值）
            if not local_file_path.exists() or local_modified != remote_modified:
                if self.download_software_file(software_name, file_info):
                    if not local_file_path.exists():
                        new_files += 1
                    else:
                        updated_files += 1
                else:
                    failed_files += 1
                        
        self.logger.info(f"软件 {software_name} 同步完成: 新增 {new_files} 个文件, 更新 {updated_files} 个文件, 失败 {failed_files} 个文件")
        return new_files + updated_files, failed_files
        
    def perform_complete_sync(self):
        """执行完整同步操作"""
        self.logger.info("开始执行完整同步操作")
        
        # 获取远程列表
        remote_list = self.get_remote_list()
        if not remote_list:
            self.logger.error("无法获取远程软件列表")
            return False
            
        # 获取本地列表
        local_list = self.get_local_list()
        
        total_updated = 0
        total_failed = 0
        sync_results = {}
        
        for software_name, software_info in remote_list['software'].items():
            local_files = []
            if local_list and software_name in local_list['software']:
                local_files = local_list['software'][software_name]['files']
                
            updated_count, failed_count = self.sync_software(
                software_name, 
                software_info['files'], 
                local_files
            )
            total_updated += updated_count
            total_failed += failed_count
            sync_results[software_name] = {
                'updated': updated_count,
                'failed': failed_count,
                'total_files': len(software_info['files'])
            }
            
        # 更新本地列表文件
        local_list_path = Path("software") / self.config["list_file"]
        with open(local_list_path, 'w', encoding='utf-8') as f:
            json.dump(remote_list, f, ensure_ascii=False, indent=2)
            
        # 输出同步结果摘要
        self.logger.info("=" * 50)
        self.logger.info("同步结果摘要:")
        self.logger.info(f"总软件数量: {len(remote_list['software'])}")
        self.logger.info(f"总文件数量: {remote_list['total_files']}")
        self.logger.info(f"成功更新: {total_updated} 个文件")
        self.logger.info(f"失败文件: {total_failed} 个文件")
        self.logger.info("=" * 50)
        
        for software_name, result in sync_results.items():
            self.logger.info(f"{software_name}: 更新 {result['updated']}/{result['total_files']} 个文件, 失败 {result['failed']} 个文件")
            
        self.logger.info("=" * 50)
        
        if total_updated > 0:
            self.logger.info(f"完整同步完成，更新了 {total_updated} 个文件")
        else:
            self.logger.info("完整同步完成，没有新更新")
            
        if total_failed > 0:
            self.logger.warning(f"有 {total_failed} 个文件同步失败")
            
        return True
        
    def run(self):
        """运行完整同步测试"""
        self.logger.info("开始运行完整同步测试")
        start_time = time.time()
        
        success = self.perform_complete_sync()
        
        end_time = time.time()
        duration = end_time - start_time
        
        if success:
            self.logger.info(f"完整同步测试完成，耗时 {duration:.2f} 秒")
        else:
            self.logger.error(f"完整同步测试失败，耗时 {duration:.2f} 秒")
            
if __name__ == "__main__":
    sync = CompleteSyncTest()
    sync.run() 