# scripts_CHS（中文脚本名）

本目录是 `scripts` 下脚本的**中文文件名副本**，功能与对应英文名脚本完全相同，便于在菜单中按中文名查找、切换使用。

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
| folder_dialog_win.py | folder_dialog_win.py |
| Base64选区编解码.py | base64_selection.py |
| 行尾LF与CRLF.py | line_endings_lf_crlf.py |
| 插入UUID.py | insert_uuid.py |

（`folder_dialog_win.py` 为辅助模块，供「批量TXT转 Markdown」「大纲转drawio」在 **无 tkinter** 时于 Windows 下用 PowerShell 弹窗；须与上述脚本放在同一目录。）

**`0token` 前缀**：仅用于「文字脑图生成/还原」「准备投喂整理」等与 **Token / 投喂前整理** 强相关的脚本；其余为普通本地工具，文件名不再加此前缀。

脚本内容与 `scripts` 中一致，仅文件名不同，可按需在英文/中文脚本名之间切换使用。
