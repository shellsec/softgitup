# -*- coding: utf-8 -*-
"""
Configure local AI API (writes ai_config.json beside this script).
OpenAI-compatible: OpenAI / DeepSeek / Qwen / custom.
"""
import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
_CFG = os.path.join(_DIR, "ai_config.json")

PRESETS = {
    "1": {
        "name": "OpenAI",
        "api_base": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    "2": {
        "name": "DeepSeek",
        "api_base": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
    },
    "3": {
        "name": "Qwen (compatible mode)",
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
    },
    "4": {
        "name": "Custom OpenAI-compatible",
        "api_base": "",
        "model": "gpt-3.5-turbo",
    },
}


def _load():
    if os.path.isfile(_CFG):
        try:
            with open(_CFG, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}


def _save(cfg):
    with open(_CFG, "w", encoding="utf-8") as fp:
        json.dump(cfg, fp, ensure_ascii=False, indent=2)


def main():
    cur = _load()
    hint = ""
    if cur.get("api_base"):
        hint = "\nCurrent: {} / {}\n".format(cur.get("api_base", ""), cur.get("model", ""))
    choice = notepad.prompt(
        "Preset:\n"
        "1 — OpenAI\n"
        "2 — DeepSeek\n"
        "3 — Qwen (compatible mode)\n"
        "4 — Custom base URL\n"
        "5 — Update API key only\n"
        "6 — Show config (masked key)\n"
        "{}".format(hint),
        "Configure AI",
        "2",
    )
    if choice is None:
        return
    choice = (choice or "").strip()

    if choice == "6":
        key = cur.get("api_key", "")
        masked = (key[:4] + "…" + key[-4:]) if len(key) > 8 else ("(empty)" if not key else "****")
        notepad.messageBox(
            "api_base: {}\nmodel: {}\napi_key: {}\ntemperature: {}\nmax_tokens: {}\n\nFile: {}".format(
                cur.get("api_base", ""),
                cur.get("model", ""),
                masked,
                cur.get("temperature", 0.7),
                cur.get("max_tokens", 2000),
                _CFG,
            ),
            "Configure AI",
            0,
        )
        return

    if choice == "5":
        key = notepad.prompt("API key:", "Configure AI · Key", "")
        if key is None or not (key or "").strip():
            return
        cur["api_key"] = key.strip()
        cur.setdefault("api_base", "https://api.openai.com/v1")
        cur.setdefault("model", "gpt-3.5-turbo")
        cur.setdefault("temperature", 0.7)
        cur.setdefault("max_tokens", 2000)
        cur.setdefault("api_type", "openai")
        try:
            _save(cur)
        except Exception as e:
            notepad.messageBox("Save failed:\n{}".format(e), "Configure AI", 0)
            return
        notepad.messageBox("API key updated.", "Configure AI", 0)
        return

    preset = PRESETS.get(choice)
    if not preset:
        notepad.messageBox("Enter 1–6.", "Configure AI", 0)
        return

    api_base = preset["api_base"]
    model = preset["model"]
    if choice == "4":
        api_base = notepad.prompt(
            "API Base (to /v1, without /chat/completions):",
            "Configure AI · Base",
            cur.get("api_base", "https://api.openai.com/v1"),
        )
        if api_base is None or not (api_base or "").strip():
            return
        api_base = api_base.strip().rstrip("/")
        model = notepad.prompt("Model:", "Configure AI · Model", cur.get("model", "gpt-3.5-turbo"))
        if model is None or not (model or "").strip():
            return
        model = model.strip()
    else:
        m2 = notepad.prompt(
            "Model (Enter keeps {}):".format(model),
            "Configure AI · Model",
            model,
        )
        if m2 is None:
            return
        if (m2 or "").strip():
            model = m2.strip()

    key = notepad.prompt("API key:", "Configure AI · Key", cur.get("api_key", ""))
    if key is None or not (key or "").strip():
        notepad.messageBox("No API key; cancelled.", "Configure AI", 0)
        return

    cfg = {
        "api_type": "openai",
        "api_key": key.strip(),
        "api_base": api_base,
        "model": model,
        "temperature": float(cur.get("temperature", 0.7) or 0.7),
        "max_tokens": int(cur.get("max_tokens", 2000) or 2000),
    }
    try:
        _save(cfg)
    except Exception as e:
        notepad.messageBox("Save failed:\n{}".format(e), "Configure AI", 0)
        return
    notepad.messageBox(
        "Saved ({}):\n{}\nModel: {}\n\n{}".format(preset["name"], api_base, model, _CFG),
        "Configure AI",
        0,
    )


main()
