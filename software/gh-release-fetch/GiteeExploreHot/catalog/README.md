# catalog（Gitee 仓库分类清单）

本目录下每个 `*.json` 文件是一个 **JSON 数组**，与仓库根 [`apps/windows/`](../../apps/windows/) 分片类似：按主题拆文件，便于维护。

## 每条目字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 本工具内唯一标识（用于下载子目录名） |
| `repo_path` | 是 | Gitee 的 `owner/repo` |
| `简介` | 否 | 给人看的说明 |
| `分类` | 否 | 建议与文件名主题一致 |
| `attachment_filter` | 否 | 精细挑选附件时可用，见下 |

## attachment_filter（可选）

按平台指定子串规则（不填则对附件名做 **启发式** 归类：`.exe`/win → windows，`.dmg`/mac → darwin，`.deb`/linux 等 → linux）：

```json
"attachment_filter": {
  "windows": { "must_include": [".exe"], "must_not_include": ["arm64"] },
  "linux": { "must_include": [".tar.gz"], "must_not_include": ["windows"] }
}
```

同一平台多个附件命中时，取 **文件名排序后的第一个**。

## 同步与下载

在项目根执行：

```bash
python GiteeExploreHot/scripts/fetch_explore_hot.py
```

会生成 `data/hot_repos.json`（仓库元数据）和 **`data/gitee_downloads.json`**（含各平台下载 URL）。

再下载 Windows 附件示例：

```bash
python GiteeExploreHot/scripts/gitee_download.py --platform windows
```
