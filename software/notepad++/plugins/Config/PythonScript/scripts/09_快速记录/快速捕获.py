# -*- coding: utf-8 -*-
"""
快速捕获：问题优先模板（先落盘，后补答案）。

可选模板文件（与本脚本同目录，UTF-8）：
  quickadd_template_new.md
  quickadd_template_daily_block.md
  quickadd_template_cursor.md
占位符：{title} {category} {date} {time} {datetime} {body} {prompt_reply} {clipboard}
  `{datetime}` 使用与「插入时间中文」相同的长串；`{date}` / `{time}` 为 ISO 风格。

分类：在 quickadd_config.json 的 categories 列表中配置（用于 1–3）。
"""

import json
import os
import re
import sys
from datetime import datetime

_sd = os.path.dirname(os.path.abspath(__file__))
if _sd not in sys.path:
    sys.path.insert(0, _sd)

_d = _sd
for _ in range(10):
    _lib = os.path.join(_d, "_lib")
    if os.path.isfile(os.path.join(_lib, "folder_dialog_win.py")):
        if _lib not in sys.path:
            sys.path.insert(0, _lib)
        break
    _parent = os.path.dirname(_d)
    if _parent == _d:
        break
    _d = _parent

try:
    from folder_dialog_win import ask_directory
except ImportError:
    ask_directory = None

try:
    from time_stamp_fmt import format_cn as _format_rich_ts
except ImportError:
    def _format_rich_ts(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y-%m-%d %H:%M")

_CONFIG_NAME = "quickadd_config.json"
_INVALID_FN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

BUILTIN_TEMPLATE_NEW = """# {title}

{datetime}

分类：{category}

**拆解**
- 一句话主题（想弄清什么）：
- 已知事实 / 硬约束：
- 其它角度（可选）：
- 暂定结论 / 待验证：

---
"""

BUILTIN_TEMPLATE_DAILY = """{datetime}

分类：{category}

- 速记一句：{prompt_reply}

**拆解**
- 触发 / 发生了什么：
- 当前看法（草稿）：
- 风险 / 模糊点：
- 最小下一步：

- 摘录 / 参考：
{body}

---
"""

BUILTIN_TEMPLATE_CURSOR = """{datetime}

**拆解**
- 此刻写下的原因（钩子）：
- 关键事实一句：
- 仍模糊：
- 最小下一步：

- 剪贴板：{clipboard}
"""


def _subst(template, mapping):
    s = template
    for k, v in mapping.items():
        s = s.replace("{" + k + "}", str(v) if v is not None else "")
    return s


def _load_optional_template(filename, fallback):
    path = os.path.join(_sd, filename)
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8-sig") as fp:
                t = fp.read()
            if t.strip():
                return t
        except Exception:
            pass
    return fallback


def _config_path():
    return os.path.join(_sd, _CONFIG_NAME)


def _defaults():
    return {
        "notes_dir": "",
        "daily_in_subdir": True,
        "date_prefix_new_files": True,
        "open_after_save": True,
        "categories": ["未分类", "工作", "生活", "学习", "健康", "灵感", "家庭", "财务", "随记"],
    }


def _load_config():
    path = _config_path()
    cfg = _defaults()
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, dict):
                cfg.update(data)
        except Exception:
            pass
    cats = cfg.get("categories")
    if not isinstance(cats, list) or not cats:
        cfg["categories"] = list(_defaults()["categories"])
    return cfg


def _save_config(cfg):
    path = _config_path()
    out = dict(_defaults())
    out.update(cfg)
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=2)


def _sanitize_filename(name):
    name = (name or "").strip()
    name = _INVALID_FN.sub("-", name)
    name = name.strip(". ").replace("\r", "").replace("\n", " ")
    if not name:
        name = "未命名"
    return name[:180]


def _unique_path(path):
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(path)
    n = 2
    while True:
        cand = "{}-{}{}".format(root, n, ext)
        if not os.path.exists(cand):
            return cand
        n += 1


def _daily_file_path(cfg):
    base = os.path.normpath(os.path.expanduser(cfg.get("notes_dir", "").strip()))
    day = datetime.now().strftime("%Y-%m-%d")
    if cfg.get("daily_in_subdir", True):
        d = os.path.join(base, "daily")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, day + ".md")
    return os.path.join(base, day + ".md")


