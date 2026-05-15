# Notepad++ PythonScript 配置目录

本目录为 Notepad++ **PythonScript** 插件配置根（通常为 `plugins\Config/PythonScript`）。脚本按语言分两套子目录，**不要**把清空工具放进 `scripts` 菜单目录内。

| 目录 / 文件 | 说明 |
|-------------|------|
| **`scripts/`** | 中文脚本名（子菜单为中文文件夹名）。详见 [scripts/README.md](scripts/README.md) |
| **`scripts_ENG/`** | 英文脚本名（与 `scripts` 字段对应）。详见 [scripts_ENG/README.md](scripts_ENG/README.md) |
| **`scripts_CHS/`** | 可选；仅中文**文件名**副本时存在 |

在 N++ 里将 **Script folder** 指向 `scripts` 或 `scripts_ENG` 之一即可；两套可同时保留于磁盘，换目录后重启 Notepad++。

---

## 统一更新脚本（清空后覆盖）

根目录提供**维护用**清空工具，用于删除旧版残留后再从本仓库或备份整包复制 `scripts` / `scripts_ENG`（及可选的 `scripts_CHS`）。

| 文件 | 用途 |
|------|------|
| **`清空PythonScript脚本.cmd`** | 双击或命令行运行（推荐）；纯 ASCII，避免 cmd 解析 `powershell.exe` 异常 |
| **`Clear-PythonScriptScripts.ps1`** | 实际逻辑（英文路径，供 `.cmd` 调用） |
| **`清空PythonScript脚本.ps1`** | 中文名包装，内部调用 `Clear-PythonScriptScripts.ps1` |

**会清空的内容**（仅删除这些文件夹**内部**的全部文件与子文件夹，不删文件夹本身，也不动根目录其它文件）：

- `scripts/`
- `scripts_ENG/`
- `scripts_CHS/`（若存在）

**建议使用流程**

1. 关闭 Notepad++（避免脚本文件被占用）。
2. 在本目录运行清空工具并确认。
3. 将仓库或备份中的 `scripts`、`scripts_ENG`（及需要的 `scripts_CHS`）整目录复制进来。
4. 重新打开 Notepad++，确认 **Script folder** 指向正确子目录。

**命令示例**（在配置根目录下）：

```bat
REM 预览，不删除
清空PythonScript脚本.cmd -WhatIf

REM 交互确认后清空
清空PythonScript脚本.cmd

REM 不询问，直接清空
清空PythonScript脚本.cmd -Force
```

```powershell
.\Clear-PythonScriptScripts.ps1 -WhatIf
.\Clear-PythonScriptScripts.ps1
.\Clear-PythonScriptScripts.ps1 -Force
```

若 `.cmd` 报错，请直接用 PowerShell 运行 `Clear-PythonScriptScripts.ps1`（勿在 `.cmd` 的 `-File` 参数中使用仅中文路径）。

---

## 插入模板（简要）

- 首行：长串日期（`time_stamp_fmt`）。
- 各字段行后**留一空行**便于填写；块末 `---`。
- Windows 多行插入经 `_lib/npp_eol.py` 的 `template_block` 使用 **CRLF**。
- 中英文模板字段一一对应：`scripts/01_时间与插入` ↔ `scripts_ENG/01_Time_Insert`。

更多分类与子目录说明见各子目录 README。
