# 洛雪音乐 Open API 控制端

**语言 / Language:** 中文 | [English](README.en.md)

[aiv123.com](https://aiv123.com/) · AI 工具导航，600+ 工具一网打尽

## 🚀 推荐使用 [ofox.ai](https://ofox.io/x/aiv123)

> **一句话**：一个账号直达最新 GPT / Claude / Gemini 等 **100+** 顶尖模型，首充额外赠 **$3** 额度。

文本、图像、视频、向量一站调用；支持缓存，重复请求更省更快。

[👉 注册领取](https://ofox.io/x/aiv123) · 全球专线 · 企业级 SLA · 不留存对话

| ⚡️ 极速更省 | 🧠 模型与模态 | 🛡️ 隐私安全 |
|:---:|:---:|:---:|
| 全球专线，企业级 SLA，支持缓存 | 100+ 模型 · 文本 / 图像 / 视频 / 向量 | 不留存任何对话 |

## ☕ 请我喝可乐

开源不易，欢迎赞助支持：  
👉 [爱发电](https://ifdian.net/a/shellsec)

---

轻量 Python 脚本：连洛雪桌面端本地开放 API，切歌、播放暂停、看当前曲、调音量/静音/进度、收藏。电脑可开网页给手机遥控；`lx启动.bat` / `--web` **默认同时**开局域网 MCP（`0.0.0.0:23334`），其它电脑的 Cursor 可直接连。只要手机页时用 `--no-mcp` 或 `LX_MCP=0`。本机 Cursor 仍可用 `--mcp`（stdio）；也可单独跑 `--mcp-http`。播放控制（含 MCP）只用 **Python 3 标准库**；微信扫码二维码需要 `segno`（见 `requirements.txt`，`启动.bat` / `启动.sh` 会尝试安装）。页面、代理和 MCP 都在 `lx_control.py` 里。局域网 MCP **不需要** segno。

<p align="center">
  <img src="docs/screenshots/01-dark-controls.jpg" width="180" alt="深色主题：暂停与音量">
  <img src="docs/screenshots/02-light-lyrics.jpg" width="180" alt="浅色主题：全文歌词">
  <img src="docs/screenshots/03-dark-lyrics.png" width="180" alt="深色主题：全文歌词">
  <img src="docs/screenshots/04-dark-playing.png" width="180" alt="深色主题：播放中">
</p>
<p align="center"><sub>手机网页遥控：深色 / 浅色 / 高对比，支持进度、歌词、音量与切歌。</sub></p>

## 洛雪桌面端下载

本仓库**不再携带**桌面端解压包。请从官方 Release 下载；可用 `gh-release-fetch` 一键拉取官方 release，或直接用 gh-proxy 加速链接。

- 官方发布页：<https://github.com/lyswhut/lx-music-desktop/releases>
- 加速示例（Windows x64 绿色版）：<https://gh-proxy.com/github.com/lyswhut/lx-music-desktop/releases/download/v2.12.5/lx-music-desktop-v2.12.5-win_x64-green.7z>
- 手头已有 **2.12.2** 压缩包且能正常运行的，可继续使用。

## 在线音源

音源在**洛雪桌面端**里加载（设置 → 自定义源 / 在线更新）。本仓库遥控页只控制当前曲，**没有搜歌**。

已打包的在线更新源（已测试，加载在线更新即可）：

<https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/lx-music-source/refs/heads/master/lx-music-source.js>

也可选加载以下在线更新 URL：

| 名称 | 地址 |
| --- | --- |
| Flower（野花） | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/flower/latest.js> |
| SixYin（六音） | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/sixyin/latest.js> |
| Huibq | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/huibq/latest.js> |
| LX | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/lx/latest.js> |
| ikun | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/ikun/latest.js> |
| Grass（野草） | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/grass/latest.js> |
| JuheApi | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/juhe/latest.js> |
| QDY | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/qdy/latest.js> |
| xinghai | <https://zrcdy.dpdns.org/lx/xinghai-music-sourcev2.3.13.js> |

## 使用场景

### 微信扫码，直接控制电脑上的洛雪

电脑开着洛雪在放歌，手机和电脑连**同一 Wi-Fi**。双击 `lx启动.bat`（macOS / Linux 用 `./lx启动.sh`）后，控制台会打印局域网地址，并画出一张**白底黑码**的二维码。用微信 **扫一扫** 扫这个码，不用装 App、不用手输 IP，就能在手机里切歌、暂停、调音量、看歌词。

<p align="center">
  <img src="docs/screenshots/05-desktop-qr.jpg" width="480" alt="控制台二维码与洛雪桌面端">
</p>

- 扫的是 `http://192.168.x.x:23333`，**不要扫** `127.0.0.1`（那是电脑自己访问用的）。
- 控制台字体把码扫花时，打开同目录的 `remote-qr.png` 再扫。
- 手机打不开：同一 Wi-Fi，防火墙放行 **TCP 23333**（默认还会开 MCP **23334**，给其它电脑的 Cursor 用）。

同一台电脑上也可以用命令行 REPL 切歌；Windows 可用 `--keys` 单键控制。详细步骤见下方「手机网页遥控」。

> **本机 `--web` / `lx启动.bat` / `lx启动.sh` 可自动开启开放 API，关闭自动下载更新，并抑制启动时的「发现新版本」弹窗（不只关自动下载）。** 官方洛雪没有命令行开关。脚本在本机自动拉起桌面端（当时没在运行）时，会先把配置里的 `openAPI.enable` 写成 `true`。Windows / macOS / Linux 都支持。已在运行时需彻底退出后再用脚本启动，或手动勾选开放 API。详见下方「洛雪里怎么开 API」。

官方文档：<https://lyswhut.github.io/lx-music-doc/desktop/open-api>（**v2.7.0+**；不保证更早的桌面端。）

## 洛雪里怎么开 API

官方桌面端**没有**命令行参数可启用开放 API。本机用 `--web` / `lx启动.bat` / `lx启动.sh` 时，若开放 API 还没起来、且洛雪当时**没在运行**，脚本会在自动启动前写入配置：

- 把 `setting["openAPI.enable"]` 写成 `true`
- 同时把 `setting["common.tryAutoUpdate"]` 写成 `false`，并把 `data.json` 的 `ignoreVersion` 写成官方当前最新版（抑制启动更新弹窗；更新日志开关不动）
- 配置文件：便携版为 `安装目录/portable/userData/LxDatas/config_v2.json`；否则为 `%APPDATA%\lx-music-desktop\LxDatas\config_v2.json`（macOS：`~/Library/Application Support/lx-music-desktop/LxDatas/config_v2.json`；Linux：`~/.config/lx-music-desktop/LxDatas/config_v2.json`）
- 已有端口会保留；配置里没有端口时默认 `23330`
- **不会**自动勾选「允许来自局域网的访问」（`bindLan`）。本机网页遥控一般不需要；跨设备才要自己勾

若洛雪**已经在运行**，改配置不会立刻生效，需要重启桌面端，或按下面步骤在设置里手动勾选。不想自动启动桌面端时用 `--no-launch`。

想自己勾选时：

1. 打开 **洛雪音乐桌面端**（需 **v2.7.0** 及以上）。
2. **设置 → 开放 API**。
3. 勾选 **启用开放 API 服务**。
4. **服务端口** 保持 `23330`（或改完后，启动脚本时用 `--port` / `LX_API_PORT` 对齐）。
5. 若要从**另一台电脑/本机局域网 IP** 控制，必须勾选 **允许来自局域网的访问**。  
   不勾时服务只绑 `127.0.0.1`，`192.168.x.x` 会连不上。
6. 设置页里的 **服务地址** 会列出本机回环和局域网 IP，用列表里的地址即可。

官方开放 API **没有密码 / token**。  
401 Forbidden 在源码里是「未知路径」的默认回应，不是缺密钥。只有你自己前面加了反代/网关时，才需要 `--token` 或环境变量 `LX_API_TOKEN`。

跨域：服务已返回 `Access-Control-Allow-Origin: *`。浏览器网页可以跨域调；本脚本是本机 Python，不受 CORS 影响。

协议：只有 **HTTP GET**。实时状态用 **SSE**（`/subscribe-player-status`），**没有 WebSocket**。本脚本用短请求控制切歌，不连 SSE。

## 手机网页遥控（推荐）

电脑和手机连**同一 Wi-Fi / 局域网**。对应系统的**洛雪桌面端**需要已安装。本机 `--web` 自动启动时可写入开放 API 开关（见「洛雪里怎么开 API」）；也可以在 **设置 → 开放 API** 里手动勾选。

`--web` / `启动.bat` / `启动.sh` 时：若本机开放 API 还没起来，脚本会尝试启动洛雪桌面端（已在运行则不再开一份），最多等约 40 秒。本机自动启动前会写入开放 API 开关（见「洛雪里怎么开 API」）。**Windows / macOS / Linux 在本机 `--web` 下都支持自动查找桌面端、自动启动、并在未运行时写入开放 API**，路径因系统而异：Windows 为 `lx-music-desktop.exe`（安装目录向上查找、Program Files、注册表）；macOS 为 `/Applications/lx-music-desktop.app`（`open -a`）；Linux 为 PATH、`/opt`、`~/.local`、AppImage 以及已安装的 snap/flatpak。脚本可放在安装目录或其子目录（例如 `D:\Program Files\lx-music-desktop\lxpy`）。找不到时，可设环境变量 `LX_APP`，或 `--lx-exe`，或在 `lx_remote_state.json` 写入 `"lxExe"`。不想自动启动：`--no-launch`。命令行 REPL / `--keys` 不会自动开洛雪。

| 系统 | 怎么启动 |
| --- | --- |
| Windows | 双击 `启动.bat` |
| macOS / Linux | `chmod +x 启动.sh`（只需一次），再 `./启动.sh` |

或任意系统：

```bash
python3 lx_control.py --web
```

默认同时监听网页 `0.0.0.0:23333` 和局域网 MCP `0.0.0.0:23334`。控制台会打印「本机」和「手机」地址，并画出**白底黑码**的局域网二维码（`http://192.168.x.x:23333`，不是 127.0.0.1），接着打印 MCP 局域网 URL（`http://192.168.x.x:23334/sse`）。用**微信扫一扫**扫控制台即可。控制台字体把码扫花时，再手动打开同目录的 `remote-qr.png`（不会自动弹窗）。扫不开：手机和电脑同一 Wi-Fi，防火墙放行 **TCP 23333**（以及 MCP **23334**）。只要手机遥控、不要 MCP：`--no-mcp` 或环境变量 `LX_MCP=0`。

页面只打 23333，由**跑脚本的这台电脑**代理到洛雪 Open API，手机不用直连 23330。

- **洛雪和脚本在同一台电脑**（`--web` / `启动.bat` / `启动.sh` 未指定主机时默认如此）：代理 `127.0.0.1:23330`，不必勾选「允许来自局域网的访问」。本机 API 若只通回环，脚本会自动改走 `127.0.0.1`。
- **洛雪在另一台电脑**：把 `LX_API_HOST` / `--host` 改成洛雪那台的 IP，并勾选 **允许来自局域网的访问**。连的不是本机时，**不会**自动启动桌面端。

```bash
# 本机洛雪
python3 lx_control.py --web --host 127.0.0.1

# 局域网上另一台洛雪
LX_API_HOST=192.168.31.169 python3 lx_control.py --web
```

右上角可点 **深色 / 浅色 / 高对比** 切换风格，选过的会记在手机浏览器里。曲目区显示当前歌词（有翻译/罗马音会多一行），点 **全文歌词** 可展开 LRC，点某一句会跳到对应进度。遥控页只做当前曲控制，没有搜歌、歌单、排行榜入口。

还需要：

1. 该系统已安装 **Python 3**（`python3` 或 `python` / Windows 的 `py -3`）。首次画二维码需要 `pip install -r requirements.txt`（启动脚本会试着装）。
2. 防火墙放行 **TCP 23333**（默认还有 MCP **23334**；Windows 首次可能弹窗；macOS「系统设置 → 网络 / 防火墙」；Linux 视发行版打开对应端口）。洛雪自己的 23330 要能被脚本所在机器访问。
3. 不要用流量/访客 Wi-Fi 隔离网络，否则手机摸不到电脑。微信必须扫局域网地址，不要扫 127.0.0.1。

网页端口可改：`--web-port 23333` 或环境变量 `LX_WEB_PORT`。只要网页、不要 MCP：`python3 lx_control.py --web --no-mcp`（或 `LX_MCP=0`）。

命令行 REPL：`python3 lx_control.py`（不要加 `--web`）。`--keys` 单键热键只在 Windows 可用，其它系统会退回普通 REPL。

## Cursor / Claude MCP

MCP **不替代** `--web` 手机遥控：手机扫码仍用 `python lx_control.py --web` 或 `lx启动.bat`。`--web` / `lx启动.bat` / `lx启动.sh` **默认同时**启动局域网 MCP（`0.0.0.0:23334`），其它电脑的 Cursor 可直接连控制台打印的局域网 URL。只要网页时加 `--no-mcp` 或 `LX_MCP=0`。

- **本机 Cursor**：`--mcp`（stdio，只给启动它的那台电脑用；行为不变）
- **其它电脑的 Cursor**：跟 `--web` 一起默认已开；也可单独 `--mcp-http`（SSE / Streamable HTTP）

未指定主机时默认连本机洛雪 `127.0.0.1:23330`（与 `--web` 相同）。可用 `--host` / `--port` / `--url` / `--token`，或环境变量 `LX_API_HOST`、`LX_API_PORT`、`LX_API_URL`、`LX_API_TOKEN`。单独 `--mcp` / `--mcp-http` 不会自动启动洛雪桌面端；走 `--web` 时仍按网页遥控逻辑自动启动。请先在洛雪里启用开放 API。

### 本机 stdio（`--mcp`）

不额外装包。启动：

```bash
python lx_control.py --mcp
```

在 **这台电脑** 的 Cursor：Settings → MCP，或项目 `.cursor/mcp.json` / 用户 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "lxpy": {
      "command": "python",
      "args": ["lx_control.py", "--mcp"],
      "cwd": "E:/GITHUB/lxpy",
      "env": {
        "LX_API_HOST": "127.0.0.1",
        "LX_API_PORT": "23330"
      }
    }
  }
}
```

把 `cwd` 改成你的仓库路径。Windows 若 `python` 不可用，把 `command` 改成 `py`，`args` 改成 `["-3", "lx_control.py", "--mcp"]`；macOS / Linux 可用 `python3`。前面有反代时再加 `"LX_API_TOKEN"`。

### 局域网远程 MCP（默认随 `--web` 开启）

让**另一台电脑**上的 Cursor（或其它 MCP 客户端）通过网络连到**跑洛雪的这台电脑**，远程切歌/暂停/音量。这是你自己的局域网遥控，不是给公网用的后门。

`lx启动.bat` / `lx启动.sh` / `python lx_control.py --web` **默认**已在同一进程里开局域网 MCP（`0.0.0.0:23334`，不占用网页 23333 和 Open API 23330）。控制台会在网页二维码后面打印 MCP 本机/局域网 URL。只要手机页：`--no-mcp` 或 `LX_MCP=0`。

也可单独启动（不要网页遥控时）：

```bash
python lx_control.py --mcp-http
```

单独启动时控制台同样打印本机和局域网 URL（**不需要** segno / 二维码）。把局域网地址粘到另一台电脑的 Cursor。端口可改：`--mcp-port 23334` 或 `LX_MCP_PORT`。监听地址：`--mcp-bind 0.0.0.0` 或 `LX_MCP_BIND`。

**另一台电脑**与洛雪电脑须在**同一 Wi-Fi / 局域网**。在那台电脑的 Cursor：Settings → MCP，或 `~/.cursor/mcp.json`（把 IP 换成控制台打印的局域网地址，不要用 `127.0.0.1`）：

```json
{
  "mcpServers": {
    "lxpy": {
      "url": "http://192.168.31.100:23334/sse"
    }
  }
}
```

也可用 Streamable HTTP：`"url": "http://192.168.31.100:23334/mcp"`。Windows 防火墙放行 **TCP 23334**（首次可能弹窗；macOS「系统设置 → 网络 / 防火墙」；Linux 视发行版打开对应端口）。访客 Wi-Fi / 客户端隔离会导致连不上。

可选口令 `--mcp-token` 或环境变量 `LX_MCP_TOKEN`。**未设置时与开放 API 一样：只信任同一局域网**，任何能访问该端口的设备都能调播放控制。设了口令后，请求须带 `Authorization: Bearer <口令>`，或 URL `?token=<口令>`：

```bash
python lx_control.py --mcp-http --mcp-token 换成你自己的口令
```

```json
{
  "mcpServers": {
    "lxpy": {
      "url": "http://192.168.31.100:23334/sse",
      "headers": {
        "Authorization": "Bearer 换成你自己的口令"
      }
    }
  }
}
```

或把口令写进 URL：`"url": "http://192.168.31.100:23334/sse?token=换成你自己的口令"`。

工具与现有命令一一对应（官方 Open API **没有**搜歌/歌单/播放模式）：

| 工具 | 作用 |
| --- | --- |
| `status` | 当前曲目与状态 |
| `play` / `pause` / `toggle` | 播放 / 暂停 / 切换 |
| `next` / `prev` | 下一曲 / 上一曲 |
| `volume` | 不传 `value` 只读；`50` 设置；`+10` / `-10` 相对调节 |
| `mute` / `unmute` | 静音 / 取消静音 |
| `seek` | 需要 `offset`（秒或 `1:20`） |
| `lyric` / `lyric-all` | 当前 LRC / 全部歌词 JSON |
| `collect` / `uncollect` | 收藏 / 取消收藏 |

## 命令行怎么用

在本目录：

```bash
python lx_control.py
```

未指定时默认连接 `http://192.168.31.169:23330`（可用 `--host 127.0.0.1` 连本机洛雪）。启动后会先读一次 `/status`，然后进入 REPL：

```
> n          # 下一曲
> p          # 上一曲
> play       # 播放
> pause      # 暂停
> t          # 按当前状态切换播放/暂停
> s          # 当前曲目（含音量）
> vol        # 看当前音量/是否静音
> vol 50     # 音量设为 50（0-100）
> vol +10    # 相对当前音量 +10
> mute       # 静音
> unmute     # 取消静音
> seek 30    # 跳到 30 秒
> seek 1:20  # 跳到 1 分 20 秒
> collect    # 收藏当前曲
> lyric      # 当前 LRC
> lyric-all  # 全部歌词 JSON
> help
> quit
```

单次命令（不进入交互）：

```bash
python lx_control.py next
python lx_control.py status
python lx_control.py volume
python lx_control.py volume 50
python lx_control.py mute
python lx_control.py unmute
python lx_control.py seek 30
```

## 音量怎么用

官方是 `GET /volume?volume=0-100`（文档写 1-100，源码允许 0）。当前音量不在默认 `/status` 里，脚本会带 `filter=...volume,mute,collect`。

```bash
python lx_control.py volume          # 只读，不改音量
python lx_control.py volume 80       # 设为 80
python lx_control.py volume +10      # 在当前基础上 +10
python lx_control.py mute            # GET /mute?mute=true
python lx_control.py unmute          # GET /mute?mute=false
```

REPL 里同样：`vol`、`vol 50`、`mute` / `unmute`。`status` 也会带上「音量 100」等字段。

官方 **没有** 播放模式（循环/随机）、播放列表接口。那些只能在洛雪窗口里操作。

覆盖地址：

```bash
python lx_control.py --host 127.0.0.1 --port 23330 status
python lx_control.py --url http://192.168.31.169:23330 next
```

环境变量（命令行优先）：

| 变量 | 含义 |
| --- | --- |
| `LX_API_HOST` | 洛雪 Open API 主机。命令行默认 `192.168.31.169`；`--web` / `--mcp` / `--mcp-http` / `启动.bat` / `启动.sh` 未指定时默认 `127.0.0.1` |
| `LX_API_PORT` | 端口，默认 `23330` |
| `LX_API_URL` | 完整基址，设置后覆盖 host/port |
| `LX_API_TOKEN` | 可选。官方 API 不需要 |
| `LX_WEB_PORT` | 网页端口，默认 `23333` |
| `LX_WEB_BIND` | 网页监听地址，默认 `0.0.0.0` |
| `LX_MCP` | 设为 `0` / `false` / `off` 时，`--web` 不启动局域网 MCP（与 `--no-mcp` 相同） |
| `LX_MCP_PORT` | 局域网 MCP 端口，默认 `23334` |
| `LX_MCP_BIND` | 局域网 MCP 监听地址，默认 `0.0.0.0` |
| `LX_MCP_TOKEN` | 可选。局域网 MCP 口令；未设则仅信任同一局域网 |
| `LX_APP` / `LX_EXE` | 洛雪桌面端 exe / `.app` 路径，找不到安装目录时用 |
| `LX_APP_WAIT` | 自动启动后等待开放 API 的秒数，默认 40 |

Windows 下可单键切歌（不用回车）：

```bash
python lx_control.py --keys
```

`n` 下一曲，`p` 上一曲，空格播放/暂停，`s` 当前曲，`q` 退出。

## API 路径（本脚本用到的）

官方控制接口全部是 **GET**，不是 `play-next` / `play-prev`。

| 动作 | 路径 | 脚本命令 |
| --- | --- | --- |
| 当前曲目/状态 | `GET /status` | `status` |
| 下一曲 | `GET /skip-next` | `next` |
| 上一曲 | `GET /skip-prev` | `prev` |
| 播放 / 暂停 | `GET /play`、`GET /pause` | `play` / `pause` / `toggle` |
| 当前 LRC | `GET /lyric` | `lyric` |
| 全部歌词 | `GET /lyric-all` | `lyric-all` |
| 音量 | `GET /volume?volume=0-100` | `volume` / `volume 50` |
| 静音 | `GET /mute?mute=true\|false` | `mute` / `unmute` |
| 进度 | `GET /seek?offset=秒` | `seek 30` |
| 收藏/取消 | `GET /collect`、`GET /uncollect` | `collect` / `uncollect` |
| 实时状态（SSE） | `GET /subscribe-player-status` | 不做 |

REPL 里 `next` / `play-next` 都会打到 `/skip-next`。官方没有播放模式、歌单列表接口。

## 常见错误

| 现象 | 原因与处理 |
| --- | --- |
| 另一台电脑 Cursor 连不上 MCP | 没用 `--web`（或加了 `--no-mcp` / `LX_MCP=0`）且没单独开 `--mcp-http`、不是同一 Wi-Fi、防火墙拦了 **TCP 23334**、`url` 写成了 `127.0.0.1`（应填洛雪电脑的局域网 IP）；23334 已被占用时控制台会提示，网页遥控仍可用 |
| MCP 返回 401 | 设了 `--mcp-token` / `LX_MCP_TOKEN` 但没带 `Authorization: Bearer` 或 `?token=` |
| 手机打不开网页 | 电脑没开 `--web`、不是同一 Wi-Fi、防火墙拦了 **23333** |
| 微信扫码进不去 | 扫的应是 `http://电脑局域网IP:23333`；可改扫 `remote-qr.png`；检查防火墙 23333 |
| 网页能开但显示连不上洛雪 | 洛雪没开、端口不对，或脚本连的不是洛雪那台（本机用 `127.0.0.1`，跨设备要勾「允许来自局域网的访问」） |
| 提示未找到洛雪桌面端 | 安装洛雪后重试；或设 `LX_APP` / `--lx-exe` 指向本机可执行文件（Windows：`lx-music-desktop.exe`；macOS：`lx-music-desktop.app`；Linux：`lx-music-desktop` 或 AppImage） |
| 进程已在运行但 API 连不上 | 已在运行时无法热启用 API：请勾选 **设置 → 开放 API → 启用**，或退出洛雪后再用 `--web` / `启动.bat` 让脚本启动前写入配置 |
| 连接被拒绝 / 超时 / 连不上 | 洛雪没开、没勾「允许来自局域网的访问」、IP/端口不对、防火墙拦了 23330 |
| 只能 `127.0.0.1` 通、局域网 IP 不通 | 未勾选 **允许来自局域网的访问**（否则只监听 127.0.0.1） |
| HTTP 401 Forbidden | 路径写错（例如 `/play-next`）。官方无密钥；自建网关才查 token |
| HTTP 400 | `seek` / `volume` / `mute` 参数不合法 |
| 能通但切歌没反应 | API 已开，但播放器里没有下一首/上一首可切 |
| 浏览器跨域失败 | 旧版本在加 CORS 之前；升级到支持跨域的版本，或用本脚本绕过浏览器 |

Windows 若 `python` 不可用，用 `py -3 lx_control.py`。macOS / Linux 一般是 `python3`。
