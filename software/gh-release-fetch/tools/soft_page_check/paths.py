"""soft_page_check 工作区路径解析（兼容 tools/soft_page_check 与旧版平铺目录）。"""
from __future__ import annotations

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def workspace_root() -> Path:
    if env := os.environ.get("SOFT_PAGE_CHECK_ROOT"):
        return Path(env).expanduser().resolve()
    for base in (HERE.parent.parent.parent, HERE.parent.parent):
        if (base / "apps").is_dir() or (base / "Lastb_soft_version.txt").is_file():
            return base
    return HERE.parent.parent


def lastb_soft_version_path() -> Path | None:
    if env := os.environ.get("LASTB_SOFT_VERSION"):
        p = Path(env).expanduser()
        return p.resolve() if p.is_file() else None
    for base in (workspace_root(), HERE.parent.parent, HERE.parent.parent.parent):
        p = (base / "Lastb_soft_version.txt").resolve()
        if p.is_file():
            return p
    return None


def config_json_path() -> Path | None:
    if env := os.environ.get("SOFT_PAGE_CHECK_CONFIG"):
        p = Path(env).expanduser()
        return p.resolve() if p.is_file() else None
    for base in (workspace_root(), HERE.parent.parent):
        p = (base / "config.json").resolve()
        if p.is_file():
            return p
    return None


def gh_release_fetch_root() -> Path:
    """gh-release-fetch 本体目录（本仓库根目录，或旧版 software/gh-release-fetch 嵌套）。"""
    if env := os.environ.get("GH_RELEASE_FETCH_ROOT"):
        return Path(env).expanduser().resolve()
    root = workspace_root()
    if (root / "apps").is_dir() and (root / "auto_update.py").is_file():
        return root
    legacy = root / "software" / "gh-release-fetch"
    if legacy.is_dir() and (legacy / "auto_update.py").is_file():
        return legacy
    return root
