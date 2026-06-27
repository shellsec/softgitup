#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补全 AI 编程生态缺口：Copilot CLI 实装、Windsurf 占位、Goose 跨平台、SRC CLI 等。"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
PLATFORMS = ("windows", "darwin", "linux")

UPSERT: dict[tuple[str, str], list] = {}
BATCH: dict[tuple[str, str], list] = {}


def _upsert(plat: str, shard: str, apps: list):
    UPSERT.setdefault((plat, shard), []).extend(apps)


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


# --- 修复 github_copilot_cli（原误指向 microsoft/vscode 占位）---
_copilot = "github/copilot-cli"
_upsert(
    "windows",
    "01-AI.json",
    [
        _b(
            id="github_copilot_cli",
            简介="GitHub Copilot CLI（官方 github/copilot-cli，Windows x64 MSI）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["copilot-x64", ".msi"],
            href_exclude_substrings=["arm64", "darwin", "linux", "tgz", "win32-x64.zip"],
            windows_installer=True,
            installer_extensions=[".msi"],
            use_download_filename=True,
            save_name="copilot-x64.msi",
            run_installer=True,
            **_repo(_copilot),
        )
    ],
)
_upsert(
    "linux",
    "01-AI.json",
    [
        _b(
            id="github_copilot_cli",
            简介="GitHub Copilot CLI（Linux x64 glibc tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["copilot-linux-x64", ".tar.gz"],
            href_exclude_substrings=["musl", "arm64", "darwin", "windows", "tgz"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="copilot-linux-x64.tar.gz",
            **_repo(_copilot),
        )
    ],
)
_upsert(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="github_copilot_cli",
            简介="GitHub Copilot CLI（macOS Apple Silicon tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["copilot-darwin-arm64", ".tar.gz"],
            href_exclude_substrings=["x64", "linux", "windows", "tgz"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="copilot-darwin-arm64.tar.gz",
            **_repo(_copilot),
        )
    ],
)

# --- Goose 跨平台补全 + Windows save_name 修正 ---
_goose = "block/goose"
_upsert(
    "windows",
    "01-AI.json",
    [
        _b(
            id="goose_ai",
            简介="Goose（block 开源 AI 编程助手，Windows CLI zip）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["goose-x86_64-pc-windows-msvc", ".zip"],
            href_exclude_substrings=["Goose-win32", "darwin", "linux", "aarch64", "cuda"],
            installer_extensions=[".zip"],
            use_download_filename=True,
            save_name="goose-x86_64-pc-windows-msvc.zip",
            **_repo(_goose),
        )
    ],
)
_upsert(
    "linux",
    "01-AI.json",
    [
        _b(
            id="goose_ai",
            简介="Goose（Linux x86_64 gnu tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["goose-x86_64-unknown-linux-gnu", ".tar.gz"],
            href_exclude_substrings=["darwin", "windows", "aarch64", "vulkan", "bzip2"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="goose-x86_64-unknown-linux-gnu.tar.gz",
            **_repo(_goose),
        )
    ],
)
_upsert(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="goose_ai",
            简介="Goose（macOS Apple Silicon tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["goose-aarch64-apple-darwin", ".tar.gz"],
            href_exclude_substrings=["x86_64", "linux", "windows", "Goose-darwin", "bzip2"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="goose-aarch64-apple-darwin.tar.gz",
            **_repo(_goose),
        )
    ],
)
_add(
    "windows",
    "01-AI.json",
    [
        _b(
            id="goose_desktop",
            简介="Goose 桌面版（Windows Electron zip，Goose-win32-x64）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["Goose-win32-x64", ".zip"],
            href_exclude_substrings=["cuda", "darwin", "linux", "goose-x86_64"],
            installer_extensions=[".zip"],
            use_download_filename=True,
            save_name="Goose-win32-x64.zip",
            **_repo(_goose),
        )
    ],
)

# --- VS Code Copilot Chat 扩展 ---
_vscx = "microsoft/vscode-copilot-chat"
for plat in PLATFORMS:
    _add(
        plat,
        "01-AI.json",
        [
            _b(
                id="vscode_copilot_chat",
                简介="GitHub Copilot Chat（VS Code 扩展 .vsix）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=["GitHub.copilot-chat.", ".vsix"],
                href_exclude_substrings=["sbom", "sig"],
                installer_extensions=[".vsix"],
                use_download_filename=True,
                save_name="GitHub.copilot-chat.vsix",
                **_repo(_vscx),
            )
        ],
    )

