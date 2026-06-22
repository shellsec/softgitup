#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补全 AI IDE 生态与跨平台缺口（cockpit-tools 同伴、VibeCoding manifest 迁入主 apps）。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
PLATFORMS = ("windows", "darwin", "linux")
BATCH: dict[tuple[str, str], list] = {}


def _add(plat: str, shard: str, apps: list):
    BATCH.setdefault((plat, shard), []).extend(apps)


def _b(**kw):
    d = {
        "enabled": False,
        "prefer_api_assets": True,
        "version_tag_as_on_github": True,
        "windows_installer": False,
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
    }
    d.update(kw)
    return d


def _repo(repo: str) -> dict:
    return {
        "releases_url": f"https://bgithub.xyz/{repo}/releases",
        "repo_path": repo,
    }


def _manifest(
    plat: str,
    shard: str,
    aid: str,
    intro: str,
    category: str,
    **extra,
):
    entry = {
        "id": aid,
        "简介": intro,
        "分类": category,
        "enabled": False,
        "resolve_via": "github_pages_manifest",
        "manifest_item_id": aid,
        "version_tag_as_on_github": True,
        "use_download_filename": True,
        "windows_installer": False,
        "process_name": "",
        "kill_before_install": False,
        "run_installer": False,
    }
    entry.update(extra)
    _add(plat, shard, [entry])


# --- GitHub Release：Kilo Code ---
_kilo = "Kilo-Org/kilocode"
for plat, shard, markers, excl, ext, dl, save in (
    (
        "windows",
        "01-AI.json",
        ["kilo-vscode-win32-x64", ".vsix"],
        ["darwin", "linux", "arm64", "alpine", "baseline"],
        [".vsix"],
        [],
        "kilo-vscode-win32-x64.vsix",
    ),
    (
        "darwin",
        "01-AI.json",
        ["kilo-vscode-darwin-arm64", ".vsix"],
        ["windows", "linux", "x64.vsix", "alpine"],
        [".vsix"],
        [],
        "kilo-vscode-darwin-arm64.vsix",
    ),
    (
        "linux",
        "01-AI.json",
        ["kilo-vscode-linux-x64", ".vsix"],
        ["windows", "darwin", "arm64", "alpine"],
        [".vsix"],
        [],
        "kilo-vscode-linux-x64.vsix",
    ),
):
    _add(
        plat,
        shard,
        [
            _b(
                id="kilocode",
                简介="Kilo Code（开源 AI 编程 VS Code 扩展）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=markers,
                href_exclude_substrings=excl,
                installer_extensions=ext,
                download_names=dl,
                save_name=save,
                **_repo(_kilo),
            )
        ],
    )

for plat, shard, markers, dl, save in (
    (
        "windows",
        "06-命令行.json",
        ["kilo-windows-x64", ".zip"],
        ["kilo-windows-x64.zip"],
        "kilo-windows-x64.zip",
    ),
    (
        "darwin",
        "06-命令行.json",
        ["kilo-darwin-arm64", ".zip"],
        ["kilo-darwin-arm64.zip"],
        "kilo-darwin-arm64.zip",
    ),
    (
        "linux",
        "06-命令行.json",
        ["kilo-linux-x64", ".tar.gz"],
        ["kilo-linux-x64.tar.gz"],
        "kilo-linux-x64.tar.gz",
    ),
):
    _add(
        plat,
        shard,
        [
            _b(
                id="kilo_cli",
                简介="Kilo Code CLI / 独立包（zip/tar.gz）",
                分类="命令行",
                installer_markers_match_all=True,
                installer_markers=markers,
                href_exclude_substrings=["vscode", "vsix", "baseline", "musl", "darwin", "linux", "arm64"],
                installer_extensions=[".zip", ".tar.gz"],
                download_names=dl,
                save_name=save,
                **_repo(_kilo),
            )
        ],
    )

