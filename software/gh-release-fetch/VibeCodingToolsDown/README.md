# VibeCodingToolsDown（独立配置包）

与仓库根目录的 **`apps/`** 完全分离：只在使用 `--apps-dir VibeCodingToolsDown` 或运行本目录 **`vibe_update.py`** / **`run_update_VibeCodingToolsDown.bat`** 时生效。

## 获取 manifest 的两种方式（GitHub）

| 方式 | URL 形态 | 说明 |
|------|-----------|------|
| **默认分支上的文件** | `https://raw.githubusercontent.com/<用户>/<仓库>/main/VibeCodingToolsDown/dist/vibecoding/manifest.json` | 将 [`ci/vibecodingtoolsdown-pages.monorepo.example.yml`](ci/vibecodingtoolsdown-pages.monorepo.example.yml) 复制到仓库根 `.github/workflows/vibecodingtoolsdown-pages.yml` 并启用 Actions 后，由 CI 构建并 **git commit** manifest；断网机器把 `vibecoding_manifest_url` 改成该 raw 地址即可拉索引（安装包链接仍在 manifest 内、指向各厂商 CDN）。 |
| **gh-pages** | `https://<用户>.github.io/<仓库>/vibecoding/manifest.json` 或对应 raw | 同一 workflow 用 peaceiris 推送 **`dist/`**；需在仓库 Settings → Pages 启用 `gh-pages` 分支。 |

本地开发：`root.json` 里 `vibecoding_manifest_url` 使用 `./dist/vibecoding/manifest.json`（相对本目录）。

## 目录与入口

| 路径 | 作用 |
|------|------|
| `root.json` | 全局项、`vibecoding_manifest_url`、`download_dir` 等 |
| `windows/`、`darwin/`、`linux/` | 平台分片（`resolve_via=github_pages_manifest`） |
| `scripts/build_manifest.py` | 聚合直链 → `dist/vibecoding/manifest.json` |
| `vibe_update.py` | 调用上级或本目录内的 `auto_update.py --apps-dir <本目录>` |
| `run_update_VibeCodingToolsDown.bat` | Windows：依赖 → 生成 manifest → 下载/安装 |
| `tools/reset_enabled_json.bat` | 仅重置本包各 JSON 里 `enabled`→`false`（快照写入 `tools/last_enabled_before_reset.json`，与主仓库 `apps/` 互不干扰） |
| `tools/apply_enabled_snapshot.bat` | 按上述快照把对应条目改回 `enabled: true` |
| `ci/vibecodingtoolsdown-pages.monorepo.example.yml` | 与本仓库同结构时：复制为根目录 `.github/workflows/vibecodingtoolsdown-pages.yml`（需有 `workflow` 权限的推送方式） |
| `ci/gh-pages-standalone-repo.example.yml` | 若本包**单独**成 GitHub 仓库时，复制到 `.github/workflows/` 并按注释改路径 |

重置逻辑与仓库根 [`tools/reset_enabled_json.py`](../tools/reset_enabled_json.py) 相同；bat 从仓库根调用该脚本并传入 `--apps-dir VibeCodingToolsDown`。若只拷贝本文件夹离线使用，请同时带上这两个 `tools/*.py`（或整份仓库的 `tools/`）。

## 与 `auto_update.py` 的关系

下载逻辑仍在仓库根的 **`auto_update.py`**（避免重复维护）。仅拷贝本文件夹时，把 **`auto_update.py`** 复制到本目录与 `vibe_update.py` 同级即可离线使用同一套逻辑。
