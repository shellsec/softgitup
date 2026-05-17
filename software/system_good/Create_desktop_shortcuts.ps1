#Requires -Version 5.1
<#
.SYNOPSIS
    为 system_good 及同级常用软件在桌面创建快捷方式（与任务栏脚本共用 Pin_taskbar_targets.json）。

.PARAMETER IncludeOptional
    额外创建 Ditto、StartBack 快捷方式。

.PARAMETER IncludeMaintenance
    额外创建 SmartDefrag 快捷方式。

.PARAMETER SoftwareRoot
    手动指定软件根目录（如 D:\Program Files）。

.PARAMETER DesktopOnly
    仅用户桌面，不包含 OneDrive 桌面路径。
#>
[CmdletBinding()]
param(
    [switch]$IncludeOptional,
    [switch]$IncludeMaintenance,
    [string]$SoftwareRoot = '',
    [switch]$DesktopOnly
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
. (Join-Path $ScriptDir 'Pin_shortcut_common.ps1')

$ManifestPath = Join-Path $ScriptDir 'Pin_taskbar_targets.json'

function Add-DesktopShortcut {
    param(
        [string]$ExePath,
        [string]$Label,
        [string[]]$DesktopFolders
    )

    $safe = Get-SafeShortcutBaseName -Label $Label
    $created = @()

    foreach ($desk in $DesktopFolders) {
        $lnkPath = Join-Path $desk ("{0}.lnk" -f $safe)
        New-ExeShortcutFile -ExePath $ExePath -Label $Label -LnkPath $lnkPath
        $created += $lnkPath
    }

    return $created
}

function Invoke-DesktopTarget {
    param(
        [hashtable]$Target,
        [object]$Layout,
        [hashtable]$ExistingMap,
        [string[]]$DesktopFolders,
        [ref]$Ok,
        [ref]$Skip,
        [ref]$Fail
    )

    $label = $Target.label
    $file = $Target.file
    $resolved = Resolve-ToolExecutable -Target $Target -Layout $Layout

    if (-not $resolved) {
        Write-Host "[跳过] $label ($file) — 未找到" -ForegroundColor DarkYellow
        $Skip.Value++
        return
    }

    $exePath = $resolved.Path
    $key = $exePath.ToLowerInvariant()

    if ($ExistingMap.ContainsKey($key)) {
        Write-Host "[已有] $label — $($ExistingMap[$key])" -ForegroundColor DarkGray
        $Skip.Value++
        return
    }

    try {
        $paths = Add-DesktopShortcut -ExePath $exePath -Label $label -DesktopFolders $DesktopFolders
        Write-Host "[成功] $label ($file)" -ForegroundColor Green
        foreach ($p in $paths) {
            Write-Host "       $p" -ForegroundColor DarkGray
        }
        $ExistingMap[$key] = $paths[0]
        $Ok.Value++
    }
    catch {
        Write-Host "[失败] $label — $($_.Exception.Message)" -ForegroundColor Red
        $Fail.Value++
    }
}

# --- main ---

$Layout = Get-SoftwareLayout -ScriptDirectory $ScriptDir -OverrideRoot $SoftwareRoot
$manifest = Get-PinTargetsFromManifest -Path $ManifestPath

$groupsToRun = @('default')
if ($IncludeOptional) { $groupsToRun += 'optional' }
if ($IncludeMaintenance) { $groupsToRun += 'maintenance' }
$toCreate = Get-TargetsForGroups -AllTargets $manifest.Targets -GroupNames $groupsToRun

$desktopFolders = if ($DesktopOnly) {
    @([Environment]::GetFolderPath('Desktop'))
} else {
    Get-DesktopFolderPaths
}

Write-Host '========================================' -ForegroundColor Cyan
Write-Host '  一键创建桌面快捷方式' -ForegroundColor Cyan
Write-Host "  system_good: $($Layout.SystemGoodDir)" -ForegroundColor DarkGray
Write-Host "  软件根目录:  $($Layout.SoftwareRoot)" -ForegroundColor DarkGray
Write-Host "  桌面目录:" -ForegroundColor DarkGray
foreach ($d in $desktopFolders) { Write-Host "    $d" -ForegroundColor DarkGray }
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''

Write-Host "[计划创建] 共 $($toCreate.Count) 项" -ForegroundColor Cyan
foreach ($t in $toCreate) {
    $r = Resolve-ToolExecutable -Target $t -Layout $Layout
    $mark = if ($r) { '[OK]' } else { '[--]' }
    Write-Host "  $mark $($t.label) ($($t.file))"
}
Write-Host ''

$existingMap = Get-ShortcutTargetMap -SearchFolders $desktopFolders
$ok = 0; $skip = 0; $fail = 0

foreach ($target in $toCreate) {
    Invoke-DesktopTarget -Target $target -Layout $Layout -ExistingMap $existingMap `
        -DesktopFolders $desktopFolders -Ok ([ref]$ok) -Skip ([ref]$skip) -Fail ([ref]$fail)
}

Write-Host ''
Write-Host "完成: 成功 $ok | 跳过 $skip | 失败 $fail" -ForegroundColor Cyan
Write-Host '清单与任务栏脚本相同: Pin_taskbar_targets.json' -ForegroundColor DarkGray
Write-Host '可选: -IncludeOptional -IncludeMaintenance' -ForegroundColor DarkGray
Write-Host ''

if ($fail -gt 0) { exit 1 }
exit 0
