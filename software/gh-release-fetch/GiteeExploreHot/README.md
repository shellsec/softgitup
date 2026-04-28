# GiteeExploreHot

在 **Gitee** 上维护一份**按分类**的仓库清单，同步 **Star 等元数据**，并从 **`releases/latest` 附件**解析出 **Windows / macOS / Linux** 下载链接，支持本目录脚本直接拉取二进制（需 API 可用或配置令牌）。

与仓库根 [`apps/`](../apps/)（面向 **GitHub Releases**）**相互独立**：此处专门处理 **Gitee API** 与 `gitee.com` 附件链。

## 目录说明

| 路径 | 作用 |
|------|------|
| [`catalog/`](catalog/) | 分类 JSON 分片（[`catalog/README.md`](catalog/README.md) 含字段说明） |
| [`root.json`](root.json) | 本包下载目录 `download_dir`、TLS 等 |
| [`scripts/fetch_explore_hot.py`](scripts/fetch_explore_hot.py) | 同步：`data/hot_repos.json` + **`data/gitee_downloads.json`** |
| [`scripts/gitee_download.py`](scripts/gitee_download.py) | 按 `--platform windows|darwin|linux` 从索引下载文件 |
| [`data/curated_paths.txt`](data/curated_paths.txt) | 可选：仅作 **追加** 仓库列表（「未分类」）；主清单请用 `catalog/` |

## 为何探索页 HTML 不直接爬

`https://gitee.com/explore` 等对脚本常返回 **405**，因此以 **Open API** + 自建 `catalog` 为主。

## Windows 一键（推荐）

在资源管理器中双击 **[`run_sync_gitee.bat`](run_sync_gitee.bat)**（或在 `GiteeExploreHot` 目录下运行）：

- 安装依赖（使用**仓库根** [`requirements.txt`](../requirements.txt)）
- 执行 `scripts/fetch_explore_hot.py` 生成 `data/hot_repos.json` 与 `data/gitee_downloads.json`

同步完成后**再按平台下载**（可选参数）：

```bat
run_sync_gitee.bat windows
run_sync_gitee.bat darwin
run_sync_gitee.bat linux
```

无参数则只做同步，不下载。

## 使用步骤

1. 编辑 [`catalog/*.json`](catalog/)：每条至少 `id`、`repo_path`。
2. 建议设置 **只读令牌**（降低 403 频控）：

```bash
set GITEE_ACCESS_TOKEN=你的token
```

3. 同步索引（可调间隔，默认 `0.45` 秒/请求）：

```bash
python GiteeExploreHot/scripts/fetch_explore_hot.py
python GiteeExploreHot/scripts/fetch_explore_hot.py --sleep 1.0
```

4. 查看 **`data/gitee_downloads.json`**：每个仓库的 `downloads.windows` / `darwin` / `linux`；若某平台为 `null`，说明 **latest Release 里没有匹配附件**（源码-only 或命名无法启发式识别），可在 catalog 里为该条加 `attachment_filter` 或接受仅「其它附件」列表 `other_assets`。

5. 下载（示例：所有条目的 Windows 附件 → `GiteeExploreHot/downloads/GiteeExploreHot/windows/<id>/`）：

```bash
python GiteeExploreHot/scripts/gitee_download.py --platform windows
```

仅某一个 `id`：

```bash
python GiteeExploreHot/scripts/gitee_download.py --platform windows --id nacos
```

## 依赖

与主仓库一致：`requests`；`--html-file` 解析需要 `beautifulsoup4`。
