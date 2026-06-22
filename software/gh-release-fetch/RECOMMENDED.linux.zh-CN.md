# 推荐开源软件（Linux · 全分类导读）

> 由 `python tools/generate_recommended_md.py` 根据 [`apps/linux/`](apps/linux/) 自动生成，生成日期：**2026-06-22**。条目 **405** 个（linux 平台）。
> 其它平台导读：[Windows](RECOMMENDED.zh-CN.md) · [macOS](RECOMMENDED.darwin.zh-CN.md)。
> 技术索引与分片统计见 [`CATALOG.md`](CATALOG.md)。启用/更新：lookup → `run_saved_apps`（Windows 可用 `run_saved_apps.bat`）。

---

## AI（39）

### aichat · `aichat`

（见仓库 Release 说明）

- 仓库：`sigoden/aichat` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux aichat`

### aider（Linux x86_64） · `aider`

aider（Linux x86_64）

- 仓库：`Aider-AI/aider` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux aider`

### anything llm · `anything_llm`

AnythingLLM Linux AppImage（官方 CDN latest；版本 tag 来自 GitHub API）

- 仓库：`Mintplex-Labs/anything-llm` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux anything_llm`

### botgem · `botgem`

BotGem：gaodeng/botgem-docs Release 当前仅有 Windows 安装包；Linux 请从官网获取。本条占位勿启用。

- 仓库：`gaodeng/botgem-docs` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux botgem`

### cc switch · `cc_switch`

CC Switch Linux x86_64（官方 AppImage；deb/rpm 见 Release 同版本）

- 仓库：`farion1231/cc-switch` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cc_switch`

### CC Switch Linux arm64（官方 AppImage） · `cc_switch_linux_arm64`

CC Switch Linux arm64（官方 AppImage）

- 仓库：`farion1231/cc-switch` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cc_switch_linux_arm64`

### chatbox · `chatbox`

Chatbox：主仓库 Release 多为源码；桌面版见 https://chatboxai.app 。

- 仓库：`chatboxai/chatbox` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux chatbox`

### Cherry Studio Linux（x86_64 AppImage · `cherry_studio`

Cherry Studio Linux（x86_64 AppImage，GitHub Release API）

- 仓库：`CherryHQ/cherry-studio` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cherry_studio`

### Claude Code（Linux x86_64 glibc · `claude_code`

Claude Code（Linux x86_64 glibc，claude-linux-x64.tar.gz；musl 见 claude-linux-x64-musl）

- 仓库：`anthropics/claude-code` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux claude_code`

### Claude Code（Linux arm64 glibc · `claude_code_linux_arm64`

Claude Code（Linux arm64 glibc，claude-linux-arm64.tar.gz）

- 仓库：`anthropics/claude-code` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux claude_code_linux_arm64`

### Cline（VS Code 扩展 · `cline`

Cline（VS Code 扩展，Release .vsix）

- 仓库：`cline/cline` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cline`

### cockpit tools · `cockpit_tools`

Cockpit Tools（通用 AI IDE 账号管理；Linux amd64 AppImage）

- 仓库：`jlcodes99/cockpit-tools` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cockpit_tools`

### OpenAI Codex CLI（Linux x86_64 gnu · `codex_cli`

OpenAI Codex CLI（Linux x86_64 gnu，codex-x86_64-unknown-linux-gnu.tar.gz）

- 仓库：`openai/codex` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux codex_cli`

### OpenAI Codex CLI（Linux aarch64 gnu · `codex_cli_linux_arm64`

OpenAI Codex CLI（Linux aarch64 gnu，codex-aarch64-unknown-linux-gnu.tar.gz）

- 仓库：`openai/codex` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux codex_cli_linux_arm64`

### Continue（Linux x64 .vsix · `continue`

Continue（Linux x64 .vsix，若 Release 提供）

- 仓库：`continuedev/continue` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux continue`

### Crush（Charmbracelet 终端 AI 编程助手） · `crush`

Crush（Charmbracelet 终端 AI 编程助手）

- 仓库：`charmbracelet/crush` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux crush`

### DeepSeek-TUI dispatcher（deepseek 命令；Linux x64 · `deepseek_cli`

DeepSeek-TUI dispatcher（deepseek 命令；Linux x64，裸 binary deepseek-linux-x64；需配套 deepseek_tui，并 chmod +x 后放入 PATH）

- 仓库：`Hmbown/DeepSeek-TUI` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux deepseek_cli`

### deepseek tui · `deepseek_tui`

DeepSeek-TUI companion runtime（deepseek-tui 命令；Linux x64，裸 binary deepseek-tui-linux-x64；需与 deepseek_cli 同时存在）

- 仓库：`Hmbown/DeepSeek-TUI` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux deepseek_tui`

### Gemini CLI（Release 多为 gemini-cli-bundle.zip 通用包） · `gemini_cli`

Gemini CLI（Release 多为 gemini-cli-bundle.zip 通用包）

- 仓库：`google-gemini/gemini-cli` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux gemini_cli`

### GitHub Copilot：IDE 插件或 gh copilot · `github_copilot_cli`

GitHub Copilot：IDE 插件或 gh copilot，无单一 Linux 安装包。

- 仓库：`microsoft/vscode` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux github_copilot_cli`

### goose ai · `goose_ai`

（见仓库 Release 说明）

- 仓库：`block/goose` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux goose_ai`

### GPT4All（Linux x64 安装器 .run） · `gpt4all`

GPT4All（Linux x64 安装器 .run）

- 仓库：`nomic-ai/gpt4all` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux gpt4all`

### 沉浸式翻译（Chrome 扩展 zip） · `immersive_translate`

沉浸式翻译（Chrome 扩展 zip）

- 仓库：`immersive-translate/immersive-translate` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux immersive_translate`

### Jan（离线优先的本地 AI 聊天客户端） · `jan`

Jan（离线优先的本地 AI 聊天客户端）

- 仓库：`janhq/jan` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux jan`

### Kilo Code（开源 AI 编程 VS Code 扩展） · `kilocode`

Kilo Code（开源 AI 编程 VS Code 扩展）

- 仓库：`Kilo-Org/kilocode` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux kilocode`

### Kiro CLI Linux（manifest） · `kiro`

Kiro CLI Linux（manifest）

- 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kiro`

### LangChain：PyPI/npm 框架 · `langchain_note`

LangChain：PyPI/npm 框架，不适合 Release 二进制拉取。

- 仓库：`langchain-ai/langchain` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux langchain_note`

### LlamaIndex：pip 框架 · `llamaindex_note`

LlamaIndex：pip 框架，无独立安装包 Release。

- 仓库：`run-llama/llama_index` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux llamaindex_note`

### Lobe Chat Hub（Linux AppImage） · `lobe_chat`

Lobe Chat Hub（Linux AppImage）

- 仓库：`lobehub/lobe-chat` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux lobe_chat`

### NextChat：Release 多为源码；部署见项目说明 · `nextchat`

NextChat：Release 多为源码；部署见项目说明。

- 仓库：`ChatGPTNextWeb/NextChat` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nextchat`

### ollama · `ollama`

（见仓库 Release 说明）

- 仓库：`ollama/ollama` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ollama`

### Open Claude Cowork：仓库无 Release 二进制 · `open_claude_cowork`

Open Claude Cowork：仓库无 Release 二进制。

- 仓库：`ComposioHQ/open-claude-cowork` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux open_claude_cowork`

### open webui desktop · `open_webui_desktop`

Open WebUI Desktop（Linux AppImage；Release 以 yml 为主，试跑前核对资产）

- 仓库：`open-webui/desktop` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux open_webui_desktop`

### OpenCat：以 App Store 等为主；repo_path 仅满足配置校验 · `opencat`

OpenCat：以 App Store 等为主；repo_path 仅满足配置校验，勿启用。

- 仓库：`octocat/Hello-World` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux opencat`

### OpenClaw（Linux 用 Release 中 OpenClaw-*.zip） · `openclaw`

OpenClaw（Linux 用 Release 中 OpenClaw-*.zip）

- 仓库：`openclaw/openclaw` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux openclaw`

### opencode · `opencode`

（见仓库 Release 说明）

- 仓库：`sst/opencode` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux opencode`

### openhands · `openhands`

（见仓库 Release 说明）

- 仓库：`All-Hands-AI/OpenHands` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux openhands`

### roo code · `roo_code`

（见仓库 Release 说明）

- 仓库：`RooCodeInc/Roo-Code` · 分片：`apps/linux/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux roo_code`

### Tabby（自托管 AI 代码补全服务 / 本地推理包） · `tabbyml`

Tabby（自托管 AI 代码补全服务 / 本地推理包）

- 仓库：`TabbyML/tabby` · 分片：`apps/linux/01-AI.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux tabbyml`

---

## 下载（16）

### aria2 · `aria2`

aria2：自 release-1.36 起 GitHub Release 仅提供源码包与 Windows/Android 预编译；Linux 请用发行版包或自编译。本条仅作仓库定位。

- 仓库：`aria2/aria2` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux aria2`

### 开源免费BT/批量下载工具 ArrowDL · `downzemall`

开源免费BT/批量下载工具 ArrowDL 4.2.1 x64 中文多语免费版

- 仓库：`setvisible/DownZemAll` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux downzemall`

### 开源免费文件蜈蚣下载器 File Centipede · `file_centipede`

开源免费文件蜈蚣下载器 File Centipede 2.82 x64 中文多语免费版

- 仓库：`filecxx/FileCentipede` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux file_centipede`

### Gopeed（HTTP/BT 等 · `gopeed`

Gopeed（HTTP/BT 等，现代下载器）

