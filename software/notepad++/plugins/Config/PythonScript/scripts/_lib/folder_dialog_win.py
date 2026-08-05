# -*- coding: utf-8 -*-
"""
Folder / save-file dialogs: try tkinter first; if missing on Windows, use
PowerShell -STA + System.Windows.Forms. No pip deps.

Paths are returned via a UTF-8 temp file (not stdout) so non-ASCII paths are not
garbled by console code page mismatches between PowerShell and Python.
"""

import os
import subprocess
import sys
import tempfile


def _ps_run_write_result(command, timeout=300):
    """
    Run PowerShell -STA with `command`. On success the script must write the
    chosen path as UTF-8 (no BOM) to the file named by env _NPP_PS_OUT.
    Returns stripped path or "".
    """
    outpath = None
    try:
        fd, outpath = tempfile.mkstemp(prefix="nppdlg_", suffix=".txt")
        os.close(fd)
        os.environ["_NPP_PS_OUT"] = outpath
        subprocess.run(
            ["powershell", "-NoProfile", "-STA", "-Command", command],
            capture_output=True,
            timeout=timeout,
        )
        if not os.path.isfile(outpath):
            return ""
        try:
            with open(outpath, "r", encoding="utf-8") as fp:
                return fp.read().strip().strip("\r\n")
        except Exception:
            return ""
    except Exception:
        return ""
    finally:
        os.environ.pop("_NPP_PS_OUT", None)
        if outpath:
            try:
                os.remove(outpath)
            except OSError:
                pass


def ask_directory(title):
    """Return normalized folder path or None if cancelled / failed."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        root.update()
        p = filedialog.askdirectory(title=title)
        root.destroy()
        return os.path.normpath(p) if p else None
    except Exception:
        pass

    if sys.platform != "win32":
        return None

    os.environ["_NPP_DIR_TITLE"] = title[:2000]
    try:
        cmd = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$f = New-Object System.Windows.Forms.FolderBrowserDialog; "
            "$f.Description = $env:_NPP_DIR_TITLE; "
            "$f.ShowNewFolderButton = $true; "
            "if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) { "
            "[System.IO.File]::WriteAllText("
            "$env:_NPP_PS_OUT, $f.SelectedPath, "
            "[System.Text.UTF8Encoding]::new($false)) "
            "}"
        )
        path = _ps_run_write_result(cmd)
        return os.path.normpath(path) if path else None
    finally:
        os.environ.pop("_NPP_DIR_TITLE", None)


def ask_save_filename(title, initialfile, filetypes):
    """
    filetypes: list of (description, pattern) for tkinter, e.g.
    [("draw.io", "*.drawio"), ("XML", "*.xml"), ("All", "*.*")]
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        root.update()
        ext = os.path.splitext(initialfile)[1] or ".drawio"
        p = filedialog.asksaveasfilename(
            title=title,
            defaultextension=ext,
            initialfile=os.path.basename(initialfile),
            filetypes=filetypes,
        )
        root.destroy()
        return p if p else None
    except Exception:
        pass

    if sys.platform != "win32":
        return None

    os.environ["_NPP_SAVE_TITLE"] = title[:1000]
    os.environ["_NPP_SAVE_FILE"] = os.path.basename(initialfile)[:500]
    try:
        cmd = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$s = New-Object System.Windows.Forms.SaveFileDialog; "
            "$s.Title = $env:_NPP_SAVE_TITLE; "
            "$s.FileName = $env:_NPP_SAVE_FILE; "
            "$s.Filter = 'draw.io (*.drawio)|*.drawio|XML (*.xml)|*.xml|All (*.*)|*.*'; "
            "$s.FilterIndex = 1; "
            "if ($s.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) { "
            "[System.IO.File]::WriteAllText("
            "$env:_NPP_PS_OUT, $s.FileName, "
            "[System.Text.UTF8Encoding]::new($false)) "
            "}"
        )
        path = _ps_run_write_result(cmd)
        return path if path else None
    finally:
        os.environ.pop("_NPP_SAVE_TITLE", None)
        os.environ.pop("_NPP_SAVE_FILE", None)


if __name__ == "__main__":
    try:
        notepad.messageBox(
            "此文件为辅助模块，请运行：批量TXT转Markdown / 大纲转drawio / 快速捕获。",
            "folder_dialog_win",
            0,
        )
    except NameError:
        pass
