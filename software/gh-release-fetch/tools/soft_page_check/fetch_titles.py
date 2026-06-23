"""抓取页面标题并比对历史；支持 A 类快检 / 全量 / 按域名分组报告。"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from build_watchlist import build as build_watchlist_index, domain_label, load_url_meta
from list_scopes import (
    EXTERNAL_LIST_SCOPES,
    LEGACY_LIST_SCOPES,
    LIST_SCOPE_DEFS,
    changed_list_filename,
    is_list_scope,
    read_url_list,
    scope_label as list_scope_label,
)
from report_html import build_index_html, save_diff

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

HERE = Path(__file__).resolve().parent
PAGES_ALL = HERE / "soft_pages_urls.txt"
PAGES_A = HERE / "watch_tier_a_urls.txt"
PAGES_423DOWN = HERE / "423down_digest_urls.txt"
PAGES_7XIAZAI = HERE / "7xiazai_list_urls.txt"
HISTORY_DIR = HERE / "history"
REPORTS_DIR = HERE / "reports"

EXTERNAL_SCOPES = frozenset({"423down"}) | EXTERNAL_LIST_SCOPES

SCOPE_URL_FILES: dict[str, Path] = {
    "a": PAGES_A,
    "all": PAGES_ALL,
    "423down": PAGES_423DOWN,
}
for _scope, _defn in LIST_SCOPE_DEFS.items():
    SCOPE_URL_FILES[_scope] = _defn["url_file"]

CHANGED_LIST_FILES: dict[str, str] = {
    "a": "changed_tier_a_urls.txt",
    "all": "changed_pages_urls.txt",
    "423down": "changed_423down_urls.txt",
}
for _scope in LIST_SCOPE_DEFS:
    CHANGED_LIST_FILES[_scope] = changed_list_filename(_scope)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT = 20
WORKERS = 8


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def normalize_title(title: str) -> str:
    title = unescape(title)
    return re.sub(r"\s+", " ", title).strip()


def latest_path(scope: str) -> Path:
    return HISTORY_DIR / f"titles_latest_{scope.upper()}.json"


def fetch_title(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    try:
        with urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            raw = resp.read(256 * 1024)
            charset = resp.headers.get_content_charset() or "utf-8"
        html = raw.decode(charset, errors="replace")
        parser = TitleParser()
        parser.feed(html)
        title = normalize_title(parser.title) or "(无 title 标签)"
        return {"url": url, "title": title, "status": "ok", "error": ""}
    except HTTPError as exc:
        return {"url": url, "title": "", "status": "http_error", "error": str(exc)}
    except URLError as exc:
        return {"url": url, "title": "", "status": "url_error", "error": str(exc.reason)}
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "title": "", "status": "error", "error": str(exc)}


def enrich_entry(entry: dict, meta: dict) -> dict:
    info = meta.get(entry["url"], {})
    return {
        **entry,
        "tier": info.get("tier", "?"),
        "software": info.get("software", []),
        "domain": info.get("domain") or domain_label(entry["url"]),
    }


def ensure_423down_list() -> None:
    if not PAGES_423DOWN.exists():
        from extract_423down_digest import main as extract_423down_digest

        extract_423down_digest()


def ensure_7xiazai_list() -> None:
    if not PAGES_7XIAZAI.exists():
        from extract_7xiazai_pages import main as extract_7xiazai_pages

        extract_7xiazai_pages()
    from split_7xiazai_urls import main as split_7xiazai_urls

    split_7xiazai_urls()


def load_urls(scope: str) -> tuple[list[str], Path] | None:
    if scope == "a" and not PAGES_A.exists():
        build_watchlist_index()
    if scope == "423down":
        ensure_423down_list()
    elif scope in ("7xiazai_system", "7xiazai_mobile"):
        ensure_7xiazai_list()

    src = SCOPE_URL_FILES.get(scope)
    if src is None:
        raise ValueError(f"未知 scope: {scope}")

    if is_list_scope(scope):
        if not src.exists():
            if LIST_SCOPE_DEFS[scope].get("optional"):
                return None
            raise FileNotFoundError(f"缺少 {src}（{LIST_SCOPE_DEFS[scope]['hint']}）")
        urls = read_url_list(src)
        if not urls:
            if LIST_SCOPE_DEFS[scope].get("optional"):
                return None
            raise FileNotFoundError(f"清单为空: {src}")
        return urls, src

    if not src.exists():
        hints = {
            "423down": "refresh_urls.bat 423down",
        }
        hint = hints.get(scope, "refresh_urls.bat core")
        raise FileNotFoundError(f"缺少 {src}，请先准备：{hint}")
    urls = [line.strip() for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]
    return urls, src


def build_snapshot(entries: list[dict], scope: str, source: Path) -> dict:
    return {
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "source": source.name,
        "count": len(entries),
        "entries": entries,
    }


def save_snapshot(snapshot: dict, scope: str) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = HISTORY_DIR / f"titles_{scope.upper()}_{stamp}.json"
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_path(scope).write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_previous(scope: str) -> dict | None:
    p = latest_path(scope)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def failure_label(entry: dict) -> str:
    """上次抓取失败时的可读摘要（用于比对，不计为标题变化）。"""
    if entry.get("status") == "ok":
        return ""
    err = (entry.get("error") or "").strip()
    if err:
        return err
    return entry.get("status") or "fetch_failed"


def compare(previous: dict, current: dict) -> dict:
    prev_map = {e["url"]: e for e in previous.get("entries", [])}
    curr_map = {e["url"]: e for e in current.get("entries", [])}

    new_urls = sorted(set(curr_map) - set(prev_map))
    removed_urls = sorted(set(prev_map) - set(curr_map))
    title_changed = []
    recovered = []
    unchanged = []
    failed = []

    for url, entry in sorted(curr_map.items()):
        if entry.get("status") != "ok":
            failed.append(entry)
            continue
        if url not in prev_map:
            continue
        prev = prev_map[url]
        if prev.get("status") != "ok":
            recovered.append(
                {
                    "url": url,
                    "old": failure_label(prev),
                    "new": entry["title"],
                    **pick_meta(entry),
                }
            )
        elif normalize_title(prev.get("title", "")) != normalize_title(entry.get("title", "")):
            title_changed.append(
                {"url": url, "old": prev.get("title", ""), "new": entry.get("title", ""), **pick_meta(entry)}
            )
        else:
            unchanged.append(url)

    for url in new_urls:
        entry = curr_map[url]
        if entry.get("status") == "ok":
            title_changed.append({"url": url, "old": "(新增)", "new": entry["title"], **pick_meta(entry)})

    open_candidates = [x["url"] for x in title_changed]
    tier_a_candidates = [x["url"] for x in title_changed if x.get("tier") == "A"]

    return {
        "new_urls": new_urls,
        "removed_urls": removed_urls,
        "title_changed": title_changed,
        "recovered": recovered,
        "unchanged_count": len(unchanged),
        "failed": failed,
        "open_candidates": open_candidates,
        "tier_a_candidates": tier_a_candidates,
    }


def pick_meta(entry: dict) -> dict:
    return {"tier": entry.get("tier", "?"), "software": entry.get("software", []), "domain": entry.get("domain", "")}


def group_by_domain(items: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        groups[item.get("domain") or domain_label(item["url"])].append(item)
    return dict(sorted(groups.items()))


def write_open_list(urls: list[str], name: str) -> Path | None:
    path = HERE / name
    if not urls:
        if path.exists():
            try:
                path.write_text("", encoding="utf-8")
            except OSError as exc:
                print(f"[WARN] 无法清空 {name}（可能被编辑器占用）: {exc}")
        return None
    try:
        path.write_text("\n".join(dict.fromkeys(urls)) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"[WARN] 无法写入 {name}: {exc}")
        return None
    return path


def save_report(scope: str, diff: dict, snapshot_path: Path) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = REPORTS_DIR / f"report_{scope.upper()}_{stamp}.txt"
    lines = [
        f"范围: {scope.upper()} 类",
        f"快照: {snapshot_path.name}",
        f"标题变化: {len(diff['title_changed'])}",
        f"恢复抓取: {len(diff.get('recovered', []))}",
        f"无变化: {diff['unchanged_count']}",
        f"失败: {len(diff['failed'])}",
        "",
    ]
    if diff["title_changed"]:
        lines.append("=== 按域名分组 · 可能有更新 ===")
        for domain, items in group_by_domain(diff["title_changed"]).items():
            lines.append(f"\n[{domain}] ({len(items)})")
            for item in items:
                sw = ",".join(item.get("software") or []) or "-"
                lines.append(f"  {item['url']}")
                lines.append(f"    软件: {sw}")
                lines.append(f"    旧: {item['old']}")
                lines.append(f"    新: {item['new']}")
    if diff.get("recovered"):
        lines.append("\n=== 上次失败 · 本次已抓到（通常无需更新） ===")
        for domain, items in group_by_domain(diff["recovered"]).items():
            lines.append(f"\n[{domain}] ({len(items)})")
            for item in items[:20]:
                lines.append(f"  {item['url']}")
                lines.append(f"    旧: {item['old']}")
                lines.append(f"    新: {item['new']}")
            if len(items) > 20:
                lines.append(f"  ... 另有 {len(items) - 20} 条")
    if diff["failed"]:
        lines.append("\n=== 抓取失败 ===")
        for item in diff["failed"][:30]:
            lines.append(f"  {item['url']}  [{item.get('status')}] {item.get('error')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def scope_label(scope: str) -> str:
    if is_list_scope(scope):
        return list_scope_label(scope)
    labels = {
        "423down": "423DOWN digest",
        "7xiazai": "7xiazai 软件页",
        "a": "A 类",
        "all": "全量页面",
    }
    return labels.get(scope, scope)


def print_report(scope: str, diff: dict, snapshot_path: Path) -> None:
    print()
    print("=" * 60)
    print(f"标题快照比对 · {scope_label(scope)}")
    print("=" * 60)
    print(f"快照: {snapshot_path.name}")
    print(f"标题变化 / 新增: {len(diff['title_changed'])}")
    if diff.get("recovered"):
        print(f"恢复抓取(不计变化): {len(diff['recovered'])}")
    if scope == "a":
        print(f"其中 A 类: {len(diff['tier_a_candidates'])}")
    print(f"无变化: {diff['unchanged_count']}")
    print(f"抓取失败: {len(diff['failed'])}")
    print()

    if diff["title_changed"]:
        print("--- 可能有更新 ---")
        show = diff["title_changed"][:50]
        for item in show:
            sw = ",".join(item.get("software") or []) or "-"
            print(f"  {item['url']}")
            if scope == "a" and item.get("software"):
                print(f"    软件: {sw}")
            print(f"    旧: {item['old']}")
            print(f"    新: {item['new']}")
        if len(diff["title_changed"]) > 50:
            print(f"  ... 另有 {len(diff['title_changed']) - 50} 条，见 reports/")
        print()

    if diff.get("recovered"):
        print("--- 上次失败 · 本次已抓到（通常无需更新） ---")
        show = diff["recovered"][:10]
        for item in show:
            print(f"  {item['url']}")
            print(f"    旧: {item['old']}")
            print(f"    新: {item['new']}")
        if len(diff["recovered"]) > 10:
            print(f"  ... 另有 {len(diff['recovered']) - 10} 条，见 reports/")
        print()

    if diff["failed"]:
        print("--- 抓取失败 ---")
        for item in diff["failed"][:10]:
            print(f"  {item['url']}  [{item.get('status')}]")
        if len(diff["failed"]) > 10:
            print(f"  ... 另有 {len(diff['failed']) - 10} 条")
        print()


def write_scope_changed_lists(scope: str, diff: dict) -> None:
    if scope == "a":
        urls = diff["tier_a_candidates"]
        label = "A类"
    elif scope in CHANGED_LIST_FILES:
        urls = diff["open_candidates"]
        label = scope_label(scope)
    else:
        return

    fname = CHANGED_LIST_FILES[scope]
    f = write_open_list(urls, fname)
    if f:
        print(f"待打开({label}): {f.name} ({len(urls)} 个)")
    elif not diff["open_candidates"]:
        print("无标题变化，无需打开页面。")
    elif scope == "a":
        print("有变化但无 A 类项。")


def cmd_fetch(scope: str, compare_after: bool, skip_missing: bool = False) -> int:
    loaded = load_urls(scope)
    if loaded is None:
        msg = f"[跳过] {scope_label(scope)} — 清单不存在或为空（可选 scope）"
        if skip_missing:
            print(msg)
            return 0
        print(msg)
        return 0

    urls, src = loaded
    meta: dict = {}
    if scope not in EXTERNAL_SCOPES:
        if not HERE.joinpath("url_meta.json").exists():
            build_watchlist_index()
        meta = load_url_meta()
    elif scope in ("423down",) or is_list_scope(scope):
        pass
    print(f"[{scope_label(scope)}] 抓取 {len(urls)} 个页面标题（并发 {WORKERS}）...")

    previous = load_previous(scope) if compare_after else None
    entries: list[dict] = []

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_title, url): url for url in urls}
        done = 0
        for future in as_completed(futures):
            done += 1
            raw = future.result()
            if scope in EXTERNAL_SCOPES:
                domain = scope if is_list_scope(scope) else scope
                if is_list_scope(scope):
                    domain = LIST_SCOPE_DEFS[scope]["site"]
                entries.append({**raw, "tier": scope, "software": [], "domain": domain})
            else:
                entries.append(enrich_entry(raw, meta))
            if done % 20 == 0 or done == len(urls):
                print(f"  进度 {done}/{len(urls)}")

    entries.sort(key=lambda x: x["url"])
    snapshot = build_snapshot(entries, scope, src)
    path = save_snapshot(snapshot, scope)
    print(f"已保存: {path}")
    print(f"最新:   {latest_path(scope)}")

    if previous:
        diff = compare(previous, snapshot)
        print_report(scope, diff, path)
        report_path = save_report(scope, diff, path)
        print(f"报告:   {report_path}")

        save_diff(scope, diff, path)
        write_scope_changed_lists(scope, diff)
    else:
        if compare_after:
            print("首次运行该范围：已保存标题基线到 history\\titles_latest_{}.json".format(scope.upper()))
            print("请再运行一次（带 --compare）才会产生「标题变化」列表与 changed_* 文件。")
        else:
            print("已保存快照。下次加 --compare 即可与本次结果比对。")

    html_path = build_index_html()
    print(f"报告页: {html_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取页面标题并比对历史")
    all_scopes = ["a", "all", "423down", "7xiazai"] + list(LIST_SCOPE_DEFS.keys()) + list(LEGACY_LIST_SCOPES.keys())
    parser.add_argument(
        "--scope",
        choices=sorted(set(all_scopes)),
        default="a",
        help="list scope 按系统/移动拆分；hybase/dayanzai/down66/7xiazai 为旧名（依次跑 system+mobile）",
    )
    parser.add_argument("--compare", action="store_true", help="与上次同范围快照比对")
    args = parser.parse_args()

    if args.scope in LEGACY_LIST_SCOPES:
        rc = 0
        for sub in LEGACY_LIST_SCOPES[args.scope]:
            sub_rc = cmd_fetch(sub, compare_after=args.compare, skip_missing=True)
            if sub_rc != 0:
                rc = sub_rc
        return rc
    return cmd_fetch(args.scope, compare_after=args.compare)


if __name__ == "__main__":
    sys.exit(main())