- 仓库：`GopeedLab/gopeed` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux gopeed`

### 开源免费视频下载工具 Hitomi Downloader · `hitomi_downloader`

开源免费视频下载工具 Hitomi Downloader 4.2 中文多语免费版

- 仓库：`KurtBestor/Hitomi-Downloader` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux hitomi_downloader`

### 开源免费 BT 下载工具  LIII BitTorrent Client · `liii_bittorrent_client`

开源免费 BT 下载工具  LIII BitTorrent Client 0.1.1.19 中文多语免费版

- 仓库：`aliakseis/LIII` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux liii_bittorrent_client`

### lux（原 annie · `lux`

lux（原 annie，命令行抓取流媒体/站点视频；Linux x86_64）

- 仓库：`iawia002/lux` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux lux`

### lux（Linux arm64 tarball · `lux_linux_arm64`

lux（Linux arm64 tarball，树莓派/ARM 服务器等）

- 仓库：`iawia002/lux` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux lux_linux_arm64`

### 开源免费 m3u8 下载工具 m3u8 downloader · `m3u8_downloader`

开源免费 m3u8 下载工具 m3u8 downloader 3.0.1 中文免费版

- 仓库：`nilaoda/N_m3u8DL-CLI` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux m3u8_downloader`

### Motrix（全能下载工具：HTTP/FTP/BT/磁力链） · `motrix`

Motrix（全能下载工具：HTTP/FTP/BT/磁力链）

- 仓库：`agalwood/Motrix` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux motrix`

### 开源免费下载工具 Persepolis Download Manager · `persepolis_download_manager`

开源免费下载工具 Persepolis Download Manager 3.2.0 中文免费版

- 仓库：`persepolisdm/persepolis` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux persepolis_download_manager`

### qBittorrent（BT/磁力） · `qbittorrent`

qBittorrent（BT/磁力）

- 仓库：`qbittorrent/qBittorrent` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux qbittorrent`

### qBittorrent 增强版 qBittorrent Enhanced Edition · `qbittorrent_enhanced_edition`

qBittorrent 增强版 qBittorrent Enhanced Edition 5.2.1.10 中文版更新发布

- 仓库：`c0re100/qBittorrent-Enhanced-Edition` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qbittorrent_enhanced_edition`

### Transmission（BT 客户端） · `transmission`

Transmission（BT 客户端）

- 仓库：`transmission/transmission` · 分片：`apps/linux/02-下载.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux transmission`

### 开源免费 Youtube 视频下载工具 YDL-UI · `ydl_ui`

开源免费 Youtube 视频下载工具 YDL-UI 2.9.1 中文多语免费版

- 仓库：`Maxstupo/ydl-ui` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ydl_ui`

### 开源免费视频下载工具 Open Video Downloader · `youtube_downloader_gui`

开源免费视频下载工具 Open Video Downloader 2.4.0 中文免费版

- 仓库：`jely2002/youtube-dl-gui` · 分片：`apps/linux/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux youtube_downloader_gui`

---

## 云原生（10）

### caddy · `caddy`

（见仓库 Release 说明）

- 仓库：`caddyserver/caddy` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux caddy`

### Consul 服务发现 · `consul`

Consul 服务发现

- 仓库：`hashicorp/consul` · 分片：`apps/linux/24-云原生.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux consul`

### kompose · `kompose`

（见仓库 Release 说明）

- 仓库：`kubernetes/kompose` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kompose`

### kubectl · `kubectl`

（见仓库 Release 说明）

- 仓库：`kubernetes/kubernetes` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kubectl`

### lazydocker · `lazydocker`

（见仓库 Release 说明）

- 仓库：`jesseduffield/lazydocker` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lazydocker`

### lens · `lens`

（见仓库 Release 说明）

- 仓库：`lensapp/lens` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lens`

### podman desktop · `podman_desktop`

（见仓库 Release 说明）

- 仓库：`containers/podman-desktop` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux podman_desktop`

### rancher desktop · `rancher_desktop`

（见仓库 Release 说明）

- 仓库：`rancher-sandbox/rancher-desktop` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux rancher_desktop`

### skaffold · `skaffold`

（见仓库 Release 说明）

- 仓库：`GoogleContainerTools/skaffold` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux skaffold`

### tilt · `tilt`

（见仓库 Release 说明）

- 仓库：`tilt-dev/tilt` · 分片：`apps/linux/24-云原生.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tilt`

---

## 代理与隧道（8）

### Clash Verge Rev（Linux amd64 deb） · `clash_verge_rev_linux_amd64`

Clash Verge Rev（Linux amd64 deb）

- 仓库：`clash-verge-rev/clash-verge-rev` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux clash_verge_rev_linux_amd64`

### FlClash（Linux amd64 deb） · `flclash_linux_amd64`

FlClash（Linux amd64 deb）

- 仓库：`chen08209/FlClash` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux flclash_linux_amd64`

### Frpc Desktop（frp 桌面 GUI · `frpc_desktop`

Frpc Desktop（frp 桌面 GUI，Linux amd64 deb）

- 仓库：`luckjiawei/frpc-desktop` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux frpc_desktop`

### Hiddify Next（Linux x64 AppImage） · `hiddify_next`

Hiddify Next（Linux x64 AppImage）

- 仓库：`hiddify/hiddify-next` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux hiddify_next`

### mihomo Clash Meta 内核（Linux amd64 gz） · `mihomo_linux_amd64`

mihomo Clash Meta 内核（Linux amd64 gz）

- 仓库：`SagerNet/sing-box` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux mihomo_linux_amd64`

### sing-box 代理内核 · `sing_box_linux_amd64`

sing-box 代理内核

- 仓库：`SagerNet/sing-box` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux sing_box_linux_amd64`

### v2rayN（Linux x86_64 · `v2rayn_linux_amd64`

v2rayN（Linux x86_64，官方 zip，仅下载）

- 仓库：`2dust/v2rayN` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux v2rayn_linux_amd64`

### v2rayN（Linux arm64 · `v2rayn_linux_arm64`

v2rayN（Linux arm64，官方 zip，仅下载）

- 仓库：`2dust/v2rayN` · 分片：`apps/linux/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux v2rayn_linux_arm64`

---

## 写作（5）

### 开源免费多平台 Markdown 写作工具 Boostnote · `boostnote`

开源免费多平台 Markdown 写作工具 Boostnote 0.16.0 x64 中文多语免费版

- 仓库：`BoostIO/boost-releases` · 分片：`apps/linux/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux boostnote`

### 开源跨平台电子书阅读器 Koodo Reader · `koodo_reader`

开源跨平台电子书阅读器 Koodo Reader 2.3.5 免费好用的电子书阅读器

- 仓库：`troyeguo/koodo-reader` · 分片：`apps/linux/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux koodo_reader`

### 专业 EPUB 格式电子书编辑器 Sigil · `sigil`

专业 EPUB 格式电子书编辑器 Sigil 2.8.0 x64 中文多语免费版

- 仓库：`Sigil-Ebook/Sigil` · 分片：`apps/linux/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sigil`

### 开源跨平台免费电子书阅读器 Thorium Reader · `thorium_reader`

开源跨平台免费电子书阅读器 Thorium Reader 2.3.0 中文多语免费版

- 仓库：`edrlab/thorium-reader` · 分片：`apps/linux/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux thorium_reader`

### vale · `vale`

（见仓库 Release 说明）

- 仓库：`errata-ai/vale` · 分片：`apps/linux/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux vale`

---

## 办公（6）

### AFFiNE 知识库/文档/白板 · `affine`

AFFiNE 知识库/文档/白板

- 仓库：`toeverything/AFFiNE` · 分片：`apps/linux/04-办公.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux affine`

### calibre · `calibre`

（见仓库 Release 说明）

- 仓库：`kovidgoyal/calibre` · 分片：`apps/linux/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux calibre`

### kiwix · `kiwix`

（见仓库 Release 说明）

- 仓库：`kiwix/kiwix-desktop` · 分片：`apps/linux/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kiwix`

### 开源免费 Office 部署管理工具 Office Tool Plus · `office_tool_plus`

开源免费 Office 部署管理工具 Office Tool Plus 11.4.17.0 中文版

- 仓库：`YerongAI/Office-Tool` · 分片：`apps/linux/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux office_tool_plus`

### onlyoffice · `onlyoffice`

（见仓库 Release 说明）

- 仓库：`ONLYOFFICE/DesktopEditors` · 分片：`apps/linux/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux onlyoffice`

### texstudio · `texstudio`

（见仓库 Release 说明）

- 仓库：`texstudio-org/texstudio` · 分片：`apps/linux/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux texstudio`

---

## 办公与设计（1）

### drawio · `drawio`

（见仓库 Release 说明）

- 仓库：`jgraph/drawio-desktop` · 分片：`apps/linux/05-办公与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux drawio`

---

## 加密货币（11）

### Bisq（去中心化交易 · `bisq_deb`

Bisq（去中心化交易，Debian/Ubuntu amd64 deb）

- 仓库：`bisq-network/bisq` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux bisq_deb`

### Bitcoin Core · `bitcoin_core`

Bitcoin Core

- 仓库：`bitcoin-core/gui` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux bitcoin_core`

### Electrum 轻钱包（Linux AppImage） · `electrum`

Electrum 轻钱包（Linux AppImage）

- 仓库：`spesmilo/electrum` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux electrum`

### Feather Wallet（Monero · `feather_wallet_appimage_amd64`

Feather Wallet（Monero，Linux x86_64 AppImage）

- 仓库：`feather-wallet/feather` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux feather_wallet_appimage_amd64`

### LND（Lightning Network · `lnd_linux_amd64`

LND（Lightning Network，Linux amd64 发行包）

