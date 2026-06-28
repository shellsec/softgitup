"""生成 HTML 报告页 reports/index.html，便于浏览与快速打开链接。"""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

from list_scopes import LIST_SITE_GROUPS, LIST_SCOPE_DEFS, build_report_meta

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
HISTORY = HERE / "history"

SCOPE_META = {
    "a": {
        "id": "a",
        "title": "A 类 · 同步软件",
        "desc": "config.json software_dirs 相关页面",
        "snapshot": "titles_latest_A.json",
        "diff": "last_diff_a.json",
        "changed_txt": "changed_tier_a_urls.txt",
        "accent": "#2563eb",
    },
    "all": {
        "id": "all",
        "title": "装机区全量",
        "desc": "最终选择指南之前全部页面",
        "snapshot": "titles_latest_ALL.json",
        "diff": "last_diff_all.json",
        "changed_txt": "changed_pages_urls.txt",
        "accent": "#059669",
    },
    "423down": {
        "id": "423down",
        "title": "423down digest",
        "desc": "digest 区去重链接（可选）",
        "snapshot": "titles_latest_423DOWN.json",
        "diff": "last_diff_423down.json",
        "changed_txt": "changed_423down_urls.txt",
        "accent": "#d97706",
    },
    "gamer520": {
        "id": "gamer520",
        "title": "gamer520 · 游戏",
        "desc": "gamer520.com 近期文章（首页 50 页分页，非全站 sitemap）",
        "snapshot": "titles_latest_GAMER520.json",
        "diff": "last_diff_gamer520.json",
        "changed_txt": "changed_gamer520_urls.txt",
        "accent": "#7c2d12",
    },
}

for _scope_key in LIST_SCOPE_DEFS:
    SCOPE_META[_scope_key] = build_report_meta(_scope_key)


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _load_changed_urls(name: str) -> list[str]:
    path = HERE / name
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _collect_scope_data(key: str) -> dict:
    meta = SCOPE_META[key]
    snapshot = _read_json(HISTORY / meta["snapshot"])
    diff = _read_json(REPORTS / meta["diff"])
    changed_urls = _load_changed_urls(meta["changed_txt"])

    failed = diff.get("failed", []) if diff else []
    changed_items = diff.get("title_changed", []) if diff else []
    recovered_items = diff.get("recovered", []) if diff else []

    return {
        **meta,
        "snapshot": snapshot,
        "diff": diff,
        "changed_urls": changed_urls,
        "changed_items": changed_items,
        "recovered_items": recovered_items,
        "failed": failed,
        "fetched_at": snapshot.get("fetched_at") if snapshot else None,
        "total": snapshot.get("count", 0) if snapshot else 0,
        "changed_count": len(changed_items),
        "recovered_count": len(recovered_items),
        "unchanged_count": diff.get("unchanged_count", 0) if diff else None,
        "failed_count": len(failed),
        "platform": meta.get("platform"),
        "site": meta.get("site"),
    }


def _render_changed_cards(items: list[dict], scope_id: str) -> str:
    if not items:
        return '<p class="empty">暂无标题变化。不更新 software/ 也完全可用。</p>'

    blocks = []
    for i, item in enumerate(items):
        url = item.get("url", "")
        old = html.escape(str(item.get("old", "")))
        new = html.escape(str(item.get("new", "")))
        sw = item.get("software") or []
        tags = "".join(f'<span class="tag">{html.escape(s)}</span>' for s in sw)
        url_e = html.escape(url)
        blocks.append(
            f"""
            <article class="card item" data-search="{html.escape((url + ' ' + new + ' ' + old).lower())}">
              <div class="card-head">
                <span class="idx">{i + 1}</span>
                <a class="link" href="{url_e}" target="_blank" rel="noopener">{url_e}</a>
                <a class="btn-sm" href="{url_e}" target="_blank" rel="noopener">打开</a>
              </div>
              {f'<div class="tags">{tags}</div>' if tags else ''}
              <div class="diff">
                <div class="diff-row"><span class="label old">旧</span><span>{old}</span></div>
                <div class="diff-row"><span class="label new">新</span><span>{new}</span></div>
              </div>
            </article>
            """
        )
    return "\n".join(blocks)


