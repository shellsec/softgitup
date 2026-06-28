# SoftGitUp - Daily Tools Cloud Update Sync System

中文 | [English](README_EN.md)

## ☕ Buy Me a Coke

Open source is hard — tips are welcome:  
👉 [Afdian / 爱发电](https://ifdian.net/a/shellsec)

A tool system for managing local software directories and automatically syncing updates, supporting GitHub and GitLab cloud storage, with Git accelerated downloads.

For the latest curated software list and notes, see [`Lastb_soft_version.txt`](Lastb_soft_version.txt).

<!-- SOFTWARE_SIZE_START -->
> 📦 **`software/` size stats** (auto-refreshed by `generate_and_push.bat`):
> **21** packages, **4,781** files, **1.62 GB** total; generated at 2026-06-28 15:09.
> Top 5 by size: system_good (677.5 MB), PotPlayer (263.1 MB), UltraEdit (198.3 MB), gh-release-fetch (88.2 MB), notepad++ (72.9 MB).
<!-- SOFTWARE_SIZE_END -->

**Maintainer page check** (optional — `software/` works fine without updates): see [`soft_page_check/`](soft_page_check/README.md). Run `monthly_sop.bat` to compare page titles; update and publish only when you confirm changes.

This toolkit is built around **information security and reducing data leakage**, aiming to minimize cloud reporting, behavioral tracking, and algorithmic data harvesting where practical.

### Software list and privacy posture (cross-check with `Lastb_soft_version.txt`)

The following is a **self-check summary** of choices in that list, useful when comparing notes with others (e.g. colleagues or other assistants). It is **not** a precise measurement of “how much data leaks” and is **not** legal or compliance advice.

**Directions that usually align well with the list**

- **Screenshot OCR**: The list warns that WeChat / QQ / “PC manager” style **active OCR** often goes to the cloud; **PixPin offline OCR** matches the recommended approach.
- **Input method**: Dropping Sogou-type IMEs for **Weasel + rime-ice (Rime)** and other local open-source stacks matches the list.
- **System-wide blocking**: **Zen** (system proxy) + **AdGuard DNS / 18bit DNS** (batch scripts under `system_good`) + **uBlock Origin** and **Privacy Badger** in the browser matches the list—a layered setup.
- **Bloat and updates**: **Win11Debloat**, **StopUpdates10**, **StartAllBack**, **HiBit Startup** in the list help cut preinstalled apps and startup noise (exact effect depends on your choices).
- **Clipboard**: **Ditto** and similar local history tools fit the “avoid cloud clipboard sync” idea.
- **Local AI**: **Ollama** and other on-device models reduce sending sensitive content through web LLMs (still mind model provenance and disk security).
- **Player / viewer / archives**: PotPlayer, XnView MP, 7-Zip, WinRAR fit a “keep common tasks local” posture.

**Objective upload or trust boundaries still present in the list**

- **Official Chrome**: Sync, crash reports, prediction services, **Enhanced Safe Browsing**, etc. send more to Google; consider turning off sync and usage reporting and using **Standard** (not Enhanced) Safe Browsing where appropriate (see Chrome settings and Google’s documentation).
- **P2P (Thunder / BitComet / qBittorrent, etc.)**: The protocol uploads while seeding; repacked / “enhanced” builds also mean **trusting the repacker**, not only the upstream project.
- **LX Music**: The desktop client is relatively transparent (open source), but **custom JS sources** call third-party music APIs—**IP, search terms**, etc. may be visible to those endpoints; avoid sensitive searches in high-risk contexts.
- **Microsoft Defender**: Even with **DefenderUI** tuning, cloud sample submission and threat telemetry may still occur per Microsoft policy.
- **Registered, repacked, or site-modified builds**: Included for day-to-day utility; from a **supply-chain** perspective they differ from “official signed builds only”—trade-offs are yours.

**Windows / hardware areas not spelled out end-to-end in the long doc**

- **Diagnostics / telemetry, advertising ID, activity history, location, OneDrive / account sync** need explicit review under **Settings → Privacy & security** (and related pages).
- **GPU suites** (e.g. GeForce Experience bundled with NVIDIA installers) often collect usage stats; prefer **driver-only** installs or disable data collection where offered.
- **.NET, WebView2, VC++ runtimes** check for updates on their own schedules; the list mentions these components—pair with firewall / update policy review if you are privacy-sensitive.

**Bottom line**: As a practice of **local-first tooling, less big-tech cloud OCR/IME, plus system and DNS filtering**, this stack **often reduces** casual side channels and behavioral reporting versus a default PC setup—but there is **no** provable “percentage cap” or **zero-upload** guarantee. High-sensitivity environments should add **Group Policy, egress monitoring, and official-trusted binaries** as needed.

## Features

### 🚀 Core Features
- **Local Software Management**: Scan local software directories, generate file indexes and version lists
- **Cloud Sync**: Automatically push to GitHub or GitLab, support Git accelerated downloads
- **Multi-Platform Support**: Support GitHub and GitLab, flexible switching
- **Smart Updates**: Compare based on file modification time, only download changed files
- **Automatic Process Management**: Automatically close related processes before update, automatically start specified programs after update
- **Windows Service Support**: Automatically identify and start Windows services (e.g., NetTime service)
- **Multi-Program Launch**: Support launching multiple programs simultaneously (e.g., main program and service program)
- **Update Order Control**: Update software according to configuration file order, ensuring dependency relationships
- **System Tray**: Run in background, support system tray icon and silent updates
- **Cross-Platform**: Support Windows, Linux, macOS
- **Complete Sync**: Full-featured sync tool with automatic process management
- **Out-of-the-Box**: Ready-to-use registered/cracked versions, keep updated versions daily, virus-scanned

### 📦 Supported Software
- **Text Editors**: Notepad++, notepad-, SublimeText, EditPlus, EmEditor (large files 16T), UltraEdit

- **System Tools**: CCleaner, WiseCare365, Everything, WinMemoryCleaner, CrystalDiskInfo, NetTime (see the [CCleaner vs WiseCare365 vs PC Fresh comparison](CCleanerPro_vs_WiseCare365Pro_vs_PCFresh.txt), Chinese)

- **Compression Tools**: WinRAR, 7-Zip, excellent image viewer XnViewMP

- **Uninstall & Data Recovery**: GeekUninstaller (single portable exe; fast, removes leftovers, handles built-in Windows apps), DiskGenius (partition management / deleted-file recovery) — both under `system_good/`

- **Startup Management**: HiBit Startup Manager, duplicate file finder Duplicate Cleaner Pro

- **System Optimization**: system_good directory contains multiple system tools
  - Driver Management: Driver Talent (overseas version)
  - System Optimization: Start menu StartBackAIO supports all Windows versions, disable patch updates, KMS activation, disable built-in antivirus
  - Utility Tools: Ditto clipboard, DuplicateCleaner duplicate file cleanup, Putty, MobaXterm, SmartDefrag disk defragmentation, PC Fresh performance tuning, WizTree disk space analyzer, PasteEx clipboard-to-file, etc.
  - File Server: [copyparty](https://github.com/9001/copyparty) - Local self-hosted sync, Web file server, open source secure, multi-platform support
  - DNS Configuration Tools: One-click encrypted DNS (DoH) configuration
    - `Configure_AdGuard_DNS.bat` - Configure AdGuard DNS (free, blocks ads, trackers, malicious websites)  
    - `Configure_18bit_DNS.bat` - Configure 18bit encrypted DNS (blocks ads, malicious websites)
    - `Restore_Default_DNS.bat` - Restore default DNS settings (automatic)
  - Taskbar / desktop shortcuts (Win10/Win11, no admin, adaptive paths)
    - `Pin_system_good_to_taskbar.bat` - Pin apps to the taskbar (default: system_good + sibling apps; see `Pin_taskbar_targets.json`)
    - `Create_desktop_shortcuts.bat` - Create desktop `.lnk` files for the same list
    - When deployed under `D:\Program Files\system_good`, resolves exes under `D:\Program Files\` (e.g. `notepad++`, `everything`)

- **GitHub Releases (on-demand)**: `software/githubwindowntools/` ships a standalone Python workflow driven by `apps.json` to resolve versions from GitHub Releases and download installers (Windows / macOS / Linux blocks in config). On Windows, run `run_update.bat`. Full steps: [githubwindowntools README](software/githubwindowntools/README.md) (Chinese). The folder is listed under `software_dirs` in `config.json` so the main sync tool can pull it with the rest.

- **More Software**: Easy to extend support, post if you need others

### 🚀 Quick One-Click Sync (No Python Environment Required)
Tested on Windows 10-11, Windows Server permission issues

  - **Download config.json, sync_software.exe**

  - **Modify the path in config.json, run sync_software.exe, and you can use it to automatically update all software to the latest version

### 🚀 Quick One-Click Sync (Python Environment Required)
Tested on Windows Server + Windows 10-11

  - **Download config.json, sync_software.py, sync_software.bat

  - **Modify the path in config.json, run sync_software.bat, and you can use it

## Project Structure

```
softgitup/
├── config.json              # Configuration file
├── soft_manager.py          # Local management tool
├── soft_sync.py            # Sync tool (GUI version)
├── sync_software.py        # Complete sync tool (command line, recommended)
├── build_exe.py            # Build script
├── generate_and_push.bat   # Generate list.txt and push
├── soft_page_check/        # Page title health check (see README)
│   ├── monthly_sop.bat     # Monthly SOP entry (recommended)
│   ├── monthly_check.bat   # Tier-A quick check (~42 pages)
│   └── monthly_check_full.bat  # Quarterly full check
├── software/               # Local software directory
│   ├── CCleaner/
│   ├── EditPlus/
│   ├── everything/
│   ├── notepad++/
│   ├── SublimeText/
│   ├── githubwindowntools/   # GitHub Releases on-demand downloader (auto_update.py, apps.json)
│   └── ...
├── logs/                   # Log directory
└── README.md              # Project documentation
```

## Quick Start

### 1. Requirements
- Python 3.7+
- Git
- Network connection

### 2. Install Dependencies
```bash
pip install requests PyQt5 gitpython
```

### 3. Configuration

#### GitHub Configuration (Default)
Edit the `config.json` file:
```json
{
  "git_platform": "github",
  "github_repo": "https://github.com/shellsec/softgitup",
  "gitlab_repo": "https://gitlab.com/your-username/softgitup",
  "manager_base_path": "./software",
  "sync_base_path": "",
  "sync_time": "07:00",
  "auto_start": true,
  "auto_kill": true,
  "git_mirrors": [
    "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
  ],
  "process_map": {
    "notepad++": ["notepad++.exe"],
    "NetTime": ["NetTime.exe", "NetTimeService.exe"]
  },
  "start_map": {
    "notepad++": "notepad++.exe",
    "NetTime": ["NetTimeService.exe", "NetTime.exe"]
  },
  "service_map": {
    "NetTimeService.exe": "NetTimeSvc"
  },
  "start_after_update": [
    "NetTime",
    "everything",
    "WinMemoryCleaner"
  ]
}
```

### 4. Use Complete Sync Tool (Recommended)

**Method 1: Use Compiled Executable (No Python Environment)** ⭐⭐⭐⭐⭐
```bash
# Run the compiled exe file directly
sync_software.exe
```
**Advantages**:
- ✅ No Python installation required
- ✅ Small file size (5-15 MB)
- ✅ Fast startup
- ✅ Better performance
- ✅ Single file deployment

**Method 2: Use Python Script**
```bash
# Use complete sync tool (command line)
python sync_software.py

# Or use batch file (no Python environment required)
一键快速同步.bat
```

### 5. Use Management Tool
```bash
# Scan local software and push to GitHub
python soft_manager.py

# Or use batch file for one-click operation
generate_and_push.bat
```

### 6. Use GUI Sync Tool
```bash
# Start GUI sync tool (system tray)
python soft_sync.py
```

## Build and Compile

### Compile to Executable
Use PyInstaller to package Python programs into executable files:

```bash
# Use build_exe.py script to package
python build_exe.py
```

Build script provides multiple options:
1. **Build All Programs** (Recommended) - Includes GUI and console versions
2. **Build Console Version Only** - No GUI dependencies, avoid PyQt5 DLL issues
3. **Build GUI Version Only** - Includes complete GUI functionality
4. **Clean Build Files** - Clean temporary files

### Direct PyInstaller Compilation
You can also use PyInstaller directly to compile `sync_software.py`:

```bash
# Basic compilation
pyinstaller --onefile --name=sync_software sync_software.py

# Optimized compilation (recommended)
pyinstaller --onefile --name=sync_software --clean --noconfirm sync_software.py
```

**Generated Files**:
- `dist/sync_software.exe` - Compiled executable file

### Generated Executable Files
- `sync_software.exe` - Complete sync tool (console, recommended)
- `SoftGitUp_Workflow.exe` - Workflow tool (console)
- `SoftGitUp_Manager.exe` - Management tool (GUI)
- `SoftGitUp_Sync.exe` - Sync tool (GUI, system tray)
- `SoftGitUp_Sync_Simple.exe` - Simplified sync tool (console)

### Solve PyQt5 DLL Issues
If you encounter `ImportError: DLL load failed while importing QtWidgets` error:

**Solution 1: Use Nuitka Compilation (Recommended)** ⭐⭐⭐⭐⭐
```bash
# Compile to native C++ code, no Python or DLL needed
python -m nuitka --standalone --onefile --windows-console-mode=disable --output-dir=dist sync_software.py
```
**Advantages**:
- Smaller file size (5-15 MB)
- No DLL dependencies
- Fast startup
- Better performance

**Solution 2: Use Console Version**
```bash
# Select option 2, build console version
python build_exe.py
# Use the generated SoftGitUp_Sync_Simple.exe
```

**Solution 3: Use Python Script**
```bash
# Run Python scripts directly to avoid packaging issues
python sync_software.py
```

**Solution 4: Install Visual C++ Redistributable**
- Download and install Microsoft Visual C++ Redistributable
- Recompile GUI version
- `SoftGitUp_Workflow.exe` - Workflow tool (console)
- `SoftGitUp_Manager.exe` - Management tool (GUI)
- `SoftGitUp_Sync.exe` - Sync tool (GUI, system tray)
- `SoftGitUp_Sync_Simple.exe` - Simplified sync tool (console)

## Workflow

### Maintainer: check → update → publish

**Principle**: Clients can keep using `software/` without monthly updates. Title changes are hints only — confirm before downloading.

| When | Action | Notes |
|------|--------|-------|
| **~Monthly** | [`soft_page_check/monthly_sop.bat`](soft_page_check/monthly_sop.bat) option `[1]` | Tier-A quick check + guided steps; or `monthly_check.bat` only |
| **~Quarterly** | [`soft_page_check/monthly_check_full.bat`](soft_page_check/monthly_check_full.bat) **twice** | Full report: A + install list + 423down + 7xiazai + list sites |
| **List sites (optional)** | [`soft_page_check/monthly_check_list.bat`](soft_page_check/monthly_check_list.bat) | hybase / dayanzai / down66 only (`list/*_urls.txt`) |
| **If changed** | Open `soft_page_check/reports/index.html` | Cracked / mirror / cloud links — download manually |
| **To update** | Replace under `software/` | GitHub apps: `software/gh-release-fetch/run_update.bat` |
| **Publish** | `generate_and_push.bat` at repo root | Regenerates `list.txt` and pushes |
| **Optional** | Edit `Lastb_soft_version.txt` | Install notes or digest summary |

Each monitor scope needs **two consecutive runs** before “title changed” appears. Details: [soft_page_check README](soft_page_check/README.md) (Chinese).

### Client: pull updates

```bash
python sync_software.py
# or sync_software.exe / 一键快速同步.bat
```

### Legacy publish (skip page check)

1. Place new files under `software/`
2. Run `generate_and_push.bat`
3. Run `sync_software.bat` / `sync_software.exe` on each client

## Configuration

### Configuration File (config.json)

#### Basic Configuration

| Configuration Item | Description | Default Value |
|--------|------|--------|
| `git_platform` | Git platform type | `"github"` or `"gitlab"` |
| `github_repo` | GitHub repository address | - |
| `gitlab_repo` | GitLab repository address | - |
| `manager_base_path` | Management tool scan directory | `./software` |
| `sync_base_path` | Sync tool download directory (empty uses project root) | `""` (empty string) |
| `sync_time` | Auto sync time | `07:00` |
| `git_mirrors` | Git mirror source list | - |
| `download_timeout` | Download timeout (seconds) | `30` |
| `retry_times` | Retry times | `3` |
| `retry_delay` | Retry delay (seconds) | `5` |
| `log_level` | Log level | `INFO` |
| `check_interval` | Check interval (seconds) | `3600` |

#### Automatic Process Management Configuration

| Configuration Item | Description | Default Value |
|--------|------|--------|
| `auto_kill` | Automatically close related processes before update | `true` |
| `auto_start` | Automatically start programs after update | `true` |
| `process_map` | Process mapping table, defines process names for each software | `{}` |
| `start_map` | Startup path mapping table, defines startup paths for each software (supports arrays) | `{}` |
| `service_map` | Service mapping table, maps service programs to Windows service names | `{}` |
| `start_after_update` | List of programs to automatically start after update | `[]` |
| `software_dirs` | Software directory mapping, controls update order | `{}` |

#### Process Mapping Configuration Example

`process_map` is used to define processes that need to be closed during update, supports multiple processes:
```json
{
  "process_map": {
    "notepad++": ["notepad++.exe"],
    "NetTime": ["NetTime.exe", "NetTimeService.exe"],
    "UltraEdit": ["uedit64.exe", "uedit32.exe"],
    "system_good": ["putty.exe", "SmartDefrag-Pro.exe", "Ditto.exe"]
  }
}
```

#### Startup Path Configuration Example

`start_map` supports single program or multiple program startup:

1. **Single Program** (string):
   ```json
   {
     "start_map": {
       "notepad++": "notepad++.exe"
     }
   }
   ```

2. **Multiple Programs** (array): Start in order
   ```json
   {
     "start_map": {
       "NetTime": ["NetTimeService.exe", "NetTime.exe"]
     }
   }
   ```

3. **Path Format**:
   - **Relative Path** (recommended): Relative to software directory
     ```json
     "NetTime": "NetTime.exe"                    // D:\Program Files\NetTime\NetTime.exe
     "NetTime": "bin/NetTime.exe"                // D:\Program Files\NetTime\bin\NetTime.exe
     ```
   - **Absolute Path**: Full path
     ```json
     "some_app": "C:/OtherPath/app.exe"          // Full absolute path
     ```

#### Windows Service Configuration Example

`service_map` is used to map service programs to Windows service names. The system will automatically use `net start` to start services:

```json
{
  "service_map": {
    "NetTimeService.exe": "NetTimeSvc",
    "Everything.exe": "Everything"              // If Everything is installed as a service
  }
}
```

**How it works**:
- If a program is in `service_map`, the system will use `net start [service name]` to start the service
- If a program is not in `service_map`, the system will directly run the program file
- Supports detection of services already running

#### Auto-Start After Update Configuration

`start_after_update` defines programs that need to be automatically started after update completion:
```json
{
  "start_after_update": [
    "NetTime",
    "everything",
    "WinMemoryCleaner",
    "notepad++"
  ]
}
```

**Note**:
- If `start_after_update` is an empty array `[]`, all software will automatically start after update (when `auto_start: true`)
- If `start_after_update` has values, only software in the list will automatically start after update

#### Update Order Control

Software update order is determined by the order in `software_dirs` in `config.json`:

```json
{
  "software_dirs": {
    "WinMemoryCleaner": "WinMemoryCleaner",      // First update
    "NetTime": "NetTime",                        // Second update
    "system_good": "system_good"                 // Last update
  }
}
```

**How it works**:
- System updates software sequentially according to the order configured in `software_dirs`
- If software exists in remote list but not configured in `software_dirs`, it will be updated last according to remote list order
- You can control update priority by adjusting the order in `software_dirs`

#### Sync Path Configuration

`sync_base_path` supports two configuration methods:

1. **Auto-use project root directory** (Recommended):
   ```json
   "sync_base_path": ""
   ```
   - When configured as empty string, software will be downloaded to project root directory
   - Example: `E:\GITHUB\softgitup\NetTime\`, `E:\GITHUB\softgitup\everything\`
   - Advantages: No administrator privileges required, easy to manage, easy to backup and migrate

2. **Specify custom path**:
   ```json
   "sync_base_path": "D:/Program Files"
   ```
   - Software will be downloaded to specified directory
   - Example: `D:\Program Files\NetTime\`, `D:\Program Files\everything\`
   - Note: If directory doesn't exist, system will automatically create it

### Git Acceleration Source Configuration
Use `gh-proxy.com` as Git accelerated download source:
```json
"git_mirrors": [
  "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
]
```

## GitLab Deployment Guide

### Why Choose GitLab?

1. **Enterprise Deployment**: Supports private deployment, suitable for intranet environments
2. **Domestic Access**: GitLab.com or self-hosted instances, more stable access
3. **Rich Features**: Built-in CI/CD, project management and other enterprise features
4. **Data Security**: Complete control over data storage location

### GitLab Deployment Steps

#### 1. Create GitLab Repository

1. Log in to GitLab (GitLab.com or self-hosted instance)
2. Create a new project
3. Push code to GitLab repository

```bash
git remote add gitlab https://gitlab.com/your-username/softgitup.git
git push gitlab master
```

#### 2. Configure config.json

Edit `config.json` file:

```json
{
  "git_platform": "gitlab",
  "gitlab_repo": "https://gitlab.com/your-username/softgitup",
  "git_mirrors": [
    "https://gitlab.com/your-username/softgitup/-/raw/master"
  ]
}
```

**Important Configuration Items:**
- `git_platform`: Set to `"gitlab"`
- `gitlab_repo`: Fill in your GitLab repository address
- `git_mirrors`: GitLab Raw file URL format: `https://gitlab.com/user/repo/-/raw/branch`

#### 3. Verify Configuration

Run sync test:

```bash
python sync_software.py
```

Or use batch file:

```bash
一键快速同步.bat
```

#### 4. Switch Back to GitHub

If you need to switch back to GitHub, just modify `git_platform`:

```json
{
  "git_platform": "github",
  "github_repo": "https://github.com/shellsec/softgitup",
  "git_mirrors": [
    "https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup"
  ]
}
```

### Self-Hosted GitLab Instance Deployment

If you have a self-hosted GitLab instance:

1. **Configure Repository Address**:
```json
{
  "git_platform": "gitlab",
  "gitlab_repo": "https://your-gitlab-instance.com/your-username/softgitup",
  "git_mirrors": [
    "https://your-gitlab-instance.com/your-username/softgitup/-/raw/master"
  ]
}
```

2. **Private Repository Access**:
   - If the repository is private, you need to create a Personal Access Token in GitLab
   - Include token in URL: `https://oauth2:YOUR_TOKEN@your-gitlab-instance.com/user/repo/-/raw/master`

3. **Branch Configuration**:
   - GitLab default branch may be `master` or `main`
   - Ensure branch name in `git_mirrors` matches actual branch name

### Common Questions

**Q: Can GitLab and GitHub be used simultaneously?**
A: Yes, configure mirror sources for both platforms in `git_mirrors`, system will try in order.

**Q: How to know which platform is currently being used?**
A: Check log files, they will show the mirror source URL being used.

**Q: How to configure GitLab private repository?**
A: Include access token in URL, or use GitLab's Deploy Token.

## Use Cases

### Personal Users
- Sync common software across multiple devices
- Automatically update software to latest version
- Backup software configurations and settings

### Enterprise Environment
- Unified management of employee common software
- Batch deployment and software updates
- Software version control and rollback

### Developers
- Manage development environment tools
- Quickly set up development environment
- Toolchain version management

## Advanced Features

### Automatic Process Management

The system supports automatically closing related processes before update and automatically starting programs after update:

1. **Close Processes Before Update**:
   - When `auto_kill: true`, the system will automatically close processes defined in `process_map` before downloading files
   - Supports closing multiple processes (e.g., NetTime main program and service program)
   - Uses Windows `taskkill` command to force close processes

2. **Start Programs After Update**:
   - When `auto_start: true`, the system will automatically start programs after file update completion
   - Determines which programs to start based on `start_after_update` list
   - Supports single program or multiple program startup (array configuration)
   - Supports relative path and absolute path configuration
   - Automatically identifies Windows services and uses `net start` to start

3. **Windows Service Support**:
   - Automatically detects if a program is in `service_map`
   - If it's a service, uses `net start [service name]` to start
   - If it's a regular program, directly runs the executable file
   - Supports detection of services already running

4. **Update Order Control**:
   - Updates according to the order in `config.json` `software_dirs`
   - Ensures software with dependency relationships are updated in correct order

5. **Workflow**:
   ```
   Start sync → In order of software_dirs → Check auto_kill → Close related processes → 
   Download update files → Check auto_start → Check start_after_update → 
   Check service_map → Start service or program
   ```

### Single Software Update
```bash
# Update only specific software
python -c "from soft_manager import SoftManager; SoftManager().generate_list_file('everything')"
```

### Scheduled Sync
- Support custom sync time
- Background silent updates
- System tray notifications
- Automatic process management

### Log Management
- Detailed sync logs
- Error tracking and debugging
- Configurable log levels
- Process close and startup log records

## Troubleshooting

### Common Issues

**Q: How to use the version without Python environment?**
A: Use the PyInstaller compiled `sync_software.exe`:
1. Run directly: `sync_software.exe`
2. Advantages: No Python installation, single file deployment, easy to use
3. Download: Get the compiled exe file from the project release page

**Q: How to compile sync_software.exe?**
A: Use PyInstaller compilation:
```bash
# Use build_exe.py script to package
python build_exe.py
# Select option 2: Build console version only

# Or use PyInstaller directly
pyinstaller --onefile --name=sync_software --clean --noconfirm sync_software.py
```

**Q: After compilation, running reports error "DLL load failed while importing QtWidgets"?**
A: This is a PyQt5 DLL dependency issue. Suggestions:
1. Use console version: `python build_exe.py` select option 2
2. Run Python scripts directly: `python sync_software.py`
3. Or use batch file: `一键快速同步.bat` (no Python environment required)
4. Install Visual C++ Redistributable and recompile

**Q: What to do if sync fails?**
A: Check network connection and GitHub repository permissions, ensure using correct Git acceleration source.

**Q: File modification time doesn't match?**
A: This is usually because file content has changed. The system will automatically download the latest version.

**Q: How to add new software?**
A: Place software in software directory, add software name in config.json, then run management tool.

**Q: How to configure automatic process closing and program startup?**
A: Configure in config.json:
1. Set `auto_kill: true` and `auto_start: true`
2. Add process names corresponding to software in `process_map`
3. Add software startup paths in `start_map` (supports relative and absolute paths)
4. Add program names that need automatic startup in `start_after_update`

**Q: How to configure startup paths?**
A: Supports two methods:
- Relative path: `"NetTime": "NetTime.exe"` or `"NetTime": "bin/NetTime.exe"`
- Absolute path: `"some_app": "C:/Path/app.exe"`

**Q: system_good contains multiple programs, how to configure?**
A: Add all process names that need to be closed in the `system_good` array in `process_map`:
```json
"system_good": ["putty.exe", "SmartDefrag-Pro.exe", "Ditto.exe", ...]
```

**Q: How to start multiple programs?**
A: Use array configuration in `start_map`:
```json
"NetTime": ["NetTimeService.exe", "NetTime.exe"]
```
The system will start programs sequentially in array order.

**Q: How to configure Windows services?**
A: Configure service program to service name mapping in `service_map`:
```json
"service_map": {
  "NetTimeService.exe": "NetTimeSvc"
}
```
The system will automatically use `net start` command to start the service.

**Q: How to control software update order?**
A: Adjust the order in `software_dirs` in `config.json`. The system will update software sequentially according to the configured order.

**Q: What to do if service startup fails?**
A: Ensure the service is installed. You can install the service through:
- Use the installation script provided by the software (e.g., NetTime's `ChangeNetTimePath.bat`)
- Or manually use `sc create` command to install the service

**Q: How to use DNS configuration scripts?**
A: Three DNS configuration scripts are provided in the system_good directory:
- `Configure_18bit_DNS.bat` - Configure 18bit encrypted DNS (blocks ads, malicious websites)
- `Configure_AdGuard_DNS.bat` - Configure AdGuard DNS (free, blocks ads, trackers)
- `Restore_Default_DNS.bat` - Restore default DNS settings
Usage: Right-click the script and select "Run as administrator". After configuration, verify in system settings that DNS shows "Encrypted".

**Q: DoH not effective after DNS configuration?**
A: If DoH is not effective after configuration, try:
1. Restart network adapter (disable and re-enable)
2. Manually enable DoH in system settings:
   - Settings → Network & Internet → Ethernet (or WLAN) → Hardware properties → DNS server assignment
   - Set "Preferred DNS encryption" and "Alternate DNS encryption" to "On (manual template)"
3. Restart computer
4. Some Windows 11 versions may require manual DoH configuration through system settings

**Q: How to pin apps to the taskbar or create desktop shortcuts in one click?**
A: Scripts live in `software/system_good/` (or your synced `system_good` folder) and share `Pin_taskbar_targets.json`:

| Script | Purpose |
|--------|---------|
| `Pin_system_good_to_taskbar.bat` | Pin to taskbar |
| `Create_desktop_shortcuts.bat` | Create desktop shortcuts |

**Adaptive paths**: If the script is in `…\system_good\`, the software root is its **parent** (e.g. `D:\Program Files`). Missing exes are skipped without aborting.

**Default set (no extra flags)**:

- **system_good**: PuTTY, VirtualDesktopSwitcher, WindowsBatchScriptManager, MediaManage, Keyvol  
- **Sibling folders**: Notepad++, Notepad--, Everything, Sublime Text, EditPlus, CCleaner, 7-Zip, WinRAR, UltraEdit, CrystalDiskInfo, WinMemoryCleaner, NetTime, HiBit Startup Manager, PotPlayer  

**Optional flags**: `-IncludeOptional` (Ditto, StartBack), `-IncludeMaintenance` (SmartDefrag-Pro); for taskbar only: `-RestartExplorer`, `-PinMode FolderOnly`.

Edit `Pin_taskbar_targets.json` → `groups.default.targets` to change the default list.

**Q: Where are software downloaded when sync_base_path is empty?**
A: When `sync_base_path` is configured as empty string `""`, software will be downloaded to project root directory (script location). For example:
- Project is at `E:\GITHUB\softgitup\`
- Software will be downloaded to `E:\GITHUB\softgitup\NetTime\`, `E:\GITHUB\softgitup\everything\`, etc.
- Advantages: No administrator privileges required, easy to manage

**Q: How to specify software download to other directory?**
A: Configure `sync_base_path` in `config.json`:
```json
"sync_base_path": "D:/Program Files"
```
Software will be downloaded to specified directory, and the directory will be created automatically if it doesn't exist.

### View Logs
```bash
# View management tool logs
tail -f logs/manager.log

# View sync tool logs
tail -f logs/sync.log

# View complete sync logs
tail -f logs/complete_sync.log
```

## Technical Support

If you encounter problems, please:
1. Check log files for detailed error information
2. Check network connection and GitHub repository permissions
3. Try using console version to avoid GUI dependency issues
4. Submit Issue to GitHub repository

## Development Plan

- [ ] Support more cloud storage platforms (Gitee, GitLab, etc.)
- [ ] Add software version management functionality
- [ ] Support incremental updates and compressed transmission
- [ ] Add Web management interface
- [ ] Support plugin system

## Contributing

Welcome to submit Issues and Pull Requests!

1. Fork the project
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License

## Contact

- Project Address: [GitHub](https://github.com/shellsec/softgitup)
- Issue Feedback: [Issues](https://github.com/shellsec/softgitup/issues)

## 📚 Related Documentation

- [**Page check & monthly SOP**](soft_page_check/README.md) — Maintainer workflow (Chinese)
- [Configuration Guide](配置说明.md) - Detailed configuration parameters (Chinese)
- [Local Server Guide](本地服务器使用说明.md) - Local file server setup guide (Chinese)
- [手机隐私安全配置指南](手机隐私安全配置指南.md) - Complete mobile privacy configuration guide (Chinese)
- [Mobile Privacy & Security Guide](Mobile_Privacy_Security_Guide.md) - Complete mobile privacy configuration guide (English)
- [常用工具开源下载](常用工具开源下载.md) - Open-source download links for common tools (Chinese)
- [Cleaner/optimizer comparison: CCleaner Pro vs WiseCare365 Pro vs PC Fresh](CCleanerPro_vs_WiseCare365Pro_vs_PCFresh.txt) - Auto-optimization features, benchmarks, setup guides and use-case matching, 2026 (Chinese)
- [GitHub Releases on-demand updates (githubwindowntools)](software/githubwindowntools/README.md) - `apps.json`, enabling apps, `--platform`, mirrors / fallback behavior (README primarily Chinese)
- [Software & privacy notes (source list)](Lastb_soft_version.txt) - Long-form curated list aligned with `software/system_good/` and related paths (mostly Chinese)

---

**Note**: Please ensure compliance with relevant software usage license agreements. This tool is only for personal learning and legal purposes.

