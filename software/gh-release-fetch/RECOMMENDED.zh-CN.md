# 推荐开源软件（全分类导读）

> 由 `python tools/generate_recommended_md.py` 根据 [`apps/windows/`](apps/windows/) 自动生成，生成日期：**2026-06-09**。条目 **516** 个（windows 平台）。
> 技术索引与分片统计见 [`CATALOG.md`](CATALOG.md)。启用/更新：`lookup_app.bat <id>` → `run_saved_apps.bat`。

---

## AI（31）

### aichat（终端里用 OpenAI/本地模型等 · `aichat`

aichat（终端里用 OpenAI/本地模型等，多提供商 CLI）

- 仓库：`sigoden/aichat` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows aichat`

### aider（终端 AI 结对编程 · `aider`

aider（终端 AI 结对编程，Windows exe）

- 仓库：`Aider-AI/aider` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows aider`

### anything llm · `anything_llm`

AnythingLLM（本地 RAG / 文档聊天桌面端；版本 tag 来自 GitHub API，安装包走官方 CDN latest）

- 仓库：`Mintplex-Labs/anything-llm` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows anything_llm`

### AnythingLLM Windows ARM64（同上 · `anything_llm_arm64`

AnythingLLM Windows ARM64（同上，CDN latest Arm64 安装包）

- 仓库：`Mintplex-Labs/anything-llm` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows anything_llm_arm64`

### botgem · `botgem`

BotGem（AI 桌面客户端；Windows 安装包在 gaodeng/botgem-docs Release）

- 仓库：`gaodeng/botgem-docs` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows botgem`

### cc switch · `cc_switch`

CC Switch（Claude Code / Codex / Gemini CLI / OpenCode / OpenClaw 一站式配置与切换，Tauri；官方 MSI）

- 仓库：`farion1231/cc-switch` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows cc_switch`

### chatbox · `chatbox`

Chatbox：主仓库 chatboxai/chatbox 的 GitHub Release 多为源码；桌面版请从官网 https://chatboxai.app 或 Microsoft Store 获取。本条仅作定位。

- 仓库：`chatboxai/chatbox` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows chatbox`

### Cherry Studio（多模型 AI 桌面客户端 · `cherry_studio`

Cherry Studio（多模型 AI 桌面客户端，CherryHQ）

- 仓库：`CherryHQ/cherry-studio` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows cherry_studio`

### Claude Code（Anthropic 官方终端 CLI 原生构建 · `claude_code`

Claude Code（Anthropic 官方终端 CLI 原生构建，Windows x64 zip）

- 仓库：`anthropics/claude-code` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows claude_code`

### Cline（VS Code / Cursor 系扩展 · `cline`

Cline（VS Code / Cursor 系扩展，Release .vsix）

- 仓库：`cline/cline` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows cline`

### OpenAI Codex CLI（Rust 发行包 · `codex_cli`

OpenAI Codex CLI（Rust 发行包，Windows x64 推荐 exe.zip）

- 仓库：`openai/codex` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows codex_cli`

### Continue（VS Code / JetBrains 系 AI 编程扩展 · `continue`

Continue（VS Code / JetBrains 系 AI 编程扩展，Release .vsix）

- 仓库：`continuedev/continue` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows continue`

### deepseek cli · `deepseek_cli`

DeepSeek-TUI dispatcher（deepseek 命令；Windows x64；需配套 deepseek_tui 一起放到 PATH）

- 仓库：`Hmbown/DeepSeek-TUI` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows deepseek_cli`

### deepseek tui · `deepseek_tui`

DeepSeek-TUI companion runtime（deepseek-tui 命令；Windows x64；需与 deepseek_cli 同时存在）

- 仓库：`Hmbown/DeepSeek-TUI` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows deepseek_tui`

### gemini cli · `gemini_cli`

Gemini CLI（Google 官方；Release 多为 gemini-cli-bundle.zip 通用包）

- 仓库：`google-gemini/gemini-cli` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gemini_cli`

### github copilot cli · `github_copilot_cli`

GitHub Copilot：以 VS Code / JetBrains 插件或 gh copilot 为主，无单一 Windows 安装包 Release。本条仅作说明占位。

- 仓库：`microsoft/vscode` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows github_copilot_cli`

### Goose（block 开源 AI 编程助手 · `goose_ai`

Goose（block 开源 AI 编程助手，Windows CLI 压缩包）

- 仓库：`block/goose` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows goose_ai`

### GPT4All（本地运行 LLM 的桌面客户端） · `gpt4all`

GPT4All（本地运行 LLM 的桌面客户端）

- 仓库：`nomic-ai/gpt4all` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows gpt4all`

### 沉浸式翻译（浏览器扩展离线包 · `immersive_translate`

沉浸式翻译（浏览器扩展离线包，Chrome zip；解压后开发者模式加载）

- 仓库：`immersive-translate/immersive-translate` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows immersive_translate`

### Jan（离线优先的本地 AI 聊天客户端） · `jan`

Jan（离线优先的本地 AI 聊天客户端）

- 仓库：`janhq/jan` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows jan`

### LangChain：Python/JS 开发框架 · `langchain_note`

LangChain：Python/JS 开发框架，通过 PyPI/npm 安装，不适合本项目的 GitHub Release 二进制拉取。

- 仓库：`langchain-ai/langchain` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows langchain_note`

### LlamaIndex：Python 开发框架 · `llamaindex_note`

LlamaIndex：Python 开发框架，通过 pip 安装，无本工具链所需的独立安装包 Release。

- 仓库：`run-llama/llama_index` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows llamaindex_note`

### Lobe Chat Hub（多模型 AI 桌面客户端 · `lobe_chat`

Lobe Chat Hub（多模型 AI 桌面客户端，LobeHub）

- 仓库：`lobehub/lobe-chat` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows lobe_chat`

### nextchat · `nextchat`

NextChat（原 ChatGPT-Next-Web）：仓库 ChatGPTNextWeb/NextChat 的 Release 多为源码；在线/部署见项目说明。本条仅作定位。

- 仓库：`ChatGPTNextWeb/NextChat` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nextchat`

### Ollama（本地运行大模型与 OpenAI 风格 API） · `ollama`

Ollama（本地运行大模型与 OpenAI 风格 API）

- 仓库：`ollama/ollama` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows ollama`

### open claude cowork · `open_claude_cowork`

Open Claude Cowork（ComposioHQ/open-claude-cowork）：当前仓库无 GitHub Release 二进制，需 clone 后 setup。本条仅作定位。

- 仓库：`ComposioHQ/open-claude-cowork` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows open_claude_cowork`

### OpenCat：分发以 macOS App Store 等渠道为主 · `opencat`

OpenCat：分发以 macOS App Store 等渠道为主，无固定 GitHub Release 二进制；repo_path 仅满足配置校验，勿启用。

- 仓库：`octocat/Hello-World` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows opencat`

### openclaw · `openclaw`

OpenClaw（个人 AI 助手；Windows 用 Release 中 OpenClaw-*.zip）

- 仓库：`openclaw/openclaw` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows openclaw`

### OpenCode（开源 AI 编程代理 / 桌面端 · `opencode`

OpenCode（开源 AI 编程代理 / 桌面端，SST 团队）

- 仓库：`sst/opencode` · 分片：`apps/windows/01-AI.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows opencode`

### OpenHands（开源 AI 软件工程师代理；桌面/CLI 以 Docker 与源码为主 · `openhands`

OpenHands（开源 AI 软件工程师代理；桌面/CLI 以 Docker 与源码为主，GitHub Release 常无安装包；本条仅索引）

- 仓库：`All-Hands-AI/OpenHands` · 分片：`apps/windows/01-AI.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows openhands`

### Roo Code（原 Roo-Cline · `roo_code`

Roo Code（原 Roo-Cline，VS Code AI 代理扩展，Release .vsix）

- 仓库：`RooCodeInc/Roo-Code` · 分片：`apps/windows/01-AI.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows roo_code`

---

## 下载（16）

### aria2（多协议下载 CLI · `aria2`

aria2（多协议下载 CLI，官方 64 位 zip；Release tag 形如 release-1.x）

- 仓库：`aria2/aria2` · 分片：`apps/windows/02-下载.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows aria2`

### 开源免费BT/批量下载工具 ArrowDL · `downzemall`

开源免费BT/批量下载工具 ArrowDL 4.2.1 x64 中文多语免费版

- 仓库：`setvisible/DownZemAll` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows downzemall`

### 开源免费文件蜈蚣下载器 File Centipede · `file_centipede`

开源免费文件蜈蚣下载器 File Centipede 2.82 x64 中文多语免费版

- 仓库：`filecxx/FileCentipede` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows file_centipede`

### gallery-dl 图站/相册批量下载（官方单文件 gallery-dl.exe） · `gallery_dl`

gallery-dl 图站/相册批量下载（官方单文件 gallery-dl.exe）

- 仓库：`mikf/gallery-dl` · 分片：`apps/windows/02-下载.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gallery_dl`

### Gopeed（HTTP/BT 等 · `gopeed`

Gopeed（HTTP/BT 等，现代下载器）

- 仓库：`GopeedLab/gopeed` · 分片：`apps/windows/02-下载.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows gopeed`

### 开源免费视频下载工具 Hitomi Downloader · `hitomi_downloader`

开源免费视频下载工具 Hitomi Downloader 4.2 中文多语免费版

- 仓库：`KurtBestor/Hitomi-Downloader` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows hitomi_downloader`

### 开源免费 BT 下载工具  LIII BitTorrent Client · `liii_bittorrent_client`

开源免费 BT 下载工具  LIII BitTorrent Client 0.1.1.19 中文多语免费版

- 仓库：`aliakseis/LIII` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows liii_bittorrent_client`

### lux（原 annie · `lux`

lux（原 annie，命令行抓取流媒体/站点视频）

- 仓库：`iawia002/lux` · 分片：`apps/windows/02-下载.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lux`

### 开源免费 m3u8 下载工具 m3u8 downloader · `m3u8_downloader`

开源免费 m3u8 下载工具 m3u8 downloader 3.0.1 中文免费版

- 仓库：`nilaoda/N_m3u8DL-CLI` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows m3u8_downloader`

### Motrix（全能下载工具：HTTP/FTP/BT/磁力链） · `motrix`

Motrix（全能下载工具：HTTP/FTP/BT/磁力链）

- 仓库：`agalwood/Motrix` · 分片：`apps/windows/02-下载.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows motrix`

### 开源免费下载工具 Persepolis Download Manager · `persepolis_download_manager`

开源免费下载工具 Persepolis Download Manager 3.2.0 中文免费版

- 仓库：`persepolisdm/persepolis` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows persepolis_download_manager`

### qBittorrent（BT/磁力下载 · `qbittorrent`

qBittorrent（BT/磁力下载，Windows x64 安装包）

- 仓库：`qbittorrent/qBittorrent` · 分片：`apps/windows/02-下载.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows qbittorrent`

### qBittorrent 增强版 qBittorrent Enhanced Edition · `qbittorrent_enhanced_edition`

qBittorrent 增强版 qBittorrent Enhanced Edition 5.2.1.10 中文版更新发布

- 仓库：`c0re100/qBittorrent-Enhanced-Edition` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows qbittorrent_enhanced_edition`

### Transmission（BT 客户端 · `transmission`

Transmission（BT 客户端，Windows x64 MSI）

- 仓库：`transmission/transmission` · 分片：`apps/windows/02-下载.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows transmission`

### 开源免费 Youtube 视频下载工具 YDL-UI · `ydl_ui`

开源免费 Youtube 视频下载工具 YDL-UI 2.9.1 中文多语免费版

- 仓库：`Maxstupo/ydl-ui` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ydl_ui`

### 开源免费视频下载工具 Open Video Downloader · `youtube_downloader_gui`

开源免费视频下载工具 Open Video Downloader 2.4.0 中文免费版

- 仓库：`jely2002/youtube-dl-gui` · 分片：`apps/windows/02-下载.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows youtube_downloader_gui`

---

## 云原生（18）

### Caddy HTTP/1-3 服务器与反向代理（自动 HTTPS · `caddy`

Caddy HTTP/1-3 服务器与反向代理（自动 HTTPS，单二进制 zip）

- 仓库：`caddyserver/caddy` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows caddy`

### 服务网格与服务发现 · `consul`

服务网格与服务发现

- 仓库：`hashicorp/consul` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows consul`

### DevSpace（K8s 本地开发循环与部署） · `devspace`

DevSpace（K8s 本地开发循环与部署）

- 仓库：`devspace-sh/devspace` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows devspace`

### Kubernetes Helm 包管理客户端 · `helm`

Kubernetes Helm 包管理客户端

- 仓库：`helm/helm` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows helm`

### K8s 终端 UI（zip） · `k9s`

K8s 终端 UI（zip）

- 仓库：`derailed/k9s` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows k9s`

### Kubernetes in Docker（无扩展名二进制） · `kind`

Kubernetes in Docker（无扩展名二进制）

- 仓库：`kubernetes-sigs/kind` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows kind`

### Compose 转 Kubernetes · `kompose`

Compose 转 Kubernetes

- 仓库：`kubernetes/kompose` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows kompose`

### kubectl 命令行（单文件） · `kubectl`

kubectl 命令行（单文件）

- 仓库：`kubernetes/kubernetes` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows kubectl`

### Lazydocker（终端里管理 Docker 容器/镜像/卷 · `lazydocker`

Lazydocker（终端里管理 Docker 容器/镜像/卷，jesseduffield）

