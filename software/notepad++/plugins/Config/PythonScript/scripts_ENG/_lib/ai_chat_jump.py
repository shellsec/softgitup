# -*- coding: utf-8 -*-
"""
Open web AI chat; copy selection/full doc when the site has no URL prefill.
Prompts: prompts.ini / 提示词.ini next to the jump scripts (section [prompts] or [提示词]).
"""
from __future__ import print_function

import os
import sys
import webbrowser

try:
    from Npp import editor, notepad
except ImportError:
    pass

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

SERVICES = {
    "chatgpt": ("ChatGPT", "https://chatgpt.com/", None),
    "claude": ("Claude", "https://claude.ai/new", None),
    "gemini": ("Gemini", "https://gemini.google.com/app", None),
    "copilot": ("Microsoft Copilot", "https://copilot.microsoft.com/", None),
    "perplexity": ("Perplexity", "https://www.perplexity.ai/", None),
    "grok": ("Grok", "https://grok.com/", None),
    "poe": ("Poe", "https://poe.com/", None),
    "meta_ai": ("Meta AI", "https://www.meta.ai/", None),
    "deepseek": ("DeepSeek", "https://chat.deepseek.com/", None),
    "kimi": ("Kimi", "https://kimi.moonshot.cn/", None),
    "qwen": ("Qwen", "https://tongyi.aliyun.com/qianwen/", None),
    "doubao": ("Doubao", "https://www.doubao.com/chat/", None),
    "wenxin": ("ERNIE (Wenxin)", "https://yiyan.baidu.com/", None),
    "yuanbao": ("Tencent Yuanbao", "https://yuanbao.tencent.com/chat", None),
    "chatglm": ("ChatGLM", "https://chatglm.cn/", None),
    "spark": ("iFlytek Spark", "https://xinghuo.xfyun.cn/desk", None),
    "metaso": ("Metaso", "https://metaso.cn/", None),
    "tiangong": ("Tiangong", "https://www.tiangong.cn/", None),
    "step": ("StepFun", "https://www.stepfun.com/", None),
    "minimax": ("MiniMax", "https://chat.minimaxi.com/", None),
    "coze": ("Coze", "https://www.coze.cn/", None),
    "baichuan": ("Baichuan", "https://chat.baichuan-ai.com/", None),
    "lingyi": ("01.AI Lingyi", "https://www.lingyiwanwu.com/", None),
    "zhipu_open": ("Zhipu Open Platform", "https://open.bigmodel.cn/", None),
}

PREFILL_MAX_CHARS = 1800
PROMPT_INI_NAMES = ("提示词.ini", "prompts.ini")
SERVICE_ORDER = (
    "chatgpt",
    "claude",
    "gemini",
    "copilot",
    "perplexity",
    "grok",
    "poe",
    "meta_ai",
    "deepseek",
    "kimi",
    "qwen",
    "doubao",
    "wenxin",
    "yuanbao",
    "chatglm",
    "spark",
    "metaso",
    "tiangong",
    "step",
    "minimax",
    "coze",
    "baichuan",
    "lingyi",
    "zhipu_open",
)


def _copy_to_clipboard(text):
    if not text:
        return False
    if sys.platform == "win32":
        try:
            import ctypes

            if not isinstance(text, str):
                text = text.decode("utf-8", errors="replace")
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            CF_UNICODETEXT = 13
            GMEM_MOVEABLE = 0x0002
            if not user32.OpenClipboard(None):
                return False
            try:
                if not user32.EmptyClipboard():
                    return False
                raw = text.encode("utf-16-le") + b"\x00\x00"
                n = len(raw)
                h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, n)
                if not h_mem:
                    return False
                p = kernel32.GlobalLock(h_mem)
                if not p:
                    kernel32.GlobalFree(h_mem)
                    return False
                try:
                    ctypes.memmove(p, raw, n)
                finally:
                    kernel32.GlobalUnlock(h_mem)
                if not user32.SetClipboardData(CF_UNICODETEXT, h_mem):
                    kernel32.GlobalFree(h_mem)
                    return False
                return True
            finally:
                user32.CloseClipboard()
        except Exception:
            pass
        try:
            import win32clipboard
            import win32con

            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
                return True
            finally:
                win32clipboard.CloseClipboard()
        except Exception:
            pass
    try:
        import tkinter

        r = tkinter.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()
        return True
    except Exception:
        pass
    return False


