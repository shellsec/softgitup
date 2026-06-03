# Notepad++ PythonScript 脚本集合（scripts_ENG）

这是为 Notepad++ PythonScript 插件编写的实用脚本集合（**英文文件名**），提供文本处理、信息提取和格式化等功能。

配置根目录总览、**清空后统一更新** 见 [../README.md](../README.md)。

## 安装说明

1. 确保已安装 Notepad++（推荐最新版本）
2. 安装 PythonScript 插件：
   - 打开 Notepad++
   - 点击 `Plugins` → `Plugins Admin`
   - 搜索 "PythonScript"
   - 点击 `Install` 按钮安装
3. 将脚本文件复制到 Notepad++ PythonScript 脚本目录：
   - 通常路径：`C:\Program Files\Notepad++\plugins\Config\PythonScript\scripts`
   - 或通过 Notepad++ 菜单：`Plugins` → `PythonScript` → `Scripts` → `Open Scripts Folder` 打开

本仓库中 **`scripts_ENG`** 已按类别分子文件夹（菜单中为**子菜单**）。公共模块在 **`scripts_ENG/_lib`**：`folder_dialog_win.py`、`time_stamp_fmt.py`、`npp_eol.py`、`ai_chat_jump.py`（勿删）。

### 与 `scripts`（中文脚本目录）的关系

| `scripts_ENG` | `scripts` |
|---------------|-----------|
| `00_AI_Chat` | `00_AI对话跳转` |
| `01_Time_Insert` | `01_时间与插入` |
| `02_Lines_Selection` | `02_行与选区` |
| … | … |

- **`01_Time_Insert`**：与中文侧插入模板**字段条数与顺序一致**；`template_block` + CRLF；每条提示后空行。对照见 [scripts/README.md](../scripts/README.md)。
- **`00_AI_Chat`**：24 AI sites in browser; **always copy** selection/full doc, then **Ctrl+V** (including ChatGPT; no URL prefill). No success **messageBox**. Edit **`prompts.ini`** (`[prompts]`). Scripts: `jump_<site>.py`, `jump_ai_menu.py`, `jump_prompt_pick_ai.py`. Logic: `_lib/ai_chat_jump.py` (`from Npp import editor, notepad`). Site order 1–24: see root [README.md](../README.md) section **AI 网页跳转**.

## 使用方法

1. 在 Notepad++ 中打开或选择要处理的文本
2. 点击 `Plugins` → `PythonScript` → `Scripts`
3. 选择相应的脚本即可运行

## 脚本分类与说明

### 一、信息提取类脚本

#### 1. 提取URL和邮箱.py
- **功能**：从选中内容或整个文档中提取所有URL和邮箱地址
- **输出**：提取结果按类型分类，显示总数并复制到剪贴板

#### 2. 提取IP地址.py
- **功能**：提取IPv4和IPv6地址
- **特点**：仅提取有效的IP地址（过滤无效格式如300.1.1.1）

#### 3. 提取电话号码.py
- **功能**：提取各种格式的电话号码
- **支持格式**：
  - 中国手机号：13812345678、139-8765-4321
  - 中国座机：010-12345678、021-87654321
  - 国际电话：+1-555-123-4567、+44 20 1234 5678

### 二、文本处理类脚本

#### 1. 行首添加字符.py
- **功能**：在选中行的行首添加指定字符
- **使用**：运行后输入要添加的字符

#### 2. 行首删除字符.py
- **功能**：删除选中行的行首指定字符
- **使用**：运行后输入要删除的字符（留空则删除第一个字符）

#### 3. 行尾添加字符.py
- **功能**：在选中行的行尾添加指定字符
- **使用**：运行后输入要添加的字符

#### 4. 行尾删除字符.py
- **功能**：删除选中行的行尾指定字符
- **使用**：运行后输入要删除的字符（留空则删除最后一个字符）

#### 5. 合并行.py
- **功能**：将选中的多行合并为一行

#### 6. 分割行.py
- **功能**：将选中的长行按指定字符分割为多行

#### 7. 多行自动编号 (add_line_numbers_NH+123.py)
- **功能**：在选中的多行文字前面自动添加 `1、` `2、` `3、` 格式的编号
- **使用**：先选中多行，再运行脚本

