#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 完整同步测试
测试所有软件的同步功能

          $$\                 $$\ $$\                               
          $$ |                $$ |$$ |                              
 $$$$$$$\ $$$$$$$\   $$$$$$\  $$ |$$ | $$$$$$$\  $$$$$$\   $$$$$$$\ 
$$  _____|$$  __$$\ $$  __$$\ $$ |$$ |$$  _____|$$  __$$\ $$  _____|
\$$$$$$\  $$ |  $$ |$$$$$$$$ |$$ |$$ |\$$$$$$\  $$$$$$$$ |$$ /      
 \____$$\ $$ |  $$ |$$   ____|$$ |$$ | \____$$\ $$   ____|$$ |      
$$$$$$$  |$$ |  $$ |\$$$$$$$\ $$ |$$ |$$$$$$$  |\$$$$$$$\ \$$$$$$$\ 
\_______/ \__|  \__| \_______|\__|\__|\_______/  \_______| \_______|
                                                                    
                                                                    
"""

import os
import json
import hashlib
import datetime
import requests
import time
from pathlib import Path
import logging
import subprocess
import sys

class CompleteSyncTest:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        # 先检测路径（在日志设置之前）
        self.local_path = Path(self.get_sync_base_path())
        self.setup_logging()
        # 记录检测到的路径
        self.logger.info(f"使用同步路径: {self.local_path}")
        self.list_file = "software/" + self.config["list_file"]
        self.git_platform = self.config.get("git_platform", "github").lower()
        self.github_repo = self.config.get("github_repo", "")
        self.gitlab_repo = self.config.get("gitlab_repo", "")
        
        # 创建本地目录
        self.local_path.mkdir(exist_ok=True)
    
    def get_sync_base_path(self):
        """获取同步路径，如果为空则使用当前根目录"""
        # 如果配置中有指定路径，优先使用
        configured_path = self.config.get("sync_base_path", "").strip()
        if configured_path:
            path = Path(configured_path)
            if path.exists():
                return path
            else:
                # 如果配置的路径不存在，创建它
                path.mkdir(parents=True, exist_ok=True)
                return path
        
        # 如果配置为空，使用可执行文件所在目录
        # 注意：Nuitka 编译后，__file__ 指向临时构建目录，需要使用可执行文件路径
        if hasattr(sys, 'frozen') and sys.frozen:
            # 编译后的可执行文件
            # 使用可执行文件所在目录作为基础路径
            exe_path = Path(sys.executable).resolve()
            base_path = exe_path.parent
            
            # 检查 config.json 是否在可执行文件所在目录
            config_in_base = base_path / "config.json"
            if config_in_base.exists():
                return base_path
            else:
                # 如果 config.json 不在可执行文件目录，尝试向上查找
                current = base_path
                for _ in range(3):  # 最多向上查找 3 层
                    if (current / "config.json").exists():
                        return current
                    current = current.parent
                # 如果还是找不到，使用可执行文件所在目录
                return base_path
        else:
            # Python 脚本运行
            current_dir = Path(__file__).parent.absolute()
            return current_dir
        
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
        
    def build_file_url(self, base_url, branch, file_path):
        """根据平台类型构建文件URL"""
        # git_platform 支持: "github", "gitlab", "remote"
        if self.git_platform == "remote":
            # 本地服务器格式: http://任意URL/software/软件名/文件路径
            # file_path 已经包含了 software/ 前缀，直接拼接
            if base_url.endswith('/'):
                base_url = base_url[:-1]
            return f"{base_url}/{file_path}"
        elif self.git_platform == "gitlab":
            # GitLab格式: https://gitlab.com/user/repo/-/raw/branch/path/to/file
            if base_url.endswith('/'):
                base_url = base_url[:-1]
            return f"{base_url}/-/raw/{branch}/{file_path}"
        else:
            # GitHub格式: https://raw.githubusercontent.com/user/repo/branch/path/to/file
            # 或者镜像格式: https://mirror.com/user/repo/refs/heads/branch/path/to/file
            if "/refs/heads/" in base_url:
                return f"{base_url}/{file_path}"
            else:
                # 标准GitHub raw格式
                return f"{base_url}/{branch}/{file_path}"
    
    def get_default_branch(self):
        """获取默认分支名"""
        if self.git_platform == "gitlab":
            return "master"  # GitLab默认分支通常是master或main
        else:
            return "master"  # GitHub默认分支
            
    def download_file(self, url, local_path):
        """下载文件，带重试机制和详细错误提示"""
        retry_times = self.config.get("retry_times", 3)
        retry_delay = self.config.get("retry_delay", 5)
        timeout = self.config.get("download_timeout", 30)
        
        for attempt in range(retry_times):
            try:
                self.logger.debug(f"尝试下载文件 (第 {attempt + 1}/{retry_times} 次): {url}")
                
                response = requests.get(url, stream=True, timeout=timeout)
                response.raise_for_status()
                
                # 获取文件大小用于进度显示
                total_size = int(response.headers.get('content-length', 0))
                
                # 写入文件
                with open(local_path, 'wb') as f:
                    downloaded_size = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # 每下载1MB记录一次进度（仅对大文件）
                            if total_size > 1024 * 1024 and downloaded_size % (1024 * 1024) < 8192:
                                progress = (downloaded_size / total_size * 100) if total_size > 0 else 0
                                self.logger.debug(f"下载进度: {progress:.1f}% ({downloaded_size}/{total_size} bytes)")
                
                self.logger.info(f"文件下载成功: {local_path.name} ({downloaded_size} bytes)")
                return True
                
            except requests.exceptions.Timeout:
                error_msg = f"下载超时 (超过 {timeout} 秒)"
                if attempt < retry_times - 1:
                    self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"{error_msg}, 已达到最大重试次数")
                    self._log_download_error(url, "超时", f"连接超过 {timeout} 秒未响应")
                    
            except requests.exceptions.ConnectionError as e:
                error_msg = f"网络连接错误: {str(e)}"
                if attempt < retry_times - 1:
                    self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"{error_msg}, 已达到最大重试次数")
                    self._log_download_error(url, "连接错误", str(e))
                    
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else "未知"
                error_msg = f"HTTP错误 ({status_code}): {str(e)}"
                
                # 4xx错误不需要重试
                if 400 <= status_code < 500:
                    self.logger.error(f"{error_msg} (客户端错误，不重试)")
                    self._log_download_error(url, f"HTTP {status_code}", str(e))
                    return False
                else:
                    # 5xx错误重试
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"{error_msg}, 已达到最大重试次数")
                        self._log_download_error(url, f"HTTP {status_code}", str(e))
                        
            except requests.exceptions.RequestException as e:
                error_msg = f"请求异常: {str(e)}"
                if attempt < retry_times - 1:
                    self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"{error_msg}, 已达到最大重试次数")
                    self._log_download_error(url, "请求异常", str(e))
                    
            except IOError as e:
                error_msg = f"文件写入错误: {str(e)}"
                self.logger.error(f"{error_msg}")
                self._log_download_error(url, "文件写入", f"无法写入到 {local_path}: {str(e)}")
                return False
                
            except Exception as e:
                error_msg = f"未知错误: {str(e)}"
                if attempt < retry_times - 1:
                    self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"{error_msg}, 已达到最大重试次数")
                    self._log_download_error(url, "未知错误", str(e))
        
        return False
    
    def _log_download_error(self, url, error_type, error_detail):
        """记录下载错误详情"""
        self.logger.error("=" * 60)
        self.logger.error(f"下载失败详情:")
        self.logger.error(f"  URL: {url}")
        self.logger.error(f"  错误类型: {error_type}")
        self.logger.error(f"  错误详情: {error_detail}")
        self.logger.error("=" * 60)
        self.logger.error("可能的解决方案:")
        self.logger.error("  1. 检查网络连接是否正常")
        self.logger.error("  2. 确认URL是否正确")
        self.logger.error("  3. 检查是否有足够的磁盘空间")
        self.logger.error("  4. 检查目标目录是否有写入权限")
        self.logger.error("  5. 尝试使用其他镜像源")
        self.logger.error("=" * 60)
            
    def get_remote_list(self):
        """获取远程列表文件，带重试机制和详细错误提示"""
        retry_times = self.config.get("retry_times", 3)
        retry_delay = self.config.get("retry_delay", 5)
        timeout = self.config.get("download_timeout", 30)
        
        # 如果 git_platform 是 remote，使用 remote_server
        if self.git_platform == "remote":
            remote_server = self.config.get("remote_server", "").strip()
            if not remote_server:
                self.logger.error("=" * 60)
                self.logger.error("配置错误: git_platform 设置为 remote，但未配置 remote_server")
                self.logger.error("=" * 60)
                self.logger.error("解决方案:")
                self.logger.error("  1. 在 config.json 中设置 remote_server")
                self.logger.error("  2. 或将 git_platform 改为 github 或 gitlab")
                self.logger.error("=" * 60)
                return None
            
            branch = self.get_default_branch()
            list_url = self.build_file_url(remote_server, branch, self.list_file)
            
            for attempt in range(retry_times):
                try:
                    self.logger.info(f"尝试从远程服务器获取列表 (第 {attempt + 1}/{retry_times} 次): {list_url}")
                    response = requests.get(list_url, timeout=timeout)
                    response.raise_for_status()
                    
                    result = json.loads(response.text)
                    self.logger.info(f"成功从远程服务器获取列表，包含 {len(result.get('software', {}))} 个软件")
                    return result
                    
                except requests.exceptions.Timeout:
                    error_msg = f"远程服务器响应超时 (超过 {timeout} 秒)"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"{error_msg}, 已达到最大重试次数")
                        self._log_remote_list_error(list_url, "超时", f"连接超过 {timeout} 秒未响应")
                        
                except requests.exceptions.ConnectionError as e:
                    error_msg = f"无法连接到远程服务器: {str(e)}"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"{error_msg}, 已达到最大重试次数")
                        self._log_remote_list_error(list_url, "连接错误", str(e))
                        
                except requests.exceptions.HTTPError as e:
                    status_code = e.response.status_code if e.response is not None else "未知"
                    error_msg = f"HTTP错误 ({status_code}): {str(e)}"
                    
                    # 4xx错误不需要重试
                    if 400 <= status_code < 500:
                        self.logger.error(f"{error_msg} (客户端错误，不重试)")
                        self._log_remote_list_error(list_url, f"HTTP {status_code}", str(e))
                        return None
                    else:
                        if attempt < retry_times - 1:
                            self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                        else:
                            self.logger.error(f"{error_msg}, 已达到最大重试次数")
                            self._log_remote_list_error(list_url, f"HTTP {status_code}", str(e))
                            
                except json.JSONDecodeError as e:
                    error_msg = f"JSON解析失败: {str(e)}"
                    self.logger.error(f"{error_msg}")
                    self._log_remote_list_error(list_url, "JSON解析错误", str(e))
                    return None
                    
                except Exception as e:
                    error_msg = f"未知错误: {str(e)}"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"{error_msg}, 已达到最大重试次数")
                        self._log_remote_list_error(list_url, "未知错误", str(e))
            
            return None
        
        # 获取镜像源列表
        mirrors = self.config.get("git_mirrors", [])
        
        # 如果没有配置镜像源，使用默认仓库
        if not mirrors:
            if self.git_platform == "gitlab" and self.gitlab_repo:
                mirrors = [self.gitlab_repo]
            elif self.github_repo:
                mirrors = [self.github_repo]
            else:
                self.logger.error("=" * 60)
                self.logger.error("配置错误: 未配置任何镜像源或仓库地址")
                self.logger.error("=" * 60)
                self.logger.error("解决方案:")
                self.logger.error("  1. 在 config.json 中配置 git_mirrors")
                self.logger.error("  2. 或配置 github_repo 或 gitlab_repo")
                self.logger.error("=" * 60)
                return None
        
        branch = self.get_default_branch()
        
        # 尝试每个镜像源
        for mirror_index, mirror in enumerate(mirrors, 1):
            # 构建列表文件URL
            list_url = self.build_file_url(mirror, branch, self.list_file)
            
            self.logger.info(f"尝试镜像源 {mirror_index}/{len(mirrors)}: {mirror}")
            
            for attempt in range(retry_times):
                try:
                    self.logger.debug(f"尝试获取列表 (第 {attempt + 1}/{retry_times} 次): {list_url}")
                    response = requests.get(list_url, timeout=timeout)
                    response.raise_for_status()
                    
                    result = json.loads(response.text)
                    self.logger.info(f"成功从镜像源 {mirror_index}/{len(mirrors)} 获取列表，包含 {len(result.get('software', {}))} 个软件")
                    return result
                    
                except requests.exceptions.Timeout:
                    error_msg = f"镜像源响应超时 (超过 {timeout} 秒)"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.warning(f"{error_msg}, 尝试下一个镜像源...")
                        
                except requests.exceptions.ConnectionError as e:
                    error_msg = f"无法连接到镜像源: {str(e)}"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.warning(f"{error_msg}, 尝试下一个镜像源...")
                        
                except requests.exceptions.HTTPError as e:
                    status_code = e.response.status_code if e.response is not None else "未知"
                    error_msg = f"HTTP错误 ({status_code}): {str(e)}"
                    
                    # 4xx错误不需要重试，直接尝试下一个镜像源
                    if 400 <= status_code < 500:
                        self.logger.warning(f"{error_msg} (客户端错误)，尝试下一个镜像源...")
                        break
                    else:
                        if attempt < retry_times - 1:
                            self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                        else:
                            self.logger.warning(f"{error_msg}, 尝试下一个镜像源...")
                            
                except json.JSONDecodeError as e:
                    error_msg = f"JSON解析失败: {str(e)}"
                    self.logger.warning(f"{error_msg}, 尝试下一个镜像源...")
                    break
                    
                except Exception as e:
                    error_msg = f"未知错误: {str(e)}"
                    if attempt < retry_times - 1:
                        self.logger.warning(f"{error_msg}, {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                    else:
                        self.logger.warning(f"{error_msg}, 尝试下一个镜像源...")
        
        # 所有镜像源都失败了
        self.logger.error("=" * 60)
        self.logger.error("所有镜像源都失败了")
        self.logger.error("=" * 60)
        self.logger.error(f"尝试的镜像源数量: {len(mirrors)}")
        self.logger.error("解决方案:")
        self.logger.error("  1. 检查网络连接是否正常")
        self.logger.error("  2. 检查 config.json 中的镜像源配置是否正确")
        self.logger.error("  3. 尝试添加其他可用的镜像源")
        self.logger.error("  4. 检查防火墙或代理设置")
        self.logger.error("  5. 稍后重试，可能是临时网络问题")
        self.logger.error("=" * 60)
        return None
    
    def _log_remote_list_error(self, url, error_type, error_detail):
        """记录获取远程列表错误详情"""
        self.logger.error("=" * 60)
        self.logger.error(f"获取远程列表失败详情:")
        self.logger.error(f"  URL: {url}")
        self.logger.error(f"  错误类型: {error_type}")
        self.logger.error(f"  错误详情: {error_detail}")
        self.logger.error("=" * 60)
        self.logger.error("可能的解决方案:")
        self.logger.error("  1. 检查网络连接是否正常")
        self.logger.error("  2. 确认URL是否正确")
        self.logger.error("  3. 检查远程服务器是否正常运行")
        self.logger.error("  4. 检查配置文件中的仓库地址")
        self.logger.error("  5. 尝试使用其他镜像源或切换平台")
        self.logger.error("=" * 60)
            
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
        """下载软件文件，支持多镜像源切换和详细错误提示"""
        file_path = file_info['path']
        
        # 如果 git_platform 是 remote，使用 remote_server
        if self.git_platform == "remote":
            remote_server = self.config.get("remote_server", "").strip()
            if not remote_server:
                self.logger.error("git_platform 设置为 remote，但未配置 remote_server")
                return False
            
            branch = self.get_default_branch()
            file_path_normalized = file_path.replace('\\', '/')
            full_path = f"software/{software_name}/{file_path_normalized}"
            file_url = self.build_file_url(remote_server, branch, full_path)
            local_file_path = self.local_path / software_name / file_path
            
            # 创建目录
            try:
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.logger.error(f"无法创建目录 {local_file_path.parent}: {str(e)}")
                return False
            
            # 下载文件
            if self.download_file(file_url, local_file_path):
                self.logger.info(f"文件下载成功: {file_path}")
                return True
            else:
                self.logger.error(f"从远程服务器 {remote_server} 下载失败: {file_path}")
                return False
        
        # 获取镜像源列表
        mirrors = self.config.get("git_mirrors", [])
        
        # 如果没有配置镜像源，使用默认仓库
        if not mirrors:
            if self.git_platform == "gitlab" and self.gitlab_repo:
                mirrors = [self.gitlab_repo]
            elif self.github_repo:
                mirrors = [self.github_repo]
            else:
                self.logger.error("未配置任何镜像源或仓库地址")
                return False
        
        branch = self.get_default_branch()
        
        # 尝试每个镜像源
        for mirror_index, mirror in enumerate(mirrors, 1):
            # 处理Windows路径分隔符
            file_path_normalized = file_path.replace('\\', '/')
            full_path = f"software/{software_name}/{file_path_normalized}"
            
            # 构建文件URL
            file_url = self.build_file_url(mirror, branch, full_path)
                
            local_file_path = self.local_path / software_name / file_path
            
            # 创建目录
            try:
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.logger.error(f"无法创建目录 {local_file_path.parent}: {str(e)}")
                return False
            
            # 下载文件
            self.logger.debug(f"尝试从镜像源 {mirror_index}/{len(mirrors)} 下载: {file_url}")
            
            if self.download_file(file_url, local_file_path):
                self.logger.info(f"文件下载成功: {file_path} (使用镜像源 {mirror_index}/{len(mirrors)})")
                return True
            else:
                self.logger.warning(f"从镜像源 {mirror_index}/{len(mirrors)} 下载失败: {file_path}")
                # 继续尝试下一个镜像源
                continue
        
        # 所有镜像源都失败了
        self.logger.error("=" * 60)
        self.logger.error(f"所有镜像源都失败了: {file_path}")
        self.logger.error("=" * 60)
        self.logger.error(f"软件名称: {software_name}")
        self.logger.error(f"文件路径: {file_path}")
        self.logger.error(f"尝试的镜像源数量: {len(mirrors)}")
        self.logger.error("=" * 60)
        self.logger.error("可能的解决方案:")
        self.logger.error("  1. 检查网络连接是否正常")
        self.logger.error("  2. 检查是否有足够的磁盘空间")
        self.logger.error("  3. 检查目标目录是否有写入权限")
        self.logger.error("  4. 尝试使用其他镜像源")
        self.logger.error("  5. 稍后重试，可能是临时网络问题")
        self.logger.error("  6. 检查文件是否在远程仓库中存在")
        self.logger.error("=" * 60)
        return False
        
    def sync_software(self, software_name, remote_files, local_files):
        """同步单个软件"""
        self.logger.info(f"开始同步软件: {software_name}")
        
        software_path = self.local_path / software_name
        software_path.mkdir(exist_ok=True)
        
        if self.config.get("auto_kill", False):
            self.kill_software_processes(software_name)

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

        if (updated_files + new_files) > 0 and self.should_auto_start(software_name):
            self.start_software(software_name)

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
        
        # 按照 config.json 中 software_dirs 的顺序进行同步
        # 如果软件不在 config.json 中，则按远程列表的顺序
        software_order = list(self.config.get("software_dirs", {}).keys())
        remote_software = remote_list['software']
        
        # 先处理 config.json 中配置的软件（按配置顺序）
        for software_name in software_order:
            if software_name in remote_software:
                software_info = remote_software[software_name]
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
        
        # 再处理远程列表中存在但 config.json 中未配置的软件
        for software_name, software_info in remote_software.items():
            if software_name not in software_order:
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

    def kill_software_processes(self, software_name):
        """关闭软件相关进程"""
        proc_map = self.config.get("process_map", {})
        start_map = self.config.get("start_map", {})
        names = proc_map.get(software_name, [])
        if not names:
            start_path = start_map.get(software_name)
            if start_path:
                exe_name = os.path.basename(start_path)
                if exe_name:
                    names = [exe_name]
        
        if not names:
            self.logger.debug(f"软件 {software_name} 未配置进程映射，跳过关闭进程")
            return
        
        self.logger.info(f"开始关闭软件 {software_name} 的相关进程: {names}")
        for name in names:
            try:
                result = subprocess.run(
                    ["taskkill", "/F", "/IM", name], 
                    check=False, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    self.logger.info(f"成功关闭进程: {name}")
                elif result.returncode == 128:
                    # 进程未找到，这是正常情况
                    self.logger.debug(f"进程未运行: {name}")
                else:
                    self.logger.warning(f"关闭进程 {name} 返回码: {result.returncode}, 输出: {result.stderr}")
            except Exception as e:
                self.logger.warning(f"结束进程失败: {name}, 错误: {e}")

    def start_software(self, software_name):
        """启动软件，支持启动多个程序，支持Windows服务"""
        start_map = self.config.get("start_map", {})
        service_map = self.config.get("service_map", {})
        rel_paths = start_map.get(software_name)
        if not rel_paths:
            self.logger.debug(f"未找到软件 {software_name} 的启动路径配置")
            return
        
        # 支持单个字符串或数组
        if isinstance(rel_paths, str):
            rel_paths = [rel_paths]
        elif not isinstance(rel_paths, list):
            self.logger.warning(f"软件 {software_name} 的启动路径配置格式错误")
            return
        
        base_path = self.local_path / software_name
        
        for rel_path in rel_paths:
            exe_name = os.path.basename(rel_path)
            
            # 检查是否是Windows服务
            if exe_name in service_map:
                service_name = service_map[exe_name]
                service_started = False
                try:
                    # 先检查服务是否存在
                    check_result = subprocess.run(
                        ["sc", "query", service_name],
                        check=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    if check_result.returncode != 0:
                        # 服务不存在，降级为普通程序启动
                        self.logger.info(f"服务 {service_name} 未安装，将作为普通程序启动: {exe_name}")
                    else:
                        # 服务存在，尝试启动服务
                        result = subprocess.run(
                            ["net", "start", service_name],
                            check=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        if result.returncode == 0:
                            self.logger.info(f"已启动服务: {software_name} -> {service_name}")
                            service_started = True
                        elif "already been started" in result.stdout or "已经启动" in result.stdout:
                            self.logger.info(f"服务已在运行: {software_name} -> {service_name}")
                            service_started = True
                        else:
                            # 服务启动失败，降级为普通程序启动
                            self.logger.warning(f"启动服务失败: {software_name} -> {service_name}, 将尝试作为普通程序启动")
                except Exception as e:
                    self.logger.warning(f"启动服务异常: {software_name} -> {service_name}, 将尝试作为普通程序启动, 错误: {e}")
                
                # 如果服务启动成功，跳过普通程序启动
                if service_started:
                    continue
                # 如果服务启动失败，继续执行下面的普通程序启动逻辑
            
            # 普通程序启动
            # 判断是绝对路径还是相对路径
            if os.path.isabs(rel_path):
                # 绝对路径，直接使用
                exe_path = Path(rel_path)
            else:
                # 相对路径，相对于软件目录
                exe_path = base_path / rel_path
            
            if not exe_path.exists():
                self.logger.warning(f"启动文件不存在: {exe_path}")
                continue
            
            try:
                subprocess.Popen(str(exe_path), cwd=str(exe_path.parent))
                self.logger.info(f"已启动软件: {software_name} -> {rel_path} (路径: {exe_path})")
            except Exception as e:
                self.logger.error(f"启动失败: {software_name} -> {rel_path}, 错误: {e}")

    def should_auto_start(self, software_name):
        if not self.config.get("auto_start", False):
            return False
        sel = self.config.get("start_after_update")
        if isinstance(sel, list) and len(sel) > 0:
            return software_name in sel
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