- 仓库：`lightningnetwork/lnd` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux lnd_linux_amd64`

### OctoBot（加密交易机器人 · `octobot_linux_amd64`

OctoBot（加密交易机器人，Linux x64）

- 仓库：`Drakkar-Software/OctoBot` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux octobot_linux_amd64`

### OctoBot（加密交易机器人 · `octobot_linux_arm64`

OctoBot（加密交易机器人，Linux arm64）

- 仓库：`Drakkar-Software/OctoBot` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux octobot_linux_arm64`

### Sparrow Wallet（比特币钱包 · `sparrow_wallet_deb_amd64`

Sparrow Wallet（比特币钱包，amd64 deb）

- 仓库：`sparrowwallet/sparrow` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux sparrow_wallet_deb_amd64`

### Sparrow Wallet（比特币钱包 · `sparrow_wallet_deb_arm64`

Sparrow Wallet（比特币钱包，arm64 deb）

- 仓库：`sparrowwallet/sparrow` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux sparrow_wallet_deb_arm64`

### Specter Desktop（比特币多签 · `specter_desktop_linux`

Specter Desktop（比特币多签，Linux x86_64 桌面包 tar.gz）

- 仓库：`cryptoadvance/specter-desktop` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux specter_desktop_linux`

### Wasabi Wallet（Linux x64 zip 便携包） · `wasabi_wallet_linux`

Wasabi Wallet（Linux x64 zip 便携包）

- 仓库：`zkSNACKs/WalletWasabi` · 分片：`apps/linux/28-加密货币.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux wasabi_wallet_linux`

---

## 可观测（8）

### Grafana 可观测性仪表盘 · `grafana`

Grafana 可观测性仪表盘

- 仓库：`grafana/grafana` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux grafana`

### Grafana Alloy（OTel Collector 发行版） · `grafana_alloy`

Grafana Alloy（OTel Collector 发行版）

- 仓库：`grafana/alloy` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux grafana_alloy`

### Jaeger 分布式链路追踪 · `jaeger`

Jaeger 分布式链路追踪

- 仓库：`jaegertracing/jaeger` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux jaeger`

### Grafana Loki 日志聚合 · `loki`

Grafana Loki 日志聚合

- 仓库：`grafana/loki` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux loki`

### Netdata（监控 Agent · `netdata`

Netdata（监控 Agent，Linux 静态二进制）

- 仓库：`netdata/netdata` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux netdata`

### Prometheus 监控 · `prometheus`

Prometheus 监控

- 仓库：`prometheus/prometheus` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux prometheus`

### Grafana Tempo 追踪后端 · `tempo`

Grafana Tempo 追踪后端

- 仓库：`grafana/tempo` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux tempo`

### Vector 日志/指标采集 · `vector`

Vector 日志/指标采集

- 仓库：`vectordotdev/vector` · 分片：`apps/linux/25-可观测.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux vector`

---

## 命令行（19）

### atuin · `atuin`

（见仓库 Release 说明）

- 仓库：`atuinsh/atuin` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux atuin`

### bat · `bat`

（见仓库 Release 说明）

- 仓库：`sharkdp/bat` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bat`

### delta · `delta`

（见仓库 Release 说明）

- 仓库：`dandavison/delta` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux delta`

### dust · `dust`

（见仓库 Release 说明）

- 仓库：`bootandy/dust` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux dust`

### eza · `eza`

（见仓库 Release 说明）

- 仓库：`eza-community/eza` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux eza`

### fd · `fd`

（见仓库 Release 说明）

- 仓库：`sharkdp/fd` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fd`

### fzf · `fzf`

（见仓库 Release 说明）

- 仓库：`junegunn/fzf` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fzf`

### glow · `glow`

（见仓库 Release 说明）

- 仓库：`charmbracelet/glow` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux glow`

### hyperfine · `hyperfine`

（见仓库 Release 说明）

- 仓库：`sharkdp/hyperfine` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux hyperfine`

### jq · `jq`

（见仓库 Release 说明）

- 仓库：`jqlang/jq` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux jq`

### Kilo Code CLI / 独立包（zip/tar.gz） · `kilo_cli`

Kilo Code CLI / 独立包（zip/tar.gz）

- 仓库：`Kilo-Org/kilocode` · 分片：`apps/linux/06-命令行.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux kilo_cli`

### procs · `procs`

（见仓库 Release 说明）

- 仓库：`dalance/procs` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux procs`

### ripgrep · `ripgrep`

（见仓库 Release 说明）

- 仓库：`BurntSushi/ripgrep` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ripgrep`

### sd · `sd`

（见仓库 Release 说明）

- 仓库：`chmln/sd` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sd`

### starship · `starship`

（见仓库 Release 说明）

- 仓库：`starship/starship` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux starship`

### yazi · `yazi`

（见仓库 Release 说明）

- 仓库：`sxyazi/yazi` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux yazi`

### yq · `yq`

（见仓库 Release 说明）

- 仓库：`mikefarah/yq` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux yq`

### zellij · `zellij`

（见仓库 Release 说明）

- 仓库：`zellij-org/zellij` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux zellij`

### zoxide · `zoxide`

（见仓库 Release 说明）

- 仓库：`ajeetdsouza/zoxide` · 分片：`apps/linux/06-命令行.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux zoxide`

---

## 备份（3）

### kopia · `kopia`

（见仓库 Release 说明）

- 仓库：`kopia/kopia` · 分片：`apps/linux/07-备份.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kopia`

### restic（Linux x86_64 · `restic_linux_amd64`

restic（Linux x86_64，官方 .bz2 单文件包）

- 仓库：`restic/restic` · 分片：`apps/linux/07-备份.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux restic_linux_amd64`

### restic（Linux arm64 · `restic_linux_arm64`

restic（Linux arm64，官方 .bz2 单文件包）

- 仓库：`restic/restic` · 分片：`apps/linux/07-备份.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux restic_linux_arm64`

---

## 多媒体（25）

### audacity · `audacity`

（见仓库 Release 说明）

- 仓库：`audacity/audacity` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux audacity`

### 开源免费批量编码工具 BatchEncoder · `batchencoder`

开源免费批量编码工具 BatchEncoder 5.1 + x64 中文免费版

- 仓库：`wieslawsoltes/BatchEncoder` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux batchencoder`

### 开源转换 HDR 和 SDR 编解码器 Cine Encoder · `cine_encoder`

开源转换 HDR 和 SDR 编解码器 Cine Encoder 3.5.5 中文多语免费版

- 仓库：`CineEncoder/cine-encoder` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cine_encoder`

### 开源免费视频编码器 FastFlix · `fastflix`

开源免费视频编码器 FastFlix 6.2.1 中文版发布下载

- 仓库：`cdgriffith/FastFlix` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fastflix`

### 开源批量视频转换工具 FFmpeg Batch AV Converter · `ffmpeg_batch_av_converter`

开源批量视频转换工具 FFmpeg Batch AV Converter 3.2.9 x64 中文版

- 仓库：`eibol/ffmpeg_batch` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ffmpeg_batch_av_converter`

### handbrake · `handbrake`

（见仓库 Release 说明）

- 仓库：`HandBrake/HandBrake` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux handbrake`

### jellyfin media player · `jellyfin_media_player`

（见仓库 Release 说明）

- 仓库：`jellyfin/jellyfin-media-player` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux jellyfin_media_player`

### Jellyfin 媒体服务器（安装见 jellyfin.org；GitHub 主仓常无安装包 · `jellyfin_server`

Jellyfin 媒体服务器（安装见 jellyfin.org；GitHub 主仓常无安装包，勿启用）

- 仓库：`jellyfin/jellyfin` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux jellyfin_server`

### kdenlive · `kdenlive`

（见仓库 Release 说明）

- 仓库：`Kdenlive/kdenlive` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux kdenlive`

### 开源免费 DJ 混音软件 Mixxx · `mixxx`

开源免费 DJ 混音软件 Mixxx 2.5.2 中文多语免费版

- 仓库：`mixxxdj/mixxx` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mixxx`

### 轻量级开源媒体播放器 MPC-BE · `mpc_be`

轻量级开源媒体播放器 MPC-BE 1.8.7 + x64 免费好用的高清视频播放器

- 仓库：`Aleksoid1978/MPC-BE` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mpc_be`

### mpv · `mpv`

（见仓库 Release 说明）

- 仓库：`mpv-player/mpv` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mpv`

### musescore · `musescore`

（见仓库 Release 说明）

- 仓库：`musescore/MuseScore` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux musescore`

### 开源免费多功能音乐播放器 MusicPlayer2 · `musicplayer2`

开源免费多功能音乐播放器 MusicPlayer2 2.76.1 中文免费版

- 仓库：`zhongyang219/MusicPlayer2` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux musicplayer2`

### 开源视频编码工具 NotEnoughAV1Encodes · `notenoughav1encodes`

开源视频编码工具 NotEnoughAV1Encodes 2.1.7 中文多语免费版

- 仓库：`Alkl58/NotEnoughAV1Encodes` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux notenoughav1encodes`

### obs · `obs`

（见仓库 Release 说明）

- 仓库：`obsproject/obs-studio` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux obs`

### 开源媒体播放器 QMPlay2 Build · `qmplay2`

开源媒体播放器 QMPlay2 Build 25.09.11 + x64 中文多语免费版

- 仓库：`zaps166/QMPlay2` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qmplay2`

### recordly · `recordly`

（见仓库 Release 说明）

- 仓库：`webadderall/Recordly` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux recordly`

### shotcut · `shotcut`

（见仓库 Release 说明）

- 仓库：`mltframework/shotcut` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux shotcut`

### 开源音频频谱分析工具 Spek · `spek`

开源音频频谱分析工具 Spek 0.8.5 帮助你检查音频是否有损

- 仓库：`alexkay/spek` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux spek`