- 仓库：`jesseduffield/lazydocker` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lazydocker`

### Lens Kubernetes IDE（OpenLens 分支常见） · `lens`

Lens Kubernetes IDE（OpenLens 分支常见）

- 仓库：`lensapp/lens` · 分片：`apps/windows/24-云原生.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows lens`

### 本地 Kubernetes 单节点集群 · `minikube`

本地 Kubernetes 单节点集群

- 仓库：`kubernetes/minikube` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows minikube`

### 工作负载调度与编排 · `nomad`

工作负载调度与编排

- 仓库：`hashicorp/nomad` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows nomad`

### 镜像构建自动化 · `packer`

镜像构建自动化

- 仓库：`hashicorp/packer` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows packer`

### Podman Desktop 容器桌面 · `podman_desktop`

Podman Desktop 容器桌面

- 仓库：`containers/podman-desktop` · 分片：`apps/windows/24-云原生.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows podman_desktop`

### Rancher Desktop（K8s/容器） · `rancher_desktop`

Rancher Desktop（K8s/容器）

- 仓库：`rancher-sandbox/rancher-desktop` · 分片：`apps/windows/24-云原生.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rancher_desktop`

### Kubernetes 开发工作流 · `skaffold`

Kubernetes 开发工作流

- 仓库：`GoogleContainerTools/skaffold` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows skaffold`

### 基础设施即代码（IaC） · `terraform`

基础设施即代码（IaC）

- 仓库：`hashicorp/terraform` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows terraform`

### Kubernetes 本地开发（tilt） · `tilt`

Kubernetes 本地开发（tilt）

- 仓库：`tilt-dev/tilt` · 分片：`apps/windows/24-云原生.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows tilt`

---

## 代理与隧道（7）

### Clash Verge Rev（Windows x64 安装包 · `clash_verge_rev`

Clash Verge Rev（Windows x64 安装包，Meta 内核；含 WebView2 修复版安装程序）

- 仓库：`clash-verge-rev/clash-verge-rev` · 分片：`apps/windows/30-代理与隧道.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows clash_verge_rev`

### FlClash（Flutter + Clash Meta 内核 · `flclash`

FlClash（Flutter + Clash Meta 内核，Windows x64 安装包）

- 仓库：`chen08209/FlClash` · 分片：`apps/windows/30-代理与隧道.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows flclash`

### Frpc Desktop（frp 桌面 GUI 客户端 · `frpc_desktop`

Frpc Desktop（frp 桌面 GUI 客户端，Windows Setup）

- 仓库：`luckjiawei/frpc-desktop` · 分片：`apps/windows/30-代理与隧道.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows frpc_desktop`

### Hiddify Next（跨平台代理客户端 · `hiddify_next`

Hiddify Next（跨平台代理客户端，Meta/多协议；Windows 官方 Setup）

- 仓库：`hiddify/hiddify-next` · 分片：`apps/windows/30-代理与隧道.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows hiddify_next`

### mihomo（Clash Meta 内核二进制 · `mihomo`

mihomo（Clash Meta 内核二进制，Windows amd64 zip）

- 仓库：`MetaCubeX/mihomo` · 分片：`apps/windows/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows mihomo`

### sing-box（通用代理内核 · `sing_box`

sing-box（通用代理内核，Windows amd64 zip）

- 仓库：`SagerNet/sing-box` · 分片：`apps/windows/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows sing_box`

### v2rayN（Windows x64 · `v2rayn`

v2rayN（Windows x64，官方 zip，仅下载解压使用；VLESS/Reality/Hysteria2 等协议）

- 仓库：`2dust/v2rayN` · 分片：`apps/windows/30-代理与隧道.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows v2rayn`

---

## 写作（8）

### 开源免费多平台 Markdown 写作工具 Boostnote · `boostnote`

开源免费多平台 Markdown 写作工具 Boostnote 0.16.0 x64 中文多语免费版

- 仓库：`BoostIO/boost-releases` · 分片：`apps/windows/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows boostnote`

### 开源跨平台电子书阅读器 Koodo Reader · `koodo_reader`

开源跨平台电子书阅读器 Koodo Reader 2.3.5 免费好用的电子书阅读器

- 仓库：`troyeguo/koodo-reader` · 分片：`apps/windows/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows koodo_reader`

### mdBook（Rust 官方 Markdown 电子书/文档站点生成器） · `mdbook`

mdBook（Rust 官方 Markdown 电子书/文档站点生成器）

- 仓库：`rust-lang/mdBook` · 分片：`apps/windows/03-写作.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows mdbook`

### Pandoc（文档格式转换 · `pandoc`

Pandoc（文档格式转换，Windows MSI）

- 仓库：`jgm/pandoc` · 分片：`apps/windows/03-写作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows pandoc`

### 专业 EPUB 格式电子书编辑器 Sigil · `sigil`

专业 EPUB 格式电子书编辑器 Sigil 2.8.0 x64 中文多语免费版

- 仓库：`Sigil-Ebook/Sigil` · 分片：`apps/windows/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows sigil`

### 开源跨平台免费电子书阅读器 Thorium Reader · `thorium_reader`

开源跨平台免费电子书阅读器 Thorium Reader 2.3.0 中文多语免费版

- 仓库：`edrlab/thorium-reader` · 分片：`apps/windows/03-写作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows thorium_reader`

### Vale（Markdown/文档风格与语法检查 CLI） · `vale`

Vale（Markdown/文档风格与语法检查 CLI）

- 仓库：`errata-ai/vale` · 分片：`apps/windows/03-写作.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows vale`

### Zola（静态站点生成器 · `zola`

Zola（静态站点生成器，Markdown 内容）

- 仓库：`getzola/zola` · 分片：`apps/windows/03-写作.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows zola`

---

## 办公（10）

### AFFiNE（知识库 / 文档 / 白板一体化 · `affine`

AFFiNE（知识库 / 文档 / 白板一体化，本地与同步）

- 仓库：`toeverything/AFFiNE` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows affine`

### 电子书管理与转换 · `calibre`

电子书管理与转换

- 仓库：`kovidgoyal/calibre` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows calibre`

### 离线维基与 ZIM 阅读 · `kiwix`

离线维基与 ZIM 阅读

- 仓库：`kiwix/kiwix-desktop` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows kiwix`

### NAPS2 扫描与 PDF 工具 · `naps2`

NAPS2 扫描与 PDF 工具

- 仓库：`naps2/naps2` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows naps2`

### 开源免费 Office 部署管理工具 Office Tool Plus · `office_tool_plus`

开源免费 Office 部署管理工具 Office Tool Plus 11.4.17.0 中文版

- 仓库：`YerongAI/Office-Tool` · 分片：`apps/windows/04-办公.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows office_tool_plus`

### ONLYOFFICE 桌面编辑器 · `onlyoffice`

ONLYOFFICE 桌面编辑器

- 仓库：`ONLYOFFICE/DesktopEditors` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows onlyoffice`

### PDF 页面合并 / 拆分 / 旋转 · `pdfarranger`

PDF 页面合并 / 拆分 / 旋转

- 仓库：`pdfarranger/pdfarranger` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows pdfarranger`

### Sumatra PDF 轻量阅读器 · `sumatra_pdf`

Sumatra PDF 轻量阅读器

- 仓库：`sumatrapdfreader/sumatrapdf` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sumatra_pdf`

### LaTeX 编辑器（需本机 TeX） · `texstudio`

LaTeX 编辑器（需本机 TeX）

- 仓库：`texstudio-org/texstudio` · 分片：`apps/windows/04-办公.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows texstudio`

### 排版系统（LaTeX 替代） · `typst`

排版系统（LaTeX 替代）

- 仓库：`typst/typst` · 分片：`apps/windows/04-办公.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows typst`

---

## 办公与设计（3）

### 流程图 / 架构图桌面版（draw.io） · `drawio`

流程图 / 架构图桌面版（draw.io）

- 仓库：`jgraph/drawio-desktop` · 分片：`apps/windows/05-办公与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows drawio`

### rnote（手写笔记 / PDF 标注 · `rnote`

rnote（手写笔记 / PDF 标注，矢量）

- 仓库：`flxzt/rnote` · 分片：`apps/windows/05-办公与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rnote`

### Stirling-PDF（本地 PDF 合并/拆分/旋转/压缩等工具箱） · `stirling_pdf`

Stirling-PDF（本地 PDF 合并/拆分/旋转/压缩等工具箱）

- 仓库：`stirling-tools/Stirling-PDF` · 分片：`apps/windows/05-办公与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows stirling_pdf`

---

## 加密货币（9）

### Bisq（去中心化比特币/P2P 交易桌面端；自托管、无中心化账户） · `bisq`

Bisq（去中心化比特币/P2P 交易桌面端；自托管、无中心化账户）

- 仓库：`bisq-network/bisq` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows bisq`

### Bitcoin Core（官方全节点 + 钱包 GUI · `bitcoin_core`

Bitcoin Core（官方全节点 + 钱包 GUI，Windows x64 setup）

- 仓库：`bitcoin-core/gui` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows bitcoin_core`

### Electrum（比特币轻钱包 · `electrum`

Electrum（比特币轻钱包，Windows setup）

- 仓库：`spesmilo/electrum` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows electrum`

### Feather Wallet（Monero 官方社区系轻钱包 · `feather_wallet`

Feather Wallet（Monero 官方社区系轻钱包，桌面端）

- 仓库：`feather-wallet/feather` · 分片：`apps/windows/28-加密货币.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows feather_wallet`

### LND（Lightning Network 守护进程 · `lnd`

LND（Lightning Network 守护进程，Bitcoin 二层支付；需配套 bitcoind）

- 仓库：`lightningnetwork/lnd` · 分片：`apps/windows/28-加密货币.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lnd`

### OctoBot（开源加密资产交易机器人/策略框架） · `octobot`

OctoBot（开源加密资产交易机器人/策略框架）

- 仓库：`Drakkar-Software/OctoBot` · 分片：`apps/windows/28-加密货币.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows octobot`

### Sparrow Wallet（比特币桌面钱包 · `sparrow_wallet`

Sparrow Wallet（比特币桌面钱包，支持硬件钱包与隐私功能）

- 仓库：`sparrowwallet/sparrow` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sparrow_wallet`

### Specter Desktop（比特币多签/硬件钱包协调与节点管理桌面端） · `specter_desktop`

Specter Desktop（比特币多签/硬件钱包协调与节点管理桌面端）

- 仓库：`cryptoadvance/specter-desktop` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows specter_desktop`

### Wasabi Wallet（比特币桌面钱包 · `wasabi_wallet`

Wasabi Wallet（比特币桌面钱包，CoinJoin 隐私向；请自行了解当地合规）

- 仓库：`zkSNACKs/WalletWasabi` · 分片：`apps/windows/28-加密货币.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows wasabi_wallet`

---

## 可观测（7）

### Grafana 可观测性仪表盘（Windows zip） · `grafana`

Grafana 可观测性仪表盘（Windows zip）

- 仓库：`grafana/grafana` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows grafana`

### Grafana Alloy（OpenTelemetry Collector 发行版 · `grafana_alloy`

Grafana Alloy（OpenTelemetry Collector 发行版，可观测数据管道）

- 仓库：`grafana/alloy` · 分片：`apps/windows/25-可观测.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows grafana_alloy`

### 分布式链路追踪 Jaeger · `jaeger`

分布式链路追踪 Jaeger

- 仓库：`jaegertracing/jaeger` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows jaeger`

### Grafana Loki（日志聚合 · `loki`

Grafana Loki（日志聚合，Windows 二进制 zip）

- 仓库：`grafana/loki` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows loki`

### Prometheus 监控 · `prometheus`

Prometheus 监控

- 仓库：`prometheus/prometheus` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows prometheus`

### Grafana Tempo（分布式追踪后端） · `tempo`

Grafana Tempo（分布式追踪后端）

- 仓库：`grafana/tempo` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows tempo`

### Vector（日志/指标采集与路由） · `vector`

Vector（日志/指标采集与路由）

- 仓库：`vectordotdev/vector` · 分片：`apps/windows/25-可观测.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows vector`

---

## 命令行（22）

### Atuin（Shell 历史同步/检索 · `atuin`

Atuin（Shell 历史同步/检索，跨会话搜索极快）

- 仓库：`atuinsh/atuin` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows atuin`

### cat 替代 · `bat`

cat 替代，带高亮（zip）

- 仓库：`sharkdp/bat` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows bat`

### git diff 高亮查看器（zip） · `delta`

git diff 高亮查看器（zip）

- 仓库：`dandavison/delta` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows delta`

### 磁盘使用可视化（du 替代） · `dust`

磁盘使用可视化（du 替代）

- 仓库：`bootandy/dust` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dust`

### 现代 ls 替代（Rust） · `eza`

现代 ls 替代（Rust）

- 仓库：`eza-community/eza` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows eza`

### find 替代（fd · `fd`

find 替代（fd，zip）

- 仓库：`sharkdp/fd` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fd`

### 命令行模糊查找器 · `fzf`

命令行模糊查找器

- 仓库：`junegunn/fzf` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fzf`

### 终端 Markdown 阅读器 · `glow`

终端 Markdown 阅读器

- 仓库：`charmbracelet/glow` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows glow`

### 命令行基准测试工具 · `hyperfine`

命令行基准测试工具

- 仓库：`sharkdp/hyperfine` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows hyperfine`

### JSON 命令行处理（官方发布页） · `jq`

JSON 命令行处理（官方发布页）

- 仓库：`jqlang/jq` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows jq`

### ls 增强（zip） · `lsd`

ls 增强（zip）

- 仓库：`lsd-rs/lsd` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lsd`

### 终端编辑器 micro（zip） · `micro`

终端编辑器 micro（zip）

