# -*- coding: utf-8 -*-
"""仓库根目录与 exe / .py 双模式调用解析（PyInstaller frozen）。"""
from __future__ import annotations

import os
import sys


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def repo_root(from_file: str | None = None) -> str:
    """配置与 JSON 所在目录：frozen 时为 exe 同目录，否则为仓库根。"""
    if is_frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    if from_file:
        path = os.path.abspath(from_file)
        if os.path.basename(path).startswith("run_saved") or path.replace("\\", "/").endswith("/tools/run_saved_apps.py"):
            return os.path.dirname(os.path.dirname(path))
        return os.path.dirname(path)
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def resolve_auto_update_argv(root: str, extra: list[str] | None = None) -> list[str]:
    """构造调用 auto_update 的 argv（不含 python 时用 exe）。"""
    extra = extra or []
    exe = os.path.join(root, "auto_update.exe")
    if os.path.isfile(exe):
        return [exe, *extra]
    py = os.path.join(root, "auto_update.py")
    if os.path.isfile(py):
        return [sys.executable, py, *extra]
    raise FileNotFoundError("未找到 auto_update.exe 或 auto_update.py（目录: %s）" % root)


def resolve_python_script_argv(root: str, rel_py: str, extra: list[str] | None = None) -> list[str]:
    """调用仓库内 .py 脚本；frozen 且无 Python 时仅支持已打包的同名 exe。"""
    extra = extra or []
    base = os.path.splitext(os.path.basename(rel_py))[0]
    exe = os.path.join(root, base + ".exe")
    if os.path.isfile(exe):
        return [exe, *extra]
    py = os.path.join(root, rel_py.replace("/", os.sep))
    if os.path.isfile(py):
        return [sys.executable, py, *extra]
    raise FileNotFoundError("未找到 %s 或 %s" % (exe, py))
