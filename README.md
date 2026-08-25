# SoftGitUp - 日常工具云升级同步系统

**中文** | [English](README_EN.md)

## 🚀 推荐使用 [ofox.ai](https://ofox.io/x/aiv123)

> **一句话**：一个账号直达 GPT-5.5 / Claude 4.8 Opus / Gemini 3.5 Flash 等 **100+** 顶尖模型，首充额外赠 **$3** 额度。

[👉 注册领取](https://ofox.io/x/aiv123) · 全球专线 · 企业级 SLA · 不留存对话

| ⚡️ 极速稳定 | 🧠 模型全 | 🛡️ 隐私安全 |
|:---:|:---:|:---:|
| 全球专线，企业级 SLA | 100+ 模型一号直达 | 不留存任何对话 |

## ☕ 请我喝可乐

开源不易，欢迎赞助支持：  
👉 [爱发电](https://ifdian.net/a/shellsec)

一个用于管理本地软件目录并自动同步更新的工具系统，支持GitHub和GitLab云存储，支持Git加速下载。
具体可查看 [`Lastb_soft_version.txt`](Lastb_soft_version.txt) 最新更新文档。

<!-- SOFTWARE_SIZE_START -->
> 📦 **software/ 体积统计**（`generate_and_push.bat` 自动刷新）：
> 共 **21** 款软件、**4,195** 个文件，合计 **1.63 GB**；统计时间 2026-08-25 13:28。
> 体积 Top5：system_good (709.6 MB)、PotPlayer (253.1 MB)、UltraEdit (202.3 MB)、WiseCare365 (74.3 MB)、notepad++ (73.7 MB)。
<!-- SOFTWARE_SIZE_END -->

**维护者月度快检**（可选，不更新 `software/` 也完全可用）：见 [`soft_page_check/`](soft_page_check/README.md) — 双击 `monthly_sop.bat` 检查标题变化；装机开源可 `monthly_a_download_soft_github.bat` 直下，其余手工更新后发布。

本工具集基于**信息安全与数据防泄漏原则**构建，尽可能减少云端上报、行为跟踪与算法数据收割

### 装机清单与隐私面（对照 `Lastb_soft_version.txt`）

以下是对清单选型的**自检式**归纳，便于和第三方讨论（如其他 AI 或同事）时核对；**不是**对「泄露比例」的精确测量，也不构成法律或合规承诺。

**与清单一致、通常认为缓解较好的方向**

- **截图 OCR**：文档强调微信 / QQ / 管家类「主动识字 / OCR」易走云端；推荐 **PixPin 本地 OCR** 等与之一致。
- **输入法**：放弃搜狗等、采用 **小狼毫 + 雾凇拼音（Rime）** 等本地开源方案，与清单一致。
- **系统侧拦截**：**Zen** 系统代理 + **AdGuard DNS / 18bit DNS**（`system_good` 内脚本）+ 浏览器 **uBlock Origin、Privacy Badger**，与清单一致，属于多层叠加。
- **系统臃肿与更新**：**Win11Debloat、StopUpdates10、StartAllBack、HiBit Startup** 等在清单中出现，有助于减少预装与自启带来的后台行为（具体效果因配置而异）。
- **剪贴板**：**Ditto** 等本地剪贴板历史与「少用系统云剪贴板」思路一致。
- **本地 AI**：**Ollama** 等本地模型可减少敏感内容经在线大模型外送（仍注意模型来源与本地磁盘安全）。
- **播放器 / 看图 / 压缩**：PotPlayer、XnView MP、7-Zip、WinRAR 等与「常用功能尽量本地化」一致。

**清单内仍存在的客观上报或信任边界（心里有数即可）**

- **Chrome 官方版**：同步、崩溃报告、预测服务、**增强型安全浏览**等会向谷歌侧传递更多信息；可按需关闭同步、使用数据上报，安全浏览用「标准」而非「增强」等（详见 Chrome 设置与官方说明）。
- **P2P 下载（迅雷 / BitComet / qBittorrent 等）**：协议本身会上传做种；修改版 /「增强版」还涉及**对打包者的信任**，与官方构建不同。
- **洛雪音乐**：客户端开源相对透明，但**自定义音源脚本**会访问各平台 API，**IP、检索词等**可能对第三方可见；敏感场景避免用其搜索敏感内容。
- **Microsoft Defender**：即使用 **DefenderUI** 调策略，云端样本与威胁情报类上报仍可能按微软策略发生。
- **注册版、烈火汉化、果核修改版等**：清单中为实用向收录，从**供应链安全**角度与「仅官方签名构建」不同，需自行权衡。

**Windows / 硬件层未在长文中逐项写全、可另行收紧的部分**

- **诊断数据与遥测、广告 ID、活动历史、定位、OneDrive / 账户同步** 等系统设置需单独在「设置 → 隐私与安全性」等处逐项关闭或限制。
- **显卡套件（如 NVIDIA 驱动安装程序附带 GeForce Experience）** 常有使用数据统计；可仅装**纯驱动**或关闭相关收集选项。
- **.NET、WebView2、VC++ 运行库** 等会按各自机制检查更新；清单中已提及这些组件，隐私敏感环境可配合防火墙 / 更新策略评估。

**小结**：若将清单理解为「**本地优先、减少大厂云 OCR/输入法、叠加系统与 DNS 拦截**」的一套实践，与多数默认装机相比**通常更利于减少日常侧信道与行为上报**；但**不存在**「百分比封顶」或「完全无上传」的绝对结论，敏感环境应叠加**组策略、网络出口审计、仅信任官方构建**等措施。

## 功能特性

### 🚀 核心功能
- **本地软件管理**: 扫描本地软件目录，生成文件索引和版本列表
- **云端同步**: 自动推送到GitHub或GitLab，支持Git加速下载
- **多平台支持**: 支持GitHub和GitLab，可灵活切换
- **智能更新**: 基于文件修改时间比较，只下载变更的文件
- **自动进程管理**: 更新前自动关闭相关进程，更新后自动启动指定程序
- **Windows服务支持**: 自动识别并启动Windows服务（如NetTime服务）
- **多程序启动**: 支持同时启动多个程序（如主程序和服务程序）
- **更新顺序控制**: 按照配置文件顺序更新软件，确保依赖关系
- **系统托盘**: 后台运行，支持系统托盘图标和静默更新
- **跨平台**: 支持Windows、Linux、macOS
- **工作流程**: 提供便捷的工作流程工具，支持单个软件更新和同步
- **页面快检（维护者）**: [`soft_page_check/`](soft_page_check/README.md) 抓取装机清单页面标题并与历史比对；月度 A 类约 42 页、季度全量约 2300+ 页；开源项可经工作台直下 GitHub Release，有变化再决定是否更新 `software/`

### 📦 支持的软件
- **文本编辑器**: Notepad++、notepad-、SublimeText、EditPlus、EmEditor(大文件16T)、UltraEdit

- **系统工具**: CCleaner、WiseCare365、Everything、WinMemoryCleaner、CrystalDiskInfo、NetTime（清理优化怎么选见 [CCleaner vs WiseCare365 vs PC Fresh 对比](CCleanerPro_vs_WiseCare365Pro_vs_PCFresh.txt)）

- **压缩工具**: WinRAR、7-Zip、非常好用看图工具XnViewMP

- **卸载与数据恢复**: GeekUninstaller（单文件免安装，卸载快、清残留、支持系统自带应用）、DiskGenius（分区管理 / 误删文件恢复），均位于 `system_good/`

- **启动管理**: HiBit Startup Manager，查找重复文件 Duplicate Cleaner Pro

- **系统优化**: system_good目录包含多个系统工具
  - 驱动管理: 驱动人生海外版 (DriverTalent)
  - 系统优化: 开始菜单StartBackAIO支持全系win、关闭补丁更新、kms激活、关闭自带杀毒
  - 实用工具: Ditto剪贴板、DuplicateCleaner重复文件清理、Putty、MobaXterm、SmartDefrag磁盘整理、PC Fresh性能调优、WizTree磁盘空间分析、PasteEx剪贴板落文件等
  - 文件服务器: [copyparty](https://github.com/9001/copyparty) - 本地自行建站同步、Web文件服务器、开源安全、多平台支持
  - DNS配置工具: 一键配置加密DNS (DoH)
    - `Configure_AdGuard_DNS.bat` - 配置 AdGuard DNS（免费，拦截广告、跟踪器、恶意网站）  
    - `Configure_18bit_DNS.bat` - 配置 18bit 加密DNS（拦截广告、恶意网站）
    - `Restore_Default_DNS.bat` - 还原为默认DNS设置（自动获取）
  - 任务栏 / 桌面快捷方式（Win10/Win11，无需管理员，路径自适应）
    - `Pin_system_good_to_taskbar.bat` - 批量固定到任务栏（默认含 system_good + 同级常用软件，清单见 `Pin_taskbar_targets.json`）
    - `Create_desktop_shortcuts.bat` - 同上列表，在桌面创建 `.lnk`
    - 部署在 `D:\Program Files\system_good` 时，自动在 `D:\Program Files\` 下解析 `notepad++`、`everything` 等子目录

- **GitHub Releases 按需更新**: `software/GithubWinDownTools/` 提供独立 Python 脚本，按 `apps.json` 从 GitHub Releases 抓取版本并下载安装包（支持 Windows / macOS / Linux 分平台配置）；Windows 可双击 `run_update.bat`。详细用法见 [GithubWinDownTools 说明](software/GithubWinDownTools/README.md)。该目录已列入 `config.json` 的 `software_dirs`，可与主同步工具一并拉取。

- **更多软件**: 可轻松扩展支持，有其他需要可以发帖

### 🚀 快速一键同步，无需安装环境,win10-11测试通过，win服务版权限问题

  - **下载 config.json、sync_software.exe**

  - **修改下config.json的路径，启动 sync_software.exe，即可使用，自动更新所有软件到最新版本

### 🚀 快速一键同步，安装python环境，win服务器版+win10-11测试通过

  - **下载 config.json、sync_software.py 、 sync_software.bat

  - **修改下config.json的路径，启动 sync_software.bat，即可使用

## 项目结构

```
softgitup/
├── config.json              # 配置文件
├── soft_manager.py          # 本地管理工具
├── soft_sync.py            # 同步工具（GUI版本）
├── sync_software.py        # 完整同步工具（命令行，推荐）
├── build_exe.py            # 打包脚本
├── generate_and_push.bat   # 一键生成 list.txt 并 push
├── soft_page_check/        # 页面标题快检 + A 类工作台（见 README）
│   ├── monthly_sop.bat     # 月度更新 SOP 主入口（推荐）
│   ├── monthly_check.bat   # 仅 A 类快检（约 42 页）
│   ├── open_monthly_a.bat  # 旧→新版本工作台 / 装机开源清单
│   ├── gh_soft_map.json    # software/ ↔ gh-release-fetch 映射
│   └── monthly_check_full.bat  # 季度全量（A+装机+423down+7xiazai+list三站）
├── software/               # 本地软件目录
│   ├── CCleaner/
│   ├── EditPlus/
│   ├── everything/
│   ├── notepad++/
│   ├── SublimeText/
│   ├── gh-release-fetch/   # GitHub Releases 按需下载（auto_update.exe、apps/）
│   └── ...
├── logs/                   # 日志目录
├── README.md              # 项目说明（中文）
└── README_EN.md           # Project docs (English)
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

#### GitHub 配置（默认）
编辑 `config.json` 文件：
```json
{
  "git_platform": "github",
  "github_repo": "https://github.com/shellsec/softgitup",
  "gitlab_repo": "https://gitlab.com/your-username/softgitup",
  "manager_base_path": "./software",
  "sync_base_path": "",
  "sync_time": "07:00",
  "auto_start": true,
  "auto_kill": true,
  "git_mirrors": [
    "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
  ],
  "process_map": {
    "notepad++": ["notepad++.exe"],
    "NetTime": ["NetTime.exe", "NetTimeService.exe"]
  },
  "start_map": {
    "notepad++": "notepad++.exe",
    "NetTime": ["NetTimeService.exe", "NetTime.exe"]
  },
  "service_map": {
    "NetTimeService.exe": "NetTimeSvc"
  },
  "start_after_update": [
    "NetTime",
    "everything",
    "WinMemoryCleaner"
  ]
}
```

#### GitLab 配置
切换到 GitLab 平台：
```json
{
  "git_platform": "gitlab",
  "github_repo": "https://github.com/shellsec/softgitup",
  "gitlab_repo": "https://gitlab.com/your-username/softgitup",
  "manager_base_path": "./software",
  "sync_base_path": "",
  "sync_time": "07:00",
  "auto_start": true,
  "auto_kill": true,
  "git_mirrors": [
    "https://gitlab.com/your-username/softgitup/-/raw/master"
  ],
  "process_map": {
    "notepad++": ["notepad++.exe"],
    "NetTime": ["NetTime.exe", "NetTimeService.exe"]
  },
  "start_map": {
    "notepad++": "notepad++.exe",
    "NetTime": ["NetTimeService.exe", "NetTime.exe"]
  },
  "service_map": {
    "NetTimeService.exe": "NetTimeSvc"
  },
  "start_after_update": [
    "NetTime",
    "everything",
    "WinMemoryCleaner"
  ]
}
```

**配置说明：**
- `git_platform`: 平台类型，可选 `"github"` 或 `"gitlab"`，默认为 `"github"`
- `github_repo`: GitHub 仓库地址（GitHub 平台使用）
- `gitlab_repo`: GitLab 仓库地址（GitLab 平台使用）
- `git_mirrors`: 镜像源列表，支持多个镜像源作为备用

### 4. 使用完整同步工具（推荐）

**方式1: 使用编译后的可执行文件（无需Python环境）** ⭐⭐⭐⭐⭐
```bash
# 直接运行编译后的 exe 文件
sync_software.exe
```
**优点**：
- ✅ 无需安装 Python
- ✅ 文件小（5-15 MB）
- ✅ 启动速度快
- ✅ 性能更好
- ✅ 单文件部署

**方式2: 使用Python脚本**
```bash
# 使用完整同步工具（命令行）
python sync_software.py

# 或使用批处理（无需Python环境）
一键快速同步.bat
```

### 5. 使用管理工具
```bash
# 扫描本地软件并推送到GitHub
python soft_manager.py

# 或使用批处理一键操作
generate_and_push.bat
```

### 6. 使用GUI同步工具
```bash
# 启动GUI同步工具（系统托盘）
python soft_sync.py
```

## 打包和编译

### 编译为可执行文件
使用 PyInstaller 将 Python 程序打包成可执行文件：

```bash
# 使用 build_exe.py 脚本打包
python build_exe.py
```

打包脚本提供多种选项：
1. **构建所有程序** (推荐) - 包含GUI和控制台版本
2. **只构建控制台版本** - 无GUI依赖，避免PyQt5 DLL问题
3. **只构建GUI版本** - 包含完整的GUI功能
4. **清理构建文件** - 清理临时文件

### 直接使用 PyInstaller 编译
也可以直接使用 PyInstaller 编译 `sync_software.py`：

```bash
# 基础编译
pyinstaller --onefile --name=sync_software sync_software.py

# 优化编译（推荐）
pyinstaller --onefile --name=sync_software --clean --noconfirm sync_software.py
```

**生成的文件**：
- `dist/sync_software.exe` - 编译后的可执行文件

### 生成的可执行文件
- `sync_software.exe` - 完整同步工具（控制台，推荐）
- `SoftGitUp_Workflow.exe` - 工作流程工具（控制台）
- `SoftGitUp_Manager.exe` - 管理工具（GUI）
- `SoftGitUp_Sync.exe` - 同步工具（GUI，系统托盘）
- `SoftGitUp_Sync_Simple.exe` - 简化同步工具（控制台）

## 工作流程

### 维护者：检查 → 更新 → 发布

**原则**：`software/` 不更新也能正常同步使用；快检只是提醒「可能有新版本」，标题变化不等于必须更新。

| 频率 | 操作 | 说明 |
|------|------|------|
| **约每月** | [`soft_page_check/monthly_sop.bat`](soft_page_check/monthly_sop.bat) 选 `[1]` | A 类 ~42 页快检 + 步骤引导；或只跑 `monthly_check.bat` |
| **看工作台** | [`soft_page_check/open_monthly_a.bat`](soft_page_check/open_monthly_a.bat) | `reports/monthly_a.html`：旧→新版本 + 装机开源可直下 |
| **装机开源** | [`soft_page_check/monthly_a_download_soft_github.bat`](soft_page_check/monthly_a_download_soft_github.bat) | 只下载不安装；先清空再拉到 `gh-release-fetch/windows/`（gitignore，不入库） |
| **约每季度** | [`soft_page_check/monthly_check_full.bat`](soft_page_check/monthly_check_full.bat) **连跑两次** | A + 装机 + 423down + 7xiazai + list 三站全量；报告七分区均有比对 |
| **list 三站（可选）** | [`soft_page_check/monthly_check_list.bat`](soft_page_check/monthly_check_list.bat) | 仅 hybase/dayanzai/down66（`list/*_urls.txt`） |
| **有变化时** | 打开 `soft_page_check/reports/monthly_a.html` / `index.html` 确认 | 423down / 网盘 / 破解版须浏览器手工下载 |
| **确定更新** | 替换 `software/` 对应子目录 | 开源包在 `software/gh-release-fetch/windows/`；也可跑 `run_update.bat` |
| **发布** | 根目录 `generate_and_push.bat` | 生成 `list.txt` 并 push |
| **可选** | 编辑 `Lastb_soft_version.txt` | 改装机说明或 digest 摘要 |

首次使用每个监控范围需**连续快检两次**才有「标题变化」；详见 [soft_page_check 说明](soft_page_check/README.md)。

### 客户端：拉取更新

```bash
# 推荐：完整同步工具
python sync_software.py
# 或
sync_software.exe
# 或
一键快速同步.bat
```

### 传统发布流程（跳过快检时）

1. **更新软件文件**: 将新版本放入 `software/` 目录
2. **生成列表并推送**: 运行 `generate_and_push.bat`（或 `python soft_manager.py`）
3. **同步到其他设备**: 各端运行 `sync_software.bat` / `sync_software.exe`

## 配置说明

### 配置文件 (config.json)

#### 基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `github_repo` | GitHub仓库地址 | - |
| `manager_base_path` | 管理工具扫描目录 | `./software` |
| `sync_base_path` | 同步工具下载目录（为空则使用项目根目录） | `""`（空字符串） |
| `sync_time` | 自动同步时间 | `07:00` |
| `git_mirrors` | Git镜像源列表 | - |
| `download_timeout` | 下载超时时间(秒) | `30` |
| `retry_times` | 重试次数 | `3` |
| `retry_delay` | 重试延迟(秒) | `5` |
| `log_level` | 日志级别 | `INFO` |
| `check_interval` | 检查间隔(秒) | `3600` |

**注意**：
- **pyinstaller 编译版本**：当 `sync_base_path` 为空时，会自动查找 `config.json` 所在目录
  - 优先在可执行文件所在目录查找
  - 如果找不到，会向上查找最多 3 层
  - 这样可以将 `sync_software.exe` 和 `config.json` 放在不同目录
- **Python 脚本版本**：使用脚本所在目录作为基础路径

#### 自动进程管理配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `auto_kill` | 更新前自动关闭相关进程 | `true` |
| `auto_start` | 更新后自动启动程序 | `true` |
| `process_map` | 进程映射表，定义每个软件对应的进程名 | `{}` |
| `start_map` | 启动路径映射表，定义每个软件的启动路径（支持数组） | `{}` |
| `service_map` | 服务映射表，定义服务程序对应的Windows服务名 | `{}` |
| `start_after_update` | 更新后需要自动启动的程序列表 | `[]` |
| `software_dirs` | 软件目录映射，控制更新顺序 | `{}` |

#### 进程映射配置示例

`process_map` 用于定义更新时需要关闭的进程，支持多个进程：
```json
{
  "process_map": {
    "notepad++": ["notepad++.exe"],
    "NetTime": ["NetTime.exe", "NetTimeService.exe"],
    "UltraEdit": ["uedit64.exe", "uedit32.exe"],
    "system_good": ["putty.exe", "SmartDefrag-Pro.exe", "Ditto.exe"]
  }
}
```

#### 启动路径配置示例

`start_map` 支持单个程序或多个程序启动：

1. **单个程序**（字符串）：
   ```json
   {
     "start_map": {
       "notepad++": "notepad++.exe"
     }
   }
   ```

2. **多个程序**（数组）：按顺序启动
   ```json
   {
     "start_map": {
       "NetTime": ["NetTimeService.exe", "NetTime.exe"]
     }
   }
   ```

3. **路径格式**：
   - **相对路径**（推荐）：相对于软件目录
     ```json
     "NetTime": "NetTime.exe"                    // D:\Program Files\NetTime\NetTime.exe
     "NetTime": "bin/NetTime.exe"                // D:\Program Files\NetTime\bin\NetTime.exe
     ```
   - **绝对路径**：完整路径
     ```json
     "some_app": "C:/OtherPath/app.exe"          // 完整绝对路径
     ```

#### Windows服务配置示例

`service_map` 用于将服务程序映射到Windows服务名，系统会自动使用 `net start` 启动服务：

```json
{
  "service_map": {
    "NetTimeService.exe": "NetTimeSvc",
    "Everything.exe": "Everything"              // 如果Everything安装为服务
  }
}
```

**工作原理**：
- 如果程序在 `service_map` 中，系统会使用 `net start [服务名]` 启动服务
- 如果程序不在 `service_map` 中，系统会直接运行程序文件
- 支持服务已在运行的情况检测

#### 更新后自动启动配置

`start_after_update` 定义更新完成后需要自动启动的程序：
```json
{
  "start_after_update": [
    "NetTime",
    "everything",
    "WinMemoryCleaner",
    "notepad++"
  ]
}
```

**注意**：
- 如果 `start_after_update` 为空数组 `[]`，则所有软件更新后都会自动启动（当 `auto_start: true` 时）
- 如果 `start_after_update` 有值，则只有列表中的软件会在更新后自动启动

#### 更新顺序控制

软件更新顺序由 `config.json` 中 `software_dirs` 的顺序决定：

```json
{
  "software_dirs": {
    "WinMemoryCleaner": "WinMemoryCleaner",      // 第一个更新
    "NetTime": "NetTime",                        // 第二个更新
    "system_good": "system_good"                 // 最后更新
  }
}
```

**工作原理**：
- 系统按照 `software_dirs` 中配置的顺序依次更新软件
- 如果远程列表中有但 `software_dirs` 中未配置的软件，会在最后按远程列表顺序更新
- 可以通过调整 `software_dirs` 的顺序来控制更新优先级

#### 同步路径配置说明

`sync_base_path` 支持两种配置方式：

1. **自动使用项目根目录**（推荐）：
   ```json
   "sync_base_path": ""
   ```
   - 当配置为空字符串时，软件会下载到项目根目录
   - 例如：`E:\GITHUB\softgitup\NetTime\`、`E:\GITHUB\softgitup\everything\`
   - 优点：无需管理员权限，便于管理，便于备份和迁移

2. **指定自定义路径**：
   ```json
   "sync_base_path": "D:/Program Files"
   ```
   - 软件会下载到指定的目录
   - 例如：`D:\Program Files\NetTime\`、`D:\Program Files\everything\`
   - 注意：如果目录不存在，系统会自动创建

### Git加速源配置
使用 `gh-proxy.com` 作为Git加速下载源：
```json
"git_mirrors": [
  "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
]
```

## GitLab 部署说明

### 为什么选择 GitLab？

1. **企业级部署**: 支持私有化部署，适合内网环境
2. **国内访问**: GitLab.com 或自建实例，访问更稳定
3. **功能丰富**: 内置 CI/CD、项目管理等企业级功能
4. **数据安全**: 可完全控制数据存储位置

### GitLab 部署步骤

#### 1. 创建 GitLab 仓库

1. 登录 GitLab（GitLab.com 或自建实例）
2. 创建新项目（Project）
3. 将代码推送到 GitLab 仓库

```bash
git remote add gitlab https://gitlab.com/your-username/softgitup.git
git push gitlab master
```

#### 2. 配置 config.json

修改 `config.json` 文件：

```json
{
  "git_platform": "gitlab",
  "gitlab_repo": "https://gitlab.com/your-username/softgitup",
  "git_mirrors": [
    "https://gitlab.com/your-username/softgitup/-/raw/master"
  ]
}
```

**重要配置项：**
- `git_platform`: 设置为 `"gitlab"`
- `gitlab_repo`: 填写你的 GitLab 仓库地址
- `git_mirrors`: GitLab 的 Raw 文件 URL 格式为 `https://gitlab.com/user/repo/-/raw/branch`

#### 3. 验证配置

运行同步测试：

```bash
python sync_software.py
```

或使用批处理文件：

```bash
一键快速同步.bat
```

#### 4. 切换回 GitHub

如果需要切换回 GitHub，只需修改 `git_platform`：

```json
{
  "git_platform": "github",
  "github_repo": "https://github.com/shellsec/softgitup",
  "git_mirrors": [
    "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
  ]
}
```

### GitLab 自建实例部署

如果你有自建 GitLab 实例：

1. **配置仓库地址**：
```json
{
  "git_platform": "gitlab",
  "gitlab_repo": "https://your-gitlab-instance.com/your-username/softgitup",
  "git_mirrors": [
    "https://your-gitlab-instance.com/your-username/softgitup/-/raw/master"
  ]
}
```

2. **私有仓库访问**：
   - 如果仓库是私有的，需要在 GitLab 中创建 Personal Access Token
   - 在 URL 中包含 token：`https://oauth2:YOUR_TOKEN@your-gitlab-instance.com/user/repo/-/raw/master`

3. **分支配置**：
   - GitLab 默认分支可能是 `master` 或 `main`
   - 确保 `git_mirrors` 中的分支名与实际分支名一致

### 常见问题

**Q: GitLab 和 GitHub 可以同时使用吗？**
A: 可以，在 `git_mirrors` 中同时配置两个平台的镜像源，系统会按顺序尝试。

**Q: 如何知道当前使用的是哪个平台？**
A: 查看日志文件，会显示使用的镜像源 URL。

**Q: GitLab 私有仓库如何配置？**
A: 在 URL 中包含访问令牌，或使用 GitLab 的 Deploy Token。

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

### 自动进程管理

系统支持在更新前自动关闭相关进程，更新后自动启动程序：

1. **更新前关闭进程**：
   - 当 `auto_kill: true` 时，系统会在下载文件前自动关闭 `process_map` 中定义的进程
   - 支持关闭多个进程（如 NetTime 的主程序和服务程序）
   - 使用 Windows `taskkill` 命令强制关闭进程

2. **更新后启动程序**：
   - 当 `auto_start: true` 时，系统会在文件更新完成后自动启动程序
   - 根据 `start_after_update` 列表决定启动哪些程序
   - 支持单个程序或多个程序启动（数组配置）
   - 支持相对路径和绝对路径配置
   - 自动识别Windows服务并使用 `net start` 启动

3. **Windows服务支持**：
   - 自动检测程序是否在 `service_map` 中
   - 如果是服务，使用 `net start [服务名]` 启动
   - 如果是普通程序，直接运行可执行文件
   - 支持服务已在运行的情况检测

4. **更新顺序控制**：
   - 按照 `config.json` 中 `software_dirs` 的顺序更新
   - 确保依赖关系正确的软件按正确顺序更新

5. **工作流程**：
   ```
   开始同步 → 按 software_dirs 顺序 → 检查 auto_kill → 关闭相关进程 → 
   下载更新文件 → 检查 auto_start → 检查 start_after_update → 
   检查 service_map → 启动服务或程序
   ```

### 单个软件更新
```bash
# 只更新特定软件
python -c "from soft_manager import SoftManager; SoftManager().generate_list_file('everything')"
```

### 定时同步
- 支持自定义同步时间
- 后台静默更新
- 系统托盘通知
- 自动进程管理

### 日志管理
- 详细的同步日志
- 错误追踪和调试
- 可配置日志级别
- 进程关闭和启动日志记录

## 故障排除

### 常见问题

**Q: 如何使用无需Python环境的版本？**
A: 使用 PyInstaller 编译后的 `sync_software.exe`：
1. 直接运行：`sync_software.exe`
2. 优点：无需安装Python、单文件部署、使用方便
3. 下载地址：从项目发布页面获取编译好的 exe 文件

**Q: 如何编译 sync_software.exe？**
A: 使用 PyInstaller 编译：
```bash
# 使用 build_exe.py 脚本打包
python build_exe.py
# 选择选项 2：只构建控制台版本

# 或直接使用 PyInstaller 编译
pyinstaller --onefile --name=sync_software --clean --noconfirm sync_software.py
```

**Q: 编译后运行报错 "DLL load failed while importing QtWidgets"？**
A: 这是PyQt5 DLL依赖问题，建议：
1. 使用控制台版本：`python build_exe.py` 选择选项2
2. 直接运行Python脚本：`python sync_software.py`
3. 或使用批处理：`一键快速同步.bat`（无需Python环境）
4. 安装Visual C++ Redistributable后重新编译

**Q: 同步失败怎么办？**
A: 检查网络连接和GitHub仓库权限，确保使用正确的Git加速源。

**Q: 文件修改时间不匹配？**
A: 这通常是因为文件内容发生了变化，系统会自动下载最新版本。

**Q: 如何添加新的软件？**
A: 将软件放入software目录，在config.json中添加软件名称，然后运行管理工具。

**Q: 如何配置自动关闭进程和启动程序？**
A: 在config.json中配置：
1. 设置 `auto_kill: true` 和 `auto_start: true`
2. 在 `process_map` 中添加软件对应的进程名
3. 在 `start_map` 中添加软件的启动路径（支持相对路径和绝对路径）
4. 在 `start_after_update` 中添加需要自动启动的程序名称

**Q: 启动路径如何配置？**
A: 支持两种方式：
- 相对路径：`"NetTime": "NetTime.exe"` 或 `"NetTime": "bin/NetTime.exe"`
- 绝对路径：`"some_app": "C:/Path/app.exe"`

**Q: system_good 包含多个程序，如何配置？**
A: 在 `process_map` 的 `system_good` 数组中添加所有需要关闭的进程名：
```json
"system_good": ["putty.exe", "SmartDefrag-Pro.exe", "Ditto.exe", ...]
```

**Q: 如何启动多个程序？**
A: 在 `start_map` 中使用数组配置：
```json
"NetTime": ["NetTimeService.exe", "NetTime.exe"]
```
系统会按数组顺序依次启动程序。

**Q: 如何配置Windows服务？**
A: 在 `service_map` 中配置服务程序到服务名的映射：
```json
"service_map": {
  "NetTimeService.exe": "NetTimeSvc"
}
```
系统会自动使用 `net start` 命令启动服务。

**Q: 如何控制软件更新顺序？**
A: 调整 `config.json` 中 `software_dirs` 的顺序即可。系统会按照配置的顺序依次更新软件。

**Q: 服务启动失败怎么办？**
A: 确保服务已安装。可以通过以下方式安装服务：
- 使用软件提供的安装脚本（如 NetTime 的 `ChangeNetTimePath.bat`）
- 或手动使用 `sc create` 命令安装服务

**Q: DNS 配置脚本如何使用？**
A: system_good 目录下提供了三个 DNS 配置脚本：
- `Configure_18bit_DNS.bat` - 配置 18bit 加密 DNS（拦截广告、恶意网站）
- `Configure_AdGuard_DNS.bat` - 配置 AdGuard DNS（免费，拦截广告、跟踪器）
- `Restore_Default_DNS.bat` - 还原为默认 DNS 设置
使用方法：右键点击脚本，选择"以管理员身份运行"。配置完成后，可在系统设置中验证 DNS 是否显示"已加密"。

**Q: DNS 配置后 DoH 未生效怎么办？**
A: 如果配置后 DoH 未生效，可以尝试：
1. 重启网络适配器（禁用后重新启用）
2. 在系统设置中手动启用 DoH：
   - 设置 → 网络和 Internet → 以太网（或 WLAN）→ 硬件属性 → DNS 服务器分配
   - 将"首选 DNS 加密"和"备用 DNS 加密"设置为"开（手动模板）"
3. 重启计算机
4. 某些 Windows 11 版本可能需要通过系统设置手动配置 DoH

**Q: 如何一键固定任务栏或创建桌面快捷方式？**
A: 脚本位于 `software/system_good/`（或同步后的 `system_good` 目录），共用清单 `Pin_taskbar_targets.json`：

| 脚本 | 作用 |
|------|------|
| `Pin_system_good_to_taskbar.bat` | 批量固定到任务栏 |
| `Create_desktop_shortcuts.bat` | 在桌面（及 OneDrive 桌面）创建快捷方式 |

**路径自适应**：脚本在 `…\system_good\` 内时，软件根目录为其**上一级**（如 `D:\Program Files`），会在该根下按子文件夹名查找 exe；本机不存在的项会跳过，不中断。

**默认处理（双击即可，无需额外参数）**：

- **system_good**：PuTTY、VirtualDesktopSwitcher、WindowsBatchScriptManager、MediaManage、Keyvol  
- **同级软件**：Notepad++、Notepad--、Everything、Sublime Text、EditPlus、CCleaner、7-Zip、WinRAR、UltraEdit、CrystalDiskInfo、WinMemoryCleaner、NetTime、HiBit Startup Manager、PotPlayer  

**可选参数**（PowerShell 或 bat 后追加）：

- `-IncludeOptional` — Ditto、StartBack（需已解压到 system_good）
- `-IncludeMaintenance` — SmartDefrag-Pro
- 任务栏专用：`-RestartExplorer`（Win11 图标未刷新时）、`-PinMode FolderOnly`（兼容性最好）

修改默认列表：编辑 `Pin_taskbar_targets.json` 中 `groups.default.targets`。

### 日志查看
```bash
# 查看管理工具日志
tail -f logs/manager.log

# 查看同步工具日志
tail -f logs/sync.log

# 查看完整同步日志
tail -f logs/complete_sync.log
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

## 📚 相关文档

- [English README](README_EN.md) — English version of this document
- [**页面快检与月度 SOP**](soft_page_check/README.md) — 维护者：标题比对、报告页、更新与发布流程
- [配置说明](配置说明.md) - 详细的配置参数说明
- [本地服务器使用说明](本地服务器使用说明.md) - 搭建本地文件服务器指南
- [手机隐私安全配置指南](手机隐私安全配置指南.md) - iOS/Android/国产系统隐私安全配置完整指南（中文）
- [Mobile Privacy & Security Guide](Mobile_Privacy_Security_Guide.md) - Complete mobile privacy configuration guide (English)
- [常用工具开源下载](常用工具开源下载.md) - 常用工具开源下载
- [清理优化选型对比：CCleaner Pro vs WiseCare365 Pro vs PC Fresh](CCleanerPro_vs_WiseCare365Pro_vs_PCFresh.txt) - 自动优化功能、实测数据、配置指南与适用场景对比（2026）
- [GitHub Releases 按需更新（githubwindowntools）](software/githubwindowntools/README.md) - `apps.json` 配置、启用应用、指定平台与镜像回退等说明
- [装机清单原文](Lastb_soft_version.txt) - 与本仓库 `software/system_good/` 等目录配套的软件与隐私向说明（长文）

---

**注意**: 请确保遵守相关软件的使用许可协议，本工具仅用于个人学习和合法用途。 