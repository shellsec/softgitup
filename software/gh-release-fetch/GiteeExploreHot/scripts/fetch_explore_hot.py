#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同步 GiteeExploreHot 目录数据：

1) 读取 catalog/*.json（分类清单，每条至少含 id、repo_path；可选 简介、分类、attachment_filter）
2) 若无分片，则回退读取 data/curated_paths.txt（每行 owner/repo，分类记为「未分类」）
3) 调用 Gitee Open API：
   - GET /api/v5/repos/{owner}/{repo}  → 写入 data/hot_repos.json（Star 等元数据）
   - GET /api/v5/repos/{owner}/{repo}/releases/latest → 解析附件 → 写入 data/gitee_downloads.json
     （按附件名启发式归类 windows / darwin / linux，便于本目录 gitee_download.py 拉取）

环境变量 GITEE_ACCESS_TOKEN（或 GITEE_TOKEN）可显著降低 403 频控概率。

可选：--html-file 传入另存的 explore 页面 HTML，仅用于补充「额外」仓库路径（仍写入 curated 兼容逻辑）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore[misc, assignment]

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(UA)
    return s


def _api_params() -> dict[str, str]:
    tok = (os.environ.get("GITEE_ACCESS_TOKEN") or os.environ.get("GITEE_TOKEN") or "").strip()
    return {"access_token": tok} if tok else {}


def _repo_path_from_href(href: str) -> str | None:
    from urllib.parse import urljoin, urlparse

    if not href or href.startswith("#"):
        return None
    p = urlparse(href if href.startswith("http") else urljoin("https://gitee.com/", href))
    path = p.path.strip("/")
    parts = path.split("/")
    if len(parts) != 2:
        return None
    owner, name = parts
    if owner in ("explore", "help", "login", "oauth", "enterprises", "groups", "mirrors"):
        return None
    return f"{owner}/{name}"


def parse_saved_explore_html(html: str) -> list[str]:
    from urllib.parse import urljoin, urlparse

    if not BeautifulSoup:
        return []
    soup = BeautifulSoup(html, "html.parser")
    out: list[str] = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        rp = _repo_path_from_href(a["href"])
        if rp and rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out


def load_curated_paths(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []
    lines: list[str] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = line.split("#", 1)[0].strip()
            if "/" in line:
                lines.append(line)
    return lines


def load_catalog_entries(catalog_dir: str) -> list[dict[str, Any]]:
    if not os.path.isdir(catalog_dir):
        return []
    out: list[dict[str, Any]] = []
    for fn in sorted(os.listdir(catalog_dir)):
        if not fn.endswith(".json"):
            continue
        fp = os.path.join(catalog_dir, fn)
        with open(fp, encoding="utf-8") as f:
            arr = json.load(f)
        if not isinstance(arr, list):
            continue
        for row in arr:
            if not isinstance(row, dict):
                continue
            row = dict(row)
            row["_shard"] = fn
            out.append(row)
    return out


def entries_from_curated(paths: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in paths:
        parts = p.split("/")
        rid = parts[-1].replace(".", "-") if parts else p.replace("/", "-")
        rows.append(
            {
                "id": rid,
                "repo_path": p,
                "简介": "",
                "分类": "未分类",
                "_shard": "curated_paths.txt",
            }
        )
    return rows


def fetch_repo_meta(s: requests.Session, path: str, params: dict[str, str]) -> dict[str, Any] | None:
    r = s.get(f"https://gitee.com/api/v5/repos/{path}", params=params or None, timeout=40)
    if r.status_code != 200:
        return None
    j = r.json()
    return {
        "path": path,
        "url": j.get("html_url") or f"https://gitee.com/{path}",
        "name": j.get("name"),
        "full_name": j.get("full_name"),
        "description": j.get("description") or "",
        "language": j.get("language"),
        "stargazers_count": int(j.get("stargazers_count") or 0),
        "forks_count": int(j.get("forks_count") or 0),
        "watchers_count": int(j.get("watchers_count") or 0),
        "open_issues_count": int(j.get("open_issues_count") or 0),
        "license": (j.get("license") or {}) if isinstance(j.get("license"), dict) else {},
        "updated_at": j.get("updated_at"),
    }


def fetch_latest_release(
    s: requests.Session, path: str, params: dict[str, str]
) -> tuple[dict[str, Any] | None, str | None]:
    r = s.get(
        f"https://gitee.com/api/v5/repos/{path}/releases/latest",
        params=params or None,
        timeout=40,
    )
    if r.status_code == 404:
        return None, "无 latest Release（404）"
    if r.status_code != 200:
        return None, f"releases/latest HTTP {r.status_code}"
    try:
        return r.json(), None
    except Exception as e:
        return None, str(e)


def _attachments_from_release(rel: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for key in ("assets", "attach_files", "attachments"):
        for it in rel.get(key) or []:
            if not isinstance(it, dict):
                continue
            nm = (it.get("name") or it.get("filename") or "").strip()
            url = (
                it.get("browser_download_url")
                or it.get("direct_asset_url")
                or it.get("download_url")
                or it.get("url")
                or ""
            ).strip()
            if not nm or not url:
                continue
            if url.startswith("/"):
                url = "https://gitee.com" + url
            sig = (nm, url)
            if sig in seen:
                continue
            seen.add(sig)
            pairs.append((nm, url))
    return pairs


def _heuristic_platform(filename: str) -> str | None:
    n = filename.lower()
    if n.endswith((".exe", ".msi")) or "win64" in n or "win32" in n or "windows" in n:
        return "windows"
    if n.endswith((".dmg", ".pkg")) or "darwin" in n or "macos" in n or "osx" in n:
        return "darwin"
    if n.endswith((".deb", ".rpm", ".appimage")):
        return "linux"
    if n.endswith((".tar.gz", ".tgz", ".zip")):
        if any(x in n for x in ("win", "windows", "msvc")) and "darwin" not in n:
            return "windows"
        if any(x in n for x in ("darwin", "macosx", "macos", "apple")):
            return "darwin"
        if "linux" in n or "manylinux" in n or "ubuntu" in n:
            return "linux"
    return None


def _match_rule(filename: str, rule: dict[str, Any] | None) -> bool:
    if not rule:
        return True
    n = filename.lower()
    for s in rule.get("must_include", []) or []:
        if str(s).lower() not in n:
            return False
    for s in rule.get("must_not_include", []) or []:
        if str(s).lower() in n:
            return False
    return True


def pick_platform_downloads(
    entry: dict[str, Any], attachments: list[tuple[str, str]]
) -> tuple[dict[str, dict[str, str] | None], list[dict[str, str]]]:
    """返回 (downloads windows/darwin/linux, other_assets 未入选附件)。"""
    filt: dict[str, Any] = entry.get("attachment_filter") or {}
    buckets: dict[str, list[tuple[str, str]]] = {"windows": [], "darwin": [], "linux": []}

    for name, url in attachments:
        plat: str | None = None
        for p in ("windows", "darwin", "linux"):
            rule = filt.get(p)
            if rule and _match_rule(name, rule):
                plat = p
                break
        if plat is None:
            plat = _heuristic_platform(name)
        if plat and _match_rule(name, filt.get(plat)):
            buckets[plat].append((name, url))

    def best(cands: list[tuple[str, str]]) -> dict[str, str] | None:
        if not cands:
            return None
        cands = sorted(cands, key=lambda x: x[0])
        name, url = cands[0]
        return {"url": url, "filename": os.path.basename(name.split("?", 1)[0])}

    downloads: dict[str, dict[str, str] | None] = {
        "windows": best(buckets["windows"]),
        "darwin": best(buckets["darwin"]),
        "linux": best(buckets["linux"]),
    }
    chosen = {d["url"] for d in downloads.values() if d}
    other: list[dict[str, str]] = []
    for name, url in sorted(attachments):
        if url not in chosen:
            other.append({"name": name, "url": url})
    return downloads, other[:80]


def main() -> int:
    ap = argparse.ArgumentParser(description="同步 Gitee catalog → hot_repos.json + gitee_downloads.json")
    ap.add_argument(
        "--catalog-dir",
        default="",
        help="分类 JSON 目录（默认：<包根>/catalog）",
    )
    ap.add_argument(
        "--curated-file",
        default="",
        help="无 catalog 时使用的每行 owner/repo 列表（默认：<包根>/data/curated_paths.txt）",
    )
    ap.add_argument(
        "--html-file",
        default="",
        help="可选：另存的 explore HTML，补充额外仓库路径",
    )
    ap.add_argument(
        "--out-hot",
        default="",
        help="hot_repos 输出路径（默认：<包根>/data/hot_repos.json）",
    )
    ap.add_argument(
        "--out-downloads",
        default="",
        help="下载索引输出路径（默认：<包根>/data/gitee_downloads.json）",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=0.45,
        help="每个仓库两次 API 之间的间隔（秒），缓解频控",
    )
    args = ap.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(script_dir, ".."))
    catalog_dir = args.catalog_dir.strip() or os.path.join(root, "catalog")
    curated = args.curated_file.strip() or os.path.join(root, "data", "curated_paths.txt")
    out_hot = args.out_hot.strip() or os.path.join(root, "data", "hot_repos.json")
    out_dl = args.out_downloads.strip() or os.path.join(root, "data", "gitee_downloads.json")
    os.makedirs(os.path.dirname(out_hot), exist_ok=True)
    os.makedirs(os.path.dirname(out_dl), exist_ok=True)

    entries = load_catalog_entries(catalog_dir)
    extra_paths = load_curated_paths(curated)
    if args.html_file.strip():
        try:
            with open(args.html_file.strip(), encoding="utf-8") as f:
                for rp in parse_saved_explore_html(f.read()):
                    if rp not in extra_paths:
                        extra_paths.append(rp)
        except OSError as e:
            print("WARN: html-file:", e, file=sys.stderr)
    if not entries:
        entries = entries_from_curated(extra_paths)
    else:
        for p in extra_paths:
            if not any((e.get("repo_path") or "").strip() == p for e in entries):
                parts = p.split("/")
                rid = parts[-1].replace(".", "-") if parts else p.replace("/", "-")
                entries.append(
                    {
                        "id": rid,
                        "repo_path": p,
                        "简介": "（来自 curated_paths.txt 追加）",
                        "分类": "未分类",
                        "_shard": "curated_paths.txt",
                    }
                )

    if not entries:
        print("ERR: 无仓库条目（请配置 catalog/*.json 或 data/curated_paths.txt）", file=sys.stderr)
        return 1

    s = _session()
    params = _api_params()
    delay = max(0.0, float(args.sleep))

    hot_rows: list[dict[str, Any]] = []
    dl_items: list[dict[str, Any]] = []
    missing_meta: list[str] = []

    for i, ent in enumerate(entries):
        rid = (ent.get("id") or "").strip()
        rp = (ent.get("repo_path") or "").strip()
        if not rid or not rp:
            continue

        meta = fetch_repo_meta(s, rp, params)
        if not meta:
            missing_meta.append(rp)
            hot_rows.append(
                {
                    "path": rp,
                    "url": f"https://gitee.com/{rp}",
                    "id": rid,
                    "repo_path": rp,
                    "简介": ent.get("简介") or "",
                    "分类": ent.get("分类") or "未分类",
                    "catalog_shard": ent.get("_shard", ""),
                    "error": "repos API 失败（检查频控或令牌）",
                }
            )
        else:
            row = {
                **meta,
                "id": rid,
                "简介": ent.get("简介") or "",
                "分类": ent.get("分类") or "未分类",
                "catalog_shard": ent.get("_shard", ""),
            }
            hot_rows.append(row)

        if delay:
            time.sleep(min(0.35, max(0.15, delay / 2)))
        rel, rel_err = fetch_latest_release(s, rp, params)
        att = _attachments_from_release(rel) if rel else []
        downloads, other_assets = pick_platform_downloads(ent, att)
        dl_items.append(
            {
                "id": rid,
                "repo_path": rp,
                "简介": ent.get("简介") or "",
                "分类": ent.get("分类") or "未分类",
                "catalog_shard": ent.get("_shard", ""),
                "tag": (rel or {}).get("tag_name") if rel else None,
                "release_name": (rel or {}).get("name") if rel else None,
                "downloads": downloads,
                "other_assets": other_assets,
                "attachments_count": len(att),
                "error": rel_err,
            }
        )

        if delay and i < len(entries) - 1:
            time.sleep(delay)

    hot_rows.sort(
        key=lambda x: int(x.get("stargazers_count") or 0) if "stargazers_count" in x else -1,
        reverse=True,
    )

    hot_doc = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reference": "https://gitee.com/explore",
        "catalog_dir": os.path.normpath(catalog_dir),
        "count": len(hot_rows),
        "repos": hot_rows,
        "missing_repo_api": missing_meta,
    }
    with open(out_hot, "w", encoding="utf-8") as f:
        json.dump(hot_doc, f, ensure_ascii=False, indent=2)

    dl_doc = {
        "schema": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reference": "https://gitee.com/api/v5/repos/*/releases/latest",
        "count": len(dl_items),
        "items": dl_items,
    }
    with open(out_dl, "w", encoding="utf-8") as f:
        json.dump(dl_doc, f, ensure_ascii=False, indent=2)

    print("Wrote", out_hot, "repos", len(hot_rows), "missing_meta", len(missing_meta))
    print("Wrote", out_dl, "download_items", len(dl_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
