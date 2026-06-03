# -*- coding: utf-8 -*-
"""先选 提示词.ini 中的前缀，再选 AI，拼接选区/全文后跳转。"""
import os
import sys

_d = os.path.dirname(os.path.abspath(__file__))
for __ in range(10):
    _lib = os.path.join(_d, "_lib")
    if os.path.isfile(os.path.join(_lib, "ai_chat_jump.py")):
        if _lib not in sys.path:
            sys.path.insert(0, _lib)
        break
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p

from ai_chat_jump import run_prompt_then_service

run_prompt_then_service()
