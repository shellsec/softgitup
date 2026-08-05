# Notepad++ PythonScript 配置目录

本目录为 Notepad++ **PythonScript** 插件配置根（通常为 `plugins\Config\PythonScript`）。脚本按语言分两套子目录；根目录下的 **清空工具** 不要复制进 `scripts` 菜单。

| 目录 / 文件 | 说明 |
|-------------|------|
| **`scripts/`** | 中文文件夹与中文脚本名（推荐日常使用）。详见 [scripts/README.md](scripts/README.md) |
| **`scripts_ENG/`** | 英文脚本名，与 `scripts` 功能对应。详见 [scripts_ENG/README.md](scripts_ENG/README.md) |

在 N++ 中：**Plugins → Python Script → Configuration → Initialisation**，将 **Script folder** 设为 `scripts` 或 `scripts_ENG` 的完整路径，保存后重启 Notepad++。

---

## 子菜单一览（`scripts`）

| 前缀 | 文件夹 | 用途 |
|------|--------|------|
| `00_` | `00_AI对话跳转` | 浏览器打开主流 AI 对话页，复制选区/全文后粘贴 |
| `01_` | `01_时间与插入` | 长串日期、简短/ISO/周次、UUID、分类日记模板、模板选择器 |
| `02_` | `02_行与选区` | 行号、排序、待办、Git 冲突、Base64、选区↔剪贴板 Diff 等 |
| `03_` | `03_编码与字符` | 全角半角、Unicode、路径、URL/HTML 实体编解码 |
| `04_` | `04_格式化与转换` | JSON/XML/SQL、CSV、Mermaid、Markdown 工具等 |
| `05_` | `05_提取与遮罩` | 电话/IP/网址、敏感信息遮罩 |
| `06_` | `06_系统与网络` | 本机与网络信息 |
| `07_` | `07_AI与Token` | 本地 AI API、配置向导、Token 统计、0token 系列（非网页跳转） |
| `08_` | `08_文档与导图` | 批量 TXT→MD、大纲→draw.io |
| `09_` | `09_快速记录` | QuickAdd 快速捕获（笔记根目录 + 提问模板） |
| `10_` | `10_打开与杂项` | 打开官网/社区等 |

公共模块在 **`scripts/_lib`** 与 **`scripts_ENG/_lib`**：`folder_dialog_win.py`、`time_stamp_fmt.py`、`npp_eol.py`、`ai_chat_jump.py`、`npp_bootstrap.py`。

---

## 推荐快捷键（Shortcut Mapper）

在 **Settings → Shortcut Mapper → Plugin commands** 中搜索脚本名并绑定（示例，可按习惯改）：

| 建议键 | 脚本（中文菜单） | 用途 |
|--------|------------------|------|
| `Ctrl+Alt+T` | `插入时间中文` | 今天长串日期 |
| `Ctrl+Alt+Shift+T` | `插入时间_简短` | `YYYY-MM-DD HH:mm` |
| `Ctrl+Alt+D` | `待办切换` | Markdown `[ ]` ↔ `[x]` |
| `Ctrl+Alt+A` | `一键跳转_AI` | 选站打开 AI 网页 |
| `Ctrl+Alt+Q` | `快速捕获` | QuickAdd 落盘 |
| `Ctrl+Alt+M` | `插入模板选择器` | 一次选日记模板 |
| `Ctrl+Alt+U` | `插入UUID` | UUID |

英文 Script folder 时对应：`InsertTimeCN`、`InsertTimeShort`、`todo_toggle`、`jump_ai_menu`、`quickadd_capture`、`insert_template_picker`、`insert_uuid`。

---

## 统一更新（清空后覆盖）

| 文件 | 说明 |
|------|------|
| `清空PythonScript脚本.cmd` | 双击运行（推荐，纯 ASCII） |
| `Clear-PythonScriptScripts.ps1` | 实际逻辑 |
| `清空PythonScript脚本.ps1` | 中文名包装 |