### strawberry · `strawberry`

（见仓库 Release 说明）

- 仓库：`strawberrymusicplayer/strawberry` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux strawberry`

### 开源本地音乐标签管理工具 Tag Editor · `tag_editor`

开源本地音乐标签管理工具 Tag Editor 3.9.10 发布下载

- 仓库：`Martchus/tageditor` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tag_editor`

### 开源 Windows 音量混合器 Volumey · `volumey`

开源 Windows 音量混合器 Volumey 1.5.4.0 + x64 中文多语免费版

- 仓库：`G-Stas/Volumey` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux volumey`

### 开源免费本地音乐播放器 Dopamine · `xmanager`

开源免费本地音乐播放器 Dopamine 3.0.5 中文多语免费版

- 仓库：`digimezzo/dopamine` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux xmanager`

### yt dlp · `yt_dlp`

（见仓库 Release 说明）

- 仓库：`yt-dlp/yt-dlp` · 分片：`apps/linux/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux yt_dlp`

---

## 多媒体与设计（14）

### blender · `blender`

（见仓库 Release 说明）

- 仓库：`blender/blender` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux blender`

### blockbench · `blockbench`

（见仓库 Release 说明）

- 仓库：`JannisX11/blockbench` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux blockbench`

### darktable · `darktable`

（见仓库 Release 说明）

- 仓库：`darktable-org/darktable` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux darktable`

### freecad · `freecad`

（见仓库 Release 说明）

- 仓库：`FreeCAD/FreeCAD` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux freecad`

### gimp · `gimp`

（见仓库 Release 说明）

- 仓库：`GNOME/gimp` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux gimp`

### Godot 游戏引擎 · `godot`

Godot 游戏引擎

- 仓库：`godotengine/godot` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux godot`

### inkscape · `inkscape`

（见仓库 Release 说明）

- 仓库：`inkscape/inkscape` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux inkscape`

### krita · `krita`

（见仓库 Release 说明）

- 仓库：`krita/krita` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux krita`

### makehuman · `makehuman`

开源 3D 人物角色建模软件 MakeHuman 1.3.0 中文多语免费版

- 仓库：`makehumancommunity/community-plugins-mhapi` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux makehuman`

### 开源VFX、动画与图形专业审阅工具 mrv2 · `mrv2`

开源VFX、动画与图形专业审阅工具 mrv2 v1.6.0 中文免费版

- 仓库：`ggarra13/mrv2` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mrv2`

### Photoshop PNG 优化插件 SuperPNG · `superpng`

Photoshop PNG 优化插件 SuperPNG 2.5 + x64 汉化中文版

- 仓库：`fnordware/Supe.PNG` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux superpng`

### 开源 AI 图像放大增强工具 Upscayl · `upscayl`

开源 AI 图像放大增强工具 Upscayl 2.15.0 x64 中文绿色汉化版

- 仓库：`upscayl/upscayl` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux upscayl`

### 图像视频智能放大工具 Waifu2x Extension GUI · `waifu2x_extension_gui`

图像视频智能放大工具 Waifu2x Extension GUI 3.111.01 中文免费版

- 仓库：`AaronFeng753/Waifu2x-Extension-GUI` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux waifu2x_extension_gui`

### 开源图像视频放大增强工具 Waifu2x GUI · `waifu2x_gui`

开源图像视频放大增强工具 Waifu2x GUI 0.5.0 中文绿色汉化版

- 仓库：`Tenpi/Waifu2x-GUI` · 分片：`apps/linux/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux waifu2x_gui`

---

## 安全（25）

### age cli · `age_cli`

（见仓库 Release 说明）

- 仓库：`FiloSottile/age` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux age_cli`

### bitwarden desktop · `bitwarden_desktop`

（见仓库 Release 说明）

- 仓库：`bitwarden/clients` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bitwarden_desktop`

### 开源免费跨平台密码管理软件 Buttercup · `buttercup`

开源免费跨平台密码管理软件 Buttercup 1.20.5 中文多语免费版

- 仓库：`buttercup/buttercup-desktop` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux buttercup`

### cryptomator · `cryptomator`

（见仓库 Release 说明）

- 仓库：`cryptomator/cryptomator` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cryptomator`

### dive Docker 镜像层分析 · `dive`

dive Docker 镜像层分析

- 仓库：`wagoodman/dive` · 分片：`apps/linux/10-安全.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux dive`

### dnsx · `dnsx`

（见仓库 Release 说明）

- 仓库：`projectdiscovery/dnsx` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux dnsx`

### duplicati · `duplicati`

（见仓库 Release 说明）

- 仓库：`duplicati/duplicati` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux duplicati`

### 开源 Windows 防火墙下载 Fort Firewall · `fort_firewall`

开源 Windows 防火墙下载 Fort Firewall 3.19.9 + x64 中文多语免费版

- 仓库：`tnodir/fort` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fort_firewall`

### gitleaks · `gitleaks`

（见仓库 Release 说明）

- 仓库：`gitleaks/gitleaks` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux gitleaks`

### katana · `katana`

（见仓库 Release 说明）

- 仓库：`projectdiscovery/katana` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux katana`

### keepassxc · `keepassxc`

（见仓库 Release 说明）

- 仓库：`keepassxreboot/keepassxc` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux keepassxc`

### 开源免费跨平台密码管理软件 KeeWeb · `keeweb`

开源免费跨平台密码管理软件 KeeWeb 1.18.1 中文免费版

- 仓库：`keeweb/keeweb` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux keeweb`

### mitmproxy · `mitmproxy`

（见仓库 Release 说明）

- 仓库：`mitmproxy/mitmproxy` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mitmproxy`

### naabu · `naabu`

（见仓库 Release 说明）

- 仓库：`projectdiscovery/naabu` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux naabu`

### opensca cli · `opensca_cli`

（见仓库 Release 说明）

- 仓库：`XmirrorSecurity/OpenSCA-cli` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux opensca_cli`

### OWASP ZAP（Linux 包） · `owasp_zap`

OWASP ZAP（Linux 包）

- 仓库：`zaproxy/zaproxy` · 分片：`apps/linux/10-安全.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux owasp_zap`

### 开源密码随机生成工具 Passliss · `passliss`

开源密码随机生成工具 Passliss 2.9.0.2302 中文多语免费版

- 仓库：`Leo-Corporation/Passliss` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux passliss`

### sops · `sops`

（见仓库 Release 说明）

- 仓库：`getsops/sops` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sops`

### subfinder · `subfinder`

（见仓库 Release 说明）

- 仓库：`projectdiscovery/subfinder` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux subfinder`

### 开源免费 Windows 网络防火墙工具 TinyWall · `tinywall`

开源免费 Windows 网络防火墙工具 TinyWall 3.5.1 中文多语免费版

- 仓库：`pylorak/TinyWall` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tinywall`

### trufflehog · `trufflehog`

（见仓库 Release 说明）

- 仓库：`trufflesecurity/trufflehog` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trufflehog`

### uncover · `uncover`

（见仓库 Release 说明）

- 仓库：`projectdiscovery/uncover` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux uncover`

### vscanplus · `vscanplus`

（见仓库 Release 说明）

- 仓库：`youki992/VscanPlus` · 分片：`apps/linux/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux vscanplus`

### zen desktop · `zen_desktop`

（见仓库 Release 说明）

- 仓库：`ZenPrivacy/zen-desktop` · 分片：`apps/linux/10-安全.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zen_desktop`

### zen desktop arm64 · `zen_desktop_arm64`

（见仓库 Release 说明）

- 仓库：`ZenPrivacy/zen-desktop` · 分片：`apps/linux/10-安全.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zen_desktop_arm64`

---

## 局域网文件共享（10）

### AList（Linux amd64 tar.gz） · `alist`

AList（Linux amd64 tar.gz）

- 仓库：`AlistGo/alist` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux alist`

### FileBrowser（Linux amd64 tar.gz） · `filebrowser`

FileBrowser（Linux amd64 tar.gz）

- 仓库：`filebrowser/filebrowser` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux filebrowser`

### fileshare-go · `fileshare-go`

（见仓库 Release 说明）

- 仓库：`fileshare-go/fileshare` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fileshare-go`

### go-drive · `go-drive`

（见仓库 Release 说明）

- 仓库：`devld/go-drive` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux go-drive`

### go-file · `go-file`

（见仓库 Release 说明）

- 仓库：`songquanpeng/go-file` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux go-file`

### go-share-cli · `go-share-cli`

（见仓库 Release 说明）

- 仓库：`sudo-init-do/go_share_cli` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux go-share-cli`

### gohttpserver · `gohttpserver`

（见仓库 Release 说明）

- 仓库：`codeskyblue/gohttpserver` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux gohttpserver`

### localfs-go · `localfs-go`

（见仓库 Release 说明）

- 仓库：`monocodx/localfs-go` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux localfs-go`

### 开源免费无线传输工具 NoCab Desktop · `nocab_desktop`

开源免费无线传输工具 NoCab Desktop 1.4.7 中文多语免费版

- 仓库：`nocab-transfer/nocab-desktop` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nocab_desktop`

### 开源免费文件共享工具 SyncTrayzor · `synctrayzor`

开源免费文件共享工具 SyncTrayzor 1.1.29 + x64 中文多语免费版

- 仓库：`canton7/SyncTrayzor` · 分片：`apps/linux/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux synctrayzor`

---

## 工具（11）

### 7-Zip（Linux x64 tar.xz · `7zip`

7-Zip（Linux x64 tar.xz，ip7z/7zip）

- 仓库：`ip7z/7zip` · 分片：`apps/linux/11-工具.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux 7zip`

### caesium · `caesium`

