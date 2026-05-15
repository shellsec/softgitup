# scripts（中文脚本目录）

本目录为 Notepad++ **PythonScript** 的默认脚本树（中文文件夹与中文 `.py` 文件名）。配置根目录说明、**统一更新（清空后覆盖）** 见上级 [../README.md](../README.md)。

若另有 **`scripts_CHS`**，则为**仅改文件名**的中文副本，功能与 `scripts` 对应项相同，便于在菜单中按另一套中文名查找。

## 如何切换使用

- **只用中文脚本名**：在 Notepad++ 中打开  
  `Plugins` → `Python Script` → **Configuration** → **Initialisation**，  
  将 “Script folder” 从 `scripts` 改为 `scripts_CHS`（或填本目录完整路径），重启 Notepad++ 后菜单中即显示中文脚本名。
- **同时显示中英文**：若 PythonScript 支持多个脚本目录，可在配置里添加 `scripts_CHS` 为额外脚本目录，则 `scripts` 与 `scripts_CHS` 中的脚本会同时出现在菜单中（一份英文名、一份中文名）。

## 文件名对应关系

| 中文文件名 | 对应 scripts 下的英文脚本 |
|-----------|---------------------------|
| 多格式添加行号.py | add_line_numbers_multi_format.py |
| 行号一二三格式.py | add_line_numbers_NH+123.py |
| 获取网络信息.py | get_network_info.py |
| 获取系统信息.py | get_system_info.py |
| 获取本机IP.py | get_local_ip.py |
| 获取MAC地址.py | get_mac_address.py |
| 获取公网IP.py | get_public_ip.py |
| 显示NPP脚本参考.py | show_npp_scripts.py |
| 取消用记事本打开.py | reg_del_use_notepad_open.py |
| 插入时间.py | InsertTime.py |
| 插入时间中文.py | InsertTimeCN.py |
| AI文本分析.py | ai_text_analyze.py |
| AI文本摘要.py | ai_text_summarize.py |
| AI文本翻译.py | ai_text_translate.py |
| AI代码审查.py | ai_code_review.py |
| 提取电话号码.py | extract_phone_numbers.py |
| 提取IP地址.py | extract_ip_addresses.py |
| 提取网址与邮箱.py | extract_urls_emails.py |
| 格式化SQL.py | format_sql.py |
| 格式化JSON.py | format_json.py |
| 格式化XML.py | format_xml.py |
| 保存选中文本.py | save_selected_text.py |
| ASCII艺术字生成.py | ascii_art_generator.py |
| 摩尔斯电码.py | morse_code.py |
| 文本格式转换.py | text_format_convert.py |
| 时间戳转换.py | timestamp_convert.py |
| 生成随机字符串.py | generate_random_string.py |
| 打开Notepad++社区.py | opencommunity-notepad-plus-plus.py |
| 打开Notepad++.py | opennotepad-plus-plus.py |
| 计算Token数_剪贴板.py | count_tokens_clipboard.py |
| 计算Token数_插入.py | count_tokens_insert.py |
| 0token文字脑图生成.py | 0token_text_mindmap.py |
| 0token文字脑图还原.py | 0token_text_mindmap_restore.py |
| 0token准备投喂整理.py | 0token_prep_for_llm.py |
| 大纲缩进.py | outline_indent.py |
| 敏感信息遮罩.py | sensitive_mask.py |
| Mermaid脑图.py | mermaid_mindmap.py |
| CSV转Markdown表.py | csv_to_md_table.py |
| 路径斜杠统一.py | path_normalize.py |
| 全角半角转换.py | fw_hw_convert.py |
| Unicode规范化.py | unicode_normalize.py |
| 行排序去重.py | sort_lines.py |
| 待办切换.py | todo_toggle.py |
| Git冲突拆分.py | git_conflict_split.py |
| 批量TXT转Markdown.py | batch_txt_to_md.py |
| 大纲转drawio.py | outline_to_drawio.py |
| folder_dialog_win.py（在 `_lib`） | folder_dialog_win.py（在 `_lib`） |
| Base64选区编解码.py | base64_selection.py |
| 行尾LF与CRLF.py | line_endings_lf_crlf.py |
| 插入UUID.py | insert_uuid.py |
| 插入模板_工作.py | insert_template_work.py |
| 工作日记_三点.py | work_daily_three.py |
| 工作日记_流水.py | work_daily_log.py |
| 插入模板_生活.py | insert_template_life.py |
| 插入模板_学习.py | insert_template_study.py |
| 插入模板_健康.py | insert_template_health.py |
| 插入模板_灵感.py | insert_template_ideas.py |
| 插入模板_家庭.py | insert_template_family.py |
| 插入模板_财务.py | insert_template_money.py |
| 插入模板_随记.py | insert_template_scratch.py |
| 插入模板_社交.py | insert_template_social.py |
| 插入模板_阅读.py | insert_template_reading.py |
| 插入模板_项目.py | insert_template_project.py |
| 插入模板_运动.py | insert_template_workout.py |
| 插入模板_情绪.py | insert_template_mood.py |
| 插入模板_副业.py | insert_template_side_gig.py |

