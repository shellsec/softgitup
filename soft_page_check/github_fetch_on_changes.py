"""soft_page_check 内：按快检 GitHub 变化引用 gh-release-fetch 下载 Release（不修改 gh-release-fetch 代码）。"""
from __future__ import annotations

import argparse
import json
import platform as py_platform
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORTS = HERE / "reports"
GH_ROOT = ROOT / "software" / "gh-release-fetch"

GITHUB_REPO_RE = re.compile(
    r"https?://(?:www\.)?github\.com/([^/]+)/([^/?#]+)",
    re.I,
)


def github_repo_key(url: str) -> str | None:
    m = GITHUB_REPO_RE.match(url.strip())
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    if owner.lower() in {"search", "topics", "orgs", "settings", "marketplace"}:
        return None
    return f"{owner}/{repo}".lower()


def load_url_meta() -> dict:
    path = HERE / "url_meta.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_diff(scope: str) -> dict | None:
    path = REPORTS / f"last_diff_{scope}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def changed_entries(scope: str, changed_txt: Path | None) -> list[dict]:
    diff = load_diff(scope)
    items: list[dict] = []
    seen: set[str] = set()

    if diff:
        for row in diff.get("title_changed", []):
            url = row.get("url", "").strip()
            if url and url not in seen:
                seen.add(url)
                items.append(row)

    if changed_txt and changed_txt.exists():
        meta = load_url_meta()
        for line in changed_txt.read_text(encoding="utf-8").splitlines():
            url = line.strip()
            if not url or url in seen:
                continue
            seen.add(url)
            info = meta.get(url, {})
            items.append(
                {
                    "url": url,
                    "software": info.get("software", []),
                    "domain": info.get("domain", ""),
                    "tier": info.get("tier", ""),
                }
            )
    return items


def detect_platform_key() -> str:
    sysname = py_platform.system().lower()
    if sysname.startswith("darwin") or sysname == "mac":
        return "darwin"
    if sysname.startswith("linux"):
        return "linux"
    return "windows"