# --- Open WebUI Desktop ---
_ow = "open-webui/desktop"
_add(
    "windows",
    "01-AI.json",
    [
        _b(
            id="open_webui_desktop",
            简介="Open WebUI Desktop（本地 AI 聊天桌面端）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["open-webui-x64-setup", ".exe"],
            href_exclude_substrings=["arm64", "blockmap", "dmg", "mac", "yml"],
            windows_installer=True,
            download_names=["open-webui-x64-setup.exe"],
            save_name="open-webui-x64-setup.exe",
            run_installer=True,
            **_repo(_ow),
        )
    ],
)
_add(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="open_webui_desktop",
            简介="Open WebUI Desktop（macOS x64 dmg）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["open-webui-x64", ".dmg"],
            href_exclude_substrings=["arm64", "blockmap", "exe", "yml", "zip"],
            installer_extensions=[".dmg"],
            download_names=["open-webui-x64.dmg"],
            save_name="open-webui-x64.dmg",
            **_repo(_ow),
        )
    ],
)
_add(
    "linux",
    "01-AI.json",
    [
        _b(
            id="open_webui_desktop",
            简介="Open WebUI Desktop（Linux x86_64 AppImage）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["open-webui_x86_64", "AppImage"],
            href_exclude_substrings=["exe", "dmg", "blockmap", "yml", "arm64"],
            installer_extensions=[".AppImage"],
            download_names=["open-webui_x86_64.AppImage"],
            save_name="open-webui_x86_64.AppImage",
            **_repo(_ow),
        )
    ],
)

# --- Crush ---
_crush = "charmbracelet/crush"
for plat, shard, markers, dl, save in (
    (
        "windows",
        "01-AI.json",
        ["crush_", "Windows_x86_64.zip"],
        ["crush_{ver}_Windows_x86_64.zip"],
        "crush_{ver}_Windows_x86_64.zip",
    ),
    (
        "darwin",
        "01-AI.json",
        ["crush_", "Darwin_arm64.tar.gz"],
        ["crush_{ver}_Darwin_arm64.tar.gz"],
        "crush_{ver}_Darwin_arm64.tar.gz",
    ),
    (
        "linux",
        "01-AI.json",
        ["crush_", "Linux_x86_64.tar.gz"],
        ["crush_{ver}_Linux_x86_64.tar.gz"],
        "crush_{ver}_Linux_x86_64.tar.gz",
    ),
):
    _add(
        plat,
        shard,
        [
            _b(
                id="crush",
                简介="Crush（Charmbracelet 终端 AI 编程助手）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=markers,
                href_exclude_substrings=["i386", "armv7", "sbom", "sigstore", "rpm", "pkg.tar"],
                installer_extensions=[".zip", ".tar.gz"],
                download_names=dl,
                save_name=save,
                **_repo(_crush),
            )
        ],
    )

# --- Langflow ---
_lf = "langflow-ai/langflow"
_add(
    "windows",
    "01-AI.json",
    [
        _b(
            id="langflow",
            简介="Langflow（可视化 LLM 工作流桌面端）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["Langflow_", "x64_en-US.msi"],
            href_exclude_substrings=["dmg", "whl", "aarch64", "universal"],
            windows_installer=True,
            installer_extensions=[".msi"],
            download_names=["Langflow_{ver}_x64_en-US.msi"],
            save_name="Langflow_{ver}_x64_en-US.msi",
            run_installer=True,
            **_repo(_lf),
        )
    ],
)
_add(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="langflow",
            简介="Langflow（macOS universal dmg）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["Langflow_", "universal.dmg"],
            href_exclude_substrings=["msi", "whl", "x64_en"],
            installer_extensions=[".dmg"],
            download_names=["Langflow_{ver}_universal.dmg"],
            save_name="Langflow_{ver}_universal.dmg",
            **_repo(_lf),
        )
    ],
)

# --- TabbyML 本地推理服务 ---
_tm = "TabbyML/tabby"
for plat, shard, markers, dl, save in (
    (
        "windows",
        "01-AI.json",
        ["tabby_x86_64-windows-msvc-cpu", ".zip"],
        ["tabby_x86_64-windows-msvc-cpu.zip"],
        "tabby_x86_64-windows-msvc-cpu.zip",
    ),
    (
        "darwin",
        "01-AI.json",
        ["tabby_aarch64-apple-darwin", ".tar.gz"],
        ["tabby_aarch64-apple-darwin.tar.gz"],
        "tabby_aarch64-apple-darwin.tar.gz",
    ),
    (
        "linux",
        "01-AI.json",
        ["tabby_x86_64-manylinux_2_28.tar.gz"],
        ["tabby_x86_64-manylinux_2_28.tar.gz"],
        "tabby_x86_64-manylinux_2_28.tar.gz",
    ),
):
    _add(
        plat,
        shard,
        [
            _b(
                id="tabbyml",
                简介="Tabby（自托管 AI 代码补全服务 / 本地推理包）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=markers,
                href_exclude_substrings=["cuda", "vulkan", "cuda123", "cuda124"],
                installer_extensions=[".zip", ".tar.gz"],
                download_names=dl,
                save_name=save,
                **_repo(_tm),
            )
        ],
    )

