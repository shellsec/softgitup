# SoftGitUp - 软件同步工具

一个用于管理和同步软件的跨平台工具。

## 功能特性

### 1. 本地管理工具 (soft_manager.py)
- 管理本地软件目录
- 生成文件索引和版本列表 (list.txt)
- 支持Git操作，自动推送到GitHub

### 2. 后台同步工具 (soft_sync.py)
- 后台运行，系统托盘图标
- 定时同步更新（默认每天7点）
- 自动下载并覆盖本地文件
- 跨平台支持

## 支持的软件
- CCleaner
- EditPlus
- everything
- HiBit Startup Manager
- notepad++
- notepad-
- SublimeText
- WinMemoryCleaner
- WinRAR



## 使用方法

### 安装依赖
```bash
pip install -r requirements.txt
```

### 本地管理
```bash
python soft_manager.py
```

### 后台同步
```bash
python soft_sync.py
```

## 配置说明

- `config.json`: 主配置文件
- `list.txt`: 软件版本索引文件
- `logs/`: 日志目录 