#### 8. 多行自动编号-多种格式 (add_line_numbers_multi_format.py)
- **功能**：在选中多行前添加可选格式的编号
- **支持格式**：
  - `1` = 1. 2. 3.
  - `2` = (1) (2) (3)
  - `3` = ① ② ③
  - `4` = 01、02、03、（补零，可设起始数与位数）
  - `5` = 自定义前缀（如 `0x0` → 0x01 0x02）
- **使用**：先选中多行，运行后先看格式说明，再在输入框输入 1～5 选择格式；选 4 或 5 时可设起始数字、补零位数及自定义前缀

#### 9. 保存选中内容.py
- **功能**：将当前选中的内容保存到新文件
- **使用**：运行后选择保存位置和文件名

#### 10. 插入文件内容.py
- **功能**：在当前光标位置插入指定文件的内容
- **使用**：运行后选择要插入的文件

### 三、编码转换类脚本

#### 1. HTML实体编码解码.py
- **功能**：对选中的HTML实体进行编码或解码
- **支持**：&amp;、&lt;、&gt; 等标准HTML实体

#### 2. URL编码解码.py
- **功能**：对选中的URL进行编码或解码

#### 3. Base64选区编解码（base64_selection.py）
- **功能**：对选中或全文进行 Base64 编码（UTF-8）或解码（自动忽略空白、补全 `=`）

### 四、代码格式化类脚本

#### 1. SQL格式化.py
- **功能**：对选中的SQL代码进行格式化
- **特点**：自动缩进、关键词大写、美化结构

#### 2. JSON格式化.py
- **功能**：对选中的JSON数据进行格式化
- **特点**：自动缩进、美化结构

#### 3. XML格式化.py
- **功能**：对选中的XML数据进行格式化
- **特点**：自动缩进、美化结构

### 五、AI辅助类脚本

#### 1. AI文本分析.py
- **功能**：使用AI对文本内容进行分析

#### 2. AI文本翻译.py
- **功能**：使用AI将文本翻译成指定语言

#### 3. AI文本总结.py
- **功能**：使用AI对长文本进行总结

#### 4. AI代码审查.py
- **功能**：使用AI对代码进行审查和优化建议

#### 5. count_tokens_clipboard.py / count_tokens_insert.py（计算 Token）
- **功能**：统计选中区域或全文的 Token 数，**英文与中文混合**按同一规则计算
- **精确模式**：若已为 PythonScript 所用 Python 安装 `tiktoken`，使用 `cl100k_base`（GPT-3.5/4）或 `o200k_base`（GPT-4o），与 OpenAI API 计费粒度一致
- **近似模式**：未安装 `tiktoken` 时使用字符启发式估算，结果仅供参考
- **count_tokens_clipboard**：**剪贴板**仅含 5 行统计（范围、字符、UTF-8 字节、行数、Token）；弹窗另含方式/编码/说明/安装提示
- **count_tokens_insert**：光标处仅**插入**上述 5 行；弹窗同上（剪贴板不写）
- **安装**：`pip install tiktoken`（与 PythonScript 所用 Python 一致）

#### 6. 带 `0token` 前缀的脚本（与「省 Token / 本地替代云端」强相关）
- **0token_text_mindmap / 0token_text_mindmap_restore**：缩进大纲 ↔ ASCII 脑图（结构可视化，无需调用模型）
- **0token_prep_for_llm**：投喂前整理（空行、遮罩、文末字符/近似 Token 统计），强调**不先烧 API**

其余本地文本工具**不使用 AI，也无需** `0token` 文件名前缀，见下节。

