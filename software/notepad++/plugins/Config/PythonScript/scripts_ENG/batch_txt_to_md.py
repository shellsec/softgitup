# -*- coding: utf-8 -*-
"""
Pick an input folder and an output folder; recursively convert all .txt files to .md (UTF-8).
Preserves relative paths under the input root. No pip deps.

Uses tkinter if available; on Windows without tkinter, falls back to PowerShell + WinForms
(folder_dialog_win.py in the same folder as this script).
"""

import os
import sys

_sd = os.path.dirname(os.path.abspath(__file__))
if _sd not in sys.path:
    sys.path.insert(0, _sd)

try:
    from folder_dialog_win import ask_directory
except ImportError:
    ask_directory = None


def _read_text(path):
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fp:
                return fp.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as fp:
        return fp.read()


def _pick_folders():
    if ask_directory is None:
        notepad.messageBox(
            "Missing folder_dialog_win.py in the same folder as this script.",
            "Batch TXT to Markdown",
            0,
        )
        return None, None
    inp = ask_directory("Select folder containing .txt files")
    if not inp:
        return None, None
    outp = ask_directory("Select folder to save .md files")
    if not outp:
        return None, None
    return os.path.normpath(inp), os.path.normpath(outp)


def batch_txt_to_md():
    inp, outp = _pick_folders()
    if inp is None:
        return

    inp = os.path.normpath(os.path.expanduser(str(inp).strip()))
    outp = os.path.normpath(os.path.expanduser(str(outp).strip()))
    if not os.path.isdir(inp):
        notepad.messageBox(
            "Input path is not a valid folder:\n{}".format(inp),
            "Batch TXT to Markdown",
            0,
        )
        return

    if os.path.normcase(os.path.normpath(inp)) == os.path.normcase(os.path.normpath(outp)):
        notepad.messageBox("Input and output folders must be different.", "Batch TXT to Markdown", 0)
        return

    ok = 0
    errors = []

    for base, _dirs, files in os.walk(inp):
        for name in files:
            if not name.lower().endswith(".txt"):
                continue
            src = os.path.join(base, name)
            rel = os.path.relpath(src, inp)
            dst_rel = os.path.splitext(rel)[0] + ".md"
            dst = os.path.join(outp, dst_rel)
            try:
                text = _read_text(src)
                parent = os.path.dirname(dst)
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent, exist_ok=True)
                with open(dst, "w", encoding="utf-8", newline="\n") as fp:
                    fp.write(text)
                ok += 1
            except Exception as e:
                errors.append("{}: {}".format(rel, e))

    msg = "Converted {} .txt file(s) to .md.".format(ok)
    if errors:
        msg += "\n\nErrors ({}):\n".format(len(errors))
        msg += "\n".join(errors[:15])
        if len(errors) > 15:
            msg += "\n..."
    if ok == 0 and not errors:
        msg = (
            "No files with extension .txt were found under the selected input folder "
            "(including subfolders).\n\n"
            "Scanned root:\n{}\n\n"
            "Check that:\n"
            "· You picked the folder that actually contains the .txt files;\n"
            "· With “hide extensions” on, a file shown as “name.txt” might really be "
            "name.txt.md — enable “File name extensions” and verify;\n"
            "· Only .txt / .TXT are matched (not .text, .log, or extensionless files)."
        ).format(inp)

    notepad.messageBox(msg, "Batch TXT to Markdown", 0)


batch_txt_to_md()