仅清空 **`scripts/`、`scripts_ENG/`** 内部文件（若存在 `scripts_CHS/` 也会清），不删文件夹本身，也不动根目录其它文件。

1. 关闭 Notepad++
2. 运行清空工具并确认（`-WhatIf` 仅预览，`-Force` 不询问）
3. 从仓库整包复制 `scripts`、`scripts_ENG` 回来
4. 重启 N++，确认 Script folder 路径正确

```bat
清空PythonScript脚本.cmd -WhatIf
清空PythonScript脚本.cmd
```

---

## 插入模板（`01_时间与插入`）

- 首行：长串日期（`time_stamp_fmt.format_cn` / `format_en`）。
- 字段行与分类名直连（如 `工作今天：`）；**每条提示后留一空行**；块末 `---`。
- Windows 多行插入使用 `_lib/npp_eol.template_block`（**CRLF**）。
- 中英文模板字段一致：`01_时间与插入` ↔ `scripts_ENG/01_Time_Insert`。
- 可用 **`插入模板选择器`** / `insert_template_picker` 一次选分类。

另有：今天/明天/昨天（中文或英文长串）、`插入时间_简短`、`插入时间_ISO`、`插入周次中文`。

---

## AI 网页跳转（`00_AI对话跳转` / `00_AI_Chat`）

与 **`07_AI与Token`**（API/Token/本地整理）分开；`00_` 前缀使该子菜单排在最前。

### 行为

| 项 | 说明 |
|----|------|
| 文本来源 | 有**选区**用选区；否则用**当前文档全文** |
| 打开方式 | 默认浏览器打开对应 URL |
| 内容传递 | **全部站点统一**：静默**复制到剪贴板**，在网页输入框 **Ctrl+V**（含 ChatGPT，避免 URL 过长失败） |
| 弹窗 | 跳转过程**无 messageBox**；`一键跳转_AI` / `跳转_提示词再选AI` 仍用 **prompt** 选序号 |
| 提示词 | `scripts/00_AI对话跳转/提示词.ini` 或 `scripts_ENG/00_AI_Chat/prompts.ini` |

### 菜单脚本

- **单站**：`跳转_ChatGPT.py` … `跳转_智谱开放平台.py`（共 **24** 个单站）+ 菜单两项。
- **`一键跳转_AI.py`**：输入 **1–24** 选站点，可选是否拼接提示词。
- **`跳转_提示词再选AI.py`**：先选提示词，再选站点。

### 站点列表（`一键跳转_AI` 输入 1–24）

1 ChatGPT · 2 Claude · 3 Gemini · 4 Copilot · 5 Perplexity · 6 Grok · 7 Poe · 8 Meta AI ·  
9 DeepSeek · 10 Kimi · 11 通义千问 · 12 豆包 · 13 文心一言 · 14 腾讯元宝 · 15 智谱清言 ·  
16 讯飞星火 · 17 秘塔 AI · 18 天工 AI · 19 阶跃星辰 · 20 MiniMax · 21 扣子 Coze ·  
22 百川 · 23 零一万物 · 24 智谱开放平台  

增删或改链接：编辑 `scripts/_lib/ai_chat_jump.py`（`scripts_ENG/_lib` 同步）中的 **`SERVICES`**、**`SERVICE_ORDER`**。

---

## 快速记录（`09_快速记录` / `09_QuickAdd`）

运行 **`快速捕获`** / `quickadd_capture`：新建笔记、追加日记、剪贴板入日记、光标插入模板、设置笔记根目录。  
首次会弹出目录选择（依赖 `_lib/folder_dialog_win.py`）。示例见目录内 `quickadd_config.json.example` 与 `quickadd_template_*.md`。

---

## 更多说明

- 中文脚本目录详解：[scripts/README.md](scripts/README.md)
- 英文脚本目录详解：[scripts_ENG/README.md](scripts_ENG/README.md)