- 仓库：`zyedidia/micro` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows micro`

### Nushell（结构化数据的现代 Shell） · `nushell`

Nushell（结构化数据的现代 Shell）

- 仓库：`nushell/nushell` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows nushell`

### 进程列表查看器（Rust） · `procs`

进程列表查看器（Rust）

- 仓库：`dalance/procs` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows procs`

### grep 替代（rg · `ripgrep`

grep 替代（rg，zip）

- 仓库：`BurntSushi/ripgrep` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ripgrep`

### 在 PDF/压缩包等中全文搜索 · `ripgrep_all`

在 PDF/压缩包等中全文搜索

- 仓库：`phiresky/ripgrep-all` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ripgrep_all`

### sed 式查找替换（更直观） · `sd`

sed 式查找替换（更直观）

- 仓库：`chmln/sd` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows sd`

### 跨 Shell 极简提示符 · `starship`

跨 Shell 极简提示符

- 仓库：`starship/starship` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows starship`

### Yazi（终端文件管理器 · `yazi`

Yazi（终端文件管理器，异步预览，Rust 实现）

- 仓库：`sxyazi/yazi` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows yazi`

### YAML/XML/JSON 命令行处理器 · `yq`

YAML/XML/JSON 命令行处理器

- 仓库：`mikefarah/yq` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows yq`

### Zellij（终端多窗格/会话与工作区 · `zellij`

Zellij（终端多窗格/会话与工作区，tmux 的现代替代之一）

- 仓库：`zellij-org/zellij` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows zellij`

### cd 智能跳转（zip） · `zoxide`

cd 智能跳转（zip）

- 仓库：`ajeetdsouza/zoxide` · 分片：`apps/windows/06-命令行.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows zoxide`

---

## 备份（4）

### Duplicacy（跨云去重备份 CLI · `duplicacy`

Duplicacy（跨云去重备份 CLI，Windows x64）

- 仓库：`gilbertchen/duplicacy` · 分片：`apps/windows/07-备份.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows duplicacy`

### Kopia（增量备份快照 · `kopia`

Kopia（增量备份快照，含 KopiaUI 安装包）

- 仓库：`kopia/kopia` · 分片：`apps/windows/07-备份.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows kopia`

### restic（加密去重备份 CLI · `restic`

restic（加密去重备份 CLI，官方 zip）

- 仓库：`restic/restic` · 分片：`apps/windows/07-备份.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows restic`

### rustic（Rust 实现的 restic 兼容备份 CLI） · `rustic`

rustic（Rust 实现的 restic 兼容备份 CLI）

- 仓库：`rustic-rs/rustic` · 分片：`apps/windows/07-备份.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows rustic`

---

## 多媒体（33）

### 多轨音频录制与编辑 · `audacity`

多轨音频录制与编辑

- 仓库：`audacity/audacity` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows audacity`

### Avidemux 简单剪辑与转码 · `avidemux`

Avidemux 简单剪辑与转码

- 仓库：`mean00/avidemux2` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows avidemux`

### 开源免费批量编码工具 BatchEncoder · `batchencoder`

开源免费批量编码工具 BatchEncoder 5.1 + x64 中文免费版

- 仓库：`wieslawsoltes/BatchEncoder` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows batchencoder`

### 开源转换 HDR 和 SDR 编解码器 Cine Encoder · `cine_encoder`

开源转换 HDR 和 SDR 编解码器 Cine Encoder 3.5.5 中文多语免费版

- 仓库：`CineEncoder/cine-encoder` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows cine_encoder`

### 开源免费视频编码器 FastFlix · `fastflix`

开源免费视频编码器 FastFlix 6.2.1 中文版发布下载

- 仓库：`cdgriffith/FastFlix` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows fastflix`

### 开源批量视频转换工具 FFmpeg Batch AV Converter · `ffmpeg_batch_av_converter`

开源批量视频转换工具 FFmpeg Batch AV Converter 3.2.9 x64 中文版

- 仓库：`eibol/ffmpeg_batch` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ffmpeg_batch_av_converter`

### FFmpeg 自动构建（BtbN · `ffmpeg_win64`

FFmpeg 自动构建（BtbN，tag 为 latest）

- 仓库：`BtbN/FFmpeg-Builds` · 分片：`apps/windows/08-多媒体.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ffmpeg_win64`

### 视频转码与压制（GUI） · `handbrake`

视频转码与压制（GUI）

- 仓库：`HandBrake/HandBrake` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows handbrake`

### Jellyfin 桌面客户端 · `jellyfin_media_player`

Jellyfin 桌面客户端

- 仓库：`jellyfin/jellyfin-media-player` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows jellyfin_media_player`

### jellyfin server · `jellyfin_server`

Jellyfin 媒体服务器（Windows 安装包见 jellyfin.org/downloads；主仓库 GitHub Release 常无 exe/msi，本条仅索引，勿启用）

- 仓库：`jellyfin/jellyfin` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows jellyfin_server`

### 非线性视频剪辑（KDE） · `kdenlive`

非线性视频剪辑（KDE）

- 仓库：`KDE/kdenlive` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows kdenlive`

### 数字音频工作站（DAW） · `lmms`

数字音频工作站（DAW）

- 仓库：`LMMS/lmms` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows lmms`

### 音视频元数据与技术信息查看 · `mediainfo`

音视频元数据与技术信息查看

- 仓库：`MediaArea/MediaInfo` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows mediainfo`

### 开源免费 DJ 混音软件 Mixxx · `mixxx`

开源免费 DJ 混音软件 Mixxx 2.5.2 中文多语免费版

- 仓库：`mixxxdj/mixxx` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows mixxx`

### 轻量级开源媒体播放器 MPC-BE · `mpc_be`

轻量级开源媒体播放器 MPC-BE 1.8.7 + x64 免费好用的高清视频播放器

- 仓库：`Aleksoid1978/MPC-BE` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows mpc_be`

### 媒体播放器 MPC-HC · `mpchc`

媒体播放器 MPC-HC

- 仓库：`clsid2/mpc-hc` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows mpchc`

### 极简命令行媒体播放器（Windows 构建） · `mpv`

极简命令行媒体播放器（Windows 构建）

- 仓库：`mpv-player/mpv` · 分片：`apps/windows/08-多媒体.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows mpv`

### MuseScore 制谱与播放 · `musescore`

MuseScore 制谱与播放

- 仓库：`musescore/MuseScore` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows musescore`

### 开源免费多功能音乐播放器 MusicPlayer2 · `musicplayer2`

开源免费多功能音乐播放器 MusicPlayer2 2.76.1 中文免费版

- 仓库：`zhongyang219/MusicPlayer2` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows musicplayer2`

### 开源视频编码工具 NotEnoughAV1Encodes · `notenoughav1encodes`

开源视频编码工具 NotEnoughAV1Encodes 2.1.7 中文多语免费版

- 仓库：`Alkl58/NotEnoughAV1Encodes` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows notenoughav1encodes`

### 直播与录屏（OBS Studio） · `obs`

直播与录屏（OBS Studio）

- 仓库：`obsproject/obs-studio` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows obs`

### 开源媒体播放器 QMPlay2 Build · `qmplay2`

开源媒体播放器 QMPlay2 Build 25.09.11 + x64 中文多语免费版

- 仓库：`zaps166/QMPlay2` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows qmplay2`

### 开源录屏与剪辑：自动缩放、光标动效、时间线、摄像头叠加、导出 MP4/GIF · `recordly`

开源录屏与剪辑：自动缩放、光标动效、时间线、摄像头叠加、导出 MP4/GIF

- 仓库：`webadderall/Recordly` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows recordly`

### 视频剪辑 · `shotcut`

视频剪辑

- 仓库：`mltframework/shotcut` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows shotcut`

### 开源音频频谱分析工具 Spek · `spek`

开源音频频谱分析工具 Spek 0.8.5 帮助你检查音频是否有损

- 仓库：`alexkay/spek` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows spek`

### Spotube（开源 Spotify 客户端 · `spotube`

Spotube（开源 Spotify 客户端，无 Premium 也可用）

- 仓库：`KRTirtho/spotube` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows spotube`

### Strawberry 音乐播放器（Clementine 分支） · `strawberry`

Strawberry 音乐播放器（Clementine 分支）

- 仓库：`strawberrymusicplayer/strawberry` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows strawberry`

### 字幕编辑与调轴 · `subtitleedit`

字幕编辑与调轴

- 仓库：`SubtitleEdit/subtitleedit` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows subtitleedit`

### 开源本地音乐标签管理工具 Tag Editor · `tag_editor`

开源本地音乐标签管理工具 Tag Editor 3.9.10 发布下载

- 仓库：`Martchus/tageditor` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows tag_editor`

### VLC 媒体播放器（跨平台） · `vlc`

VLC 媒体播放器（跨平台）

- 仓库：`videolan/vlc` · 分片：`apps/windows/08-多媒体.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows vlc`

### 开源 Windows 音量混合器 Volumey · `volumey`

开源 Windows 音量混合器 Volumey 1.5.4.0 + x64 中文多语免费版

- 仓库：`G-Stas/Volumey` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows volumey`

### 开源免费本地音乐播放器 Dopamine · `xmanager`

开源免费本地音乐播放器 Dopamine 3.0.5 中文多语免费版

- 仓库：`digimezzo/dopamine` · 分片：`apps/windows/08-多媒体.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows xmanager`

### 视频下载命令行（单文件 yt-dlp.exe） · `yt_dlp`

视频下载命令行（单文件 yt-dlp.exe）

- 仓库：`yt-dlp/yt-dlp` · 分片：`apps/windows/08-多媒体.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows yt_dlp`

---

## 多媒体与设计（16）

### blender · `blender`

开源 3D 创作套件（建模 / 渲染 / 动画）

- 仓库：`blender/blender` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows blender`

### blockbench · `blockbench`

方块风 3D 建模

- 仓库：`JannisX11/blockbench` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows blockbench`

### RAW 照片后期与工作流 · `darktable`

RAW 照片后期与工作流

- 仓库：`darktable-org/darktable` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows darktable`

### Ente Photos（端到端加密相册桌面端） · `ente_photos`

Ente Photos（端到端加密相册桌面端）

- 仓库：`ente-io/photos-desktop` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows ente_photos`

### freecad · `freecad`

参数化 3D CAD 建模

- 仓库：`FreeCAD/FreeCAD` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows freecad`

### GIMP 图像处理 · `gimp`

GIMP 图像处理

- 仓库：`GNOME/gimp` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows gimp`

### Godot 游戏引擎（Windows x64 标准版 zip） · `godot`

Godot 游戏引擎（Windows x64 标准版 zip）

- 仓库：`godotengine/godot` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows godot`

### 矢量图形编辑（SVG） · `inkscape`

矢量图形编辑（SVG）

- 仓库：`inkscape/inkscape` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows inkscape`

### 数字绘画与图像编辑 · `krita`

数字绘画与图像编辑

- 仓库：`krita/krita` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows krita`

### makehuman · `makehuman`

开源 3D 人物角色建模软件 MakeHuman 1.3.0 中文多语免费版

- 仓库：`makehumancommunity/community-plugins-mhapi` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows makehuman`

### 开源VFX、动画与图形专业审阅工具 mrv2 · `mrv2`

开源VFX、动画与图形专业审阅工具 mrv2 v1.6.0 中文免费版

- 仓库：`ggarra13/mrv2` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows mrv2`

### RAW 开发与转档 · `rawtherapee`

RAW 开发与转档

- 仓库：`Beep6581/RawTherapee` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rawtherapee`

### Photoshop PNG 优化插件 SuperPNG · `superpng`

Photoshop PNG 优化插件 SuperPNG 2.5 + x64 汉化中文版

- 仓库：`fnordware/Supe.PNG` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows superpng`

### 开源 AI 图像放大增强工具 Upscayl · `upscayl`

开源 AI 图像放大增强工具 Upscayl 2.15.0 x64 中文绿色汉化版

- 仓库：`upscayl/upscayl` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows upscayl`

### 图像视频智能放大工具 Waifu2x Extension GUI · `waifu2x_extension_gui`

图像视频智能放大工具 Waifu2x Extension GUI 3.111.01 中文免费版

- 仓库：`AaronFeng753/Waifu2x-Extension-GUI` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows waifu2x_extension_gui`

### 开源图像视频放大增强工具 Waifu2x GUI · `waifu2x_gui`

开源图像视频放大增强工具 Waifu2x GUI 0.5.0 中文绿色汉化版

- 仓库：`Tenpi/Waifu2x-GUI` · 分片：`apps/windows/09-多媒体与设计.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows waifu2x_gui`

---

## 安全（45）

### age（现代文件加密/解密工具 · `age_cli`

age（现代文件加密/解密工具，FiloSottile）

- 仓库：`FiloSottile/age` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows age_cli`

### OWASP Amass（子域枚举与信息收集） · `amass`

OWASP Amass（子域枚举与信息收集）

- 仓库：`owasp-amass/amass` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows amass`

### Bitwarden 桌面端（发布资产名含 desktop） · `bitwarden_desktop`

Bitwarden 桌面端（发布资产名含 desktop）

- 仓库：`bitwarden/clients` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows bitwarden_desktop`

### 开源免费跨平台密码管理软件 Buttercup · `buttercup`

开源免费跨平台密码管理软件 Buttercup 1.20.5 中文多语免费版

- 仓库：`buttercup/buttercup-desktop` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows buttercup`

### ClamAV 杀毒引擎（Windows x64 MSI） · `clamav`

ClamAV 杀毒引擎（Windows x64 MSI）

- 仓库：`Cisco-Talos/clamav` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows clamav`

### 容器镜像签名 · `cosign`

容器镜像签名

