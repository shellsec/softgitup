# GitHub 发行版拉取工具（GH Release Fetch）

## ☕ 请我喝可乐

开源不易，欢迎赞助支持：  
👉 [爱发电](https://ifdian.net/a/shellsec)

**中文** · [English README](README.md)

| | |
|:---|:---|
| **英文名称** | **GH Release Fetch** |
| **中文名称** | **GitHub 发行版拉取工具** |
| **仓库地址** | [`shellsec/gh-release-fetch`](https://github.com/shellsec/gh-release-fetch) |
| **英文描述** | **Search by name, download or update** — no hunting Release pages, version tags, or direct URLs. A curated JSON catalog + scripts resolve the latest GitHub Release (or CDN/manifest where configured), pick the right Windows/macOS/Linux asset, download it, and optionally run the installer. Mirrors are tried first with fallback to `github.com`. |
| **中文描述** | **按名字搜索即可下载/更新**——不必自己翻 GitHub Release 页、不必记版本号或找直链。维护者在 JSON 清单里写好匹配规则；你用 `lookup_app.bat` 搜软件名，脚本自动解析最新 Release 并匹配对应平台安装包，镜像失败回退官方。 |

### 你能得到什么

| 你**不用**自己做 | 工具替你做了 |
|------------------|--------------|
| 去 GitHub 翻 Release、在几十个附件里找 x64 / dmg / AppImage | 按清单规则解析**最新 tag**，过滤架构与格式，选出对的安装包 |
| 记住「现在该下 v几、链接是哪条」 | 下载文件名通常带**版本号**（由 `save_name` 等模板生成） |
| 自己维护一长串下载地址 | 仓库 **500+ 条**已收录规则，**模糊搜索**即可用 |

```bat
lookup_app.bat drawio
REM 选序号 → 1 立刻下载（无需改 enabled）→ 2 加入并下载 → 3 仅加入列表 → 4 启用
```

**边界**：规则写在清单里，**收录与维护**仍是维护者/社区工作；部分条目仅占位或规则不全时无法自动下。非 GitHub/CDN 可解析的分发走 **频道线**（`search_soft_pages.bat` 搜介绍页，人工下载）。

### 复制到 GitHub「About」

在仓库页右侧 **About → ⚙** 粘贴：

**Description（中文）**

```
GitHub 发行版拉取工具：500+ 开源软件清单，搜名字即可下载/更新，无需自己翻 Release 页或找下载链接。脚本自动解析最新版本并匹配 Win/macOS/Linux 安装包，支持 lookup 一键下载与批量更新。
```

**Description（English）**

```
GH Release Fetch: 500+ app catalog — search by name, download/update without hunting Release pages or URLs. Auto-resolves latest assets for Windows/macOS/Linux. One-click lookup + batch updates.
```

**Website（可选）** `https://github.com/shellsec/gh-release-fetch#readme`

**Topics（建议）** `github-releases` `windows` `macos` `linux` `download-manager` `open-source-software` `automation` `python` `software-catalog`

---

这是一个 **「搜名字 → 自动找最新包 → 下载（可选安装）」** 的工具仓库：维护者把「怎么从 GitHub Releases / CDN 找对安装包」写成 JSON 规则；**使用者不必自己盯版本号、不必去 Release 页复制链接**。

底层仍基于 **GitHub Releases**（及发布页 HTML / API），按需更新 Windows / macOS / Linux（及可选 Android APK 下载）安装包或归档。

**曾用称呼**：GithubWinDownTools；现用 **GH Release Fetch / GitHub 发行版拉取工具** 以反映多平台配置与用途。

### 设计原则（两条线）

| 线 | 适用 | 本仓库 |
|----|------|--------|
| **Git 线** | 开源、Release 在 GitHub/Gitee 上可解析 | `apps/` + `lookup_app` → `run_saved_apps`；可选 `GiteeExploreHot/`、`VibeCodingToolsDown/` |
| **频道线** | 其它（介绍页、网盘、厂商 CDN、非 Release 分发） | `tools/soft_page_check/` 定期抓标题比对；`search_soft_pages.bat` 按标题打开链接；变化后 **人工** 下载或替换装机包 |

**开源走 Git，其它走各类频道；频道按节奏定期快检**（不必把非 Git 软件硬塞进 `apps/`）。大眼仔等频道里筛出的开源项可用 `import_dayanzai_windows.py` 写入 Git 线；本地抓取缓存 `tools/dayanzai_cache/` 可删（`.gitignore`），再导入时会自动重建。

核心文件：

- `auto_update.py`：按配置抓取版本、下载文件、按需启动安装程序（优先读取 `apps/` 目录合并结果，否则使用单文件 `apps.json`）
- `apps/`：推荐布局——[`apps/root.json`](apps/root.json)（全局）+ [`apps/windows/*.json`](apps/windows/) + [`apps/darwin/*.json`](apps/darwin/) + [`apps/linux/*.json`](apps/linux/)（均按分类拆成多个数组文件，与 windows 命名风格一致）；若无分片目录则回退单文件 `apps/darwin.json`、`apps/linux.json`。历史单文件备份见 `apps.json.monolith.bak`；darwin/linux 由单文件迁出后的备份见 `apps/darwin.json.bak`、`apps/linux.json.bak`
- `run_update.bat`：Windows 下一键检查 Python、安装依赖并执行 `python auto_update.py`
- `lookup_app.py` / `lookup_app.bat`：在清单中**模糊检索** → 选条目 → **1 立刻下载 / 2 加入并下载 / 3 加入列表 / 4 启用**（见 §3）
- `search_soft_pages.bat`：在 [`tools/soft_page_check/`](tools/soft_page_check/) 已抓取的介绍页**标题**中搜索并打开链接；**无参数**时提示输入关键词（与 GitHub 清单互补）
- `run_saved_apps.bat`：按列表一键开启并执行 `auto_update.py`（与 `lookup_app` 配套）

### 推荐软件介绍（Markdown）

不知道清单里有什么、各自干什么用时，先看各平台全分类导读（简介、仓库、分片、配置完整度、lookup 命令）：

| 平台 | 中文导读 | 英文简表 | 规模（约） |
|------|----------|----------|------------|
| Windows | [`RECOMMENDED.zh-CN.md`](RECOMMENDED.zh-CN.md) | [`RECOMMENDED.md`](RECOMMENDED.md) | 567 条 |
| macOS | [`RECOMMENDED.darwin.zh-CN.md`](RECOMMENDED.darwin.zh-CN.md) | [`RECOMMENDED.darwin.md`](RECOMMENDED.darwin.md) | 539 条 |
| Linux | [`RECOMMENDED.linux.zh-CN.md`](RECOMMENDED.linux.zh-CN.md) | [`RECOMMENDED.linux.md`](RECOMMENDED.linux.md) | 539 条 |

刷新三份文档：`python tools/generate_recommended_md.py`（或指定 `windows` / `darwin` / `linux`）。分片统计见 [`CATALOG.md`](CATALOG.md)。

### VibeCodingToolsDown（可选独立清单）

与主 [`apps/`](apps/) **完全分离** 的第二套配置，目录为 [`VibeCodingToolsDown/`](VibeCodingToolsDown/)：面向 AI 编程相关 IDE 等条目；各产品下载直链由 [`VibeCodingToolsDown/scripts/build_manifest.py`](VibeCodingToolsDown/scripts/build_manifest.py) 聚合写入 **`dist/vibecoding/manifest.json`**，[`auto_update.py`](auto_update.py) 通过条目中的 `resolve_via=github_pages_manifest` 与 [`VibeCodingToolsDown/root.json`](VibeCodingToolsDown/root.json) 里的 `vibecoding_manifest_url` 读取（支持本地相对路径或 **HTTPS**，例如 **`raw.githubusercontent.com`** 上的 manifest）。

- **Windows 一键**：[`VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat`](VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat)（在本目录内执行：装依赖 → 生成 manifest → 调用 `vibe_update.py`）
- **命令行**：`python auto_update.py --apps-dir VibeCodingToolsDown`；或在 [`VibeCodingToolsDown/`](VibeCodingToolsDown/) 下执行 `python vibe_update.py`（内部仍调用仓库根的 `auto_update.py`，仅固定 `--apps-dir`）
- **批量关闭/恢复 `enabled`**：[`VibeCodingToolsDown/tools/reset_enabled_json.bat`](VibeCodingToolsDown/tools/reset_enabled_json.bat) / [`apply_enabled_snapshot.bat`](VibeCodingToolsDown/tools/apply_enabled_snapshot.bat)（调用仓库根 `tools/*.py`，快照在 `VibeCodingToolsDown/tools/`，与主 `apps/` 互不覆盖）
- **GitHub Actions**：仓库根未内置 workflow 文件（HTTPS PAT 无 `workflow` 权限时无法推送）。将 [`VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml`](VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml) 复制为 `.github/workflows/vibecodingtoolsdown-pages.yml` 后，即可定时/手动构建 manifest、提交默认分支并推 **gh-pages**；细节见 [`VibeCodingToolsDown/README.md`](VibeCodingToolsDown/README.md)

### GiteeExploreHot（可选 Gitee 分类 + 下载）

与 [`apps/`](apps/)（面向 **GitHub Releases**）**独立**：[`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/) 按主题维护 `owner/repo`；[`GiteeExploreHot/scripts/fetch_explore_hot.py`](GiteeExploreHot/scripts/fetch_explore_hot.py) 生成 **`data/gitee_downloads.json`**（从 Gitee `releases/latest` 解析附件并归类 **windows / darwin / linux**），[`GiteeExploreHot/scripts/gitee_download.py`](GiteeExploreHot/scripts/gitee_download.py) 可按平台拉取到本包 `downloads/`。**Windows 一键**：[`GiteeExploreHot/run_sync_gitee.bat`](GiteeExploreHot/run_sync_gitee.bat)（可选参数 `windows` / `darwin` / `linux` 表示同步后再下载）。**未接入** `auto_update.py`。详见 [`GiteeExploreHot/README.md`](GiteeExploreHot/README.md)。

### soft_page_check（介绍页标题监控 · 可选）

目录 [`tools/soft_page_check/`](tools/soft_page_check/) 与主 `apps/` **独立**：监控 **dayanzai / down66 / 7xiazai / hybase / 423down / gamer520（游戏）/ 装机 A 类** 等介绍页的 `<title>` 变化，用于发现「可能有新版本」的资讯页，**不负责** GitHub 自动下载。

| 用途 | 入口 |
|------|------|
| **按标题搜介绍页并打开** | 仓库根 **`search_soft_pages.bat`**（无参数时提示输入关键词；亦支持 `search_soft_pages.bat 7zip`） |
| **按标题搜游戏页（gamer520）** | 仓库根 **`search_games.bat`** |
| 月度快检 SOP | `tools\soft_page_check\monthly_sop.bat` |
| **每月 · A 类**（~42 页，~15 秒） | `tools\soft_page_check\monthly_check.bat` |
| **每季 · 频道全量**（~2300+ 页，~20–35 分钟，**只比标题、不下载**） | `tools\soft_page_check\monthly_check_full.bat` |
| 单站快检 / 打开变化页 | `monthly_check_site.bat <站点>` / `open_changed_site.bat <站点>`（`423down` `7xiazai` `hybase` `dayanzai` `down66` **`gamer520`**） |
| list 四站连跑 | `tools\soft_page_check\monthly_check_list.bat`（7xiazai + hybase + dayanzai + down66） |
| 刷新 URL 清单 | `tools\soft_page_check\refresh_urls.bat`（`core` / `all` / `423down` / `7xiazai` …） |
| 清理历史快照 | `tools\soft_page_check\prune_artifacts.bat` |
| HTML 报告 | `tools\soft_page_check\open_report.bat` → `reports/index.html` |
| A 类 GitHub 页变化后拉 Release | `tools\soft_page_check\fetch_github_on_changes.bat`（只读引用本仓库 `apps/` + `auto_update.py`） |

**与 `lookup_app` 的分工**：`lookup_app` → **GitHub Releases 清单**；`search_soft_pages` → **各站工具介绍页标题**；`search_games` → **gamer520 游戏页**（本地近期列表 + 无匹配时站内搜索；均只打开链接，不自动下载）。本仓库通常**无** `Lastb_soft_version.txt`；首次快检需连跑两次才建立「标题变化」基线，详见 [`tools/soft_page_check/README.md`](tools/soft_page_check/README.md)。

```bat
search_soft_pages.bat
REM 无参数：提示输入关键词（与 lookup_app.bat 相同交互）
search_soft_pages.bat 7zip
search_soft_pages.bat --scope dayanzai 优化
search_soft_pages.bat --stats
search_games.bat 艾尔登
```

### 仓库现状与收录范围（约略）

合并配置后规模约为：**Windows 567 条**、**darwin 539 条**、**linux 539 条**（[`apps/windows/`](apps/windows/) 等下各 **30** 个分类分片；**不含** `99-未匹配-windows分片.json` 占位条目）。**分片级概览**见根目录 [`CATALOG.md`](CATALOG.md)（运行 `python tools/generate_catalog_index.py` 可刷新）。精确数以运行 `python auto_update.py` 时日志里「已从 apps/ 目录合并配置」为准。

**移动端**（独立清单 [`apps-mobile/`](apps-mobile/)）：Android **164 条** / **39 分片**（30 类 + 移动专属；GitHub APK **仅下载**）；iOS **52 条** App Store 占位（**不可** auto_update）。索引 [`CATALOG.mobile.md`](CATALOG.mobile.md)。

主清单以 **GitHub Releases**（及镜像）为主；部分 AI IDE（Cursor、Trae、Qoder 等）通过 `resolve_via=github_pages_manifest` 读取 [`apps/root.json`](apps/root.json) 中的 `vibecoding_manifest_url`（默认 `./VibeCodingToolsDown/dist/vibecoding/manifest.json`）。使用前可先运行 `python VibeCodingToolsDown/scripts/build_manifest.py` 刷新 manifest。

**注意**：同一平台内 **`id` 不可重复**（含 `99-` 分片）。若 `auto_update.py` 报「重复的 id」，请从占位分片删除与正式分片同 id 的条目。

Windows 可从 [大眼仔旭 Windows 专区](https://www.dayanzai.me/windows) 批量补收录开源项：`python tools/import_dayanzai_windows.py --apply`（可选本地缓存 `tools/dayanzai_cache/`，导入完成后可删）；同步到 macOS/Linux：`python tools/sync_dayanzai_to_darwin_linux.py`。

收录以 **GitHub（及镜像）上可解析的 Releases 资产** 为主，涵盖编辑器、笔记、安全、云原生、可观测、下载、办公与设计等常见分类。**不包含**破解、盗版或绕过授权的软件分发；个别条目仅含基础字段时需自行补全规则后才能稳定自动下载。

---

## 解决什么问题（痛点）

日常装开源桌面工具时，常见摩擦包括：

- **Release 页信息杂**：同一版本下有 macOS / Linux / Windows、便携版、校验文件等，手动找对的 `.exe` / `.msi` / `.zip` 费时且容易下错架构。
- **版本与链接分散**：页面标题、API `latest`、预发布混在一起，**用户只想装最新版，却要自己判断 tag 和直链**。
- **网络不稳定**：直连 GitHub 慢或被拦；纯镜像站又可能 403、证书异常，需要 **可回退的拉取策略**。
- **工具一多就难维护**：编辑器、笔记、CLI、运行时各自去官网点一遍，**缺少一份可搜索、可一键更新的「软件清单」**。

本仓库把 **「查最新版本 → 选对资产 → 下载 →（可选）安装」** 做成可复用流程：**你负责搜软件名（或维护列表），脚本负责版本解析与链接匹配**（镜像失败回退官方、HTML 与 API 互补等，见下文）。

---

## 面向谁、适合做什么

- **只想装/更新某个开源工具、不想翻 Release 页**：`lookup_app.bat 关键词` → 选 **1 立刻下载**（不必先改 `enabled`）。
- **有一批常用软件、希望定期跟上新版本**：用 **2/3** 加入 `saved_apps_*.json`，再 `run_saved_apps.bat` 批量更新。
- **维护清单或跑定时任务**：把规则写进 JSON，对稳定条目设 `enabled: true`，用任务计划/cron 跑 `auto_update.py`。
- **不适合**：主要走应用商店、无公开可解析安装包、或命名毫无规律且无法写匹配规则的闭源软件（走 **频道线** 或人工）。

---

## 版本与更新：谁需要关注什么

| 角色 | 需要关注什么 |
|------|--------------|
| **普通用户**（lookup 搜名下载） | 一般**不用**自己找下载链接、不用记版本号；搜名字 → 选 1/2 即可 |
| **列表用户**（`run_saved_apps`） | 列表里有哪些软件、定时/一键更新是否成功 |
| **维护者 / 无人值守 cron** | 上游是否改名安装包、匹配规则是否仍有效、哪些条目 `enabled` |

| 技术细节 | 说明 |
|--------|------|
| **脚本每次重新解析「当前最新」** | 以发布页与 GitHub API 为准；`latest` 通常为非草稿、非预发布的最新 tag（因仓库设置而异，以日志为准）。 |
| **本地是否重复下载** | 若本地已有同版本、同名文件，行为以 `auto_update.py` 下载逻辑为准；看日志与文件名中的版本即可。 |
| **配置随上游变** | 上游改 tag 规则或安装包命名时，需在 JSON 调整 `installer_markers`、`download_names` 等（**维护者工作**）。 |
| **条目质量参差** | 仅规则写全的条目适合无人值守；占位条目需补规则或仅手工测试。 |

简言之：**日常使用交给脚本找版本和链接；清单规则与批量策略由你或维护者负责。**

---

## 需求

使用前请确认满足下列条件。

### 运行环境与软件

| 项目 | 说明 |
|------|------|
| **操作系统** | 脚本可在 **Windows、macOS、Linux** 上运行；`run_update.bat` 仅适用于 Windows。 |
| **Python** | **3.6 及以上**（与 `run_update.bat` 提示一致）；建议使用当前仍受支持的 3.x 版本。Windows 也可选 **exe**（见下），日常不必装 Python。 |
| **包管理** | 已安装 **pip**，可执行 `pip install -r requirements.txt`（使用 exe 时可跳过）。 |

### 无 Python（Windows · 可选 exe）

可将日常流程打成 **5 个 exe**，与 [`apps/`](apps/) 放在**同一仓库根目录**。对应 bat：**有 Python 时走 `.py`**，**无 Python 时用 exe**（双击 exe 也会提示输入关键词）。

| exe | bat | 作用 |
|-----|-----|------|
| `lookup_app.exe` | [`lookup_app.bat`](lookup_app.bat) | 模糊搜索 → 1/2/3/4 |
| `run_saved_apps.exe` | [`run_saved_apps.bat`](run_saved_apps.bat) | 按列表批量更新 |
| `search_soft_pages.exe` | [`search_soft_pages.bat`](search_soft_pages.bat) | 搜工具介绍页标题（打开链接） |
| `search_games.exe` | [`search_games.bat`](search_games.bat) | 搜 gamer520 游戏页（本地近期 + 站内搜索回退） |
| `auto_update.exe` | [`run_update.bat`](run_update.bat) / lookup 选 1 调用 | 下载引擎 |

打包（本机需 Python **一次**）：

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_exe.ps1
```

产物在 `dist/exe/`，复制上述 **5 个 exe** 到仓库根即可。维护脚本（`monthly_check` 等）仍依赖 Python。

**打 Release 附件 zip**（含 exe + 清单 + 索引，解压即用）：

```bat
pack_windows_release.bat
```

或：

```powershell
powershell -ExecutionPolicy Bypass -File tools\pack_windows_release.ps1 -Version 1.0.0
```

输出 `dist/release/gh-release-fetch-windows-<版本>.zip`，说明见 [`release/windows/PACKAGING.md`](release/windows/PACKAGING.md)。

### Python 依赖（requirements.txt）

使用 **Python 路径**时安装，包含但不限于：

- `requests`（≥2.25.0）：HTTP 请求、GitHub API
- `beautifulsoup4`（≥4.9.0）：解析 GitHub Releases 页面 HTML

```bash
pip install -r requirements.txt
```

### 网络与访问

| 项目 | 说明 |
|------|------|
| **GitHub** | 需能访问 **`github.com`** 与 **`api.github.com`**（至少其一在回退链路上可用）。条目里的 `releases_url` 若指向镜像（如 `bgithub.xyz`），镜像失败时脚本会 **自动回退到官方 Releases 页**，必要时再试 **GitHub API**。 |
| **稳定性** | 企业网络、代理或防火墙若拦截上述域名，会导致版本检测或下载失败。 |
| **TLS** | 若镜像站证书异常，可使用 `--insecure` 或在 [`apps/root.json`](apps/root.json) 根级设置 `"ssl_verify": false`（有中间人风险，修复证书后建议改回）。 |

### 配置文件

| 项目 | 说明 |
|------|------|
| **推荐** | 存在 [`apps/root.json`](apps/root.json)，且 [`apps/windows/`](apps/windows/)、[`apps/darwin/`](apps/darwin/)、[`apps/linux/`](apps/linux/) 下为若干 JSON **数组**分片（按文件名排序合并，**同一平台内 `id` 不可重复**）。无分片时回退 `apps/darwin.json` / `apps/linux.json`。从旧单文件拆目录可运行 `python tools/split_darwin_linux_to_dirs.py`。 |
| **兼容** | 若不存在 `apps/root.json`，可在仓库根目录放置单文件 `apps.json`（旧版布局）。 |
| **每条应用至少** | `id`、`releases_url`、`repo_path`（详见下文「apps 常用字段」）。 |

### 使用前提与能力边界

- **批量模式**只处理 `enabled: true` 的条目（如直接 `python auto_update.py` 不带 id）。
- **指定 id 下载**（如 `lookup_app` 选 1，或 `auto_update.py drawio`）**不要求** `enabled=true`。
- **数据源以 GitHub 为主**（部分条目走 CDN / manifest）；非可解析分发的闭源产品走 **频道线**。
- 仓库中条目数量多，但 **规则完整度不一**：带齐 `installer_markers`、`download_names`、`save_name` 等的条目才可稳定自动下载；仅有基础字段的条目需自行补全规则后才能依赖脚本下载。

---

## 1. 安装依赖

在仓库根目录执行：

```bash
pip install -r requirements.txt
```

---

## 2. 最快使用方式

### 方式一：Windows 直接双击

运行：

```bat
run_update.bat
```

它会自动：检查 Python → `pip install -r requirements.txt` → `python auto_update.py`。

### 方式二：命令行运行

在仓库目录执行：

```bash
python auto_update.py
```

默认行为：

- 自动识别当前系统平台，读取 `platforms` 下对应列表（来自 `apps/` 合并结果或单文件 `apps.json`）
- **只处理 `enabled: true` 的应用**
- 发布页优先使用条目中的 `releases_url`；失败时回退 GitHub 官方 Releases，再视情况使用 GitHub API
- 版本号优先从发布页中 `releases/tag/<tag>` 一类链接提取，减少与页面标题或 API `latest` 不一致的误判

---

## 3. 如何启用某个应用

### 方式 A：查找脚本（推荐）

在仓库根目录：

```bat
lookup_app.bat drawio
```

或：

```bash
python lookup_app.py drawio
```

**速查**（与无参数运行 `lookup_app` 时屏幕提示一致）：

```text
用法: lookup_app [选项与关键词...]
示例: lookup_app drawio
      lookup_app --platform android termux
选条目后: 1=立刻下载  2=加入并下载  3=加入列表  4=启用
跳过交互: lookup_app -y --download drawio
```

**无参数：** 直接运行 `lookup_app.bat` 会提示输入关键词（同一行可带 `--platform android termux` 等）。

**两步交互：** 搜索 → 选序号（`1`、`1,3`、`a`，**回车**跳过）→ 选操作 **1**–**4**。短关键词如 `draw` 常出现 **三条**（darwin / linux / windows，同一 `id`）；选对平台，或用 `--platform windows drawio` 缩小范围。

```text
lookup_app.bat draw
> 3          # 选 windows 行
> 1          # 立刻下载（不改 enabled）
```

脚本会列出匹配项的 **平台**、**分片路径**、**分类**、当前 **enabled** 状态。交互流程：**选序号** → **选操作**：

| 操作 | 说明 |
|------|------|
| **1** | 立刻下载（**不**改 `enabled`） |
| **2** | 加入更新列表 **并** 立刻下载 |
| **3** | 仅加入更新列表（`saved_apps_<平台>.json`） |
| **4** | 设为 `enabled=true` |

常用选项：

| 选项 | 说明 |
|------|------|
| `--platform windows\|darwin\|linux` | 只显示该平台匹配项 |
| `--save [文件]` | 选中项加入更新列表（默认 `saved_apps_<平台>.json`） |
| `--no-save-prompt` | 不询问是否加入列表 |
| `--no-prompt` | 只查询，不交互 |
| `--yes` / `-y` | 对全部匹配项直接 `enabled=true`（常与 `--save` 联用） |
| `--download` / `-d` | 交互时默认 **1** 立刻下载；与 `-y` 联用则对全部匹配项立刻下载 |
| `--dry-run` | 预览，不写盘 |
| `--apps-dir VibeCodingToolsDown` | 检索另一套清单（与主 `apps/` 分离） |
| `--min-score N` | 调低/调高模糊匹配阈值（默认 40） |

交互时：`1` 或 `1,3` 选序号，`a` 选全部，**回车** 跳过。

### 方式 A″：游戏频道搜索（gamer520）

在 **gamer520.com** 已抓取标题中搜索并打开浏览器；**本地无匹配时自动改用站内搜索**（`?s=关键词`，PC/Switch 混排，需联网）。**不提供**自动下载；开源工具用 `lookup_app`，工具介绍页用 `search_soft_pages`。

```bat
search_games.bat
search_games.bat 艾尔登
search_games.bat 卡比
search_games.bat --open 黑神话
search_games.bat --stats
```

本地索引来自首页近期列表（`refresh_urls.bat gamer520` 默认 **50 页**，约千条，适合搜新上架）。较旧条目（如部分「星之卡比」）可能不在本地索引中，会走站内搜索；来源显示为 `gamer520 · 游戏（站内搜索）`。刷新 URL 清单：`tools\soft_page_check\refresh_urls.bat gamer520`。标题快检：`monthly_check_site.bat gamer520`（首次需连跑两次建基线）。

### 方式 A′：介绍页标题搜索（非 GitHub 清单）

在 **dayanzai / down66 / 7xiazai** 等已抓取标题中搜索并打开浏览器（见 [`tools/soft_page_check/`](tools/soft_page_check/)）。**无参数**双击或运行 `search_soft_pages.bat` 会提示输入关键词（行为同 `lookup_app.bat`）。

```bat
search_soft_pages.bat
search_soft_pages.bat 7zip
search_soft_pages.bat dayanzai WindowTabs
search_soft_pages.bat --open github copilot
```

| 选项 | 说明 |
|------|------|
| `--scope dayanzai` / `a` / `hybase_system` 等 | 限定来源 |
| `--open` | 不交互，直接打开前几条匹配 |
| `--stats` | 显示索引条数与各来源规模 |

### 闭环：查询 → 列表 → 本机更新

```bat
REM 1. 搜索并加入列表（可多跑几次，列表会合并去重）
lookup_app.bat --platform windows cherrytree

REM 2. 一键按列表开启 enabled 并下载/更新
run_saved_apps.bat
```

列表文件默认在仓库根 **`saved_apps_windows.json`**（macOS/Linux 为 `saved_apps_darwin.json` / `saved_apps_linux.json`）。可改名或放子目录：

```bat
lookup_app.bat --save lists\my.json joplin
run_saved_apps.bat lists\my.json
set SAVED_APPS_LIST=lists\my.json
run_saved_apps.bat
```

大眼仔旭批量收录（仅 Windows 清单源）：`python tools/import_dayanzai_windows.py --apply`；同步到 darwin/linux：`python tools/sync_dayanzai_to_darwin_linux.py`。

### 方式 B：手改 JSON

在 [`apps/windows/`](apps/windows/)（或对应平台的 JSON）中打开包含该应用的分片文件，将：

```json
"enabled": false
```

改为：

```json
"enabled": true
```

全局选项（如下载目录、SSL 校验）在 [`apps/root.json`](apps/root.json) 中配置。

改完后运行：

```bash
python auto_update.py
```

### 查找范围说明（是否「包含所有」）

| 范围 | 是否检索 |
|------|----------|
| [`apps/windows/`](apps/windows/)、[`apps/darwin/`](apps/darwin/)、[`apps/linux/`](apps/linux/) 下所有 `*.json` 分片中的**每条应用** | **是**（与 `auto_update.py` 合并清单的范围一致） |
| 匹配字段 | `id`、`简介`、`分类`、`repo_path`、`releases_url`、`url_hint`（模糊、不区分大小写） |
| [`apps/root.json`](apps/root.json) | **否**（仅全局项，无应用条目） |
| [`GiteeExploreHot/`](GiteeExploreHot/)、[`VibeCodingToolsDown/`](VibeCodingToolsDown/) | **默认否**；后者可用 `--apps-dir VibeCodingToolsDown` |
| 根目录单文件 `apps.json`、各平台 `*.json.bak` | **否**（仅当某平台无分片目录且存在 `apps/<platform>.json` 单文件时，才会扫该单文件） |
| `dist/vibecoding/manifest.json` 等构建产物 | **否** |

同一 `id` 在三个平台各有一条时，检索会显示 **3 行**；开启时可只选 Windows 或 `a` 全开。

---

## 4. 只更新指定应用

只处理若干个 **已启用** 的应用：

```bash
python auto_update.py obsidian vscodium nodejs
```

若应用未启用，脚本会提示该 `id` 不存在或未启用。

---

## 5. 指定平台读取

即使当前不是该系统，也可强制读取某个平台块：

```bash
python auto_update.py --platform windows
python auto_update.py --platform darwin
python auto_update.py --platform linux
```

与指定 `id` 组合：

```bash
python auto_update.py nodejs --platform windows
```

---

## 6. HTTPS 证书问题

临时关闭证书校验：

```bash
python auto_update.py --insecure
```

或在 [`apps/root.json`](apps/root.json) 根级设置：

```json
"ssl_verify": false
```

注意：关闭证书校验有安全风险，证书恢复正常后建议改回 `true`。

---

## 7. 发布页镜像与自适应回退

脚本对发布页抓取采用自适应策略：

- 先访问应用条目里的 `releases_url`
- 若镜像返回 403、5xx 或不可访问，自动回退到 `https://github.com/<owner>/<repo>/releases`
- 若页面能打开但未解析到合适安装包，会继续尝试 GitHub API
- 若页面标题不是可靠版本号，会优先从发布链接中的 tag 提取版本
- 若页面版本与 API `latest` 不一致，会按页面识别到的 tag 请求对应版本的 API

可在 [`apps/root.json`](apps/root.json) 根级增加可选配置：

```json
"release_page_mirrors": [
  "https://github.com",
  "https://你的自建镜像域名"
]
```

脚本会按顺序尝试这些发布页来源（具体以 `auto_update.py` 实现为准）。

---

## 8. 下载目录与平台子目录

默认下载根目录由 [`apps/root.json`](apps/root.json) 中的 `download_dir` 控制（例如 `"."` 或 `"downloads"`）。

当根级 **`download_subdir_by_platform` 为 `true`**（本仓库默认开启）时，实际保存路径为：

`{download_dir}/{windows|darwin|linux}/…`

便于在同一台机器上交叉执行 `--platform windows` / `darwin` / `linux` 时，安装包按系统类型分文件夹存放。日志中会标注 **`[平台: …]`** 与完整目标路径。

大文件经公共下载镜像（如 `gh-proxy.com` 等）时可能较慢；控制台会显示 **百分比（含小数）与已下/总大小（MiB）**，避免长时间停在「0%」的错觉。直连 GitHub 的备用 URL 会按脚本逻辑依次尝试。

若希望所有平台文件仍落在同一目录，可在 [`apps/root.json`](apps/root.json) 中将 `download_subdir_by_platform` 设为 `false`。

---

## 9. apps 常用字段

每条应用至少需要：

- `id`
- `releases_url`
- `repo_path`

常见可选字段：

- `enabled`：是否参与批量处理
- `installer_markers`：在发布页里识别安装包链接的关键字
- `download_names`：兜底拼接下载地址时使用的文件名模板（`{ver}` 为去掉 `v` 的版本号）
- `download_url_templates`：自定义备用下载地址模板，支持 `{ver}`（保留 `v`）与 `{ver_plain}`（去掉 `v`）
- `save_name`：本地保存文件名模板
- `windows_installer`：Windows 安装包模式（与 `installer_extensions` 等配合）
- `installer_extensions`：如 `.exe`、`.msi`
- `process_name`：安装前要结束的进程名（Windows）
- `kill_before_install`：安装前是否先结束进程
- `run_installer`：是否下载完成后自动启动安装程序
- `url_hint`：页面兜底搜索时使用的关键字
- `href_exclude_substrings`：排除不需要的链接
- `installer_markers_match_all`：要求多个关键字同时命中
- `prefer_api_assets`：优先从 GitHub API 资产列表中选包（适合附件很多的仓库或 tag 无 `v` 前缀等场景）
- `version_tag_as_on_github`：`true` 时不强行给版本号加 `v`（适用于 tag 为 `0.11.7` 这类仓库）

更完整的字段说明见 [`apps/root.json`](apps/root.json) 内 `_说明` 对象（仅供人阅读，脚本不使用以下划线开头的键）。

**`apps/root.json` 根级（非单条应用）常用**：`download_dir`、`ssl_verify`、`download_subdir_by_platform`（`true` 时下载落在 `download_dir/<windows|darwin|linux>/`）、`release_page_mirrors` 等。

---

## 10. 当前需要注意

- 想 **立即稳定使用**，请优先启用 **已带完整匹配规则** 的条目（Windows 侧多数常用软件已配 `installer_markers` / `download_names` / `save_name` 等，但仍建议先对单个 `id` 试跑再批量定时）。
- 想让某条 **目录型/占位** 条目真正可自动下载，需补全 `installer_markers`、`download_names`、`save_name` 等。
- 部分条目下载结果为 **压缩包**（`run_installer: false`），脚本 **不会** 自动解压或安装。
- 个别条目（如 `nodejs`）含特殊逻辑：可能结合 `nodejs.org` 等官方地址，以脚本为准。
- **GitHub API 有未认证请求频率限制**；短时间对大量 `prefer_api_assets` 条目连跑可能触发 403，可隔段时间重试、配置网络代理，或为请求配置 GitHub 令牌（需自行在环境中使 `requests` 生效，本仓库不内置令牌逻辑）。
- 若某软件 **tag 与资产文件名规则不一致**（例如 tag 为 `release-1.x` 而包名为 `1.x`），可能无法仅靠 `{ver}` 模板拼对，需改配置或等脚本扩展；这类情况在 README 中无法穷举，以实际日志为准。

---

## 11. 常见命令

```bash
pip install -r requirements.txt
python auto_update.py
python auto_update.py nodejs
python auto_update.py --platform windows
python auto_update.py --insecure
```

查找应用（不写盘）：

```bat
lookup_app.bat drawio
python lookup_app.py --no-prompt v2ray
search_soft_pages.bat
search_soft_pages.bat --stats
search_soft_pages.bat 7zip
```

---

## 12. 日志与排错

- 运行日志：`update_log.txt`
- 各应用抓取到的发布页 HTML：`github_page_<platform>_<app_id>.html`（例如 `github_page_windows_obsidian.html`）
- 下载失败时优先检查：`releases_url` 是否可访问、是否已回退到官方页或 API、`installer_markers` / `download_names` / `download_url_templates` 是否仍与真实资产一致、网络与证书、是否命中 GitHub API 限流
- **`enabled`**：**批量** `python auto_update.py`（不带 id）只处理 `enabled: true`；**lookup 选 1/2** 或 **`auto_update.py <id>` 指定 id 时不要求 enabled**
- **`重复的 id`**：同一平台多个分片出现相同 `id` 时会报错；`auto_update --platform windows` 仅合并 **windows** 分片，其它平台的重复 id **不会挡住** 本次 Windows 下载。检查 `99-未匹配-windows分片.json` 是否与正式分片重复

---

## 13. 维护工具（可选）

### 日常使用

| 目的 | 命令 |
|------|------|
| GitHub 清单模糊查找 / 加入更新列表 | `lookup_app.bat <关键词>`（见 §3） |
| 介绍页标题搜索 / 打开链接 | **`search_soft_pages.bat`**（无参数可交互输入） |
| 游戏页标题搜索（gamer520） | **`search_games.bat`** |
| 按列表一键更新 | **`run_saved_apps.bat`** 或 `python tools/run_saved_apps.py` |
| Windows 无 Python 打包 exe | `powershell -File tools\build_exe.ps1` → 复制 `dist/exe/*.exe` 到仓库根 |
| 刷新推荐导读 Markdown | `python tools/generate_recommended_md.py` |
| 刷新 [`CATALOG.md`](CATALOG.md) | `python tools/generate_catalog_index.py` |
| 刷新 [`CATALOG.mobile.md`](CATALOG.mobile.md) | `python tools/generate_mobile_catalog_index.py` |

### enabled 与清单维护

- 将所有应用 JSON 中的 `enabled` 写回 `false`：项目根 **`reset_enabled_json.bat`** 或 `python tools/reset_enabled_json.py`（可加 `--dry-run` 预览；快照默认 `tools/last_enabled_before_reset.json`）
- 按快照恢复 `enabled`：项目根 **`apply_enabled_snapshot.bat`** 或 `python tools/apply_enabled_snapshot.py`
- 将 `apps/darwin.json`、`apps/linux.json` 按 windows 分片名拆到 `apps/darwin/`、`apps/linux/`：`python tools/split_darwin_linux_to_dirs.py`（会备份原单文件为 `*.json.bak`）
- 单文件与 `apps/` 目录的拆分与恢复说明见 [`apps/root.json`](apps/root.json) 内 `_说明`

### 批量扩充收录（幂等脚本，勿重复执行）

| 脚本 | 用途 |
|------|------|
| `tools/import_dayanzai_windows.py --apply` | 从大眼仔旭 Windows 专区抓取开源 GitHub 项 |
| `tools/split_dayanzai_unmatched.py` | 将 `99-未匹配` 分片拆到各分类 |
| `tools/sync_dayanzai_to_darwin_linux.py` | Windows 新条目同步到 darwin/linux |
| `tools/append_catalog_batch5.py` … `batch11.py` | AI IDE、截图/OCR、跨平台缺口等（见 [`CATALOG.md`](CATALOG.md)） |
| `tools/append_mobile_catalog_batch1.py` | 首批 Android APK + iOS App Store 占位（见 [`CATALOG.mobile.md`](CATALOG.mobile.md)） |
| `tools/append_mobile_catalog_batch2.py` | v2rayNG、SmsForwarder（Android） |
| `tools/append_mobile_catalog_batch3.py` | 按桌面 30 分类大补 Android（约 +65 条） |
| `tools/append_mobile_catalog_batch4.py` | NipaPlay-Reload、NextPlayer、mpv-android（Android） |
| `tools/append_mobile_catalog_batch5.py` | Android 薄分类大补 + iOS App Store 占位扩展 |
| `tools/append_mobile_catalog_batch6.py` | Android / iOS 尽量全覆盖（batch5 后再 +77） |
| `tools/append_catalog_batch2.py` ~ `batch4.py` | 历史批处理（跨平台常用软件） |

### 介绍页监控（soft_page_check）

详见 [`tools/soft_page_check/README.md`](tools/soft_page_check/README.md)。常用：`monthly_check.bat`、`monthly_check_site.bat`、`open_changed_site.bat`、`refresh_urls.bat`、`search_soft_pages.bat`（根目录）、`fetch_github_on_changes.bat`。
