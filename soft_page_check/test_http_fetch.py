"""http_fetch / 清单保护 单测（不访问外网）。"""
from __future__ import annotations

import unittest
from unittest.mock import patch
from extract_7xiazai_pages import merge_discovered
from extract_list_system_urls import crawl_pages, last_page_hint
from fetch_titles import encoding_only_change, looks_garbled_cjk, should_preserve_latest
from http_fetch import FetchError, decode_html, is_cloudflare_challenge


class FakeHeaders(dict):
    def get(self, key, default=None):
        for k, v in self.items():
            if k.lower() == str(key).lower():
                return v
        return default


class HttpFetchTests(unittest.TestCase):
    def test_decode_gb18030_without_header(self) -> None:
        raw = "Wine 安装 Windows".encode("gb18030")
        self.assertEqual(decode_html(raw), "Wine 安装 Windows")

    def test_decode_prefers_meta_gbk(self) -> None:
        raw = b'<meta charset="gbk">' + "\u9ed1\u57df".encode("gb18030")
        self.assertIn("黑域", decode_html(raw))

    def test_cloudflare_challenge_header(self) -> None:
        headers = FakeHeaders({"Server": "cloudflare", "Cf-Mitigated": "challenge"})
        self.assertTrue(is_cloudflare_challenge(403, headers, b"Just a moment..."))
        self.assertFalse(is_cloudflare_challenge(404, headers, b"Just a moment..."))

    def test_merge_keeps_existing_when_discover_fails(self) -> None:
        merged = merge_discovered(
            discovered=[],
            extras=["https://www.7xiazai.com/chrome"],
            existing=["https://www.7xiazai.com/winrar", "https://www.7xiazai.com/chrome"],
            errors=["page/1: Cloudflare 人机验证拦截"],
        )
        self.assertEqual(
            merged,
            ["https://www.7xiazai.com/chrome", "https://www.7xiazai.com/winrar"],
        )

    def test_merge_unions_new_links(self) -> None:
        merged = merge_discovered(
            discovered=["https://www.7xiazai.com/newsoft"],
            extras=["https://www.7xiazai.com/chrome"],
            existing=["https://www.7xiazai.com/winrar"],
            errors=[],
        )
        self.assertEqual(len(merged), 3)

    def test_crawl_pages_skips_timeout(self) -> None:
        def parse(html: str) -> set[str]:
            return {html} if html else set()

        with patch("extract_list_system_urls.fetch") as mock_fetch:
            mock_fetch.side_effect = [FetchError("读取超时", kind="timeout"), "ok-page"]
            found, errors = crawl_pages(["https://a/", "https://b/"], parse)
        self.assertEqual(found, {"ok-page"})
        self.assertEqual(len(errors), 1)

    def test_last_page_hint(self) -> None:
        from pathlib import Path
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "list.txt"
            path.write_text("# pages: 1-271\n# total: 3\nhttps://x\n", encoding="utf-8")
            self.assertEqual(last_page_hint(path, 10), 271)
            self.assertEqual(last_page_hint(Path(tmp) / "missing.txt", 10), 10)

    def test_preserve_latest_when_all_fail(self) -> None:
        prev = {"entries": [{"status": "ok"}, {"status": "ok"}]}
        curr = {"entries": [{"status": "cf_challenge"}, {"status": "http_error"}]}
        self.assertTrue(should_preserve_latest(prev, curr))
        self.assertFalse(should_preserve_latest(None, curr))
        self.assertFalse(should_preserve_latest(prev, {"entries": [{"status": "ok"}]}))

    def test_garbled_title_same_version_is_not_change(self) -> None:
        old = "[Linux] Linux\ufffd\ufffd Wine v10.0 \ufffd"
        new = "[Linux] Linux安装Windows程序 Wine v10.0 稳定版发布"
        self.assertTrue(looks_garbled_cjk(old))
        self.assertFalse(looks_garbled_cjk(new))
        self.assertTrue(encoding_only_change(old, new))
        self.assertFalse(encoding_only_change(old, new.replace("v10.0", "v10.1")))

    def test_http_error_body_cloudflare(self) -> None:
        body = b"<!DOCTYPE html><title>Just a moment...</title>challenges.cloudflare"
        headers = FakeHeaders({"Server": "cloudflare"})
        self.assertTrue(is_cloudflare_challenge(403, headers, body))


if __name__ == "__main__":
    unittest.main()