- 仓库：`sigstore/cosign` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows cosign`

### CrowdSec（协作式入侵检测 / 防火墙） · `crowdsec`

CrowdSec（协作式入侵检测 / 防火墙）

- 仓库：`crowdsecurity/crowdsec` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows crowdsec`

### 网盘目录加密 · `cryptomator`

网盘目录加密

- 仓库：`cryptomator/cryptomator` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows cryptomator`

### dive（分析 Docker 镜像层体积） · `dive`

dive（分析 Docker 镜像层体积）

- 仓库：`wagoodman/dive` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dive`

### dnsx（ProjectDiscovery DNS 探测与枚举） · `dnsx`

dnsx（ProjectDiscovery DNS 探测与枚举）

- 仓库：`projectdiscovery/dnsx` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dnsx`

### 云备份与增量备份 · `duplicati`

云备份与增量备份

- 仓库：`duplicati/duplicati` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows duplicati`

### 开源 Windows 防火墙下载 Fort Firewall · `fort_firewall`

开源 Windows 防火墙下载 Fort Firewall 3.19.9 + x64 中文多语免费版

- 仓库：`tnodir/fort` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows fort_firewall`

### FOSSA CLI（依赖与许可证分析） · `fossa_cli`

FOSSA CLI（依赖与许可证分析）

- 仓库：`fossas/fossa-cli` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fossa_cli`

### Gitleaks（Git 仓库密钥泄露扫描） · `gitleaks`

Gitleaks（Git 仓库密钥泄露扫描）

- 仓库：`gitleaks/gitleaks` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gitleaks`

### 容器镜像漏洞扫描 · `grype`

容器镜像漏洞扫描

- 仓库：`anchore/grype` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows grype`

### httpx（ProjectDiscovery · `httpx_pd`

httpx（ProjectDiscovery，HTTP 探测）

- 仓库：`projectdiscovery/httpx` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows httpx_pd`

### katana（ProjectDiscovery 爬虫/URL 抓取） · `katana`

katana（ProjectDiscovery 爬虫/URL 抓取）

- 仓库：`projectdiscovery/katana` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows katana`

### KeePass 经典版密码管理 · `keepass`

KeePass 经典版密码管理

- 仓库：`KeePass/KeePass` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows keepass`

### KeePass 系密码库 · `keepassxc`

KeePass 系密码库，离线为主

- 仓库：`keepassxreboot/keepassxc` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows keepassxc`

### 开源免费跨平台密码管理软件 KeeWeb · `keeweb`

开源免费跨平台密码管理软件 KeeWeb 1.18.1 中文免费版

- 仓库：`keeweb/keeweb` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows keeweb`

### kubeaudit（K8s 资源配置审计） · `kubeaudit`

kubeaudit（K8s 资源配置审计）

- 仓库：`Shopify/kubeaudit` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows kubeaudit`

### Kubescape（K8s 安全合规扫描） · `kubescape`

Kubescape（K8s 安全合规扫描）

- 仓库：`kubescape/kubescape` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows kubescape`

### mitmproxy · `mitmproxy`

mitmproxy 交互式 TLS HTTP 代理（安装包在 downloads.mitmproxy.org，非 GitHub 资产）

- 仓库：`mitmproxy/mitmproxy` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows mitmproxy`

### naabu（ProjectDiscovery 快速端口扫描） · `naabu`

naabu（ProjectDiscovery 快速端口扫描）

- 仓库：`projectdiscovery/naabu` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows naabu`

### Nuclei（漏洞扫描模板引擎） · `nuclei`

Nuclei（漏洞扫描模板引擎）

- 仓库：`projectdiscovery/nuclei` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows nuclei`

### OpenSCA-cli 软件成分分析 SCA / 供应链漏洞检测 · `opensca_cli`

OpenSCA-cli 软件成分分析 SCA / 供应链漏洞检测

- 仓库：`XmirrorSecurity/OpenSCA-cli` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows opensca_cli`

### osquery（SQL 查本机状态 · `osquery`

osquery（SQL 查本机状态，端点可见性）

- 仓库：`osquery/osquery` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows osquery`

### OWASP ZAP（Web 安全测试 · `owasp_zap`

OWASP ZAP（Web 安全测试，Windows 安装包）

- 仓库：`zaproxy/zaproxy` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows owasp_zap`

### 开源密码随机生成工具 Passliss · `passliss`

开源密码随机生成工具 Passliss 2.9.0.2302 中文多语免费版

- 仓库：`Leo-Corporation/Passliss` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows passliss`

### Rekor CLI（sigstore 透明日志查询） · `rekor_cli`

Rekor CLI（sigstore 透明日志查询）

- 仓库：`sigstore/rekor` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows rekor_cli`

### SLSA provenance 校验工具（slsa-verifier） · `slsa_verifier`

SLSA provenance 校验工具（slsa-verifier）

- 仓库：`slsa-framework/slsa-verifier` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows slsa_verifier`

### SOPS（YAML/JSON 等配置文件加密 · `sops`

SOPS（YAML/JSON 等配置文件加密，Mozilla）

- 仓库：`getsops/sops` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows sops`

### subfinder（ProjectDiscovery 子域发现） · `subfinder`

subfinder（ProjectDiscovery 子域发现）

- 仓库：`projectdiscovery/subfinder` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows subfinder`

### SBOM 生成工具 · `syft`

SBOM 生成工具

- 仓库：`anchore/syft` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows syft`

### Terrascan（IaC 静态分析与策略） · `terrascan`

Terrascan（IaC 静态分析与策略）

- 仓库：`tenable/terrascan` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows terrascan`

### 开源免费 Windows 网络防火墙工具 TinyWall · `tinywall`

开源免费 Windows 网络防火墙工具 TinyWall 3.5.1 中文多语免费版

- 仓库：`pylorak/TinyWall` · 分片：`apps/windows/10-安全.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows tinywall`

### 容器与 IaC 漏洞扫描 · `trivy`

容器与 IaC 漏洞扫描

- 仓库：`aquasecurity/trivy` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows trivy`

### TruffleHog（仓库/CI 密钥与敏感信息扫描） · `trufflehog`

TruffleHog（仓库/CI 密钥与敏感信息扫描）

- 仓库：`trufflesecurity/trufflehog` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows trufflehog`

### uncover（ProjectDiscovery 搜索引擎暴露面查询） · `uncover`

uncover（ProjectDiscovery 搜索引擎暴露面查询）

- 仓库：`projectdiscovery/uncover` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows uncover`

### 密钥与机密管理 · `vault`

密钥与机密管理

- 仓库：`hashicorp/vault` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows vault`

### 磁盘加密（VeraCrypt） · `veracrypt`

磁盘加密（VeraCrypt）

- 仓库：`veracrypt/VeraCrypt` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows veracrypt`

### VscanPlus 网站漏洞扫描（基于 vscan 二次开发 · `vscanplus`

VscanPlus 网站漏洞扫描（基于 vscan 二次开发，端口/指纹/目录 fuzz/POC）

- 仓库：`youki992/VscanPlus` · 分片：`apps/windows/10-安全.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows vscanplus`

### YubiKey Manager（Yubico 设备管理） · `yubikey_manager`

YubiKey Manager（Yubico 设备管理）

- 仓库：`Yubico/yubikey-manager` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows yubikey_manager`

### Zen 系统级广告拦截与隐私守护（Windows x64 安装包） · `zen_desktop`

Zen 系统级广告拦截与隐私守护（Windows x64 安装包）

- 仓库：`ZenPrivacy/zen-desktop` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zen_desktop`

### Zen 系统级广告拦截与隐私守护（Windows ARM64 安装包） · `zen_desktop_arm64`

Zen 系统级广告拦截与隐私守护（Windows ARM64 安装包）

- 仓库：`ZenPrivacy/zen-desktop` · 分片：`apps/windows/10-安全.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zen_desktop_arm64`

---

## 局域网文件共享（10）

### AList（多网盘挂载 · `alist`

AList（多网盘挂载，Windows amd64 zip）

- 仓库：`AlistGo/alist` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows alist`

### FileBrowser（Web 文件管理 · `filebrowser`

FileBrowser（Web 文件管理，单二进制 zip）

- 仓库：`filebrowser/filebrowser` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows filebrowser`

### fileshare-go · `fileshare-go`

fileshare-go/fileshare：gRPC + Web UI 内网传输（Windows 资产名为 fileshare-windows-x86_64.exe，无版本号后缀）

- 仓库：`fileshare-go/fileshare` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fileshare-go`

### devld/go-drive：轻量私有网盘（原 astaxie/GoDrive 仓库已不存在 · `go-drive`

devld/go-drive：轻量私有网盘（原 astaxie/GoDrive 仓库已不存在，此处用活跃维护的 devld/go-drive；Windows 为 zip 归档）

- 仓库：`devld/go-drive` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows go-drive`

### go-file · `go-file`

songquanpeng/go-file：单二进制 Web 共享、上传/下载、图床/视频/二维码（Release 资产名为 go-file.exe，无版本号后缀）

- 仓库：`songquanpeng/go-file` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows go-file`

### go-share-cli · `go-share-cli`

sudo-init-do/go_share_cli：CLI + Web 共享（仓库当前无 GitHub Release 二进制，仅作定位；请自行编译或关注作者分发）

- 仓库：`sudo-init-do/go_share_cli` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows go-share-cli`

### gohttpserver · `gohttpserver`

codeskyblue/gohttpserver：轻量 HTTP 目录服务（chfs 系常用实现；tag 如 1.3.0 无 v 前缀）

- 仓库：`codeskyblue/gohttpserver` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gohttpserver`

### localfs-go · `localfs-go`

monocodx/localfs-go：局域网文件服务（仓库当前无 GitHub Release 二进制，仅作定位；请自行编译或关注作者分发）

- 仓库：`monocodx/localfs-go` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows localfs-go`

### 开源免费无线传输工具 NoCab Desktop · `nocab_desktop`

开源免费无线传输工具 NoCab Desktop 1.4.7 中文多语免费版

- 仓库：`nocab-transfer/nocab-desktop` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nocab_desktop`

### 开源免费文件共享工具 SyncTrayzor · `synctrayzor`

开源免费文件共享工具 SyncTrayzor 1.1.29 + x64 中文多语免费版

- 仓库：`canton7/SyncTrayzor` · 分片：`apps/windows/29-局域网文件共享.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows synctrayzor`

---

## 工具（16）

### 7-Zip（官方 x64 MSI 安装包 · `7zip`

7-Zip（官方 x64 MSI 安装包，ip7z/7zip Release）

- 仓库：`ip7z/7zip` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows 7zip`

### AutoHotkey · `autohotkey`

AutoHotkey v2（Windows 安装包）

- 仓库：`AutoHotkey/AutoHotkey` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows autohotkey`

### Caesium Image Compressor（批量压缩图片 · `caesium`

Caesium Image Compressor（批量压缩图片，Windows 安装包）

- 仓库：`Lymphatus/caesium-image-compressor` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows caesium`

### 开源免费颜色拾取工具 ColorPicker Max · `colorpicker`

开源免费颜色拾取工具 ColorPicker Max 6.9.0.2602 中文多语免费版

- 仓库：`Leo-Corporation/ColorPicker` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows colorpicker`

### Ditto（剪贴板历史；Release 资产名带版本号 · `ditto`

Ditto（剪贴板历史；Release 资产名带版本号，优先 API 匹配 DittoSetup_64bit）

- 仓库：`saber/ditto` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows ditto`

### File Converter（右键菜单将图片/音视频转为其他格式 · `fileconverter`

File Converter（右键菜单将图片/音视频转为其他格式，依赖 FFmpeg）

- 仓库：`Tichau/FileConverter` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows fileconverter`

### 开源平替 Picasa 极速看图工具 FlyPhotos · `flyphotos`

开源平替 Picasa 极速看图工具 FlyPhotos v2.6.1 for Windows

- 仓库：`riyasy/FlyPhotos` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows flyphotos`

### 开源哈希校验工具 Hashing · `hashing`

开源哈希校验工具 Hashing 3.7 中文多语免费版

- 仓库：`hellzerg/hashing` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows hashing`

### ImageGlass（轻量看图 · `imageglass`

ImageGlass（轻量看图，x64 MSI）

- 仓库：`d2phap/ImageGlass` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows imageglass`

### 开源免费图像压缩工具 Imagine · `imagine_compression`

开源免费图像压缩工具 Imagine 0.7.5 中文多语免费版

- 仓库：`meowtec/Imagine` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows imagine_compression`

### 开源免费 · `nanazip`

开源免费 7-Zip 衍生产品 NanaZip 6.0.1711.0 x64 中文多语免费版

- 仓库：`M2Team/NanaZip` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nanazip`

### 开源免费文件批量重命名工具 OncePower · `oncepower`

开源免费文件批量重命名工具 OncePower 3.1.2 中文便携版

- 仓库：`ilgnefz/once_power` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows oncepower`

### 开源文件哈希外壳扩展 OpenHashTab · `openhashtab`

开源文件哈希外壳扩展 OpenHashTab 3.1.1 中文安装版

- 仓库：`namazso/OpenHashTab` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows openhashtab`

### PeaZip（压缩/解压缩工具） · `peazip`

PeaZip（压缩/解压缩工具）

- 仓库：`peazip/PeaZip` · 分片：`apps/windows/11-工具.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows peazip`

### 免费开源菠萝看图 Pineapple Picture · `pineapple_picture`

免费开源菠萝看图 Pineapple Picture 1.4.1 中文多语免费版

- 仓库：`BLumia/pineapple-pictures` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows pineapple_picture`

### 开源免费轻量级 Windows 图像查看器 Quick Picture Viewer · `quick_picture_viewer`

