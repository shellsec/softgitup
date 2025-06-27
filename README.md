# SoftGitUp - 日常工具云升级同步系统

一个用于管理本地软件目录并自动同步更新的工具系统，支持GitHub云存储和多镜像源加速下载。

## 功能特性

### 🚀 核心功能
- **本地软件管理**: 扫描本地软件目录，生成文件索引和版本列表
- **云端同步**: 自动推送到GitHub，支持多镜像源下载
- **智能更新**: 基于文件哈希比较，只下载变更的文件
- **系统托盘**: 后台运行，支持系统托盘图标和静默更新
- **跨平台**: 支持Windows、Linux、macOS

### 📦 支持的软件
- **文本编辑器**: Notepad++、SublimeText、EditPlus
- **系统工具**: CCleaner、Everything、WinMemoryCleaner
- **压缩工具**: WinRAR
- **启动管理**: HiBit Startup Manager
- **更多软件**: 可轻松扩展支持

## 项目结构

```
softgitup/
├── config.json              # 配置文件
├── soft_manager.py          # 本地管理工具
├── soft_sync.py            # 同步工具（GUI版本）
├── test_sync.py            # 同步测试工具
├── test_simple_sync.py     # 简单同步测试
├── build_exe.py            # 打包脚本
├── list.txt                # 软件列表文件
├── software/               # 本地软件目录
│   ├── CCleaner/
│   ├── EditPlus/
│   ├── everything/
│   ├── notepad++/
│   ├── SublimeText/
│   └── ...
├── logs/                   # 日志目录
└── README.md              # 项目说明
```

## 快速开始

### 1. 环境要求
- Python 3.7+
- Git
- 网络连接

### 2. 安装依赖
```bash
pip install requests PyQt5 gitpython
```

### 3. 配置设置
编辑 `config.json` 文件：
```json
{
  "github_repo": "https://github.com/your-username/your-repo",
  "manager_base_path": "./software",
  "sync_base_path": "D:/Program Files",
  "sync_time": "07:00",
  "git_mirrors": [
    "https://github.com/your-username/your-repo",
    "https://ghproxy.com/https://github.com/your-username/your-repo"
  ]
}
```

### 4. 使用管理工具
```bash
# 扫描本地软件并推送到GitHub
python soft_manager.py
```

### 5. 使用同步工具
```bash
# 启动GUI同步工具（系统托盘）
python soft_sync.py

# 或使用命令行测试
python test_sync.py
```

## 配置说明

### 配置文件 (config.json)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `github_repo` | GitHub仓库地址 | - |
| `manager_base_path` | 管理工具扫描目录 | `./software` |
| `sync_base_path` | 同步工具下载目录 | `D:/Program Files` |
| `sync_time` | 自动同步时间 | `07:00` |
| `git_mirrors` | Git镜像源列表 | - |
| `download_timeout` | 下载超时时间(秒) | `30` |
| `retry_times` | 重试次数 | `3` |
| `retry_delay` | 重试延迟(秒) | `5` |
| `log_level` | 日志级别 | `INFO` |
| `auto_start` | 开机自启动 | `true` |
| `check_interval` | 检查间隔(秒) | `3600` |

### 镜像源配置
支持多种Git镜像源以提高下载稳定性：
- GitHub官方: `https://github.com/username/repo`
- GitHub代理: `https://ghproxy.com/https://github.com/username/repo`
- FastGit: `https://hub.fastgit.xyz/username/repo`
- CNPMJS: `https://github.com.cnpmjs.org/username/repo`

## 使用场景

### 个人用户
- 在多台设备间同步常用软件
- 自动更新软件到最新版本
- 备份软件配置和设置

### 企业环境
- 统一管理员工常用软件
- 批量部署和更新软件
- 软件版本控制和回滚

### 开发者
- 管理开发环境工具
- 快速搭建开发环境
- 工具链版本管理

## 高级功能

### 自定义软件包
1. 将软件放入 `software/` 目录
2. 在 `config.json` 中添加软件名称
3. 运行管理工具生成索引

### 定时同步
- 支持自定义同步时间
- 后台静默更新
- 系统托盘通知

### 日志管理
- 详细的同步日志
- 错误追踪和调试
- 可配置日志级别

## 故障排除

### 常见问题

**Q: 同步失败怎么办？**
A: 检查网络连接和GitHub仓库权限，尝试使用不同的镜像源。

**Q: 文件哈希验证失败？**
A: 这通常是因为文件内容发生了变化，删除本地文件重新下载即可。

**Q: 如何添加新的软件？**
A: 将软件放入software目录，在config.json中添加软件名称，然后运行管理工具。

### 日志查看
```bash
# 查看管理工具日志
tail -f logs/manager.log

# 查看同步工具日志
tail -f logs/sync.log
```

## 开发计划

- [ ] 支持更多云存储平台（Gitee、GitLab等）
- [ ] 添加软件版本管理功能
- [ ] 支持增量更新和压缩传输
- [ ] 添加Web管理界面
- [ ] 支持插件系统

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址: [GitHub](https://github.com/shellsec/softgitup)
- 问题反馈: [Issues](https://github.com/shellsec/softgitup/issues)

---

**注意**: 请确保遵守相关软件的使用许可协议，本工具仅用于个人学习和合法用途。 