# --- Void Editor ---
_void = "voideditor/binaries"
_add(
    "windows",
    "26-编辑器.json",
    [
        _b(
            id="void_editor",
            简介="Void（开源 AI 代码编辑器，基于 VS Code）",
            分类="编辑器",
            installer_markers_match_all=True,
            installer_markers=["VoidUserSetup-x64-", ".exe"],
            href_exclude_substrings=["arm64", "sha1", "sha256", "reh", "zip", "darwin", "linux"],
            windows_installer=True,
            download_names=["VoidUserSetup-x64-{ver}.exe"],
            save_name="VoidUserSetup-x64-{ver}.exe",
            run_installer=True,
            **_repo(_void),
        )
    ],
)
_add(
    "darwin",
    "26-编辑器.json",
    [
        _b(
            id="void_editor",
            简介="Void（macOS arm64 zip）",
            分类="编辑器",
            installer_markers_match_all=True,
            installer_markers=["Void-darwin-arm64-", ".zip"],
            href_exclude_substrings=["sha1", "sha256", "reh", "x64", "win32", "linux", "exe"],
            installer_extensions=[".zip"],
            download_names=["Void-darwin-arm64-{ver}.zip"],
            save_name="Void-darwin-arm64-{ver}.zip",
            **_repo(_void),
        )
    ],
)
_add(
    "linux",
    "26-编辑器.json",
    [
        _b(
            id="void_editor",
            简介="Void（Linux x64 tar.gz）",
            分类="编辑器",
            installer_markers_match_all=True,
            installer_markers=["Void-linux-x64-", ".tar.gz"],
            href_exclude_substrings=["sha1", "sha256", "reh", "darwin", "win32", "exe"],
            installer_extensions=[".tar.gz"],
            download_names=["Void-linux-x64-{ver}.tar.gz"],
            save_name="Void-linux-x64-{ver}.tar.gz",
            **_repo(_void),
        )
    ],
)

# --- Neovide ---
_nv = "neovide/neovide"
_add(
    "windows",
    "26-编辑器.json",
    [
        _b(
            id="neovide",
            简介="Neovide（Neovim 图形前端）",
            分类="编辑器",
            installer_markers=["neovide.exe.zip"],
            href_exclude_substrings=["dmg", "AppImage", "msi", "zsync", "darwin"],
            installer_extensions=[".zip"],
            download_names=["neovide.exe.zip"],
            save_name="neovide.exe.zip",
            **_repo(_nv),
        )
    ],
)
_add(
    "darwin",
    "26-编辑器.json",
    [
        _b(
            id="neovide",
            简介="Neovide（macOS Apple Silicon dmg）",
            分类="编辑器",
            installer_markers=["Neovide-aarch64-apple-darwin", ".dmg"],
            href_exclude_substrings=["x86_64", "AppImage", "exe", "msi", "zsync"],
            installer_extensions=[".dmg"],
            download_names=["Neovide-aarch64-apple-darwin.dmg"],
            save_name="Neovide-aarch64-apple-darwin.dmg",
            **_repo(_nv),
        )
    ],
)
_add(
    "linux",
    "26-编辑器.json",
    [
        _b(
            id="neovide",
            简介="Neovide（Linux AppImage）",
            分类="编辑器",
            installer_markers=["neovide.AppImage"],
            href_exclude_substrings=["dmg", "exe", "msi", "zsync", "darwin", ".tar"],
            installer_extensions=[".AppImage"],
            download_names=["neovide.AppImage"],
            save_name="neovide.AppImage",
            **_repo(_nv),
        )
    ],
)

