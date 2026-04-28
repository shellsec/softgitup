#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GH Release Fetch（GitHub 发行版拉取工具）：按 GitHub Releases 解析版本并下载资产。
配置可为单文件 apps.json，或 apps/ 目录（root.json + windows|darwin|linux 分片目录）。
也可用 --apps-dir 指向另一套同级目录（如 VibeCodingToolsDown/，内含 root.json 与分片），与 apps/ 互不合并。
resolve_via=github_pages_manifest：从 root.json 的 vibecoding_manifest_url（本地路径或 https raw）读取 manifest.json，可与 CI 提交到 main 的 manifest 或 gh-pages 配套。
合并后仍使用 platforms.windows / darwin / linux；可用 --platform 覆盖当前系统。
条目的「简介」「分类」仅供人阅读，脚本不解析。
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

try:
    import urllib3
except ImportError:
    urllib3 = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "apps.json")
APPS_DIR = os.path.join(SCRIPT_DIR, "apps")
APPS_ROOT_FRAGMENT = os.path.join(APPS_DIR, "root.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("update_log.txt", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

DEFAULT_RELEASE_PAGE_MIRRORS = [
    "https://github.com",
]


def resolve_tls_verify(cfg, insecure_cli):
    """默认校验证书；--insecure 或 apps.json 根级 ssl_verify=false 时关闭（镜像证书过期等场景）。"""
    if insecure_cli:
        return False
    if cfg.get("ssl_verify") is False:
        return False
    return True


def configure_insecure_requests(verify):
    if verify or urllib3 is None:
        return
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _load_json_array_file(path, label):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "apps" in data:
        data = data["apps"]
    if not isinstance(data, list):
        raise ValueError("%s：必须是 JSON 数组，或 {\"apps\": []} 形式" % label)
    return data


def _merge_platform_json_dir(platform_dir, platform_label):
    """合并 apps/<platform>/*.json 分片；同一平台内 id 必须唯一。"""
    merged = []
    seen_ids = set()
    if not os.path.isdir(platform_dir):
        return merged
    for name in sorted(os.listdir(platform_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(platform_dir, name)
        chunk = _load_json_array_file(path, path)
        for app in chunk:
            aid = (app.get("id") or "").strip()
            if not aid:
                raise ValueError("%s 中有缺少 id 的条目" % path)
            if aid in seen_ids:
                raise ValueError(
                    "重复的 id %r（出现在多个 %s 分片中）" % (aid, platform_label)
                )
            seen_ids.add(aid)
        merged.extend(chunk)
    return merged


def _load_platform_apps(apps_dir, platform_key):
    """
    优先读取 apps/<platform_key>/*.json（按文件名排序合并）；
    若该目录不存在或无 .json 分片，则回退到 apps/<platform_key>.json 单文件。
    """
    dir_path = os.path.join(apps_dir, platform_key)
    single_path = os.path.join(apps_dir, "%s.json" % platform_key)
    if os.path.isdir(dir_path):
        json_names = [n for n in os.listdir(dir_path) if n.endswith(".json")]
        if json_names:
            return _merge_platform_json_dir(dir_path, platform_key)
    if os.path.isfile(single_path):
        return _load_json_array_file(single_path, single_path)
    return []


def load_config_from_apps_dir(apps_dir):
    root_path = os.path.join(apps_dir, "root.json")
    if not os.path.isfile(root_path):
        raise FileNotFoundError(f"缺少 {root_path}")
    with open(root_path, encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg, dict):
        raise ValueError("apps/root.json 必须是 JSON 对象")
    cfg.setdefault("platforms", {})
    for key in ("windows", "darwin", "linux"):
        cfg["platforms"][key] = _load_platform_apps(apps_dir, key)
    logger.info(
        "已从配置目录合并：%s — windows %s 项，darwin %s 项，linux %s 项",
        apps_dir,
        len(cfg["platforms"].get("windows") or []),
        len(cfg["platforms"].get("darwin") or []),
        len(cfg["platforms"].get("linux") or []),
    )
    cfg["_apps_config_root"] = os.path.abspath(apps_dir)
    return cfg


def load_config(apps_dir=None):
    """
    apps_dir: 可选，为含 root.json 的配置根目录（相对路径时相对本脚本所在目录）。
    默认使用 apps/（存在 apps/root.json 时）或 apps.json。
    """
    if apps_dir:
        path = apps_dir
        if not os.path.isabs(path):
            path = os.path.normpath(os.path.join(SCRIPT_DIR, path))
        root_path = os.path.join(path, "root.json")
        if not os.path.isfile(root_path):
            raise FileNotFoundError("缺少 %s（--apps-dir 须指向含 root.json 的目录）" % root_path)
        return load_config_from_apps_dir(path)
    if os.path.isfile(APPS_ROOT_FRAGMENT):
        return load_config_from_apps_dir(APPS_DIR)
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError(
        "缺少配置：请放置 apps.json，或创建 apps/root.json 与 apps/windows/*.json"
    )


def github_headers():
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }


def uses_github_pages_manifest(app):
    return (app.get("resolve_via") or "").strip().lower() == "github_pages_manifest"


def _load_vibecoding_manifest(url_or_path, verify=True, apps_config_root=None):
    """加载 manifest.json（HTTPS URL；本地路径相对 --apps-dir 配置根，见 cfg _apps_config_root）。"""
    raw = (url_or_path or "").strip()
    if not raw:
        raise ValueError("manifest URL 为空")
    if raw.startswith("http://") or raw.startswith("https://"):
        response = requests.get(raw, headers=github_headers(), timeout=45, verify=verify)
        response.raise_for_status()
        return response.json()
    path = raw
    if not os.path.isabs(path):
        rel = path.lstrip("./\\")
        if apps_config_root:
            path = os.path.normpath(os.path.join(apps_config_root, rel))
        else:
            path = os.path.normpath(os.path.join(SCRIPT_DIR, rel))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve_github_pages_manifest(app, verify, cfg, platform_key):
    raw = (app.get("manifest_url") or "").strip() or (cfg.get("vibecoding_manifest_url") or "").strip()
    data = _load_vibecoding_manifest(
        raw, verify=verify, apps_config_root=cfg.get("_apps_config_root")
    )
    mid = (app.get("manifest_item_id") or app["id"]).strip()
    item = None
    for it in data.get("items") or []:
        if (it.get("id") or "").strip() == mid:
            item = it
            break
    if not item:
        raise RuntimeError("manifest 中找不到 id=%r" % mid)
    plat = platform_key or detect_platform_key()
    blk = (item.get("downloads") or {}).get(plat)
    if not blk or not (blk.get("url") or "").strip():
        raise RuntimeError("manifest 中 %s / %s 无可用下载地址（参见 manifest notes）" % (mid, plat))
    url = blk["url"].strip()
    vtag = (item.get("version_tag") or "").strip()
    vplain = (item.get("version") or "").strip()
    if app.get("version_tag_as_on_github") and vtag:
        version = vtag
    elif vplain and not str(vplain).startswith("v"):
        version = "v" + vplain.lstrip("v")
    else:
        version = vplain or "v0"
    return version, url


def canonical_releases_url(repo_path, base_url="https://github.com"):
    repo = repo_path.strip("/")
    return f"{base_url.rstrip('/')}/{repo}/releases"


def normalize_release_mirror_base(url):
    if not url:
        return None
    base = url.strip().rstrip("/")
    if not base.startswith("http://") and not base.startswith("https://"):
        base = "https://" + base
    return base


def release_page_candidates(app, cfg=None):
    urls = []
    seen = set()

    def add(url):
        if not url:
            return
        if url not in seen:
            seen.add(url)
            urls.append(url)

    add((app.get("releases_url") or "").strip())

    for base in (cfg or {}).get("release_page_mirrors") or []:
        normalized = normalize_release_mirror_base(base)
        if normalized:
            add(canonical_releases_url(app["repo_path"], normalized))

    for base in DEFAULT_RELEASE_PAGE_MIRRORS:
        add(canonical_releases_url(app["repo_path"], base))

    return urls


def request_release_page(app, verify=True, cfg=None):
    errors = []
    if cfg is None:
        cfg = load_config()
    for url in release_page_candidates(app, cfg):
        try:
            logger.info("[%s] 正在检查最新版本: %s", app["id"], url)
            response = requests.get(url, headers=github_headers(), timeout=30, verify=verify)
            response.raise_for_status()
            return url, response.text
        except Exception as e:
            errors.append((url, e))
            logger.warning("[%s] 发布页获取失败: %s -> %s", app["id"], url, e)

    detail = " | ".join(f"{url}: {err}" for url, err in errors) if errors else "无候选地址"
    raise RuntimeError(f"所有发布页来源均失败：{detail}")


def api_latest_release_url(app):
    repo = app["repo_path"].strip("/")
    return f"https://api.github.com/repos/{repo}/releases/latest"


def api_release_tag_url(app, version):
    repo = app["repo_path"].strip("/")
    encoded = urllib.parse.quote((version or "").strip(), safe="")
    return f"https://api.github.com/repos/{repo}/releases/tags/{encoded}"


def extract_version_for_app(app, version):
    version = (version or "").strip()
    if not version:
        raise RuntimeError("版本号为空")
    if app.get("version_tag_as_on_github"):
        return version
    if not version.startswith("v"):
        return "v" + version
    return version


def asset_targets_app(asset_name, asset_url, app):
    href = asset_url or asset_name or ""
    text = asset_name or ""
    if link_targets_app(href, text, app):
        return True
    markers = app.get("installer_markers") or []
    if markers:
        return False
    hint = (app.get("url_hint") or app["id"]).lower()
    if hint not in href.lower() and hint not in text.lower():
        return False
    exts = installer_extensions(app)
    base = href.split("?", 1)[0].lower()
    if exts and not any(base.endswith(e) for e in exts):
        return False
    return href_allowed_for_app(href, app)


def fetch_release_via_api(app, verify=True, version_hint=None):
    url = api_release_tag_url(app, version_hint) if version_hint else api_latest_release_url(app)
    logger.info("[%s] 尝试使用 GitHub API: %s", app["id"], url)
    response = requests.get(
        url,
        headers={
            **github_headers(),
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
        verify=verify,
    )
    response.raise_for_status()
    payload = response.json()
    version = extract_version_for_app(app, payload.get("tag_name") or payload.get("name") or "")
    download_url = None
    for asset in payload.get("assets") or []:
        asset_url = asset.get("browser_download_url") or ""
        asset_name = asset.get("name") or ""
        if asset_targets_app(asset_name, asset_url, app):
            download_url = asset_url
            logger.info("[%s] 从 GitHub API 中找到下载链接: %s", app["id"], download_url)
            break
    logger.info("[%s] 通过 GitHub API 找到最新版本: %s", app["id"], version)
    return version, download_url


def find_release_version_from_page(soup, app):
    repo = app["repo_path"].strip("/")
    pattern = re.compile(rf"^/{re.escape(repo)}/releases/tag/([^/?#]+)$")
    for link in soup.find_all("a", href=True):
        href = link.get("href", "").strip()
        match = pattern.match(href)
        if not match:
            continue
        text = link.get_text(strip=True)
        tag_from_href = urllib.parse.unquote(match.group(1))
        if re.fullmatch(r"v?\d+(?:\.\d+){1,3}(?:[-+._a-zA-Z0-9]*)?", text or ""):
            version = text
        else:
            version = tag_from_href
        if not version:
            continue
        return extract_version_for_app(app, version)
    return None


def resolve_download_root(cfg):
    raw = (cfg.get("download_dir") or ".").strip()
    path = raw if os.path.isabs(raw) else os.path.normpath(os.path.join(SCRIPT_DIR, raw))
    if not os.path.isdir(path):
        os.makedirs(path)
        logger.info("创建下载目录: %s", path)
    return path


def app_target_dir(root, app):
    sub = (app.get("save_subdir") or "").strip().replace("\\", "/").strip("/")
    if not sub:
        return root
    d = os.path.join(root, *sub.split("/"))
    if not os.path.isdir(d):
        os.makedirs(d)
    return d


def detect_platform_key():
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "darwin"
    if sys.platform.startswith("linux"):
        return "linux"
    return "windows"


def normalize_platform_arg(name):
    if not name:
        return None
    n = name.strip().lower()
    aliases = {"win": "windows", "mac": "darwin", "macos": "darwin", "osx": "darwin"}
    return aliases.get(n, n)


def apps_list_from_config(cfg, platform_override=None):
    """
    优先使用 platforms.<windows|darwin|linux> 分块；
    若仍使用根级 apps（旧版），则按条目的 only_on 过滤当前系统。
    """
    if isinstance(cfg.get("platforms"), dict):
        key = normalize_platform_arg(platform_override) or detect_platform_key()
        block = cfg["platforms"].get(key)
        if block is None:
            logger.warning(
                "配置 platforms 中无 %r 键，当前没有可处理的应用（可用 --platform 指定）",
                key,
            )
            return []
        if not isinstance(block, list):
            raise ValueError("platforms.%s 必须是 JSON 数组" % key)
        logger.info("使用 platforms.%s（共 %s 项）", key, len(block))
        return block
    legacy = cfg.get("apps") or []
    return _filter_legacy_apps_by_only_on(legacy)


def _filter_legacy_apps_by_only_on(apps):
    out = []
    for a in apps:
        only = (a.get("only_on") or "").strip().lower()
        if not only or only in ("any", "all", "*"):
            out.append(a)
            continue
        if only == "windows" and sys.platform == "win32":
            out.append(a)
        elif only == "darwin" and sys.platform == "darwin":
            out.append(a)
        elif only == "linux" and sys.platform.startswith("linux"):
            out.append(a)
    if len(out) != len(apps):
        logger.info("根级 apps：已按 only_on 过滤为 %s 项（旧版配置）", len(out))
    return out


def installer_extensions(app):
    if app.get("installer_extensions"):
        return list(app["installer_extensions"])
    if app.get("windows_installer"):
        return [".exe"]
    return []


def href_allowed_for_app(href, app):
    for sub in app.get("href_exclude_substrings") or []:
        if sub in href:
            return False
    return True


def link_targets_app(href, text, app):
    markers = app.get("installer_markers") or []
    if not markers:
        return False
    if app.get("installer_markers_match_all"):
        if not all(m in href or m in text for m in markers):
            return False
    elif not any(m in href or m in text for m in markers):
        return False
    if not href_allowed_for_app(href, app):
        return False
    base = href.split("?", 1)[0].lower()
    if base.endswith(".blockmap") or base.endswith(".sig") or base.endswith(".digest"):
        return False
    exts = installer_extensions(app)
    if exts and not any(base.endswith(e) for e in exts):
        return False
    return True


def check_latest_version(app, debug_html_path, verify=True, cfg=None, platform_key=None):
    if uses_github_pages_manifest(app):
        plat = platform_key or detect_platform_key()
        return resolve_github_pages_manifest(app, verify, cfg, plat)

    try:
        if app.get("prefer_api_assets"):
            return fetch_release_via_api(app, verify=verify)

        used_url, page_html = request_release_page(app, verify=verify, cfg=cfg)
        with open(debug_html_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        logger.info("[%s] 已保存发布页 HTML: %s", app["id"], debug_html_path)

        soup = BeautifulSoup(page_html, "html.parser")
        download_url = None
        logger.info("[%s] 尝试从页面中查找下载链接...", app["id"])

        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            text = link.get_text(strip=True)
            if not link_targets_app(href, text, app):
                continue
            if "release-assets.githubusercontent.com" in href:
                if not any(m in href for m in (app.get("installer_markers") or [])):
                    continue
            if href.startswith("/"):
                download_url = f"https://github.com{href}"
            elif href.startswith("http"):
                download_url = href
            else:
                download_url = f"https://github.com/{href}"
            logger.info("[%s] 从页面中找到下载链接: %s", app["id"], download_url)
            break

        if not download_url:
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                data_href = link.get("data-href", "")
                text = link.get_text(strip=True)
                for url in (href, data_href):
                    if not url or not link_targets_app(url, text, app):
                        continue
                    if url.startswith("/"):
                        download_url = f"https://github.com{url}"
                    elif url.startswith("http"):
                        download_url = url
                    else:
                        download_url = f"https://github.com/{url}"
                    logger.info("[%s] 从链接属性中找到下载链接: %s", app["id"], download_url)
                    break
                if download_url:
                    break

        hint = (app.get("url_hint") or app["id"]).lower()
        exts_for_scan = installer_extensions(app)
        if not exts_for_scan and app.get("windows_installer"):
            exts_for_scan = [".exe"]
        if not download_url:
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                text = link.get_text(strip=True)
                if exts_for_scan and not any(e in href or e in text for e in exts_for_scan):
                    continue
                if hint not in href.lower() and hint not in text.lower():
                    continue
                if not any(m in href or m in text for m in (app.get("installer_markers") or []) if len(m) >= 2):
                    continue
                if exts_for_scan:
                    base = href.split("?", 1)[0].lower()
                    if not any(base.endswith(e) for e in exts_for_scan):
                        continue
                if not href_allowed_for_app(href, app):
                    continue
                if href.startswith("/"):
                    download_url = f"https://github.com{href}"
                elif href.startswith("http"):
                    download_url = href
                else:
                    download_url = f"https://github.com/{href}"
                logger.info("[%s] 从通用搜索中找到下载链接: %s", app["id"], download_url)
                break

        version = find_release_version_from_page(soup, app)
        if not version:
            latest_release = soup.find("div", class_="release-header")
            if not latest_release:
                latest_release = soup.select_one(".release")
            if not latest_release:
                latest_release = soup.select_one('[data-view-component="true"].Link--primary')
            if not latest_release:
                raise RuntimeError("无法找到最新版本信息")

            version_tag = None
            if hasattr(latest_release, "find"):
                version_tag = latest_release.find("a", class_="Link--primary")
            if not version_tag:
                version_tag = soup.select_one('a[data-view-component="true"].Link--primary')
            if not version_tag:
                for tag in soup.find_all("a"):
                    if tag.text and re.search(r"v?\d+\.\d+\.\d+", tag.text):
                        version_tag = tag
                        break
            if not version_tag:
                raise RuntimeError("无法找到版本标签")

            version = extract_version_for_app(app, version_tag.text.strip())
        if not download_url:
            try:
                api_version, api_download_url = fetch_release_via_api(
                    app,
                    verify=verify,
                    version_hint=version,
                )
                if not version:
                    version = api_version or version
                download_url = api_download_url or download_url
            except Exception as api_error:
                logger.warning("[%s] GitHub API 补充下载链接失败: %s", app["id"], api_error)

        logger.info("[%s] 找到最新版本: %s", app["id"], version)
        logger.info("[%s] 成功使用发布页来源: %s", app["id"], used_url)
        if download_url:
            logger.info("[%s] 同时找到下载链接: %s", app["id"], download_url)
        else:
            logger.warning("[%s] 未能在页面中找到下载链接，将使用拼接 URL", app["id"])

        return version, download_url

    except Exception as e:
        logger.warning("[%s] 发布页解析失败，准备回退 GitHub API: %s", app["id"], e)
        try:
            return fetch_release_via_api(app, verify=verify)
        except Exception as api_error:
            logger.error("[%s] 检查版本时出错: %s", app["id"], api_error)
            import traceback

            logger.error(traceback.format_exc())
            raise api_error


def build_fallback_urls(version, app):
    if uses_github_pages_manifest(app):
        return []
    version_plain = version.lstrip("v")
    repo = (app.get("repo_path") or "").strip("/")
    if not repo:
        return []
    names = app.get("download_names") or []
    out = []
    for tpl in (app.get("download_url_templates") or []):
        out.append(tpl.replace("{ver}", version).replace("{ver_plain}", version_plain))
    for tpl in names:
        fname = tpl.replace("{ver}", version_plain)
        out.append(f"https://github.com/{repo}/releases/download/{version}/{fname}")
    return out


def normalize_download_url_list(parsed_url, fallback_urls):
    def expand_url(url):
        if not url:
            return []
        if "release-assets.githubusercontent.com" in url:
            return [url]
        if "github.com" in url and "gh-proxy" not in url and "release-assets" not in url:
            return [
                f"https://gh-proxy.com/{url}",
                f"https://ghp.ci/{url}",
                f"https://mirror.ghproxy.com/{url}",
                url,
            ]
        return [url]

    download_urls = []
    if parsed_url:
        logger.info("使用从页面解析的下载链接: %s", parsed_url)
        download_urls.extend(expand_url(parsed_url))

    for base_url in fallback_urls:
        download_urls.extend(expand_url(base_url))

    deduped = []
    seen = set()
    for url in download_urls:
        if url in seen:
            continue
        seen.add(url)
        deduped.append(url)
    return deduped


def download_installer(
    version, parsed_url, app, local_filename, max_retries=3, verify=True, platform_key=None
):
    version_plain = version.lstrip("v")
    fallback = build_fallback_urls(version, app)
    download_urls = normalize_download_url_list(parsed_url, fallback)

    if app.get("use_download_filename") and parsed_url:
        parsed = urllib.parse.urlparse(parsed_url)
        bn = urllib.parse.unquote(os.path.basename(parsed.path))
        if bn and "." in bn:
            expected_name = bn
        else:
            tpl = app.get("save_name") or (app.get("download_names") or ["setup-{ver}.exe"])[0]
            expected_name = tpl.replace("{ver}", version_plain)
    else:
        tpl = app.get("save_name") or (app.get("download_names") or ["setup-{ver}.exe"])[0]
        expected_name = tpl.replace("{ver}", version_plain)
    if os.path.basename(local_filename) != expected_name:
        local_filename = os.path.join(os.path.dirname(local_filename), expected_name)

    if platform_key:
        logger.info("开始下载安装程序到: %s [平台: %s]", local_filename, platform_key)
    else:
        logger.info("开始下载安装程序到: %s", local_filename)
    if os.path.exists(local_filename):
        try:
            os.remove(local_filename)
            logger.info("已删除旧文件: %s", local_filename)
        except OSError as e:
            logger.warning("删除旧文件失败: %s", e)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    for url_index, download_url in enumerate(download_urls):
        if download_url.startswith("https://gh-proxy"):
            if "https:/github.com" in download_url and "https://github.com" not in download_url:
                download_url = download_url.replace("https:/github.com", "https://github.com")
            download_url = download_url.replace("https://https://", "https://")

        logger.info("尝试下载源 %s/%s: %s", url_index + 1, len(download_urls), download_url)
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(
                    download_url, stream=True, timeout=60, headers=headers, verify=verify
                )
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0
                with open(local_filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = 100.0 * downloaded / total_size
                                mb_done = downloaded / (1024 * 1024)
                                mb_total = total_size / (1024 * 1024)
                                sys.stdout.write(
                                    f"\r下载进度: {percent:.1f}% "
                                    f"({mb_done:.1f}/{mb_total:.1f} MiB)"
                                )
                                sys.stdout.flush()

                if os.path.exists(local_filename) and os.path.getsize(local_filename) > 0:
                    file_size = os.path.getsize(local_filename)
                    if total_size > 0:
                        if file_size != total_size:
                            logger.warning(
                                "下载的文件大小(%s)与预期(%s)不匹配", file_size, total_size
                            )
                            if retries < max_retries - 1:
                                retries += 1
                                logger.info("重试下载 (%s/%s)...", retries, max_retries)
                                try:
                                    os.remove(local_filename)
                                except OSError:
                                    pass
                                continue
                            raise RuntimeError(f"文件大小不匹配 ({file_size} != {total_size})")
                        logger.info("\n下载完成: %s (%s 字节)", local_filename, file_size)
                        logger.info("成功使用下载源 %s", download_url)
                        return local_filename
                    if file_size > 1000:
                        logger.info("\n下载完成: %s (%s 字节)", local_filename, file_size)
                        logger.info("成功使用下载源 %s", download_url)
                        return local_filename
                    logger.warning("下载的文件太小(%s 字节)", file_size)
                    if retries < max_retries - 1:
                        retries += 1
                        try:
                            os.remove(local_filename)
                        except OSError:
                            pass
                        continue
                    raise RuntimeError(f"文件太小 ({file_size} 字节)")
                logger.error("下载的文件不存在或为空")
                if retries < max_retries - 1:
                    retries += 1
                    continue
                raise RuntimeError("文件不存在或为空")

            except requests.exceptions.RequestException as e:
                logger.error("下载请求出错: %s", e)
                if retries < max_retries - 1:
                    time.sleep(2**retries)
                    retries += 1
                    continue
                logger.warning("当前下载源失败，尝试下一个")
                break
            except Exception as e:
                logger.error("下载安装程序时出错: %s", e)
                import traceback

                logger.error(traceback.format_exc())
                logger.warning("当前下载源失败，尝试下一个")
                break

        if os.path.exists(local_filename) and os.path.getsize(local_filename) > 0:
            file_size = os.path.getsize(local_filename)
            if file_size > 1000:
                logger.info("下载源 %s 成功，文件大小: %s 字节", url_index + 1, file_size)
                return local_filename
            try:
                os.remove(local_filename)
            except OSError:
                pass

    raise RuntimeError(f"所有下载源均失败（共 {len(download_urls)} 个）")


def kill_process(process_name):
    if not process_name:
        return
    try:
        logger.info("尝试终止进程: %s", process_name)
        if sys.platform == "win32":
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", process_name],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info("已终止进程: %s", process_name)
            except subprocess.CalledProcessError as e:
                if e.returncode == 128:
                    logger.info("进程未运行: %s", process_name)
                else:
                    logger.warning("终止进程警告: %s", e)
        else:
            logger.warning("非 Windows 环境，跳过 taskkill")
    except Exception as e:
        logger.error("终止进程时出错: %s", e)
        raise


def run_installer(installer_path):
    logger.info("开始运行安装程序: %s", installer_path)
    if not os.path.exists(installer_path):
        raise FileNotFoundError(f"安装程序不存在: {installer_path}")

    try:
        subprocess.Popen([installer_path], shell=True)
        logger.info("安装程序已启动 (Popen)")
        return
    except Exception as e1:
        logger.warning("Popen 失败: %s", e1)

    if sys.platform == "win32":
        try:
            os.startfile(installer_path)
            logger.info("安装程序已启动 (startfile)")
            return
        except Exception as e2:
            logger.warning("startfile 失败: %s", e2)

    cmd = f'powershell -Command "Start-Process \'{installer_path}\' -Verb RunAs"'
    subprocess.run(cmd, shell=True, check=True)
    logger.info("安装程序已启动 (PowerShell RunAs)")


def select_apps(cfg, only_ids, platform_override=None):
    apps = apps_list_from_config(cfg, platform_override)
    enabled = [a for a in apps if a.get("enabled", True)]
    if not only_ids:
        return enabled
    want = {x.lower() for x in only_ids}
    picked = [a for a in enabled if a.get("id", "").lower() in want]
    unknown = want - {a.get("id", "").lower() for a in picked}
    for u in unknown:
        logger.warning("未处理 id=%r：不存在或未启用（请在 apps.json 中设置 enabled）", u)
    return picked


def update_one(app, download_root, verify=True, platform_key=None, cfg=None):
    cfg = cfg or {}
    aid = app["id"]
    plat = platform_key or detect_platform_key()
    debug_html = os.path.join(SCRIPT_DIR, f"github_page_{plat}_{aid}.html")

    root = download_root
    if cfg.get("download_subdir_by_platform"):
        root = os.path.join(download_root, plat)
        if not os.path.isdir(root):
            os.makedirs(root)

    target_dir = app_target_dir(root, app)

    logger.info("=== [%s] 开始 === [平台: %s] [下载目录: %s]", aid, plat, target_dir)
    version, dl_url = check_latest_version(
        app, debug_html, verify=verify, cfg=cfg, platform_key=plat
    )
    version_plain = version.lstrip("v")
    tpl_save = app.get("save_name") or (app.get("download_names") or ["setup-{ver}.exe"])[0]
    local_filename = os.path.join(target_dir, tpl_save.replace("{ver}", version_plain))
    if app.get("use_download_filename") and dl_url:
        pu = urllib.parse.urlparse(dl_url)
        base = urllib.parse.unquote(os.path.basename(pu.path))
        if base and "." in base:
            local_filename = os.path.join(target_dir, base)

    installer_path = download_installer(
        version, dl_url, app, local_filename, verify=verify, platform_key=plat
    )
    logger.info("[%s] 安装包已下载: %s", aid, installer_path)

    if not app.get("run_installer", True):
        logger.info("[%s] 配置为仅下载，跳过结束进程与启动安装包", aid)
        return 0

    if app.get("kill_before_install", True):
        kill_process(app.get("process_name") or "")
        time.sleep(2)

    run_installer(installer_path)
    logger.info("=== [%s] 完成 ===", aid)
    return 0


def main():
    parser = argparse.ArgumentParser(description="按 apps.json 按需下载/更新应用")
    parser.add_argument(
        "app_id",
        nargs="*",
        help="只处理这些 id（须已在配置中 enabled）；省略则处理所有已启用的项",
    )
    parser.add_argument(
        "--platform",
        metavar="NAME",
        help="读取 platforms.<NAME>（windows|darwin|linux），默认随当前系统",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="跳过 HTTPS 证书校验（镜像站点证书过期/自签时使用，存在中间人风险）",
    )
    parser.add_argument(
        "--apps-dir",
        metavar="DIR",
        help="替代默认 apps/：指定含 root.json 的目录（如 VibeCodingToolsDown，相对项目根目录）",
    )
    args = parser.parse_args()

    try:
        cfg = load_config(apps_dir=args.apps_dir)
    except Exception as e:
        logger.error("%s", e)
        return 1

    download_root = resolve_download_root(cfg)
    platform_key = normalize_platform_arg(args.platform) or detect_platform_key()
    apps = select_apps(cfg, args.app_id, args.platform)
    if not apps:
        logger.error("没有可处理的应用：请检查 apps.json 中的 enabled，或命令行指定的 id")
        return 1

    verify = resolve_tls_verify(cfg, args.insecure)
    configure_insecure_requests(verify)
    if not verify:
        logger.warning("已关闭 TLS 证书校验（--insecure 或 apps.json ssl_verify=false）")

    try:
        requests.get("https://github.com", timeout=10, verify=verify)
    except requests.exceptions.RequestException as e:
        logger.error("网络不可用: %s", e)
        return 1

    exit_code = 0
    for app in apps:
        if uses_github_pages_manifest(app):
            missing = [k for k in ("id",) if not app.get(k)]
        else:
            missing = [k for k in ("id", "releases_url", "repo_path") if k not in app]
        if missing:
            logger.error("应用配置缺少字段 %s: %s", missing, app)
            exit_code = 1
            continue
        try:
            update_one(
                app,
                download_root,
                verify=verify,
                platform_key=platform_key,
                cfg=cfg,
            )
        except Exception as e:
            logger.error("[%s] 失败: %s", app.get("id"), e)
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
