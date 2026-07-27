"""A 类月度工作台：旧版本 → 新版本，开源可直下，噪声标忽略。"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOFTWARE = ROOT / "software"
REPORTS = HERE / "reports"
OUT_HTML = REPORTS / "monthly_a.html"
OUT_JSON = REPORTS / "monthly_a.json"
OUT_DL_BAT = HERE / "monthly_a_download_github.bat"
OUT_SOFT_BAT = HERE / "monthly_a_download_soft_github.bat"
SOFT_MAP = HERE / "gh_soft_map.json"
GH_CACHE = ROOT / "software" / "gh-release-fetch" / "windows"

# 版本号候选（取最长/最靠前的合理命中）
VERSION_PATTERNS = [
    re.compile(r"(?i)\bv?\d+\.\d+\.\d+(?:\.\d+)?\b"),
    re.compile(r"(?i)\bv\d+\.\d+\b"),
    re.compile(r"(?i)\bbuild\s*[#:]?\s*(\d{3,})\b"),
    re.compile(r"(?<!\d)(20\d{2}[01]\d[0-3]\d)(?!\d)"),  # PotPlayer 260716 / 20260622
    re.compile(r"(?<!\d)(\d{6})(?!\d)"),  # 6 位日期型版本
]

NOISE_NEW = re.compile(
    r"(?i)安全验证|人机验证|just a moment|cloudflare|access denied|403 forbidden|"
    r"^\(无 title|\(无标题\)|^$|^error|^http",
)


def extract_version(title: str) -> str:
    text = (title or "").strip()
    if not text or text in ("(新增)", "(无标题)", "(无 title 标签)"):
        return "—"
    hits: list[str] = []
    for pat in VERSION_PATTERNS:
        for m in pat.finditer(text):
            g = m.group(1) if m.lastindex else m.group(0)
            hits.append(g.lstrip("vV"))
    if not hits:
        return "—"
    # 优先带点的语义版本，其次更长串
    dotted = [h for h in hits if "." in h]
    if dotted:
        return max(dotted, key=len)
    return max(hits, key=len)


def is_noise_change(old: str, new: str) -> bool:
    new = (new or "").strip()
    if NOISE_NEW.search(new):
        return True
    if len(new) < 4:
        return True
    # 新旧都抽不到版本且新标题极短 → 噪声
    if extract_version(old) == "—" and extract_version(new) == "—" and len(new) < 20:
        return True
    return False


def is_github_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return host in ("github.com", "www.github.com")


def load_diff_a() -> dict | None:
    path = REPORTS / "last_diff_a.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def load_soft_map() -> list[dict]:
    if not SOFT_MAP.exists():
        return []
    try:
        data = json.loads(SOFT_MAP.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return list(data.get("apps") or [])


def load_gh_app_status() -> dict[str, dict]:
    """gh_id -> {enabled, repo_path, id}"""
    try:
        from github_fetch_on_changes import load_gh_apps
    except Exception:
        return {}
    try:
        _, apps, _ = load_gh_apps()
    except Exception:
        return {}
    return {
        a.get("id", ""): {
            "id": a.get("id", ""),
            "enabled": bool(a.get("enabled", True)),
            "repo_path": a.get("repo_path", ""),
        }
        for a in apps
        if a.get("id")
    }


def normalize_ver(v: str) -> str:
    s = (v or "").strip()
    if not s or s == "—":
        return ""
    # tag 如 notepad-v3.8.0 / release-1.2.3 → 抽出版本
    extracted = extract_version(s)
    if extracted != "—":
        s = extracted
    else:
        s = s.lstrip("vV")
    # 去掉末尾多余 .0（8.9.7.0 → 8.9.7），保留 3.25.113.0 这类末位非零
    while s.endswith(".0") and s.count(".") >= 3:
        s = s[:-2]
    return s


def ver_parts(v: str) -> list:
    s = normalize_ver(v)
    if not s:
        return []
    parts: list = []
    for chunk in re.split(r"[.\-_]+", s):
        if not chunk:
            continue
        if chunk.isdigit():
            parts.append(int(chunk))
            continue
        m = re.match(r"(\d+)(.*)$", chunk)
        if m:
            parts.append(int(m.group(1)))
            if m.group(2):
                parts.append(m.group(2))
        else:
            parts.append(chunk)
    return parts


def version_cmp(a: str, b: str) -> int | None:
    """比较版本：-1 a<b，0 相等，1 a>b；无法比则 None。"""
    pa, pb = ver_parts(a), ver_parts(b)
    if not pa or not pb:
        return None
    n = max(len(pa), len(pb))
    for i in range(n):
        x = pa[i] if i < len(pa) else 0
        y = pb[i] if i < len(pb) else 0
        if isinstance(x, int) and isinstance(y, int):
            if x != y:
                return -1 if x < y else 1
            continue
        xs, ys = str(x), str(y)
        if xs != ys:
            return -1 if xs < ys else 1
    return 0


def win_file_version(path: Path) -> str:
    """读 PE FileVersion（Windows）；失败返回空串。"""
    if sys.platform != "win32" or not path.is_file():
        return ""
    try:
        import ctypes
        from ctypes import wintypes

        GetFileVersionInfoSizeW = ctypes.windll.version.GetFileVersionInfoSizeW
        GetFileVersionInfoW = ctypes.windll.version.GetFileVersionInfoW
        VerQueryValueW = ctypes.windll.version.VerQueryValueW

        size = GetFileVersionInfoSizeW(str(path), None)
        if not size:
            return ""
        data = ctypes.create_string_buffer(size)
        if not GetFileVersionInfoW(str(path), 0, size, data):
            return ""

        class VS_FIXEDFILEINFO(ctypes.Structure):
            _fields_ = [
                ("dwSignature", wintypes.DWORD),
                ("dwStrucVersion", wintypes.DWORD),
                ("dwFileVersionMS", wintypes.DWORD),
                ("dwFileVersionLS", wintypes.DWORD),
                ("dwProductVersionMS", wintypes.DWORD),
                ("dwProductVersionLS", wintypes.DWORD),
                ("dwFileFlagsMask", wintypes.DWORD),
                ("dwFileFlags", wintypes.DWORD),
                ("dwFileOS", wintypes.DWORD),
                ("dwFileType", wintypes.DWORD),
                ("dwFileSubtype", wintypes.DWORD),
                ("dwFileDateMS", wintypes.DWORD),
                ("dwFileDateLS", wintypes.DWORD),
            ]

        lptr = ctypes.c_void_p()
        llen = wintypes.UINT()
        if not VerQueryValueW(data, "\\", ctypes.byref(lptr), ctypes.byref(llen)):
            return ""
        info = ctypes.cast(lptr, ctypes.POINTER(VS_FIXEDFILEINFO)).contents
        major = info.dwFileVersionMS >> 16
        minor = info.dwFileVersionMS & 0xFFFF
        build = info.dwFileVersionLS >> 16
        rev = info.dwFileVersionLS & 0xFFFF
        if rev:
            return f"{major}.{minor}.{build}.{rev}"
        if build:
            return f"{major}.{minor}.{build}"
        return f"{major}.{minor}"
    except Exception:
        return ""


def find_local_exe(software_dir: str, local_exe: str) -> Path | None:
    base = SOFTWARE / software_dir
    if not base.is_dir():
        return None
    name = (local_exe or "").strip()
    if not name:
        return None
    direct = base / name
    if direct.is_file():
        return direct
    # 在子目录里找同名（如 system_good/.../Ditto.exe）
    matches = list(base.rglob(name))
    files = [p for p in matches if p.is_file()]
    if not files:
        return None
    files.sort(key=lambda p: (len(p.parts), str(p).lower()))
    return files[0]


def local_version_from_archives(software_dir: str, gh_id: str) -> str:
    """目录内只有压缩包时，从文件名抽版本（如 lx-music-desktop-v2.12.2…7z）。"""
    base = SOFTWARE / software_dir
    if not base.is_dir():
        return ""
    aliases = {
        "lx_music_desktop": ("lx-music", "lx_music"),
        "ditto": ("ditto",),
        "win11_debloat": ("win11debloat", "debloat"),
        "win11_debloat_scavin": ("win11debloat", "debloat"),
        "7zip": ("7z", "7-zip"),
        "notepadplusplus": ("npp", "notepad++"),
        "notepad_minusminus": ("notepad--",),
        "win_memory_cleaner": ("winmemory",),
        "everything_cli": ("everything",),
    }
    keys = aliases.get(gh_id, ())
    if not keys:
        return ""
    best = ""
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".7z", ".zip", ".rar", ".exe", ".msi", ".ps1"}:
            continue
        name = p.name.lower()
        if not any(k in name for k in keys):
            continue
        ver = normalize_ver(extract_version(p.name))
        if ver and len(ver) >= len(best):
            best = ver
    return best


def local_version(software_dir: str, local_exe: str, gh_id: str = "") -> str:
    path = find_local_exe(software_dir, local_exe)
    if path:
        ver = normalize_ver(win_file_version(path))
        if ver:
            return ver
    # lx-music 等可能只在 system_good 里有压缩包
    for folder in {software_dir, "system_good"}:
        arch = local_version_from_archives(folder, gh_id)
        if arch:
            return arch
    return "—"


def fetch_github_latest(repo_path: str, cache: dict[str, str]) -> str:
    repo = (repo_path or "").strip().strip("/")
    if not repo:
        return "—"
    key = repo.lower()
    if key in cache:
        return cache[key]
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "softgitup-monthly-a-board",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        tag = normalize_ver(str(data.get("tag_name") or ""))
        name_ver = normalize_ver(str(data.get("name") or ""))
        ver = tag or name_ver
        cache[key] = ver or "—"
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        cache[key] = "—"
    return cache[key]


def cache_download_hint(gh_id: str) -> str:
    """从 gh-release-fetch/windows 文件名猜刚下的版本（可选提示）。"""
    if not GH_CACHE.is_dir():
        return ""
    needle = (gh_id or "").replace("_", "").lower()
    best = ""
    for p in GH_CACHE.iterdir():
        if not p.is_file():
            continue
        name = p.name.lower()
        if needle and needle[:6] not in name.replace("-", "").replace("_", ""):
            # 宽松：用常见关键字
            pass
        ver = extract_version(p.name)
        if ver != "—" and len(ver) >= len(best):
            # 只在文件名能明显关联时采用
            aliases = {
                "7zip": ("7z", "7-zip"),
                "ditto": ("ditto",),
                "notepadplusplus": ("npp.", "notepad"),
                "notepad_minusminus": ("notepad--", "notepad-"),
                "lx_music_desktop": ("lx-music", "lx_music"),
                "win_memory_cleaner": ("winmemory", "memorycleaner", "setup-"),
                "win11_debloat": ("get.ps1", "win11debloat"),
                "win11_debloat_scavin": ("get.ps1", "win11debloat"),
                "everything_cli": ("everything",),
            }
            keys = aliases.get(gh_id, (gh_id.replace("_", ""),))
            if any(k in name for k in keys):
                best = ver
    return best


def version_status(local: str, latest: str) -> str:
    """same | update | local_newer | unknown"""
    cmp = version_cmp(local, latest)
    if cmp is None:
        return "unknown"
    if cmp == 0:
        return "same"
    if cmp < 0:
        return "update"
    return "local_newer"


def build_soft_catalog() -> list[dict]:
    status = load_gh_app_status()
    api_cache: dict[str, str] = {}
    rows: list[dict] = []
    for item in load_soft_map():
        gid = item.get("gh_id", "")
        st = status.get(gid, {})
        enabled = bool(st.get("enabled")) if st else False
        repo = st.get("repo_path") or item.get("repo_path", "")
        sw = item.get("software_dir", "")
        local = local_version(sw, item.get("local_exe", ""), gid)
        latest = fetch_github_latest(repo, api_cache)
        cached = cache_download_hint(gid)
        vstat = version_status(local, latest)
        rows.append(
            {
                "software_dir": sw,
                "gh_id": gid,
                "repo_path": repo,
                "enabled": enabled,
                "note": item.get("note", ""),
                "github_url": f"https://github.com/{repo}" if repo else "",
                "local_version": local,
                "latest_version": latest,
                "cache_version": cached,
                "version_status": vstat,
                "needs_update": vstat == "update",
            }
        )
    return rows


def match_gh_apps(urls: list[str]) -> dict[str, list[dict]]:
    """url -> [{id, enabled, repo_path}, ...]"""
    try:
        from github_fetch_on_changes import build_repo_index, github_repo_key, load_gh_apps
    except Exception:
        return {}

    try:
        _, apps, _ = load_gh_apps()
    except Exception:
        return {}

    index = build_repo_index(apps)
    out: dict[str, list[dict]] = {}
    for url in urls:
        repo = github_repo_key(url)
        if not repo:
            continue
        matched = index.get(repo, [])
        if matched:
            out[url] = [
                {
                    "id": a.get("id", ""),
                    "enabled": bool(a.get("enabled", True)),
                    "repo_path": a.get("repo_path", ""),
                }
                for a in matched
                if a.get("id")
            ]
    return out


def build_rows() -> list[dict]:
    diff = load_diff_a()
    if not diff:
        return []

    items = list(diff.get("title_changed") or [])
    urls = [i.get("url", "") for i in items if i.get("url")]
    gh_map = match_gh_apps(urls)

    rows: list[dict] = []
    for item in items:
        url = item.get("url", "")
        old = str(item.get("old", ""))
        new = str(item.get("new", ""))
        software = item.get("software") or []
        domain = item.get("domain") or urlparse(url).netloc
        noise = is_noise_change(old, new)
        old_ver = extract_version(old)
        new_ver = extract_version(new)
        gh_apps = gh_map.get(url, [])
        enabled_ids = [a["id"] for a in gh_apps if a.get("enabled")]
        disabled_ids = [a["id"] for a in gh_apps if not a.get("enabled")]

        if noise:
            action = "ignore"
            action_label = "忽略（噪声/验证页）"
        elif enabled_ids:
            action = "github_download"
            action_label = f"开源·可直下 ({', '.join(enabled_ids)})"
        elif disabled_ids:
            action = "github_disabled"
            action_label = f"开源·未启用 ({', '.join(disabled_ids)})"
        elif is_github_url(url):
            action = "github_unmapped"
            action_label = "开源·未配置 gh-release-fetch"
        else:
            action = "manual"
            action_label = "手工打开页面"

        rows.append(
            {
                "url": url,
                "software": software,
                "domain": domain,
                "old_title": old,
                "new_title": new,
                "old_version": old_ver,
                "new_version": new_ver,
                "noise": noise,
                "action": action,
                "action_label": action_label,
                "gh_app_ids": enabled_ids,
                "gh_disabled_ids": disabled_ids,
            }
        )
    return rows


def write_download_bat(rows: list[dict]) -> Path | None:
    ids: list[str] = []
    for r in rows:
        if r["action"] == "github_download":
            for aid in r["gh_app_ids"]:
                if aid not in ids:
                    ids.append(aid)
    if not ids:
        if OUT_DL_BAT.exists():
            OUT_DL_BAT.unlink()
        return None

    content = f"""@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo A 类月度 · 下载本月 GitHub 变化（只下载不安装）
