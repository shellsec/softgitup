# GitHub 发行版拉取工具（GH Release Fetch）

**中文** · [English README](README.md)

| | |
|:---|:---|
| **英文名称** | **GH Release Fetch** |
| **中文名称** | **GitHub 发行版拉取工具** |
| **仓库地址** | [`shellsec/gh-release-fetch`](https://github.com/shellsec/gh-release-fetch) |
| **英文描述** | Cross-platform **JSON catalog + Python helper** to resolve versions from **GitHub Releases** (release pages and API), pick the right Windows/macOS/Linux asset, download it, and optionally run the installer. Mirrors are tried first where configured, with fallback to `github.com`. |
| **中文描述** | 基于 **GitHub Releases**（发布页与 API）的跨平台 **JSON 清单 + Python 脚本**：解析版本、匹配安装包/归档、下载并可选择启动安装程序；支持镜像优先与回退官方。 |

---

这是一个基于 **GitHub Releases**（及发布页 HTML / API）的按需下载、更新 Windows / macOS / Linux 安装包或归档的脚本仓库。

**曾用称呼**：GithubWinDownTools；现用 **GH Release Fetch / GitHub 发行版拉取工具** 以反映多平台配置与用途。

核心文件：

- `auto_update.py`：按配置抓取版本、下载文件、按需启动安装程序（优先读取 `apps/` 目录合并结果，否则使用单文件 `apps.json`）
- `apps/`：推荐布局——[`apps/root.json`](apps/root.json)（全局）+ [`apps/windows/*.json`](apps/windows/) + [`apps/darwin/*.json`](apps/darwin/) + [`apps/linux/*.json`](apps/linux/)（均按分类拆成多个数组文件，与 windows 命名风格一致）；若无分片目录则回退单文件 `apps/darwin.json`、`apps/linux.json`。历史单文件备份见 `apps.json.monolith.bak`；darwin/linux 由单文件迁出后的备份见 `apps/darwin.json.bak`、`apps/linux.json.bak`
- `run_update.bat`：Windows 下一键检查 Python、安装依赖并执行 `python auto_update.py`

### VibeCodingToolsDown（可选独立清单）

与主 [`apps/`](apps/) **完全分离** 的第二套配置，目录为 [`VibeCodingToolsDown/`](VibeCodingToolsDown/)：面向 AI 编程相关 IDE 等条目；各产品下载直链由 [`VibeCodingToolsDown/scripts/build_manifest.py`](VibeCodingToolsDown/scripts/build_manifest.py) 聚合写入 **`dist/vibecoding/manifest.json`**，[`auto_update.py`](auto_update.py) 通过条目中的 `resolve_via=github_pages_manifest` 与 [`VibeCodingToolsDown/root.json`](VibeCodingToolsDown/root.json) 里的 `vibecoding_manifest_url` 读取（支持本地相对路径或 **HTTPS**，例如 **`raw.githubusercontent.com`** 上的 manifest）。

- **Windows 一键**：[`VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat`](VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat)（在本目录内执行：装依赖 → 生成 manifest → 调用 `vibe_update.py`）
- **命令行**：`python auto_update.py --apps-dir VibeCodingToolsDown`；或在 [`VibeCodingToolsDown/`](VibeCodingToolsDown/) 下执行 `python vibe_update.py`（内部仍调用仓库根的 `auto_update.py`，仅固定 `--apps-dir`）
- **批量关闭/恢复 `enabled`**：[`VibeCodingToolsDown/tools/reset_enabled_json.bat`](VibeCodingToolsDown/tools/reset_enabled_json.bat) / [`apply_enabled_snapshot.bat`](VibeCodingToolsDown/tools/apply_enabled_snapshot.bat)（调用仓库根 `tools/*.py`，快照在 `VibeCodingToolsDown/tools/`，与主 `apps/` 互不覆盖）
- **GitHub Actions**：仓库根未内置 workflow 文件（HTTPS PAT 无 `workflow` 权限时无法推送）。将 [`VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml`](VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml) 复制为 `.github/workflows/vibecodingtoolsdown-pages.yml` 后，即可定时/手动构建 manifest、提交默认分支并推 **gh-pages**；细节见 [`VibeCodingToolsDown/README.md`](VibeCodingToolsDown/README.md)

### GiteeExploreHot（可选 Gitee 分类 + 下载）

与 [`apps/`](apps/)（面向 **GitHub Releases**）**独立**：[`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/) 按主题维护 `owner/repo`；[`GiteeExploreHot/scripts/fetch_explore_hot.py`](GiteeExploreHot/scripts/fetch_explore_hot.py) 生成 **`data/gitee_downloads.json`**（从 Gitee `releases/latest` 解析附件并归类 **windows / darwin / linux**），[`GiteeExploreHot/scripts/gitee_download.py`](GiteeExploreHot/scripts/gitee_download.py) 可按平台拉取到本包 `downloads/`。**Windows 一键**：[`GiteeExploreHot/run_sync_gitee.bat`](GiteeExploreHot/run_sync_gitee.bat)（可选参数 `windows` / `darwin` / `linux` 表示同步后再下载）。**未接入** `auto_update.py`。详见 [`GiteeExploreHot/README.md`](GiteeExploreHot/README.md)。

### 仓库现状与收录范围（约略）

合并配置后规模约为：**Windows 约 345 条**（[`apps/windows/`](apps/windows/) 下 **29** 个分类分片）、**darwin 约 215 条**、**linux 约 213 条**（[`apps/darwin/`](apps/darwin/)、[`apps/linux/`](apps/linux/) 与 Windows 同风格分片）。数量会随你增删 JSON 变化，以运行 `python auto_update.py` 时日志里「已从 apps/ 目录合并配置」为准。

收录以 **GitHub（及镜像）上可解析的 Releases 资产** 为主，涵盖编辑器、笔记、安全、云原生、可观测、下载、办公与设计等常见分类。**不包含**破解、盗版或绕过授权的软件分发；个别条目仅含基础字段时需自行补全规则后才能稳定自动下载。

---

## 解决什么问题（痛点）

日常装开源桌面工具时，常见摩擦包括：

- **Release 页信息杂**：同一版本下有 macOS / Linux / Windows、便携版、校验文件等，手动找对的 `.exe` / `.msi` / `.zip` 费时且容易下错架构。
- **版本不直观**：页面标题、API `latest`、预发布（pre-release）混在一起，**不清楚当前最新 tag 对应哪个安装包**。
- **网络不稳定**：直连 GitHub 慢或被拦；纯镜像站又可能 403、证书异常，需要 **可回退的拉取策略**。
- **工具一多就难维护**：编辑器、笔记、CLI、运行时各自去官网点一遍，**缺少一份可版本化、可筛选的「软件清单」**。

本仓库用 **统一 JSON 配置 + 脚本** 把「查版本 → 选对资产 → 下载 →（可选）启动安装」串起来，并针对上述情况做了 **镜像失败回退官方、HTML 与 API 互补、按 tag / 文件名规则过滤** 等处理（细节见下文「发布页镜像与自适应回退」及 `auto_update.py`）。

---

## 面向谁、适合做什么

- **关注开源桌面软件、希望定期跟上新版本** 的用户或运维：把常用项目在配置里 `enabled: true`，按需或 **定时**（Windows 任务计划程序、Linux/macOS `cron` 等）执行 `python auto_update.py`，减少手工刷 Releases。
- **需要明确「当前装的是哪一版」**：下载文件名由 `save_name` 等模板控制，通常带 **版本号**；运行日志写入 `update_log.txt`，并会保留 `github_page_<platform>_<id>.html` 便于核对发布页解析结果（平台为 `windows` / `darwin` / `linux`）。
- **不适合**：主要走应用商店、无公开 GitHub Release、或安装包命名毫无规律且无法写匹配规则的闭源软件（需另找分发方式）。

---

## 版本与更新：你需要关注什么

| 关注点 | 说明 |
|--------|------|
| **脚本每次会重新解析「当前最新」** | 以发布页与 GitHub API 为准；不是「增量同步整个仓库」，而是按配置拉取 **你启用条目** 对应的 **Release 资产**。GitHub API 的 `latest` 通常指向 **非草稿、非预发布** 的最新一条；若项目只发预发布，解析结果可能因仓库设置而异，需以实际日志与下载 URL 为准。 |
| **本地是否重复下载** | 若本地已有同版本、同名文件，行为以 `auto_update.py` 中下载逻辑为准；建议结合日志与保存文件名中的版本判断是否已更新。 |
| **配置也要随上游变** | 上游若改名安装包、改 tag 规则（例如去掉 `v` 前缀），可能需在对应 JSON 里调整 `installer_markers`、`download_names`、`version_tag_as_on_github`、`prefer_api_assets` 等字段。 |
| **条目质量参差** | 仓库里收录了大量 **目录型** 条目；**只有匹配规则写全的条目** 才适合无人值守定时跑，其余需自行补全或仅手工启用测试。 |

简言之：**脚本帮你盯「上游 Release 与资产链接」；你这边要盯「哪些应用启用、规则是否仍匹配、定时任务是否执行成功」**。

---

## 需求

使用前请确认满足下列条件。

### 运行环境与软件

| 项目 | 说明 |
|------|------|
| **操作系统** | 脚本可在 **Windows、macOS、Linux** 上运行；`run_update.bat` 仅适用于 Windows。 |
| **Python** | **3.6 及以上**（与 `run_update.bat` 提示一致）；建议使用当前仍受支持的 3.x 版本。 |
| **包管理** | 已安装 **pip**，可执行 `pip install -r requirements.txt`。 |

### Python 依赖（requirements.txt）

安装后包含但不限于：

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

- **只处理 `enabled: true` 的条目**；命令行指定 `id` 时，该条目也必须已启用，否则提示不存在或未启用。
- **数据源以 GitHub 为主**：适合在 Releases 上提供可识别安装包/归档的开源项目；**非 GitHub 分发**（如仅官网、应用商店）的闭源产品通常无法直接套用同一套规则。
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

---

## 12. 日志与排错

- 运行日志：`update_log.txt`
- 各应用抓取到的发布页 HTML：`github_page_<platform>_<app_id>.html`（例如 `github_page_windows_obsidian.html`）
- 下载失败时优先检查：`releases_url` 是否可访问、是否已回退到官方页或 API、`installer_markers` / `download_names` 是否仍与真实资产一致、网络与证书、条目是否已 `enabled: true`、是否命中 GitHub API 限流

---

## 13. 维护工具（可选）

- 将所有应用 JSON 中的 `enabled` 写回 `false`：在项目根执行 `python tools/reset_enabled_json.py`（可加 `--dry-run` 预览）
- 将 `apps/darwin.json`、`apps/linux.json` 按 windows 分片名拆到 `apps/darwin/`、`apps/linux/`：`python tools/split_darwin_linux_to_dirs.py`（会备份原单文件为 `*.json.bak`）
- 单文件与 `apps/` 目录的拆分与恢复说明见 [`apps/root.json`](apps/root.json) 内 `_说明`