#### 7. 其他本地工具（无 `0token` 前缀）
- **outline_indent / 大纲缩进**：每行增加或减少 2 个前导空格（Tab 按 4 列展开）
- **sensitive_mask / 敏感信息遮罩**：邮箱、中国手机号、身份证、`sk-…`、`AKIA…` → `[MASKED:…]` / `[已遮罩:…]`
- **mermaid_mindmap / Mermaid脑图**：与脑图生成相同缩进规则，输出 ```mermaid mindmap 代码块
- **csv_to_md_table / CSV转Markdown表**：CSV/TSV → Markdown 表
- **path_normalize / 路径斜杠统一**：`/` 或 `\\` 统一
- **fw_hw_convert / 全角半角转换**：常见全角数字字母标点、全角空格 ↔ 半角（映射有限）
- **unicode_normalize / Unicode规范化**：NFC / NFD / NFKC / NFKD
- **sort_lines / 行排序去重**：排序或去重保序
- **todo_toggle / 待办切换**：Markdown `[ ]` ↔ `[x]`
- **git_conflict_split / Git冲突拆分**：`<<<<<<<` 冲突块拆成 OURS / THEIRS 分段
- **batch_txt_to_md / 批量TXT转Markdown**：选择输入/输出目录，递归 `.txt` → `.md`（UTF-8，保持相对路径）；**无需 pip**。有 **tkinter** 用自带对话框；**无 tkinter 时（Windows）** 使用 **scripts_ENG/_lib/folder_dialog_win.py** 调 PowerShell + WinForms
- **outline_to_drawio / 大纲转drawio**：缩进大纲 → **draw.io** `.drawio` XML；保存路径同上（tkinter 或 **folder_dialog_win.py** 回退）
- **folder_dialog_win.py**：位于 **scripts_ENG/_lib**（菜单中单独运行会提示）；勿删；依赖脚本会自动向上查找 `_lib`
- **base64_selection / Base64选区编解码**：选中或全文 Base64 编码（UTF-8）/ 解码（忽略空白）
- **line_endings_lf_crlf / 行尾LF与CRLF**：选中或全文统一为 LF 或 CRLF
- **insert_uuid / 插入UUID**：光标处插入 UUID（可选数量、标准或 32 位 hex）

## 脚本结构说明

所有脚本都遵循相似的结构：

1. **文本获取**：支持处理选中内容或整个文档
2. **核心处理**：使用正则表达式或字符串处理进行实际操作
3. **结果展示**：通过消息框显示处理结果
4. **剪贴板操作**：自动将结果复制到剪贴板（如适用）
5. **撤销支持**：所有修改都支持撤销操作

## 注意事项

1. **权限问题**：部分脚本可能需要管理员权限才能正常运行
2. **大型文件**：处理大型文件时可能会占用较多系统资源
3. **编码问题**：建议使用UTF-8编码保存脚本文件
4. **自定义修改**：可以根据需要修改脚本代码以适应特定需求

## 故障排除

- 如果脚本运行失败，检查是否已正确安装 PythonScript 插件
- 确保脚本文件编码为 UTF-8
- 检查脚本是否有语法错误（可以用 Notepad++ 语法高亮功能查看）
- 查看 Notepad++ 控制台输出（`Plugins` → `PythonScript` → `Show Console`）以获取详细错误信息

## 维护：清空后统一更新

在 **PythonScript 配置根目录**（`scripts_ENG` 的上一级）运行 `清空PythonScript脚本.cmd` 或 `Clear-PythonScriptScripts.ps1`，可清空 `scripts`、`scripts_ENG`、`scripts_CHS`（若存在）内的旧文件，再从仓库整包复制。详见 [../README.md](../README.md)。

## 更新日志

- 2026-05-28：
  - **`00_AI_Chat`**：24 mainstream AI sites; all use clipboard + paste (ChatGPT no URL `?q=`); no success popups; `00_` menu prefix; `getSelText()` fix; README sync.
- 2026-05-15：
  - 配置根目录新增清空工具（`清空PythonScript脚本.cmd` / `Clear-PythonScriptScripts.ps1`）；根 [README.md](../README.md) 说明统一更新流程。
  - `01_Time_Insert` 插入模板与 `scripts/01_时间与插入` **字段对齐**（英文提示）；每条提示后保留空行；README 补充与 `scripts` 的对应说明。
- 2026-04-28：
  - 新增：`base64_selection.py`、`line_endings_lf_crlf.py`、`insert_uuid.py`（及中文文件名对应脚本）
- 2026-03-06：
  - 新增多行自动编号脚本：`add_line_numbers_NH+123.py`（固定格式 1、2、3、）
  - 新增多行自动编号-多种格式：`add_line_numbers_multi_format.py`（可选 1. 2. / (1)(2) / ①②③ / 01、02、/ 自定义前缀如 0x0）
  - 更新 README 文本处理类脚本说明
- 2025-12-16：
  - 添加 README.md 文档
  - 优化提取类脚本的正则表达式
  - 统一脚本结构和风格

## 贡献

欢迎提交新的脚本或改进建议！

## 许可证

本脚本集合采用 MIT 许可证，可自由使用和修改。