echo ========================================
echo apps: {' '.join(ids)}
echo 会先清空再下载到 software\\gh-release-fetch\\windows\\（gitignore）
echo.
python github_fetch_on_changes.py --scope a
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (echo 完成。包在 windows\\ 目录，请手工覆盖到 software\\) else (echo [错误] 见上方输出)
pause
exit /b %RC%
"""
    OUT_DL_BAT.write_text(content, encoding="utf-8")
    return OUT_DL_BAT


def write_soft_download_bat(catalog: list[dict]) -> Path | None:
    ids = [c["gh_id"] for c in catalog if c.get("enabled") and c.get("gh_id")]
    if not ids:
        if OUT_SOFT_BAT.exists():
            OUT_SOFT_BAT.unlink()
        return None
    content = f"""@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo software/ 开源包 · 只下载不安装
echo ========================================
echo apps: {' '.join(ids)}
echo 映射: gh_soft_map.json （只读引用 gh-release-fetch）
echo 会先清空再下载到 software\\gh-release-fetch\\windows\\（gitignore，不入库）
echo.
python github_fetch_on_changes.py --soft-map
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (echo 完成。包在 software\\gh-release-fetch\\windows\\ ，请手工覆盖到 software\\) else (echo [错误] 见上方输出)
pause
exit /b %RC%
"""
    OUT_SOFT_BAT.write_text(content, encoding="utf-8")
    return OUT_SOFT_BAT


def render_html(rows: list[dict], compared_at: str, catalog: list[dict] | None = None) -> str:
    catalog = catalog or []
    actionable = [r for r in rows if not r["noise"]]
    github_ready = [r for r in rows if r["action"] == "github_download"]
    manual = [r for r in rows if r["action"] == "manual"]
    noise = [r for r in rows if r["noise"]]
    soft_on = [c for c in catalog if c.get("enabled")]
    soft_off = [c for c in catalog if not c.get("enabled")]
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def row_html(r: dict) -> str:
        sw = "、".join(r["software"]) if r["software"] else "—"
        url_e = html.escape(r["url"])
        cls = "noise" if r["noise"] else ("gh" if r["action"] == "github_download" else "manual")
        old_v = html.escape(r["old_version"])
        new_v = html.escape(r["new_version"])
        ver_arrow = f"<code>{old_v}</code> → <code class='newv'>{new_v}</code>"
        if r["noise"]:
            action_cell = f"<span class='pill noise'>{html.escape(r['action_label'])}</span>"
        elif r["action"] == "github_download":
            action_cell = (
                f"<span class='pill gh'>{html.escape(r['action_label'])}</span>"
                f"<div class='hint'>运行 monthly_a_download_github.bat</div>"
            )
        else:
            action_cell = (
                f"<span class='pill man'>{html.escape(r['action_label'])}</span> "
                f"<a class='btn' href='{url_e}' target='_blank' rel='noopener'>打开</a>"
            )
        return f"""
        <tr class="{cls}">
          <td>{html.escape(sw)}</td>
          <td class="ver">{ver_arrow}</td>
          <td><span class="dom">{html.escape(str(r['domain']))}</span></td>
          <td class="act">{action_cell}</td>
          <td class="titles">
            <div><span class="lab old">旧</span> {html.escape(r['old_title'][:160])}</div>
            <div><span class="lab new">新</span> {html.escape(r['new_title'][:160])}</div>
            <a class="link" href="{url_e}" target="_blank" rel="noopener">{url_e}</a>
          </td>
        </tr>"""

    body_rows = "\n".join(row_html(r) for r in rows) if rows else (
        "<tr><td colspan='5' class='empty'>暂无 A 类标题变化。先跑 monthly_check.bat（带 --compare）。</td></tr>"
    )

    dl_hint = (
        f"<p class='cta'>本月标题变化中开源可直下 <b>{len(github_ready)}</b> 项 → "
        f"<code>monthly_a_download_github.bat</code></p>"
        if github_ready
        else "<p class='muted'>本月标题变化中无「开源·可直下」项。</p>"
    )

    soft_cta = (
        f"<p class='cta'>software/ 装机开源已启用 <b>{len(soft_on)}</b> 项 → 双击 "
        f"<code>monthly_a_download_soft_github.bat</code>（随时可拉最新 Release）</p>"
        if soft_on
        else "<p class='muted'>gh_soft_map.json 中尚无 enabled 的装机开源。</p>"
    )

    def soft_row(c: dict) -> str:
        status = (
            "<span class='pill gh'>可直下</span>"
            if c.get("enabled")
            else "<span class='pill noise'>未启用</span>"
        )
        vstat = c.get("version_status") or "unknown"
        if vstat == "update":
            status += " <span class='pill man'>可更新</span>"
        elif vstat == "same":
            status += " <span class='pill gh'>已是最新</span>"
        elif vstat == "local_newer":
            status += " <span class='pill noise'>本地较新</span>"
        repo = html.escape(c.get("repo_path") or "—")
        note = html.escape(c.get("note") or "")
        note_html = f"<div class='hint'>{note}</div>" if note else ""
        gh = c.get("github_url") or "#"
        local_v = html.escape(c.get("local_version") or "—")
        latest_v = html.escape(c.get("latest_version") or "—")
        latest_cls = "newv" if vstat == "update" else ""
        cache_v = c.get("cache_version") or ""
        cache_html = (
            f"<div class='hint'>缓存包: {html.escape(cache_v)}</div>" if cache_v else ""
        )
        return f"""
        <tr class="{'gh' if c.get('enabled') else 'noise'}">
          <td><code>{html.escape(c.get('software_dir') or '—')}</code>
            <div class='hint'><code>{html.escape(c.get('gh_id') or '—')}</code></div></td>
          <td class="ver"><code>{local_v}</code></td>
          <td class="ver"><code class="{latest_cls}">{latest_v}</code>{cache_html}</td>
          <td><a href="{html.escape(gh)}" target="_blank" rel="noopener">{repo}</a>{note_html}</td>
          <td>{status}</td>
        </tr>"""

    soft_body = "\n".join(soft_row(c) for c in catalog) if catalog else (
        "<tr><td colspan='5' class='empty'>无 gh_soft_map.json 映射。</td></tr>"
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>A 类月度工作台 · 旧版本 → 新版本</title>
  <style>
    :root {{ --bg:#f1f5f9; --card:#fff; --text:#0f172a; --muted:#64748b; --line:#e2e8f0;
      --gh:#166534; --man:#9a3412; --noise:#64748b; --accent:#2563eb; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family:"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
      background:var(--bg); color:var(--text); line-height:1.5; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 24px 18px 48px; }}
    .hero {{ background: linear-gradient(135deg,#0f766e,#2563eb); color:#fff;
      border-radius:14px; padding:22px 26px; margin-bottom:18px; }}
    .hero h1 {{ margin:0 0 6px; font-size:1.35rem; }}
    .hero p {{ margin:0; opacity:.92; font-size:.92rem; }}
    .stats {{ display:flex; flex-wrap:wrap; gap:10px; margin:16px 0; }}
    .stat {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
      padding:10px 14px; min-width:100px; }}
    .stat b {{ display:block; font-size:1.25rem; }}
    .stat span {{ color:var(--muted); font-size:.8rem; }}
    .cta {{ background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46;
      padding:10px 14px; border-radius:10px; }}
    table {{ width:100%; border-collapse:collapse; background:var(--card);
      border-radius:12px; overflow:hidden; border:1px solid var(--line); }}
    th, td {{ padding:10px 12px; border-bottom:1px solid var(--line); text-align:left;
      vertical-align:top; font-size:.88rem; }}
    th {{ background:#f8fafc; color:var(--muted); font-weight:600; }}
    tr.noise {{ opacity:.55; }}
    tr.gh {{ background:#f0fdf4; }}
    .ver code {{ background:#f1f5f9; padding:1px 6px; border-radius:4px; }}
    .ver .newv {{ background:#dcfce7; color:var(--gh); font-weight:700; }}
    .pill {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:.75rem; font-weight:600; }}
    .pill.gh {{ background:#dcfce7; color:var(--gh); }}
    .pill.man {{ background:#ffedd5; color:var(--man); }}
    .pill.noise {{ background:#f1f5f9; color:var(--noise); }}
    .btn {{ display:inline-block; margin-left:6px; padding:2px 8px; border-radius:6px;
      background:var(--accent); color:#fff; text-decoration:none; font-size:.75rem; }}
    .hint {{ color:var(--muted); font-size:.72rem; margin-top:4px; }}
    .lab {{ display:inline-block; font-size:.68rem; font-weight:700; padding:0 5px;
      border-radius:4px; margin-right:4px; }}
    .lab.old {{ background:#fee2e2; color:#991b1b; }}
    .lab.new {{ background:#dcfce7; color:#166534; }}
    .titles {{ color:#334155; max-width:420px; }}
    .titles .link {{ display:block; margin-top:4px; font-size:.75rem; word-break:break-all; }}
    .dom {{ color:var(--muted); font-size:.8rem; }}
    .empty {{ text-align:center; color:var(--muted); padding:28px; }}
    .muted {{ color:var(--muted); }}
    .nav a {{ color:#fff; margin-right:12px; }}
    h2 {{ font-size:1.05rem; margin:22px 0 10px; }}
    footer {{ margin-top:18px; color:var(--muted); font-size:.8rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>A 类月度工作台 · 旧版本 → 新版本</h1>
      <p>只盯 config.json 同步软件。装机开源随时可直下；423down/网盘仍手工。变化≠必须更新。</p>
      <p class="nav" style="margin-top:10px">
        <a href="index.html">完整报告</a>
        <a href="#soft-oss">装机开源</a>
        <a href="../monthly_check.bat">跑 A 类快检</a>
      </p>
    </header>

    <div class="stats">
      <div class="stat"><b>{len(rows)}</b><span>标题变化</span></div>
      <div class="stat"><b>{len(actionable)}</b><span>待处理</span></div>
      <div class="stat"><b>{len(github_ready)}</b><span>本月开源变化</span></div>
      <div class="stat"><b>{len(soft_on)}</b><span>装机开源可直下</span></div>
      <div class="stat"><b>{len(manual)}</b><span>需手工</span></div>
      <div class="stat"><b>{len(noise)}</b><span>噪声忽略</span></div>
    </div>

    {soft_cta}
    {dl_hint}
    <p class="muted">比对时间: {html.escape(compared_at or "—")} · 页面生成: {html.escape(generated)}</p>

    <h2 id="soft-oss">software/ 装机开源（可随时直下）</h2>
    <p class="muted">本地版本读 <code>software/</code> 内 exe；最新版查 GitHub Release API。映射见 <code>gh_soft_map.json</code>；下载写入缓存后再手工同步到 software/。</p>
    <table>
      <thead>
        <tr>
          <th>software/ 目录</th>
          <th>本地版本</th>
          <th>最新 Release</th>
          <th>GitHub</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        {soft_body}
      </tbody>
    </table>
    {"<p class='muted'>未启用 " + str(len(soft_off)) + " 项（可在 apps/windows JSON 设 enabled=true）。</p>" if soft_off else ""}

    <h2>本月 A 类标题变化</h2>
    <table>
      <thead>
        <tr>
          <th>软件目录</th>
          <th>旧版本 → 新版本</th>
          <th>来源</th>
          <th>动作</th>
          <th>标题对照</th>
        </tr>
      </thead>
      <tbody>
        {body_rows}
      </tbody>
    </table>
    <footer>soft_page_check/reports/monthly_a.html · 由 monthly_a_board.py / report_html 生成</footer>
  </div>
</body>
</html>
"""


