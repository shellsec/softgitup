# SoftGitUp - 日常工具云升级同步系统

一个用于管理本地软件目录并自动同步更新的工具系统，支持GitHub云存储和Git加速下载。

## 功能特性

### 🚀 核心功能
- **本地软件管理**: 扫描本地软件目录，生成文件索引和版本列表
- **云端同步**: 自动推送到GitHub，支持Git加速下载
- **智能更新**: 基于文件修改时间比较，只下载变更的文件
- **系统托盘**: 后台运行，支持系统托盘图标和静默更新
- **跨平台**: 支持Windows、Linux、macOS
- **工作流程**: 提供便捷的工作流程工具，支持单个软件更新和同步
- **开箱即用**: 所见即所得注册破解版本，日常保持更新版本，已杀毒

### 📦 支持的软件
- **文本编辑器**: Notepad++、notepad-、SublimeText、EditPlus、EmEditor(大文件16T)
- **系统工具**: CCleaner、Everything、WinMemoryCleaner、CrystalDiskInfo、NetTime
- **压缩工具**: WinRAR
- **启动管理**: HiBit Startup Manager
- **更多软件**: 可轻松扩展支持，有其他需要可以发帖
- **更多软件**: （默认不下载，看喜好）想要system_good的话在配置文件自行添加，system_good目录更新，驱动人生海外版、StartAllBack任务栏、关闭补丁更新、kms激活、关闭自带杀毒

## 项目结构

```
softgitup/
├── config.json              # 配置文件
├── soft_manager.py          # 本地管理工具
├── soft_sync.py            # 同步工具（GUI版本）
├── simple_sync.py          # 简单同步工具（命令行）
├── workflow.py             # 工作流程工具
├── build_exe.py            # 打包脚本
├── generate_and_push.bat   # 一键生成和推送批处理
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
  "github_repo": "https://github.com/shellsec/softgitup",
  "manager_base_path": "./software",
  "sync_base_path": "D:/Program Files",
  "sync_time": "07:00",
  "git_mirrors": [
    "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
  ]
}
```

### 4. 使用工作流程工具（推荐）
```bash
# 启动工作流程工具
python workflow.py
```

### 5. 使用管理工具
```bash
# 扫描本地软件并推送到GitHub
python soft_manager.py

# 或使用批处理一键操作
generate_and_push.bat
```

### 6. 使用同步工具
```bash
# 同步单个软件
python simple_sync.py everything

# 同步所有软件
python simple_sync.py

# 启动GUI同步工具（系统托盘）
python soft_sync.py
```

## 打包和编译

### 编译为可执行文件
使用 `build_exe.py` 脚本将Python程序打包成可执行文件：

```bash
python build_exe.py
```

打包脚本提供多种选项：
1. **构建所有程序** (推荐) - 包含GUI和控制台版本
2. **只构建控制台版本** - 无GUI依赖，避免PyQt5 DLL问题
3. **只构建GUI版本** - 包含完整的GUI功能
4. **清理构建文件** - 清理临时文件

### 解决PyQt5 DLL问题
如果遇到 `ImportError: DLL load failed while importing QtWidgets` 错误：

**方案1: 使用控制台版本**
```bash
# 选择选项2，构建控制台版本
python build_exe.py
# 使用生成的 SoftGitUp_Sync_Simple.exe
```

**方案2: 使用Python脚本**
```bash
# 直接运行Python脚本，避免打包问题
python simple_sync.py
python workflow.py
```

**方案3: 安装Visual C++ Redistributable**
- 下载并安装Microsoft Visual C++ Redistributable
- 重新编译GUI版本

### 生成的可执行文件
- `SoftGitUp_Workflow.exe` - 工作流程工具（控制台）
- `SoftGitUp_Manager.exe` - 管理工具（GUI）
- `SoftGitUp_Sync.exe` - 同步工具（GUI，系统托盘）
- `SoftGitUp_Sync_Simple.exe` - 简化同步工具（控制台）

## 工作流程

### 更新软件流程
1. **更新软件文件**: 将新版本的软件放入 `software/` 目录
2. **生成列表**: 运行 `python soft_manager.py` 或使用批处理
3. **推送到GitHub**: 自动提交并推送更新
4. **同步到其他设备**: 在其他设备上运行同步工具

### 使用工作流程工具
```bash
python workflow.py
```
选择相应的操作：
- 更新单个软件并生成列表
- 同步单个软件
- 同步所有软件
- 生成完整软件列表

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

### Git加速源配置
使用 `gh-proxy.com` 作为Git加速下载源：
```json
"git_mirrors": [
  "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
]
```

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

### 单个软件更新
```bash
# 只更新特定软件
python -c "from soft_manager import SoftManager; SoftManager().generate_list_file('everything')"
```

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

**Q: 编译后运行报错 "DLL load failed while importing QtWidgets"？**
A: 这是PyQt5 DLL依赖问题，建议：
1. 使用控制台版本：`python build_exe.py` 选择选项2
2. 直接运行Python脚本：`python simple_sync.py`
3. 安装Visual C++ Redistributable后重新编译

**Q: 同步失败怎么办？**
A: 检查网络连接和GitHub仓库权限，确保使用正确的Git加速源。

**Q: 文件修改时间不匹配？**
A: 这通常是因为文件内容发生了变化，系统会自动下载最新版本。

**Q: 如何添加新的软件？**
A: 将软件放入software目录，在config.json中添加软件名称，然后运行管理工具。

### 日志查看
```bash
# 查看管理工具日志
tail -f logs/manager.log

# 查看同步工具日志
tail -f logs/sync.log

# 查看简单同步日志
tail -f logs/simple_sync.log
```

## 技术支持

如果遇到问题，请：
1. 查看日志文件获取详细错误信息
2. 检查网络连接和GitHub仓库权限
3. 尝试使用控制台版本避免GUI依赖问题
4. 提交Issue到GitHub仓库

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