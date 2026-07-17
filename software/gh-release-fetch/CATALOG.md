# apps 软件清单索引

> 自动生成：运行 `python tools/generate_catalog_index.py` 刷新。生成时间：**2026-07-17 04:20 UTC**

主清单数据在 [`apps/`](apps/)（`windows` / `darwin` / `linux` 各 30 个分类分片）。本文件只做**概览与导航**，不替代 JSON 配置。

## 规模概览

| 平台 | 条目数 | 已启用 (`enabled: true`) | 分类分片 |
|------|--------|--------------------------|----------|
| windows | 742 | 0 | 30 |
| darwin | 653 | 0 | 30 |
| linux | 633 | 0 | 30 |

不含 `99-未匹配-windows分片.json`（占位/待归类条目）。精确数以运行 `python auto_update.py` 时日志「已从 apps/ 目录合并配置」为准。

## 分片一览（按文件名）

| 分片文件 | 分类 | Windows | Darwin | Linux |
|----------|------|---------|--------|-------|
| `01-AI.json` | AI | 54 | 58 | 53 |
| `02-下载.json` | 下载 | 20 | 20 | 20 |
| `03-写作.json` | 写作 | 13 | 14 | 14 |
| `04-办公.json` | 办公 | 11 | 8 | 9 |
| `05-办公与设计.json` | 办公与设计 | 5 | 5 | 5 |
| `06-命令行.json` | 命令行 | 28 | 30 | 29 |
| `07-备份.json` | 备份 | 6 | 8 | 8 |
| `08-多媒体.json` | 多媒体 | 46 | 36 | 35 |
| `09-多媒体与设计.json` | 多媒体与设计 | 16 | 16 | 16 |
| `10-安全.json` | 安全 | 51 | 44 | 45 |
| `11-工具.json` | 工具 | 35 | 15 | 14 |
| `12-开发.json` | 开发 | 69 | 54 | 53 |
| `13-效率.json` | 效率 | 45 | 43 | 28 |
| `14-游戏.json` | 游戏 | 31 | 28 | 30 |
| `15-笔记.json` | 笔记 | 28 | 27 | 27 |
| `16-系统.json` | 系统 | 64 | 39 | 38 |
| `17-终端.json` | 终端 | 17 | 15 | 15 |
| `18-网络.json` | 网络 | 29 | 24 | 26 |
| `19-网络与协作.json` | 网络与协作 | 5 | 5 | 5 |
| `20-网络与通讯.json` | 网络与通讯 | 11 | 7 | 7 |
| `21-远程与协作.json` | 远程与协作 | 15 | 9 | 9 |
| `22-音视频.json` | 音视频 | 9 | 9 | 9 |
| `23-数据库.json` | 数据库 | 18 | 12 | 12 |
| `24-云原生.json` | 云原生 | 23 | 24 | 23 |
| `25-可观测.json` | 可观测 | 11 | 11 | 11 |
| `26-编辑器.json` | 编辑器 | 39 | 33 | 33 |
| `27-金融与股票.json` | 金融与股票 | 8 | 10 | 11 |
| `28-加密货币.json` | 加密货币 | 9 | 16 | 17 |
| `29-局域网文件共享.json` | 局域网文件共享 | 13 | 13 | 13 |
| `30-代理与隧道.json` | 代理与隧道 | 13 | 20 | 18 |

## 常用操作

| 目的 | 命令 |
|------|------|
| 模糊查找应用、开启条目 | `lookup_app.bat <关键词>` 或 `python lookup_app.py <关键词>` |
| 批量下载已启用条目 | `python auto_update.py`（可选 `--platform windows\|darwin\|linux`） |
| 全部关闭 enabled | 根目录 `reset_enabled_json.bat` 或 `python tools/reset_enabled_json.py` |
| 字段说明与分类参考 | [`apps/root.json`](apps/root.json) 内 `_说明` |
| 刷新本索引 | `python tools/generate_catalog_index.py` |

## 其它清单（与 apps/ 独立）

| 目录 | 用途 |
|------|------|
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