def build_monthly_a() -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    diff = load_diff_a()
    rows = build_rows()
    catalog = build_soft_catalog()
    compared_at = (diff or {}).get("compared_at", "")
    write_download_bat(rows)
    write_soft_download_bat(catalog)
    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "compared_at": compared_at,
        "count": len(rows),
        "github_download": sum(1 for r in rows if r["action"] == "github_download"),
        "manual": sum(1 for r in rows if r["action"] == "manual"),
        "noise": sum(1 for r in rows if r["noise"]),
        "soft_catalog": catalog,
        "soft_enabled": sum(1 for c in catalog if c.get("enabled")),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_HTML.write_text(render_html(rows, compared_at, catalog), encoding="utf-8")
    return OUT_HTML


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    path = build_monthly_a()
    data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    print(f"A 类月度工作台: {path}")
    print(
        f"  变化 {data['count']} · 本月开源变化 {data['github_download']} · "
        f"装机开源可直下 {data.get('soft_enabled', 0)} · "
        f"手工 {data['manual']} · 噪声 {data['noise']}"
    )
    if OUT_SOFT_BAT.exists():
        print(f"  装机开源下载: {OUT_SOFT_BAT.name}")
    if OUT_DL_BAT.exists():
        print(f"  本月变化下载: {OUT_DL_BAT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