# --- opencode-ai CLI（与 sst/opencode 桌面端不同仓）---
_ocli = "opencode-ai/opencode"
_add(
    "linux",
    "01-AI.json",
    [
        _b(
            id="opencode_cli",
            简介="OpenCode CLI（opencode-ai 独立 CLI；Linux x86_64 tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["opencode-linux-x86_64", ".tar.gz"],
            href_exclude_substrings=["arm64", "deb", "rpm", "mac", "checksums"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="opencode-linux-x86_64.tar.gz",
            **_repo(_ocli),
        )
    ],
)
_add(
    "darwin",
    "01-AI.json",
    [
        _b(
            id="opencode_cli",
            简介="OpenCode CLI（macOS arm64 tar.gz）",
            分类="AI",
            installer_markers_match_all=True,
            installer_markers=["opencode-mac-arm64", ".tar.gz"],
            href_exclude_substrings=["linux", "deb", "rpm", "x86", "checksums"],
            installer_extensions=[".tar.gz"],
            use_download_filename=True,
            save_name="opencode-mac-arm64.tar.gz",
            **_repo(_ocli),
        )
    ],
)

# --- Sourcegraph src-cli（Cody 生态命令行）---
_src = "sourcegraph/src-cli"
for plat, marker, excl, save in (
    (
        "windows",
        ["src-cli_", "_windows_amd64.tar.gz"],
        ["darwin", "linux", "checksums"],
        "src-cli_{ver}_windows_amd64.tar.gz",
    ),
    (
        "linux",
        ["src-cli_", "_linux_amd64.tar.gz"],
        ["darwin", "windows", "arm64", "checksums"],
        "src-cli_{ver}_linux_amd64.tar.gz",
    ),
    (
        "darwin",
        ["src-cli_", "_darwin_arm64.tar.gz"],
        ["linux", "windows", "amd64.tar", "checksums"],
        "src-cli_{ver}_darwin_arm64.tar.gz",
    ),
):
    _add(
        plat,
        "01-AI.json",
        [
            _b(
                id="sourcegraph_src_cli",
                简介=f"Sourcegraph src CLI（{plat}，Cody/源码搜索生态）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=marker,
                href_exclude_substrings=excl,
                installer_extensions=[".tar.gz"],
                download_names=[save],
                save_name=save,
                version_tag_as_on_github=False,
                **_repo(_src),
            )
        ],
    )

# --- Zed Codex ACP 桥接 ---
_acp = "zed-industries/codex-acp"
for plat, marker, excl, save in (
    (
        "windows",
        ["codex-acp-", "aarch64-pc-windows-msvc.zip"],
        ["linux", "darwin", "x86_64-pc"],
        "codex-acp-{ver}-aarch64-pc-windows-msvc.zip",
    ),
    (
        "linux",
        ["codex-acp-", "x86_64-unknown-linux-gnu.tar.gz"],
        ["windows", "darwin", "aarch64", "musl"],
        "codex-acp-{ver}-x86_64-unknown-linux-gnu.tar.gz",
    ),
    (
        "darwin",
        ["codex-acp-", "aarch64-apple-darwin.tar.gz"],
        ["windows", "linux", "x86_64-apple"],
        "codex-acp-{ver}-aarch64-apple-darwin.tar.gz",
    ),
):
    _add(
        plat,
        "01-AI.json",
        [
            _b(
                id="zed_codex_acp",
                简介=f"Zed Codex ACP（在 Zed 中使用 Codex，{plat}）",
                分类="AI",
                installer_markers_match_all=True,
                installer_markers=marker,
                href_exclude_substrings=excl,
                installer_extensions=[".zip", ".tar.gz"],
                download_names=[save],
                save_name=save,
                **_repo(_acp),
            )
        ],
    )

# --- Windsurf / Amazon Q：无 GitHub 安装包，仅占位索引 ---
for plat in PLATFORMS:
    _add(
        plat,
        "26-编辑器.json",
        [
            _b(
                id="windsurf",
                简介="Windsurf IDE（Codeium AI IDE；官网 codeium.com/windsurf 分发，GitHub 无桌面安装包；勿启用）",
                分类="编辑器",
                prefer_api_assets=False,
                releases_url="https://bgithub.xyz/Exafunction/Windsurf/releases",
                repo_path="Exafunction/Windsurf",
                url_hint="windsurf",
            )
        ],
    )
    _add(
        plat,
        "01-AI.json",
        [
            _b(
                id="amazon_q_cli",
                简介="Amazon Q Developer CLI（aws/amazon-q-developer-cli；Release 无附件，请用官方 curl/install 脚本；勿启用）",
                分类="AI",
                prefer_api_assets=False,
                releases_url="https://bgithub.xyz/aws/amazon-q-developer-cli/releases",
                repo_path="aws/amazon-q-developer-cli",
                url_hint="amazon-q",
            )
        ],
    )


def _apply_upsert(data: list, apps: list) -> int:
    n = 0
    index_by_id: dict[str, int] = {}
    for i, a in enumerate(data):
        if isinstance(a, dict) and a.get("id"):
            index_by_id[a["id"]] = i
    for app in apps:
        aid = (app.get("id") or "").strip()
        if not aid:
            continue
        if aid in index_by_id:
            merged = dict(data[index_by_id[aid]])
            merged.update(app)
            data[index_by_id[aid]] = merged
        else:
            data.append(app)
            index_by_id[aid] = len(data) - 1
        n += 1
    return n


def merge_all(dry_run: bool = False) -> tuple[int, int, int]:
    upserted = added = skipped = 0
    for mapping, is_upsert in ((UPSERT, True), (BATCH, False)):
        for (plat, shard), apps in sorted(mapping.items()):
            path = os.path.join(APPS, plat, shard)
            if not os.path.isfile(path):
                print("SKIP missing", path)
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("SKIP not array", path)
                continue
            if is_upsert:
                upserted += _apply_upsert(data, apps)
            else:
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
    return upserted, added, skipped


def main():
    dry = "--dry-run" in sys.argv
    u, a, s = merge_all(dry_run=dry)
    mode = "dry-run" if dry else "written"
    print(f"{mode}: upserted {u}, added {a}, skipped duplicate {s}")


if __name__ == "__main__":
    main()