Caesium Image Compressor：当前 GitHub Release 无 Linux 通用二进制，请用 Flatpak（flathub）或发行版源。本条仅作仓库定位。

- 仓库：`Lymphatus/caesium-image-compressor` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux caesium`

### 开源免费颜色拾取工具 ColorPicker Max · `colorpicker`

开源免费颜色拾取工具 ColorPicker Max 6.9.0.2602 中文多语免费版

- 仓库：`Leo-Corporation/ColorPicker` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux colorpicker`

### 开源平替 Picasa 极速看图工具 FlyPhotos · `flyphotos`

开源平替 Picasa 极速看图工具 FlyPhotos v2.6.1 for Windows

- 仓库：`riyasy/FlyPhotos` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux flyphotos`

### 开源哈希校验工具 Hashing · `hashing`

开源哈希校验工具 Hashing 3.7 中文多语免费版

- 仓库：`hellzerg/hashing` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux hashing`

### 开源免费图像压缩工具 Imagine · `imagine_compression`

开源免费图像压缩工具 Imagine 0.7.5 中文多语免费版

- 仓库：`meowtec/Imagine` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux imagine_compression`

### 开源免费 · `nanazip`

开源免费 7-Zip 衍生产品 NanaZip 6.0.1711.0 x64 中文多语免费版

- 仓库：`M2Team/NanaZip` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nanazip`

### 开源免费文件批量重命名工具 OncePower · `oncepower`

开源免费文件批量重命名工具 OncePower 3.1.2 中文便携版

- 仓库：`ilgnefz/once_power` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux oncepower`

### 开源文件哈希外壳扩展 OpenHashTab · `openhashtab`

开源文件哈希外壳扩展 OpenHashTab 3.1.1 中文安装版

- 仓库：`namazso/OpenHashTab` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux openhashtab`

### 免费开源菠萝看图 Pineapple Picture · `pineapple_picture`

免费开源菠萝看图 Pineapple Picture 1.4.1 中文多语免费版

- 仓库：`BLumia/pineapple-pictures` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pineapple_picture`

### 开源免费轻量级 Windows 图像查看器 Quick Picture Viewer · `quick_picture_viewer`

开源免费轻量级 Windows 图像查看器 Quick Picture Viewer 3.1.4 中文免费版

- 仓库：`ModuleArt/quick-picture-viewer` · 分片：`apps/linux/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux quick_picture_viewer`

---

## 开发（37）

### act（Linux x64） · `act`

act（Linux x64）

- 仓库：`nektos/act` · 分片：`apps/linux/12-开发.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux act`

### actionlint · `actionlint`

（见仓库 Release 说明）

- 仓库：`rhysd/actionlint` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux actionlint`

### air · `air`

（见仓库 Release 说明）

- 仓库：`cosmtrek/air` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux air`

### biome · `biome`

（见仓库 Release 说明）

- 仓库：`biomejs/biome` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux biome`

### bruno · `bruno`

（见仓库 Release 说明）

- 仓库：`usebruno/bruno` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bruno`

### buf · `buf`

（见仓库 Release 说明）

- 仓库：`bufbuild/buf` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux buf`

### bun · `bun`

（见仓库 Release 说明）

- 仓库：`oven-sh/bun` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bun`

### chezmoi · `chezmoi`

（见仓库 Release 说明）

- 仓库：`twpayne/chezmoi` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux chezmoi`

### CMake 构建系统 · `cmake`

CMake 构建系统

- 仓库：`Kitware/CMake` · 分片：`apps/linux/12-开发.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux cmake`

### 开源免费 C/C++ 和 Fortran IDE Code::Blocks · `codeblocks`

开源免费 C/C++ 和 Fortran IDE Code::Blocks 24.04 中文汉化版

- 仓库：`anbangli/codeblocks-cn` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux codeblocks`

### deno · `deno`

（见仓库 Release 说明）

- 仓库：`denoland/deno` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux deno`

### 开源 .Net 反汇编工具 dnSpy · `dnspy`

开源 .Net 反汇编工具 dnSpy 6.5.1 + x64 中文绿色免费版

- 仓库：`dnSpyEx/dnSpy` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux dnspy`

### etcd 分布式键值 · `etcd`

etcd 分布式键值

- 仓库：`etcd-io/etcd` · 分片：`apps/linux/12-开发.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux etcd`

### fastfetch · `fastfetch`

（见仓库 Release 说明）

- 仓库：`fastfetch-cli/fastfetch` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fastfetch`

### Forgejo（Linux amd64） · `forgejo`

Forgejo（Linux amd64）

- 仓库：`forgejo/forgejo` · 分片：`apps/linux/12-开发.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux forgejo`

### git lfs · `git_lfs`

（见仓库 Release 说明）

- 仓库：`git-lfs/git-lfs` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux git_lfs`

### github cli · `github_cli`

（见仓库 Release 说明）

- 仓库：`cli/cli` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux github_cli`

### github desktop · `github_desktop`

（见仓库 Release 说明）

- 仓库：`desktop/desktop` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux github_desktop`

### Go 语言（Linux amd64 tar.gz · `go`

Go 语言（Linux amd64 tar.gz，go.dev/dl；非 GoLand）

- 仓库：`golang/go` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux go`

### GoLand IDE：仅 jetbrains.com；勿启用 · `goland`

GoLand IDE：仅 jetbrains.com；勿启用。Go 语言搜 go。

- 仓库：`octocat/Hello-World` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux goland`

### grpcurl · `grpcurl`

（见仓库 Release 说明）

- 仓库：`fullstorydev/grpcurl` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux grpcurl`

### httpie desktop · `httpie_desktop`

（见仓库 Release 说明）

- 仓库：`httpie/desktop` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux httpie_desktop`

### insomnia · `insomnia`

（见仓库 Release 说明）

- 仓库：`Kong/insomnia` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux insomnia`

### 免费开源 Flash 反编译工具 JPEXS Free Flash Decompiler · `jpexs_flash_decompiler`

免费开源 Flash 反编译工具 JPEXS Free Flash Decompiler 26.2.1 中文免费版

- 仓库：`jindrapetrik/jpexs-decompiler` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux jpexs_flash_decompiler`

### just · `just`

（见仓库 Release 说明）

- 仓库：`casey/just` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux just`

### lazygit · `lazygit`

（见仓库 Release 说明）

- 仓库：`jesseduffield/lazygit` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lazygit`

### mise · `mise`

（见仓库 Release 说明）

- 仓库：`jdx/mise` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux mise`

### 开源 .Net Reactor 脱壳工具 .Net Reactor Slayer · `net_reactor_slayer`

开源 .Net Reactor 脱壳工具 .Net Reactor Slayer 6.4.0 免费版下载

- 仓库：`SychicBoy/NetReactorSlayer` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux net_reactor_slayer`

### nodejs · `nodejs`

（见仓库 Release 说明）

- 仓库：`nodejs/node` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nodejs`

### oxlint · `oxlint`

（见仓库 Release 说明）

- 仓库：`oxc-project/oxc` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux oxlint`

### 开源 PE 文件分析工具 PE-bear · `pe_bear`

开源 PE 文件分析工具 PE-bear 0.7.1 中文绿色便携版

- 仓库：`hasherezade/pe-bear` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pe_bear`

### Playwright CLI（linux zip） · `playwright_cli`

Playwright CLI（linux zip）

- 仓库：`microsoft/playwright` · 分片：`apps/linux/12-开发.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux playwright_cli`

### shfmt · `shfmt`

（见仓库 Release 说明）

- 仓库：`mvdan/sh` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux shfmt`

### taplo · `taplo`

（见仓库 Release 说明）

- 仓库：`tamasfe/taplo` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux taplo`

### ty · `ty`

（见仓库 Release 说明）

- 仓库：`astral-sh/ty` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ty`

### 开源 EXE/Dll 资源压缩工具 UPX · `ultimate_packer_for_executables`

开源 EXE/Dll 资源压缩工具 UPX 5.1.1 + x64 发布！

- 仓库：`upx/upx` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ultimate_packer_for_executables`

### uv · `uv`

（见仓库 Release 说明）

- 仓库：`astral-sh/uv` · 分片：`apps/linux/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux uv`

---

## 效率（12）

### 开源免费思维导图工具 BlinkMind · `blinkmind`

开源免费思维导图工具 BlinkMind 0.1.6 中文多语免费版

- 仓库：`awehook/blink-mind-desktop` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux blinkmind`

### CopyQ 剪贴板管理 · `copyq`

CopyQ 剪贴板管理

- 仓库：`hluk/CopyQ` · 分片：`apps/linux/13-效率.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux copyq`

### 开源复制即翻译解决方案 CopyTranslator · `copytranslator`

开源复制即翻译解决方案 CopyTranslator 12.1.0 中文免费版

- 仓库：`copytranslator/CopyTranslator` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux copytranslator`

### Espanso 文本扩展 · `espanso`

Espanso 文本扩展

- 仓库：`espanso/espanso` · 分片：`apps/linux/13-效率.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux espanso`

### 开源免费屏幕截图工具 ksnip · `ksnip`

开源免费屏幕截图工具 ksnip 1.10.1 中文多语免费版

- 仓库：`ksnip/ksnip` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ksnip`

### 免费快速启动工具 Maye Nano · `maye`

免费快速启动工具 Maye Nano 6.1.0.260422 中文免费版

- 仓库：`25H/MayeNano` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux maye`

### picgo · `picgo`

（见仓库 Release 说明）

- 仓库：`Molunerfinn/PicGo` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux picgo`

### 开源免费 Windows 实用程序 PowerToys · `powertoys_2`

开源免费 Windows 实用程序 PowerToys 0.99.1 中文多语免费版

- 仓库：`ZetaSp/PowerToys-Chinese-TransMOD` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux powertoys_2`

