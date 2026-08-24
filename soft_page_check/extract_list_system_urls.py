"""从 dayanzai 首页分页、down66 /pc 分页发现 PC 区 URL，写入 list/*_system_urls.txt。"""
from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from http_fetch import FetchError, fetch_html

HERE = Path(__file__).resolve().parent
LIST = HERE / "list"

TIMEOUT = 25
WORKERS = 8
HREF_PAT = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)
PAGES_HINT = re.compile(r"pages:\s*\d+-(\d+)", re.I)


def fetch(url: str) -> str:
    return fetch_html(url, timeout=TIMEOUT, retries=3, max_bytes=768 * 1024)


def read_url_lines(path: Path) -> set[str]:
    if not path.exists():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line.split()[0])
    return out


def last_page_hint(path: Path, default: int) -> int:
    if not path.exists():
        return default
    for line in path.read_text(encoding="utf-8").splitlines()[:8]:
        match = PAGES_HINT.search(line)
        if match:
            return int(match.group(1))
    return default


def write_url_list(path: Path, urls: list[str], header_lines: list[str]) -> None:
    body = "\n".join(header_lines + [""] + urls) + "\n"
    path.write_text(body, encoding="utf-8")


def dayanzai_article_urls(html: str) -> set[str]:
    urls: set[str] = set()
    for href in HREF_PAT.findall(html):
        u = urljoin("https://www.dayanzai.me/", href.split("#")[0].strip())
        parsed = urlparse(u)
        host = parsed.netloc.lower()
        if host not in ("dayanzai.me", "www.dayanzai.me"):
            continue
        path = parsed.path.strip("/")
        if not path.endswith(".html"):
            continue
        if path.startswith("android") or "/android/" in parsed.path:
            continue
        urls.add(f"https://www.dayanzai.me/{path}")
    return urls


def down66_pc_urls(html: str) -> set[str]:
    skip = {
        "pc",
        "windows",
        "app",
        "wp-admin",
        "wp-content",
        "tag",
        "category",
        "author",
        "feed",
        "login",
        "register",
        "wp-login.php",
        "xmlrpc.php",
    }
    urls: set[str] = set()
    for href in HREF_PAT.findall(html):
        u = urljoin("https://down66.com/", href.split("#")[0].strip())
        parsed = urlparse(u)
        host = parsed.netloc.lower()
        if host not in ("down66.com", "www.down66.com"):
            continue
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        if len(parts) != 1 or parts[0] in skip:
            continue
        urls.add(f"https://down66.com/{parts[0]}")
    return urls


def discover_last_page(page_url_fmt: str, max_probe: int = 400, fallback: int = 1) -> int:
    lo, hi = 1, 1
    while hi <= max_probe:
        try:
            fetch(page_url_fmt.format(hi))
            lo = hi
            hi *= 2
        except FetchError as exc:
            if exc.status == 404:
                break
            print(f"  分页探测失败 page {hi}: {exc}，沿用已确认 {lo} / 回退 {fallback}")
            return max(lo, fallback) if lo > 1 else fallback
    left, right = lo + 1, min(hi - 1, max_probe)
    last = lo
    while left <= right:
        mid = (left + right) // 2
        try:
            fetch(page_url_fmt.format(mid))
            last = mid
            left = mid + 1
        except FetchError as exc:
            if exc.status == 404:
                right = mid - 1
            else:
                print(f"  分页探测失败 page {mid}: {exc}，使用已确认 {last}")
                return max(last, fallback)
    return last


def crawl_pages(page_urls: list[str], parse_fn) -> tuple[set[str], list[str]]:
    found: set[str] = set()
    errors: list[str] = []
    done = 0
    total = len(page_urls)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch, url): url for url in page_urls}
        for fut in as_completed(futures):
            url = futures[fut]
            done += 1
            try:
                html = fut.result()
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{url}: {exc}")
            else:
                found |= parse_fn(html)
            if done % 20 == 0 or done == total:
                print(f"  进度 {done}/{total} · 已发现 {len(found)} · 失败 {len(errors)}")
    return found, errors


def crawl_dayanzai_system() -> tuple[list[str], list[str]]:
    out_path = LIST / "dayanzai_system_urls.txt"
    mobile = read_url_lines(LIST / "dayanzai_android_urls.txt")
    existing = read_url_lines(out_path)
    fallback = last_page_hint(out_path, 271)
    last = discover_last_page(
        "https://www.dayanzai.me/page/{}/",
        fallback=fallback,
    )
    page_urls = ["https://www.dayanzai.me/"] + [
        f"https://www.dayanzai.me/page/{p}/" for p in range(2, last + 1)
    ]
    print(f"dayanzai 系统区分页 1-{last}（并发 {WORKERS}）...")
    found, errors = crawl_pages(page_urls, dayanzai_article_urls)
    if errors:
        print(f"  列表页异常 {len(errors)} 个，与已有清单合并以免丢 URL")
        found |= existing
    system = sorted(found - mobile)
    header = [
        "# dayanzai.me 首页分页（排除 android 清单已有 URL）",
        f"# pages: 1-{last}",
        f"# total: {len(system)}",
    ]
    return system, header


def crawl_down66_system() -> tuple[list[str], list[str]]:
    out_path = LIST / "down66_system_urls.txt"
    mobile = read_url_lines(LIST / "down66_app_urls.txt")
    existing = read_url_lines(out_path)
    fallback = last_page_hint(out_path, 20)
    last = discover_last_page(
        "https://down66.com/pc/page/{}/",
        max_probe=80,
        fallback=fallback,
    )
    page_urls = ["https://down66.com/pc"] + [
        f"https://down66.com/pc/page/{p}/" for p in range(2, last + 1)
    ]
    print(f"down66 系统区分页 1-{last}（并发 {WORKERS}）...")
    found, errors = crawl_pages(page_urls, down66_pc_urls)
    if errors:
        print(f"  列表页异常 {len(errors)} 个，与已有清单合并以免丢 URL")
        found |= existing
    system = sorted(found - mobile)
    header = [
        "# down66.com/pc 分页（排除 app 清单已有 URL）",
        f"# pages: 1-{last}",
        f"# total: {len(system)}",
    ]
    return system, header


def _write_or_keep(name: str, crawl_fn, out_path: Path) -> None:
    existing = read_url_lines(out_path)
    try:
        urls, header = crawl_fn()
    except Exception as exc:  # noqa: BLE001
        print(f"{name}: 抓取中断（{exc}），保留现有 {len(existing)} 条")
        return
    if not urls and existing:
        print(f"{name}: 未发现 URL，保留现有 {len(existing)} 条 -> {out_path.relative_to(HERE)}")
        return
    write_url_list(out_path, urls, header)
    print(f"{name}: {len(urls)} -> {out_path.relative_to(HERE)}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    _write_or_keep("dayanzai_system", crawl_dayanzai_system, LIST / "dayanzai_system_urls.txt")
    _write_or_keep("down66_system", crawl_down66_system, LIST / "down66_system_urls.txt")


if __name__ == "__main__":
    main()
