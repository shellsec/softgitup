"""soft_page_check 内：按快检 GitHub 变化引用 gh-release-fetch 下载 Release（不修改 gh-release-fetch 代码）。"""
from __future__ import annotations

import argparse
import json
import os
import re
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


def _import_gh_release_fetch():
    """只读引用 software/gh-release-fetch/auto_update.py，不在该目录写代码。"""
    if not GH_ROOT.is_dir():
        raise FileNotFoundError(f"缺少 gh-release-fetch 目录: {GH_ROOT}")
    gh_path = str(GH_ROOT)
    if gh_path not in sys.path:
        sys.path.insert(0, gh_path)
    import auto_update

    return auto_update


def load_gh_apps():
    auto_update = _import_gh_release_fetch()
    prev = os.getcwd()
    try:
        os.chdir(GH_ROOT)
        cfg = auto_update.load_config()
        platform = auto_update.detect_platform_key()
        apps = auto_update.apps_list_from_config(cfg, platform)
        return cfg, apps, auto_update
    finally:
        os.chdir(prev)


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


def download_apps(apps: list[dict], dry_run: bool) -> int:
    if not apps:
        return 0
    auto_update = _import_gh_release_fetch()
    ids = [a["id"] for a in apps]
    print(f"[soft_page_check] {'(dry-run) ' if dry_run else ''}GitHub Release 下载: {', '.join(ids)}")
    if dry_run:
        return 0

    prev = os.getcwd()
    os.chdir(GH_ROOT)
    try:
        cfg = auto_update.load_config()
        platform = auto_update.detect_platform_key()
        download_root = auto_update.resolve_download_root(cfg)
        verify = auto_update.resolve_tls_verify(cfg, False)
        auto_update.configure_insecure_requests(verify)
        auto_update.probe_network(cfg, verify=verify)

        exit_code = 0
        for app in apps:
            missing = [k for k in ("id", "releases_url", "repo_path") if k not in app]
            if missing:
                print(f"[错误] 应用配置缺少字段 {missing}: {app.get('id')}")
                exit_code = 1
                continue
            try:
                auto_update.update_one(
                    app,
                    download_root,
                    verify=verify,
                    platform_key=platform,
                    cfg=cfg,
                )
            except Exception as exc:
                print(f"[错误] [{app.get('id')}] {exc}")
                exit_code = 1
        return exit_code
    finally:
        os.chdir(prev)


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
    parser.add_argument("--dry-run", action="store_true", help="只列出将下载的 app id，不实际下载")
    args = parser.parse_args()

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
