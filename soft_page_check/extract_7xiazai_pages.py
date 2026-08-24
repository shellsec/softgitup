"""从 7xiazai 列表页发现软件详情页 URL，并合并 Lastb_soft_version.txt 中的链接。"""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from http_fetch import FetchError, fetch_html

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SRC = ROOT / "Lastb_soft_version.txt"
OUT = HERE / "7xiazai_list_urls.txt"
CONFIG = HERE / "7xiazai_config.json"

TXT_PAT = re.compile(r"https?://(?:www\.)?7xiazai\.com[^\s<>\"'\)\]\（]*", re.I)
HREF_PAT = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)

TIMEOUT = 20
WORKERS = 8

DEFAULT_EXCLUDE = {
    "app",
    "os",
    "data",
    "design",
    "hardware",
    "media",
    "microsoft",
    "software",
    "mediaapp",
    "tag",
    "category",
    "author",
    "feed",
    "comments",
    "wp-content",
    "wp-admin",
    "xmlrpc.php",
}


def load_config() -> dict:
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    else:
        cfg = {}
    cfg.setdefault("base", "https://www.7xiazai.com")
    cfg.setdefault("max_page", 65)
    cfg.setdefault("exclude_slugs", sorted(DEFAULT_EXCLUDE))
    cfg.setdefault("discover_from_lists", True)
    return cfg


def list_page_url(base: str, page_num: int) -> str:
    base = base.rstrip("/")
    if page_num <= 1:
        return f"{base}/"
    return f"{base}/page/{page_num}/"


def normalize_soft_url(href: str, base: str, exclude: set[str]) -> str | None:
    href = href.split("#")[0].strip()
    if not href or href.startswith(("javascript:", "mailto:", "tel:")):
        return None
    url = urljoin(base.rstrip("/") + "/", href)
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in ("7xiazai.com", "www.7xiazai.com"):
        return None
    path = parsed.path.strip("/")
    if not path:
        return None
    if path.startswith("page/"):
        return None
    if "/" in path:
        return None
    slug = path.lower()
    if slug in exclude:
        return None
    return f"https://www.7xiazai.com/{slug}"


def merge_discovered(
    discovered: list[str],
    extras: list[str],
    existing: list[str],
    errors: list[str],
) -> list[str]:
    """列表页全失败时保留已有清单，避免 403/Cloudflare 把 URL 覆盖成 txt 残集。"""
    if not discovered and errors:
        return sorted(set(existing) | set(extras))
    return sorted(set(discovered) | set(extras) | set(existing))


def existing_soft_urls(exclude: set[str]) -> list[str]:
    found: set[str] = set()
    for path in (OUT, HERE / "list" / "7xiazai_list_urls.txt"):
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            norm = normalize_soft_url(line, "https://www.7xiazai.com", exclude)
            if norm:
                found.add(norm)
    return sorted(found)


def fetch_list_links(page_num: int, base: str, exclude: set[str]) -> tuple[int, set[str], str | None]:
    url = list_page_url(base, page_num)
    try:
        html = fetch_html(url, timeout=TIMEOUT, retries=2, max_bytes=768 * 1024)
    except FetchError as exc:
        return page_num, set(), str(exc)
    except Exception as exc:  # noqa: BLE001
        return page_num, set(), str(exc)

    found: set[str] = set()
    for href in HREF_PAT.findall(html):
        norm = normalize_soft_url(href, base, exclude)
        if norm:
            found.add(norm)
    return page_num, found, None


def discover_from_lists(base: str, max_page: int, exclude: set[str]) -> tuple[list[str], list[str]]:
    merged: set[str] = set()
    errors: list[str] = []
    print(f"从列表页 / ~ /page/{max_page}/ 发现软件页链接（并发 {WORKERS}）...")
    first_page, first_found, first_err = fetch_list_links(1, base, exclude)
    if first_err:
        errors.append(f"page/{first_page}: {first_err}")
        if "Cloudflare" in first_err:
            print(f"  首页被拦截（{first_err}），跳过其余 {max_page - 1} 个列表页，保留已有清单。")
            return [], errors
    merged |= first_found

    rest = list(range(2, max_page + 1))
    if rest:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(fetch_list_links, n, base, exclude): n for n in rest}
            done = 1
            total = max_page
            for future in as_completed(futures):
                done += 1
                page_num, found, err = future.result()
                merged |= found
                if err:
                    errors.append(f"page/{page_num}: {err}")
                if done % 10 == 0 or done == total:
                    print(f"  进度 {done}/{total} · 已发现 {len(merged)} 个软件页")
    if errors:
        print(f"  列表页抓取异常: {len(errors)} 个（见下方）")
        for line in errors[:5]:
            print(f"    {line}")
        if len(errors) > 5:
            print(f"    ... 另有 {len(errors) - 5} 个")
    return sorted(merged), errors


def urls_from_txt(base: str, exclude: set[str]) -> list[str]:
    if not SRC.exists():
        return []
    out: set[str] = set()
    for raw in TXT_PAT.findall(SRC.read_text(encoding="utf-8")):
        norm = normalize_soft_url(raw, base, exclude)
        if norm:
            out.add(norm)
    return sorted(out)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = load_config()
    base = cfg.get("base", "https://www.7xiazai.com")
    max_page = int(cfg.get("max_page", 65))
    exclude = {s.lower() for s in cfg.get("exclude_slugs", [])}
    exclude |= DEFAULT_EXCLUDE

    discovered: list[str] = []
    errors: list[str] = []
    if cfg.get("discover_from_lists", True):
        discovered, errors = discover_from_lists(base, max_page, exclude)

    extras = urls_from_txt(base, exclude)
    existing = existing_soft_urls(exclude)
    merged = merge_discovered(discovered, extras, existing, errors)
    if not discovered and errors:
        print(f"列表页未发现新链接（{len(errors)} 个异常），保留已有 {len(existing)} 条并合并 txt。")
    OUT.write_text("\n".join(merged) + "\n", encoding="utf-8")
    list_out = HERE / "list" / "7xiazai_list_urls.txt"
    list_out.parent.mkdir(parents=True, exist_ok=True)
    list_out.write_text("\n".join(merged) + "\n", encoding="utf-8")

    from split_7xiazai_urls import main as split_7xiazai_urls

    split_7xiazai_urls()

    print()
    print(f"软件详情页（监控标题）: {len(merged)} 条 -> {OUT.name}")
    print(f"  自列表页发现: {len(discovered)}")
    print(f"  自 txt 合并: {len(extras)}")
    print("说明: 不再监控 /page/N/ 列表页，只监控各软件页 <title>（含版本号）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
