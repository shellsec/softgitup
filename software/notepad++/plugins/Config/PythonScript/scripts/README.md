# scripts（中文脚本目录）

本目录为 Notepad++ **PythonScript** 的默认脚本树（中文文件夹与中文 `.py` 文件名）。配置根目录说明、**统一更新（清空后覆盖）**、**推荐快捷键** 见上级 [../README.md](../README.md)。

## 如何使用

在 Notepad++ 中打开  
`Plugins` → `Python Script` → **Configuration** → **Initialisation**，  
将 **Script folder** 设为本目录（`scripts`）的完整路径，重启 Notepad++。

英文菜单请改指向 `scripts_ENG`。

## 文件名对应关系（节选）

| 中文文件名 | `scripts_ENG` 对应 |
|-----------|-------------------|
| 插入时间.py | InsertTime.py |
| 插入时间中文.py | InsertTimeCN.py |
| 插入明天时间中文.py | InsertTomorrowTimeCN.py |
| 插入昨天时间中文.py | InsertYesterdayTimeCN.py |
| 插入明天时间.py | InsertTomorrowTime.py |
| 插入昨天时间.py | InsertYesterdayTime.py |
| 插入时间_简短.py | InsertTimeShort.py |
| 插入时间_ISO.py | InsertTimeISO.py |
| 插入周次中文.py | InsertWeekEN.py |
| 插入模板选择器.py | insert_template_picker.py |
| 插入模板_工作.py 等 | insert_template_*.py |
| 工作日记_三点.py | work_daily_three.py |
| 工作日记_流水.py | work_daily_log.py |
| 快速捕获.py | quickadd_capture.py |
| Markdown工具.py | markdown_tools.py |
| URL编解码.py | url_encode_decode.py |
| HTML实体编解码.py | html_entity_encode_decode.py |
| 选区与剪贴板Diff.py | diff_selection_clipboard.py |
| 配置AI.py | configure_ai.py |
| 跳转_智谱开放平台.py | jump_zhipu_open.py |
| 一键跳转_AI.py | jump_ai_menu.py |
| 跳转_提示词再选AI.py | jump_prompt_pick_ai.py |
| 跳转_*.py | jump_*.py |
| 批量TXT转Markdown.py | batch_txt_to_md.py |
| 大纲转drawio.py | outline_to_drawio.py |
| Base64选区编解码.py | base64_selection.py |
| 行尾LF与CRLF.py | line_endings_lf_crlf.py |
| 插入UUID.py | insert_uuid.py |
| 待办切换.py | todo_toggle.py |
| 行排序去重.py | sort_lines.py |
| … | 其余按子文件夹中英文对照 |

完整旧表中的提取/格式化/系统信息等脚本仍在对应子文件夹，命名规则不变。

## 目录结构

| 子文件夹 | 内容概要 |
|----------|----------|
| `00_AI对话跳转` | **24 个**单站跳转 + 一键菜单；复制后浏览器粘贴；`提示词.ini` |
| `01_时间与插入` | 长串/简短/ISO/周次、UUID、14 类模板 + 选择器、工作日记 |
| `02_行与选区` | 行尾、排序、待办、行号、Git 冲突、Base64、Diff、大纲缩进等 |
| `03_编码与字符` | 全角半角、Unicode、路径、URL/HTML 实体 |
| `04_格式化与转换` | JSON/XML/SQL、CSV→MD、Mermaid、Markdown 工具等 |
| `05_提取与遮罩` | 电话/IP/网址、敏感信息遮罩 |
| `06_系统与网络` | 本机与网络信息 |
| `07_AI与Token` | API 脚本、**配置AI**、Token、0token（非网页跳转） |
| `08_文档与导图` | 批量 TXT→MD、大纲→draw.io（依赖 `_lib/folder_dialog_win`） |
| `09_快速记录` | 快速捕获 + 示例配置/模板 |
| `10_打开与杂项` | 打开官网/社区等 |
| `_lib` | `folder_dialog_win.py`、`time_stamp_fmt.py`、`npp_eol.py`、`ai_chat_jump.py`、`npp_bootstrap.py`（勿删） |

`scripts/_lib` 与 `scripts_ENG/_lib` 内容应对齐；脚本会自动向上查找本侧 `_lib`。

---

## `00_AI对话跳转`

| 脚本 | 作用 |
|------|------|
| `跳转_<站点>.py` | 打开对应 AI 网页并复制内容（**24** 个单站） |
| `一键跳转_AI.py` | 输入序号 1–24 选站；可选拼接 `提示词.ini` |
| `跳转_提示词再选AI.py` | 先选提示词，再选站点 |
| `提示词.ini` | `[提示词]`：审查/总结/翻译/润色/会议纪要/周报/PR 等 |

逻辑在 `_lib/ai_chat_jump.py`。

---

## `09_快速记录`

运行 `快速捕获.py`。首次选择笔记根目录（写入 `quickadd_config.json`）。  
可选覆盖模板：`quickadd_template_*.md`。示例配置：`quickadd_config.json.example`。

---

## 维护

清空后统一更新见 [../README.md](../README.md)。

## 更新日志

- **2026-08-05**：补齐 `folder_dialog_win`（中文 `_lib`）；`09_快速记录`；明天/昨天中英长串与简短/ISO/周次；模板选择器；Markdown/URL/HTML/Diff；配置AI；第 24 站单站脚本；提示词办公预设；README/快捷键表。
- **2026-05-28**：`00_AI对话跳转` 扩展至 24 站；全部复制粘贴；去掉跳转成功弹窗。
- **2026-05-15**：插入模板空行 + CRLF；`npp_eol`；根目录清空工具。