# --- PearAI（Release 当前以 Linux tar 为主）---
_add(
    "linux",
    "26-编辑器.json",
    [
        _b(
            id="pearai",
            简介="PearAI（开源 AI 编辑器；GitHub Release 当前主要为 Linux tar.gz）",
            分类="编辑器",
            installer_markers=["PearAI-linux.tar.gz"],
            href_exclude_substrings=["beta", "sha"],
            installer_extensions=[".tar.gz"],
            download_names=["PearAI-linux.tar.gz"],
            save_name="PearAI-linux.tar.gz",
            **_repo("trypear/pearai-app"),
        )
    ],
)

# --- jan / gpt4all / lobe_chat：darwin & linux ---
_jan = "janhq/jan"
for plat, markers, dl, save in (
    ("darwin", ["Jan_", "universal.dmg"], ["Jan_{ver}_universal.dmg"], "Jan_{ver}_universal.dmg"),
    ("linux", ["Jan_", "amd64.AppImage"], ["Jan_{ver}_amd64.AppImage"], "Jan_{ver}_amd64.AppImage"),
):
    _add(
        plat,
        "01-AI.json",
        [
            _b(
                id="jan",
                简介="Jan（离线优先的本地 AI 聊天客户端）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=markers,
                href_exclude_substrings=["setup.exe", "deb", "zip", "arm64", "sha"],
                installer_extensions=[".dmg", ".AppImage"],
                download_names=dl,
                save_name=save,
                **_repo(_jan),
            )
        ],
    )

_ga = "nomic-ai/gpt4all"
_add(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="gpt4all",
            简介="GPT4All（本地运行 LLM 的桌面客户端）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["gpt4all-installer-macos-v", ".dmg"],
            href_exclude_substrings=["linux", "win", "arm", "sha"],
            installer_extensions=[".dmg"],
            download_names=["gpt4all-installer-macos-v{ver}.dmg"],
            save_name="gpt4all-installer-macos-v{ver}.dmg",
            **_repo(_ga),
        )
    ],
)
_add(
    "linux",
    "01-AI.json",
    [
        _b(
            id="gpt4all",
            简介="GPT4All（Linux x64 安装器 .run）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["gpt4all-installer-linux-v", ".run"],
            href_exclude_substrings=["macos", "win", "arm", "sha"],
            installer_extensions=[".run"],
            download_names=["gpt4all-installer-linux-v{ver}.run"],
            save_name="gpt4all-installer-linux-v{ver}.run",
            **_repo(_ga),
        )
    ],
)

_lb = "lobehub/lobe-chat"
_add(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="lobe_chat",
            简介="Lobe Chat Hub（多模型 AI 桌面客户端，LobeHub）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["LobeHub-", "x64.dmg"],
            href_exclude_substrings=["setup.exe", "AppImage", "arm64", "blockmap", "zip", "deb", "rpm"],
            installer_extensions=[".dmg"],
            download_names=["LobeHub-{ver}-x64.dmg"],
            save_name="LobeHub-{ver}-x64.dmg",
            **_repo(_lb),
        )
    ],
)
_add(
    "linux",
    "01-AI.json",
    [
        _b(
            id="lobe_chat",
            简介="Lobe Chat Hub（Linux AppImage）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["LobeHub-", ".AppImage"],
            href_exclude_substrings=["setup.exe", "dmg", "arm64", "blockmap", "deb", "rpm", "snap"],
            installer_extensions=[".AppImage"],
            download_names=["LobeHub-{ver}.AppImage"],
            save_name="LobeHub-{ver}.AppImage",
            **_repo(_lb),
        )
    ],
)

# --- VibeCoding manifest → 主 apps（需 apps/root.json 的 vibecoding_manifest_url）---
_editor = "编辑器"
_ai = "AI"

_manifest(
    "windows",
    "26-编辑器.json",
    "cursor",
    "Cursor（manifest：cursor-downloads + 官方 CDN）",
    _editor,
    windows_installer=True,
    save_name="CursorUserSetup-x64-{ver}.exe",
    process_name="Cursor.exe",
    kill_before_install=True,
    run_installer=True,
)
_manifest(
    "darwin",
    "26-编辑器.json",
    "cursor",
    "Cursor macOS universal zip（manifest）",
    _editor,
    installer_extensions=[".zip"],
    save_name="Cursor-darwin-universal.zip",
)
_manifest(
    "linux",
    "26-编辑器.json",
    "cursor",
    "Cursor（manifest 当前 linux 多为 null，勿盲目启用）",
    _editor,
)

