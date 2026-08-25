# 移动端软件清单索引（apps-mobile）

> 自动生成：`python tools/generate_mobile_catalog_index.py`。生成时间：**2026-08-25 07:36 UTC**

与桌面 [`apps/`](apps/) 分离。Android 走 GitHub Release APK；iOS 多为 App Store 占位。

## 规模概览

| 平台 | 条目数 | 已启用 | 分片数 |
|------|--------|--------|--------|
| android | 252 | 0 | 39 |
| ios | 123 | 0 | 15 |

## 常用命令

```bat
python lookup_app.py --apps-dir apps-mobile --platform android 微信
python lookup_app.py --apps-dir apps-mobile --platform ios 微信
python auto_update.py --apps-dir apps-mobile --platform android termux
```

下载目录默认：`./android/`（`download_subdir_by_platform: true`）。**仅下载 APK，不自动安装。** iOS 为 App Store 占位，lookup 选 **1/5** 打开商店页。

## 分片一览

| 分片 | 分类 | Android | iOS |
|------|------|---------|-----|
| `01-AI.json` | AI | 6 | 2 |
| `01-工具.json` | 工具 | 9 | 0 |
| `02-下载.json` | 下载 | 5 | 1 |
| `03-写作.json` | 写作 | 7 | 2 |
| `04-办公.json` | 办公 | 9 | 5 |
| `04-多媒体.json` | 多媒体 | 5 | 0 |
| `05-办公与设计.json` | 办公与设计 | 4 | 0 |
| `05-安全.json` | 安全 | 10 | 0 |
| `06-命令行.json` | 命令行 | 3 | 0 |
| `06-网络.json` | 网络 | 6 | 0 |
| `07-备份.json` | 备份 | 10 | 5 |
| `07-笔记.json` | 笔记 | 3 | 0 |
| `08-多媒体.json` | 多媒体 | 17 | 2 |
| `08-输入.json` | 输入 | 6 | 1 |
| `09-多媒体与设计.json` | 多媒体与设计 | 3 | 0 |
| `09-通讯.json` | 通讯 | 3 | 0 |
| `10-安全.json` | 安全 | 4 | 0 |
| `10-浏览器.json` | 浏览器 | 7 | 3 |
| `11-工具.json` | 工具 | 19 | 12 |
| `11-智能家居.json` | 智能家居 | 2 | 0 |
| `12-开发.json` | 开发 | 5 | 0 |
| `13-效率.json` | 效率 | 5 | 0 |
| `14-游戏.json` | 游戏 | 8 | 2 |
| `15-笔记.json` | 笔记 | 3 | 0 |
| `16-系统.json` | 系统 | 6 | 0 |
| `17-终端.json` | 终端 | 2 | 0 |
| `18-网络.json` | 网络 | 7 | 0 |
| `19-网络与协作.json` | 网络与协作 | 4 | 0 |
| `20-网络与通讯.json` | 网络与通讯 | 25 | 17 |
| `21-远程与协作.json` | 远程与协作 | 10 | 7 |
| `22-音视频.json` | 音视频 | 13 | 9 |
| `23-数据库.json` | 数据库 | 3 | 0 |
| `24-云原生.json` | 云原生 | 2 | 0 |
| `25-可观测.json` | 可观测 | 2 | 0 |
| `26-编辑器.json` | 编辑器 | 2 | 0 |
| `27-金融与股票.json` | 金融与股票 | 5 | 3 |
| `28-加密货币.json` | 加密货币 | 4 | 0 |
| `29-局域网文件共享.json` | 局域网文件共享 | 1 | 0 |
| `30-代理与隧道.json` | 代理与隧道 | 7 | 0 |
| `99-占位-AppStore.json` | 占位-AppStore | 0 | 52 |

## 维护脚本

- `tools/append_mobile_catalog_batch1.py` — 首批 Android + iOS 占位
- `tools/append_mobile_catalog_batch2.py` — v2rayNG、SmsForwarder
- `tools/append_mobile_catalog_batch3.py` — 按桌面 30 分类大补 Android
- `tools/append_mobile_catalog_batch4.py` — NipaPlay-Reload、NextPlayer、mpv-android
- `tools/append_mobile_catalog_batch5.py` — Android 薄分类 + iOS 占位扩展
- `tools/append_mobile_catalog_batch6.py` — Android / iOS 尽量全覆盖
- `tools/append_mobile_catalog_batch7.py` — Facebook / Instagram / Telegram 等社交通讯
- `tools/append_mobile_catalog_batch8.py` — 各分类装机必备（微信/Chrome/YouTube 等）
- `tools/append_mobile_catalog_batch9.py` — iOS 装机必备 App Store 占位（对齐 Android）

