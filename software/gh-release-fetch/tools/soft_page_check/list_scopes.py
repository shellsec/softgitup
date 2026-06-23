"""list/ 站点 scope 定义：系统 / 移动分开监控与比对。"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
LIST_DIR = HERE / "list"

# 每个站点在报告页合并为一个分组，内含 system + mobile 两个子 scope
LIST_SITE_GROUPS: list[dict] = [
    {
        "id": "hybase",
        "title": "hybase",
        "desc": "黑域 bases soft/newlist · 系统与移动分开比对",
        "accent": "#0891b2",
        "scopes": ["hybase_system", "hybase_mobile"],
    },
    {
        "id": "dayanzai",
        "title": "dayanzai",
        "desc": "大眼仔 · PC 与 Android 分开比对",
        "accent": "#db2777",
        "scopes": ["dayanzai_system", "dayanzai_mobile"],
    },
    {
        "id": "down66",
        "title": "down66",
        "desc": "软仓 · PC 与 Android app 分开比对",
        "accent": "#ca8a04",
        "scopes": ["down66_system", "down66_mobile"],
    },
    {
        "id": "7xiazai",
        "title": "7xiazai",
        "desc": "小兵下载站 · PC 与 Android 分开比对",
        "accent": "#7c3aed",
        "scopes": ["7xiazai_system", "7xiazai_mobile"],
    },
]

LIST_SCOPE_DEFS: dict[str, dict] = {
    "hybase_system": {
        "url_file": LIST_DIR / "hybase_newlist_urls_system.txt",
        "hint": "list/hybase_newlist_urls_system.txt",
        "site": "hybase",
        "platform": "system",
        "title": "系统",
        "subtitle": "PC/Windows · 系统镜像（约 358 条）",
        "accent": "#0e7490",
        "optional": False,
    },
    "hybase_mobile": {
        "url_file": LIST_DIR / "hybase_newlist_urls_mobile.txt",
        "hint": "list/hybase_newlist_urls_mobile.txt",
        "site": "hybase",
        "platform": "mobile",
        "title": "移动",
        "subtitle": "Android · TV（约 242 条）",
        "accent": "#06b6d4",
        "optional": False,
    },
    "dayanzai_system": {
        "url_file": LIST_DIR / "dayanzai_system_urls.txt",
        "hint": "list/dayanzai_system_urls.txt",
        "site": "dayanzai",
        "platform": "system",
        "title": "系统",
        "subtitle": "dayanzai.me 首页 PC/教程等（约 2936 条，已排除 android 清单）",
        "accent": "#be185d",
        "optional": False,
    },
    "dayanzai_mobile": {
        "url_file": LIST_DIR / "dayanzai_android_urls.txt",
        "hint": "list/dayanzai_android_urls.txt",
        "site": "dayanzai",
        "platform": "mobile",
        "title": "移动",
        "subtitle": "dayanzai.me/android（约 262 条）",
        "accent": "#ec4899",
        "optional": False,
    },
    "down66_system": {
        "url_file": LIST_DIR / "down66_system_urls.txt",
        "hint": "list/down66_system_urls.txt",
        "site": "down66",
        "platform": "system",
        "title": "系统",
        "subtitle": "down66.com/pc（约 357 条，已排除 app 清单）",
        "accent": "#a16207",
        "optional": False,
    },
    "down66_mobile": {
        "url_file": LIST_DIR / "down66_app_urls.txt",
        "hint": "list/down66_app_urls.txt",
        "site": "down66",
        "platform": "mobile",
        "title": "移动",
        "subtitle": "down66.com/app Android（约 226 条）",
        "accent": "#eab308",
        "optional": False,
    },
    "7xiazai_system": {
        "url_file": LIST_DIR / "7xiazai_list_urls_system.txt",
        "hint": "list/7xiazai_list_urls_system.txt",
        "site": "7xiazai",
        "platform": "system",
        "title": "系统",
        "subtitle": "7xiazai.com PC/Windows 等（约 442 条）",
        "accent": "#6d28d9",
        "optional": False,
    },
    "7xiazai_mobile": {
        "url_file": LIST_DIR / "7xiazai_list_urls_mobile.txt",
        "hint": "list/7xiazai_list_urls_mobile.txt",
        "site": "7xiazai",
        "platform": "mobile",
        "title": "移动",
        "subtitle": "7xiazai.com Android/TV 等（约 226 条）",
        "accent": "#a855f7",
        "optional": False,
    },
}

# 旧 scope 名 → 拆成 system + mobile 依次执行
LEGACY_LIST_SCOPES: dict[str, list[str]] = {
    "hybase": ["hybase_system", "hybase_mobile"],
    "dayanzai": ["dayanzai_system", "dayanzai_mobile"],
    "down66": ["down66_system", "down66_mobile"],
    "7xiazai": ["7xiazai_system", "7xiazai_mobile"],
}

LIST_SCOPE_KEYS = list(LIST_SCOPE_DEFS.keys())
EXTERNAL_LIST_SCOPES = frozenset(LIST_SCOPE_KEYS)


def is_list_scope(scope: str) -> bool:
    return scope in LIST_SCOPE_DEFS


def scope_label(scope: str) -> str:
    if scope in LIST_SCOPE_DEFS:
        d = LIST_SCOPE_DEFS[scope]
        return f"{d['site']} · {d['title']}"
    return scope


def changed_list_filename(scope: str) -> str:
    return f"changed_{scope}_urls.txt"


def build_report_meta(scope: str) -> dict:
    d = LIST_SCOPE_DEFS[scope]
    return {
        "id": scope,
        "site": d["site"],
        "platform": d["platform"],
        "title": f"{d['site']} · {d['title']}",
        "desc": d.get("subtitle", ""),
        "snapshot": f"titles_latest_{scope.upper()}.json",
        "diff": f"last_diff_{scope}.json",
        "changed_txt": changed_list_filename(scope),
        "accent": d.get("accent", "#64748b"),
    }


def read_url_list(path: Path) -> list[str]:
    if not path.exists():
        return []
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls
