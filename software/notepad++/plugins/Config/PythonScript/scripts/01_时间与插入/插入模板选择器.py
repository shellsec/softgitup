# -*- coding: utf-8 -*-
"""一次选择分类，运行对应「插入模板_*.py」或工作日记脚本。"""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))

ITEMS = [
    ("1", "工作", "插入模板_工作.py"),
    ("2", "生活", "插入模板_生活.py"),
    ("3", "学习", "插入模板_学习.py"),
    ("4", "健康", "插入模板_健康.py"),
    ("5", "灵感", "插入模板_灵感.py"),
    ("6", "家庭", "插入模板_家庭.py"),
    ("7", "财务", "插入模板_财务.py"),
    ("8", "随记", "插入模板_随记.py"),
    ("9", "社交", "插入模板_社交.py"),
    ("10", "阅读", "插入模板_阅读.py"),
    ("11", "项目", "插入模板_项目.py"),
    ("12", "运动", "插入模板_运动.py"),
    ("13", "情绪", "插入模板_情绪.py"),
    ("14", "副业", "插入模板_副业.py"),
    ("15", "工作日记·三点", "工作日记_三点.py"),
    ("16", "工作日记·流水", "工作日记_流水.py"),
]


def _run_script(filename):
    path = os.path.join(_here, filename)
    if not os.path.isfile(path):
        notepad.messageBox("找不到脚本：\n{}".format(path), "插入模板选择器", 0)
        return
    with open(path, "r", encoding="utf-8") as fp:
        src = fp.read()
    g = {
        "editor": editor,
        "notepad": notepad,
        "__name__": "__main__",
        "__file__": path,
    }
    try:
        g["console"] = console
    except NameError:
        pass
    exec(compile(src, path, "exec"), g)


def main():
    lines = "\n".join("{} — {}".format(k, label) for k, label, _ in ITEMS)
    r = notepad.prompt(
        "选择要插入的模板（输入序号）：\n" + lines,
        "插入模板选择器",
        "1",
    )
    if r is None:
        return
    r = (r or "").strip()
    for key, _label, fname in ITEMS:
        if r == key:
            _run_script(fname)
            return
    notepad.messageBox("请输入 1–{}。".format(len(ITEMS)), "插入模板选择器", 0)


main()
