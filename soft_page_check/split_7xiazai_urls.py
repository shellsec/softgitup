"""将 7xiazai 合并清单按标题拆成 system / mobile 两份 list 文件。"""
from __future__ import annotations

import json
import re
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
LIST = HERE / "list"
MERGED = HERE / "7xiazai_list_urls.txt"
MERGED_LIST = LIST / "7xiazai_list_urls.txt"
OUT_SYSTEM = LIST / "7xiazai_list_urls_system.txt"
OUT_MOBILE = LIST / "7xiazai_list_urls_mobile.txt"
LEGACY_SNAPSHOT = HERE / "history" / "titles_latest_7XIAZAI.json"

MOBILE_TITLE = re.compile(
    r"(?i)^android\b|^andriod\b|安卓|\[电视|\[盒子|/手机\]|tv版|车机版",
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
WORKERS = 8


def read_urls(path: Path) -> list[str]:
    if not path.exists():
        return []
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def load_title_map() -> dict[str, str]:
    titles: dict[str, str] = {}
    if LEGACY_SNAPSHOT.exists():
        data = json.loads(LEGACY_SNAPSHOT.read_text(encoding="utf-8"))
        for entry in data.get("entries", []):
            url = entry.get("url", "")
            if url and entry.get("title"):
                titles[url] = entry["title"]
    for scope in ("7XIAZAI_SYSTEM", "7XIAZAI_MOBILE"):
        snap = HERE / "history" / f"titles_latest_{scope}.json"
        if snap.exists():
            data = json.loads(snap.read_text(encoding="utf-8"))
            for entry in data.get("entries", []):
                url = entry.get("url", "")
                if url and entry.get("title"):
                    titles[url] = entry["title"]
    return titles


def fetch_title(url: str) -> str:
    from fetch_titles import fetch_title as _fetch

    return _fetch(url).get("title") or ""


def classify(title: str) -> str:
    return "mobile" if MOBILE_TITLE.search(title or "") else "system"


def write_list(path: Path, header: list[str], urls: list[str]) -> None:
    path.write_text("\n".join(header + [""] + urls) + "\n", encoding="utf-8")


def split_urls(urls: list[str], titles: dict[str, str]) -> tuple[list[str], list[str], int]:
    missing = [u for u in urls if u not in titles]
    if missing:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(fetch_title, url): url for url in missing}
            for fut in as_completed(futures):
                titles[futures[fut]] = fut.result()

    system: list[str] = []
    mobile: list[str] = []
    for url in urls:
        platform = classify(titles.get(url, ""))
        if platform == "mobile":
            mobile.append(url)
        else:
            system.append(url)
    return sorted(system), sorted(mobile), len(missing)


def seed_scope_snapshots(system_urls: list[str], mobile_urls: list[str]) -> None:
    if not LEGACY_SNAPSHOT.exists():
        return
    legacy = json.loads(LEGACY_SNAPSHOT.read_text(encoding="utf-8"))
    by_url = {e["url"]: e for e in legacy.get("entries", []) if e.get("url")}
    history = HERE / "history"
    history.mkdir(parents=True, exist_ok=True)

    for scope, urls in (("7xiazai_system", system_urls), ("7xiazai_mobile", mobile_urls)):
        upper = scope.upper()
        latest = history / f"titles_latest_{upper}.json"
        if latest.exists():
            continue
        entries = [by_url[u] for u in urls if u in by_url]
        if not entries:
            continue
        snap = {
            "fetched_at": legacy.get("fetched_at", ""),
            "scope": scope,
            "source": OUT_SYSTEM.name if scope.endswith("system") else OUT_MOBILE.name,
            "count": len(entries),
            "entries": sorted(entries, key=lambda x: x["url"]),
        }
        latest.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    merged_path = MERGED if MERGED.exists() else MERGED_LIST
    urls = read_urls(merged_path)
    if not urls:
        print(f"缺少合并清单: {merged_path.name}")
        return 1

    titles = load_title_map()
    system, mobile, fetched = split_urls(urls, titles)

    write_list(
        OUT_SYSTEM,
        [
            "# 7xiazai.com 软件页 · 系统（非 Android 标题）",
            f"# source: {merged_path.name}",
            f"# total: {len(system)}",
        ],
        system,
    )
    write_list(
        OUT_MOBILE,
        [
            "# 7xiazai.com 软件页 · 移动（标题含 Android/安卓/TV 等）",
            f"# source: {merged_path.name}",
            f"# total: {len(mobile)}",
        ],
        mobile,
    )
    MERGED_LIST.write_text(merged_path.read_text(encoding="utf-8"), encoding="utf-8")
    seed_scope_snapshots(system, mobile)

    print(f"7xiazai 拆分: 系统 {len(system)} -> {OUT_SYSTEM.relative_to(HERE)}")
    print(f"             移动 {len(mobile)} -> {OUT_MOBILE.relative_to(HERE)}")
    if fetched:
        print(f"  为 {fetched} 个新 URL 抓取标题后分类")
    return 0


if __name__ == "__main__":
    sys.exit(main())
