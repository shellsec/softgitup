#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 gamer520.com 首页分页抓取近期文章 URL（默认 50 页，月检/refresh 用）。"""
from __future__ import annotations

import argparse
import html as html_lib
import re
import ssl
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
OUT = HERE / "list" / "gamer520_urls.txt"
OUT_LIST = HERE / "list" / "gamer520_list.txt"

BASE = "https://www.gamer520.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT = 25
HREF_PAT = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)
ARTICLE_PAT = re.compile(r"^/\d+\.html$")
LINK_TITLE_PAT = re.compile(
    r"""href\s*=\s*['"]([^'"]+)['"][^>]*>([^<]{2,300})</a>""",
    re.I | re.S,
)
CTX = ssl.create_default_context()
PAGE_SLEEP = 0.6

SKIP_PATH_PREFIX = (
    "/wp-",
    "/page/",
    "/tag/",
    "/category/",
    "/author/",
    "/xgq",
    "/ign-hot",
    "/hypervisor",
    "/user/",
)


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
        return resp.read().decode("utf-8", errors="replace")


def listing_url(page: int) -> str:
    if page <= 1:
        return f"{BASE}/"
    return f"{BASE}/page/{page}/"


def normalize_article_url(href: str) -> str | None:
    u = urljoin(BASE + "/", href.split("#")[0].strip())
    parsed = urlparse(u)
    if parsed.netloc.lower() not in ("www.gamer520.com", "gamer520.com"):
        return None
    path = parsed.path or ""
    if not ARTICLE_PAT.match(path):
        return None
    if any(path.startswith(p) for p in SKIP_PATH_PREFIX):
        return None
    return f"https://www.gamer520.com{path}"


def clean_title(raw: str) -> str:
    t = html_lib.unescape(re.sub(r"\s+", " ", raw)).strip()
    t = re.sub(r"^(免费|VIP|登录|注册)\s*", "", t)
    return t.strip()


def extract_from_listing(html: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for href, raw_title in LINK_TITLE_PAT.findall(html):
        url = normalize_article_url(href)
        if not url:
            continue
        title = clean_title(raw_title)
        if len(title) < 2 or title in ("免费", "登录", "注册"):
            continue
        prev = found.get(url, "")
        if len(title) > len(prev):
            found[url] = title
    if found:
        return found
    for href in HREF_PAT.findall(html):
        url = normalize_article_url(href)
        if url:
            found.setdefault(url, "")
    return found


def crawl(pages: int) -> dict[str, str]:
    found: dict[str, str] = {}
    for page in range(1, max(1, pages) + 1):
        url = listing_url(page)
        try:
            html = fetch(url)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            print(f"  [warn] {url} -> {exc}", file=sys.stderr)
            continue
        batch = extract_from_listing(html)
        new_urls = sum(1 for u in batch if u not in found)
        found.update(batch)
        titled = sum(1 for t in found.values() if t)
        print(f"  page {page}: +{new_urls} url (累计 {len(found)}, 有标题 {titled})")
        if page < pages:
            time.sleep(PAGE_SLEEP)
    return found


def main() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    ap = argparse.ArgumentParser(description="抓取 gamer520 近期文章 URL 清单")
    ap.add_argument("--pages", type=int, default=50, help="抓取首页分页数（默认 50，月检用）")
    args = ap.parse_args()

    print(f"抓取 {BASE} 前 {args.pages} 页 …")
    items = crawl(args.pages)
    urls = sorted(items.keys(), reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "# gamer520.com 近期文章（extract_gamer520_urls.py 生成）",
        f"# pages={args.pages} count={len(urls)}",
        "# 全量 sitemap 约 3 万条，日常仅用近期分页；标题见 gamer520_list.txt",
    ]
    OUT.write_text("\n".join(header + [""] + urls) + ("\n" if urls else ""), encoding="utf-8")
    list_lines = [f"{items[u] or '(列表页无标题)'}\t{u}" for u in urls]
    list_header = [
        "# title<TAB>url — search_games 搜索用（列表页标题，非逐页 fetch）",
        f"# pages={args.pages} count={len(list_lines)}",
    ]
    OUT_LIST.write_text(
        "\n".join(list_header + [""] + list_lines) + ("\n" if list_lines else ""),
        encoding="utf-8",
    )
    print(f"已写入 {len(urls)} 条 -> {OUT}")
    print(f"已写入 {len(list_lines)} 条 -> {OUT_LIST}")


if __name__ == "__main__":
    main()