## 目录结构（分类子文件夹）

脚本按用途放在 `scripts` 下的子文件夹中；Notepad++ 菜单 **Plugins → Python Script → Scripts** 中会显示**与文件夹同名的子菜单**。

| 子文件夹 | 内容概要 |
|----------|----------|
| `_lib` | 公共模块：`folder_dialog_win.py`、`time_stamp_fmt.py`（长串日期）、`npp_eol.py`（Windows CRLF 下多行插入用 `template_block`，避免只写 `\n` 时换行异常）。勿删。 |
| `01_时间与插入` | 长串日期、UUID；各**插入模板**：首行长串日期，下接各字段行；**每条提示后留一空行**便于填写；换行由 `_lib/npp_eol.template_block` 统一为 CRLF（Windows）。**英文文件名、同字段**对照在 **`scripts_ENG/01_Time_Insert`**。 |
| `02_行与选区` | 行尾、排序、待办、行号、Git 冲突拆分、Base64、大纲缩进、保存选区等 |
| `03_编码与字符` | 全角半角、Unicode、路径斜杠 |
| `04_格式化与转换` | JSON/XML/SQL、CSV→MD、Mermaid、时间戳、ASCII、摩尔斯等 |
| `05_提取与遮罩` | 电话/IP/网址提取、敏感信息遮罩 |
| `06_系统与网络` | 本机与网络信息、IP/MAC 等 |
| `07_AI与Token` | AI 文本脚本、0token 系列、Token 计数 |
| `08_文档与导图` | 批量 TXT→MD、大纲转 draw.io |
| `09_快速捕获` | （当前 `scripts` 树未包含此文件夹时可忽略） |
| `10_打开与杂项` | 打开官网/社区、脚本参考、注册表、随机串等 |

（`folder_dialog_win.py`、`time_stamp_fmt.py`、`npp_eol.py` 位于各侧的 `_lib`：`scripts/_lib` 与 `scripts_ENG/_lib` 内容对齐；依赖脚本会自动向上查找本侧的 `_lib`。）

**`scripts_ENG`**：英文脚本名与 `01_Time_Insert` 等子目录；插入模板与 `scripts/01_时间与插入` **字段一一对应**（提示为英文）。

**`0token` 前缀**：仅用于「文字脑图生成/还原」「准备投喂整理」等与 **Token / 投喂前整理** 强相关的脚本；其余为普通本地工具，文件名不再加此前缀。

脚本内容与 `scripts` 中一致，仅文件名不同，可按需在英文/中文脚本名之间切换使用。

## 维护：清空后统一更新

在 **PythonScript 配置根目录**（`scripts` 的上一级）运行 `清空PythonScript脚本.cmd` 或 `Clear-PythonScriptScripts.ps1`，可清空 `scripts`、`scripts_ENG`、`scripts_CHS`（若存在）内的旧文件，再从仓库整包复制。详见 [../README.md](../README.md)。
