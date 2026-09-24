# apps 软件清单索引

> 自动生成：运行 `python tools/generate_catalog_index.py` 刷新。生成时间：**2026-09-22 06:14 UTC**

主清单数据在 [`apps/`](apps/)（`windows` / `darwin` / `linux` 各 30 个分类分片）。本文件只做**概览与导航**，不替代 JSON 配置。

## 规模概览

| 平台 | 条目数 | 已启用 (`enabled: true`) | 分类分片 |
|------|--------|--------------------------|----------|
| windows | 1018 | 0 | 30 |
| darwin | 963 | 0 | 30 |
| linux | 858 | 0 | 30 |

不含 `99-未匹配-windows分片.json`（占位/待归类条目）。精确数以运行 `python auto_update.py` 时日志「已从 apps/ 目录合并配置」为准。

## 分类展示页

本地用浏览器打开 [`catalog.html`](catalog.html) 即可按平台/分类浏览（支持搜索、区分可下载与仅官网）。快捷入口：根目录 `open_catalog.bat`。刷新：`python tools/generate_catalog_html.py`。

Markdown 全分类导读：[`RECOMMENDED.zh-CN.md`](RECOMMENDED.zh-CN.md)（Windows）/ [`RECOMMENDED.darwin.zh-CN.md`](RECOMMENDED.darwin.zh-CN.md) / [`RECOMMENDED.linux.zh-CN.md`](RECOMMENDED.linux.zh-CN.md)；刷新：`python tools/generate_recommended_md.py`。

## 分片一览（按文件名）

| 分片文件 | 分类 | Windows | Darwin | Linux |
|----------|------|---------|--------|-------|
| `01-AI.json` | AI | 151 | 153 | 144 |
| `02-下载.json` | 下载 | 26 | 27 | 25 |
| `03-写作.json` | 写作 | 18 | 20 | 19 |
| `04-办公.json` | 办公 | 18 | 17 | 16 |
| `05-办公与设计.json` | 办公与设计 | 8 | 8 | 7 |
| `06-命令行.json` | 命令行 | 29 | 30 | 29 |
| `07-备份.json` | 备份 | 13 | 15 | 11 |
| `08-多媒体.json` | 多媒体 | 51 | 40 | 40 |
| `09-多媒体与设计.json` | 多媒体与设计 | 16 | 16 | 16 |
| `10-安全.json` | 安全 | 51 | 45 | 45 |
| `11-工具.json` | 工具 | 43 | 34 | 16 |
| `12-开发.json` | 开发 | 79 | 62 | 61 |
| `13-效率.json` | 效率 | 59 | 61 | 39 |
| `14-游戏.json` | 游戏 | 37 | 34 | 34 |
| `15-笔记.json` | 笔记 | 33 | 33 | 32 |
| `16-系统.json` | 系统 | 76 | 52 | 41 |
| `17-终端.json` | 终端 | 20 | 20 | 20 |
| `18-网络.json` | 网络 | 38 | 34 | 33 |
| `19-网络与协作.json` | 网络与协作 | 6 | 6 | 6 |
| `20-网络与通讯.json` | 网络与通讯 | 24 | 29 | 16 |
| `21-远程与协作.json` | 远程与协作 | 30 | 25 | 23 |
| `22-音视频.json` | 音视频 | 35 | 36 | 25 |
| `23-数据库.json` | 数据库 | 20 | 15 | 15 |
| `24-云原生.json` | 云原生 | 25 | 26 | 25 |
| `25-可观测.json` | 可观测 | 13 | 13 | 13 |
| `26-编辑器.json` | 编辑器 | 45 | 41 | 38 |
| `27-金融与股票.json` | 金融与股票 | 11 | 14 | 13 |
| `28-加密货币.json` | 加密货币 | 9 | 16 | 17 |
| `29-局域网文件共享.json` | 局域网文件共享 | 17 | 18 | 17 |
| `30-代理与隧道.json` | 代理与隧道 | 17 | 23 | 22 |

## 常用操作

| 目的 | 命令 |
|------|------|
| 打开分类展示页 | 根目录 `open_catalog.bat` |
| 模糊查找应用、开启条目 | `lookup_app.bat <关键词>` 或 `python lookup_app.py <关键词>` |
| 搜 Android APK | `lookup_mobile.bat <关键词>` |
| 搜 iOS 商店占位 | `lookup_ios.bat <关键词>` |
| 批量下载已启用条目 | `python auto_update.py`（可选 `--platform windows\|darwin\|linux`） |
| 全部关闭 enabled | 根目录 `reset_enabled_json.bat` 或 `python tools/reset_enabled_json.py` |
| 字段说明与分类参考 | [`apps/root.json`](apps/root.json) 内 `_说明` |
| 刷新本索引 | `python tools/generate_catalog_index.py` |
| 刷新分类展示页 | `python tools/generate_catalog_html.py` → [`catalog.html`](catalog.html) |
| 刷新推荐导读 | `python tools/generate_recommended_md.py` |

## 其它清单（与 apps/ 独立）

| 目录 | 用途 |
|------|------|
| [`apps-mobile/`](apps-mobile/) | Android APK / iOS 占位；`lookup_mobile.bat` / `lookup_ios.bat` |
| [`VibeCodingToolsDown/`](VibeCodingToolsDown/) | AI 编程 IDE 等，manifest 由脚本生成 |
| [`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/) | Gitee 仓库分类与 Release 附件索引 |

## 批量维护脚本（追加条目，幂等）

- `tools/append_catalog_batch2.py` … `append_catalog_batch4.py` — 早期跨平台批
- `tools/append_catalog_batch5.py` — AI IDE 生态
- `tools/append_catalog_batch6.py` — AI 编程 / Copilot 类
- `tools/append_catalog_batch7.py` — 截图/贴图/OCR（Snipaste、OhMyShot 等）
- `tools/append_catalog_batch8.py` — SnapX/XerahS、系统/云原生/多媒体等
- `tools/append_catalog_batch9.py` — 跨平台缺口大补（命令行/安全/游戏等）
- `tools/append_catalog_batch10.py` — 安全 CLI、编辑器、备份、AI 等
- `tools/append_catalog_batch11.py` — Vault/Trivy/Terrascan 等
- `tools/append_catalog_batch19.py` — 装机必备闭源软件（仅打开官网）
- `tools/append_catalog_batch20.py` — 第二批必备官网（Office/网盘/JetBrains/娱乐等）

