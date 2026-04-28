#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VibeCodingToolsDown 独立入口：调用主仓库的 auto_update.py，并固定 --apps-dir 为本目录。

查找 auto_update.py 顺序：
  1) 上一级目录（与本文件夹并列，即仓库根）
  2) 本目录内（若单独复制了 auto_update.py）
"""
import os
import subprocess
import sys
from typing import Optional, Tuple


def _find_auto_update() -> Optional[Tuple[str, str]]:
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.path.dirname(here), "auto_update.py"),
        os.path.join(here, "auto_update.py"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path, os.path.dirname(path)
    return None


def main() -> int:
    found = _find_auto_update()
    if not found:
        sys.stderr.write(
            "[vibe_update] 找不到 auto_update.py。\n"
            "  方式 A：将本文件夹放在仓库根下的 VibeCodingToolsDown/（与 auto_update.py 同级目录并列）。\n"
            "  方式 B：把仓库根目录的 auto_update.py 复制到本文件夹内。\n"
        )
        return 1
    au_path, repo_root = found
    here = os.path.dirname(os.path.abspath(__file__))
    argv = [sys.executable, au_path, "--apps-dir", here, *sys.argv[1:]]
    return subprocess.call(argv, cwd=repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
