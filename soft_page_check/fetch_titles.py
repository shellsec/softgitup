"""抓取页面标题并比对历史；支持 A 类快检 / 全量 / 按域名分组报告。"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from http_fetch import FetchError, fetch_html

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


VERSION_TOKEN = re.compile(r"v\d+(?:[A-Za-z]\d*)?(?:\.\d+){0,4}|\b\d+(?:\.\d+){2,4}\b|\b\d{6,}\b", re.I)


def looks_garbled_cjk(title: str) -> bool:
    """Detect CJK mojibake: U+FFFD and/or Cyrillic leftovers from GBK→UTF-8 replace."""
    if not title:
        return False
    if "\ufffd" in title:
        return True
    cyr = sum(1 for c in title if "\u0400" <= c <= "\u04ff" or "\u0300" <= c <= "\u036f")
    cjk = sum(1 for c in title if "\u4e00" <= c <= "\u9fff")
    if cyr >= 2 and cjk == 0:
        return True
    if cyr >= 1 and cjk == 0 and ("[Windows]" in title or "[Android]" in title or "[Mac]" in title):
        return True
    return False


def ascii_skeleton(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "", title or "")


def version_tokens(title: str) -> list[str]:
    return [m.group(0).lower() for m in VERSION_TOKEN.finditer(title or "")]


def version_tokens_raw(title: str) -> list[str]:
    return [m.group(0) for m in VERSION_TOKEN.finditer(title or "")]


def try_mojibake_repair(title: str) -> str | None:
    """Best-effort classic repairs (UTF-8-as-latin1/cp1252, or as GBK)."""
    if not title or not looks_garbled_cjk(title):
        return None
    for enc_from in ("latin-1", "cp1252"):
        try:
            raw = title.encode(enc_from)
        except UnicodeEncodeError:
            continue
        for enc_to in ("utf-8", "gb18030", "gbk"):
            try:
                fixed = raw.decode(enc_to)
            except UnicodeDecodeError:
                continue
            if fixed and not looks_garbled_cjk(fixed) and fixed != title:
                return normalize_title(fixed)
    return None


def reconstruct_title_from_hint(garbled: str, good: str) -> str | None:
    """Rebuild readable old title by swapping version tokens into a good new title."""
    if not garbled or not good or looks_garbled_cjk(good):
        return None
    old_v = version_tokens_raw(garbled)
    new_v = version_tokens_raw(good)
    if not old_v or not new_v:
        if ascii_skeleton(garbled) == ascii_skeleton(good):
            return normalize_title(good)
        return None
    # Pair shared version-token prefix even when counts differ.
    result = good
    for new_tok, old_tok in zip(new_v, old_v):
        if new_tok.lower() == old_tok.lower():
            continue
        idx = result.lower().find(new_tok.lower())
        if idx < 0:
            if ascii_skeleton(garbled) == ascii_skeleton(good):
                return normalize_title(good)
            return None
        result = result[:idx] + old_tok + result[idx + len(new_tok) :]
    return normalize_title(result)


def fix_title(title: str, hint: str | None = None) -> str:
    """Repair a garbled title; optionally use a known-good hint (same URL / new title)."""
    if not looks_garbled_cjk(title):
        return title
    repaired = try_mojibake_repair(title)
    if repaired:
        return repaired
    if hint:
        reconstructed = reconstruct_title_from_hint(title, hint)
        if reconstructed:
            return reconstructed
    return title


def encoding_only_change(old_title: str, new_title: str) -> bool:
    if not looks_garbled_cjk(old_title) or looks_garbled_cjk(new_title):
        return False
    old_v = version_tokens(old_title)
    new_v = version_tokens(new_title)
    if old_v or new_v:
        return old_v == new_v
    return True

def should_preserve_latest(previous: dict | None, current: dict) -> bool:
    curr_ok = sum(1 for e in current.get("entries", []) if e.get("status") == "ok")
    prev_ok = sum(1 for e in (previous or {}).get("entries", []) if e.get("status") == "ok")
    return curr_ok == 0 and prev_ok > 0


def fetch_title(url: str) -> dict:
    try:
        html = fetch_html(url, timeout=TIMEOUT, retries=2, max_bytes=256 * 1024)
        parser = TitleParser()
        parser.feed(html)
        title = normalize_title(parser.title) or "(无 title 标签)"
        return {"url": url, "title": title, "status": "ok", "error": ""}
    except FetchError as exc:
        return {"url": url, "title": "", "status": exc.kind, "error": str(exc)}
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
            "423down": "extract_423down_digest.bat",
        }
        hint = hints.get(scope, "extract_pages.bat / build_watchlist.bat")
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


def save_snapshot(snapshot: dict, scope: str, update_latest: bool = True) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = HISTORY_DIR / f"titles_{scope.upper()}_{stamp}.json"
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    if update_latest:
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



def repair_stored_titles() -> int:
    """Repair mojibake in history snapshots and last_diff_*.json. Returns fix count."""
    fixed = 0

    good_by_url: dict[str, str] = {}
    for latest in HISTORY_DIR.glob("titles_latest_*.json"):
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for entry in data.get("entries", []):
            title = entry.get("title") or ""
            url = entry.get("url") or ""
            if url and title and entry.get("status") == "ok" and not looks_garbled_cjk(title):
                good_by_url[url] = title

    def _fix_entry_title(entry: dict) -> bool:
        nonlocal fixed
        title = entry.get("title") or ""
        url = entry.get("url") or ""
        if not looks_garbled_cjk(title):
            return False
        repaired = fix_title(title, hint=good_by_url.get(url))
        if repaired != title:
            entry["title"] = repaired
            fixed += 1
            return True
        return False

    for snap in HISTORY_DIR.glob("titles_*.json"):
        try:
            data = json.loads(snap.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        changed = False
        for entry in data.get("entries", []):
            if _fix_entry_title(entry):
                changed = True
        if changed:
            snap.write_text(json.dumps(data, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")

    for diff_path in REPORTS_DIR.glob("last_diff_*.json"):
        try:
            data = json.loads(diff_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        changed = False
        for key in ("title_changed", "recovered"):
            for item in data.get(key) or []:
                old = item.get("old") or ""
                new = item.get("new") or ""
                url = item.get("url") or ""
                if looks_garbled_cjk(old):
                    hint = new if new and not looks_garbled_cjk(new) else good_by_url.get(url)
                    repaired = fix_title(old, hint=hint)
                    if repaired != old:
                        item["old"] = repaired
                        fixed += 1
                        changed = True
                if looks_garbled_cjk(new):
                    repaired = fix_title(new, hint=good_by_url.get(url))
                    if repaired != new:
                        item["new"] = repaired
                        fixed += 1
                        changed = True
        if changed:
            diff_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")

    return fixed



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
            raw_old = prev.get("title", "")
            new_title = entry.get("title", "")
            old_title = fix_title(raw_old, hint=new_title)
            if normalize_title(old_title) == normalize_title(new_title):
                recovered.append(
                    {
                        "url": url,
                        "old": old_title,
                        "new": new_title,
                        **pick_meta(entry),
                    }
                )
            elif encoding_only_change(raw_old, new_title):
                recovered.append(
                    {
                        "url": url,
                        "old": old_title,
                        "new": new_title,
                        **pick_meta(entry),
                    }
                )
            else:
                title_changed.append(
                    {"url": url, "old": old_title, "new": new_title, **pick_meta(entry)}
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
        print(f"恢复抓取/编码修复(不计变化): {len(diff['recovered'])}")
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

    previous_latest = load_previous(scope)
    previous = previous_latest if compare_after else None
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
    preserve = should_preserve_latest(previous_latest, snapshot)
    path = save_snapshot(snapshot, scope, update_latest=not preserve)
    print(f"已保存: {path}")
    if preserve:
        print("本次全部抓取失败，未覆盖 titles_latest（避免冲掉可用基线）。")
    else:
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
        help="list scope 按系统/移动拆分；hybase/dayanzai/appx64/down66/7xiazai 为旧名（依次跑 system+mobile；down66=appx64 别名）",
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
