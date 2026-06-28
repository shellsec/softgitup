#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
游戏频道搜索：在 gamer520 标题快照中检索并打开链接（不自动下载）。

底层与 search_pages.py 相同，默认 --scope gamer520，索引仅加载游戏 scope。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tools.ghrf_runtime import argv_from_prompt  # noqa: E402

import search_pages as sp  # noqa: E402

GAME_SCOPES = frozenset({"gamer520"})
DEFAULT_SCOPE = "gamer520"

USAGE_LINES = [
    "用法: search_games [选项与关键词...]",
    "示例: search_games 艾尔登",
    "      search_games --open 黑神话",
    "      search_games --stats",
    "",
    "搜索 gamer520 等游戏频道介绍页标题并打开链接（不自动下载）。",
    "开源软件 GitHub 下载请用 lookup_app；工具介绍页请用 search_soft_pages。",
]


def _ensure_default_scope(argv: list[str]) -> list[str]:
    if any(a == "--scope" or a.startswith("--scope=") for a in argv[1:]):
        return argv
    return argv[:1] + ["--scope", DEFAULT_SCOPE] + argv[1:]


def main() -> int:
    sys.argv = _ensure_default_scope(sys.argv)
    if not argv_from_prompt(USAGE_LINES, "请输入游戏名（可含 --open 等）: "):
        return 0
    return sp.run_search(
        default_scope=DEFAULT_SCOPE,
        index_scopes=GAME_SCOPES,
    )


if __name__ == "__main__":
    raise SystemExit(main())
