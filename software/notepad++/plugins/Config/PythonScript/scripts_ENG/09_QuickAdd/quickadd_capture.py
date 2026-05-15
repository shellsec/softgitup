# -*- coding: utf-8 -*-
"""
Quick capture with question-first templates (you fill answers later).

Optional template files next to this script (UTF-8):
  quickadd_template_new.md
  quickadd_template_daily_block.md
  quickadd_template_cursor.md
Placeholders: {title} {category} {date} {time} {datetime} {body} {prompt_reply} {clipboard}
  `{datetime}` uses the same long stamp as InsertTime.py (English); `{date}` / `{time}` stay ISO-style for mixed custom templates.

Categories: configure list `categories` in quickadd_config.json (used for 1–3).
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
    from time_stamp_fmt import format_en as _format_rich_ts
except ImportError:
    def _format_rich_ts(now=None):
        n = now if now is not None else datetime.now()
        return n.strftime("%Y-%m-%d %H:%M")

_CONFIG_NAME = "quickadd_config.json"
_INVALID_FN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

BUILTIN_TEMPLATE_NEW = """# {title}

{datetime}

Category: {category}

**Breakdown**
- One-line theme (what I want clear):
- Known facts / hard constraints:
- Other angles (optional):
- Provisional conclusion / to verify:

---
"""

BUILTIN_TEMPLATE_DAILY = """{datetime}

Category: {category}

- Quick line: {prompt_reply}

**Breakdown**
- Trigger / what happened:
- My current take (draft):
- Risks / fuzzy spots:
- Smallest next move:

- Clippings / reference:
{body}

---
"""

BUILTIN_TEMPLATE_CURSOR = """{datetime}

**Breakdown**
- Why I'm writing this now (hook):
- One line of key fact:
- Still fuzzy:
- Smallest next step:

- Clipboard: {clipboard}
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
        "categories": ["Uncategorized", "Work", "Life", "Study", "Health", "Ideas", "Family", "Money", "Scratch"],
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
        name = "untitled"
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
        "Pick a category (number), or type a custom label (Cancel = abort):\n" + lines,
        "QuickAdd · Category",
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
            "folder_dialog_win.py not found under scripts_ENG/_lib; cannot pick notes folder.",
            "QuickAdd",
            0,
        )
        return False

    picked = ask_directory("Pick notes root (saved to quickadd_config.json)")
    if not picked:
        return False
    cfg["notes_dir"] = os.path.normpath(picked)
    _save_config(cfg)
    notepad.messageBox(
        "Saved notes root:\n{}".format(cfg["notes_dir"]),
        "QuickAdd",
        0,
    )
    return True


def action_set_root(cfg):
    if ask_directory is None:
        notepad.messageBox("folder_dialog_win.py not found under scripts_ENG/_lib.", "QuickAdd", 0)
        return
    picked = ask_directory("Pick a new notes root")
    if not picked:
        return
    cfg["notes_dir"] = os.path.normpath(picked)
    _save_config(cfg)
    notepad.messageBox("Config updated.", "QuickAdd", 0)


def action_new_note(cfg):
    if not _ensure_notes_dir(cfg):
        return
    cat, cancelled = _pick_category(cfg)
    if cancelled:
        return
    base = os.path.normpath(cfg["notes_dir"])
    title_raw = notepad.prompt("Note title (empty = time-based):", "QuickAdd · New note", "")
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
        notepad.messageBox("Write failed:\n{}".format(e), "QuickAdd", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "Created with template (category: {}):\n{}".format(cat, path),
        "QuickAdd",
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
        "prompt_reply": (prompt_reply or "").strip() or "(fill later)",
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
        "Optional one-liner summary (can be empty; template still has answer blanks):",
        "QuickAdd · Daily",
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
        notepad.messageBox("Write failed:\n{}".format(e), "QuickAdd", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "Appended block (category: {}) to:\n{}".format(cat, path),
        "QuickAdd",
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
        notepad.messageBox("Clipboard is empty.", "QuickAdd", 0)
        return
    path = _daily_file_path(cfg)
    block = _daily_block(cfg, cat, prompt_reply="", body=clip, clipboard=clip)
    prev = _read_utf8(path)
    if prev and not prev.endswith("\n"):
        prev += "\n"
    try:
        _write_utf8(path, prev + block.rstrip() + "\n\n")
    except Exception as e:
        notepad.messageBox("Write failed:\n{}".format(e), "QuickAdd", 0)
        return
    _open_if(cfg, path)
    notepad.messageBox(
        "Appended clipboard block (category: {}) to:\n{}".format(cat, path),
        "QuickAdd",
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
        notepad.messageBox("Insert failed:\n{}".format(e), "QuickAdd", 0)
        return
    notepad.messageBox("Inserted question template at cursor.", "QuickAdd", 0)


def main():
    cfg = _load_config()
    choice = notepad.prompt(
        "Choose (enter a digit):\n"
        "1 — New Markdown (question template + category)\n"
        "2 — Append block to daily (template + category; optional one-liner)\n"
        "3 — Clipboard into daily (same template; body section filled)\n"
        "4 — Insert short template + clipboard at cursor\n"
        "5 — Set notes root folder\n"
        "6 — Toggle open-after-save (now: {})\n"
        "\n"
        "Edit categories in quickadd_config.json (key: categories).".format(
            "on" if cfg.get("open_after_save", True) else "off"
        ),
        "QuickAdd · Templates",
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
            "open_after_save = {}".format(cfg["open_after_save"]),
            "QuickAdd",
            0,
        )
    else:
        notepad.messageBox("Enter 1–6.", "QuickAdd", 0)


main()
