#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
在 soft_page_check 已抓取的标题快照中搜索，并打开介绍页链接。

数据来源：history/titles_latest_*.json（fetch_titles.py 生成）
无快照时回退 soft_pages_urls.txt 与 list/*.txt（仅 URL，标题为空）。

用法：
  python tools/soft_page_check/search_pages.py 7zip
  python tools/soft_page_check/search_pages.py --open dayanzai 微信
  python tools/soft_page_check/search_pages.py --stats
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import webbrowser
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

if getattr(sys, "frozen", False):
    _REPO = Path(sys.executable).resolve().parent
else:
    _REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tools.ghrf_runtime import argv_from_prompt, soft_page_check_dir  # noqa: E402

HERE = Path(soft_page_check_dir(__file__))
HISTORY = HERE / "history"
LIST_DIR = HERE / "list"

sys.path.insert(0, str(HERE))
from list_scopes import LIST_SCOPE_DEFS, read_url_list, scope_label  # noqa: E402

SCOPE_LABELS = {
    "a": "A 类 · 同步软件",
    "all": "全量 · Lastb 装机页",
    "423down": "423down digest",
    "gamer520": "gamer520 · 游戏",
    "7xiazai": "7xiazai 列表",
}
for _scope in LIST_SCOPE_DEFS:
    SCOPE_LABELS[_scope] = scope_label(_scope)

FALLBACK_URL_FILES: list[tuple[str, Path]] = [
    ("all", HERE / "soft_pages_urls.txt"),
    ("a", HERE / "watch_tier_a_urls.txt"),
    ("gamer520", LIST_DIR / "gamer520_urls.txt"),
]


def _scope_from_snapshot(name: str) -> str:
    # titles_latest_DAYANZAI_SYSTEM.json -> dayanzai_system
    stem = name.replace("titles_latest_", "").replace(".json", "")
    return stem.lower()


def _load_snapshot(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    scope = _scope_from_snapshot(path.name)
    if scope == "all" and isinstance(data, dict) and "scope" in data:
        scope = str(data.get("scope") or scope).lower()
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return []
    out: list[dict] = []
    for row in entries:
        if not isinstance(row, dict):
            continue
        url = (row.get("url") or "").strip()
        if not url:
            continue
        out.append(
            {
                "url": url,
                "title": (row.get("title") or "").strip(),
                "tier": row.get("tier") or "",
                "software": row.get("software") or [],
                "domain": row.get("domain") or "",
                "scope": scope,
                "scope_label": SCOPE_LABELS.get(scope, scope),
            }
        )
    return out


def _load_url_file(scope: str, path: Path | str) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    label = SCOPE_LABELS.get(scope, scope)
    out: list[dict] = []
    for url in read_url_list(p):
        out.append(
            {
                "url": url,
                "title": "",
                "tier": "",
                "software": [],
                "domain": "",
                "scope": scope,
                "scope_label": label,
            }
        )
    return out


def _load_gamer520_list(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    label = SCOPE_LABELS.get("gamer520", "gamer520")
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            continue
        title, url = line.split("\t", 1)
        title = title.strip()
        url = url.strip()
        if not url.startswith("http"):
            continue
        rows.append(
            {
                "url": url,
                "title": title if title != "(列表页无标题)" else "",
                "scope": "gamer520",
                "scope_label": label,
            }
        )
    return rows


def build_index(scopes: frozenset[str] | None = None) -> list[dict]:
    by_url: dict[str, dict] = {}
    for snap in sorted(HISTORY.glob("titles_latest_*.json")):
        scope = _scope_from_snapshot(snap.name)
        if scopes and scope not in scopes:
            continue
        for row in _load_snapshot(snap):
            url = row["url"]
            prev = by_url.get(url)
            if prev is None or (not prev.get("title") and row.get("title")):
                by_url[url] = row
            elif prev and len(row.get("title") or "") > len(prev.get("title") or ""):
                by_url[url] = row

    for scope, path in FALLBACK_URL_FILES:
        if scopes and scope not in scopes:
            continue
        for row in _load_url_file(scope, path):
            if row["url"] not in by_url:
                by_url[row["url"]] = row
        if scope == "gamer520":
            for row in _load_gamer520_list(LIST_DIR / "gamer520_list.txt"):
                prev = by_url.get(row["url"])
                if prev is None or (not prev.get("title") and row.get("title")):
                    by_url[row["url"]] = row

    if scopes:
        for scope in scopes:
            if scope in LIST_SCOPE_DEFS:
                for row in _load_url_file(scope, LIST_SCOPE_DEFS[scope]["url_file"]):
                    if row["url"] not in by_url:
                        by_url[row["url"]] = row
    else:
        for scope, defn in LIST_SCOPE_DEFS.items():
            for row in _load_url_file(scope, defn["url_file"]):
                if row["url"] not in by_url:
                    by_url[row["url"]] = row

    return sorted(by_url.values(), key=lambda r: (r.get("title") or r["url"]).lower())


def _norm(s: str) -> str:
    return re.sub(r"[\s\-_]+", "", (s or "").lower())


def _haystack(row: dict) -> str:
    parts = [
        row.get("title") or "",
        row.get("url") or "",
        row.get("domain") or "",
        row.get("scope_label") or "",
        " ".join(row.get("software") or []),
    ]
    return " ".join(parts).lower()


def match_score(query: str, row: dict) -> int:
    q = query.strip().lower()
    if not q:
        return 0
    hay = _haystack(row)
    qn = _norm(q)
    hayn = _norm(hay)
    if q in hay or (qn and qn in hayn):
        score = 100
    else:
        tokens = [t for t in re.split(r"\s+", q) if t]
        if not tokens:
            return 0
        if not all(t in hay or _norm(t) in hayn for t in tokens):
            return 0
        score = 60 + 10 * len(tokens)
    title = (row.get("title") or "").lower()
    if q in title or _norm(q) in _norm(title):
        score += 40
    for sw in row.get("software") or []:
        if q in sw.lower() or _norm(q) in _norm(sw):
            score += 30
    url = (row.get("url") or "").lower()
    if q in url or _norm(q) in _norm(url):
        score += 20
    return score


def search(index: list[dict], queries: list[str], scope_filter: str = "") -> list[dict]:
    qs = [q.strip() for q in queries if q.strip()]
    if not qs:
        return []
    scored: list[tuple[int, dict]] = []
    sf = scope_filter.strip().lower()
    for row in index:
        if sf and sf not in (row.get("scope") or "").lower() and sf not in (row.get("scope_label") or "").lower():
            continue
        best = max(match_score(q, row) for q in qs)
        if best > 0:
            scored.append((best, row))
    scored.sort(key=lambda x: (-x[0], (x[1].get("title") or x[1]["url"]).lower()))
    return [r for _, r in scored]


def open_urls(rows: list[dict]) -> None:
    for row in rows:
        url = row["url"]
        print("打开:", url)
        webbrowser.open(url)


def print_stats(index: list[dict]) -> None:
    scopes: dict[str, int] = {}
    titled = 0
    for row in index:
        scopes[row.get("scope_label") or row.get("scope") or "?"] = scopes.get(row.get("scope_label") or "?", 0) + 1
        if row.get("title"):
            titled += 1
    print("soft_page_check 搜索索引：共 %d 条 URL，其中 %d 条有标题" % (len(index), titled))
    print("快照目录:", HISTORY)
    if not any(HISTORY.glob("titles_latest_*.json")):
        print("提示: 尚未运行 fetch_titles.py，多数条目仅 URL 可搜。")
        print("      可先运行 tools\\soft_page_check\\monthly_check.bat 建立标题基线。")
    print("\n按来源（约）：")
    for label, n in sorted(scopes.items(), key=lambda x: (-x[1], x[0])):
        print("  %-28s %5d" % (label, n))


def _gamer520_live_fallback(
    queries: list[str],
    scope_filter: str,
    index_scopes: frozenset[str] | None,
    limit: int,
) -> list[dict]:
    sf = (scope_filter or "").strip().lower()
    if sf and sf != "gamer520":
        return []
    if index_scopes is not None and "gamer520" not in index_scopes:
        return []
    try:
        from gamer520_live_search import search_live
    except ImportError:
        return []

    seen: set[str] = set()
    rows: list[dict] = []
    for q in queries:
        for row in search_live(q, limit=limit):
            if match_score(q, row) <= 0:
                continue
            u = row["url"]
            if u in seen:
                continue
            seen.add(u)
            rows.append(row)
    return rows


def pick_and_open(hits: list[dict], auto_open: bool) -> int:
    if not hits:
        print("无匹配。换关键词，或先运行 monthly_check / fetch_titles 建立标题快照。")
        return 1

    show = hits[:40]
    if len(hits) > len(show):
        print("（共 %d 条匹配，仅显示前 %d 条）" % (len(hits), len(show)))

    print("\n共 %d 条匹配：" % len(hits))
    print("-" * 72)
    for i, row in enumerate(show, 1):
        title = row.get("title") or "（无标题）"
        if len(title) > 56:
            title = title[:53] + "..."
        print("[%d] %s" % (i, title))
        print("     %s" % row["url"])
        print("     来源: %s" % (row.get("scope_label") or row.get("scope")))
        sw = row.get("software") or []
        if sw:
            print("     软件: %s" % ", ".join(sw[:5]))

    if auto_open:
        open_urls(show[: min(5, len(show))])
        return 0

    print("\n请选择要打开的页面：")
    print("  输入序号（1-%d）| 1,3,5 | a=全部显示项 | 回车=取消" % len(show))
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return 0

    if not choice:
        return 0
    if choice.lower() == "a":
        open_urls(show)
        return 0

    picked: list[dict] = []
    for part in re.split(r"[,，\s]+", choice):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            print("无效输入:", part)
            return 1
        idx = int(part)
        if idx < 1 or idx > len(show):
            print("序号超出范围:", idx)
            return 1
        picked.append(show[idx - 1])
    if picked:
        open_urls(picked)
    return 0


def run_search(
    *,
    default_scope: str = "",
    index_scopes: frozenset[str] | None = None,
) -> int:
    ap = argparse.ArgumentParser(description="在 soft_page_check 标题快照中搜索并打开链接")
    ap.add_argument("queries", nargs="*", help="搜索关键词（标题 / URL / 软件名）")
    ap.add_argument("--scope", default=default_scope, help="限定来源，如 dayanzai、a、gamer520")
    ap.add_argument("--open", action="store_true", help="不交互，直接打开前几条匹配")
    ap.add_argument("--stats", action="store_true", help="显示索引统计")
    ap.add_argument("--limit", type=int, default=40, help="最多显示条数")
    args = ap.parse_args()

    index = build_index(index_scopes)
    if args.stats:
        print_stats(index)
        if not args.queries:
            return 0

    if not args.queries and not args.stats:
        from tools.ghrf_runtime import prompt_cli_line

        text = prompt_cli_line([], "请输入搜索关键词: ")
        if not text:
            return 0
        import shlex

        args.queries = shlex.split(text, posix=(os.name != "nt"))
    if not args.queries and not args.stats:
        ap.print_help()
        print_stats(index)
        return 0

    hits = search(index, args.queries, args.scope)
    if not hits:
        live = _gamer520_live_fallback(
            args.queries,
            args.scope,
            index_scopes,
            args.limit,
        )
        if live:
            print(
                "本地近期首页列表无匹配，已改用 gamer520 站内搜索（PC/Switch 混排）。"
            )
            hits = live
    if args.limit and len(hits) > args.limit and not args.open:
        pass
    return pick_and_open(hits, args.open)


def main() -> int:
    if not argv_from_prompt(
        [
            "用法: search_soft_pages [选项与关键词...]",
            "示例: search_soft_pages 7zip",
            "      search_soft_pages --scope dayanzai 优化",
            "      search_soft_pages --stats",
            "",
            "搜索 soft_page_check 介绍页标题并打开链接（不自动下载）。",
            "GitHub 清单请用 lookup_app；游戏频道请用 search_games。",
        ],
        "请输入关键词（可含 --scope a 等）: ",
    ):
        return 0
    return run_search()


if __name__ == "__main__":
    raise SystemExit(main())
