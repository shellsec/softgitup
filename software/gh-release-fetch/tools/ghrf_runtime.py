# -*- coding: utf-8 -*-
"""仓库根目录与 exe / .py 双模式调用解析（PyInstaller frozen）。"""
from __future__ import annotations

import os
import shlex
import sys


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def repo_root(from_file: str | None = None) -> str:
    """配置与 JSON 所在目录：frozen 时为 exe 同目录，否则为仓库根。"""
    if is_frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    if from_file:
        path = os.path.abspath(from_file)
        norm = path.replace("\\", "/")
        if os.path.basename(path).startswith("run_saved") or norm.endswith("/tools/run_saved_apps.py"):
            return os.path.dirname(os.path.dirname(path))
        if norm.endswith("/tools/soft_page_check/search_pages.py"):
            return os.path.dirname(os.path.dirname(os.path.dirname(path)))
        return os.path.dirname(path)
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def soft_page_check_dir(from_file: str | None = None) -> str:
    return os.path.join(repo_root(from_file), "tools", "soft_page_check")


def prompt_cli_line(
    usage_lines: list[str],
    prompt: str,
    *,
    allow_empty: bool = False,
) -> str | None:
    """无命令行参数时展示用法并读一行；取消或空输入返回 None。"""
    for line in usage_lines:
        print(line)
    print()
    try:
        text = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return None
    if not text:
        if allow_empty:
            return ""
        print("未输入，已退出。")
        return None
    return text


def argv_from_prompt(
    usage_lines: list[str],
    prompt: str,
) -> bool:
    """
    若 sys.argv 仅有程序名，则提示输入并 shlex 拆入 sys.argv。
    返回 False 表示用户取消或空输入（调用方应 exit 0）。
    """
    if len(sys.argv) > 1:
        return True
    text = prompt_cli_line(usage_lines, prompt)
    if text is None:
        return False
    sys.argv[1:] = shlex.split(text, posix=(os.name != "nt"))
    return True


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