开源免费轻量级 Windows 图像查看器 Quick Picture Viewer 3.1.4 中文免费版

- 仓库：`ModuleArt/quick-picture-viewer` · 分片：`apps/windows/11-工具.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows quick_picture_viewer`

---

## 开发（60）

### act（本地运行 GitHub Actions · `act`

act（本地运行 GitHub Actions，Windows x64 zip）

- 仓库：`nektos/act` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows act`

### actionlint（GitHub Actions 工作流静态检查） · `actionlint`

actionlint（GitHub Actions 工作流静态检查）

- 仓库：`rhysd/actionlint` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows actionlint`

### Air（Go 热重载：保存即编译运行 · `air`

Air（Go 热重载：保存即编译运行，本地开发常用）

- 仓库：`cosmtrek/air` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows air`

### AST 结构感知的代码搜索 · `astgrep`

AST 结构感知的代码搜索

- 仓库：`ast-grep/ast-grep` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows astgrep`

### Biome（Rust：格式化 + Lint · `biome`

Biome（Rust：格式化 + Lint，高性能；可替代部分 ESLint/Prettier 工作流）

- 仓库：`biomejs/biome` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows biome`

### Bruno API 客户端（离线集合） · `bruno`

Bruno API 客户端（离线集合）

- 仓库：`usebruno/bruno` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows bruno`

### Buf（Protobuf 工具链：lint/breaking/format · `buf`

Buf（Protobuf 工具链：lint/breaking/format，含 buf 与 protoc 插件）

- 仓库：`bufbuild/buf` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows buf`

### Bun JavaScript 运行时与工具链 · `bun`

Bun JavaScript 运行时与工具链

- 仓库：`oven-sh/bun` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows bun`

### 点文件（dotfiles）管理 · `chezmoi`

点文件（dotfiles）管理

- 仓库：`twpayne/chezmoi` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows chezmoi`

### CMake 构建系统（Windows x64 安装包） · `cmake`

CMake 构建系统（Windows x64 安装包）

- 仓库：`Kitware/CMake` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows cmake`

### 开源免费 C/C++ 和 Fortran IDE Code::Blocks · `codeblocks`

开源免费 C/C++ 和 Fortran IDE Code::Blocks 24.04 中文汉化版

- 仓库：`anbangli/codeblocks-cn` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows codeblocks`

### Deno JavaScript/TypeScript 运行时 · `deno`

Deno JavaScript/TypeScript 运行时

- 仓库：`denoland/deno` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows deno`

### 开源 .Net 反汇编工具 dnSpy · `dnspy`

开源 .Net 反汇编工具 dnSpy 6.5.1 + x64 中文绿色免费版

- 仓库：`dnSpyEx/dnSpy` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows dnspy`

### dprint（多语言格式化 · `dprint`

dprint（多语言格式化，带插件生态）

- 仓库：`dprint/dprint` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dprint`

### etcd 分布式键值 · `etcd`

etcd 分布式键值

- 仓库：`etcd-io/etcd` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows etcd`

### Fastfetch（系统信息展示 · `fastfetch`

Fastfetch（系统信息展示，neofetch 的现代替代品，速度快）

- 仓库：`fastfetch-cli/fastfetch` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fastfetch`

### Fast Node Manager（fnm） · `fnm`

Fast Node Manager（fnm）

- 仓库：`Schniz/fnm` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows fnm`

### Forgejo（Git 托管 · `forgejo`

Forgejo（Git 托管，Windows amd64 zip）

- 仓库：`forgejo/forgejo` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows forgejo`

### Git for Windows（官方安装包） · `git_for_windows`

Git for Windows（官方安装包）

- 仓库：`git-for-windows/git` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows git_for_windows`

### Git LFS 大文件扩展 · `git_lfs`

Git LFS 大文件扩展

- 仓库：`git-lfs/git-lfs` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows git_lfs`

### Git for Windows（含 Git Bash） · `git_windows`

Git for Windows（含 Git Bash）

- 仓库：`git-for-windows/git` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows git_windows`

### 轻量 Git 服务（Windows amd64） · `gitea`

轻量 Git 服务（Windows amd64）

- 仓库：`go-gitea/gitea` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gitea`

### GitHub 官方命令行 gh（PR/Issue/Release 等） · `github_cli`

GitHub 官方命令行 gh（PR/Issue/Release 等）

- 仓库：`cli/cli` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows github_cli`

### GitHub Desktop（tag 常为 release-x.y.z） · `github_desktop`

GitHub Desktop（tag 常为 release-x.y.z）

- 仓库：`desktop/desktop` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows github_desktop`

### GitLab CLI（zip） · `glab`

GitLab CLI（zip）

- 仓库：`gitlab-org/cli` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows glab`

### Go 语言官方发行版（Windows MSI · `go`

Go 语言官方发行版（Windows MSI，自 go.dev/dl 解析；非 JetBrains GoLand IDE）

- 仓库：`golang/go` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows go`

### goland · `goland`

JetBrains GoLand IDE（商业/试用；请从 https://www.jetbrains.com/go/ 下载；本条仅索引，repo 占位，勿启用。Go 语言运行时请搜 id=go）

- 仓库：`octocat/Hello-World` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows goland`

### grpcurl（命令行调用 gRPC · `grpcurl`

grpcurl（命令行调用 gRPC，调试/脚本友好）

- 仓库：`fullstorydev/grpcurl` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows grpcurl`

### HTTPie Desktop（API 调试桌面客户端） · `httpie_desktop`

HTTPie Desktop（API 调试桌面客户端）

- 仓库：`httpie/desktop` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows httpie_desktop`

### 静态站点生成器 Hugo Extended（zip） · `hugo_extended`

静态站点生成器 Hugo Extended（zip）

- 仓库：`gohugoio/hugo` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows hugo_extended`

### HTTP 请求测试（curl 风格） · `hurl`

HTTP 请求测试（curl 风格）

- 仓库：`Orange-OpenSource/hurl` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows hurl`

### Insomnia REST/GraphQL 客户端 · `insomnia`

Insomnia REST/GraphQL 客户端

- 仓库：`Kong/insomnia` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows insomnia`

### 免费开源 Flash 反编译工具 JPEXS Free Flash Decompiler · `jpexs_flash_decompiler`

免费开源 Flash 反编译工具 JPEXS Free Flash Decompiler 26.2.1 中文免费版

- 仓库：`jindrapetrik/jpexs-decompiler` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows jpexs_flash_decompiler`

### 命令运行器（make 替代） · `just`

命令运行器（make 替代）

- 仓库：`casey/just` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows just`

### 终端 Git TUI（zip） · `lazygit`

终端 Git TUI（zip）

- 仓库：`jesseduffield/lazygit` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lazygit`

### mise（asdf 风格的多语言运行时与工具版本管理 · `mise`

mise（asdf 风格的多语言运行时与工具版本管理，jdx）

- 仓库：`jdx/mise` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows mise`

### 开源 .Net Reactor 脱壳工具 .Net Reactor Slayer · `net_reactor_slayer`

开源 .Net Reactor 脱壳工具 .Net Reactor Slayer 6.4.0 免费版下载

- 仓库：`SychicBoy/NetReactorSlayer` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows net_reactor_slayer`

### 模型结构可视化 · `netron`

模型结构可视化

- 仓库：`lutzroeder/netron` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows netron`

### Ninja 极速构建工具（release 为 zip） · `ninja`

Ninja 极速构建工具（release 为 zip）

- 仓库：`ninja-build/ninja` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ninja`

### Node.js 运行时（MSI 安装包） · `nodejs`

Node.js 运行时（MSI 安装包）

- 仓库：`nodejs/node` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows nodejs`

### nvm-windows（Node 版本管理器） · `nvm_windows`

nvm-windows（Node 版本管理器）

- 仓库：`coreybutler/nvm-windows` · 分片：`apps/windows/12-开发.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows nvm_windows`

### OpenCV 计算机视觉库（开发用） · `opencamera_bridge`

OpenCV 计算机视觉库（开发用）

- 仓库：`opencv/opencv` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows opencamera_bridge`

### Oxlint（Oxc 生态：极快 JS/TS Lint · `oxlint`

Oxlint（Oxc 生态：极快 JS/TS Lint，零配置倾向）

- 仓库：`oxc-project/oxc` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows oxlint`

### 开源 PE 文件分析工具 PE-bear · `pe_bear`

开源 PE 文件分析工具 PE-bear 0.7.1 中文绿色便携版

- 仓库：`hasherezade/pe-bear` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows pe_bear`

### Playwright CLI（Node 驱动浏览器自动化 · `playwright_cli`

Playwright CLI（Node 驱动浏览器自动化，Release zip）

- 仓库：`microsoft/playwright` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows playwright_cli`

### Python Standalone · `python_standalone_3_10`

Python Standalone 3.10（x64，stripped）

- 仓库：`astral-sh/python-build-standalone` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows python_standalone_3_10`

### Python Standalone · `python_standalone_3_11`

Python Standalone 3.11（x64，stripped）

- 仓库：`astral-sh/python-build-standalone` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows python_standalone_3_11`

### Python Standalone · `python_standalone_3_12`

Python Standalone 3.12（x64，stripped）

- 仓库：`astral-sh/python-build-standalone` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows python_standalone_3_12`

### Python Standalone · `python_standalone_3_13`

Python Standalone 3.13（x64，stripped）

- 仓库：`astral-sh/python-build-standalone` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows python_standalone_3_13`

### Python Standalone · `python_standalone_3_14`

Python Standalone 3.14（x64，stripped）

- 仓库：`astral-sh/python-build-standalone` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows python_standalone_3_14`

### 极快 Python linter/格式化 · `ruff`

极快 Python linter/格式化

- 仓库：`astral-sh/ruff` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ruff`

### Android 投屏控制（zip） · `scrcpy`

Android 投屏控制（zip）

- 仓库：`Genymobile/scrcpy` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows scrcpy`

### Semgrep 静态分析 · `semgrep`

Semgrep 静态分析

- 仓库：`returntocorp/semgrep` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows semgrep`

### shfmt（Shell 脚本格式化 · `shfmt`

shfmt（Shell 脚本格式化，mvdan/sh）

- 仓库：`mvdan/sh` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows shfmt`

### Taplo（TOML 格式化 / 校验 / LSP · `taplo`

Taplo（TOML 格式化 / 校验 / LSP，CLI）

- 仓库：`tamasfe/taplo` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows taplo`

### ty（Astral 出品 · `ty`

ty（Astral 出品，Python 类型检查器/语言服务器）

- 仓库：`astral-sh/ty` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ty`

### 开源 EXE/Dll 资源压缩工具 UPX · `ultimate_packer_for_executables`

开源 EXE/Dll 资源压缩工具 UPX 5.1.1 + x64 发布！

- 仓库：`upx/upx` · 分片：`apps/windows/12-开发.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ultimate_packer_for_executables`

### Python 包与项目管理（Rust） · `uv`

Python 包与项目管理（Rust）

- 仓库：`astral-sh/uv` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows uv`

### 文件变更时执行命令 · `watchexec`

文件变更时执行命令

- 仓库：`watchexec/watchexec` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows watchexec`

### Zig 语言工具链 · `zig`

Zig 语言工具链

- 仓库：`ziglang/zig` · 分片：`apps/windows/12-开发.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows zig`

---

## 效率（20）

### 开源免费思维导图工具 BlinkMind · `blinkmind`

开源免费思维导图工具 BlinkMind 0.1.6 中文多语免费版

- 仓库：`awehook/blink-mind-desktop` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows blinkmind`

### CopyQ（剪贴板历史与管理） · `copyq`

CopyQ（剪贴板历史与管理）

- 仓库：`hluk/CopyQ` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows copyq`

### 开源复制即翻译解决方案 CopyTranslator · `copytranslator`

开源复制即翻译解决方案 CopyTranslator 12.1.0 中文免费版

- 仓库：`copytranslator/CopyTranslator` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows copytranslator`

### 文本扩展/片段工具（安装包名无版本号） · `espanso`

文本扩展/片段工具（安装包名无版本号）

- 仓库：`espanso/espanso` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows espanso`

### 开源免费截图工具 Flameshot · `flameshot`

开源免费截图工具 Flameshot 13.2.0 x64 中文多语免费版

- 仓库：`flameshot-org/flameshot` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows flameshot`

### Flow Launcher（Windows 启动器 / 全局搜索与插件） · `flow_launcher`

Flow Launcher（Windows 启动器 / 全局搜索与插件）

- 仓库：`Flow-Launcher/Flow.Launcher` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows flow_launcher`

### Alt+Space 类启动器 · `flowlauncher`

Alt+Space 类启动器，可搜应用与插件

- 仓库：`Flow-Launcher/Flow.Launcher` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows flowlauncher`

### 截图与标注 · `greenshot`

截图与标注

- 仓库：`greenshot/greenshot` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows greenshot`

### 开源免费屏幕截图工具 ksnip · `ksnip`

开源免费屏幕截图工具 ksnip 1.10.1 中文多语免费版

- 仓库：`ksnip/ksnip` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ksnip`

### 免费快速启动工具 Maye Nano · `maye`

免费快速启动工具 Maye Nano 6.1.0.260422 中文免费版

- 仓库：`25H/MayeNano` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows maye`

### 图床上传工具 · `picgo`

图床上传工具

- 仓库：`Molunerfinn/PicGo` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows picgo`

### 开源免费 Windows 实用程序 PowerToys · `powertoys_2`

开源免费 Windows 实用程序 PowerToys 0.99.1 中文多语免费版

