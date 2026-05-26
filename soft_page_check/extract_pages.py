"""从 Lastb_soft_version.txt 提取页面 URL（不含直链下载）。"""
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Lastb_soft_version.txt"
OUT_ALL = Path(__file__).resolve().parent / "all_urls.txt"
OUT_PAGES = Path(__file__).resolve().parent / "soft_pages_urls.txt"

DOWNLOAD_EXT = re.compile(
    r"\.(?:exe|zip|apk|7z|msi|dmg|iso|rar|deb|rpm|pkg|msix|appimage|tar\.gz|tgz)(?:\?|$|/)",
    re.I,
)


def is_direct_download(url: str) -> bool:
    lower = url.lower()
    path = urlparse(url).path.lower()
    if DOWNLOAD_EXT.search(path):
        return True
    if "/releases/download/" in lower:
        return True
    if "/ftp/" in lower:
        return True
    if "gh-proxy.com/" in lower:
        return True
    return False


def extract_section(text: str) -> str:
    lines = text.splitlines()
    cut = next(i for i, line in enumerate(lines) if "最终选择指南" in line)
    return "\n".join(lines[: cut - 1])


def main() -> None:
    section = extract_section(SRC.read_text(encoding="utf-8"))
    raw = re.findall(r"https?://[^\s<>\"'\)\]\（]+", section)
    urls = []
    for url in raw:
        url = url.rstrip(".,;)\]\"'（）")
        if url.startswith(("http://", "https://")) and "localhost" not in url:
            urls.append(url)
    all_unique = sorted(set(urls))
    pages = [u for u in all_unique if not is_direct_download(u)]

    OUT_ALL.write_text("\n".join(all_unique) + "\n", encoding="utf-8")
    OUT_PAGES.write_text("\n".join(pages) + "\n", encoding="utf-8")
    print(f"全部 URL: {len(all_unique)} -> {OUT_ALL.name}")
    print(f"页面 URL: {len(pages)} -> {OUT_PAGES.name}")


if __name__ == "__main__":
    main()
