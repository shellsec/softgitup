"""从 Lastb_soft_version.txt 提取页面 URL（不含直链下载）。"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from paths import lastb_soft_version_path

HERE = Path(__file__).resolve().parent
OUT_ALL = HERE / "all_urls.txt"
OUT_PAGES = HERE / "soft_pages_urls.txt"

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
    src = lastb_soft_version_path()
    if src is None:
        if OUT_PAGES.exists():
            n = sum(1 for line in OUT_PAGES.read_text(encoding="utf-8").splitlines() if line.strip())
            print(f"跳过 extract_pages：未找到 Lastb_soft_version.txt，沿用已有 {OUT_PAGES.name}（{n} 条）")
            print("  若需刷新装机区 URL，请设置环境变量 LASTB_SOFT_VERSION=源文件路径")
            return
        print(
            "错误：未找到 Lastb_soft_version.txt，且无缓存 soft_pages_urls.txt。\n"
            "  请将装机清单放到仓库根目录，或设置 LASTB_SOFT_VERSION=完整路径",
            file=sys.stderr,
        )
        raise SystemExit(1)

    section = extract_section(src.read_text(encoding="utf-8"))
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
