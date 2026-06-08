#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
在 apps/ 配置中模糊查找应用，显示分片与分类，并可交互开启 enabled / 加入更新列表。

用法：
  python lookup_app.py drawio
  python lookup_app.py --platform windows cherrytree
  python lookup_app.py --apps-dir VibeCodingToolsDown warp
  python lookup_app.py --yes drawio          # 匹配项全部开启，不询问
  python lookup_app.py --dry-run drawio      # 只查询，不写文件

加入更新列表（根目录 saved_apps_<平台>.json，配合 run_saved_apps.bat 一键更新）：
  python lookup_app.py cherrytree            # 交互：选序号 → 是否 enabled → 是否加入列表
  python lookup_app.py --save cherrytree     # 选中后默认加入列表（仍询问序号）
  python lookup_app.py -y --save drawio      # 全部开启并加入列表
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_APPS_DIR = os.path.join(SCRIPT_DIR, "apps")
PLATFORMS = ("windows", "darwin", "linux")
SHARD_RE = re.compile(r"^\d+-(.+)\.json$", re.UNICODE)

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
from tools.app_list import (  # noqa: E402
    default_list_basename,
    default_list_path,
    save_hits_by_platform,
)


def _dump(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def discover_shard_files(apps_dir: str) -> list[tuple[str, str]]:
    """返回 [(platform, abspath), ...]"""
    out: list[tuple[str, str]] = []
    for plat in PLATFORMS:
        sub = os.path.join(apps_dir, plat)
        if os.path.isdir(sub):
            for name in sorted(os.listdir(sub)):
                if name.endswith(".json"):
                    out.append((plat, os.path.join(sub, name)))
            continue
        single = os.path.join(apps_dir, "%s.json" % plat)
        if os.path.isfile(single):
            out.append((plat, single))
    return out


def shard_label_from_filename(filename: str) -> str:
    m = SHARD_RE.match(filename)
    return m.group(1) if m else ""


def load_apps_array(abspath: str) -> list:
    with open(abspath, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "apps" in data:
        data = data["apps"]
    if not isinstance(data, list):
        raise ValueError("%s：必须是 JSON 数组" % abspath)
    return data


def match_score(query: str, app: dict) -> int:
    q = query.strip().lower()
    if not q:
        return 0
    parts = [q]
    if " " in q:
        parts.extend(p for p in q.split() if p)

    best = 0
    idv = (app.get("id") or "").lower()
    fields = [
        idv,
        (app.get("简介") or "").lower(),
        (app.get("分类") or "").lower(),
        (app.get("repo_path") or "").lower(),
        (app.get("releases_url") or "").lower(),
        (app.get("url_hint") or "").lower(),
    ]
    for token in parts:
        if idv == token:
            best = max(best, 100)
        elif idv.startswith(token):
            best = max(best, 80)
        elif token in idv:
            best = max(best, 60)
        for text in fields[1:]:
            if token in text:
                best = max(best, 40)
    return best


def search_apps(apps_dir: str, query: str, min_score: int = 40) -> list[dict]:
    hits: list[dict] = []
    for platform, abspath in discover_shard_files(apps_dir):
        rel = os.path.relpath(abspath, apps_dir).replace("\\", "/")
        shard_name = os.path.basename(abspath)
        shard_cat = shard_label_from_filename(shard_name)
        try:
            items = load_apps_array(abspath)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print("[WARN] 跳过 %s: %s" % (rel, e), file=sys.stderr)
            continue
        for app in items:
            if not isinstance(app, dict):
                continue
            score = match_score(query, app)
            if score < min_score:
                continue
            cat = (app.get("分类") or "").strip() or shard_cat or "(未填分类)"
            hits.append(
                {
                    "score": score,
                    "platform": platform,
                    "path": rel,
                    "abspath": abspath,
                    "shard": shard_name,
                    "shard_category": shard_cat,
                    "id": (app.get("id") or "").strip(),
                    "分类": cat,
                    "enabled": app.get("enabled") is True,
                    "简介": (app.get("简介") or "").strip(),
                    "repo_path": (app.get("repo_path") or "").strip(),
                }
            )
    hits.sort(key=lambda h: (-h["score"], h["platform"], h["id"]))
    return hits


def print_hits(hits: list[dict]) -> None:
    print()
    print("共 %d 条匹配：" % len(hits))
    print("-" * 72)
    for i, h in enumerate(hits, 1):
        en = "是" if h["enabled"] else "否"
        brief = h["简介"]
        if len(brief) > 56:
            brief = brief[:53] + "..."
        print("[%d] %s  id=%s  enabled=%s" % (i, h["platform"], h["id"], en))
        print("    分片: %s" % h["path"])
        print("    分类: %s" % h["分类"])
        if h["repo_path"]:
            print("    仓库: %s" % h["repo_path"])
        if brief:
            print("    简介: %s" % brief)
        print()


def set_enabled_in_file(abspath: str, app_id: str, enabled: bool) -> bool:
    items = load_apps_array(abspath)
    changed = False
    for app in items:
        if isinstance(app, dict) and (app.get("id") or "").strip() == app_id:
            if app.get("enabled") is enabled:
                continue
            app["enabled"] = enabled
            changed = True
    if changed:
        _dump(abspath, items)
    return changed


def prompt_choose_hits(hits: list[dict]) -> list[dict]:
    """让用户勾选序号，回车跳过则返回空列表。"""
    if not hits:
        return []
    print("请选择要操作的条目：")
    print("  输入序号（如 1 或 1,3）| a=全部 | 回车=跳过")
    try:
        line = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return []
    if not line:
        print("未选择。")
        return []
    if line.lower() in ("a", "all", "*"):
        return list(hits)
    indices: list[int] = []
    for part in line.replace("，", ",").split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            print("无效输入: %r" % part)
            return []
        idx = int(part)
        if idx < 1 or idx > len(hits):
            print("序号超出范围: %d" % idx)
            return []
        indices.append(idx - 1)
    return [hits[i] for i in sorted(set(indices))]


def apply_enable(chosen: list[dict], dry_run: bool) -> int:
    """对 chosen 开启 enabled，返回成功条数。"""
    n = 0
    for h in chosen:
        if h["enabled"]:
            print("[跳过] %s / %s 已是开启状态" % (h["platform"], h["id"]))
            continue
        if dry_run:
            print("[dry-run] 将开启 %s / %s → %s" % (h["platform"], h["id"], h["path"]))
            n += 1
            continue
        if set_enabled_in_file(h["abspath"], h["id"], True):
            print("[已开启] %s / %s → %s" % (h["platform"], h["id"], h["path"]))
            n += 1
        else:
            print("[失败] 未在 %s 中找到 id=%s" % (h["path"], h["id"]))
    return n


def prompt_yes_no(question: str, default_no: bool = True) -> bool:
    try:
        line = input(question).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return False
    if not line:
        return not default_no
    return line in ("y", "yes", "是", "1")


def _list_files_hint(chosen: list[dict]) -> str:
    plats = sorted({h["platform"] for h in chosen})
    names = [default_list_basename(p) for p in plats]
    return "、".join(names)


def prompt_add_to_saved_list(
    chosen: list[dict],
    apps_dir: str,
    dry_run: bool,
    *,
    auto: bool = False,
    save_path: str | None = None,
) -> bool:
    """询问是否加入根目录更新列表。"""
    if not chosen:
        return False
    hint = save_path or _list_files_hint(chosen)
    if not auto:
        print()
        print("是否加入到更新列表 %s ？" % hint)
        print("（之后可运行 run_saved_apps.bat 一键开启并更新）")
        if not prompt_yes_no("> "):
            print("未加入列表。")
            return False
    if dry_run:
        for h in chosen:
            print("[dry-run] 将加入列表 %s / %s" % (h["platform"], h["id"]))
        return True
    save_hits_by_platform(
        SCRIPT_DIR,
        chosen,
        apps_dir,
        merge=True,
        explicit_path=save_path,
    )
    return True


def run_interactive(
    hits: list[dict],
    apps_dir: str,
    dry_run: bool,
    *,
    auto_save: bool,
    ask_save: bool,
    save_path: str | None = None,
) -> None:
    chosen = prompt_choose_hits(hits)
    if not chosen:
        return

    print("\n已选 %d 条。" % len(chosen))
    if any(not h["enabled"] for h in chosen):
        if prompt_yes_no("是否设为 enabled=true？(y/n) "):
            n = apply_enable(chosen, dry_run)
            if n:
                print("共开启 %d 条。" % n)
    else:
        print("所选条目均已 enabled=true。")

    if ask_save or auto_save:
        prompt_add_to_saved_list(
            chosen, apps_dir, dry_run, auto=auto_save, save_path=save_path
        )


def enable_all_matches(hits: list[dict], dry_run: bool) -> int:
    return apply_enable(hits, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="在 apps 配置中模糊查找应用并可开启 enabled")
    parser.add_argument("query", nargs="+", help="关键词（如 drawio、v2ray）")
    parser.add_argument(
        "--apps-dir",
        default=DEFAULT_APPS_DIR,
        help="配置根目录（默认项目 apps/）",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=40,
        help="最低匹配分（默认 40）",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="对全部匹配项直接 enabled=true，不交互询问",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示结果，不写 JSON（与 --yes 联用时仅预览）",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="只查询，不交互",
    )
    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        help="只显示该平台的匹配项",
    )
    parser.add_argument(
        "--save",
        nargs="?",
        const="",
        default=None,
        metavar="FILE",
        help="将选中项加入根目录更新列表（默认 saved_apps_<平台>.json）；与 -y 联用则对全部匹配项加入",
    )
    parser.add_argument(
        "--no-save-prompt",
        action="store_true",
        help="不询问是否加入更新列表（未指定 --save 时生效）",
    )
    args = parser.parse_args()

    apps_dir = args.apps_dir
    if not os.path.isabs(apps_dir):
        apps_dir = os.path.normpath(os.path.join(SCRIPT_DIR, apps_dir))
    if not os.path.isdir(apps_dir):
        print("[ERROR] 目录不存在: %s" % apps_dir, file=sys.stderr)
        return 1

    query = " ".join(args.query).strip()
    if not query:
        parser.print_help()
        return 1

    print("检索: %r  （目录: %s）" % (query, apps_dir))
    hits = search_apps(apps_dir, query, min_score=args.min_score)
    if args.platform:
        hits = [h for h in hits if h["platform"] == args.platform]
    if not hits:
        print("未找到匹配项。可尝试更短关键词或调低 --min-score。")
        return 2

    print_hits(hits)

    save_path: str | None = None
    if args.save is not None:
        if args.save:
            save_path = args.save if os.path.isabs(args.save) else os.path.join(SCRIPT_DIR, args.save)
        elif args.platform:
            save_path = default_list_path(SCRIPT_DIR, args.platform)

    if args.no_prompt:
        if args.save is not None:
            prompt_add_to_saved_list(
                hits, apps_dir, args.dry_run, auto=True, save_path=save_path
            )
        return 0

    if args.yes:
        n = enable_all_matches(hits, args.dry_run)
        if n:
            print("\n共开启 %d 条。" % n)
        if args.save is not None or not args.no_save_prompt:
            if args.save is not None:
                prompt_add_to_saved_list(
                    hits, apps_dir, args.dry_run, auto=True, save_path=save_path
                )
            elif not args.no_save_prompt:
                prompt_add_to_saved_list(hits, apps_dir, args.dry_run, auto=False)
        return 0

    run_interactive(
        hits,
        apps_dir,
        args.dry_run,
        auto_save=args.save is not None,
        ask_save=not args.no_save_prompt,
        save_path=save_path,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