def _render_failed(items: list[dict]) -> str:
    if not items:
        return ""
    rows = []
    for item in items[:30]:
        url_e = html.escape(item.get("url", ""))
        err = html.escape(str(item.get("error", item.get("status", ""))))
        rows.append(
            f'<li><a href="{url_e}" target="_blank" rel="noopener">{url_e}</a>'
            f' <span class="muted">({err})</span></li>'
        )
    extra = f"<li class='muted'>… 另有 {len(items) - 30} 条</li>" if len(items) > 30 else ""
    return f"<ul class='fail-list'>{''.join(rows)}{extra}</ul>"


def _render_snapshot_rows(snapshot: dict | None, scope_id: str, changed_urls: set[str]) -> str:
    if not snapshot or not snapshot.get("entries"):
        return '<p class="empty">尚无快照。请先运行对应范围的快检。</p>'

    rows = []
    for i, entry in enumerate(snapshot["entries"], 1):
        url = entry.get("url", "")
        url_e = html.escape(url)
        title = html.escape(entry.get("title") or "(无标题)")
        status = entry.get("status", "")
        sw = entry.get("software") or []
        tags = "".join(f'<span class="tag">{html.escape(s)}</span>' for s in sw)
        domain = html.escape(entry.get("domain") or "")
        search = html.escape((url + " " + entry.get("title", "") + " " + " ".join(sw) + " " + domain).lower())

        if status != "ok":
            title = html.escape(f"抓取失败: {entry.get('error') or status}")
            status_cls = " snap-bad"
        else:
            status_cls = ""

        changed_badge = '<span class="badge-changed">有变化</span>' if url in changed_urls else ""

        rows.append(
            f"""
            <div class="snap-row{status_cls}" data-search="{search}">
              <span class="idx">{i}</span>
              <div class="snap-main">
                <a class="link" href="{url_e}" target="_blank" rel="noopener">{url_e}</a>
                <div class="snap-title">{title}</div>
                {f'<div class="tags">{tags}</div>' if tags else ''}
              </div>
              <div class="snap-side">
                {changed_badge}
                {f'<span class="tag domain">{domain}</span>' if domain else ''}
                <a class="btn-sm" href="{url_e}" target="_blank" rel="noopener">打开</a>
              </div>
            </div>
            """
        )
    return "\n".join(rows)


