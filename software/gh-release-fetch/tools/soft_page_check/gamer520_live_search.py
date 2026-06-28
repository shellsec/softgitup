#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""gamer520.com 站内 WordPress 搜索（本地 50 页索引未收录时的补充）。"""
from __future__ import annotations

import html as html_lib
import re
import ssl
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

BASE = "https://www.gamer520.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CTX = ssl.create_default_context()
ARTICLE_URL = re.compile(r"https://www\.gamer520\.com/\d+\.html", re.I)
LINK_PAT = re.compile(
    r"""href\s*=\s*['"]([^'"]+)['"][^>]*>([^<]{2,300})</a>""",
    re.I | re.S,
)


def _normalize_url(href: str) -> str | None:
    u = urljoin(BASE + "/", href.split("#")[0].strip())
    if ARTICLE_URL.fullmatch(u):
        return u
    return None


def _clean_title(raw: str) -> str:
    return html_lib.unescape(re.sub(r"\s+", " ", raw)).strip()


def search_live(query: str, limit: int = 30) -> list[dict]:
    q = (query or "").strip()
    if not q:
        return []
    url = f"{BASE}/?s={quote(q)}"
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=25, context=CTX) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    by_url: dict[str, str] = {}
    for href, raw_title in LINK_PAT.findall(body):
        norm = _normalize_url(href)
        if not norm:
            continue
        title = _clean_title(raw_title)
        if len(title) < 2:
            continue
        if title in ("免费", "登录", "注册", "Switch520-Gamer520"):
            continue
        prev = by_url.get(norm, "")
        if len(title) > len(prev):
            by_url[norm] = title

    if not by_url:
        for href in ARTICLE_URL.findall(body):
            by_url[href] = ""

    rows: list[dict] = []
    for u, title in by_url.items():
        rows.append(
            {
                "url": u,
                "title": title or u,
                "scope": "gamer520",
                "scope_label": "gamer520 · 游戏（站内搜索）",
                "domain": "gamer520",
                "software": [],
                "live_search": True,
            }
        )
    return rows[:limit]