def _read_utf8(path):
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8-sig") as fp:
            return fp.read()
    except Exception:
        with open(path, "r", encoding="utf-8", errors="replace") as fp:
            return fp.read()


def _write_utf8(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(text)


def _open_if(cfg, path):
    if cfg.get("open_after_save", True):
        try:
            notepad.open(path)
        except Exception:
            pass


def _clipboard_text():
    try:
        import tkinter as tk

        r = tk.Tk()
        r.withdraw()
        try:
            r.attributes("-topmost", True)
        except Exception:
            pass
        r.update()
        try:
            t = r.clipboard_get()
        except Exception:
            t = ""
        r.destroy()
        return t or ""
    except Exception:
        return ""


def _pick_category(cfg):
    cats = cfg.get("categories") or _defaults()["categories"]
    lines = "\n".join("{0} — {1}".format(i + 1, c) for i, c in enumerate(cats))
    r = notepad.prompt(
        "选择分类（序号），或直接输入自定义名称（取消=中止）：\n" + lines,
        "快速捕获 · 分类",
        "1",
    )
    if r is None:
        return None, True
    r = (r or "").strip()
    if not r:
        return cats[0], False
    if r.isdigit():
        i = int(r) - 1
        if 0 <= i < len(cats):
            return cats[i], False
    return r, False


def _ensure_notes_dir(cfg):
    n = (cfg.get("notes_dir") or "").strip()
    n = os.path.normpath(os.path.expanduser(n))
    if n and os.path.isdir(n):
        cfg["notes_dir"] = n
        return True

    if ask_directory is None:
        notepad.messageBox(
            "未找到 scripts/_lib/folder_dialog_win.py，无法选择笔记目录。",
            "快速捕获",
            0,
        )
        return False

    picked = ask_directory("选择笔记根目录（将写入 quickadd_config.json）")
    if not picked:
        return False
    cfg["notes_dir"] = os.path.normpath(picked)
    _save_config(cfg)
    notepad.messageBox(
        "已保存笔记根目录：\n{}".format(cfg["notes_dir"]),
        "快速捕获",
        0,
    )
    return True


def action_set_root(cfg):
    if ask_directory is None:
        notepad.messageBox("未找到 scripts/_lib/folder_dialog_win.py。", "快速捕获", 0)
        return
    picked = ask_directory("选择新的笔记根目录")
    if not picked:
        return
    cfg["notes_dir"] = os.path.normpath(picked)
    _save_config(cfg)
    notepad.messageBox("配置已更新。", "快速捕获", 0)


def action_new_note(cfg):
    if not _ensure_notes_dir(cfg):
        return
    cat, cancelled = _pick_category(cfg)
    if cancelled:
        return
    base = os.path.normpath(cfg["notes_dir"])
    title_raw = notepad.prompt("笔记标题（空=按时间命名）：", "快速捕获 · 新建笔记", "")
    if title_raw is None:
        return
    title_raw = title_raw.strip()
    now = datetime.now()
    auto_time_title = now.strftime("%H%M%S")
    if not title_raw:
        title_raw = auto_time_title
    slug = _sanitize_filename(title_raw)
    ext = ".md"
    if cfg.get("date_prefix_new_files", True):
        prefix = now.strftime("%Y%m%d")
        fname = "{}-{}{}".format(prefix, slug, ext)
    else:
        fname = "{}{}".format(slug, ext)
    path = _unique_path(os.path.join(base, fname))
    h1 = title_raw if title_raw != auto_time_title else slug
    tpl = _load_optional_template("quickadd_template_new.md", BUILTIN_TEMPLATE_NEW)
    mapping = {
        "title": h1,
        "category": cat,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "datetime": _format_rich_ts(now),
        "body": "",
        "prompt_reply": "",
        "clipboard": "",
    }
    body = _subst(tpl, mapping)
    try:
        _write_utf8(path, body)
    except Exception as e:
        notepad.messageBox("写入失败：\n{}".format(e), "快速捕获", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "已用模板创建（分类：{}）：\n{}".format(cat, path),
        "快速捕获",
        0,
    )


def _daily_block(cfg, category, prompt_reply, body, clipboard):
    tpl = _load_optional_template(
        "quickadd_template_daily_block.md",
        BUILTIN_TEMPLATE_DAILY,
    )
    now = datetime.now()
    mapping = {
        "title": "",
        "category": category,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "datetime": _format_rich_ts(now),
        "body": body or "",
        "prompt_reply": (prompt_reply or "").strip() or "（稍后填写）",
        "clipboard": clipboard or "",
    }
    return _subst(tpl, mapping)


def action_append_daily(cfg):
    if not _ensure_notes_dir(cfg):
        return
    cat, cancelled = _pick_category(cfg)
    if cancelled:
        return
    path = _daily_file_path(cfg)
    extra = notepad.prompt(
        "可选一句摘要（可空；模板仍留有填写空位）：",
        "快速捕获 · 日记",
        "",
    )
    if extra is None:
        return
    block = _daily_block(cfg, cat, extra, body="", clipboard="")
    prev = _read_utf8(path)
    if prev and not prev.endswith("\n"):
        prev += "\n"
    try:
        _write_utf8(path, prev + block.rstrip() + "\n\n")
    except Exception as e:
        notepad.messageBox("写入失败：\n{}".format(e), "快速捕获", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "已追加块（分类：{}）到：\n{}".format(cat, path),
        "快速捕获",
        0,
    )


def action_clipboard_daily(cfg):
    if not _ensure_notes_dir(cfg):
        return
    cat, cancelled = _pick_category(cfg)
    if cancelled:
        return
    clip = _clipboard_text().strip()
    if not clip:
        notepad.messageBox("剪贴板为空。", "快速捕获", 0)
        return
    path = _daily_file_path(cfg)
    block = _daily_block(cfg, cat, prompt_reply="", body=clip, clipboard=clip)
    prev = _read_utf8(path)
    if prev and not prev.endswith("\n"):
        prev += "\n"
    try:
        _write_utf8(path, prev + block.rstrip() + "\n\n")
    except Exception as e:
        notepad.messageBox("写入失败：\n{}".format(e), "快速捕获", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "已追加剪贴板块（分类：{}）到：\n{}".format(cat, path),
        "快速捕获",
        0,
    )


def action_insert_cursor_clipboard():
    tpl = _load_optional_template(
        "quickadd_template_cursor.md",
        BUILTIN_TEMPLATE_CURSOR,
    )
    clip = _clipboard_text()
    now = datetime.now()
    mapping = {
        "title": "",
        "category": "",
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "datetime": _format_rich_ts(now),
        "body": "",
        "prompt_reply": "",
        "clipboard": clip.rstrip() if clip else "",
    }
    line = "\n" + _subst(tpl, mapping).rstrip() + "\n"
    try:
        editor.insertText(editor.getCurrentPos(), line)
    except Exception as e:
        notepad.messageBox("插入失败：\n{}".format(e), "快速捕获", 0)
        return
    notepad.messageBox("已在光标处插入提问模板。", "快速捕获", 0)


def main():
    cfg = _load_config()
    choice = notepad.prompt(
        "选择（输入数字）：\n"
        "1 — 新建 Markdown（提问模板 + 分类）\n"
        "2 — 追加到日记（模板 + 分类；可选一句）\n"
        "3 — 剪贴板写入日记（同模板；正文区已填）\n"
        "4 — 在光标插入短模板 + 剪贴板\n"
        "5 — 设置笔记根目录\n"
        "6 — 切换保存后打开（当前：{}）\n"
        "\n"
        "可在 quickadd_config.json 中编辑 categories。".format(
            "开" if cfg.get("open_after_save", True) else "关"
        ),
        "快速捕获 · 模板",
        "1",
    )
    if choice is None:
        return
    choice = choice.strip()
    if choice == "1":
        action_new_note(cfg)
    elif choice == "2":
        action_append_daily(cfg)
    elif choice == "3":
        action_clipboard_daily(cfg)
    elif choice == "4":
        action_insert_cursor_clipboard()
    elif choice == "5":
        action_set_root(_load_config())
    elif choice == "6":
        cfg["open_after_save"] = not bool(cfg.get("open_after_save", True))
        _save_config(cfg)
        notepad.messageBox(
            "保存后打开 = {}".format(cfg["open_after_save"]),
            "快速捕获",
            0,
        )
    else:
        notepad.messageBox("请输入 1–6。", "快速捕获", 0)


main()
