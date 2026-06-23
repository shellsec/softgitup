"""从 Lastb_soft_version.txt digest 区提取 423down 链接（去重）。"""
import re
import sys
from pathlib import Path

from paths import lastb_soft_version_path

HERE = Path(__file__).resolve().parent
OUT = HERE / "423down_digest_urls.txt"

PAT = re.compile(r"https?://(?:www\.)?423down\.com/[^\s<>\"'\)\]\（]+", re.I)


def normalize(url: str) -> str:
    url = url.rstrip(".,;)\]\"'（）")
    url = url.lower().replace("https://423down.com/", "https://www.423down.com/")
    return url


def extract_digest_section(text: str) -> str:
    lines = text.splitlines()
    cut = next(i for i, line in enumerate(lines) if "最终选择指南" in line)
    return "\n".join(lines[cut:])


def main() -> None:
    src = lastb_soft_version_path()
    if src is None:
        if OUT.exists():
            n = sum(1 for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip())
            print(f"跳过 digest 提取：未找到 Lastb_soft_version.txt，沿用已有 {OUT.name}（{n} 条）")
            return
        print("错误：未找到 Lastb_soft_version.txt，且无 423down_digest_urls.txt", file=sys.stderr)
        raise SystemExit(1)

    digest = extract_digest_section(src.read_text(encoding="utf-8"))
    urls = sorted({normalize(u) for u in PAT.findall(digest)})
    OUT.write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8")
    print(f"digest 区 423down 去重: {len(urls)} 条")
    print(f"已写入: {OUT}")


if __name__ == "__main__":
    main()