- 仓库：`ZetaSp/PowerToys-Chinese-TransMOD` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows powertoys_2`

### 这款开源免费的 QuickClipboard · `quickclipboard`

这款开源免费的 QuickClipboard 0.1.1 正在重新定义你的复制粘贴体验

- 仓库：`mosheng1/QuickClipboard` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows quickclipboard`

### 多网页应用聚合（社区版） · `rambox`

多网页应用聚合（社区版）

- 仓库：`ramboxapp/community-edition` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rambox`

### 开源免费全快捷键截图/贴图工具 Screenote · `screenote`

开源免费全快捷键截图/贴图工具 Screenote 2020-07-02 中文免费版

- 仓库：`poerin/Screenote` · 分片：`apps/windows/13-效率.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows screenote`

### 截图、录屏、OCR、上传分享 · `sharex`

截图、录屏、OCR、上传分享

- 仓库：`ShareX/ShareX` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sharex`

### 番茄钟与休息提醒 · `stretchly`

番茄钟与休息提醒

- 仓库：`hovancik/stretchly` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows stretchly`

### VHS（终端录屏生成 GIF/视频 · `vhs`

VHS（终端录屏生成 GIF/视频，charmbracelet）

- 仓库：`charmbracelet/vhs` · 分片：`apps/windows/13-效率.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows vhs`

### VocoType（本地端侧语音转文字输入工具 · `vocotype`

VocoType（本地端侧语音转文字输入工具，内置 Paraformer 中文 ASR 模型；Windows x64 NSIS 安装包）

- 仓库：`233stone/vocotype-cli` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows vocotype`

### 应用启动器（安装包名无版本号） · `wox`

应用启动器（安装包名无版本号）

- 仓库：`Wox-launcher/Wox` · 分片：`apps/windows/13-效率.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows wox`

---

## 数据库（12）

### SQL 编辑器与数据库管理 · `beekeeper`

SQL 编辑器与数据库管理

- 仓库：`beekeeper-studio/beekeeper-studio` · 分片：`apps/windows/23-数据库.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows beekeeper`

### CockroachDB（企业版注意许可） · `cockroach`

CockroachDB（企业版注意许可）

- 仓库：`cockroachdb/cockroach` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows cockroach`

### 数据库客户端（DBeaver CE） · `dbeaver`

数据库客户端（DBeaver CE）

- 仓库：`dbeaver/dbeaver` · 分片：`apps/windows/23-数据库.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows dbeaver`

### Dolt（Git 语义的关系型数据库 / 数据版本控制 CLI） · `dolt`

Dolt（Git 语义的关系型数据库 / 数据版本控制 CLI）

- 仓库：`dolthub/dolt` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dolt`

### DuckDB 命令行工具（Windows amd64 压缩包 · `duckdb_cli`

DuckDB 命令行工具（Windows amd64 压缩包，内含 duckdb.exe）

- 仓库：`duckdb/duckdb` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows duckdb_cli`

### PocketBase（单文件后端：嵌入式 SQLite + 实时 API + 管理后台） · `pocketbase`

PocketBase（单文件后端：嵌入式 SQLite + 实时 API + 管理后台）

- 仓库：`pocketbase/pocketbase` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows pocketbase`

### Redis Insight（Redis 图形客户端 · `redis_insight`

Redis Insight（Redis 图形客户端，Windows exe）

- 仓库：`RedisInsight/RedisInsight` · 分片：`apps/windows/23-数据库.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows redis_insight`

### sqlc（从 SQL 生成类型安全 Go 代码） · `sqlc`

sqlc（从 SQL 生成类型安全 Go 代码）

- 仓库：`sqlc-dev/sqlc` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows sqlc`

### DB Browser for SQLite（SQLite 图形化管理） · `sqlitebrowser`

DB Browser for SQLite（SQLite 图形化管理）

- 仓库：`sqlitebrowser/sqlitebrowser` · 分片：`apps/windows/23-数据库.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sqlitebrowser`

### 开源跨平台 SQLite 管理工具 SQLiteStudio · `sqlitestudio`

开源跨平台 SQLite 管理工具 SQLiteStudio 3.4.21 中文多语免费版

- 仓库：`pawelsalawa/sqlitestudio` · 分片：`apps/windows/23-数据库.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows sqlitestudio`

### Supabase CLI（本地开发、迁移与项目管理） · `supabase_cli`

Supabase CLI（本地开发、迁移与项目管理）

- 仓库：`supabase/cli` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows supabase_cli`

### usql（通用 SQL 客户端 · `usql`

usql（通用 SQL 客户端，支持多数据库）

- 仓库：`xo/usql` · 分片：`apps/windows/23-数据库.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows usql`

---

## 游戏（30）

### 古代战争 RTS · `0ad`

古代战争 RTS 0 A.D.

- 仓库：`0ad/0ad` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows 0ad`

### Wii U 模拟器 Cemu · `cemu`

Wii U 模拟器 Cemu

- 仓库：`cemu-project/Cemu` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows cemu`

### DOSBox Staging  DOS 环境 · `dosbox_staging`

DOSBox Staging  DOS 环境

- 仓库：`dosbox-staging/dosbox-staging` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows dosbox_staging`

### 经典 DOSBox 项目开源模拟器 DOSBox-X · `dosbox_x`

经典 DOSBox 项目开源模拟器 DOSBox-X  2026.06.02 中文版

- 仓库：`joncampbell123/dosbox-x` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows dosbox_x`

### PlayStation · `duckstation`

PlayStation 1 模拟器

- 仓库：`stenzek/duckstation` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows duckstation`

### 游戏启动器（Epic/GOG 等） · `heroic`

游戏启动器（Epic/GOG 等）

- 仓库：`Heroic-Games-Launcher/HeroicGamesLauncher` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows heroic`

### 体素沙盒（类 Minecraft） · `minetest`

体素沙盒（类 Minecraft）

- 仓库：`minetest/minetest` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows minetest`

### Moonlight（开源 GameStream 客户端 · `moonlight_qt`

Moonlight（开源 GameStream 客户端，配合 Sunshine / GeForce Experience）

- 仓库：`moonlight-stream/moonlight-qt` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows moonlight_qt`

### 开源 NES 游戏模拟器 My Nes · `my_nes`

开源 NES 游戏模拟器 My Nes 7.13.8155.38062 中文绿色版

- 仓库：`alaahadid/My-Nes` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows my_nes`

### Morrowind 开源引擎 · `openmw`

Morrowind 开源引擎

- 仓库：`OpenMW/openmw` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openmw`

### OpenRA（C&C 系列开源 RTS 引擎与 MOD） · `openra`

OpenRA（C&C 系列开源 RTS 引擎与 MOD）

- 仓库：`OpenRA/OpenRA` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openra`

### OpenRCT2（过山车大亨2）开源重制 · `openrct2`

OpenRCT2（过山车大亨2）开源重制

- 仓库：`OpenRCT2/OpenRCT2` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openrct2`

### 开源运输大亨 · `openttd`

开源运输大亨

- 仓库：`OpenTTD/OpenTTD` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openttd`

### PS2 模拟器 PCSX2 · `pcsx2`

PS2 模拟器 PCSX2

- 仓库：`PCSX2/pcsx2` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows pcsx2`

### 游戏库管理器 / 启动器（Playnite） · `playnite`

游戏库管理器 / 启动器（Playnite）

- 仓库：`JosefNemec/Playnite` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows playnite`

### Prism Launcher（Minecraft） · `prismlauncher`

Prism Launcher（Minecraft）

- 仓库：`PrismLauncher/PrismLauncher` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows prismlauncher`

### 开源跨平台 NES 模拟器 puNES · `punes`

开源跨平台 NES 模拟器 puNES 0.111 中文多语免费版

- 仓库：`punesemu/puNES` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows punes`

### RetroArch 模拟器前端 · `retroarch`

RetroArch 模拟器前端

- 仓库：`libretro/RetroArch` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows retroarch`

### PS3 模拟器（实验性） · `rpcs3`

PS3 模拟器（实验性）

- 仓库：`RPCS3/rpcs3` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows rpcs3`

### 开源 Flash Player 模拟器 Ruffle Nightly · `ruffle`

开源 Flash Player 模拟器 Ruffle Nightly 2026-05-11 免费下载

- 仓库：`ruffle-rs/ruffle` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ruffle`

### Ryujinx（Nintendo Switch 模拟器 · `ryujinx`

Ryujinx（Nintendo Switch 模拟器，Windows x64 便携 zip）

- 仓库：`Ryubing/Ryujinx` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ryujinx`

### 开源免费 Switch 模拟器 Ryujinx · `ryujinx_2`

开源免费 Switch 模拟器 Ryujinx 1.1.1403 中文多语免费版

- 仓库：`Ryujinx/Ryujinx` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ryujinx_2`

### 经典点击冒险游戏解释器 · `scummvm`

经典点击冒险游戏解释器

- 仓库：`scummvm/scummvm` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows scummvm`

### 开源独数解算工具 SudokuSolver · `sudokusolver`

开源独数解算工具 SudokuSolver 1.14.1 中文多语免费版

- 仓库：`DHancock/SudokuSolver` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows sudokusolver`

### Sunshine（Moonlight 的开源 GameStream 主机端） · `sunshine`

Sunshine（Moonlight 的开源 GameStream 主机端）

- 仓库：`LizardByte/Sunshine` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sunshine`

### SuperTuxKart 赛车 · `supertuxkart`

SuperTuxKart 赛车

- 仓库：`supertuxkart/stk-code` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows supertuxkart`

### 开源免费 GBA 模拟器 VisualBoyAdvance-M · `visualboyadvance_m`

开源免费 GBA 模拟器 VisualBoyAdvance-M 2.2.3 轻松畅玩 GBA 怀旧游戏

- 仓库：`visualboyadvance-m/visualboyadvance-m` · 分片：`apps/windows/14-游戏.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows visualboyadvance_m`

### 即时战略 Warzone · `warzone2100`

即时战略 Warzone 2100

- 仓库：`Warzone2100/warzone2100` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows warzone2100`

### 战棋《韦诺之战》 · `wesnoth`

战棋《韦诺之战》

- 仓库：`wesnoth/wesnoth` · 分片：`apps/windows/14-游戏.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows wesnoth`

### Xbox 模拟器 xemu · `xemu`

Xbox 模拟器 xemu

- 仓库：`mborgerson/xemu` · 分片：`apps/windows/14-游戏.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows xemu`

---

## 笔记（23）

### Anytype（开源本地优先 / P2P 对象笔记；Windows 安装包） · `anytype`

Anytype（开源本地优先 / P2P 对象笔记；Windows 安装包）

- 仓库：`anyproto/anytype-ts` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows anytype`

### AppFlowy（开源 Notion 类 · `appflowy`

AppFlowy（开源 Notion 类，本地与同步）

- 仓库：`AppFlowy-IO/AppFlowy` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows appflowy`

### 开源免费海狸笔记 Beaver Notes · `beaver_notes`

开源免费海狸笔记 Beaver Notes 4.4.0 x64 中文多语免费版

- 仓库：`Beaver-Notes/Beaver-Notes` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows beaver_notes`

### 优秀开源免费笔记软件 CherryTree · `cherrytree`

优秀开源免费笔记软件 CherryTree 1.7.0.0 x64 中文多语免费版

- 仓库：`giuspen/cherrytree` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows cherrytree`

### 开源免费加密记事本 Crypto Notepad · `crypto_notepad`

开源免费加密记事本 Crypto Notepad 1.7.3 中文汉化版

- 仓库：`Crypto-Notepad/Crypto-Notepad` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows crypto_notepad`

### 开源免费桌面笔记工具 DesktopNote · `desktopnote`

开源免费桌面笔记工具 DesktopNote 1.6.4 绿色中文版

- 仓库：`changbowen/DesktopNote` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows desktopnote`

### Markdown 笔记 · `joplin`

Markdown 笔记，默认参与更新

- 仓库：`laurent22/joplin` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows joplin`

### 大纲/双链笔记 · `logseq`

大纲/双链笔记

- 仓库：`logseq/logseq` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows logseq`

### Markdown 编辑器（安装包名无版本号） · `marktext`

Markdown 编辑器（安装包名无版本号）

- 仓库：`marktext/marktext` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows marktext`

### Memos（轻量自托管笔记/备忘录服务 · `memos`

Memos（轻量自托管笔记/备忘录服务，单二进制+Web）

- 仓库：`usememos/memos` · 分片：`apps/windows/15-笔记.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows memos`

### 开源免费加密笔记软件 Notesnook · `notesnook`

开源免费加密笔记软件 Notesnook 3.3.18 x64 中文汉化解锁版

- 仓库：`streetwriters/notesnook` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows notesnook`

### 本地知识库 / Markdown · `obsidian`

本地知识库 / Markdown，双链笔记

- 仓库：`obsidianmd/obsidian-releases` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows obsidian`

### 开源桌面便签应用 Pinny Notes · `pinny_notes`

开源桌面便签应用 Pinny Notes 1.13.0 钉在屏幕上的便签神器

- 仓库：`63BeetleSmurf/PinnyNotes` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows pinny_notes`

### Markdown 笔记（支持 Nextcloud） · `qownnotes`

Markdown 笔记（支持 Nextcloud）

- 仓库：`pbek/QOwnNotes` · 分片：`apps/windows/15-笔记.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows qownnotes`

### Rowboat 本地优先 AI 协作 / 知识图谱 · `rowboat`

Rowboat 本地优先 AI 协作 / 知识图谱，Obsidian 兼容 Markdown 库

- 仓库：`rowboatlabs/rowboat` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rowboat`

### 思源笔记（块级大纲 / Markdown） · `siyuan`

思源笔记（块级大纲 / Markdown）

