# GH Release Fetch

**English** · [中文 README](README.zh-CN.md)

| | |
|:---|:---|
| **Project name (EN)** | **GH Release Fetch** |
| **Project name (ZH)** | **GitHub 发行版拉取工具** |
| **Repository** | [`shellsec/gh-release-fetch`](https://github.com/shellsec/gh-release-fetch) |
| **Description (EN)** | Cross-platform **JSON catalog + Python helper** to resolve versions from **GitHub Releases** (release pages and API), pick the right Windows/macOS/Linux asset, download it, and optionally run the installer. Mirrors are tried first where configured, with fallback to `github.com`. |
| **Description (ZH)** | 基于 **GitHub Releases**（发布页与 API）的跨平台 **JSON 清单 + Python 脚本**：解析版本、匹配安装包/归档、下载并可选择启动安装程序；支持镜像优先与回退官方。 |

---

## Overview

This repository helps you maintain a **version-controlled list** of open-source (and other) apps that ship binaries on **GitHub Releases**, and automate **check → download → (optional) install** instead of clicking through noisy release pages.

**Core files**

- [`auto_update.py`](auto_update.py) — loads merged config from [`apps/`](apps/) (or legacy root [`apps.json`](apps.json)), resolves latest release, downloads assets, optionally launches installers.
- [`apps/`](apps/) — recommended layout: [`apps/root.json`](apps/root.json) + per-platform JSON shards under [`apps/windows/`](apps/windows/), [`apps/darwin/`](apps/darwin/), [`apps/linux/`](apps/linux/). Falls back to `apps/darwin.json` / `apps/linux.json` if shard dirs are empty. Monolith backup: `apps.json.monolith.bak`; optional backups after splitting: `apps/darwin.json.bak`, `apps/linux.json.bak`.
- [`run_update.bat`](run_update.bat) — Windows shortcut: checks Python, installs deps, runs `python auto_update.py`.

**Optional second catalog: [`VibeCodingToolsDown/`](VibeCodingToolsDown/)**

Separate from [`apps/`](apps/): AI-coding–oriented entries, `manifest.json` built by [`VibeCodingToolsDown/scripts/build_manifest.py`](VibeCodingToolsDown/scripts/build_manifest.py), consumed via `resolve_via=github_pages_manifest` and `vibecoding_manifest_url` in [`VibeCodingToolsDown/root.json`](VibeCodingToolsDown/root.json) (local path or HTTPS, e.g. raw GitHub). Windows: [`run_update_VibeCodingToolsDown.bat`](VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat). Reset/restore `enabled` for this catalog only: [`VibeCodingToolsDown/tools/reset_enabled_json.bat`](VibeCodingToolsDown/tools/reset_enabled_json.bat) / [`apply_enabled_snapshot.bat`](VibeCodingToolsDown/tools/apply_enabled_snapshot.bat) (snapshots under that folder’s `tools/`). CLI: `python auto_update.py --apps-dir VibeCodingToolsDown` or `python vibe_update.py` from that folder. CI: copy [`VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml`](VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml) to `.github/workflows/` when your token can modify workflows (needs `workflow` scope for HTTPS PAT). See [`VibeCodingToolsDown/README.md`](VibeCodingToolsDown/README.md).

**Optional Gitee bundle: [`GiteeExploreHot/`](GiteeExploreHot/)**

Categorized **Gitee** repos under [`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/); [`GiteeExploreHot/scripts/fetch_explore_hot.py`](GiteeExploreHot/scripts/fetch_explore_hot.py) writes `hot_repos.json` plus **`gitee_downloads.json`** (Windows/macOS/Linux URLs from `releases/latest` attachments). [`GiteeExploreHot/scripts/gitee_download.py`](GiteeExploreHot/scripts/gitee_download.py) pulls binaries into `GiteeExploreHot/downloads/…`. Windows one-shot: [`GiteeExploreHot/run_sync_gitee.bat`](GiteeExploreHot/run_sync_gitee.bat) (optional first arg `windows`, `darwin`, or `linux` to download after sync). Not wired into `auto_update.py` (GitHub-focused). See [`GiteeExploreHot/README.md`](GiteeExploreHot/README.md).

**Approximate catalog size** (changes when you edit JSON): **~345** Windows entries across **29** shard files; **~215** darwin and **~213** linux. Confirm with the log line *“已从 apps/ 目录合并配置”* when you run the script.

**Scope**: entries target assets discoverable from **GitHub (or mirrors)**. **No** cracked software, piracy, or license circumvention. Some rows are stubs until you add full `installer_markers` / `download_names` / `save_name` rules.

---

## Problems this solves

- Release pages mix **many assets** (OS, arch, portable, checksums); picking the right `.exe` / `.msi` / `.zip` is slow and error-prone.
- **Version vs “latest”** can disagree between page title, `latest` API, and pre-releases.
- **Networks** block or throttle GitHub; you want **mirror → official → API** style fallback.
- Many tools ⇒ you want a **single maintainable manifest** instead of ad-hoc bookmarks.

---

## Who it is for

- Users and admins who **refresh open-source desktop/CLI tools** from GitHub and want `enabled: true` + scheduled `python auto_update.py` (Task Scheduler, `cron`, etc.).
- Anyone who wants **filenames and logs** that reflect versions (`save_name`, `update_log.txt`, `github_page_<platform>_<id>.html`).
- **Not ideal** for apps only on app stores, closed-source without public GitHub assets, or releases with naming that cannot be matched by the JSON rules.

---

## Version semantics (what you should watch)

| Topic | Note |
|--------|------|
| **“Latest” each run** | The script re-resolves the current release from the page/API; it does not sync the whole GitHub repo. GitHub’s `latest` API usually skips **drafts** and **pre-releases**; behavior may differ if a project only ships prereleases. |
| **Re-download** | Whether an existing file is skipped depends on `auto_update.py`; use logs and expected filenames to see if a re-run fetched again. |
| **Upstream renames** | If tags or asset names change, update `installer_markers`, `download_names`, `version_tag_as_on_github`, `prefer_api_assets`, etc. |
| **Rule quality** | Only rows with complete matching rules are suitable for unattended schedules; stub rows need manual completion. |

---

## Requirements

### Environment

| Item | Detail |
|------|--------|
| **OS** | Script runs on **Windows, macOS, Linux**; `run_update.bat` is Windows-only. |
| **Python** | **3.6+** (same as `run_update.bat` message); prefer a supported 3.x release. |
| **pip** | Install dependencies with `pip install -r requirements.txt`. |

### Dependencies (`requirements.txt`)

- `requests` (≥2.25.0) — HTTP and GitHub API.
- `beautifulsoup4` (≥4.9.0) — parse GitHub release HTML.

### Network

| Item | Detail |
|------|--------|
| **GitHub** | Reach **`github.com`** and **`api.github.com`** (or get them via fallback). If `releases_url` uses a mirror (e.g. `bgithub.xyz`), the script can **fall back to official** release pages and then the **API**. |
| **TLS** | Use `--insecure` or root [`apps/root.json`](apps/root.json) `"ssl_verify": false` only when needed (MITM risk); revert when certificates are fixed. |

### Config layout

| Item | Detail |
|------|--------|
| **Recommended** | [`apps/root.json`](apps/root.json) plus shard arrays under [`apps/windows/`](apps/windows/), [`apps/darwin/`](apps/darwin/), [`apps/linux/`](apps/linux/) (**unique `id` per platform**). Use `python tools/split_darwin_linux_to_dirs.py` to migrate legacy single-file darwin/linux lists. |
| **Legacy** | Root [`apps.json`](apps.json) if `apps/root.json` is absent. |
| **Per app** | At minimum: `id`, `releases_url`, `repo_path`. |

### Preconditions

- Only **`enabled: true`** entries run; CLI-listed ids must also be enabled.
- **Data source** is primarily **GitHub Releases**; other distribution channels may not fit the same schema.

---

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Quick start

**Windows (double-click)**  
Run [`run_update.bat`](run_update.bat) — checks Python, installs requirements, runs `python auto_update.py`.

**CLI (any OS)**

```bash
python auto_update.py
```

Default behavior: detect platform, merge `apps/` into `platforms.*`, process **only enabled** apps, try `releases_url` then official GitHub and API, prefer **tag-derived** versions when the page is ambiguous.

---

## 3. Enable an app

In the relevant shard under [`apps/windows/`](apps/windows/) (or darwin/linux), set:

```json
"enabled": true
```

Global options live in [`apps/root.json`](apps/root.json).

---

## 4. Update specific apps (must be enabled)

```bash
python auto_update.py obsidian vscodium nodejs
```

---

## 5. Force a platform block

```bash
python auto_update.py --platform windows
python auto_update.py nodejs --platform windows
```

---

## 6. TLS issues

```bash
python auto_update.py --insecure
```

Or in [`apps/root.json`](apps/root.json): `"ssl_verify": false` (temporary).

---

## 7. Mirrors and fallback

Order of operations (see [`auto_update.py`](auto_update.py) for details): entry `releases_url` → on failure, `https://github.com/<owner>/<repo>/releases` → optional API. Optional root `release_page_mirrors` list for extra release-page hosts.

---

## 8. Download directory and per-platform folders

`download_dir` in [`apps/root.json`](apps/root.json) sets the root (e.g. `"."` or `"downloads"`).

If **`download_subdir_by_platform`** is `true` (default in this repo), files go under:

`{download_dir}/{windows|darwin|linux}/…`

Logs include **`[platform: …]`** and the resolved target directory. Large files via public proxies may be slow; the console shows **percent (with decimals) and MiB** to avoid a stuck “0%” display. Direct GitHub URLs are tried in the script’s mirror chain.

---

## 9. Common app JSON fields

Required: `id`, `releases_url`, `repo_path`.

Useful optional fields: `enabled`, `installer_markers`, `download_names`, `download_url_templates`, `save_name`, `windows_installer`, `installer_extensions`, `process_name`, `kill_before_install`, `run_installer`, `url_hint`, `href_exclude_substrings`, `installer_markers_match_all`, `prefer_api_assets`, `version_tag_as_on_github`.

Human-oriented field glossary: `_说明` inside [`apps/root.json`](apps/root.json) (keys starting with `_` are not consumed by the script).

Root keys: `download_dir`, `ssl_verify`, `download_subdir_by_platform`, `release_page_mirrors`, etc.

---

## 10. Caveats

- Prefer **fully specified rules** before enabling many apps for cron; smoke-test single `id` first.
- Archives with `run_installer: false` are **not** auto-extracted.
- Special cases (e.g. `nodejs`) may use extra official URLs — see script.
- **Unauthenticated GitHub API** rate limits can return 403; retry later, use a proxy, or wire a token into your environment for `requests` (not built into this repo).
- If **tag names and file names diverge** (e.g. `release-1.x` vs `1.x` in the asset), `{ver}` templates may need manual tuning.

---

## 11. Common commands

```bash
pip install -r requirements.txt
python auto_update.py
python auto_update.py nodejs
python auto_update.py --platform windows
python auto_update.py --insecure
```

---

## 12. Logs and troubleshooting

- Log file: `update_log.txt`
- Saved release HTML: `github_page_<platform>_<app_id>.html` (e.g. `github_page_windows_obsidian.html`)
- On failure: check `releases_url`, fallbacks, markers vs real asset names, TLS, `enabled`, API rate limits

---

## 13. Maintenance scripts

- Reset all `enabled` to `false`: `python tools/reset_enabled_json.py` (`--dry-run` to preview)
- Split legacy `apps/darwin.json` / `apps/linux.json` into shard dirs: `python tools/split_darwin_linux_to_dirs.py` (backs up `*.json.bak`)
- Monolith vs `apps/` notes: [`apps/root.json`](apps/root.json) → `_说明`

---

*Former working title: **GithubWinDownTools** — renamed for clarity now that darwin/linux catalogs are first-class.*
