#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据 fetch_explore_hot.py 生成的 data/gitee_downloads.json，按平台下载「已归类」附件。

示例：
  python GiteeExploreHot/scripts/gitee_download.py --platform windows
  python GiteeExploreHot/scripts/gitee_download.py --platform linux --id nacos

下载目录优先读 GiteeExploreHot/root.json 的 download_dir（相对路径以本包根目录为基准）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import requests

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}


def _load_root(root_path: str) -> dict:
    if not os.path.isfile(root_path):
        return {}
    with open(root_path, encoding="utf-8") as f:
        return json.load(f)


def _download(url: str, dest: str, verify: bool) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with requests.get(url, headers=UA, stream=True, timeout=120, verify=verify) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)


def main() -> int:
    ap = argparse.ArgumentParser(description="从 gitee_downloads.json 按平台下载附件")
    ap.add_argument(
        "--index",
        default="",
        help="gitee_downloads.json 路径（默认：<包根>/data/gitee_downloads.json）",
    )
    ap.add_argument(
        "--platform",
        required=True,
        choices=("windows", "darwin", "linux"),
        help="下载 downloads 下对应平台的条目（若该条目为 null 则跳过）",
    )
    ap.add_argument("--id", default="", help="仅下载指定 id（默认可下载全部有链接的）")
    ap.add_argument(
        "--insecure",
        action="store_true",
        help="关闭 TLS 校验（不推荐）",
    )
    args = ap.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(script_dir, ".."))
    index_path = args.index.strip() or os.path.join(root, "data", "gitee_downloads.json")
    if not os.path.isfile(index_path):
        print("ERR: 找不到索引文件:", index_path, file=sys.stderr)
        return 1

    root_cfg = _load_root(os.path.join(root, "root.json"))
    dl_root = (root_cfg.get("download_dir") or "downloads/GiteeExploreHot").strip()
    if not os.path.isabs(dl_root):
        dl_root = os.path.normpath(os.path.join(root, dl_root))
    verify = bool(root_cfg.get("ssl_verify", True)) and (not args.insecure)

    with open(index_path, encoding="utf-8") as f:
        doc = json.load(f)
    plat = args.platform
    want_id = (args.id or "").strip()

    n_ok, n_skip = 0, 0
    for it in doc.get("items") or []:
        rid = (it.get("id") or "").strip()
        if want_id and rid != want_id:
            continue
        blk = (it.get("downloads") or {}).get(plat)
        if not blk or not (blk.get("url") or "").strip():
            n_skip += 1
            continue
        url = blk["url"].strip()
        fname = (blk.get("filename") or os.path.basename(url.split("?", 1)[0])).strip()
        dest = os.path.join(dl_root, plat, rid, fname)
        try:
            print("GET", url[:80], "->", dest)
            _download(url, dest, verify=verify)
            n_ok += 1
        except Exception as e:
            print("ERR", rid, e, file=sys.stderr)
    print("done ok", n_ok, "skip_no_url", n_skip)
    return 0 if n_ok or not want_id else 1


if __name__ == "__main__":
    raise SystemExit(main())
