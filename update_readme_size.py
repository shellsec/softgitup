# -*- coding: utf-8 -*-
"""读取 software/list.txt 的统计数据，刷新 README.md / README_EN.md 中的 software/ 体积统计块。

由 generate_and_push.bat 在 soft_manager.py 生成 list.txt 之后调用，
只改写 <!-- SOFTWARE_SIZE_START --> 与 <!-- SOFTWARE_SIZE_END --> 之间的内容。
"""
import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(BASE_DIR, "software", "list.txt")
START_MARK = "<!-- SOFTWARE_SIZE_START -->"
END_MARK = "<!-- SOFTWARE_SIZE_END -->"


def human_size(num_bytes):
    if num_bytes >= 1024 ** 3:
        return "{:.2f} GB".format(num_bytes / (1024 ** 3))
    return "{:.1f} MB".format(num_bytes / (1024 ** 2))


def update_block(readme_path, block):
    name = os.path.basename(readme_path)
    if not os.path.exists(readme_path):
        print("[WARN] 未找到 {}，跳过".format(name))
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_MARK)
    end = content.find(END_MARK)
    if start == -1 or end == -1 or end < start:
        print("[WARN] {} 中未找到统计标记，跳过".format(name))
        return False

    new_content = (
        content[: start + len(START_MARK)] + "\n" + block + "\n" + content[end:]
    )
    if new_content != content:
        with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        print("[OK] {} 体积统计已更新".format(name))
    else:
        print("[OK] {} 体积统计无变化".format(name))
    return True


def main():
    if not os.path.exists(LIST_FILE):
        print("[WARN] 未找到 {}，跳过 README 体积统计".format(LIST_FILE))
        return 1

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_software = data.get("total_software", len(data.get("software", {})))
    total_files = data.get("total_files", 0)
    total_size = data.get("total_size", 0)
    generated_at = data.get("generated_at", "")
    if generated_at:
        try:
            generated_at = datetime.fromisoformat(generated_at).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            pass

    # 按体积排出前 5 大软件目录，便于直观看到空间都花在哪
    top = sorted(
        data.get("software", {}).items(),
        key=lambda kv: kv[1].get("total_size", 0),
        reverse=True,
    )[:5]
    top_pairs = [(name, human_size(info.get("total_size", 0))) for name, info in top]

    files_str = "{:,}".format(total_files)
    size_str = human_size(total_size)

    block_zh = (
        "> 📦 **software/ 体积统计**（`generate_and_push.bat` 自动刷新）：\n"
        "> 共 **{}** 款软件、**{}** 个文件，合计 **{}**；统计时间 {}。\n"
        "> 体积 Top5：{}。".format(
            total_software,
            files_str,
            size_str,
            generated_at or "未知",
            "、".join("{} ({})".format(n, s) for n, s in top_pairs) or "无",
        )
    )
    block_en = (
        "> 📦 **`software/` size stats** (auto-refreshed by `generate_and_push.bat`):\n"
        "> **{}** packages, **{}** files, **{}** total; generated at {}.\n"
        "> Top 5 by size: {}.".format(
            total_software,
            files_str,
            size_str,
            generated_at or "unknown",
            ", ".join("{} ({})".format(n, s) for n, s in top_pairs) or "none",
        )
    )

    ok = update_block(os.path.join(BASE_DIR, "README.md"), block_zh)
    ok = update_block(os.path.join(BASE_DIR, "README_EN.md"), block_en) and ok
    print("[INFO] 统计：{} 款 / {} 文件 / {}".format(total_software, files_str, size_str))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
