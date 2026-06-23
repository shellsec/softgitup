# list — 扩展站点 URL 清单（系统 / 移动 分开）

供 `fetch_titles.py` 按 **scope** 监控；报告页 `reports/index.html` 按站点分组，**系统变化** 与 **移动变化** 分开显示。

## scope 与文件

| scope | 平台 | URL 清单 | 约数量 | 必选 |
|-------|------|----------|--------|------|
| `hybase_system` | 系统 | `hybase_newlist_urls_system.txt` | 358 | ✅ |
| `hybase_mobile` | 移动 | `hybase_newlist_urls_mobile.txt` | 242 | ✅ |
| `dayanzai_system` | 系统 | `dayanzai_system_urls.txt` | 2936 | ✅ |
| `dayanzai_mobile` | 移动 | `dayanzai_android_urls.txt` | 262 | ✅ |
| `down66_system` | 系统 | `down66_system_urls.txt` | 357 | ✅ |
| `down66_mobile` | 移动 | `down66_app_urls.txt` | 226 | ✅ |
| `7xiazai_system` | 系统 | `7xiazai_list_urls_system.txt` | 442 | ✅ |
| `7xiazai_mobile` | 移动 | `7xiazai_list_urls_mobile.txt` | 226 | ✅ |

合并版（仅人工查阅，**快检不用**）：

- `hybase_newlist_urls.txt` / `hybase_newlist_list.txt`（600）
- `7xiazai_list_urls.txt` — 合并清单（extract 后按标题自动拆分）
- `dayanzai_android_list.txt`、`down66_app_list.txt` — 标题+URL 对照

## 快检入口

| 批处理 | 作用 |
|--------|------|
| `monthly_check_site.bat hybase` | hybase 系统 + 移动 |
| `monthly_check_site.bat dayanzai` | dayanzai 系统 + 移动 |
| `monthly_check_site.bat down66` | down66 系统 + 移动 |
| `monthly_check_list.bat` | 7xiazai + 上述三站连跑 |
| `open_changed_site.bat <站点>` | 打开该系统/移动变化 URL |

命令行：

```bat
python fetch_titles.py --scope hybase_system --compare
python fetch_titles.py --scope hybase_mobile --compare
```

旧 scope 名仍可用（依次跑 system+mobile）：

```bat
python fetch_titles.py --scope hybase --compare
```

## 补充 / 更新 PC 清单

运行爬虫（从站点分页发现 URL，并排除已有 android/app 清单）：

```bat
python extract_list_system_urls.py
```

也可手工编辑 `dayanzai_system_urls.txt` / `down66_system_urls.txt`，每行一个 URL（`#` 开头为注释）。

## 报告页

每个站点一块：**合计变化 | 系统变化 | 移动变化**，下面分 **系统** / **移动** 两个子区，各自列出标题变动。

**首次运行**每个 scope 只建基线；**再跑一遍**才有 `changed_*_urls.txt`。