def load_gh_apps(platform_key: str | None = None):
    """只读解析 software/gh-release-fetch/apps/<platform>/*.json（不依赖 auto_update.py）。"""
    if not GH_ROOT.is_dir():
        raise FileNotFoundError(f"缺少 gh-release-fetch 目录: {GH_ROOT}")
    platform = platform_key or detect_platform_key()
    apps_dir = GH_ROOT / "apps" / platform
    if not apps_dir.is_dir():
        raise FileNotFoundError(f"缺少应用配置目录: {apps_dir}")

    apps: list[dict] = []
    seen: set[str] = set()
    for path in sorted(apps_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue
        for item in data:
            if not isinstance(item, dict):
                continue
            aid = (item.get("id") or "").strip()
            if not aid or aid in seen:
                continue
            seen.add(aid)
            apps.append(item)
    return {"platform": platform}, apps, None


def resolve_auto_update_cmd() -> list[str]:
    """优先 Python 源码，否则用便携版 auto_update.exe。"""
    py_script = GH_ROOT / "auto_update.py"
    exe = GH_ROOT / "auto_update.exe"
    if py_script.is_file():
        return [sys.executable, str(py_script)]
    if exe.is_file():
        return [str(exe)]
    raise FileNotFoundError(
        f"未找到 auto_update.py 或 auto_update.exe（目录: {GH_ROOT}）"
    )


def download_cache_dir() -> Path:
    """与 apps/root.json 的 download_subdir_by_platform 一致：默认 gh-release-fetch/<platform>/。"""
    return GH_ROOT / detect_platform_key()


def clear_download_cache() -> Path:
    """删除上次下载目录内容（目录本身保留），避免旧包混入。"""
    import shutil

    cache = download_cache_dir()
    if cache.is_dir():
        removed = 0
        for child in cache.iterdir():
            if child.is_file() or child.is_symlink():
                child.unlink(missing_ok=True)
                removed += 1
            elif child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
                removed += 1
        print(f"[soft_page_check] 已清空上次下载: {cache}（{removed} 项）")
    else:
        cache.mkdir(parents=True, exist_ok=True)
        print(f"[soft_page_check] 下载目录: {cache}")
    return cache


def build_repo_index(apps: list[dict]) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for app in apps:
        repo = (app.get("repo_path") or "").strip().lower()
        if not repo:
            continue
        index.setdefault(repo, []).append(app)
    return index


def resolve_apps(entries: list[dict], repo_index: dict[str, list[dict]]) -> tuple[list[dict], list[str]]:
    picked: dict[str, dict] = {}
    unmatched_github: list[str] = []

    for entry in entries:
        url = entry.get("url", "")
        repo = github_repo_key(url)
        if not repo:
            continue
        apps = repo_index.get(repo, [])
        if not apps:
            unmatched_github.append(url)
            continue
        for app in apps:
            aid = app.get("id", "")
            if aid:
                picked[aid] = app

    return list(picked.values()), unmatched_github


def download_apps(apps: list[dict], dry_run: bool, *, clear_cache: bool = True) -> int:
    if not apps:
        return 0
    ids = [a["id"] for a in apps if a.get("id")]
    print(f"[soft_page_check] {'(dry-run) ' if dry_run else ''}GitHub Release 下载: {', '.join(ids)}")
    print("[soft_page_check] 模式: 只下载不运行安装（依赖 apps 里 run_installer=false）")
    if dry_run:
        return 0

    if clear_cache:
        clear_download_cache()

    try:
        base = resolve_auto_update_cmd()
    except FileNotFoundError as exc:
        print(f"[错误] {exc}")
        return 1

    cmd = [*base, *ids]
    print(f"[soft_page_check] 调用: {' '.join(cmd)}")
    print(f"[soft_page_check] 下载目录（不入库）: {download_cache_dir()}")
    completed = subprocess.run(cmd, cwd=str(GH_ROOT))
    return int(completed.returncode or 0)


def load_soft_map_ids() -> list[str]:
    path = HERE / "gh_soft_map.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    ids: list[str] = []
    for item in data.get("apps") or []:
        gid = (item.get("gh_id") or "").strip()
        if gid and gid not in ids:
            ids.append(gid)
    return ids


def run_soft_map(dry_run: bool) -> int:
    """按 gh_soft_map.json 下载 software/ 装机开源（不依赖本月标题变化）。"""
    want = set(load_soft_map_ids())
    if not want:
        print("[跳过] gh_soft_map.json 为空或不存在")
        return 0
    try:
        _, apps, _ = load_gh_apps()
    except FileNotFoundError as exc:
        print(f"[错误] {exc}")
        return 1

    by_id = {a.get("id", ""): a for a in apps if a.get("id")}
    matched = [by_id[i] for i in want if i in by_id]
    missing = sorted(want - set(by_id))
    if missing:
        print("[提示] 映射 id 在 gh-release-fetch 中不存在:")
        for mid in missing:
            print(f"  - {mid}")
    if not matched:
        print("[跳过] 无匹配应用")
        return 0

    enabled = [a for a in matched if a.get("enabled", True)]
    disabled = [a for a in matched if not a.get("enabled", True)]
    print(f"software/ 装机开源映射 {len(want)} → 可下载 {len(enabled)}")
    for app in matched:
        flag = "enabled" if app.get("enabled", True) else "disabled"
        print(f"  - {app['id']} ({app.get('repo_path')}) [{flag}]")
    if disabled:
        print()
        print("[提示] 未 enabled=true，跳过:")
        for app in disabled:
            print(f"  - {app['id']}")
    return download_apps(enabled, dry_run)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="soft_page_check：按快检 GitHub 变化下载 Release（引用 gh-release-fetch 配置）",
    )
    parser.add_argument("--scope", default="a", help="读取 reports/last_diff_<scope>.json（默认 a）")
    parser.add_argument(
        "--changed-txt",
        default="",
        help="额外读取变化 URL 列表（默认 scope=a 时用 changed_tier_a_urls.txt）",
    )
    parser.add_argument(
        "--soft-map",
        action="store_true",
        help="按 gh_soft_map.json 下载 software/ 装机开源（忽略本月标题变化）",
    )
    parser.add_argument("--dry-run", action="store_true", help="只列出将下载的 app id，不实际下载")
    args = parser.parse_args()

    if args.soft_map:
        return run_soft_map(args.dry_run)

    changed_txt = Path(args.changed_txt) if args.changed_txt else None
    if changed_txt is None and args.scope == "a":
        changed_txt = HERE / "changed_tier_a_urls.txt"

    entries = changed_entries(args.scope, changed_txt)
    github_entries = [e for e in entries if github_repo_key(e.get("url", ""))]
    if not entries:
        print(f"[跳过] 无标题变化（scope={args.scope}，请先跑 fetch_titles.py --scope {args.scope} --compare）")
        return 0
    if not github_entries:
        print(f"[跳过] 有 {len(entries)} 处变化，但无 github.com 链接（本工具仅处理 GitHub Release）")
        print("  423down / 7xiazai / list 四站仍请浏览器手工下载。")
        return 0

    try:
        _, apps, _ = load_gh_apps()
    except FileNotFoundError as exc:
        print(f"[错误] {exc}")
        return 1

    repo_index = build_repo_index(apps)
    matched, unmatched = resolve_apps(github_entries, repo_index)

    if unmatched:
        print("[提示] 以下 GitHub 页在 gh-release-fetch 配置中无 repo_path 匹配:")
        for url in unmatched:
            print(f"  - {url}")

    if not matched:
        print("[跳过] 无匹配的 GitHub Release 应用配置")
        return 0

    enabled = [a for a in matched if a.get("enabled", True)]
    disabled = [a for a in matched if not a.get("enabled", True)]

    print(f"GitHub 变化 {len(github_entries)} 条 -> 匹配 {len(matched)} 个应用")
    for app in matched:
        flag = "enabled" if app.get("enabled", True) else "disabled"
        print(f"  - {app['id']} ({app.get('repo_path')}) [{flag}]")

    if disabled:
        print()
        print("[提示] 以下应用配置存在但未 enabled=true，不会下载:")
        for app in disabled:
            print(f"  - {app['id']}")
        print("  请在 software/gh-release-fetch/apps/ 对应 JSON 里设 enabled=true 后重试")

    return download_apps(enabled, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