### 这款开源免费的 QuickClipboard · `quickclipboard`

这款开源免费的 QuickClipboard 0.1.1 正在重新定义你的复制粘贴体验

- 仓库：`mosheng1/QuickClipboard` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux quickclipboard`

### 开源免费全快捷键截图/贴图工具 Screenote · `screenote`

开源免费全快捷键截图/贴图工具 Screenote 2020-07-02 中文免费版

- 仓库：`poerin/Screenote` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux screenote`

### stretchly · `stretchly`

（见仓库 Release 说明）

- 仓库：`hovancik/stretchly` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux stretchly`

### vhs · `vhs`

（见仓库 Release 说明）

- 仓库：`charmbracelet/vhs` · 分片：`apps/linux/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux vhs`

---

## 数据库（8）

### beekeeper · `beekeeper`

（见仓库 Release 说明）

- 仓库：`beekeeper-studio/beekeeper-studio` · 分片：`apps/linux/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux beekeeper`

### DBeaver CE 数据库客户端 · `dbeaver`

DBeaver CE 数据库客户端

- 仓库：`dbeaver/dbeaver` · 分片：`apps/linux/23-数据库.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux dbeaver`

### duckdb cli · `duckdb_cli`

（见仓库 Release 说明）

- 仓库：`duckdb/duckdb` · 分片：`apps/linux/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux duckdb_cli`

### pocketbase · `pocketbase`

（见仓库 Release 说明）

- 仓库：`pocketbase/pocketbase` · 分片：`apps/linux/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pocketbase`

### Redis Insight（Linux amd64 deb） · `redis_insight`

Redis Insight（Linux amd64 deb）

- 仓库：`RedisInsight/RedisInsight` · 分片：`apps/linux/23-数据库.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux redis_insight`

### DB Browser for SQLite（Linux x86_64 AppImage） · `sqlitebrowser`

DB Browser for SQLite（Linux x86_64 AppImage）

- 仓库：`sqlitebrowser/sqlitebrowser` · 分片：`apps/linux/23-数据库.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux sqlitebrowser`

### 开源跨平台 SQLite 管理工具 SQLiteStudio · `sqlitestudio`

开源跨平台 SQLite 管理工具 SQLiteStudio 3.4.21 中文多语免费版

- 仓库：`pawelsalawa/sqlitestudio` · 分片：`apps/linux/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sqlitestudio`

### supabase cli · `supabase_cli`

（见仓库 Release 说明）

- 仓库：`supabase/cli` · 分片：`apps/linux/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux supabase_cli`

---

## 游戏（18）

### cemu · `cemu`

（见仓库 Release 说明）

- 仓库：`cemu-project/Cemu` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cemu`

### 经典 DOSBox 项目开源模拟器 DOSBox-X · `dosbox_x`

经典 DOSBox 项目开源模拟器 DOSBox-X  2026.06.02 中文版

- 仓库：`joncampbell123/dosbox-x` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux dosbox_x`

### duckstation · `duckstation`

（见仓库 Release 说明）

- 仓库：`stenzek/duckstation` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux duckstation`

### heroic · `heroic`

（见仓库 Release 说明）

- 仓库：`Heroic-Games-Launcher/HeroicGamesLauncher` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux heroic`

### minetest · `minetest`

（见仓库 Release 说明）

- 仓库：`minetest/minetest` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux minetest`

### 开源 NES 游戏模拟器 My Nes · `my_nes`

开源 NES 游戏模拟器 My Nes 7.13.8155.38062 中文绿色版

- 仓库：`alaahadid/My-Nes` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux my_nes`

### openttd · `openttd`

（见仓库 Release 说明）

- 仓库：`OpenTTD/OpenTTD` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux openttd`

### pcsx2 · `pcsx2`

（见仓库 Release 说明）

- 仓库：`PCSX2/pcsx2` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pcsx2`

### prismlauncher · `prismlauncher`

（见仓库 Release 说明）

- 仓库：`PrismLauncher/PrismLauncher` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux prismlauncher`

### 开源跨平台 NES 模拟器 puNES · `punes`

开源跨平台 NES 模拟器 puNES 0.111 中文多语免费版

- 仓库：`punesemu/puNES` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux punes`

### retroarch · `retroarch`

（见仓库 Release 说明）

- 仓库：`libretro/RetroArch` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux retroarch`

### 开源 Flash Player 模拟器 Ruffle Nightly · `ruffle`

开源 Flash Player 模拟器 Ruffle Nightly 2026-05-11 免费下载

- 仓库：`ruffle-rs/ruffle` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ruffle`

### Ryujinx（Switch 模拟器 · `ryujinx`

Ryujinx（Switch 模拟器，linux）

- 仓库：`Ryubing/Ryujinx` · 分片：`apps/linux/14-游戏.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux ryujinx`

### 开源免费 Switch 模拟器 Ryujinx · `ryujinx_2`

开源免费 Switch 模拟器 Ryujinx 1.1.1403 中文多语免费版

- 仓库：`Ryujinx/Ryujinx` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux ryujinx_2`

### 开源独数解算工具 SudokuSolver · `sudokusolver`

开源独数解算工具 SudokuSolver 1.14.1 中文多语免费版

- 仓库：`DHancock/SudokuSolver` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sudokusolver`

### supertuxkart · `supertuxkart`

（见仓库 Release 说明）

- 仓库：`supertuxkart/stk-code` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux supertuxkart`

### 开源免费 GBA 模拟器 VisualBoyAdvance-M · `visualboyadvance_m`

开源免费 GBA 模拟器 VisualBoyAdvance-M 2.2.3 轻松畅玩 GBA 怀旧游戏

- 仓库：`visualboyadvance-m/visualboyadvance-m` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux visualboyadvance_m`

### wesnoth · `wesnoth`

（见仓库 Release 说明）

- 仓库：`wesnoth/wesnoth` · 分片：`apps/linux/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux wesnoth`

---

## 笔记（19）

### anytype · `anytype`

（见仓库 Release 说明）

- 仓库：`anyproto/anytype-ts` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux anytype`

### AppFlowy 开源 Notion 类 · `appflowy`

AppFlowy 开源 Notion 类

- 仓库：`AppFlowy-IO/AppFlowy` · 分片：`apps/linux/15-笔记.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux appflowy`

### 开源免费海狸笔记 Beaver Notes · `beaver_notes`

开源免费海狸笔记 Beaver Notes 4.4.0 x64 中文多语免费版

- 仓库：`Beaver-Notes/Beaver-Notes` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux beaver_notes`

### 优秀开源免费笔记软件 CherryTree · `cherrytree`

优秀开源免费笔记软件 CherryTree 1.7.0.0 x64 中文多语免费版

- 仓库：`giuspen/cherrytree` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cherrytree`

### 开源免费加密记事本 Crypto Notepad · `crypto_notepad`

开源免费加密记事本 Crypto Notepad 1.7.3 中文汉化版

- 仓库：`Crypto-Notepad/Crypto-Notepad` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux crypto_notepad`

### 开源免费桌面笔记工具 DesktopNote · `desktopnote`

开源免费桌面笔记工具 DesktopNote 1.6.4 绿色中文版

- 仓库：`changbowen/DesktopNote` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux desktopnote`

### joplin · `joplin`

（见仓库 Release 说明）

- 仓库：`laurent22/joplin` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux joplin`

### logseq · `logseq`

（见仓库 Release 说明）

- 仓库：`logseq/logseq` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux logseq`

### memos · `memos`

（见仓库 Release 说明）

- 仓库：`usememos/memos` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux memos`

### 开源免费加密笔记软件 Notesnook · `notesnook`

开源免费加密笔记软件 Notesnook 3.3.18 x64 中文汉化解锁版

- 仓库：`streetwriters/notesnook` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux notesnook`

### obsidian · `obsidian`

（见仓库 Release 说明）

- 仓库：`obsidianmd/obsidian-releases` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux obsidian`

### 开源桌面便签应用 Pinny Notes · `pinny_notes`

开源桌面便签应用 Pinny Notes 1.13.0 钉在屏幕上的便签神器

- 仓库：`63BeetleSmurf/PinnyNotes` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pinny_notes`

### qownnotes · `qownnotes`

（见仓库 Release 说明）

- 仓库：`pbek/QOwnNotes` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qownnotes`

### rowboat · `rowboat`

（见仓库 Release 说明）

- 仓库：`rowboatlabs/rowboat` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux rowboat`

### standardnotes · `standardnotes`

（见仓库 Release 说明）

- 仓库：`standardnotes/app` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux standardnotes`

### tangent · `tangent`

（见仓库 Release 说明）

- 仓库：`suchnsuch/Tangent` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tangent`

### trilium · `trilium`

（见仓库 Release 说明）

- 仓库：`TriliumNext/Trilium` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trilium`

### 免费开源笔记应用程序 Trilium Notes · `trilium_notes`

免费开源笔记应用程序 Trilium Notes 0.103.0 x64 官方中文免费版

- 仓库：`zadam/trilium` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trilium_notes`

### zettlr · `zettlr`

（见仓库 Release 说明）

- 仓库：`Zettlr/Zettlr` · 分片：`apps/linux/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux zettlr`

---

## 系统（22）

### Windows · `auto_dark_mode`

Windows 10 自动深色模式 Auto Dark Mode X 11.0.0.54 中文多语免费版

- 仓库：`Armin2208/Windows-Auto-Night-Mode` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux auto_dark_mode`

### Windows 右键菜单管理工具 ContextMenuManager · `context_menu_manager`

Windows 右键菜单管理工具 ContextMenuManager 3.3.3.1 中文免费版

- 仓库：`BluePointLilac/ContextMenuManager` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux context_menu_manager`

