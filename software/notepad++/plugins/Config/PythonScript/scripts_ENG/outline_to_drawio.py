# -*- coding: utf-8 -*-
"""
Export the current indented outline (same rules as Mermaid mindmap) to a diagrams.net
(draw.io) .drawio XML file. Pick save path via dialog. Stdlib only; tkinter or
folder_dialog_win.py (PowerShell returns path via UTF-8 temp file on Windows).

First non-empty line = root; following lines use leading spaces/tabs (tab = 4).
"""

import os
import sys
import uuid

_sd = os.path.dirname(os.path.abspath(__file__))
if _sd not in sys.path:
    sys.path.insert(0, _sd)

try:
    from folder_dialog_win import ask_save_filename
except ImportError:
    ask_save_filename = None
from datetime import datetime
from xml.sax.saxutils import escape

TAB_WIDTH = 4
_CELL_W = 140
_CELL_H = 44
_V_GAP = 56


class _Node(object):
    __slots__ = ("text", "children")

    def __init__(self, text):
        self.text = text
        self.children = []


def _leading_space_count(line):
    e = line.expandtabs(TAB_WIDTH)
    n = 0
    for ch in e:
        if ch == " ":
            n += 1
        else:
            break
    return n


def _parse_outline(body_lines):
    stripped = [ln.rstrip() for ln in body_lines]
    first_i = None
    for i, ln in enumerate(stripped):
        if ln.strip():
            first_i = i
            break
    if first_i is None:
        return None
    root_text = stripped[first_i].strip()
    root = _Node(root_text)
    stack = [(root, -1)]

    for ln in stripped[first_i + 1 :]:
        if not ln.strip():
            continue
        indent = _leading_space_count(ln)
        text = ln.expandtabs(TAB_WIDTH).strip()
        if not text:
            continue
        node = _Node(text)
        while stack[-1][1] >= indent:
            stack.pop()
        stack[-1][0].children.append(node)
        stack.append((node, indent))
    return root


def _count_leaves(n):
    if not n.children:
        return 1
    return sum(_count_leaves(c) for c in n.children)


def _layout(node, depth, x0, x1, pos):
    """Store (x, y, w, h) top-left for each node; return center x."""
    if not node.children:
        cx = (x0 + x1) / 2.0
        y = depth * (_CELL_H + _V_GAP)
        pos[node] = (cx - _CELL_W / 2.0, y, _CELL_W, _CELL_H)
        return cx
    total = sum(_count_leaves(c) for c in node.children)
    if total <= 0:
        total = 1
    cur = float(x0)
    centers = []
    span = float(x1 - x0)
    for ch in node.children:
        w = (_count_leaves(ch) / total) * span
        cx_ch = _layout(ch, depth + 1, cur, cur + w, pos)
        centers.append(cx_ch)
        cur += w
    cx = sum(centers) / len(centers)
    y = depth * (_CELL_H + _V_GAP)
    pos[node] = (cx - _CELL_W / 2.0, y, _CELL_W, _CELL_H)
    return cx


def _esc_attr(s):
    return escape(str(s), {'"': "&quot;", "'": "&apos;"})


def _build_drawio_xml(root, pos):
    next_id = [2]

    def new_id():
        i = next_id[0]
        next_id[0] += 1
        return str(i)

    cell_ids = {}
    for n in _walk_preorder(root):
        cell_ids[n] = new_id()

    max_r = 0.0
    max_b = 0.0
    for n, geom in pos.items():
        x, y, w, h = geom
        max_r = max(max_r, x + w)
        max_b = max(max_b, y + h)

    pw = int(max(850, max_r + 80))
    ph = int(max(1169, max_b + 80))

    did = "d-" + uuid.uuid4().hex[:12]
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    lines = [
        '<mxfile host="app.diagrams.net" modified="{}" agent="Notepad++ PythonScript" version="22.1.0" type="device">'.format(
            ts
        ),
        '  <diagram name="Page-1" id="{}">'.format(did),
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{}" pageHeight="{}" math="0" shadow="0">'.format(
            pw, ph
        ),
        "      <root>",
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>',
    ]

    style_v = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
    style_e = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#6c8ebf;"

    for n in _walk_preorder(root):
        cid = cell_ids[n]
        x, y, w, h = pos[n]
        val = _esc_attr(n.text)
        lines.append(
            '        <mxCell id="{}" value="{}" style="{}" vertex="1" parent="1">'.format(
                cid, val, style_v
            )
        )
        lines.append(
            '          <mxGeometry x="{:.0f}" y="{:.0f}" width="{:.0f}" height="{:.0f}" as="geometry"/>'.format(
                x, y, w, h
            )
        )
        lines.append("        </mxCell>")

    for n in _walk_preorder(root):
        for ch in n.children:
            eid = new_id()
            lines.append(
                '        <mxCell id="{}" style="{}" edge="1" parent="1" source="{}" target="{}">'.format(
                    eid, style_e, cell_ids[n], cell_ids[ch]
                )
            )
            lines.append('          <mxGeometry relative="1" as="geometry"/>')
            lines.append("        </mxCell>")

    lines.extend(
        [
            "      </root>",
            "    </mxGraphModel>",
            "  </diagram>",
            "</mxfile>",
        ]
    )
    return "\n".join(lines) + "\n"


def _walk_preorder(root):
    out = []

    def w(n):
        out.append(n)
        for c in n.children:
            w(c)

    w(root)
    return out


def outline_to_drawio():
    sel = editor.getSelText()
    if sel is not None and len(sel) > 0:
        raw = sel
    else:
        raw = editor.getText()

    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    root = _parse_outline(lines)
    if root is None:
        notepad.messageBox("No outline to export.", "Outline to draw.io", 0)
        return

    leaves = max(1, _count_leaves(root))
    width_px = max(600.0, leaves * (_CELL_W + 20))

    pos = {}
    _layout(root, 0, 0.0, width_px, pos)

    xml = _build_drawio_xml(root, pos)
    if ask_save_filename is None:
        notepad.messageBox(
            "Missing folder_dialog_win.py in the same folder as this script.",
            "Outline to draw.io",
            0,
        )
        return
    path = ask_save_filename(
        "Save draw.io file",
        "outline.drawio",
        [
            ("draw.io / diagrams.net", "*.drawio"),
            ("XML", "*.xml"),
            ("All", "*.*"),
        ],
    )
    if not path:
        return

    path = os.path.normpath(os.path.expanduser(str(path).strip()))
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception as e:
            notepad.messageBox(
                "Could not create parent folder for save path:\n{}".format(e),
                "Outline to draw.io",
                0,
            )
            return

    try:
        with open(path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(xml)
    except Exception as e:
        notepad.messageBox("Write failed:\n{}".format(e), "Outline to draw.io", 0)
        return

    notepad.messageBox("Saved:\n{}".format(path), "Outline to draw.io", 0)


outline_to_drawio()
