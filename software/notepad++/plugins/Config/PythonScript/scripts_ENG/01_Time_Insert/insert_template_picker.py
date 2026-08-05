# -*- coding: utf-8 -*-
"""Pick a category once, then run the matching insert_template_*.py / work diary script."""
import os

_here = os.path.dirname(os.path.abspath(__file__))

ITEMS = [
    ("1", "Work", "insert_template_work.py"),
    ("2", "Life", "insert_template_life.py"),
    ("3", "Study", "insert_template_study.py"),
    ("4", "Health", "insert_template_health.py"),
    ("5", "Ideas", "insert_template_ideas.py"),
    ("6", "Family", "insert_template_family.py"),
    ("7", "Money", "insert_template_money.py"),
    ("8", "Scratch", "insert_template_scratch.py"),
    ("9", "Social", "insert_template_social.py"),
    ("10", "Reading", "insert_template_reading.py"),
    ("11", "Project", "insert_template_project.py"),
    ("12", "Workout", "insert_template_workout.py"),
    ("13", "Mood", "insert_template_mood.py"),
    ("14", "Side gig", "insert_template_side_gig.py"),
    ("15", "Work diary · three", "work_daily_three.py"),
    ("16", "Work diary · log", "work_daily_log.py"),
]


def _run_script(filename):
    path = os.path.join(_here, filename)
    if not os.path.isfile(path):
        notepad.messageBox("Script not found:\n{}".format(path), "Template picker", 0)
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
        "Pick a template (number):\n" + lines,
        "Template picker",
        "1",
    )
    if r is None:
        return
    r = (r or "").strip()
    for key, _label, fname in ITEMS:
        if r == key:
            _run_script(fname)
            return
    notepad.messageBox("Enter 1–{}.".format(len(ITEMS)), "Template picker", 0)


main()
