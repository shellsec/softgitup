"""监控清单：A= config.json 同步目录相关页面，B= 其余参考页。"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CONFIG = ROOT / "config.json"
PAGES_FILE = HERE / "soft_pages_urls.txt"
WATCHLIST = HERE / "watchlist.json"
TIER_A_FILE = HERE / "watch_tier_a_urls.txt"
URL_META = HERE / "url_meta.json"

# config.json software_dirs -> URL 匹配关键词（小写子串）
A_PATTERNS: dict[str, list[str]] = {
    "WinMemoryCleaner": ["winmemorycleaner", "igormundstein/winmemorycleaner"],
    "NetTime": ["timesynctool", "nettime"],
    "everything": ["voidtools"],
    "Chrome": [],
    "system_good": [
        "putty",
        "chiark.greenend",
        "sabrogden/ditto",
        "iobitsmartdefrag",
        "423down.com/10540",
        "startallback",
        "423down.com/5573",
        "423down.com/12420",
        "423down.com/16859",
        "win11debloat",
        "heu_kms",
        "423down.com/1202",
        "virtualdesktopswitcher",
        "windowsbatchscriptmanager",
        "defenderui",
        "52pojie.cn/thread-965894",
        "423down.com/9655",
        "423down.com/16774",
    ],
    "notepad++": ["notepad-plus-plus", "423down.com/4966", "pythonscript"],
    "notepad--": ["notepad--", "cxasm/notepad", "gitee.com/cxasm/notepad"],
    "CCleaner": ["123pan.com/s/a6ca-e9ojh", "ccleaner"],
    "WiseCare365": ["423down.com/3471", "wisecare", "hybase.com/pc/windows/3471"],
    "EditPlus": ["editplus", "d586d0925b85"],
    "EmEditor": ["423down.com/7569", "emeditor"],
    "HiBit Startup Manager": ["hibit"],
    "SublimeText": ["sublimetext"],
    "WinRAR": ["423down.com/778", "winrar", "7xiazai.com/winrar"],
    "7-Zip": ["7-zip.org"],
    "UltraEdit": ["uestudio", "down66.com/uestudio"],
    "CrystalDiskInfo": ["423down.com/5432", "crystaldiskinfo"],
    "lx-music-desktop": [
        "lx-music-desktop",
        "lyswhut/lx-music-desktop",
        "lx-music-source",
        "lx-music-mobile",
    ],
    "typora": ["typora", "423down.com/15527", "b03v5h3sd"],
    "PotPlayer": [
        "potplayer",
        "423down.com/3050",
        "videohelp.com/software/potplayer",
        "purecodec",
        "423down.com/10813",
    ],
    "gh-release-fetch": [],
}

DOMAIN_LABELS = {
    "423down.com": "423down",
    "www.423down.com": "423down",
    "github.com": "github",
    "ghxi.com": "ghxi",
    "www.ghxi.com": "ghxi",
    "7xiazai.com": "7xiazai",
    "www.7xiazai.com": "7xiazai",
    "hybase.com": "hybase",
    "www.hybase.com": "hybase",
    "pan.quark.cn": "quark",
    "pan.baidu.com": "baidu",
    "gitee.com": "gitee",
    "down66.com": "down66",
}


def load_sync_dirs() -> list[str]:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return list(data.get("software_dirs", {}).keys())


def domain_label(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host in DOMAIN_LABELS:
        return DOMAIN_LABELS[host]
    if host.endswith(".423down.com"):
        return "423down"
    if host.endswith(".github.com"):
        return "github"
    if "lanzou" in host or "lanzout" in host or "lanzouj" in host:
        return "lanzou"
    return host or "unknown"


def classify_url(url: str) -> tuple[str, list[str]]:
    lower = url.lower()
    matched: list[str] = []
    for name, patterns in A_PATTERNS.items():
        if not patterns:
            continue
        for pat in patterns:
            if pat in lower:
                matched.append(name)
                break
    tier = "A" if matched else "B"
    return tier, sorted(set(matched))


def build() -> dict:
    if not PAGES_FILE.exists():
        raise FileNotFoundError(f"缺少 {PAGES_FILE}，请先运行 extract_pages.bat")

    pages = [line.strip() for line in PAGES_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    sync_dirs = load_sync_dirs()

    entries = []
    tier_a: list[str] = []
    by_software: dict[str, list[str]] = {k: [] for k in sync_dirs}

    for url in pages:
        tier, software = classify_url(url)
        domain = domain_label(url)
        item = {"url": url, "tier": tier, "software": software, "domain": domain}
        entries.append(item)
        if tier == "A":
            tier_a.append(url)
            for name in software:
                if name in by_software:
                    by_software[name].append(url)

    unmapped_a = [name for name in sync_dirs if name not in A_PATTERNS]
    no_url_a = [name for name in sync_dirs if not by_software.get(name)]

    result = {
        "built_at": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sync_dirs": sync_dirs,
        "stats": {
            "total_pages": len(pages),
            "tier_a_pages": len(tier_a),
            "tier_b_pages": len(pages) - len(tier_a),
            "no_url_sync_dirs": no_url_a,
        },
        "by_software": {k: v for k, v in by_software.items() if v},
        "entries": entries,
    }

    WATCHLIST.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    TIER_A_FILE.write_text("\n".join(tier_a) + ("\n" if tier_a else ""), encoding="utf-8")

    meta = {e["url"]: {"tier": e["tier"], "software": e["software"], "domain": e["domain"]} for e in entries}
    URL_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


def load_url_meta() -> dict:
    if URL_META.exists():
        return json.loads(URL_META.read_text(encoding="utf-8"))
    build()
    return json.loads(URL_META.read_text(encoding="utf-8"))


def main() -> None:
    result = build()
    stats = result["stats"]
    print(f"同步目录(A 类来源): {len(result['sync_dirs'])} 个")
    print(f"页面总数: {stats['total_pages']}")
    print(f"A 类监控页: {stats['tier_a_pages']}")
    print(f"B 类参考页: {stats['tier_b_pages']}")
    print(f"已写入: {WATCHLIST.name}, {TIER_A_FILE.name}, {URL_META.name}")
    if stats["no_url_sync_dirs"]:
        print("以下 sync 目录在页面清单中无匹配 URL（正常，可能无网页或仅直链）:")
        for name in stats["no_url_sync_dirs"]:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