def _render_scope_section(data: dict) -> str:
    sid = data["id"]
    accent = data["accent"]
    fetched = data["fetched_at"] or "未运行"
    has_diff = data["diff"] is not None
    snapshot = data.get("snapshot")
    snap_count = len(snapshot.get("entries", [])) if snapshot else 0
    changed_url_set = {it.get("url") for it in data["changed_items"]}

    stat_unchanged = (
        str(data["unchanged_count"])
        if data["unchanged_count"] is not None
        else ("—" if not has_diff else "0")
    )

    urls_json = html.escape(json.dumps([it.get("url") for it in data["changed_items"]], ensure_ascii=False))

    changed_block = (
        _render_changed_cards(data["changed_items"], sid)
        if has_diff
        else '<p class="empty">尚无比对结果。对该范围再运行一次带 --compare 的快检即可。</p>'
    )

    return f"""
    <section class="scope" id="scope-{sid}" style="--accent:{accent}">
      <header class="scope-head">
        <div>
          <h2>{html.escape(data['title'])}</h2>
          <p class="muted">{html.escape(data['desc'])}</p>
        </div>
        <div class="scope-actions">
          <button type="button" class="btn" data-open-scope="{sid}"{" disabled" if not data['changed_items'] else ""}>
            依次打开变化页 ({data['changed_count']})
          </button>
        </div>
      </header>
      <div class="stats">
        <div class="stat"><b>{data['total']}</b><span>监控页</span></div>
        <div class="stat highlight"><b>{data['changed_count']}</b><span>标题变化</span></div>
        <div class="stat"><b>{data['recovered_count']}</b><span>恢复抓取</span></div>
        <div class="stat"><b>{stat_unchanged}</b><span>无变化</span></div>
        <div class="stat"><b>{data['failed_count']}</b><span>抓取失败</span></div>
        <div class="stat wide"><b>{html.escape(fetched)}</b><span>最近快照</span></div>
      </div>

      <h3 class="section-label">标题变化</h3>
      <div class="toolbar">
        <input type="search" class="search search-changed" placeholder="筛选变化项…" data-scope="{sid}" />
      </div>
      <div class="items changed-items" data-scope-changed="{sid}">
        {changed_block}
      </div>
      {f'<details class="recover-box"><summary>恢复抓取 ({data["recovered_count"]}) · 上次失败本次成功，通常无需更新</summary>{_render_changed_cards(data["recovered_items"], sid)}</details>' if data['recovered_count'] else ''}
      <script type="application/json" id="urls-{sid}">{urls_json}</script>

      <details class="snapshot-box">
        <summary>全部快照标题（{snap_count}）· 默认折叠，可查当前页标题</summary>
        <div class="toolbar">
          <input type="search" class="search search-snapshot" placeholder="搜索 URL / 标题 / 软件…" data-scope="{sid}" />
        </div>
        <div class="snapshot-list" data-scope-snapshot="{sid}">
          {_render_snapshot_rows(snapshot, sid, changed_url_set)}
        </div>
      </details>

      {f'<details class="fail-box"><summary>抓取失败 ({data["failed_count"]})</summary>{_render_failed(data["failed"])}</details>' if data['failed_count'] else ''}
    </section>
    """


def _render_scope_subsection(data: dict) -> str:
    """list 站点内的 系统/移动 子分区。"""
    sid = data["id"]
    accent = data["accent"]
    platform_label = "系统" if data.get("platform") == "system" else "移动"
    fetched = data["fetched_at"] or "未运行"
    has_diff = data["diff"] is not None
    snapshot = data.get("snapshot")
    snap_count = len(snapshot.get("entries", [])) if snapshot else 0
    changed_url_set = {it.get("url") for it in data["changed_items"]}
    stat_unchanged = (
        str(data["unchanged_count"])
        if data["unchanged_count"] is not None
        else ("—" if not has_diff else "0")
    )
    urls_json = html.escape(json.dumps([it.get("url") for it in data["changed_items"]], ensure_ascii=False))
    changed_block = (
        _render_changed_cards(data["changed_items"], sid)
        if has_diff
        else '<p class="empty">尚无比对结果。对该子范围再运行一次带 --compare 的快检即可。</p>'
    )
    if not snapshot and not has_diff:
        changed_block = '<p class="empty">清单未运行或为空（可选 PC 清单待补充 URL）。</p>'

    return f"""
    <div class="scope-sub" id="scope-{sid}" style="--accent:{accent}">
      <header class="scope-sub-head">
        <div>
          <h3><span class="platform-badge platform-{data.get('platform', '')}">{platform_label}</span> {html.escape(data['desc'])}</h3>
        </div>
        <div class="scope-actions">
          <button type="button" class="btn btn-sm" data-open-scope="{sid}"{" disabled" if not data['changed_items'] else ""}>
            打开变化 ({data['changed_count']})
          </button>
        </div>
      </header>
      <div class="stats stats-compact">
        <div class="stat"><b>{data['total']}</b><span>监控页</span></div>
        <div class="stat highlight"><b>{data['changed_count']}</b><span>标题变化</span></div>
        <div class="stat"><b>{stat_unchanged}</b><span>无变化</span></div>
        <div class="stat"><b>{data['failed_count']}</b><span>失败</span></div>
        <div class="stat wide"><b>{html.escape(fetched)}</b><span>快照</span></div>
      </div>
      <div class="toolbar">
        <input type="search" class="search search-changed" placeholder="筛选 {platform_label} 变化…" data-scope="{sid}" />
      </div>
      <div class="items changed-items" data-scope-changed="{sid}">
        {changed_block}
      </div>
      <script type="application/json" id="urls-{sid}">{urls_json}</script>
      <details class="snapshot-box">
        <summary>全部快照（{snap_count}）</summary>
        <div class="toolbar">
          <input type="search" class="search search-snapshot" placeholder="搜索…" data-scope="{sid}" />
        </div>
        <div class="snapshot-list" data-scope-snapshot="{sid}">
          {_render_snapshot_rows(snapshot, sid, changed_url_set)}
        </div>
      </details>
    </div>
    """


