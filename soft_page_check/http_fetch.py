"""共享页面抓取：浏览器头、证书、重试、HTML 编码、Cloudflare 识别。"""
from __future__ import annotations

import functools
import re
import socket
import ssl
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "close",
}
RETRY_STATUS = {429, 502, 503, 504}
META_CHARSET = re.compile(br"""charset\s*=\s*['\"]?([\w-]+)""", re.I)
TRANSIENT = (TimeoutError, socket.timeout, ConnectionError, BrokenPipeError)


class FetchError(Exception):
    def __init__(self, message: str, *, kind: str = "error", status: int | None = None) -> None:
        super().__init__(message)
        self.kind = kind
        self.status = status


@functools.lru_cache(maxsize=1)
def ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


def is_cloudflare_challenge(status: int | None, headers, body: bytes = b"") -> bool:
    if status not in (403, 503):
        return False
    server = ""
    mitigated = ""
    if headers is not None:
        server = str(headers.get("Server") or headers.get("server") or "")
        mitigated = str(headers.get("Cf-Mitigated") or headers.get("cf-mitigated") or "")
    if mitigated.lower() == "challenge":
        return True
    if "cloudflare" in server.lower() and (
        b"just a moment" in body.lower() or b"cf-mitigated" in body.lower() or b"challenges.cloudflare" in body
    ):
        return True
    return False


def decode_html(raw: bytes, header_charset: str | None = None) -> str:
    candidates: list[str] = []
    if header_charset:
        candidates.append(header_charset)
    match = META_CHARSET.search(raw[:8192])
    if match:
        candidates.append(match.group(1).decode("ascii", errors="ignore"))
    candidates.extend(["utf-8", "gb18030"])
    seen: set[str] = set()
    for enc in candidates:
        enc = (enc or "").strip().lower().replace("_", "-")
        if not enc or enc in seen:
            continue
        seen.add(enc)
        if enc in {"gbk", "gb2312", "gb-2312"}:
            enc = "gb18030"
        try:
            return raw.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", errors="replace")


def fetch_bytes(
    url: str,
    *,
    timeout: int = 20,
    retries: int = 3,
    max_bytes: int | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, str | None]:
    req_headers = dict(BROWSER_HEADERS)
    if headers:
        req_headers.update(headers)
    last_exc: BaseException | None = None
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers=req_headers)
            with urlopen(req, timeout=timeout, context=ssl_context()) as resp:
                raw = resp.read(max_bytes) if max_bytes else resp.read()
                return raw, resp.headers.get_content_charset()
        except HTTPError as exc:
            body = b""
            try:
                body = exc.read(2048)
            except Exception:  # noqa: BLE001
                pass
            if is_cloudflare_challenge(exc.code, exc.headers, body):
                raise FetchError("Cloudflare 人机验证拦截", kind="cf_challenge", status=exc.code) from exc
            if exc.code in RETRY_STATUS and attempt < retries:
                last_exc = exc
                time.sleep(1.2 * attempt)
                continue
            raise FetchError(f"HTTP {exc.code}", kind="http_error", status=exc.code) from exc
        except TRANSIENT as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(1.2 * attempt)
                continue
            raise FetchError("读取超时", kind="timeout") from exc
        except URLError as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(1.2 * attempt)
                continue
            raise FetchError(str(exc.reason), kind="url_error") from exc
    raise FetchError(str(last_exc or "fetch failed"), kind="error")


def fetch_html(
    url: str,
    *,
    timeout: int = 20,
    retries: int = 3,
    max_bytes: int | None = None,
    headers: dict[str, str] | None = None,
) -> str:
    raw, charset = fetch_bytes(url, timeout=timeout, retries=retries, max_bytes=max_bytes, headers=headers)
    return decode_html(raw, charset)
