#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 dayanzai.me/windows 抓取开源软件条目，解析 GitHub 仓库并追加到 apps/windows。

用法:
  python tools/import_dayanzai_windows.py --dry-run          # 仅统计
  python tools/import_dayanzai_windows.py --max-pages 5      # 试跑前 5 页
  python tools/import_dayanzai_windows.py                    # 全量（约 151 页）
  python tools/import_dayanzai_windows.py --apply            # 写入 JSON

筛选：标题/摘要/标签含「开源」或标签含 GitHub；正文含 github.com 链接。
无直链时尝试 GitHub Search API（需 GITHUB_TOKEN 环境变量，否则跳过）。
新条目默认写入 apps/windows/99-未匹配-windows分片.json。
缓存目录 tools/dayanzai_cache/ 仅加速重复抓取，已 .gitignore，日常 lookup/run_saved_apps 闭环不需要。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import quote

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
DATA_DIR = os.path.join(ROOT, "tools", "dayanzai_cache")
BASE = "https://www.dayanzai.me"
LIST_URL = f"{BASE}/windows"
TARGET_SHARD = "99-未匹配-windows分片.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; gh-release-fetch/1.0)"}

GH_RE = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
    re.I,
)
GH_SKIP_SUFFIX = {
    "releases", "issues", "pull", "blob", "tree", "wiki", "discussions",
    "actions", "settings", "security", "pulse", "graphs", "tags",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch(url: str, retries: int = 3, allow_fail: bool = False) -> str:
    last_err: Exception | None = None
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=45)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or "utf-8"
            return r.text
        except Exception as e:
            last_err = e
            if i < retries - 1:
                time.sleep(1.2 * (i + 1))
                print(f"  retry {url}: {e}", file=sys.stderr)
    if allow_fail:
        print(f"  skip {url}: {last_err}", file=sys.stderr)
        return ""
    raise last_err  # type: ignore[misc]


def max_page(html: str) -> int:
    nums = [int(x) for x in re.findall(r"/windows/page/(\d+)", html)]
    return max(nums) if nums else 1


def list_entries(html: str) -> list[dict]:
    entries = []
    for block in re.findall(
        r'<p class="r-top">.*?</p>\s*<p class="(?:other|desc)">.*?(?:</p>\s*<p class="tagls">|</p>\s*<a class="a-link")',
        html,
        re.S,
    ):
        m_title = re.search(
            r'<span class="name"><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>',
            block,
        )
        if not m_title:
            continue
        url, title = m_title.group(1), m_title.group(2).strip()
        tags = re.findall(r'rel="tag">([^<]+)<', block)
        desc_m = re.search(r'<p class="desc">([^<]+)', block)
        desc = (desc_m.group(1) if desc_m else "").replace("&hellip;", "…").strip()
        entries.append({"url": url, "title": title, "tags": tags, "desc": desc})
    return entries


def is_opensource_candidate(entry: dict) -> bool:
    blob = f"{entry['title']} {entry['desc']} {' '.join(entry['tags'])}"
    if "开源" in blob:
        return True
    if any(t.lower() == "github" for t in entry["tags"]):
        return True
    if "Github开源" in blob or "GPL" in blob or "MIT" in blob:
        return True
    return False


def extract_github_repos(html: str) -> list[str]:
    repos = []
    seen = set()
    for m in GH_RE.finditer(html):
        owner, repo = m.group(1), m.group(2)
        if repo.lower() in GH_SKIP_SUFFIX:
            continue
        key = f"{owner}/{repo}".lower()
        if key not in seen:
            seen.add(key)
            repos.append(f"{owner}/{repo}")
    return repos


def slug_to_id(slug: str) -> str:
    s = slug.replace(".html", "")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s[:64] or "unknown"


def app_name_from_title(title: str) -> str:
    # 去掉版本号、中文描述，取英文软件名
    t = re.sub(r"\s+\d+[\d.]*.*$", "", title)
    t = re.sub(r"^(开源|免费|专业|本地|轻量级|基于\s+\w+\s+的?)", "", t)
    m = re.search(r"([A-Za-z][A-Za-z0-9_.+\- ]{1,40})", t)
    return m.group(1).strip() if m else ""


