# scripts_ENG (English script tree)

English filenames for Notepad++ **PythonScript**. Root overview, update/clear tools, and **recommended shortcuts** live in [../README.md](../README.md).

## Install / switch

1. Install Notepad++ + PythonScript plugin.
2. Set **Script folder** to this directory’s full path:  
   `Plugins → Python Script → Configuration → Initialisation`  
   (Chinese UI: point at `../scripts` instead.)
3. Restart Notepad++.

Shared helpers: **`scripts_ENG/_lib`** — `folder_dialog_win.py`, `time_stamp_fmt.py`, `npp_eol.py`, `ai_chat_jump.py`, `npp_bootstrap.py`.

## Folders vs Chinese tree

| `scripts_ENG` | `scripts` |
|---------------|-----------|
| `00_AI_Chat` | `00_AI对话跳转` |
| `01_Time_Insert` | `01_时间与插入` |
| `02_Lines_Selection` | `02_行与选区` |
| `03_Encoding_Chars` | `03_编码与字符` |
| `04_Format_Convert` | `04_格式化与转换` |
| `05_Extract_Mask` | `05_提取与遮罩` |
| `06_System_Network` | `06_系统与网络` |
| `07_AI_Token` | `07_AI与Token` |
| `08_Docs_Diagram` | `08_文档与导图` |
| `09_QuickAdd` | `09_快速记录` |
| `10_Open_Misc` | `10_打开与杂项` |

Template field order matches Chinese side (`template_block` + CRLF). Filename map: [../scripts/README.md](../scripts/README.md).

## Highlights

### `00_AI_Chat`
24 sites; always **copy** selection/full doc → browser → **Ctrl+V**.  
`jump_<site>.py`, `jump_ai_menu.py`, `jump_prompt_pick_ai.py`, `prompts.ini` (meeting notes, weekly report, PR, etc.).

### `01_Time_Insert`
Long stamps (`InsertTime` / `InsertTimeCN`), tomorrow/yesterday (EN + CN), short/ISO/week, UUID, 14 templates + `insert_template_picker.py`, work diaries.

### `02_Lines_Selection`
Line numbers, sort/dedupe, todo toggle, Git conflict split, Base64, line endings, outline indent, **`diff_selection_clipboard.py`**.

### `03_Encoding_Chars`
FW/HW, Unicode normalize, path normalize, **`url_encode_decode.py`**, **`html_entity_encode_decode.py`**.

### `04_Format_Convert`
JSON/XML/SQL, CSV→MD, Mermaid, Morse, ASCII art, timestamp convert, **`markdown_tools.py`**.

### `07_AI_Token`
API summarize/translate/analyze/review; **`configure_ai.py`** (OpenAI / DeepSeek / Qwen / custom); token count; 0token mindmap/prep. See `AI_CONFIG.txt`, `ai_config.json.example`.

### `08_Docs_Diagram`
`batch_txt_to_md.py`, `outline_to_drawio.py` (tkinter or `_lib/folder_dialog_win.py`).

### `09_QuickAdd`
`quickadd_capture.py` + `quickadd_config.json.example` + `quickadd_template_*.md`.

### `10_Open_Misc`
Community/home links, random string, `manage_context_menu.bat` (admin; looks for `notepad++.exe` under `D:\Program Files\notepad++\`).

## Maintenance

From the **config root** (parent of `scripts_ENG`), run `清空PythonScript脚本.cmd` / `Clear-PythonScriptScripts.ps1`, then copy trees back. See [../README.md](../README.md).

## Changelog

- **2026-08-05**: CN/EN parity pass — QuickAdd CN, folder_dialog on CN `_lib`, tomorrow/yesterday EN stamps, template picker, Markdown/URL/HTML/Diff, configure_ai, `jump_zhipu_open`, prompt presets, README cleanup + shortcuts.
- **2026-05-28**: 24 AI sites; clipboard paste; no success popups.
- **2026-05-15**: Template blank lines + CRLF; clear tools at config root.