def _render_list_site_group(group: dict) -> str:
    scope_data = [_collect_scope_data(s) for s in group["scopes"]]
    total_changed = sum(d["changed_count"] for d in scope_data)
    total_pages = sum(d["total"] for d in scope_data)
    system_data = next((d for d in scope_data if d.get("platform") == "system"), None)
    mobile_data = next((d for d in scope_data if d.get("platform") == "mobile"), None)
    sys_chg = system_data["changed_count"] if system_data else 0
    mob_chg = mobile_data["changed_count"] if mobile_data else 0
    subs = "\n".join(_render_scope_subsection(d) for d in scope_data)

    return f"""
    <section class="site-group scope" id="site-{group['id']}" style="--accent:{group['accent']}">
      <header class="scope-head">
        <div>
          <h2>{html.escape(group['title'])}</h2>
          <p class="muted">{html.escape(group['desc'])}</p>
        </div>
      </header>
      <div class="stats site-summary">
        <div class="stat"><b>{total_pages}</b><span>合计监控</span></div>
        <div class="stat highlight"><b>{total_changed}</b><span>合计变化</span></div>
        <div class="stat"><b>{sys_chg}</b><span>系统变化</span></div>
        <div class="stat"><b>{mob_chg}</b><span>移动变化</span></div>
      </div>
      {subs}
    </section>
    """