for aid, intro_w, intro_d, intro_l, shard in (
    (
        "trae",
        "Trae IDE（manifest：api.trae.ai）",
        "Trae macOS dmg（manifest）",
        "Trae Linux（manifest）",
        "26-编辑器.json",
    ),
    (
        "trae_cn",
        "Trae 国内版（manifest：api.trae.cn）",
        "Trae CN dmg（manifest）",
        "Trae CN Linux（manifest）",
        "26-编辑器.json",
    ),
    (
        "trae_solo",
        "TRAE SOLO（manifest；Windows/Linux 常无包）",
        "TRAE SOLO dmg（manifest）",
        "TRAE SOLO（manifest）",
        "26-编辑器.json",
    ),
    (
        "qoder",
        "Qoder IDE（manifest：qoder.com CDN）",
        "Qoder dmg（manifest）",
        "Qoder Linux（manifest）",
        "26-编辑器.json",
    ),
    (
        "qoderwork",
        "QoderWork 桌面（manifest）",
        "QoderWork dmg（manifest）",
        "QoderWork（manifest）",
        "26-编辑器.json",
    ),
    (
        "workbuddy",
        "WorkBuddy（manifest：copilot.tencent.com）",
        "WorkBuddy mac zip（manifest）",
        "WorkBuddy（manifest；Linux 常 null）",
        "26-编辑器.json",
    ),
    (
        "codebuddy",
        "CodeBuddy 国际版（manifest：codebuddy.ai）",
        "CodeBuddy dmg（manifest）",
        "CodeBuddy Linux（manifest）",
        "26-编辑器.json",
    ),
    (
        "codebuddy_cn",
        "CodeBuddy 国内版（manifest：copilot.tencent.com）",
        "CodeBuddy CN dmg（manifest）",
        "CodeBuddy CN Linux（manifest）",
        "26-编辑器.json",
    ),
    (
        "antigravity",
        "Google Antigravity（manifest：edgedl CDN）",
        "Antigravity dmg（manifest）",
        "Antigravity Linux（manifest）",
        "26-编辑器.json",
    ),
):
    _manifest(
        "windows",
        shard,
        aid,
        intro_w,
        _editor,
        windows_installer=True,
        use_download_filename=True,
        run_installer=True,
    )
    _manifest("darwin", shard, aid, intro_d, _editor, installer_extensions=[".dmg", ".zip"])
    _manifest("linux", shard, aid, intro_l, _editor)

_manifest(
    "windows",
    "01-AI.json",
    "kiro",
    "Kiro CLI（manifest：prod.download.cli.kiro.dev）",
    _ai,
    version_tag_as_on_github=False,
    installer_extensions=[".msi"],
    windows_installer=True,
    save_name="kiro-cli-x86_64-pc-windows-msvc.msi",
    run_installer=True,
)
_manifest(
    "darwin",
    "01-AI.json",
    "kiro",
    "Kiro CLI macOS（manifest）",
    _ai,
    version_tag_as_on_github=False,
)
_manifest(
    "linux",
    "01-AI.json",
    "kiro",
    "Kiro CLI Linux（manifest）",
    _ai,
    version_tag_as_on_github=False,
)


def merge_batch(dry_run: bool = False) -> tuple[int, int]:
    added = skipped = 0
    for (plat, shard), apps in sorted(BATCH.items()):
        path = os.path.join(APPS, plat, shard)
        if not os.path.isfile(path):
            print("SKIP missing", path)
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        seen = {(a.get("id") or "").strip() for a in data if isinstance(a, dict)}
        for app in apps:
            aid = (app.get("id") or "").strip()
            if not aid or aid in seen:
                skipped += 1
                continue
            data.append(app)
            seen.add(aid)
            added += 1
        if not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
    return added, skipped


def main():
    dry = "--dry-run" in sys.argv
    added, skipped = merge_batch(dry_run=dry)
    print(f"{'dry-run' if dry else 'written'}: added {added}, skipped {skipped}")


if __name__ == "__main__":
    main()