def guess_repo_from_slug(slug: str) -> str | None:
    """无正文链接时，最多试探 2 个常见命名（避免 API 风暴）。"""
    base = slug.replace(".html", "").strip("-")
    if not base or len(base) < 2:
        return None
    parts = [p for p in re.split(r"[-_]+", base) if p]
    repo_name = "".join(p.capitalize() for p in parts) if parts else base.capitalize()
    owners = []
    if parts:
        owners.append(parts[0].capitalize())
    owners.append(repo_name)
    for owner in owners[:2]:
        try:
            r = requests.get(
                f"https://api.github.com/repos/{owner}/{repo_name}",
                timeout=12,
                headers={"Accept": "application/vnd.github+json"},
            )
            if r.status_code == 200 and r.json().get("full_name"):
                return r.json()["full_name"]
            if r.status_code == 403:
                return None
        except Exception:
            pass
        time.sleep(0.35)
    return None


def github_search_repo(name: str, token: str | None) -> str | None:
    if not name or not token:
        return None
    q = f"{name} in:name fork:false"
    url = f"https://api.github.com/search/repositories?q={quote(q)}&per_page=5"
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 403:
            return None
        r.raise_for_status()
        items = r.json().get("items") or []
        for it in items:
            full = it.get("full_name")
            if full and not it.get("archived"):
                return full
    except Exception:
        pass
    return None


def make_app_entry(
    repo_path: str,
    title: str,
    slug: str,
    source_url: str,
    existing_ids: set[str],
) -> dict:
    base_id = slug_to_id(slug)
    cand = base_id
    n = 2
    while cand.lower() in existing_ids:
        cand = f"{base_id}_{n}"
        n += 1
    existing_ids.add(cand.lower())

    short = title[:80] if len(title) > 80 else title
    return {
        "id": cand,
        "简介": f"{short}（来源：dayanzai）",
        "分类": "未匹配",
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "releases_url": f"https://bgithub.xyz/{repo_path}/releases",
        "repo_path": repo_path,
        "windows_installer": True,
        "installer_extensions": [".exe", ".msi"],
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
        "url_hint": cand,
    }


def load_catalog(platform: str = "windows") -> tuple[dict[str, dict], set[str], set[str]]:
    by_repo: dict[str, dict] = {}
    ids: set[str] = set()
    repos: set[str] = set()
    plat_dir = os.path.join(APPS, platform)
    for fn in os.listdir(plat_dir):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(plat_dir, fn)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if not isinstance(item, dict):
                continue
            iid = (item.get("id") or "").strip()
            rp = (item.get("repo_path") or "").strip()
            if iid:
                ids.add(iid.lower())
            if rp:
                repos.add(rp.lower())
                by_repo[rp.lower()] = item
    return by_repo, ids, repos


def list_cache_path(page: int) -> str:
    return os.path.join(DATA_DIR, "lists", f"page_{page}.html")


def crawl_list_pages(max_pages: int | None) -> list[dict]:
    html = fetch(LIST_URL)
    mp = max_page(html)
    limit = mp if max_pages is None else min(max_pages, mp)
    print(f"列表共 {mp} 页，将抓取 {limit} 页", flush=True)

    all_entries: list[dict] = []
    seen_url: set[str] = set()
    os.makedirs(os.path.join(DATA_DIR, "lists"), exist_ok=True)
    for p in range(1, limit + 1):
        cache = list_cache_path(p)
        if p == 1:
            page_html = html
            with open(cache, "w", encoding="utf-8") as f:
                f.write(page_html)
        else:
            if os.path.isfile(cache):
                with open(cache, encoding="utf-8", errors="replace") as f:
                    page_html = f.read()
            else:
                page_html = fetch(f"{LIST_URL}/page/{p}")
                with open(cache, "w", encoding="utf-8") as f:
                    f.write(page_html)
                time.sleep(0.25)
        for e in list_entries(page_html):
            if e["url"] not in seen_url:
                seen_url.add(e["url"])
                all_entries.append(e)
        if p % 10 == 0 or p == limit:
            print(f"  列表页 {p}/{limit}，累计 {len(all_entries)} 篇", flush=True)
    return all_entries


