#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扫描 apps / apps-mobile 中的 id 重复、格式、空 id。"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_PAT = re.compile(r"^[a-z][a-z0-9_]*$")


def scan_dir(base: str, plat: str) -> list[tuple]:
    issues: list[tuple] = []
    d = os.path.join(base, plat)
    if not os.path.isdir(d):
        return issues
    by_id: dict[str, list] = defaultdict(list)
    by_repo: dict[str, list] = defaultdict(list)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(d, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            issues.append(("PARSE", plat, fn, str(e)))
            continue
        if not isinstance(data, list):
            issues.append(("NOT_LIST", plat, fn))
            continue
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                issues.append(("NOT_DICT", plat, fn, i))
                continue
            aid = (item.get("id") or "").strip()
            rp = (item.get("repo_path") or "").strip()
            if not aid:
                issues.append(("EMPTY_ID", plat, fn, i, rp))
                continue
            if not ID_PAT.match(aid):
                issues.append(("BAD_FORMAT", plat, fn, aid, rp))
            by_id[aid].append((fn, rp))
            if rp:
                by_repo[rp.lower()].append((fn, aid))
    for aid, locs in sorted(by_id.items()):
        if len(locs) > 1:
            issues.append(("DUP_ID", plat, aid, locs))
    for rp, locs in sorted(by_repo.items()):
        if len(locs) > 1:
            issues.append(("DUP_REPO", plat, rp, locs))
    return issues


def main() -> int:
    all_issues: list[tuple] = []
    for plat in ("windows", "darwin", "linux"):
        all_issues.extend(scan_dir(os.path.join(ROOT, "apps"), plat))
    for plat in ("android", "ios"):
        all_issues.extend(scan_dir(os.path.join(ROOT, "apps-mobile"), plat))

    print(f"=== 共 {len(all_issues)} 项问题 ===\n")
    by_kind: dict[str, list] = defaultdict(list)
    for row in all_issues:
        by_kind[row[0]].append(row)

    for kind in (
        "DUP_ID",
        "DUP_REPO",
        "BAD_FORMAT",
        "EMPTY_ID",
        "PARSE",
        "NOT_LIST",
        "NOT_DICT",
    ):
        rows = by_kind.get(kind, [])
        if not rows:
            continue
        print(f"--- {kind} ({len(rows)}) ---")
        for row in rows:
            print("  ", " | ".join(str(x) for x in row[1:]))
        print()

    dup_ids = by_kind.get("DUP_ID", [])
    # same id -> different repo on one platform
    for plat in ("windows", "darwin", "linux"):
        id_repo: dict[str, str] = {}
        collisions: list[tuple] = []
        d = os.path.join(ROOT, "apps", plat)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".json"):
                continue
            for item in json.load(open(os.path.join(d, fn), encoding="utf-8")):
                if not isinstance(item, dict):
                    continue
                aid = (item.get("id") or "").strip()
                rp = (item.get("repo_path") or "").strip().lower()
                if not aid or not rp:
                    continue
                prev = id_repo.get(aid)
                if prev and prev != rp:
                    collisions.append((plat, aid, prev, rp, fn))
                else:
                    id_repo[aid] = rp
        if collisions:
            print(f"--- ID_REPO_COLLISION ({plat}, {len(collisions)}) ---")
            for row in collisions:
                print("  ", " | ".join(row))
            print()

    return 1 if dup_ids else 0


if __name__ == "__main__":
    sys.exit(main())
