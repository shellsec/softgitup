# GH Release Fetch

## ☕ 请我喝可乐

开源不易，欢迎赞助支持：  
👉 [爱发电](https://ifdian.net/a/shellsec)

**English** · [中文 README](README.zh-CN.md)

| | |
|:---|:---|
| **Project name (EN)** | **GH Release Fetch** |
| **Project name (ZH)** | **GitHub 发行版拉取工具** |
| **Repository** | [`shellsec/gh-release-fetch`](https://github.com/shellsec/gh-release-fetch) |
| **Description (EN)** | **Search by name, download or update** — no hunting Release pages, version tags, or direct URLs. Curated JSON + scripts resolve the latest release, pick the right OS asset, download, and optionally install. Mirrors first, fallback to `github.com`. |
| **Description (ZH)** | **按名字搜索即可下载/更新**——不必翻 Release 页、不必记版本号或找直链；`lookup_app.bat` 搜软件名，脚本自动解析最新包并匹配安装文件。 |

### What you get

| You **don’t** have to | The tool does |
|------------------------|---------------|
| Browse GitHub Releases and pick x64/dmg/AppImage links | Resolve the **latest tag** and filter assets by rules in the catalog |
| Track “which version / which URL today” | Filenames usually include the **version** (`save_name` templates) |
| Maintain hundreds of download URLs yourself | **500+** pre-catalogued entries; **fuzzy search** by app name |

```bat
lookup_app.bat drawio
REM pick row → 1 download now (no enabled) → 2 save+download → 3 save only → 4 enable
```

**Limits:** Rules live in JSON (maintainer work). Some entries are placeholders. Non-GitHub distribution → **channel track** (`search_soft_pages.bat`).

### Copy to GitHub «About»

In the repo sidebar **About → ⚙**, paste:

**Description (Chinese)**

```
GitHub 发行版拉取工具：500+ 开源软件清单，搜名字即可下载/更新，无需自己翻 Release 页或找下载链接。脚本自动解析最新版本并匹配 Win/macOS/Linux 安装包，支持 lookup 一键下载与批量更新。
```

**Description (English)**

```
GH Release Fetch: 500+ app catalog — search by name, download/update without hunting Release pages or URLs. Auto-resolves latest assets for Windows/macOS/Linux. One-click lookup + batch updates.
```

**Website (optional)** `https://github.com/shellsec/gh-release-fetch#readme`

**Topics (suggested)** `github-releases` `windows` `macos` `linux` `download-manager` `open-source-software` `automation` `python` `software-catalog`

---

## Overview

This repository is for **“search by name → resolve latest package → download (optional install)”**. Maintainers encode “how to find the right asset on GitHub/CDN” in JSON; **end users don’t hunt Release pages or copy URLs**.

Under the hood it targets **GitHub Releases** (HTML + API) for Windows / macOS / Linux (optional Android APK download).

### Design: two tracks

| Track | When | In this repo |
|-------|------|----------------|
| **Git** | Open source with parseable GitHub/Gitee Releases | `apps/` + `lookup_app` → `run_saved_apps`; optional `GiteeExploreHot/`, `VibeCodingToolsDown/` |
| **Channels** | Intro pages, mirrors, vendor CDN, non-Release distribution | `tools/soft_page_check/` periodic title checks; `search_soft_pages.bat`; manual download after changes |

Open source on Git; everything else on monitored channels (scheduled checks). Do not force non-Git apps into `apps/`. Optional `tools/dayanzai_cache/` when running `import_dayanzai_windows.py` is local-only (gitignored) and safe to delete after import.

**Core files**

- [`auto_update.py`](auto_update.py) — loads merged config from [`apps/`](apps/) (or legacy root [`apps.json`](apps.json)), resolves latest release, downloads assets, optionally launches installers.
- [`apps/`](apps/) — recommended layout: [`apps/root.json`](apps/root.json) + per-platform JSON shards under [`apps/windows/`](apps/windows/), [`apps/darwin/`](apps/darwin/), [`apps/linux/`](apps/linux/). Falls back to `apps/darwin.json` / `apps/linux.json` if shard dirs are empty. Monolith backup: `apps.json.monolith.bak`; optional backups after splitting: `apps/darwin.json.bak`, `apps/linux.json.bak`.
- [`run_update.bat`](run_update.bat) — Windows shortcut: checks Python, installs deps, runs `python auto_update.py`.
- [`lookup_app.py`](lookup_app.py) / [`lookup_app.bat`](lookup_app.bat) — fuzzy search → pick row → **1 download / 2 save+download / 3 save list / 4 enable** (see **§3**).
- [`search_soft_pages.bat`](search_soft_pages.bat) — search **intro page titles** from [`tools/soft_page_check/`](tools/soft_page_check/) and open URLs; no-arg run prompts for keywords; complements GitHub catalog lookup.
- [`run_saved_apps.bat`](run_saved_apps.bat) — enable + run `auto_update.py` for all apps in that list.

### Recommended apps (Markdown guide)

Full catalog guides by platform:

| Platform | Chinese | English table | Scale |
|----------|---------|---------------|-------|
| Windows | [`RECOMMENDED.zh-CN.md`](RECOMMENDED.zh-CN.md) | [`RECOMMENDED.md`](RECOMMENDED.md) | 567 |
| macOS | [`RECOMMENDED.darwin.zh-CN.md`](RECOMMENDED.darwin.zh-CN.md) | [`RECOMMENDED.darwin.md`](RECOMMENDED.darwin.md) | 539 |
| Linux | [`RECOMMENDED.linux.zh-CN.md`](RECOMMENDED.linux.zh-CN.md) | [`RECOMMENDED.linux.md`](RECOMMENDED.linux.md) | 539 |

Regenerate all: `python tools/generate_recommended_md.py`. Stats: [`CATALOG.md`](CATALOG.md).

**Optional second catalog: [`VibeCodingToolsDown/`](VibeCodingToolsDown/)**

Separate from [`apps/`](apps/): AI-coding–oriented entries, `manifest.json` built by [`VibeCodingToolsDown/scripts/build_manifest.py`](VibeCodingToolsDown/scripts/build_manifest.py), consumed via `resolve_via=github_pages_manifest` and `vibecoding_manifest_url` in [`VibeCodingToolsDown/root.json`](VibeCodingToolsDown/root.json) (local path or HTTPS, e.g. raw GitHub). Windows: [`run_update_VibeCodingToolsDown.bat`](VibeCodingToolsDown/run_update_VibeCodingToolsDown.bat). Reset/restore `enabled` for this catalog only: [`VibeCodingToolsDown/tools/reset_enabled_json.bat`](VibeCodingToolsDown/tools/reset_enabled_json.bat) / [`apply_enabled_snapshot.bat`](VibeCodingToolsDown/tools/apply_enabled_snapshot.bat) (snapshots under that folder’s `tools/`). CLI: `python auto_update.py --apps-dir VibeCodingToolsDown` or `python vibe_update.py` from that folder. CI: copy [`VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml`](VibeCodingToolsDown/ci/vibecodingtoolsdown-pages.monorepo.example.yml) to `.github/workflows/` when your token can modify workflows (needs `workflow` scope for HTTPS PAT). See [`VibeCodingToolsDown/README.md`](VibeCodingToolsDown/README.md).

**Optional Gitee bundle: [`GiteeExploreHot/`](GiteeExploreHot/)**

Categorized **Gitee** repos under [`GiteeExploreHot/catalog/`](GiteeExploreHot/catalog/); [`GiteeExploreHot/scripts/fetch_explore_hot.py`](GiteeExploreHot/scripts/fetch_explore_hot.py) writes `hot_repos.json` plus **`gitee_downloads.json`** (Windows/macOS/Linux URLs from `releases/latest` attachments). [`GiteeExploreHot/scripts/gitee_download.py`](GiteeExploreHot/scripts/gitee_download.py) pulls binaries into `GiteeExploreHot/downloads/…`. Windows one-shot: [`GiteeExploreHot/run_sync_gitee.bat`](GiteeExploreHot/run_sync_gitee.bat) (optional first arg `windows`, `darwin`, or `linux` to download after sync). Not wired into `auto_update.py` (GitHub-focused). See [`GiteeExploreHot/README.md`](GiteeExploreHot/README.md).

**Optional intro-page monitor: [`tools/soft_page_check/`](tools/soft_page_check/)**

Separate from the GitHub **`apps/`** catalog: tracks **page titles** on dayanzai, down66, 7xiazai, hybase, 423down, **gamer520** (games), tier-A install pages, etc. Use repo-root **[`search_soft_pages.bat`](search_soft_pages.bat)** to search ~5500+ indexed URLs and open matches in the browser. **Games:** [`search_games.bat`](search_games.bat) (gamer520; local recent list + **live site search fallback**). **No arguments:** prompts for keywords (same as `lookup_app.bat`).

| Task | Entry |
|------|--------|
| Search titles / open URLs | **`search_soft_pages.bat`** or **`search_soft_pages.bat <keyword>`** (repo root) |
| Search game pages (gamer520) | **`search_games.bat`** or **`search_games.bat <keyword>`** |
| Monthly SOP | `tools\soft_page_check\monthly_sop.bat` |
| **Monthly · tier A** (~42 pages, ~15s) | `tools\soft_page_check\monthly_check.bat` |
| **Quarterly · all channels** (~2300+ pages, ~20–35 min; title diff only) | `tools\soft_page_check\monthly_check_full.bat` |
| Per-site check / open changed URLs | `monthly_check_site.bat <site>` / `open_changed_site.bat <site>` (`423down` `7xiazai` `hybase` `dayanzai` `down66` **`gamer520`**) |
| List four sites batch | `tools\soft_page_check\monthly_check_list.bat` (7xiazai + hybase + dayanzai + down66) |
| Refresh URL lists | `tools\soft_page_check\refresh_urls.bat` |
| Prune dated snapshots | `tools\soft_page_check\prune_artifacts.bat` |
| HTML report | `tools\soft_page_check\open_report.bat` |
| GitHub title change → Release fetch | `tools\soft_page_check\fetch_github_on_changes.bat` (read-only `apps/` + `auto_update.py`) |

**vs `lookup_app`:** GitHub Releases catalog vs intro-page titles. This repo often has **no** `Lastb_soft_version.txt`; checks reuse cached URL lists under `soft_page_check/`. SoftGitUp-style `generate_and_push.bat` / `software/` sync is optional; the main gh-release-fetch flow uses `run_saved_apps.bat`, etc. Run tier-A check **twice** on first use for a diff baseline. Details: [`tools/soft_page_check/README.md`](tools/soft_page_check/README.md).

**Approximate catalog size** (changes when you edit JSON): **567** Windows, **539** darwin, **539** linux entries across **30** shard files each (**excluding** `99-未匹配-windows分片.json` placeholders). See [`CATALOG.md`](CATALOG.md) for a per-shard table (`python tools/generate_catalog_index.py` to refresh). Confirm totals with the merge log line when you run the script.

Some AI IDE rows in main `apps/` use `resolve_via=github_pages_manifest` via `vibecoding_manifest_url` in [`apps/root.json`](apps/root.json) (default `./VibeCodingToolsDown/dist/vibecoding/manifest.json`). Refresh with `python VibeCodingToolsDown/scripts/build_manifest.py` before enabling those entries.

**Duplicate `id`**: within one platform, each `id` must appear once across all shards (including `99-*`); remove stale placeholders if `auto_update.py` reports duplicates.

Bulk extend from [dayanzai.me/windows](https://www.dayanzai.me/windows): `python tools/import_dayanzai_windows.py --apply` (Windows), then `python tools/sync_dayanzai_to_darwin_linux.py` for darwin/linux (API-first stubs; tune markers before enabling).

**Scope**: entries target assets discoverable from **GitHub (or mirrors)**. **No** cracked software, piracy, or license circumvention. Some rows are stubs until you add full `installer_markers` / `download_names` / `save_name` rules.

---

## Problems this solves

- Release pages mix **many assets**; users just want the **latest installer**, not to hunt links and tags manually.
- **Networks** block or throttle GitHub; you want **mirror → official → API** fallback.
- Many tools ⇒ a **searchable catalog** beats bookmarking every Release page.

The script handles **version resolution and asset matching**; you search by name or maintain a saved list.

---

## Who it is for

- **Install/update one app without opening GitHub:** `lookup_app.bat keyword` → **1 download now** (no `enabled` change).
- **A personal set updated on a schedule:** options **2/3** → `saved_apps_*.json` → `run_saved_apps.bat`.
- **Maintainers / cron:** curate JSON rules, set `enabled: true` for stable rows, run `auto_update.py` on a timer.
- **Not ideal:** app-store-only apps, assets that cannot be matched by rules (use **channel track** / manual).

---

## Versions: who cares about what

| Role | What to watch |
|------|----------------|
| **Casual user** (lookup) | Usually **no** manual URLs or version tracking — search → download |
| **Saved list user** | Which apps are in the list; whether batch update succeeded |
| **Maintainer / cron** | Whether rules still match upstream renames; which entries are `enabled` |

| Technical detail | Note |
|------------------|------|
| **“Latest” each run** | Re-resolved from page/API; `latest` usually skips drafts/prereleases. |
| **Re-download** | Depends on `auto_update.py`; check logs and filenames. |
| **Upstream renames** | Update JSON markers/templates (**maintainer**). |
| **Rule quality** | Complete rules only for unattended runs. |

---

## Requirements

### Environment

| Item | Detail |
|------|--------|
| **OS** | Script runs on **Windows, macOS, Linux**; `run_update.bat` is Windows-only. |
| **Python** | **3.6+** (same as `run_update.bat` message); prefer a supported 3.x release. On Windows you can use **exe** instead (below). |
| **pip** | `pip install -r requirements.txt` (skip if using exe only). |

### No Python (Windows · optional exe)

Pack **5 exe files** beside [`apps/`](apps/). Bats use **Python when installed**, otherwise **exe**. Double-clicking an exe also prompts for keywords when run with no args.

| exe | bat | Role |
|-----|-----|------|
| `lookup_app.exe` | [`lookup_app.bat`](lookup_app.bat) | Search → actions 1/2/3/4 |
| `run_saved_apps.exe` | [`run_saved_apps.bat`](run_saved_apps.bat) | Batch update from saved list |
| `search_soft_pages.exe` | [`search_soft_pages.bat`](search_soft_pages.bat) | Search intro-page titles |
| `search_games.exe` | [`search_games.bat`](search_games.bat) | Search gamer520 game pages (local index + live site fallback) |
| `auto_update.exe` | [`run_update.bat`](run_update.bat) / lookup download | Download engine |

Build (needs Python **once** on the build machine):

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_exe.ps1
```

Output: `dist/exe/` — copy all **5 exe** files to the repo root. Maintainer scripts still need Python.

**Windows Release zip** (exe + catalog + soft_page_check index, ready to unzip):

```bat
pack_windows_release.bat
```

Or:

```powershell
powershell -ExecutionPolicy Bypass -File tools\pack_windows_release.ps1 -Version 1.0.0
```

Output: `dist/release/gh-release-fetch-windows-<version>.zip`. Details: [`release/windows/PACKAGING.md`](release/windows/PACKAGING.md).

### Dependencies (`requirements.txt`)

When using the **Python path**, install:

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

- **Batch mode** (no ids on CLI) processes only **`enabled: true`** entries.
- **Explicit ids** (`lookup_app` option 1, or `auto_update.py drawio`) **do not require** `enabled=true`.
- **Data source** is primarily GitHub (some rows use CDN/manifest); other channels → **channel track**.

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

### Option A: lookup script (recommended)

```bat
lookup_app.bat drawio
```

```bash
python lookup_app.py drawio
```

**Quick reference** (matches the on-screen help when you run `lookup_app` with no arguments):

```text
Usage: lookup_app [options and keywords...]
Examples: lookup_app drawio
         lookup_app --platform android termux
After picking rows: 1=download now  2=save+download  3=save list  4=enable
Non-interactive:    lookup_app -y --download drawio
```

**No arguments:** `lookup_app.bat` prompts for a keyword (you can type `--platform android termux` on the same line).

**Two-step flow:** search → pick row (`1`, `1,3`, `a`, or **Enter** to skip) → pick action **1**–**4**. Short keywords like `draw` often match **three rows** (darwin / linux / windows with the same `id`); pick the right platform or narrow with `--platform windows drawio`.

```text
lookup_app.bat draw
> 3          # windows row
> 1          # download now (does not change enabled)
```

Lists **platform**, **shard path**, **category**, and **enabled**. Interactive flow: **pick rows** → **pick action**:

| Action | Meaning |
|--------|---------|
| **1** | Download now (**does not** change `enabled`) |
| **2** | Add to saved list **and** download |
| **3** | Add to saved list only |
| **4** | Set `enabled=true` |

| Flag | Meaning |
|------|---------|
| `--platform windows\|darwin\|linux` | Filter to one platform |
| `--save [FILE]` | Add selection to update list (default `saved_apps_<platform>.json`) |
| `--no-save-prompt` | Do not ask to add to list |
| `--no-prompt` | Search only |
| `--yes` / `-y` | Enable all matches |
| `--download` / `-d` | Default action **1**; with `-y`, download all matches |
| `--dry-run` | Preview only |
| `--apps-dir VibeCodingToolsDown` | Search the separate catalog |
| `--min-score N` | Match threshold (default 40) |

At the row prompt: index `1` or `1,3`, `a` for all, **Enter** to skip.

### Option A″: game channel search (gamer520)

Search **game intro pages** on gamer520.com and open URLs in the browser. **Falls back to live site search** (`?s=query`, PC/Switch mixed, requires network) when the local index has no match. Does **not** download files. Open-source tools → `lookup_app`; utility intro pages → `search_soft_pages`.

```bat
search_games.bat
search_games.bat 艾尔登
search_games.bat 卡比
search_games.bat --open 黑神话
search_games.bat --stats
```

The local index covers **recent homepage listings** (`refresh_urls.bat gamer520`, **50 pages** by default, ~1000 URLs). Older posts may only appear via live site search (source label: `gamer520 · 游戏（站内搜索）`). Title check: `monthly_check_site.bat gamer520` (run twice for baseline).

### Option A′: intro-page title search (not the GitHub catalog)

Search captured titles from download-site intro pages and open URLs. **No arguments:** `search_soft_pages.bat` prompts for keywords (like `lookup_app.bat`).

```bat
search_soft_pages.bat
search_soft_pages.bat 7zip
search_soft_pages.bat --scope dayanzai WindowTabs
search_soft_pages.bat --open github copilot
search_soft_pages.bat --stats
```

Flags: `--scope` (e.g. `dayanzai`, `a`), `--open` (open top matches without prompting), `--stats` (index size).

### Closed loop: search → list → update

```bat
lookup_app.bat --platform windows cherrytree
run_saved_apps.bat
```

Default list files: `saved_apps_windows.json` (or `_darwin` / `_linux`). Custom path:

```bat
lookup_app.bat --save lists\my.json joplin
run_saved_apps.bat lists\my.json
set SAVED_APPS_LIST=lists\my.json
run_saved_apps.bat
```

Bulk catalog from [dayanzai.me/windows](https://www.dayanzai.me/windows): `python tools/import_dayanzai_windows.py --apply`; sync to darwin/linux: `python tools/sync_dayanzai_to_darwin_linux.py`.

### Option B: edit JSON

In the relevant shard under [`apps/windows/`](apps/windows/) (or darwin/linux), set `"enabled": true`. Global options live in [`apps/root.json`](apps/root.json).

### What the lookup searches (scope)

| Scope | Included? |
|--------|-----------|
| Every app row in `apps/windows/`, `apps/darwin/`, `apps/linux/` `*.json` shards | **Yes** (same merge as `auto_update.py`) |
| Fields matched | `id`, `简介`, `分类`, `repo_path`, `releases_url`, `url_hint` (case-insensitive fuzzy) |
| [`apps/root.json`](apps/root.json) | **No** |
| [`GiteeExploreHot/`](GiteeExploreHot/), [`VibeCodingToolsDown/`](VibeCodingToolsDown/) | **No** by default; use `--apps-dir VibeCodingToolsDown` for the latter |
| Root `apps.json`, `*.json.bak` | **No** (falls back to `apps/<platform>.json` only if a platform has no shard directory) |
| Built manifests (e.g. `dist/vibecoding/manifest.json`) | **No** |

The same `id` on three platforms appears as **three lines**; you can enable one platform or all.

---

## 4. Update specific apps

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
lookup_app.bat drawio
python lookup_app.py --no-prompt v2ray
```bat
search_soft_pages.bat
search_soft_pages.bat --stats
search_soft_pages.bat 7zip
```

---

## 12. Logs and troubleshooting

- Log file: `update_log.txt`
- Saved release HTML: `github_page_<platform>_<app_id>.html` (e.g. `github_page_windows_obsidian.html`)
- On failure: check `releases_url`, fallbacks, markers / `download_url_templates` vs real asset names, TLS, API rate limits
- **`enabled`**: **batch** `auto_update.py` (no ids) only runs `enabled: true` rows; **lookup options 1/2** or **`auto_update.py <id>`** do **not** require `enabled`
- **Duplicate `id`**: same-platform duplicates fail merge; with `--platform windows` only **windows** shards load — duplicates on other platforms do not block that run. Remove stale rows from `99-未匹配-windows分片.json` if needed

---

## 13. Maintenance scripts

### Daily use

| Goal | Command |
|------|---------|
| Fuzzy search GitHub catalog / saved list | `lookup_app.bat <keyword>` (§3) |
| Search intro-page titles / open URLs | **`search_soft_pages.bat`** (no-arg interactive) |
| Search game pages (gamer520) | **`search_games.bat`** |
| Update from saved list | **`run_saved_apps.bat`** or `python tools/run_saved_apps.py` |
| Build Windows exe (no Python for daily use) | `powershell -File tools\build_exe.ps1` → copy `dist/exe/*.exe` to repo root |
| **Pack Release zip (one-click)** | **`pack_windows_release.bat`** or `tools\pack_windows_release.ps1` |
| Regenerate RECOMMENDED*.md | `python tools/generate_recommended_md.py` |
| Refresh [`CATALOG.md`](CATALOG.md) | `python tools/generate_catalog_index.py` |

### enabled & layout

- Reset all `enabled` to `false`: **`reset_enabled_json.bat`** at repo root, or `python tools/reset_enabled_json.py` (`--dry-run` to preview; snapshot defaults to `tools/last_enabled_before_reset.json`)
- Restore `enabled` from snapshot: **`apply_enabled_snapshot.bat`** or `python tools/apply_enabled_snapshot.py`
- Split legacy `apps/darwin.json` / `apps/linux.json` into shard dirs: `python tools/split_darwin_linux_to_dirs.py` (backs up `*.json.bak`)
- Monolith vs `apps/` notes: [`apps/root.json`](apps/root.json) → `_说明`

### Bulk catalog import (idempotent; do not re-run blindly)

| Script | Purpose |
|--------|---------|
| `tools/import_dayanzai_windows.py --apply` | Import open-source GitHub rows from dayanzai.me/windows |
| `tools/split_dayanzai_unmatched.py` | Move `99-未匹配` rows into category shards |
| `tools/sync_dayanzai_to_darwin_linux.py` | Mirror new Windows rows to darwin/linux |
| `tools/append_catalog_batch2.py` … `batch4.py` | Historical cross-platform batches |
| `tools/append_catalog_batch5.py` … `batch11.py` | AI IDE、截图/OCR、跨平台缺口等（见 [`CATALOG.md`](CATALOG.md)） |

### Intro-page monitoring

See [`tools/soft_page_check/README.md`](tools/soft_page_check/README.md). Common entry points: `monthly_check.bat`, `monthly_check_site.bat`, `open_changed_site.bat`, `refresh_urls.bat`, root `search_soft_pages.bat`, `fetch_github_on_changes.bat`.

---

*Former working title: **GithubWinDownTools** — renamed for clarity now that darwin/linux catalogs are first-class.*
