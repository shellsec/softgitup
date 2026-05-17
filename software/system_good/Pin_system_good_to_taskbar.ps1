#Requires -Version 5.1
<#
.SYNOPSIS
    批量将 system_good 及同级常用软件固定到 Windows 任务栏（Win10 / Win11）。

.PARAMETER IncludeOptional
    额外包含 Ditto、StartBack。

.PARAMETER IncludeMaintenance
    额外包含 SmartDefrag。

.PARAMETER PinMode
    Auto | Verb | FolderOnly

.PARAMETER RestartExplorer
    完成后重启资源管理器（Win11 建议）。

.PARAMETER SoftwareRoot
    手动指定软件根目录（如 D:\Program Files）。
#>
[CmdletBinding()]
param(
    [switch]$IncludeOptional,
    [switch]$IncludeMaintenance,
    [ValidateSet('Auto', 'Verb', 'FolderOnly')]
    [string]$PinMode = 'Auto',
    [switch]$RestartExplorer,
    [string]$SoftwareRoot = ''
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
. (Join-Path $ScriptDir 'Pin_shortcut_common.ps1')

$ManifestPath = Join-Path $ScriptDir 'Pin_taskbar_targets.json'
$PinFolder = Join-Path $env:APPDATA 'Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar'

function Get-WindowsTaskbarProfile {
    $v = [Environment]::OSVersion.Version
    $build = $v.Build
    $isWin11 = ($build -ge 22000)
    return [PSCustomObject]@{
        Build   = $build
        IsWin11 = $isWin11
        OsLabel = if ($isWin11) { 'Windows 11' } else { 'Windows 10' }
    }
}

function Get-EffectivePinMode {
    param([string]$Requested, [object]$Profile)
    switch ($Requested) {
        'Verb' { return 'Verb' }
        'FolderOnly' { return 'FolderOnly' }
        default {
            if ($Profile.IsWin11) { return 'AutoWin11' }
            return 'AutoWin10'
        }
    }
}

function Invoke-TaskbarPinVerb {
    param([string]$LnkPath)
    $folderPath = Split-Path -Parent $LnkPath
    $fileName = [System.IO.Path]::GetFileName($LnkPath)
    $shellApp = New-Object -ComObject Shell.Application
    $folder = $shellApp.Namespace($folderPath)
    if (-not $folder) { throw '无法打开任务栏固定目录' }
    $item = $folder.ParseName($fileName)
    if (-not $item) { throw '无法解析快捷方式' }
    $null = $item.InvokeVerb('taskbarpin')
}

function Add-TaskbarPin {
    param(
        [string]$ExePath,
        [string]$Label,
        [string]$Mode
    )

    if (-not (Test-Path -LiteralPath $PinFolder)) {
        New-Item -ItemType Directory -Path $PinFolder -Force | Out-Null
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($ExePath)
    $safeName = ($baseName -replace '[\\/:*?"<>|]', '_')
    $lnkPath = Join-Path $PinFolder ("softgitup_{0}.lnk" -f $safeName)

    New-ExeShortcutFile -ExePath $ExePath -Label $Label -LnkPath $lnkPath

    $usedVerb = $false
    $tryVerb = ($Mode -eq 'Verb') -or ($Mode -like 'AutoWin*')
    if ($tryVerb) {
        try {
            Invoke-TaskbarPinVerb -LnkPath $lnkPath
            $usedVerb = $true
        }
        catch {
            if ($Mode -eq 'Verb') { throw }
        }
    }

    return [PSCustomObject]@{
        LnkPath  = $lnkPath
        UsedVerb = $usedVerb
    }
}

function Write-Banner {
    param($Layout, $Profile, $Mode)
    Write-Host '========================================' -ForegroundColor Cyan
    Write-Host '  一键固定到任务栏 (Win10 / Win11)' -ForegroundColor Cyan
    Write-Host "  系统: $($Profile.OsLabel) (Build $($Profile.Build))" -ForegroundColor DarkGray
    Write-Host "  固定模式: $Mode" -ForegroundColor DarkGray
    Write-Host "  system_good: $($Layout.SystemGoodDir)" -ForegroundColor DarkGray
    Write-Host "  软件根目录:  $($Layout.SoftwareRoot)" -ForegroundColor DarkGray
    Write-Host '========================================' -ForegroundColor Cyan
    Write-Host ''
}

function Invoke-PinTarget {
    param(
        [hashtable]$Target,
        [object]$Layout,
        [hashtable]$PinnedMap,
        [string]$PinModeEffective,
        [object]$Profile,
        [ref]$Ok,
        [ref]$Skip,
        [ref]$Fail
    )

    $label = $Target.label
    $file = $Target.file
    $resolved = Resolve-ToolExecutable -Target $Target -Layout $Layout

    if (-not $resolved) {
        Write-Host "[跳过] $label ($file) — 未在软件根下找到" -ForegroundColor DarkYellow
        $Skip.Value++
        return
    }

    $exePath = $resolved.Path
    $key = $exePath.ToLowerInvariant()

    if ($PinnedMap.ContainsKey($key)) {
        Write-Host "[已有] $label — $($PinnedMap[$key])" -ForegroundColor DarkGray
        $Skip.Value++
        return
    }

    try {
        $result = Add-TaskbarPin -ExePath $exePath -Label $label -Mode $PinModeEffective
        $method = if ($result.UsedVerb) { 'taskbarpin' } else { '固定目录' }
        Write-Host "[成功] $label ($file) — $method" -ForegroundColor Green
        Write-Host "       $exePath" -ForegroundColor DarkGray
        $PinnedMap[$key] = [System.IO.Path]::GetFileName($result.LnkPath)
        $Ok.Value++
    }
    catch {
        Write-Host "[失败] $label — $($_.Exception.Message)" -ForegroundColor Red
        $Fail.Value++
    }
}

# --- main ---

$Layout = Get-SoftwareLayout -ScriptDirectory $ScriptDir -OverrideRoot $SoftwareRoot
$Profile = Get-WindowsTaskbarProfile
$PinModeEffective = Get-EffectivePinMode -Requested $PinMode -Profile $Profile

$manifest = Get-PinTargetsFromManifest -Path $ManifestPath
$groupsToRun = @('default')
if ($IncludeOptional) { $groupsToRun += 'optional' }
if ($IncludeMaintenance) { $groupsToRun += 'maintenance' }
$toPin = Get-TargetsForGroups -AllTargets $manifest.Targets -GroupNames $groupsToRun
$skipReasons = $manifest.Skip

Write-Banner -Layout $Layout -Profile $Profile -Mode $PinModeEffective

Write-Host "[计划固定] 共 $($toPin.Count) 项（default 含 system_good + 同级常用软件）" -ForegroundColor Cyan
foreach ($t in $toPin) {
    $r = Resolve-ToolExecutable -Target $t -Layout $Layout
    $mark = if ($r) { '[OK]' } else { '[--]' }
    Write-Host "  $mark $($t.label) ($($t.file))"
}
Write-Host ''

$PinnedMap = Get-ShortcutTargetMap -SearchFolders @($PinFolder)
$ok = 0; $skip = 0; $fail = 0

foreach ($target in $toPin) {
    Invoke-PinTarget -Target $target -Layout $Layout -PinnedMap $PinnedMap `
        -PinModeEffective $PinModeEffective -Profile $Profile `
        -Ok ([ref]$ok) -Skip ([ref]$skip) -Fail ([ref]$fail)
}

$plannedFiles = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($t in $toPin) { [void]$plannedFiles.Add($t.file) }

$unlisted = @()
if (Test-Path -LiteralPath $Layout.SystemGoodDir) {
    Get-ChildItem -LiteralPath $Layout.SystemGoodDir -Filter '*.exe' -File -ErrorAction SilentlyContinue | ForEach-Object {
        if ($plannedFiles.Contains($_.Name)) { return }
        $reason = $skipReasons[$_.Name]
        if (-not $reason) { $reason = '未在 Pin_taskbar_targets.json；可编辑 JSON 或加 -IncludeOptional' }
        $unlisted += [PSCustomObject]@{ Name = $_.Name; Reason = $reason }
    }
}

if ($unlisted.Count -gt 0) {
    Write-Host ''
    Write-Host '[未自动固定（system_good 内其它 exe）]' -ForegroundColor Yellow
    foreach ($u in $unlisted) {
        Write-Host "  * $($u.Name) — $($u.Reason)" -ForegroundColor DarkGray
    }
}

Write-Host ''
Write-Host "完成: 成功 $ok | 跳过 $skip | 失败 $fail" -ForegroundColor Cyan
Write-Host '可选: -IncludeOptional -IncludeMaintenance -RestartExplorer -PinMode FolderOnly' -ForegroundColor DarkGray
Write-Host ''

$needRestart = $RestartExplorer -or ($Profile.IsWin11 -and $ok -gt 0 -and $PinModeEffective -ne 'Verb')
if ($needRestart -and $ok -gt 0) {
    Write-Host '[刷新] 正在重启资源管理器...' -ForegroundColor Yellow
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process explorer
}

if ($fail -gt 0) { exit 1 }
exit 0