- 仓库：`siyuan-note/siyuan` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows siyuan`

### Standard Notes 加密笔记 · `standardnotes`

Standard Notes 加密笔记

- 仓库：`standardnotes/app` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows standardnotes`

### tangent · `tangent`

Tangent（开源本地 Markdown PKM；官方安装包见 https://www.tangentnotes.com/Download 。GitHub suchnsuch/Tangent 无 Release 资产，启用自动下载前请改规则或用手动安装）

- 仓库：`suchnsuch/Tangent` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows tangent`

### 分层笔记（TriliumNext） · `trilium`

分层笔记（TriliumNext）

- 仓库：`TriliumNext/Trilium` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows trilium`

### 免费开源笔记应用程序 Trilium Notes · `trilium_notes`

免费开源笔记应用程序 Trilium Notes 0.103.0 x64 官方中文免费版

- 仓库：`zadam/trilium` · 分片：`apps/windows/15-笔记.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows trilium_notes`

### 手写笔记与 PDF 标注 · `xournalpp`

手写笔记与 PDF 标注

- 仓库：`xournalpp/xournalpp` · 分片：`apps/windows/15-笔记.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows xournalpp`

### Yank Note（yn）Markdown 笔记 · `yanknote`

Yank Note（yn）Markdown 笔记，本地优先、可运行代码块

- 仓库：`purocean/yn` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows yanknote`

### Markdown 写作环境 · `zettlr`

Markdown 写作环境

- 仓库：`Zettlr/Zettlr` · 分片：`apps/windows/15-笔记.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zettlr`

---

## 系统（35）

### Windows · `auto_dark_mode`

Windows 10 自动深色模式 Auto Dark Mode X 11.0.0.54 中文多语免费版

- 仓库：`Armin2208/Windows-Auto-Night-Mode` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows auto_dark_mode`

### Windows 右键菜单管理工具 ContextMenuManager · `context_menu_manager`

Windows 右键菜单管理工具 ContextMenuManager 3.3.3.1 中文免费版

- 仓库：`BluePointLilac/ContextMenuManager` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows context_menu_manager`

### 开源 Windows 动态桌面工具 DreamScene2 中文免费版 · `dreamscene2`

开源 Windows 动态桌面工具 DreamScene2 中文免费版

- 仓库：`he55/DreamScene2` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows dreamscene2`

### 磁盘空间概览（df 替代） · `duf`

磁盘空间概览（df 替代）

- 仓库：`muesli/duf` · 分片：`apps/windows/16-系统.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows duf`

### 开源 EFI 引导编辑器 EFI Boot Editor · `efi_boot_editor`

开源 EFI 引导编辑器 EFI Boot Editor 1.5.7 中文多语免费版

- 仓库：`Neverous/efibooteditor` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows efi_boot_editor`

### Everything 极速文件名搜索 · `everything_cli`

Everything 极速文件名搜索

- 仓库：`voidtools/Everything` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows everything_cli`

### Everything 任务栏集成（x64 安装包） · `everythingtoolbar`

Everything 任务栏集成（x64 安装包）

- 仓库：`stnkl/EverythingToolbar` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows everythingtoolbar`

### 开源电脑风扇控制软件 Fan Control · `fan_control`

开源电脑风扇控制软件 Fan Control v269 绿色中文便携版

- 仓库：`Rem0o/FanControl.Releases` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows fan_control`

### Fedora Linux 系统启动盘创建工具 Fedora Media Writer · `fedora_media_writer`

Fedora Linux 系统启动盘创建工具 Fedora Media Writer 5.3.1 x64 中文版

- 仓库：`FedoraQt/MediaWriter` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows fedora_media_writer`

### 交互式磁盘占用分析 · `gdu`

交互式磁盘占用分析

- 仓库：`dundee/gdu` · 分片：`apps/windows/16-系统.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows gdu`

### LightBulb 开源护眼软件 LightBulb · `lightbulb`

LightBulb 开源护眼软件 LightBulb 2.7.1 + x64 中文绿色版

- 仓库：`Tyrrrz/LightBulb` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows lightbulb`

### 开源 Windows 动态壁纸软件 Lively Wallpaper · `lively_wallpaper`

开源 Windows 动态壁纸软件 Lively Wallpaper 2.2.1.0 中文多语免费版

- 仓库：`rocksdanister/lively` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows lively_wallpaper`

### 将任意程序注册为 Windows 服务 · `nssm`

将任意程序注册为 Windows 服务

- 仓库：`nssm/nssm` · 分片：`apps/windows/16-系统.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows nssm`

### 开源免费系统管理软件 NSudo · `nsudo`

开源免费系统管理软件 NSudo 8.2.0 中文免费版

- 仓库：`Thdub/NSudo_Installer` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nsudo`

### 开源电脑硬件信息检测工具 NWinfo · `nwinfo`

开源电脑硬件信息检测工具 NWinfo 1.6.4 绿色中文便携版

- 仓库：`a1ive/nwinfo` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nwinfo`

### 开源 Windows · `optimizer`

开源 Windows 10/11 系统优化工具 Optimizer 16.7 中文多语免费版

- 仓库：`hellzerg/optimizer` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows optimizer`

### 开源免费 Windows 系统优化利器 optimizerDuck · `optimizerduck`

开源免费 Windows 系统优化利器 optimizerDuck v2.20.0 更新发布

- 仓库：`itsfatduck/optimizerDuck` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows optimizerduck`

### Windows 密钥激活次数查询工具 PID Key Checker · `pid_key_checker`

Windows 密钥激活次数查询工具 PID Key Checker 4.0.0.0 中文免费版

- 仓库：`Ja7ad/PIDChecker` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows pid_key_checker`

### 窗口置顶、重排、快捷键、命令面板等系统增强 · `powertoys`

窗口置顶、重排、快捷键、命令面板等系统增强

- 仓库：`microsoft/PowerToys` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows powertoys`

### Process Hacker 进程监视（现 System Informer） · `processhacker`

Process Hacker 进程监视（现 System Informer）

- 仓库：`processhacker/processhacker` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows processhacker`

### QEMU 模拟器（Windows 安装包名随发布变化） · `qemu`

QEMU 模拟器（Windows 安装包名随发布变化）

- 仓库：`qemu/qemu` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows qemu`

### 空格快速预览文件 · `quicklook`

空格快速预览文件

- 仓库：`QL-Win/QuickLook` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows quicklook`

### 制作 USB 启动盘 / 系统安装介质 · `rufus`

制作 USB 启动盘 / 系统安装介质

- 仓库：`pbatard/rufus` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rufus`

### 开源 Windows 系统优化调整工具 SophiApp · `sophiapp`

开源 Windows 系统优化调整工具 SophiApp 1.0.0.97 中文多语免费版

- 仓库：`Sophia-Community/SophiApp` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows sophiapp`

### 强大的开源动态壁纸引擎 Sucrose Wallpaper Engine · `sucrose_wallpaper_engine`

强大的开源动态壁纸引擎 Sucrose Wallpaper Engine 26.6.4.0 中文版

- 仓库：`Taiizor/Sucrose` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows sucrose_wallpaper_engine`

### System Informer（原 Process Hacker） · `systeminformer`

System Informer（原 Process Hacker）

- 仓库：`winsiderss/systeminformer` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows systeminformer`

### 开源免费注册表工具 Total Registry · `total_registry`

开源免费注册表工具 Total Registry 0.9.7.9 绿色汉化版

- 仓库：`zodiacon/TotalRegistry` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows total_registry`

### TrafficMonitor（任务栏/悬浮窗网速与硬件监控） · `trafficmonitor`

TrafficMonitor（任务栏/悬浮窗网速与硬件监控）

- 仓库：`zhongyang219/TrafficMonitor` · 分片：`apps/windows/16-系统.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows trafficmonitor`

### 任务栏调节显示器亮度 · `twinkletray`

任务栏调节显示器亮度

- 仓库：`xanderfrangos/twinkle-tray` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows twinkletray`

### UniGetUI（Winget / Scoop 等的图形化软件包管理前端 · `unigetui`

UniGetUI（Winget / Scoop 等的图形化软件包管理前端，原 WingetUI）

- 仓库：`marticliment/WingetUI` · 分片：`apps/windows/16-系统.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows unigetui`

### 多系统 U 盘启动（windows zip） · `ventoy`

多系统 U 盘启动（windows zip）

- 仓库：`ventoy/Ventoy` · 分片：`apps/windows/16-系统.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ventoy`

### 开源检测 Win11 硬件需求工具 WhyNotWin11 · `whynotwin11`

开源检测 Win11 硬件需求工具 WhyNotWin11 2.7.0.0 中文多语免费版

- 仓库：`rcmaehl/WhyNotWin11` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows whynotwin11`

### 开源免费 Windows 动态桌面壁纸 WinDynamicDesktop · `windynamicdesktop`

开源免费 Windows 动态桌面壁纸 WinDynamicDesktop 5.6.1 中文免费版

- 仓库：`t1m0thyj/WinDynamicDesktop` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows windynamicdesktop`

### 开源免费 Windows · `winslop`

开源免费 Windows 11 优化工具 Winslop 26.03.110 绿色中文版

- 仓库：`builtbybel/Winslop` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows winslop`

### 开源 WSL 发行版管理器 WSL Manager · `wsl_manager`

开源 WSL 发行版管理器 WSL Manager 1.11.0 中文多语免费版

- 仓库：`bostrot/wsl2-distro-manager` · 分片：`apps/windows/16-系统.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows wsl_manager`

---

## 终端（12）

### GPU 终端（Windows 安装器 MSI） · `alacritty`

GPU 终端（Windows 安装器 MSI）

- 仓库：`alacritty/alacritty` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows alacritty`

### 终端系统资源监视器（文件名无版本号） · `bottom`

终端系统资源监视器（文件名无版本号）

- 仓库：`ClementTsang/bottom` · 分片：`apps/windows/17-终端.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows bottom`

### 跨平台终端 / SSH / SFTP 客户端 · `electerm`

跨平台终端 / SSH / SFTP 客户端

- 仓库：`electerm/electerm` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows electerm`

### ghostty · `ghostty`

Ghostty 终端（Windows 安装包尚未在 GitHub Release 稳定提供；macOS/Linux 见对应平台配置；本条仅占位）

- 仓库：`ghostty-org/ghostty` · 分片：`apps/windows/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows ghostty`

### 开源免费 Windows 终端仿真器 NxShell · `nxshell`

开源免费 Windows 终端仿真器 NxShell 1.9.3 中文多语免费版

- 仓库：`nxshell/nxshell` · 分片：`apps/windows/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows nxshell`

### 开源免费 SSH 和 Telnet 客户端 Putty · `putty`

开源免费 SSH 和 Telnet 客户端 Putty 0.84 中文汉化版

- 仓库：`larryli/PuTTY` · 分片：`apps/windows/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows putty`

### Rio（Rust 终端模拟器 · `rio`

Rio（Rust 终端模拟器，GPU 渲染）

- 仓库：`raphamorim/rio` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rio`

### 跨平台终端 · `tabby`

跨平台终端，多标签与插件

- 仓库：`Eugeny/tabby` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows tabby`

### Warp（agentic 终端与开发环境 · `warp`

Warp（agentic 终端与开发环境，源码在 GitHub；正式安装包由 warp.dev 分发，Release 页无 exe/dmg 等资产；本条仅作索引，勿启用自动下载）

- 仓库：`warpdotdev/warp` · 分片：`apps/windows/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows warp`

### GPU 加速终端 · `wezterm`

GPU 加速终端，Lua 配置

- 仓库：`wezterm/wezterm` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows wezterm`

### Windows 终端（多标签 Shell） · `windows_terminal`

Windows 终端（多标签 Shell）

- 仓库：`microsoft/terminal` · 分片：`apps/windows/17-终端.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows windows_terminal`

### 开源免费命令终端 xTerminal · `xterminal`

开源免费命令终端 xTerminal 3.0.1.0 + x64 中文多语免费版

- 仓库：`0x78654C/xTerminal` · 分片：`apps/windows/17-终端.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows xterminal`

---

## 编辑器（21）

### 开源免费 Windows 记事本 AkelPad · `akelpad`

开源免费 Windows 记事本 AkelPad 4.10.0.8 + x64 中文绿色版

- 仓库：`ssrlive/akelpad` · 分片：`apps/windows/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows akelpad`

### 开源免费跨平台代码编辑器 Atom · `atom_editor`

开源免费跨平台代码编辑器 Atom 1.63.0 + x64 官方中文最终版

- 仓库：`atom/atom` · 分片：`apps/windows/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows atom_editor`

### 免费开源代码编辑器 CudaText · `cudatext`

免费开源代码编辑器 CudaText 1.222.0.0 + x64 中文多语免费版

- 仓库：`Alexey-T/CudaText` · 分片：`apps/windows/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows cudatext`

### Fork Git 图形客户端（Windows） · `fork`

Fork Git 图形客户端（Windows）

- 仓库：`fork-dev/fork` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows fork`

### Git Extensions — Git 图形界面 · `gitextensions`

Git Extensions — Git 图形界面

- 仓库：`gitextensions/gitextensions` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows gitextensions`

### Helix（模态终端文本编辑器 · `helix`

Helix（模态终端文本编辑器，Rust）

- 仓库：`helix-editor/helix` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows helix`

### Helix 终端编辑器（Rust） · `helix_editor`

Helix 终端编辑器（Rust）

- 仓库：`helix-editor/helix` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows helix_editor`

### 十六进制编辑器 · `imhex`

十六进制编辑器

- 仓库：`WerWolv/ImHex` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows imhex`

### Rust 编写的代码编辑器 · `lapce`

Rust 编写的代码编辑器

- 仓库：`lapce/lapce` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows lapce`