### 开源 Windows 动态桌面工具 DreamScene2 中文免费版 · `dreamscene2`

开源 Windows 动态桌面工具 DreamScene2 中文免费版

- 仓库：`he55/DreamScene2` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux dreamscene2`

### duf 磁盘空间概览 · `duf`

duf 磁盘空间概览

- 仓库：`muesli/duf` · 分片：`apps/linux/16-系统.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux duf`

### 开源 EFI 引导编辑器 EFI Boot Editor · `efi_boot_editor`

开源 EFI 引导编辑器 EFI Boot Editor 1.5.7 中文多语免费版

- 仓库：`Neverous/efibooteditor` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux efi_boot_editor`

### 开源电脑风扇控制软件 Fan Control · `fan_control`

开源电脑风扇控制软件 Fan Control v269 绿色中文便携版

- 仓库：`Rem0o/FanControl.Releases` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fan_control`

### Fedora Linux 系统启动盘创建工具 Fedora Media Writer · `fedora_media_writer`

Fedora Linux 系统启动盘创建工具 Fedora Media Writer 5.3.1 x64 中文版

- 仓库：`FedoraQt/MediaWriter` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux fedora_media_writer`

### LightBulb 开源护眼软件 LightBulb · `lightbulb`

LightBulb 开源护眼软件 LightBulb 2.7.1 + x64 中文绿色版

- 仓库：`Tyrrrz/LightBulb` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lightbulb`

### 开源 Windows 动态壁纸软件 Lively Wallpaper · `lively_wallpaper`

开源 Windows 动态壁纸软件 Lively Wallpaper 2.2.1.0 中文多语免费版

- 仓库：`rocksdanister/lively` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lively_wallpaper`

### 开源免费系统管理软件 NSudo · `nsudo`

开源免费系统管理软件 NSudo 8.2.0 中文免费版

- 仓库：`Thdub/NSudo_Installer` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nsudo`

### 开源电脑硬件信息检测工具 NWinfo · `nwinfo`

开源电脑硬件信息检测工具 NWinfo 1.6.4 绿色中文便携版

- 仓库：`a1ive/nwinfo` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nwinfo`

### 开源 Windows · `optimizer`

开源 Windows 10/11 系统优化工具 Optimizer 16.7 中文多语免费版

- 仓库：`hellzerg/optimizer` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux optimizer`

### 开源免费 Windows 系统优化利器 optimizerDuck · `optimizerduck`

开源免费 Windows 系统优化利器 optimizerDuck v2.20.0 更新发布

- 仓库：`itsfatduck/optimizerDuck` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux optimizerduck`

### Windows 密钥激活次数查询工具 PID Key Checker · `pid_key_checker`

Windows 密钥激活次数查询工具 PID Key Checker 4.0.0.0 中文免费版

- 仓库：`Ja7ad/PIDChecker` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux pid_key_checker`

### qemu · `qemu`

（见仓库 Release 说明）

- 仓库：`qemu/qemu` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qemu`

### 开源 Windows 系统优化调整工具 SophiApp · `sophiapp`

开源 Windows 系统优化调整工具 SophiApp 1.0.0.97 中文多语免费版

- 仓库：`Sophia-Community/SophiApp` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sophiapp`

### 强大的开源动态壁纸引擎 Sucrose Wallpaper Engine · `sucrose_wallpaper_engine`

强大的开源动态壁纸引擎 Sucrose Wallpaper Engine 26.6.4.0 中文版

- 仓库：`Taiizor/Sucrose` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux sucrose_wallpaper_engine`

### 开源免费注册表工具 Total Registry · `total_registry`

开源免费注册表工具 Total Registry 0.9.7.9 绿色汉化版

- 仓库：`zodiacon/TotalRegistry` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux total_registry`

### 开源检测 Win11 硬件需求工具 WhyNotWin11 · `whynotwin11`

开源检测 Win11 硬件需求工具 WhyNotWin11 2.7.0.0 中文多语免费版

- 仓库：`rcmaehl/WhyNotWin11` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux whynotwin11`

### 开源免费 Windows 动态桌面壁纸 WinDynamicDesktop · `windynamicdesktop`

开源免费 Windows 动态桌面壁纸 WinDynamicDesktop 5.6.1 中文免费版

- 仓库：`t1m0thyj/WinDynamicDesktop` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux windynamicdesktop`

### 开源免费 Windows · `winslop`

开源免费 Windows 11 优化工具 Winslop 26.03.110 绿色中文版

- 仓库：`builtbybel/Winslop` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux winslop`

### 开源 WSL 发行版管理器 WSL Manager · `wsl_manager`

开源 WSL 发行版管理器 WSL Manager 1.11.0 中文多语免费版

- 仓库：`bostrot/wsl2-distro-manager` · 分片：`apps/linux/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux wsl_manager`

---

## 终端（10）

### alacritty · `alacritty`

（见仓库 Release 说明）

- 仓库：`alacritty/alacritty` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux alacritty`

### bottom · `bottom`

（见仓库 Release 说明）

- 仓库：`ClementTsang/bottom` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bottom`

### electerm 终端/SSH/SFTP · `electerm`

electerm 终端/SSH/SFTP

- 仓库：`electerm/electerm` · 分片：`apps/linux/17-终端.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux electerm`

### Ghostty 终端（Linux 构建见官方文档；Release 以 tag 资产为准 · `ghostty`

Ghostty 终端（Linux 构建见官方文档；Release 以 tag 资产为准，优先 tar.gz/zip）

- 仓库：`ghostty-org/ghostty` · 分片：`apps/linux/17-终端.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux ghostty`

### 开源免费 Windows 终端仿真器 NxShell · `nxshell`

开源免费 Windows 终端仿真器 NxShell 1.9.3 中文多语免费版

- 仓库：`nxshell/nxshell` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nxshell`

### 开源免费 SSH 和 Telnet 客户端 Putty · `putty`

开源免费 SSH 和 Telnet 客户端 Putty 0.84 中文汉化版

- 仓库：`larryli/PuTTY` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux putty`

### tabby · `tabby`

（见仓库 Release 说明）

- 仓库：`Eugeny/tabby` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tabby`

### Warp：安装包见 warp.dev；GitHub Release 无桌面安装资产；勿启用 · `warp`

Warp：安装包见 warp.dev；GitHub Release 无桌面安装资产；勿启用。

- 仓库：`warpdotdev/warp` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux warp`

### wezterm · `wezterm`

（见仓库 Release 说明）

- 仓库：`wezterm/wezterm` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux wezterm`

### 开源免费命令终端 xTerminal · `xterminal`

开源免费命令终端 xTerminal 3.0.1.0 + x64 中文多语免费版

- 仓库：`0x78654C/xTerminal` · 分片：`apps/linux/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux xterminal`

---

## 编辑器（27）

### 开源免费 Windows 记事本 AkelPad · `akelpad`

开源免费 Windows 记事本 AkelPad 4.10.0.8 + x64 中文绿色版

- 仓库：`ssrlive/akelpad` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux akelpad`

### Antigravity Linux（manifest） · `antigravity`

Antigravity Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux antigravity`

### 开源免费跨平台代码编辑器 Atom · `atom_editor`

开源免费跨平台代码编辑器 Atom 1.63.0 + x64 官方中文最终版

- 仓库：`atom/atom` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux atom_editor`

### CodeBuddy Linux（manifest） · `codebuddy`

CodeBuddy Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux codebuddy`

### CodeBuddy CN Linux（manifest） · `codebuddy_cn`

CodeBuddy CN Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux codebuddy_cn`

### 免费开源代码编辑器 CudaText · `cudatext`

免费开源代码编辑器 CudaText 1.222.0.0 + x64 中文多语免费版

- 仓库：`Alexey-T/CudaText` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cudatext`

### Cursor（manifest 当前 linux 多为 null · `cursor`

Cursor（manifest 当前 linux 多为 null，勿盲目启用）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cursor`

### helix editor · `helix_editor`

（见仓库 Release 说明）

- 仓库：`helix-editor/helix` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux helix_editor`

### imhex · `imhex`

（见仓库 Release 说明）

- 仓库：`WerWolv/ImHex` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux imhex`

### lapce · `lapce`

（见仓库 Release 说明）

- 仓库：`lapce/lapce` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux lapce`

### Lite XL（Linux x86_64 tar.gz） · `lite_xl`

Lite XL（Linux x86_64 tar.gz）

- 仓库：`lite-xl/lite-xl` · 分片：`apps/linux/26-编辑器.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux lite_xl`

### Neovide（Linux AppImage） · `neovide`

Neovide（Linux AppImage）

- 仓库：`neovide/neovide` · 分片：`apps/linux/26-编辑器.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux neovide`

### neovim · `neovim`

（见仓库 Release 说明）

- 仓库：`neovim/neovim` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux neovim`

### notepad minusminus · `notepad_minusminus`

（见仓库 Release 说明）

- 仓库：`cxasm/notepad--` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux notepad_minusminus`

### 开源免费代码编辑器 Notepad Next · `notepad_next`

开源免费代码编辑器 Notepad Next 0.14 中文多语免费版

- 仓库：`dail8859/NotepadNext` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux notepad_next`

### pearai · `pearai`

PearAI（开源 AI 编辑器；GitHub Release 当前主要为 Linux tar.gz）

- 仓库：`trypear/pearai-app` · 分片：`apps/linux/26-编辑器.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux pearai`

### Pulsar（Linux x64 tar.gz） · `pulsar`

Pulsar（Linux x64 tar.gz）

- 仓库：`pulsar-edit/pulsar` · 分片：`apps/linux/26-编辑器.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux pulsar`

### Qoder Linux（manifest） · `qoder`

