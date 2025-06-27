#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 后台同步工具
后台运行，定时从GitHub同步软件更新
"""

import sys
import os
import json
import requests
import hashlib
import datetime
import schedule
import time
import threading
from pathlib import Path
import logging
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

class SyncSignals(QObject):
    """同步信号类"""
    update_available = pyqtSignal(str)
    sync_completed = pyqtSignal(bool, str)
    error_occurred = pyqtSignal(str)

class SoftSync:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.local_path = Path(self.config.get("sync_base_path", "D:/Program Files"))
        self.list_file = "software/" + self.config["list_file"]
        self.github_repo = self.config["github_repo"]
        self.sync_time = self.config["sync_time"]
        
        # 创建本地目录
        self.local_path.mkdir(exist_ok=True)
        
        # 信号
        self.signals = SyncSignals()
        
        # 应用和系统托盘
        self.app = None
        self.tray = None
        self.menu = None
        
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
                logging.FileHandler(log_dir / "sync.log", encoding='utf-8'),
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
        list_url = f"{self.github_repo}/raw/refs/heads/master/{self.list_file}"
        try:
            response = requests.get(list_url, timeout=30)
            response.raise_for_status()
            return json.loads(response.text)
        except Exception as e:
            self.logger.error(f"获取远程列表失败: {e}")
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
        # 处理Windows路径分隔符
        file_path = file_info['path'].replace('\\', '/')
        file_url = f"{self.github_repo}/raw/refs/heads/master/software/{software_name}/{file_path}"
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
                local_file_path.unlink()  # 删除损坏的文件
                return False
        return False
        
    def sync_software(self, software_name, remote_files, local_files):
        """同步单个软件"""
        self.logger.info(f"开始同步软件: {software_name}")
        
        software_path = self.local_path / software_name
        software_path.mkdir(exist_ok=True)
        
        updated_files = 0
        new_files = 0
        
        for file_info in remote_files:
            file_path = file_info['path']
            remote_hash = file_info['hash']
            
            local_file_path = software_path / file_path
            local_hash = None
            
            if local_file_path.exists():
                local_hash = self.calculate_file_hash(local_file_path)
                
            # 检查是否需要更新
            if not local_file_path.exists() or local_hash != remote_hash:
                if self.download_software_file(software_name, file_info):
                    if not local_file_path.exists():
                        new_files += 1
                    else:
                        updated_files += 1
                        
        self.logger.info(f"软件 {software_name} 同步完成: 新增 {new_files} 个文件, 更新 {updated_files} 个文件")
        return new_files + updated_files
        
    def perform_sync(self):
        """执行同步操作"""
        self.logger.info("开始执行同步操作")
        
        # 获取远程列表
        remote_list = self.get_remote_list()
        if not remote_list:
            self.signals.error_occurred.emit("无法获取远程软件列表")
            return False
            
        # 获取本地列表
        local_list = self.get_local_list()
        
        total_updated = 0
        
        for software_name, software_info in remote_list['software'].items():
            local_files = []
            if local_list and software_name in local_list['software']:
                local_files = local_list['software'][software_name]['files']
                
            updated_count = self.sync_software(
                software_name, 
                software_info['files'], 
                local_files
            )
            total_updated += updated_count
            
        # 更新本地列表文件
        local_list_path = Path("software") / self.config["list_file"]
        with open(local_list_path, 'w', encoding='utf-8') as f:
            json.dump(remote_list, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"同步完成，共更新 {total_updated} 个文件")
        
        if total_updated > 0:
            self.signals.sync_completed.emit(True, f"同步完成，更新了 {total_updated} 个文件")
        else:
            self.signals.sync_completed.emit(True, "同步完成，没有新更新")
            
        return True
        
    def setup_system_tray(self):
        """设置系统托盘"""
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 创建系统托盘图标
        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("SoftGitUp 同步工具")
        
        # 创建菜单
        self.menu = QMenu()
        
        # 手动同步
        sync_action = QAction("立即同步", self.menu)
        sync_action.triggered.connect(self.perform_sync)
        self.menu.addAction(sync_action)
        
        self.menu.addSeparator()
        
        # 查看日志
        log_action = QAction("查看日志", self.menu)
        log_action.triggered.connect(self.show_logs)
        self.menu.addAction(log_action)
        
        # 设置
        settings_action = QAction("设置", self.menu)
        settings_action.triggered.connect(self.show_settings)
        self.menu.addAction(settings_action)
        
        self.menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", self.menu)
        quit_action.triggered.connect(self.app.quit)
        self.menu.addAction(quit_action)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        # 连接信号
        self.signals.sync_completed.connect(self.on_sync_completed)
        self.signals.error_occurred.connect(self.on_error)
        
    def show_logs(self):
        """显示日志"""
        log_path = Path("logs/sync.log")
        if log_path.exists():
            os.startfile(log_path)
        else:
            QMessageBox.information(None, "日志", "日志文件不存在")
            
    def show_settings(self):
        """显示设置"""
        QMessageBox.information(None, "设置", f"同步时间: {self.sync_time}\n检查间隔: {self.config['check_interval']}秒")
        
    def on_sync_completed(self, success, message):
        """同步完成回调"""
        if success:
            self.tray.showMessage("SoftGitUp", message, QSystemTrayIcon.Information, 3000)
        else:
            self.tray.showMessage("SoftGitUp", f"同步失败: {message}", QSystemTrayIcon.Warning, 3000)
            
    def on_error(self, error_message):
        """错误回调"""
        self.tray.showMessage("SoftGitUp", f"错误: {error_message}", QSystemTrayIcon.Critical, 5000)
        
    def schedule_sync(self):
        """设置定时同步"""
        schedule.every().day.at(self.sync_time).do(self.perform_sync)
        self.logger.info(f"设置定时同步: 每天 {self.sync_time}")
        
    def run_scheduler(self):
        """运行调度器"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
            
    def run(self):
        """运行同步工具"""
        self.logger.info("启动SoftGitUp同步工具")
        
        # 设置系统托盘
        self.setup_system_tray()
        
        # 设置定时同步
        self.schedule_sync()
        
        # 启动调度器线程
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # 显示启动消息
        self.tray.showMessage("SoftGitUp", "同步工具已启动", QSystemTrayIcon.Information, 2000)
        
        # 运行应用
        sys.exit(self.app.exec_())
        
if __name__ == "__main__":
    sync_tool = SoftSync()
    sync_tool.run() 