### Lite XL（轻量 Lua 编辑器 · `lite_xl`

Lite XL（轻量 Lua 编辑器，Windows portable zip）

- 仓库：`lite-xl/lite-xl` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows lite_xl`

### Neovim 编辑器（Windows zip） · `neovim`

Neovim 编辑器（Windows zip）

- 仓库：`neovim/neovim` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows neovim`

### Notepad--（国产轻量跨平台编辑器 · `notepad_minusminus`

Notepad--（国产轻量跨平台编辑器，GPL，便携 zip）

- 仓库：`cxasm/notepad--` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows notepad_minusminus`

### 开源免费代码编辑器 Notepad Next · `notepad_next`

开源免费代码编辑器 Notepad Next 0.14 中文多语免费版

- 仓库：`dail8859/NotepadNext` · 分片：`apps/windows/26-编辑器.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows notepad_next`

### 轻量文本编辑器 · `notepadplusplus`

轻量文本编辑器，x64 安装包

- 仓库：`notepad-plus-plus/notepad-plus-plus` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows notepadplusplus`

### Pulsar（Atom 继任编辑器 · `pulsar`

Pulsar（Atom 继任编辑器，Windows zip）

- 仓库：`pulsar-edit/pulsar` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows pulsar`

### Skylark（C 编写 · `skylark`

Skylark（C 编写，文本/十六进制、便携 7z，GPL）

- 仓库：`adonais/skylark` · 分片：`apps/windows/26-编辑器.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows skylark`

### Sublime Merge Git 客户端 · `sublime_merge`

Sublime Merge Git 客户端

- 仓库：`sublimehq/sublime_merge` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows sublime_merge`

### Visual Studio Code（微软构建） · `vscode`

Visual Studio Code（微软构建）

- 仓库：`microsoft/vscode` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows vscode`

### VS Code 开源构建 · `vscodium`

VS Code 开源构建，无微软遥测

- 仓库：`VSCodium/vscodium` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows vscodium`

### 目录与文件差异对比、合并 · `winmerge`

目录与文件差异对比、合并

- 仓库：`WinMerge/winmerge` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows winmerge`

### Zed（Rust 高性能编辑器 · `zed`

Zed（Rust 高性能编辑器，开源，Windows x64 安装包）

- 仓库：`zed-industries/zed` · 分片：`apps/windows/26-编辑器.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zed`

---

## 网络（21）

### 局域网 IP 扫描 · `angryip`

局域网 IP 扫描

- 仓库：`angryip/ipscan` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows angryip`

### 终端带宽按进程展示 · `bandwhich`

终端带宽按进程展示

- 仓库：`imsnif/bandwhich` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows bandwhich`

### Cloudflare Tunnel 客户端 · `cloudflared`

Cloudflare Tunnel 客户端

- 仓库：`cloudflare/cloudflared` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows cloudflared`

### croc（端到端加密传文件 · `croc`

croc（端到端加密传文件，命令行）

- 仓库：`schollz/croc` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows croc`

### 开源免费网络测试工具 InternetTest Pro · `internettest`

开源免费网络测试工具 InternetTest Pro 9.1.0.2602 中文多语免费版

- 仓库：`Leo-Corporation/InternetTest` · 分片：`apps/windows/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows internettest`

### 局域网跨设备传文件 · `localsend`

局域网跨设备传文件，需同网段

- 仓库：`localsend/localsend` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows localsend`

### NetBird（WireGuard 组网与零信任访问 · `netbird`

NetBird（WireGuard 组网与零信任访问，含桌面 UI）

- 仓库：`netbirdio/netbird` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows netbird`

### Nextcloud 桌面同步客户端 · `nextcloud_desktop`

Nextcloud 桌面同步客户端

- 仓库：`nextcloud/desktop` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows nextcloud_desktop`

### Nmap 网络扫描（Zenmap 安装包名因版本而异） · `nmap`

Nmap 网络扫描（Zenmap 安装包名因版本而异）

- 仓库：`nmap/nmap` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows nmap`

### OpenTrace · `opentrace`

OpenTrace 1.5.0.0 绿色中文版，让网络追踪从未如此简单

- 仓库：`Archeb/opentrace` · 分片：`apps/windows/18-网络.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows opentrace`

### OpenVPN 社区版安装包 · `openvpn`

OpenVPN 社区版安装包

- 仓库：`OpenVPN/openvpn` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openvpn`

### 云存储同步命令行（zip） · `rclone`

云存储同步命令行（zip）

- 仓库：`rclone/rclone` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows rclone`

### Syncthing（P2P 文件同步 · `syncthing`

Syncthing（P2P 文件同步，官方 zip，仅下载）

- 仓库：`syncthing/syncthing` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows syncthing`

### Syncthing 托盘与集成 · `syncthingtray`

Syncthing 托盘与集成

- 仓库：`Martchus/syncthingtray` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows syncthingtray`

### Tailscale 组网客户端（以发布页为准） · `tailscale`

Tailscale 组网客户端（以发布页为准）

- 仓库：`tailscale/tailscale` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows tailscale`

### Thorium 浏览器（Chromium 优化版） · `thorium`

Thorium 浏览器（Chromium 优化版）

- 仓库：`Alex313031/Thorium` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows thorium`

### 网络协议分析（Wireshark） · `wireshark`

网络协议分析（Wireshark）

- 仓库：`wireshark/wireshark` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows wireshark`

### 友好 HTTP 客户端（curl 风格） · `xh`

友好 HTTP 客户端（curl 风格）

- 仓库：`ducaale/xh` · 分片：`apps/windows/18-网络.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows xh`

### Zen 浏览器（Firefox 分支 · `zen_browser`

Zen 浏览器（Firefox 分支，隐私向，Windows x64 安装包）

- 仓库：`zen-browser/desktop` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zen_browser`

### Zen 浏览器（Firefox 分支 · `zen_browser_arm64`

Zen 浏览器（Firefox 分支，Windows ARM64 安装包）

- 仓库：`zen-browser/desktop` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zen_browser_arm64`

### ZeroTier 虚拟组网 · `zerotier`

ZeroTier 虚拟组网

- 仓库：`zerotier/ZeroTierOne` · 分片：`apps/windows/18-网络.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zerotier`

---

## 网络与协作（4）

### Ferdium（聚合 Slack/Discord/Matrix 等服务的桌面端 · `ferdium`

Ferdium（聚合 Slack/Discord/Matrix 等服务的桌面端，原 Ferdi 分支）

- 仓库：`ferdium/ferdium-app` · 分片：`apps/windows/19-网络与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows ferdium`

### Mattermost 桌面客户端 · `mattermost_desktop`

Mattermost 桌面客户端

- 仓库：`mattermost/desktop` · 分片：`apps/windows/19-网络与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows mattermost_desktop`

### Rocket.Chat 桌面客户端（Electron） · `rocketchat_desktop`

Rocket.Chat 桌面客户端（Electron）

- 仓库：`RocketChat/Rocket.Chat.Electron` · 分片：`apps/windows/19-网络与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rocketchat_desktop`

### Zulip 桌面客户端 · `zulip_desktop`

Zulip 桌面客户端

- 仓库：`zulip/zulip-desktop` · 分片：`apps/windows/19-网络与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows zulip_desktop`

---

## 网络与通讯（6）

### Twitch 聊天客户端 Chatterino · `chatterino`

Twitch 聊天客户端 Chatterino

- 仓库：`Chatterino/chatterino2` · 分片：`apps/windows/20-网络与通讯.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows chatterino`

### Element 去中心化聊天（Matrix） · `element_desktop`

Element 去中心化聊天（Matrix）

- 仓库：`element-hq/element-desktop` · 分片：`apps/windows/20-网络与通讯.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows element_desktop`

### Signal 端到端加密通讯 · `signal_desktop`

Signal 端到端加密通讯

- 仓库：`signalapp/Signal-Desktop` · 分片：`apps/windows/20-网络与通讯.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows signal_desktop`

### Telegram 桌面客户端 · `telegram`

Telegram 桌面客户端

- 仓库：`telegramdesktop/tdesktop` · 分片：`apps/windows/20-网络与通讯.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows telegram`

### Mozilla Thunderbird 邮件客户端 · `thunderbird`

Mozilla Thunderbird 邮件客户端

- 仓库：`thunderbird/thunderbird` · 分片：`apps/windows/20-网络与通讯.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows thunderbird`

### 开源免费雷鸟邮件客户端 Mozilla Thunderbird · `thunderbird_2`

开源免费雷鸟邮件客户端 Mozilla Thunderbird 151.0 + x64 中文多语免费版

- 仓库：`mozilla/kitsune` · 分片：`apps/windows/20-网络与通讯.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows thunderbird_2`

---

## 远程与协作（5）

### Barrier（开源 KVM：一套键鼠控制多台电脑） · `barrier`

Barrier（开源 KVM：一套键鼠控制多台电脑）

- 仓库：`debauchee/barrier` · 分片：`apps/windows/21-远程与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows barrier`

### Deskreen（将本机屏幕无线投到浏览器 · `deskreen`

Deskreen（将本机屏幕无线投到浏览器，第二屏/演示）

- 仓库：`pavlobu/deskreen` · 分片：`apps/windows/21-远程与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows deskreen`

### 开源远程控制和屏幕镜像工具 Escrcpy · `escrcpy`

开源远程控制和屏幕镜像工具 Escrcpy 2.11.1 中文免费版

- 仓库：`viarotel-org/escrcpy` · 分片：`apps/windows/21-远程与协作.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows escrcpy`

### 多协议远程桌面管理 · `mremoteng`

多协议远程桌面管理

- 仓库：`mRemoteNG/mRemoteNG` · 分片：`apps/windows/21-远程与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows mremoteng`

### 开源远程桌面 · `rustdesk`

开源远程桌面，可自建中继

- 仓库：`rustdesk/rustdesk` · 分片：`apps/windows/21-远程与协作.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows rustdesk`

---

## 金融与股票（5）

### Actual Budget（开源个人/家庭预算与银行同步风格记账 · `actual_budget`

Actual Budget（开源个人/家庭预算与银行同步风格记账，E2E 加密）

- 仓库：`actualbudget/actual` · 分片：`apps/windows/27-金融与股票.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows actual_budget`

### FreqUI（Freqtrade 配套 Web 监控/交易界面发行包 zip） · `frequi`

FreqUI（Freqtrade 配套 Web 监控/交易界面发行包 zip）

- 仓库：`freqtrade/frequi` · 分片：`apps/windows/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows frequi`

### go-stock（Wails：A股/港股/美股行情、AI 分析与选股辅助；数据偏本地 · `go_stock`

go-stock（Wails：A股/港股/美股行情、AI 分析与选股辅助；数据偏本地。仅供学习研究，投资有风险）

- 仓库：`ArvinLovegood/go-stock` · 分片：`apps/windows/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows go_stock`

### OpenBB Open Data Platform（桌面端：金融/投研数据与工具链入口） · `openbb_desktop`

OpenBB Open Data Platform（桌面端：金融/投研数据与工具链入口）

- 仓库：`OpenBB-finance/OpenBB` · 分片：`apps/windows/27-金融与股票.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openbb_desktop`

### TA-Lib（技术分析 C 库；Windows x86_64 官方 zip · `ta_lib`

TA-Lib（技术分析 C 库；Windows x86_64 官方 zip，量化/指标常用）

- 仓库：`ta-lib/ta-lib` · 分片：`apps/windows/27-金融与股票.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows ta_lib`

---

## 音视频（7）

### LosslessCut（无损裁剪/合并视频音频 · `losslesscut`

LosslessCut（无损裁剪/合并视频音频，Windows 便携版）

- 仓库：`mifi/lossless-cut` · 分片：`apps/windows/22-音视频.json` · 配置：已配匹配规则
- 查找：`lookup_app.bat --platform windows losslesscut`

### OpenShot 视频编辑器（Windows x64 exe） · `openshot`

OpenShot 视频编辑器（Windows x64 exe）

- 仓库：`OpenShot/openshot-qt` · 分片：`apps/windows/22-音视频.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows openshot`

### 开源免费多功能视频编辑下载工具 QuickCut · `quickcut`

开源免费多功能视频编辑下载工具 QuickCut 1.6.10 中文免费版

- 仓库：`HaujetZhao/QuickCut` · 分片：`apps/windows/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows quickcut`

### 开源免费 Gif 录制工具 ScreenToGif · `screen_to_gif`

开源免费 Gif 录制工具 ScreenToGif 2.43.1 中文多语免费版

- 仓库：`NickeManarin/ScreenToGif` · 分片：`apps/windows/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows screen_to_gif`

### 开源 Windows 桌面录像工具 Simple Screen Recorder · `simple_screen_recorder`

开源 Windows 桌面录像工具 Simple Screen Recorder 1.3.4 中文多语免费版

- 仓库：`lextrack/Simple-Screen-Recorder` · 分片：`apps/windows/22-音视频.json` · 配置：基础条目（试跑前建议补规则）
- 查找：`lookup_app.bat --platform windows simple_screen_recorder`

### Syncplay（异地同步播放本地视频 · `syncplay`

Syncplay（异地同步播放本地视频，连麦追剧）

- 仓库：`Syncplay/syncplay` · 分片：`apps/windows/22-音视频.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows syncplay`

### VidCutter（基于 mpv 的视频剪切/合并） · `vidcutter`

VidCutter（基于 mpv 的视频剪切/合并）

- 仓库：`ozmartian/vidcutter` · 分片：`apps/windows/22-音视频.json` · 配置：规则较完整
- 查找：`lookup_app.bat --platform windows vidcutter`

---
