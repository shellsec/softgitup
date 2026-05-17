# 供任务栏固定 / 桌面快捷方式脚本共用（点号引入，勿直接运行）
$ErrorActionPreference = 'Stop'

function Get-SoftwareLayout {
    param(
        [string]$ScriptDirectory,
        [string]$OverrideRoot
    )

    $systemGoodDir = [System.IO.Path]::GetFullPath($ScriptDirectory)
    $leaf = [System.IO.Path]::GetFileName($systemGoodDir.TrimEnd('\', '/'))

    if ($OverrideRoot) {
        $root = [System.IO.Path]::GetFullPath($OverrideRoot)
    }
    elseif ($leaf -ieq 'system_good') {
        $root = [System.IO.Path]::GetFullPath((Join-Path $systemGoodDir '..'))
    }
    else {
        $root = [System.IO.Path]::GetFullPath((Join-Path $systemGoodDir '..'))
        Write-Host "[路径] 未检测到 system_good 目录名，使用上一级作为软件根: $root" -ForegroundColor DarkYellow
    }

    return [PSCustomObject]@{
        SystemGoodDir        = $systemGoodDir
        SoftwareRoot         = $root
        SystemGoodFolderName = if ($leaf -ieq 'system_good') { 'system_good' } else { $leaf }
    }
}

function Resolve-FolderPath {
    param(
        [string]$SoftwareRoot,
        [string]$SystemGoodDir,
        [string]$SystemGoodFolderName,
        [string]$FolderName
    )

    if ([string]::IsNullOrWhiteSpace($FolderName) -or $FolderName -eq '.' -or $FolderName -ieq 'system_good') {
        return $SystemGoodDir
    }
    if ($FolderName -ieq $SystemGoodFolderName) {
        return $SystemGoodDir
    }

    $direct = Join-Path $SoftwareRoot $FolderName
    if (Test-Path -LiteralPath $direct) {
        return ([System.IO.Path]::GetFullPath($direct))
    }

    if (Test-Path -LiteralPath $SoftwareRoot) {
        $match = Get-ChildItem -LiteralPath $SoftwareRoot -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ieq $FolderName } |
            Select-Object -First 1
        if ($match) { return $match.FullName }
    }

    return $direct
}

function Resolve-ToolExecutable {
    param(
        [object]$Target,
        [object]$Layout,
        [int]$SearchDepth = 3
    )

    $fileNames = @($Target.file)
    if ($Target.alternates) { $fileNames += @($Target.alternates) }
    $fileNames = $fileNames | Where-Object { $_ } | Select-Object -Unique

    $folderNames = @($Target.folders)
    if (-not $folderNames -or $folderNames.Count -eq 0) {
        $folderNames = @('system_good')
    }

    $roots = @()
    foreach ($fn in $folderNames) {
        $roots += (Resolve-FolderPath -SoftwareRoot $Layout.SoftwareRoot `
            -SystemGoodDir $Layout.SystemGoodDir `
            -SystemGoodFolderName $Layout.SystemGoodFolderName `
            -FolderName $fn)
    }
    $roots = $roots | Select-Object -Unique

    foreach ($root in $roots) {
        if ($Target.relativePath) {
            $relPath = Join-Path $root $Target.relativePath
            if (Test-Path -LiteralPath $relPath) {
                return ([PSCustomObject]@{ Path = ([System.IO.Path]::GetFullPath($relPath)); Via = $relPath })
            }
        }

        foreach ($name in $fileNames) {
            $direct = Join-Path $root $name
            if (Test-Path -LiteralPath $direct) {
                return ([PSCustomObject]@{ Path = ([System.IO.Path]::GetFullPath($direct)); Via = $direct })
            }
        }

        if (-not (Test-Path -LiteralPath $root)) { continue }

        foreach ($name in $fileNames) {
            $found = Get-ChildItem -LiteralPath $root -Filter $name -Recurse -Depth $SearchDepth -File -ErrorAction SilentlyContinue |
                Select-Object -First 1
            if ($found) {
                return ([PSCustomObject]@{ Path = $found.FullName; Via = $found.FullName })
            }
        }
    }

    if ($Target.searchSiblings -ne $false) {
        if (Test-Path -LiteralPath $Layout.SoftwareRoot) {
            foreach ($name in $fileNames) {
                $found = Get-ChildItem -LiteralPath $Layout.SoftwareRoot -Filter $name -Recurse -Depth $SearchDepth -File -ErrorAction SilentlyContinue |
                    Select-Object -First 1
                if ($found) {
                    return ([PSCustomObject]@{ Path = $found.FullName; Via = $found.FullName })
                }
            }
        }
    }

    return $null
}

function Get-PinTargetsFromManifest {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "找不到清单文件: $Path"
    }

    $raw = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    $json = $raw | ConvertFrom-Json
    $list = New-Object System.Collections.ArrayList

    foreach ($prop in $json.groups.PSObject.Properties) {
        $groupName = $prop.Name
        foreach ($t in $prop.Value.targets) {
            $entry = @{
                label          = $t.label
                file           = $t.file
                folders        = @($t.folders)
                note           = $t.note
                group          = $groupName
                relativePath   = $t.relativePath
                alternates     = @($t.alternates)
                searchSiblings = if ($null -ne $t.searchSiblings) { [bool]$t.searchSiblings } else { $true }
            }
            [void]$list.Add($entry)
        }
    }

    $skip = @{}
    if ($json.skip) {
        foreach ($p in $json.skip.PSObject.Properties) {
            $skip[$p.Name] = $p.Value
        }
    }

    return [PSCustomObject]@{ Targets = $list; Skip = $skip }
}

function Get-TargetsForGroups {
    param(
        [System.Collections.ArrayList]$AllTargets,
        [string[]]$GroupNames
    )
    return @($AllTargets | Where-Object { $GroupNames -contains $_.group })
}

function Get-DesktopFolderPaths {
    $paths = @()
    $userDesktop = [Environment]::GetFolderPath('Desktop')
    if ($userDesktop) { $paths += $userDesktop }

    $oneDrive = $env:OneDrive
    if ($oneDrive) {
        $odDesk = Join-Path $oneDrive 'Desktop'
        if ((Test-Path -LiteralPath $odDesk) -and ($paths -notcontains $odDesk)) {
            $paths += $odDesk
        }
    }

    return ($paths | Select-Object -Unique)
}

function New-ExeShortcutFile {
    param(
        [string]$ExePath,
        [string]$Label,
        [string]$LnkPath
    )

    $exePath = [System.IO.Path]::GetFullPath($ExePath)
    $dir = Split-Path -Parent $LnkPath
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    $wsh = New-Object -ComObject WScript.Shell
    $shortcut = $wsh.CreateShortcut($LnkPath)
    $shortcut.TargetPath = $exePath
    $shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($exePath)
    $shortcut.IconLocation = '{0},0' -f $exePath
    $shortcut.Description = '{0} (softgitup)' -f $Label
    $shortcut.Save()
}

function Get-ShortcutTargetMap {
    param([string[]]$SearchFolders)

    $map = @{}
    $shell = New-Object -ComObject WScript.Shell

    foreach ($folder in $SearchFolders) {
        if (-not (Test-Path -LiteralPath $folder)) { continue }
        Get-ChildItem -LiteralPath $folder -Filter '*.lnk' -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $shortcut = $shell.CreateShortcut($_.FullName)
                if ($shortcut.TargetPath) {
                    $key = [System.IO.Path]::GetFullPath($shortcut.TargetPath).ToLowerInvariant()
                    if (-not $map.ContainsKey($key)) {
                        $map[$key] = $_.FullName
                    }
                }
            }
            catch { }
        }
    }
    return $map
}

function Get-SafeShortcutBaseName {
    param([string]$Label)
    $safe = ($Label -replace '[\\/:*?"<>|]', '_').Trim()
    if ([string]::IsNullOrWhiteSpace($safe)) { $safe = 'app' }
    return $safe
}
