# -*- coding: utf-8 -*-
"""
配置本地 AI API（写入同目录 ai_config.json）。
支持 OpenAI 兼容接口：OpenAI / DeepSeek / 通义 / 自定义。
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
        "name": "通义千问（兼容模式）",
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
    },
    "4": {
        "name": "自定义 OpenAI 兼容",
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
        hint = "\n当前：{} / {}\n".format(cur.get("api_base", ""), cur.get("model", ""))
    choice = notepad.prompt(
        "选择预设：\n"
        "1 — OpenAI\n"
        "2 — DeepSeek\n"
        "3 — 通义千问（兼容模式）\n"
        "4 — 自定义 base URL\n"
        "5 — 仅更新 API Key（保留其余）\n"
        "6 — 显示当前配置（遮罩 Key）\n"
        "{}".format(hint),
        "配置AI",
        "2",
    )
    if choice is None:
        return
    choice = (choice or "").strip()

    if choice == "6":
        key = cur.get("api_key", "")
        masked = (key[:4] + "…" + key[-4:]) if len(key) > 8 else ("（空）" if not key else "****")
        notepad.messageBox(
            "api_base: {}\nmodel: {}\napi_key: {}\ntemperature: {}\nmax_tokens: {}\n\n文件：{}".format(
                cur.get("api_base", ""),
                cur.get("model", ""),
                masked,
                cur.get("temperature", 0.7),
                cur.get("max_tokens", 2000),
                _CFG,
            ),
            "配置AI",
            0,
        )
        return

    if choice == "5":
        key = notepad.prompt("输入 API Key：", "配置AI · Key", "")
        if key is None or not (key or "").strip():
            return
        cur["api_key"] = key.strip()
        if "api_base" not in cur:
            cur["api_base"] = "https://api.openai.com/v1"
        if "model" not in cur:
            cur["model"] = "gpt-3.5-turbo"
        cur.setdefault("temperature", 0.7)
        cur.setdefault("max_tokens", 2000)
        cur.setdefault("api_type", "openai")
        try:
            _save(cur)
        except Exception as e:
            notepad.messageBox("保存失败：\n{}".format(e), "配置AI", 0)
            return
        notepad.messageBox("已更新 API Key。", "配置AI", 0)
        return

    preset = PRESETS.get(choice)
    if not preset:
        notepad.messageBox("请输入 1–6。", "配置AI", 0)
        return

    api_base = preset["api_base"]
    model = preset["model"]
    if choice == "4":
        api_base = notepad.prompt(
            "API Base（勿带 /chat/completions，只要到 /v1）：",
            "配置AI · Base",
            cur.get("api_base", "https://api.openai.com/v1"),
        )
        if api_base is None or not (api_base or "").strip():
            return
        api_base = api_base.strip().rstrip("/")
        model = notepad.prompt("模型名：", "配置AI · Model", cur.get("model", "gpt-3.5-turbo"))
        if model is None or not (model or "").strip():
            return
        model = model.strip()
    else:
        m2 = notepad.prompt(
            "模型（回车用默认 {}）：".format(model),
            "配置AI · Model",
            model,
        )
        if m2 is None:
            return
        if (m2 or "").strip():
            model = m2.strip()

    key = notepad.prompt("API Key：", "配置AI · Key", cur.get("api_key", ""))
    if key is None or not (key or "").strip():
        notepad.messageBox("未填写 API Key，已取消。", "配置AI", 0)
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
        notepad.messageBox("保存失败：\n{}".format(e), "配置AI", 0)
        return
    notepad.messageBox(
        "已保存（{}）：\n{}\n模型：{}\n\n{}".format(preset["name"], api_base, model, _CFG),
        "配置AI",
        0,
    )


main()