def build_index_html() -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    core_scopes = [_collect_scope_data(k) for k in ("a", "all", "423down", "gamer520")]
    list_sections = [_render_list_site_group(g) for g in LIST_SITE_GROUPS]
    all_data = core_scopes + [d for g in LIST_SITE_GROUPS for d in [_collect_scope_data(s) for s in g["scopes"]]]
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = "\n".join(_render_scope_section(s) for s in core_scopes)
    sections += "\n" + "\n".join(list_sections)
    total_changed = sum(s["changed_count"] for s in all_data)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Soft Page Check · 报告</title>
  <style>
    :root {{
      --bg: #f4f6fb;
      --surface: #fff;
      --text: #1e293b;
      --muted: #64748b;
      --border: #e2e8f0;
      --shadow: 0 1px 3px rgb(15 23 42 / 8%);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px 48px; }}
    .hero {{
      background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
      color: #fff;
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: var(--shadow);
    }}
    .hero h1 {{ margin: 0 0 8px; font-size: 1.6rem; font-weight: 650; }}
    .hero p {{ margin: 0; opacity: 0.9; font-size: 0.95rem; }}
    .hero-meta {{ margin-top: 16px; font-size: 0.85rem; opacity: 0.85; }}
    .nav {{
      display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;
    }}
    .nav a {{
      padding: 8px 14px; background: var(--surface); border: 1px solid var(--border);
      border-radius: 999px; text-decoration: none; color: var(--text); font-size: 0.88rem;
    }}
    .nav a:hover {{ border-color: #2563eb; color: #2563eb; }}
    .scope {{
      background: var(--surface);
      border-radius: 14px;
      border: 1px solid var(--border);
      padding: 20px 22px 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
    }}
    .scope-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 16px; }}
    .scope h2 {{ margin: 0; font-size: 1.15rem; color: var(--accent); }}
    .muted {{ color: var(--muted); font-size: 0.88rem; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin-bottom: 16px; }}
    .stat {{
      background: var(--bg); border-radius: 10px; padding: 12px; text-align: center;
    }}
    .stat b {{ display: block; font-size: 1.35rem; }}
    .stat span {{ font-size: 0.75rem; color: var(--muted); }}
    .stat.highlight b {{ color: var(--accent); }}
    .stat.wide {{ grid-column: span 2; text-align: left; }}
    .stat.wide b {{ font-size: 0.95rem; font-weight: 600; }}
    .toolbar {{ margin-bottom: 12px; }}
    .search {{
      width: 100%; max-width: 400px; padding: 10px 14px; border: 1px solid var(--border);
      border-radius: 10px; font-size: 0.9rem;
    }}
    .card {{
      border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px;
      margin-bottom: 10px; background: #fafbfc;
    }}
    .card.hidden {{ display: none; }}
    .card-head {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }}
    .idx {{ color: var(--muted); font-size: 0.8rem; min-width: 1.5em; }}
    .link {{ flex: 1; word-break: break-all; color: #2563eb; text-decoration: none; font-size: 0.88rem; }}
    .link:hover {{ text-decoration: underline; }}
    .btn, .btn-sm {{
      border: none; cursor: pointer; border-radius: 8px; font-size: 0.82rem;
      background: var(--accent, #2563eb); color: #fff; text-decoration: none;
      display: inline-block; padding: 8px 14px;
    }}
    .btn-sm {{ padding: 4px 10px; }}
    .btn:hover, .btn-sm:hover {{ filter: brightness(1.08); }}
    .btn:disabled {{ opacity: 0.45; cursor: not-allowed; }}
    .tags {{ margin-top: 6px; }}
    .tag {{
      display: inline-block; background: #e0e7ff; color: #3730a3;
      font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; margin-right: 4px;
    }}
    .diff {{ margin-top: 8px; font-size: 0.84rem; }}
    .diff-row {{ display: flex; gap: 8px; margin-top: 4px; }}
    .label {{ flex-shrink: 0; font-size: 0.72rem; font-weight: 600; padding: 2px 6px; border-radius: 4px; }}
    .label.old {{ background: #fee2e2; color: #991b1b; }}
    .label.new {{ background: #dcfce7; color: #166534; }}
    .empty {{ color: var(--muted); font-style: italic; margin: 8px 0; }}
    .section-label {{ margin: 20px 0 8px; font-size: 0.92rem; color: var(--muted); font-weight: 600; }}
    .snapshot-box {{
      margin-top: 18px; border: 1px dashed var(--border); border-radius: 10px;
      padding: 12px 14px; background: #f8fafc;
    }}
    .snapshot-box summary {{
      cursor: pointer; font-weight: 600; font-size: 0.9rem; color: var(--accent);
      user-select: none;
    }}
    .snapshot-list {{ margin-top: 12px; max-height: 480px; overflow-y: auto; }}
    .snap-row {{
      display: flex; flex-wrap: wrap; align-items: flex-start; gap: 8px;
      padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 0.84rem;
    }}
    .snap-row:last-child {{ border-bottom: none; }}
    .snap-row.hidden {{ display: none; }}
    .snap-row.snap-bad {{ background: #fff7ed; }}
    .snap-main {{ flex: 1; min-width: 200px; }}
    .snap-title {{ color: var(--text); margin-top: 4px; word-break: break-word; }}
    .snap-side {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }}
    .badge-changed {{
      font-size: 0.7rem; background: #fef3c7; color: #92400e;
      padding: 2px 8px; border-radius: 999px; font-weight: 600;
    }}
    .tag.domain {{ background: #f1f5f9; color: #475569; }}
    .fail-box {{ margin-top: 12px; font-size: 0.85rem; }}
    .fail-list {{ margin: 8px 0 0; padding-left: 1.2em; }}
    .toast {{
      position: fixed; bottom: 20px; right: 20px; background: #1e293b; color: #fff;
      padding: 12px 18px; border-radius: 10px; font-size: 0.88rem; opacity: 0;
      transition: opacity 0.2s; pointer-events: none; z-index: 99;
    }}
    .toast.show {{ opacity: 1; }}
    footer {{ text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 24px; }}
    .site-group {{ border-left: 4px solid var(--accent); }}
    .site-summary {{ margin-bottom: 8px; }}
    .scope-sub {{
      border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px 18px;
      margin-top: 14px; background: #fafbfc;
    }}
    .scope-sub-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 10px; }}
    .scope-sub h3 {{ margin: 0; font-size: 1rem; color: var(--text); font-weight: 600; }}
    .stats-compact {{ margin-bottom: 10px; }}
    .platform-badge {{
      display: inline-block; font-size: 0.72rem; font-weight: 700; padding: 2px 8px;
      border-radius: 999px; margin-right: 6px; vertical-align: middle;
    }}
    .platform-system {{ background: #dbeafe; color: #1e40af; }}
    .platform-mobile {{ background: #fce7f3; color: #9d174d; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>Soft Page Check</h1>
      <p>标题比对报告 · 点击链接或「打开」快速核查 · 变化≠必须更新</p>
      <div class="hero-meta">生成于 {html.escape(generated)} · 合计 {total_changed} 处标题变化</div>
    </header>
    <nav class="nav">
      <a href="#scope-a">A 类</a>
      <a href="#scope-all">装机全量</a>
      <a href="#scope-423down">423down</a>
      <a href="#scope-gamer520">gamer520</a>
      <a href="#site-7xiazai">7xiazai</a>
      <a href="#site-hybase">hybase</a>
      <a href="#site-dayanzai">dayanzai</a>
      <a href="#site-down66">down66</a>
    </nav>
    {sections}
    <footer>soft_page_check/reports/index.html · 重新运行 monthly_check.bat 后刷新</footer>
  </div>
  <div class="toast" id="toast"></div>
  <script>
    function toast(msg) {{
      const el = document.getElementById('toast');
      el.textContent = msg;
      el.classList.add('show');
      setTimeout(() => el.classList.remove('show'), 3200);
    }}

    document.querySelectorAll('.search-changed').forEach(input => {{
      input.addEventListener('input', () => {{
        const scope = input.dataset.scope;
        const q = input.value.trim().toLowerCase();
        document.querySelectorAll(`[data-scope-changed="${{scope}}"] .item`).forEach(card => {{
          const text = card.dataset.search || '';
          card.classList.toggle('hidden', q && !text.includes(q));
        }});
      }});
    }});

    document.querySelectorAll('.search-snapshot').forEach(input => {{
      input.addEventListener('input', () => {{
        const scope = input.dataset.scope;
        const q = input.value.trim().toLowerCase();
        document.querySelectorAll(`[data-scope-snapshot="${{scope}}"] .snap-row`).forEach(row => {{
          const text = row.dataset.search || '';
          row.classList.toggle('hidden', q && !text.includes(q));
        }});
      }});
    }});

    document.querySelectorAll('[data-open-scope]').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const id = btn.dataset.openScope;
        const raw = document.getElementById('urls-' + id);
        if (!raw) return;
        let urls = [];
        try {{ urls = JSON.parse(raw.textContent); }} catch (e) {{ return; }}
        if (!urls.length) {{ toast('无变化链接'); return; }}
        if (!confirm('将依次打开 ' + urls.length + ' 个标签页（间隔 800ms），可能被浏览器拦截。继续？')) return;
        urls.forEach((u, i) => setTimeout(() => window.open(u, '_blank'), i * 800));
        toast('正在打开 ' + urls.length + ' 个页面…');
      }});
    }});
  </script>
</body>
</html>
"""
    out = REPORTS / "index.html"
    out.write_text(doc, encoding="utf-8")
    return out


def save_diff(scope: str, diff: dict, snapshot_path: Path) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "compared_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "snapshot": snapshot_path.name,
        **diff,
    }
    key = scope
    (REPORTS / f"last_diff_{key}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    path = build_index_html()
    print(f"报告页: {path}")


if __name__ == "__main__":
    main()
