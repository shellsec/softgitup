# apps 软件清单索引

> 自动生成：运行 `python tools/generate_catalog_index.py` 刷新。生成时间：**2026-06-08 08:05 UTC**

主清单数据在 [`apps/`](apps/)（`windows` / `darwin` / `linux` 各 30 个分类分片）。本文件只做**概览与导航**，不替代 JSON 配置。

## 规模概览

| 平台 | 条目数 | 已启用 (`enabled: true`) | 分类分片 |
|------|--------|--------------------------|----------|
| windows | 516 | 0 | 30 |
| darwin | 384 | 0 | 30 |
| linux | 382 | 0 | 30 |

不含 `99-未匹配-windows分片.json`（占位/待归类条目）。精确数以运行 `python auto_update.py` 时日志「已从 apps/ 目录合并配置」为准。

## 分片一览（按文件名）

| 分片文件 | 分类 | Windows | Darwin | Linux |
|----------|------|---------|--------|-------|
| `01-AI.json` | AI | 31 | 29 | 30 |
| `02-下载.json` | 下载 | 16 | 16 | 16 |
| `03-写作.json` | 写作 | 8 | 5 | 5 |
| `04-办公.json` | 办公 | 10 | 6 | 6 |
| `05-办公与设计.json` | 办公与设计 | 3 | 1 | 1 |
| `06-命令行.json` | 命令行 | 22 | 18 | 18 |
| `07-备份.json` | 备份 | 4 | 3 | 3 |
| `08-多媒体.json` | 多媒体 | 33 | 25 | 25 |
| `09-多媒体与设计.json` | 多媒体与设计 | 16 | 14 | 14 |
| `10-安全.json` | 安全 | 45 | 25 | 25 |
| `11-工具.json` | 工具 | 16 | 11 | 11 |
| `12-开发.json` | 开发 | 60 | 37 | 37 |
| `13-效率.json` | 效率 | 20 | 13 | 12 |
| `14-游戏.json` | 游戏 | 30 | 18 | 18 |
| `15-笔记.json` | 笔记 | 23 | 19 | 19 |
| `16-系统.json` | 系统 | 35 | 22 | 22 |
| `17-终端.json` | 终端 | 12 | 10 | 10 |
| `18-网络.json` | 网络 | 21 | 16 | 18 |
| `19-网络与协作.json` | 网络与协作 | 4 | 4 | 4 |
| `20-网络与通讯.json` | 网络与通讯 | 6 | 5 | 5 |
| `21-远程与协作.json` | 远程与协作 | 5 | 3 | 3 |
| `22-音视频.json` | 音视频 | 7 | 7 | 7 |
| `23-数据库.json` | 数据库 | 12 | 8 | 8 |
| `24-云原生.json` | 云原生 | 18 | 10 | 10 |
| `25-可观测.json` | 可观测 | 7 | 8 | 8 |
| `26-编辑器.json` | 编辑器 | 21 | 14 | 14 |
| `27-金融与股票.json` | 金融与股票 | 5 | 5 | 4 |
| `28-加密货币.json` | 加密货币 | 9 | 13 | 11 |
| `29-局域网文件共享.json` | 局域网文件共享 | 10 | 10 | 10 |
| `30-代理与隧道.json` | 代理与隧道 | 7 | 9 | 8 |

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

- `tools/append_catalog_batch2.py`
- `tools/append_catalog_batch3.py`
- `tools/append_catalog_batch4.py`

