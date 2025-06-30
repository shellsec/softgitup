#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 本地软件管理工具
用于管理本地软件目录，生成文件索引和版本列表
"""

import os
import json
import hashlib
import datetime
import git
from pathlib import Path
import logging

class SoftManager:
    def __init__(self, config_file="config_system.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.local_path = Path(self.config.get("manager_base_path", "./software"))
        self.list_file = self.local_path / self.config["list_file"]
        
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
                logging.FileHandler(log_dir / "manager.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def calculate_file_hash(self, file_path):
        """计算文件MD5哈希"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"计算文件哈希失败: {file_path}, 错误: {e}")
            return None
            
    def scan_software_directory(self, software_name):
        """扫描软件目录，生成文件列表"""
        software_path = self.local_path / software_name
        if not software_path.exists():
            self.logger.warning(f"软件目录不存在 {software_path}")
            return []
            
        files_info = []
        for file_path in software_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(software_path)
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    files_info.append({
                        "path": str(relative_path),
                        "size": file_path.stat().st_size,
                        "hash": file_hash,
                        "modified": datetime.datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat()
                    })
                    
        return files_info
        
    def generate_list_file(self, software_name=None):
        """生成软件列表文件"""
        software_list = {}
        total_files = 0
        
        # 如果指定了软件名称，只扫描该软件
        if software_name:
            if software_name in self.config["software_dirs"]:
                self.logger.info(f"扫描软件: {software_name}")
                files_info = self.scan_software_directory(software_name)
                if files_info:
                    software_list[software_name] = {
                        "version": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "files": files_info,
                        "total_files": len(files_info),
                        "total_size": sum(f["size"] for f in files_info),
                        "last_updated": datetime.datetime.now().isoformat()
                    }
                    total_files += len(files_info)
        else:
            # 扫描所有软件
            for software_name in self.config["software_dirs"]:
                self.logger.info(f"扫描软件: {software_name}")
                files_info = self.scan_software_directory(software_name)
                if files_info:
                    software_list[software_name] = {
                        "version": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "files": files_info,
                        "total_files": len(files_info),
                        "total_size": sum(f["size"] for f in files_info),
                        "last_updated": datetime.datetime.now().isoformat()
                    }
                    total_files += len(files_info)
                
        # 生成list.txt内容
        list_content = {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_software": len(software_list),
            "total_files": total_files,
            "software": software_list
        }
        
        # 保存到文件
        with open(self.list_file, 'w', encoding='utf-8') as f:
            json.dump(list_content, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"生成列表文件完成: {self.list_file}")
        self.logger.info(f"包含 {len(software_list)} 个软件，共 {total_files} 个文件")
        
        return list_content
        
    def git_commit_and_push(self):
        """Git提交并推送到远程仓库"""
        try:
            repo = git.Repo(".")
            
            # 添加所有更改
            repo.index.add([self.list_file])
            
            # 提交更改
            commit_message = f"更新软件列表 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            repo.index.commit(commit_message)
            
            # 推送到远程
            origin = repo.remote(name='origin')
            origin.push()
            
            self.logger.info("成功推送到GitHub")
            return True
            
        except git.exc.InvalidGitRepositoryError:
            self.logger.error("当前目录不是Git仓库")
            return False
        except Exception as e:
            self.logger.error(f"Git操作失败: {e}")
            return False
            
    def run(self):
        """运行管理工具"""
        self.logger.info("开始运行软件管理工具")
        
        # 生成列表文件
        list_content = self.generate_list_file()
        
        # Git提交和推送
        if self.git_commit_and_push():
            self.logger.info("软件管理完成")
        else:
            self.logger.warning("Git推送失败，但列表文件已生成")
            
if __name__ == "__main__":
    manager = SoftManager()
    manager.run() 
