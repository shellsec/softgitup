#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""删除 soft_page_check 可再生的历史快照与旧文本报告。"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HISTORY = HERE / "history"
REPORTS = HERE / "reports"
DATED = re.compile(r"^titles_.+_\d{4}-\d{2}-\d{2}_\d{6}\.json$", re.I)


def main() -> int:
    dry = "--dry-run" in sys.argv
    removed = 0
    freed = 0

    for p in HISTORY.glob("titles_*.json"):
        if p.name.startswith("titles_latest_"):
            continue
        if DATED.match(p.name):
            freed += p.stat().st_size
            removed += 1
            if not dry:
                p.unlink()

    for p in REPORTS.glob("report_*.txt"):
        freed += p.stat().st_size
        removed += 1
        if not dry:
            p.unlink()

    cache = HERE / "__pycache__"
    if cache.is_dir():
        n = sum(1 for _ in cache.rglob("*") if _.is_file())
        if not dry:
            shutil.rmtree(cache)
        removed += n

    legacy = HERE / "changed_7xiazai_urls.txt"
    if legacy.is_file():
        freed += legacy.stat().st_size
        removed += 1
        if not dry:
            legacy.unlink()

    mode = "dry-run" if dry else "已删除"
    print(f"{mode}: {removed} 项，约 {freed / 1024 / 1024:.2f} MB")
    print("保留: history/titles_latest_*.json、reports/index.html、reports/last_diff_*.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
