#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGitUp - 本地软件管理工具
用于管理本地软件目录，生成文件索引和版本列表
"""

import os
import sys
import json
import hashlib
import datetime
import argparse
import fnmatch
import git
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# 默认配置，避免空 config 导致 KeyError
DEFAULT_CONFIG = {
    "manager_base_path": "./software",
    "list_file": "list.txt",
    "software_dirs": {},
    "log_level": "INFO",
    "ignore_patterns": ["*.pyc", "__pycache__", "*.log", "*.tmp", ".DS_Store", "Thumbs.db"],
}

class SoftManager:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self._validate_config()
        self.setup_logging()
        self.local_path = Path(self.config.get("manager_base_path", "./software"))
        self.list_file = self.local_path / self.config["list_file"]
        
    def load_config(self, config_file):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 合并默认值，确保必填项存在
                merged = {**DEFAULT_CONFIG, **data}
                if "software_dirs" not in data or not data["software_dirs"]:
                    merged.setdefault("software_dirs", DEFAULT_CONFIG["software_dirs"])
                return merged
        except FileNotFoundError:
            print(f"配置文件 {config_file} 不存在", file=sys.stderr)
            return dict(DEFAULT_CONFIG)
        except json.JSONDecodeError as e:
            print(f"配置文件 JSON 解析失败: {e}", file=sys.stderr)
            return dict(DEFAULT_CONFIG)
            
    def _validate_config(self):
        """校验必填配置项"""
        if not self.config.get("software_dirs"):
            self.config["software_dirs"] = DEFAULT_CONFIG["software_dirs"]
        if not self.config.get("list_file"):
            self.config["list_file"] = DEFAULT_CONFIG["list_file"]
        # 若仍无软件目录，仅警告，不退出（允许后续只做 push-only 等）
            
    def setup_logging(self):
        """设置日志（带轮转，避免单文件过大）"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        level = getattr(logging, self.config.get("log_level", "INFO"), logging.INFO)
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        
        file_handler = RotatingFileHandler(
            log_dir / "manager.log",
            maxBytes=2 * 1024 * 1024,  # 2MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(fmt))
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt))
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        
    def _should_ignore(self, relative_path_str):
        """根据 ignore_patterns 判断是否忽略该路径"""
        patterns = self.config.get("ignore_patterns") or []
        # 统一用 / 比较
        path_for_match = relative_path_str.replace("\\", "/")
        for pat in patterns:
            if fnmatch.fnmatch(path_for_match, pat):
                return True
            if fnmatch.fnmatch(Path(path_for_match).name, pat):
                return True
        return False

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
            
    def _load_previous_list(self):
        """加载上一次生成的列表（用于增量哈希与版本比较）"""
        if not self.list_file.exists():
            return None
        try:
            with open(self.list_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.debug(f"读取旧列表失败: {e}")
            return None
            
    def scan_software_directory(self, software_name, old_files_by_path=None):
        """扫描软件目录，生成文件列表。old_files_by_path 为 {path: {hash, modified}}，用于按 mtime 跳过未变更文件的哈希计算。"""
        software_path = self.local_path / software_name
        if not software_path.exists():
            self.logger.warning(f"软件目录不存在 {software_path}")
            return []
        old_files_by_path = old_files_by_path or {}
            
        files_info = []
        for file_path in software_path.rglob("*"):
            if not file_path.is_file():
                continue
            relative_path = file_path.relative_to(software_path)
            rel_str = str(relative_path).replace("\\", "/")
            if self._should_ignore(rel_str):
                continue
            st = file_path.stat()
            mtime_iso = datetime.datetime.fromtimestamp(st.st_mtime).isoformat()
            old = old_files_by_path.get(rel_str)
            if old and old.get("modified") == mtime_iso and old.get("hash"):
                file_hash = old["hash"]
            else:
                file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                files_info.append({
                    "path": str(relative_path),
                    "size": st.st_size,
                    "hash": file_hash,
                    "modified": mtime_iso
                })
        return files_info
        
    def _software_content_changed(self, old_files, new_files):
        """比较两个文件列表是否一致（按 path+hash+modified 判断）"""
        if not old_files and not new_files:
            return False
        if len(old_files) != len(new_files):
            return True
        new_by_path = {f["path"].replace("\\", "/"): f for f in new_files}
        for f in old_files:
            key = f["path"].replace("\\", "/")
            if key not in new_by_path:
                return True
            if f.get("hash") != new_by_path[key].get("hash") or f.get("modified") != new_by_path[key].get("modified"):
                return True
        return False

    def generate_list_file(self, software_name=None, dry_run=False):
        """生成软件列表文件。dry_run=True 时不写入文件，仅返回内容。"""
        previous_list = self._load_previous_list()
        prev_software = (previous_list or {}).get("software") or {}
        software_list = {}
        total_files = 0
        
        def make_entry(name, files_info, prev_entry):
            changed = self._software_content_changed(
                (prev_entry or {}).get("files") or [],
                files_info
            )
            now_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            now_iso = datetime.datetime.now().isoformat()
            if prev_entry and not changed:
                version = prev_entry.get("version", now_ts)
                last_updated = prev_entry.get("last_updated", now_iso)
            else:
                version = now_ts
                last_updated = now_iso
            return {
                "version": version,
                "files": files_info,
                "total_files": len(files_info),
                "total_size": sum(f["size"] for f in files_info),
                "last_updated": last_updated
            }
        
        if software_name:
            # 单软件模式：先继承旧列表，再只更新该软件
            if previous_list and previous_list.get("software"):
                for k, v in previous_list["software"].items():
                    software_list[k] = v
            if software_name in self.config["software_dirs"]:
                self.logger.info(f"扫描软件: {software_name}")
                old_files = {}
                if prev_software.get(software_name) and prev_software[software_name].get("files"):
                    old_files = {f["path"].replace("\\", "/"): f for f in prev_software[software_name]["files"]}
                files_info = self.scan_software_directory(software_name, old_files)
                if files_info:
                    software_list[software_name] = make_entry(
                        software_name, files_info, prev_software.get(software_name)
                    )
                else:
                    software_list.pop(software_name, None)
            else:
                self.logger.warning(f"未在 software_dirs 中配置: {software_name}，仅保留旧列表")
            total_files = sum(s.get("total_files", 0) for s in software_list.values())
            total_size_bytes = sum(s.get("total_size", 0) for s in software_list.values())
            list_content = {
                "generated_at": datetime.datetime.now().isoformat(),
                "total_software": len(software_list),
                "total_files": total_files,
                "total_size": total_size_bytes,
                "software": software_list
            }
            if not dry_run:
                self.list_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.list_file, 'w', encoding='utf-8') as f:
                    json.dump(list_content, f, ensure_ascii=False, indent=2)
                self.logger.info(f"生成列表文件完成: {self.list_file}")
            else:
                self.logger.info("[dry-run] 未写入文件")
            self.logger.info(f"包含 {len(software_list)} 个软件，共 {total_files} 个文件，总大小: {self._format_size(total_size_bytes)}")
            return list_content
        else:
            for name in self.config["software_dirs"]:
                self.logger.info(f"扫描软件: {name}")
                old_files = {}
                if prev_software.get(name) and prev_software[name].get("files"):
                    old_files = {f["path"].replace("\\", "/"): f for f in prev_software[name]["files"]}
                files_info = self.scan_software_directory(name, old_files)
                if files_info:
                    software_list[name] = make_entry(name, files_info, prev_software.get(name))
                    total_files += len(files_info)
                
        total_size_bytes = sum(s["total_size"] for s in software_list.values())
        list_content = {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_software": len(software_list),
            "total_files": total_files,
            "total_size": total_size_bytes,
            "software": software_list
        }
        
        if not dry_run:
            self.list_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.list_file, 'w', encoding='utf-8') as f:
                json.dump(list_content, f, ensure_ascii=False, indent=2)
            self.logger.info(f"生成列表文件完成: {self.list_file}")
        else:
            self.logger.info("[dry-run] 未写入文件")
        self.logger.info(f"包含 {len(software_list)} 个软件，共 {total_files} 个文件，总大小: {self._format_size(total_size_bytes)}")
        return list_content
    
    def _format_size(self, size_bytes):
        """将字节数格式化为可读大小"""
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
        
    def git_commit_and_push(self):
        """Git 提交并推送到远程仓库；仅当列表文件有变更时才提交。"""
        try:
            repo = git.Repo(".")
            # 使用相对路径，便于与 untracked_files / diff 一致
            list_rel = str(self.list_file).replace("\\", "/")
            
            # 若列表文件处于合并冲突状态（索引中存在多 stage），先用工作区版本解析
            try:
                unmerged = repo.index.unmerged
            except Exception:
                unmerged = {}
            if unmerged and list_rel in unmerged:
                self.logger.warning("检测到 %s 合并冲突，正在用当前列表文件解析", list_rel)
                repo.git.add(str(self.list_file))
                repo = git.Repo(".")  # 重新打开以刷新索引（部分 GitPython 版本无 index.read）
            
            # 未跟踪或工作区有修改才需要 add
            is_untracked = list_rel in repo.untracked_files
            try:
                is_modified = bool(repo.is_dirty(path=list_rel))
            except Exception:
                is_modified = True
            if not is_untracked and not is_modified:
                self.logger.info("列表文件无变更，跳过 Git 提交")
                return True
            
            repo.index.add([str(self.list_file)])
            # 暂存后检查相对 HEAD 是否有差异，无差异则跳过提交
            if len(repo.index.diff("HEAD")) == 0:
                self.logger.info("无新变更需要提交，跳过 push")
                return True
            
            commit_message = f"更新软件列表 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            self.logger.info("成功推送到远程")
            return True
            
        except git.exc.InvalidGitRepositoryError:
            self.logger.error("当前目录不是 Git 仓库")
            return False
        except Exception as e:
            self.logger.error(f"Git 操作失败: {e}")
            return False
            
    def run(self, generate_only=False, push_only=False, software_name=None, dry_run=False):
        """运行管理工具。
        generate_only: 仅生成列表，不 push
        push_only: 仅提交并推送当前列表（不重新扫描）
        software_name: 仅扫描指定软件
        dry_run: 仅扫描并输出，不写入文件、不 push
        """
        self.logger.info("开始运行软件管理工具")
        
        if push_only:
            if self.git_commit_and_push():
                self.logger.info("推送完成")
            else:
                self.logger.warning("Git 推送失败")
            return
        
        list_content = self.generate_list_file(software_name=software_name, dry_run=dry_run)
        
        if dry_run:
            self.logger.info("dry-run 结束")
            return
            
        if not generate_only and self.git_commit_and_push():
            self.logger.info("软件管理完成")
        elif generate_only:
            self.logger.info("仅生成列表完成")
        else:
            self.logger.warning("Git 推送失败，但列表文件已生成")


def main():
    parser = argparse.ArgumentParser(description="SoftGitUp 本地软件管理：生成列表并推送")
    parser.add_argument("--config", "-c", default="config.json", help="配置文件路径")
    parser.add_argument("--generate-only", action="store_true", help="仅生成列表文件，不提交推送")
    parser.add_argument("--push-only", action="store_true", help="仅提交并推送当前列表，不重新扫描")
    parser.add_argument("--software", "-s", metavar="NAME", help="仅扫描指定软件目录")
    parser.add_argument("--dry-run", action="store_true", help="仅扫描并输出，不写入文件、不推送")
    args = parser.parse_args()
    
    manager = SoftManager(config_file=args.config)
    if not manager.config.get("software_dirs") and not args.push_only:
        manager.logger.warning("配置中 software_dirs 为空，将不会扫描任何软件")
    manager.run(
        generate_only=args.generate_only,
        push_only=args.push_only,
        software_name=args.software,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