def get_scope_text():
    try:
        editor
    except NameError:
        from Npp import editor, notepad  # noqa: F401

    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        return sel
    return editor.getText()


def _config_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        for name in ("00_AI对话跳转", "00_AI_Chat", "11_AI对话跳转", "11_AI_Chat"):
            d = os.path.join(here, name)
            if os.path.isdir(d):
                return d
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.path.dirname(os.path.abspath(__file__))


def load_prompts():
    cfg_dir = _config_dir()
    path = None
    for fn in PROMPT_INI_NAMES:
        p = os.path.join(cfg_dir, fn)
        if os.path.isfile(p):
            path = p
            break
    if not path:
        return []

    try:
        try:
            import configparser
        except ImportError:
            import ConfigParser as configparser

        cp = configparser.ConfigParser()
        try:
            cp.read(path, encoding="utf-8")
        except TypeError:
            cp.read(path)
        items = []
        for section in cp.sections():
            if section in ("提示词", "prompts"):
                for key in cp.options(section):
                    val = cp.get(section, key)
                    items.append((key, val.replace("\\n", "\n")))
        if items:
            return items
    except Exception:
        pass
    return _load_prompts_plain(path)


def _load_prompts_plain(path):
    items = []
    try:
        f = open(path, "r", encoding="utf-8")
    except TypeError:
        f = open(path, "r")
    with f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                items.append((k.strip(), v.strip().replace("\\n", "\n")))
    return items


def _pick_prompt():
    items = load_prompts()
    if not items:
        return None
    lines = []
    for i, (name, _body) in enumerate(items, 1):
        lines.append("{0}. {1}".format(i, name))
    msg = "Prompt number:\n\n" + "\n".join(lines)
    raw = notepad.prompt(msg, "Pick prompt", "1")
    if raw is None:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        idx = int(raw) - 1
    except ValueError:
        return None
    if idx < 0 or idx >= len(items):
        return None
    name, body = items[idx]
    return name, body


def _pick_service():
    keys = [k for k in SERVICE_ORDER if k in SERVICES]
    lines = []
    for i, sid in enumerate(keys, 1):
        lines.append("{0}. {1}".format(i, SERVICES[sid][0]))
    msg = "AI service number:\n\n" + "\n".join(lines)
    raw = notepad.prompt(msg, "Jump to AI", "2")
    if raw is None:
        return None
    raw = raw.strip()
    try:
        idx = int(raw) - 1
    except ValueError:
        return None
    if idx < 0 or idx >= len(keys):
        return None
    return keys[idx]


def build_payload(scope_text, prompt_body=None):
    if prompt_body:
        body = prompt_body
        if scope_text:
            body = body + scope_text
        return body
    return scope_text or ""


def open_for_service(service_id, text):
    if service_id not in SERVICES:
        return
    _name, base_url, prefill_key = SERVICES[service_id]
    url = base_url

    if text:
        if prefill_key and len(text) <= PREFILL_MAX_CHARS:
            sep = "&" if "?" in base_url else "?"
            try:
                q = url_quote(text)
            except TypeError:
                q = url_quote(text.encode("utf-8"))
            url = base_url + sep + prefill_key + "=" + q
        else:
            _copy_to_clipboard(text)

    try:
        webbrowser.open(url)
    except Exception:
        pass


def run_service(service_id, use_prompt_menu=False):
    scope = get_scope_text()
    prompt_body = None
    if use_prompt_menu:
        picked = _pick_prompt()
        if picked is None:
            return
        _pname, prompt_body = picked
    text = build_payload(scope, prompt_body)
    open_for_service(service_id, text)


def run_prompt_then_service():
    picked = _pick_prompt()
    if picked is None:
        return
    sid = _pick_service()
    if sid is None:
        return
    _pname, prompt_body = picked
    text = build_payload(get_scope_text(), prompt_body)
    open_for_service(sid, text)


def run_one_click_menu():
    sid = _pick_service()
    if sid is None:
        return
    scope = get_scope_text()
    use_prompt = notepad.prompt(
        "Add prompt prefix?\n1 = selection/full doc only\n2 = pick prompt first",
        "Jump to AI",
        "1",
    )
    if use_prompt is None:
        return
    prompt_body = None
    if use_prompt.strip() == "2":
        picked = _pick_prompt()
        if picked is None:
            return
        _pname, prompt_body = picked
    text = build_payload(scope, prompt_body)
    open_for_service(sid, text)
