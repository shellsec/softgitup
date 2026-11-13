# SoftGitUp 私有化部署

SoftGitUp 已支持 `remote` 模式。发布端用 `soft_manager.py` 为软件文件生成清单，静态 HTTP 服务提供清单和文件，Windows 客户端用 `sync_software.exe` 拉取更新。软件文件可以全部存放在内网。

## 本机跑通

### 1. 准备发布目录

新建独立的发布目录 `C:\SoftGitUp-publish`，复制项目根目录的 `soft_manager.py` 和本目录的 `publisher.example.json` 到其中。建立 `software\demo` 并放入测试文件 `hello.txt`。每个软件用一个子目录，在发布配置的 `software_dirs` 中列出这些目录名。

在 PowerShell 执行以下命令。发布机需要 Python 和 GitPython。

```powershell
Set-Location C:\SoftGitUp-publish
python -m pip install GitPython
python .\soft_manager.py --config .\publisher.example.json --generate-only
```

确认 `software\list.txt` 中的 `software.demo.files` 包含 `hello.txt`。清单是 JSON，记录相对路径、大小、MD5 和修改时间。

### 2. 启动测试源

将发布端的整个 `software` 目录复制到独立的站点根目录 `C:\SoftGitUp-web`，得到 `C:\SoftGitUp-web\software\list.txt` 和 `C:\SoftGitUp-web\software\demo\hello.txt`。在一个 PowerShell 窗口运行：

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory C:\SoftGitUp-web
```

### 3. 同步到测试客户端

在另一个目录 `C:\SoftGitUp-client` 放入新版 `sync_software.exe`，将本目录的 `client.example.json` 复制为 `config.json`。从客户端目录执行：

```powershell
Set-Location C:\SoftGitUp-client
New-Item -ItemType Directory -Force .\software | Out-Null
.\sync_software.exe
$LASTEXITCODE
Get-Content .\software\demo\hello.txt
```

首次同步预期退出码为 `0`，并得到测试文件。再执行一次，服务端访问日志应只有清单请求。修改发布端文件、重新生成清单并复制到测试站点后，可再次同步验证更新。

## 内网部署

1. **发布机**保存软件文件、发布配置和历史快照。更新时先在独立目录准备完整文件，再生成清单。检查清单中的文件条目和数量，然后将完整快照部署到静态服务。
2. **静态服务**以独立站点目录为根，例如使用企业已有的 IIS 或 Nginx。站点只需提供 `/software/` 下的只读文件，关闭目录浏览，将写权限交给发布账号。让企业内网或 VPN 客户端能访问站点，并使用客户端信任的 HTTPS 证书。
3. **客户端**把 `remote_server` 改成站点根 URL，例如 `https://updates.example.internal`。客户端会自行追加 `/software/list.txt` 和文件路径。每台设备从自己的客户端工作目录启动 EXE。使用 Windows 任务计划程序时，将该目录填入“起始于”，并让运行账号拥有软件目录和工作目录的写权限。

## 发布切换与回滚

可以用站点路径区分每次发布。例如将一个完整快照放在 `/releases/20261113-1/`，其下保留 `software/list.txt` 和所有清单文件。先验证该路径，再把客户端的 `remote_server` 更新为 `https://updates.example.internal/releases/20261113-1`。同一轮同步的清单和文件都从同一个快照读取。后续可以由现有的终端配置管理工具分发新版配置。

回滚时把 `remote_server` 指回旧快照并重新运行客户端。它会按旧清单恢复内容不同的同路径文件。当前客户端不会删除旧清单未列出的文件。如发布涉及文件改名或移除，需要按该软件的部署流程处理旧文件。

## 访问控制如何实现

现有 `remote` 模式会直接请求静态 URL，适合通过防火墙、内网或 VPN 限制访问的场景。如果需要按设备授权，可以扩展客户端，为获取清单和下载文件共用一个 HTTP 会话，从设备的凭据存储取得令牌，通过请求头发送，由网关统一校验。服务端为设备提供只读权限，并支持凭据轮换。认证扩展需要修改源码并重新打包 EXE。