def article_cache_path(url: str) -> str:
    slug = url.rsplit("/", 1)[-1].replace(".html", "")
    return os.path.join(DATA_DIR, "articles", f"{slug}.html")


def fetch_article(url: str) -> str:
    cache = article_cache_path(url)
    if os.path.isfile(cache):
        with open(cache, encoding="utf-8", errors="replace") as f:
            return f.read()
    html = fetch(url, allow_fail=True)
    if not html:
        return ""
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w", encoding="utf-8") as f:
        f.write(html)
    time.sleep(0.2)
    return html


def resolve_repos_for_entry(entry: dict, token: str | None) -> list[str]:
    html = fetch_article(entry["url"])
    if not html:
        return []
    repos = extract_github_repos(html)
    if repos:
        return repos
    slug = entry["url"].rsplit("/", 1)[-1]
    if any(t.lower() == "github" for t in entry.get("tags") or []):
        found = guess_repo_from_slug(slug)
        if found:
            return [found]
    name = app_name_from_title(entry["title"]) or slug.replace(".html", "").replace("-", " ")
    found = github_search_repo(name, token)
    return [found] if found else []


def apply_entries(new_apps: list[dict]) -> int:
    path = os.path.join(APPS, "windows", TARGET_SHARD)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    seen = {(a.get("id") or "").strip().lower() for a in data if isinstance(a, dict)}
    seen_rp = {(a.get("repo_path") or "").strip().lower() for a in data if isinstance(a, dict)}
    added = 0
    for app in new_apps:
        aid = (app.get("id") or "").strip().lower()
        rp = (app.get("repo_path") or "").strip().lower()
        if not aid or aid in seen or rp in seen_rp:
            continue
        data.append(app)
        seen.add(aid)
        seen_rp.add(rp)
        added += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-pages", type=int, default=None)
    ap.add_argument("--max-articles", type=int, default=None, help="限制解析正文篇数（调试）")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    _, existing_ids, existing_repos = load_catalog("windows")

    entries = crawl_list_pages(args.max_pages)
    candidates = [e for e in entries if is_opensource_candidate(e)]
    print(f"全站条目 {len(entries)}，开源/GitHub 候选 {len(candidates)}", flush=True)

    if args.max_articles:
        candidates = candidates[: args.max_articles]

    new_apps: list[dict] = []
    skipped_existing = 0
    no_repo = 0

    for i, entry in enumerate(candidates, 1):
        if i % 20 == 0:
            print(f"  解析正文 {i}/{len(candidates)}…", flush=True)
        repos = resolve_repos_for_entry(entry, token)
        if not repos:
            no_repo += 1
            continue
        slug = entry["url"].rsplit("/", 1)[-1]
        for rp in repos:
            if rp.lower() in existing_repos:
                skipped_existing += 1
                continue
            app = make_app_entry(rp, entry["title"], slug, entry["url"], set(existing_ids))
            new_apps.append(app)
            existing_repos.add(rp.lower())

    # 去重 repo
    dedup: dict[str, dict] = {}
    for a in new_apps:
        dedup[a["repo_path"].lower()] = a
    new_apps = list(dedup.values())

    print(f"\n统计:")
    print(f"  候选文章: {len(candidates)}")
    print(f"  已收录跳过: {skipped_existing}")
    print(f"  无 GitHub 仓库: {no_repo}")
    print(f"  可新增: {len(new_apps)}")

    os.makedirs(DATA_DIR, exist_ok=True)
    report_path = os.path.join(DATA_DIR, "import_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_list": len(entries),
                "candidates": len(candidates),
                "new_count": len(new_apps),
                "new_apps": new_apps,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"报告已写: {report_path}")

    if args.apply and new_apps:
        n = apply_entries(new_apps)
        print(f"已写入 {n} 条到 apps/windows/{TARGET_SHARD}")
    elif args.apply:
        print("无新条目，未修改 JSON")
    elif not args.dry_run:
        print("未加 --apply，仅生成报告。确认后执行: python tools/import_dayanzai_windows.py --apply")


if __name__ == "__main__":
    main()