Qoder Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qoder`

### QoderWork（manifest） · `qoderwork`

QoderWork（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux qoderwork`

### skylark · `skylark`

（见仓库 Release 说明）

- 仓库：`adonais/skylark` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux skylark`

### Trae Linux（manifest） · `trae`

Trae Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trae`

### Trae CN Linux（manifest） · `trae_cn`

Trae CN Linux（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trae_cn`

### TRAE SOLO（manifest） · `trae_solo`

TRAE SOLO（manifest）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux trae_solo`

### Void（Linux x64 tar.gz） · `void_editor`

Void（Linux x64 tar.gz）

- 仓库：`voideditor/binaries` · 分片：`apps/linux/26-编辑器.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux void_editor`

### vscodium · `vscodium`

（见仓库 Release 说明）

- 仓库：`VSCodium/vscodium` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux vscodium`

### WorkBuddy（manifest；Linux 常 null） · `workbuddy`

WorkBuddy（manifest；Linux 常 null）

- 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux workbuddy`

### zed · `zed`

（见仓库 Release 说明）

- 仓库：`zed-industries/zed` · 分片：`apps/linux/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux zed`

---

## 网络（18）

### bandwhich · `bandwhich`

（见仓库 Release 说明）

- 仓库：`imsnif/bandwhich` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux bandwhich`

### cloudflared · `cloudflared`

（见仓库 Release 说明）

- 仓库：`cloudflare/cloudflared` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux cloudflared`

### croc · `croc`

（见仓库 Release 说明）

- 仓库：`schollz/croc` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux croc`

### 开源免费网络测试工具 InternetTest Pro · `internettest`

开源免费网络测试工具 InternetTest Pro 9.1.0.2602 中文多语免费版

- 仓库：`Leo-Corporation/InternetTest` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux internettest`

### localsend · `localsend`

（见仓库 Release 说明）

- 仓库：`localsend/localsend` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux localsend`

### nmap · `nmap`

（见仓库 Release 说明）

- 仓库：`nmap/nmap` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux nmap`

### OpenTrace · `opentrace`

OpenTrace 1.5.0.0 绿色中文版，让网络追踪从未如此简单

- 仓库：`Archeb/opentrace` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux opentrace`

### openvpn · `openvpn`

（见仓库 Release 说明）

- 仓库：`OpenVPN/openvpn` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux openvpn`

### rclone · `rclone`

（见仓库 Release 说明）

- 仓库：`rclone/rclone` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux rclone`

### Syncthing（Linux x86_64 官方 tar.gz · `syncthing`

Syncthing（Linux x86_64 官方 tar.gz，仅下载）

- 仓库：`syncthing/syncthing` · 分片：`apps/linux/18-网络.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux syncthing`

### Syncthing（Linux arm64 官方 tar.gz · `syncthing_linux_arm64`

Syncthing（Linux arm64 官方 tar.gz，仅下载）

- 仓库：`syncthing/syncthing` · 分片：`apps/linux/18-网络.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux syncthing_linux_arm64`

### syncthingtray · `syncthingtray`

（见仓库 Release 说明）

- 仓库：`Martchus/syncthingtray` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux syncthingtray`

### tailscale · `tailscale`

（见仓库 Release 说明）

- 仓库：`tailscale/tailscale` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux tailscale`

### thorium · `thorium`

（见仓库 Release 说明）

- 仓库：`Alex313031/Thorium` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux thorium`

### wireshark · `wireshark`

（见仓库 Release 说明）

- 仓库：`wireshark/wireshark` · 分片：`apps/linux/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux wireshark`

### zen browser · `zen_browser`

（见仓库 Release 说明）

- 仓库：`zen-browser/desktop` · 分片：`apps/linux/18-网络.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zen_browser`

### zen browser arm64 · `zen_browser_arm64`

（见仓库 Release 说明）

- 仓库：`zen-browser/desktop` · 分片：`apps/linux/18-网络.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zen_browser_arm64`

### ZeroTier 虚拟组网 · `zerotier`

ZeroTier 虚拟组网

- 仓库：`zerotier/ZeroTierOne` · 分片：`apps/linux/18-网络.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zerotier`

---

## 网络与协作（4）

### Ferdium（聚合 Slack/Discord 等） · `ferdium`

Ferdium（聚合 Slack/Discord 等）

- 仓库：`ferdium/ferdium-app` · 分片：`apps/linux/19-网络与协作.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux ferdium`

### Mattermost 桌面客户端 · `mattermost_desktop`

Mattermost 桌面客户端

- 仓库：`mattermost/desktop` · 分片：`apps/linux/19-网络与协作.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux mattermost_desktop`

### Rocket.Chat 桌面客户端 · `rocketchat_desktop`

Rocket.Chat 桌面客户端

- 仓库：`RocketChat/Rocket.Chat.Electron` · 分片：`apps/linux/19-网络与协作.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux rocketchat_desktop`

### Zulip 桌面客户端 · `zulip_desktop`

Zulip 桌面客户端

- 仓库：`zulip/zulip-desktop` · 分片：`apps/linux/19-网络与协作.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux zulip_desktop`

---

## 网络与通讯（5）

### chatterino · `chatterino`

（见仓库 Release 说明）

- 仓库：`Chatterino/chatterino2` · 分片：`apps/linux/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux chatterino`

### element desktop · `element_desktop`

（见仓库 Release 说明）

- 仓库：`element-hq/element-desktop` · 分片：`apps/linux/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux element_desktop`

### signal desktop · `signal_desktop`

（见仓库 Release 说明）

- 仓库：`signalapp/Signal-Desktop` · 分片：`apps/linux/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux signal_desktop`

### telegram · `telegram`

（见仓库 Release 说明）

- 仓库：`telegramdesktop/tdesktop` · 分片：`apps/linux/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux telegram`

### 开源免费雷鸟邮件客户端 Mozilla Thunderbird · `thunderbird_2`

开源免费雷鸟邮件客户端 Mozilla Thunderbird 151.0 + x64 中文多语免费版

- 仓库：`mozilla/kitsune` · 分片：`apps/linux/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux thunderbird_2`

---

## 远程与协作（3）

### Barrier 开源 KVM · `barrier`

Barrier 开源 KVM

- 仓库：`debauchee/barrier` · 分片：`apps/linux/21-远程与协作.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux barrier`

### 开源远程控制和屏幕镜像工具 Escrcpy · `escrcpy`

开源远程控制和屏幕镜像工具 Escrcpy 2.11.1 中文免费版

- 仓库：`viarotel-org/escrcpy` · 分片：`apps/linux/21-远程与协作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux escrcpy`

### rustdesk · `rustdesk`

（见仓库 Release 说明）

- 仓库：`rustdesk/rustdesk` · 分片：`apps/linux/21-远程与协作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux rustdesk`

---

## 金融与股票（4）

### Actual Budget（Linux x86_64 AppImage） · `actual_budget_appimage_amd64`

Actual Budget（Linux x86_64 AppImage）

- 仓库：`actualbudget/actual` · 分片：`apps/linux/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux actual_budget_appimage_amd64`

### Actual Budget（Linux arm64 AppImage） · `actual_budget_appimage_arm64`

Actual Budget（Linux arm64 AppImage）

- 仓库：`actualbudget/actual` · 分片：`apps/linux/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux actual_budget_appimage_arm64`

### FreqUI（Freqtrade Web 界面 zip · `frequi`

FreqUI（Freqtrade Web 界面 zip，Linux 通用解压使用）

- 仓库：`freqtrade/frequi` · 分片：`apps/linux/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux frequi`

### TA-Lib（技术分析 C 库 · `ta_lib_deb_amd64`

TA-Lib（技术分析 C 库，Debian/Ubuntu amd64 deb）

- 仓库：`ta-lib/ta-lib` · 分片：`apps/linux/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux ta_lib_deb_amd64`

---

## 音视频（7）

### LosslessCut（无损裁剪/合并） · `losslesscut`

LosslessCut（无损裁剪/合并）

- 仓库：`mifi/lossless-cut` · 分片：`apps/linux/22-音视频.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux losslesscut`

### OpenShot 视频编辑器（AppImage） · `openshot`

OpenShot 视频编辑器（AppImage）

- 仓库：`OpenShot/openshot-qt` · 分片：`apps/linux/22-音视频.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux openshot`

### 开源免费多功能视频编辑下载工具 QuickCut · `quickcut`

开源免费多功能视频编辑下载工具 QuickCut 1.6.10 中文免费版

- 仓库：`HaujetZhao/QuickCut` · 分片：`apps/linux/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux quickcut`

### 开源免费 Gif 录制工具 ScreenToGif · `screen_to_gif`

开源免费 Gif 录制工具 ScreenToGif 2.43.1 中文多语免费版

- 仓库：`NickeManarin/ScreenToGif` · 分片：`apps/linux/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux screen_to_gif`

### 开源 Windows 桌面录像工具 Simple Screen Recorder · `simple_screen_recorder`

开源 Windows 桌面录像工具 Simple Screen Recorder 1.3.4 中文多语免费版

- 仓库：`lextrack/Simple-Screen-Recorder` · 分片：`apps/linux/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`python lookup_app.py --platform linux simple_screen_recorder`

### Syncplay（异地同步播放） · `syncplay`

Syncplay（异地同步播放）

- 仓库：`Syncplay/syncplay` · 分片：`apps/linux/22-音视频.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux syncplay`

### VidCutter（视频剪切/合并） · `vidcutter`

VidCutter（视频剪切/合并）

- 仓库：`ozmartian/vidcutter` · 分片：`apps/linux/22-音视频.json` · 配置：已配匹配规则
- 查找：`python lookup_app.py --platform linux vidcutter`

---
