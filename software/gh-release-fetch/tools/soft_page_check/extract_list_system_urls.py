"""从 dayanzai 首页分页、down66 /pc 分页发现 PC 区 URL，写入 list/*_system_urls.txt。"""
from __future__ import annotations

import re
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
LIST = HERE / "list"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT = 25
WORKERS = 12
HREF_PAT = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)
CTX = ssl.create_default_context()


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
        return resp.read().decode("utf-8", errors="replace")


def read_url_lines(path: Path) -> set[str]:
    if not path.exists():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line.split()[0])
    return out


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


def discover_last_page(first_url: str, page_url_fmt: str, max_probe: int = 400) -> int:
    lo, hi = 1, 1
    while hi <= max_probe:
        try:
            fetch(page_url_fmt.format(hi))
            lo = hi
            hi *= 2
        except HTTPError as exc:
            if exc.code == 404:
                break
            raise
    left, right = lo + 1, min(hi - 1, max_probe)
    last = lo
    while left <= right:
        mid = (left + right) // 2
        try:
            fetch(page_url_fmt.format(mid))
            last = mid
            left = mid + 1
        except HTTPError as exc:
            if exc.code == 404:
                right = mid - 1
            else:
                raise
    return last


def crawl_pages(page_urls: list[str], parse_fn) -> set[str]:
    found: set[str] = set()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch, url): url for url in page_urls}
        for fut in as_completed(futures):
            html = fut.result()
            found |= parse_fn(html)
    return found


def crawl_dayanzai_system() -> tuple[list[str], list[str]]:
    mobile = read_url_lines(LIST / "dayanzai_android_urls.txt")
    last = discover_last_page(
        "https://www.dayanzai.me/",
        "https://www.dayanzai.me/page/{}/",
    )
    page_urls = ["https://www.dayanzai.me/"] + [
        f"https://www.dayanzai.me/page/{p}/" for p in range(2, last + 1)
    ]
    found = crawl_pages(page_urls, dayanzai_article_urls)
    system = sorted(found - mobile)
    header = [
        "# dayanzai.me 首页分页（排除 android 清单已有 URL）",
        f"# pages: 1-{last}",
        f"# total: {len(system)}",
    ]
    return system, header


def crawl_down66_system() -> tuple[list[str], list[str]]:
    mobile = read_url_lines(LIST / "down66_app_urls.txt")
    last = discover_last_page(
        "https://down66.com/pc",
        "https://down66.com/pc/page/{}/",
        max_probe=80,
    )
    page_urls = ["https://down66.com/pc"] + [
        f"https://down66.com/pc/page/{p}/" for p in range(2, last + 1)
    ]
    found = crawl_pages(page_urls, down66_pc_urls)
    system = sorted(found - mobile)
    header = [
        "# down66.com/pc 分页（排除 app 清单已有 URL）",
        f"# pages: 1-{last}",
        f"# total: {len(system)}",
    ]
    return system, header


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    dayanzai_urls, dayanzai_hdr = crawl_dayanzai_system()
    out_d = LIST / "dayanzai_system_urls.txt"
    write_url_list(out_d, dayanzai_urls, dayanzai_hdr)
    print(f"dayanzai_system: {len(dayanzai_urls)} -> {out_d.relative_to(HERE)}")

    down66_urls, down66_hdr = crawl_down66_system()
    out_66 = LIST / "down66_system_urls.txt"
    write_url_list(out_66, down66_urls, down66_hdr)
    print(f"down66_system: {len(down66_urls)} -> {out_66.relative_to(HERE)}")


if __name__ == "__main__":
    main()
