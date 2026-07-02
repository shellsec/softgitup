GH Release Fetch — Windows 便携版（含 exe，无需安装 Python）
================================================================

解压到任意目录（路径尽量不含特殊字符），保持本文件夹结构不变。

日常用法（双击 bat，无参数时会提示输入关键词）
------------------------------------------------
  lookup_app.bat          搜 GitHub 清单 → 1立刻下载 2加入并下载 3加入列表 4启用
  search_soft_pages.bat   搜工具/频道介绍页标题（只打开网页）
  search_games.bat        搜 gamer520 游戏页（本地近期列表；无匹配时自动站内搜索，PC/Switch 混排）
  run_saved_apps.bat      按 saved_apps_windows.json 批量更新

也可直接双击同名 .exe（效果相同；无 Python 时 bat 会自动用 exe）。

首次建议
--------
  1. lookup_app.bat drawio  试搜并选 1 立刻下载
  2. 常用软件用 lookup 选 3 加入列表，生成 saved_apps_windows.json
  3. 以后 run_saved_apps.bat 一键更新列表

文件说明
--------
  apps/                   桌面清单（Windows/macOS/Linux JSON，脚本按平台读取）
  apps-mobile/            移动清单（Android APK 下载 / iOS 占位）
  tools/soft_page_check/  search_soft_pages 的标题索引（history、list）
  auto_update.exe         下载引擎（lookup 选 1/2 时会调用）
  update_log.txt          运行后生成于本目录

说明
----
  - 本包不含 Python；维护脚本（monthly_check 等）请使用完整 Git 仓库。
  - 个人列表 saved_apps_windows.json 可在本目录新建，勿覆盖他人配置。
  - 项目：https://github.com/shellsec/gh-release-fetch
