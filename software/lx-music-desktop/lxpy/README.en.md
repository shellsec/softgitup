# LX Music Open API Controller

**语言 / Language:** [中文](README.md) | English

[aiv123.com](https://aiv123.com/) · AI tools directory, 600+ tools in one place

## 🚀 Recommended: [ofox.ai](https://ofox.io/x/aiv123)

> **In short**: One account for the latest GPT / Claude / Gemini and **100+** top models. First top-up gets an extra **$3** credit.

Text, image, video, and embeddings in one place. Caching supported — repeat calls stay cheaper and faster.

[👉 Sign up](https://ofox.io/x/aiv123) · Global dedicated lines · Enterprise SLA · No conversation retention

| ⚡️ Faster & Leaner | 🧠 Models & Modalities | 🛡️ Privacy |
|:---:|:---:|:---:|
| Global lines, enterprise SLA, plus caching | 100+ models · text / image / video / embeddings | No conversation retention |

## ☕ Buy Me a Coke

Open source takes effort — sponsorship is welcome:  
👉 [爱发电 / Afdian](https://ifdian.net/a/shellsec)

---

A small Python tool that talks to the LX Music desktop Open API: skip tracks, play/pause, show the current song, volume/mute/seek, and collect. The computer can host a web page for phone remote control; `lx启动.bat` / `--web` **also start LAN MCP by default** (`0.0.0.0:23334`) so Cursor on another PC can connect. Use `--no-mcp` or `LX_MCP=0` if you only want the phone page. Local Cursor can still use `--mcp` (stdio); `--mcp-http` still works alone. Playback control (including MCP) uses the **Python 3 standard library**; WeChat QR codes need `segno` (see `requirements.txt`; `lx启动.bat` / `lx启动.sh` will try to install it). The page, proxy, and MCP server all live in `lx_control.py`. LAN MCP does **not** need segno.

<p align="center">
  <img src="docs/screenshots/01-dark-controls.jpg" width="180" alt="Dark theme: paused with volume">
  <img src="docs/screenshots/02-light-lyrics.jpg" width="180" alt="Light theme: full lyrics">
  <img src="docs/screenshots/03-dark-lyrics.png" width="180" alt="Dark theme: full lyrics">
  <img src="docs/screenshots/04-dark-playing.png" width="180" alt="Dark theme: playing">
</p>
<p align="center"><sub>Phone web remote: dark / light / high-contrast, with progress, lyrics, volume, and skip.</sub></p>

## Download LX Music Desktop

This repo **no longer ships** a desktop zip/7z. Get the official Release; you can one-click fetch it with `gh-release-fetch`, or use a gh-proxy accelerated URL.

- Official releases: <https://github.com/lyswhut/lx-music-desktop/releases>
- Accelerated example (Windows x64 green 7z): <https://gh-proxy.com/github.com/lyswhut/lx-music-desktop/releases/download/v2.12.5/lx-music-desktop-v2.12.5-win_x64-green.7z>
- If you already have a **2.12.2** archive that runs fine, keep using it.

## Online music sources

Load sources in **LX Music Desktop** (Settings → custom source / online update). This repo’s remote page only controls the current track — **it has no search**.

Bundled online-update source (tested; load it via online update):

<https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/lx-music-source/refs/heads/master/lx-music-source.js>

Optional online-update URLs:

| Name | URL |
| --- | --- |
| Flower | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/flower/latest.js> |
| SixYin | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/sixyin/latest.js> |
| Huibq | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/huibq/latest.js> |
| LX | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/lx/latest.js> |
| ikun | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/ikun/latest.js> |
| Grass | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/grass/latest.js> |
| JuheApi | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/juhe/latest.js> |
| QDY | <https://gh-proxy.com/raw.githubusercontent.com/pdone/lx-music-source/main/qdy/latest.js> |
| xinghai | <https://zrcdy.dpdns.org/lx/xinghai-music-sourcev2.3.13.js> |

## Use cases

### Scan the QR code in WeChat to control LX Music on the PC

LX Music is playing on the computer. Phone and PC are on the **same Wi-Fi**. Double-click `lx启动.bat` (or `./lx启动.sh` on macOS / Linux). The console prints the LAN URL and draws a **black-on-white** QR code. Open WeChat **Scan**, point at that code — no extra app, no typing an IP — and skip, pause, change volume, or read lyrics from the phone.

<p align="center">
  <img src="docs/screenshots/05-desktop-qr.jpg" width="480" alt="Console QR code and LX Music desktop">
</p>

- Scan `http://192.168.x.x:23333`. **Do not** scan `127.0.0.1` (that URL is only for the PC itself).
- If the console font smears the code, open `remote-qr.png` in the same folder and scan that.
- If the phone cannot open it: same Wi-Fi, and allow **TCP 23333** through the firewall (default start also opens MCP **23334** for Cursor on another PC).

You can also use the CLI REPL on the same computer; Windows supports `--keys` for single-key control. Full steps are in **Phone web remote** below.

> **Local `--web` / `lx启动.bat` / `lx启动.sh` can turn Open API on automatically, disable auto-download, and suppress the startup “new version” popup (not only auto-download).** Official LX Music has no CLI flag for this. When the script auto-launches the desktop app locally (and it is not already running), it writes `openAPI.enable` to `true` first. Windows, macOS, and Linux all support this. If LX Music is already running, fully quit it and start via the script, or enable Open API by hand. See **Enable the API in LX Music** below.

Official docs: <https://lyswhut.github.io/lx-music-doc/desktop/open-api> (**v2.7.0+**; older desktop builds are not guaranteed.)

## Enable the API in LX Music

Official LX Music has **no** CLI flag to enable Open API. With local `--web` / `lx启动.bat` / `lx启动.sh`, if the Open API is not up yet **and** LX Music is **not** already running, the script writes the desktop config before auto-launch:

- Sets `setting["openAPI.enable"]` to `true`
- Also sets `setting["common.tryAutoUpdate"]` to `false`, and writes official latest into `data.json` `ignoreVersion` (suppresses the startup update popup; changelog toggle is left alone)
- Config file: portable install uses `install-dir/portable/userData/LxDatas/config_v2.json`; otherwise `%APPDATA%\lx-music-desktop\LxDatas\config_v2.json` (macOS: `~/Library/Application Support/lx-music-desktop/LxDatas/config_v2.json`; Linux: `~/.config/lx-music-desktop/LxDatas/config_v2.json`)
- Keeps an existing port; defaults to `23330` if missing
- Does **not** auto-enable **Allow access from LAN** (`bindLan`). Local web remote usually does not need it; tick it yourself for another machine

If LX Music is **already running**, that config write will not take effect until you restart the desktop app, or enable it by hand in settings as below. To skip auto-launch: `--no-launch`.

To enable it yourself:

1. Open **LX Music Desktop** (**v2.7.0** or later).
2. **Settings → Open API**.
3. Enable **Open API service**.
4. Keep the **service port** at `23330` (or match it with `--port` / `LX_API_PORT` when starting this script).
5. To control from **another machine / a LAN IP**, enable **Allow access from LAN**.  
   If this is off, the service binds `127.0.0.1` only, and `192.168.x.x` will fail.
6. The settings page lists loopback and LAN addresses under **Service address** — use one of those.

The official Open API has **no password / token**.  
HTTP 401 Forbidden in the source is the default response for an unknown path, not a missing key. `--token` or `LX_API_TOKEN` is only needed if you put your own reverse proxy/gateway in front.

CORS: the service already returns `Access-Control-Allow-Origin: *`. Browser pages can call it cross-origin; this script is local Python, so CORS does not apply.

Protocol: **HTTP GET only**. Live status uses **SSE** (`/subscribe-player-status`); there is **no WebSocket**. This script uses short requests for skip/control and does not connect to SSE.

## Phone web remote (recommended)

Phone and computer must be on the **same Wi-Fi / LAN**. The matching **LX Music desktop** app must be installed. A local `--web` auto-launch can write the Open API switch (see **Enable the API in LX Music**); you can also tick it yourself under **Settings → Open API**.

With `--web` / `lx启动.bat` / `lx启动.sh`, if the Open API is not up yet, the script tries to launch LX Music desktop (it will not start a second copy if one is already running) and waits up to about 40 seconds. Before a local auto-launch it writes the Open API switch (see **Enable the API in LX Music**). **Windows, macOS, and Linux all support auto-find, auto-launch, and auto-enable Open API on local `--web`**, with platform-specific paths: Windows `lx-music-desktop.exe` (parent folders, Program Files, registry); macOS `/Applications/lx-music-desktop.app` (`open -a`); Linux PATH, `/opt`, `~/.local`, AppImage, and installed snap/flatpak. You can keep the script in the install folder or a subfolder (for example `D:\Program Files\lx-music-desktop\lxpy`). If the install path cannot be found, set `LX_APP`, `--lx-exe`, or `"lxExe"` in `lx_remote_state.json`. To skip auto-launch: `--no-launch`. The CLI REPL / `--keys` modes do not auto-start LX Music.

| OS | How to start |
| --- | --- |
| Windows | Double-click `lx启动.bat` |
| macOS / Linux | `chmod +x lx启动.sh` (once), then `./lx启动.sh` |

Or on any OS:

```bash
python3 lx_control.py --web
```

By default it listens on web `0.0.0.0:23333` and LAN MCP `0.0.0.0:23334`. The console prints **local** and **phone** URLs and draws a **black-on-white** LAN QR code (`http://192.168.x.x:23333`, not 127.0.0.1), then prints the MCP LAN URL (`http://192.168.x.x:23334/sse`). Scan it with **WeChat Scan**. If the console font smears the code, open `remote-qr.png` in the same folder (it does not pop up automatically). If scanning fails: same Wi-Fi, and allow **TCP 23333** (and MCP **23334**) through the firewall. Phone page only, no MCP: `--no-mcp` or `LX_MCP=0`.

The page only talks to 23333. The computer running this script proxies to the LX Open API, so the phone does not need to reach 23330.

- **LX Music and this script on the same computer** (`--web` / `lx启动.bat` / `lx启动.sh` when no host is set): proxy `127.0.0.1:23330`. You do not need “Allow access from LAN”. If the local API only works on loopback, the script switches to `127.0.0.1` automatically.
- **LX Music on another computer**: set `LX_API_HOST` / `--host` to that machine’s IP and enable **Allow access from LAN**. Auto-launch does **not** run when the target is not local.

```bash
# LX Music on this machine
python3 lx_control.py --web --host 127.0.0.1

# LX Music on another LAN machine
LX_API_HOST=192.168.31.169 python3 lx_control.py --web
```

The top-right **Dark / Light / High contrast** switch is remembered in the phone browser. The track area shows the current lyric line (plus a translation/romaji line when present). **Full lyrics** expands the LRC; tapping a line seeks to that time. The remote page only controls the current track — no search, playlists, or charts.

Also required:

1. **Python 3** (`python3` or `python` / Windows `py -3`). The first QR render needs `pip install -r requirements.txt` (the start scripts try this).
2. Firewall allow **TCP 23333** (and MCP **23334** by default; Windows may prompt; macOS “System Settings → Network / Firewall”; Linux depends on the distro). LX Music’s own 23330 must be reachable from the machine running this script.
3. Avoid cellular / guest Wi-Fi client isolation, or the phone cannot reach the computer. WeChat must scan the LAN URL, not 127.0.0.1.

Web port: `--web-port 23333` or `LX_WEB_PORT`. Web only, no MCP: `python3 lx_control.py --web --no-mcp` (or `LX_MCP=0`).

CLI REPL: `python3 lx_control.py` (do not add `--web`). `--keys` single-key hotkeys are Windows-only; other OS fall back to a normal REPL.

## Cursor / Claude MCP

MCP does **not** replace the `--web` phone remote: phones still use `python lx_control.py --web` or `lx启动.bat`. `--web` / `lx启动.bat` / `lx启动.sh` **start LAN MCP by default** (`0.0.0.0:23334`); Cursor on another PC can paste the printed LAN URL. Web only: `--no-mcp` or `LX_MCP=0`.

- **Local Cursor**: `--mcp` (stdio; only the machine that launches it; unchanged)
- **Cursor on another PC**: already on with `--web`; or run `--mcp-http` alone (SSE / Streamable HTTP over the LAN)

When no host is set it defaults to local LX Music at `127.0.0.1:23330` (same as `--web`). Override with `--host` / `--port` / `--url` / `--token`, or `LX_API_HOST`, `LX_API_PORT`, `LX_API_URL`, `LX_API_TOKEN`. Standalone `--mcp` / `--mcp-http` do not auto-launch LX Music; `--web` still follows the phone-remote auto-launch rules. Enable Open API in the desktop app first.

### Local stdio (`--mcp`)

No extra packages. Start:

```bash
python lx_control.py --mcp
```

On **this** PC in Cursor: Settings → MCP, or project `.cursor/mcp.json` / user `~/.cursor/mcp.json`:

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

Change `cwd` to your clone. On Windows, if `python` is missing, set `command` to `py` and `args` to `["-3", "lx_control.py", "--mcp"]`. On macOS / Linux use `python3`. Add `"LX_API_TOKEN"` only if you have a reverse proxy in front.

### LAN remote MCP (on by default with `--web`)

Let Cursor (or another MCP client) on **another machine** connect over the network to **the PC running LX Music** and control playback. This is your own LAN remote, not a public backdoor.

`lx启动.bat` / `lx启动.sh` / `python lx_control.py --web` **already** start LAN MCP in the same process (`0.0.0.0:23334`; does not use web 23333 or Open API 23330). The console prints MCP local/LAN URLs after the web QR. Phone page only: `--no-mcp` or `LX_MCP=0`.

Or start MCP alone (no web remote):

```bash
python lx_control.py --mcp-http
```

Standalone mode also prints local and LAN URLs (**no** segno / QR code). Paste the LAN URL into Cursor on the other PC. Port: `--mcp-port 23334` or `LX_MCP_PORT`. Bind: `--mcp-bind 0.0.0.0` or `LX_MCP_BIND`.

The **other PC** must be on the **same Wi-Fi / LAN**. In that PC’s Cursor: Settings → MCP, or `~/.cursor/mcp.json` (use the printed LAN address, not `127.0.0.1`):

```json
{
  "mcpServers": {
    "lxpy": {
      "url": "http://192.168.31.100:23334/sse"
    }
  }
}
```

Streamable HTTP also works: `"url": "http://192.168.31.100:23334/mcp"`. Allow **TCP 23334** through the firewall (Windows may prompt; macOS “System Settings → Network / Firewall”; Linux depends on the distro). Guest Wi-Fi / client isolation will block the connection.

Optional token: `--mcp-token` or `LX_MCP_TOKEN`. **If unset, same as the Open API: LAN-trust only** — any device that can reach the port can control playback. When set, requests need `Authorization: Bearer <token>` or `?token=<token>`:

```bash
python lx_control.py --mcp-http --mcp-token your-own-secret
```

```json
{
  "mcpServers": {
    "lxpy": {
      "url": "http://192.168.31.100:23334/sse",
      "headers": {
        "Authorization": "Bearer your-own-secret"
      }
    }
  }
}
```

Or put it in the URL: `"url": "http://192.168.31.100:23334/sse?token=your-own-secret"`.

Tools map 1:1 to existing commands (the official Open API has **no** search / playlist / play-mode endpoints):

| Tool | Action |
| --- | --- |
| `status` | Current track and player state |
| `play` / `pause` / `toggle` | Play / pause / toggle |
| `next` / `prev` | Next / previous track |
| `volume` | Omit `value` to read; `50` to set; `+10` / `-10` relative |
| `mute` / `unmute` | Mute / unmute |
| `seek` | Requires `offset` (seconds or `1:20`) |
| `lyric` / `lyric-all` | Current LRC / full lyrics JSON |
| `collect` / `uncollect` | Collect / uncollect |

## Command-line usage

In this directory:

```bash
python lx_control.py
```

If unspecified, it defaults to `http://192.168.31.169:23330` (use `--host 127.0.0.1` for local LX Music). On start it reads `/status` once, then enters a REPL:

```
> n          # next track
> p          # previous track
> play       # play
> pause      # pause
> t          # toggle play/pause from current state
> s          # current track (includes volume)
> vol        # current volume / mute
> vol 50     # set volume to 50 (0-100)
> vol +10    # relative +10
> mute       # mute
> unmute     # unmute
> seek 30    # jump to 30 seconds
> seek 1:20  # jump to 1 minute 20 seconds
> collect    # collect current track
> lyric      # current LRC
> lyric-all  # full lyrics JSON
> help
> quit
```

One-shot commands (no REPL):

```bash
python lx_control.py next
python lx_control.py status
python lx_control.py volume
python lx_control.py volume 50
python lx_control.py mute
python lx_control.py unmute
python lx_control.py seek 30
```

## Volume

Official API: `GET /volume?volume=0-100` (docs say 1-100; the source allows 0). Current volume is not in the default `/status`; the script requests `filter=...volume,mute,collect`.

```bash
python lx_control.py volume          # read only
python lx_control.py volume 80       # set to 80
python lx_control.py volume +10      # +10 from current
python lx_control.py mute            # GET /mute?mute=true
python lx_control.py unmute          # GET /mute?mute=false
```

Same in the REPL: `vol`, `vol 50`, `mute` / `unmute`. `status` also includes fields like “volume 100”.

The official API has **no** play-mode (loop/shuffle) or playlist endpoints. Those stay in the LX Music window.

Override the address:

```bash
python lx_control.py --host 127.0.0.1 --port 23330 status
python lx_control.py --url http://192.168.31.169:23330 next
```

Environment variables (CLI flags win):

| Variable | Meaning |
| --- | --- |
| `LX_API_HOST` | Open API host. CLI default `192.168.31.169`; `--web` / `--mcp` / `--mcp-http` / `lx启动.bat` / `lx启动.sh` default `127.0.0.1` when unset |
| `LX_API_PORT` | Port, default `23330` |
| `LX_API_URL` | Full base URL; overrides host/port when set |
| `LX_API_TOKEN` | Optional. Official API does not need it |
| `LX_WEB_PORT` | Web port, default `23333` |
| `LX_WEB_BIND` | Web bind address, default `0.0.0.0` |
| `LX_MCP` | Set to `0` / `false` / `off` to skip LAN MCP with `--web` (same as `--no-mcp`) |
| `LX_MCP_PORT` | LAN MCP port, default `23334` |
| `LX_MCP_BIND` | LAN MCP bind address, default `0.0.0.0` |
| `LX_MCP_TOKEN` | Optional. LAN MCP token; if unset, LAN-trust only |
| `LX_APP` / `LX_EXE` | Path to the desktop exe / `.app` when install dir cannot be found |
| `LX_APP_WAIT` | Seconds to wait for Open API after auto-launch, default 40 |

Windows single-key skip (no Enter):

```bash
python lx_control.py --keys
```

`n` next, `p` previous, space play/pause, `s` current track, `q` quit.

## API paths used by this script

Official control endpoints are all **GET**, not `play-next` / `play-prev`.

| Action | Path | Script command |
| --- | --- | --- |
| Current track/status | `GET /status` | `status` |
| Next | `GET /skip-next` | `next` |
| Previous | `GET /skip-prev` | `prev` |
| Play / pause | `GET /play`, `GET /pause` | `play` / `pause` / `toggle` |
| Current LRC | `GET /lyric` | `lyric` |
| All lyrics | `GET /lyric-all` | `lyric-all` |
| Volume | `GET /volume?volume=0-100` | `volume` / `volume 50` |
| Mute | `GET /mute?mute=true\|false` | `mute` / `unmute` |
| Seek | `GET /seek?offset=seconds` | `seek 30` |
| Collect / uncollect | `GET /collect`, `GET /uncollect` | `collect` / `uncollect` |
| Live status (SSE) | `GET /subscribe-player-status` | not used |

In the REPL, `next` / `play-next` both hit `/skip-next`. There are no official play-mode or playlist-list endpoints.

## Common errors

| Symptom | Cause / fix |
| --- | --- |
| Other PC Cursor cannot reach MCP | `--web` was not used (or `--no-mcp` / `LX_MCP=0`) and `--mcp-http` is not running, not the same Wi-Fi, firewall blocks **TCP 23334**, or `url` uses `127.0.0.1` (use the LX Music PC’s LAN IP); if 23334 is already in use the console says so and the web remote still works |
| MCP returns 401 | `--mcp-token` / `LX_MCP_TOKEN` is set but the request has no `Authorization: Bearer` or `?token=` |
| Phone cannot open the page | Computer is not running `--web`, not the same Wi-Fi, or firewall blocks **23333** |
| WeChat scan fails | Scan `http://PC-LAN-IP:23333`; try `remote-qr.png`; check firewall 23333 |
| Page opens but cannot reach LX Music | LX Music is off, wrong port, or the script is not pointing at that machine (use `127.0.0.1` locally; enable “Allow access from LAN” across devices) |
| Desktop app not found | Install LX Music and retry, or set `LX_APP` / `--lx-exe` to the local app (Windows: `lx-music-desktop.exe`; macOS: `lx-music-desktop.app`; Linux: `lx-music-desktop` or AppImage) |
| Process running but API unreachable | Cannot hot-enable while running: tick **Settings → Open API → enable**, or quit LX Music and let `--web` / `lx启动.bat` write the config before launch |
| Connection refused / timeout | LX Music off, LAN access not allowed, wrong IP/port, or firewall blocks 23330 |
| Only `127.0.0.1` works, LAN IP fails | “Allow access from LAN” is off (otherwise it listens on 127.0.0.1 only) |
| HTTP 401 Forbidden | Wrong path (e.g. `/play-next`). Official API has no key; only a custom gateway checks a token |
| HTTP 400 | Invalid `seek` / `volume` / `mute` parameter |
| Connected but skip does nothing | API is up, but there is no next/previous track in the player |
| Browser CORS failure | Older builds before CORS; upgrade, or use this script to bypass the browser |

If `python` is missing on Windows, use `py -3 lx_control.py`. macOS / Linux usually use `python3`.
