<#
.SYNOPSIS
    Clear contents of scripts / scripts_ENG / scripts_CHS under this PythonScript config root.

.EXAMPLE
    .\Clear-PythonScriptScripts.ps1 -WhatIf
    .\Clear-PythonScriptScripts.ps1 -Force
#>
param(
    [switch]$Force,
    [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
if (-not $root) {
    $root = Split-Path -Parent $MyInvocation.MyCommand.Path
}

$targets = @('scripts', 'scripts_ENG', 'scripts_CHS')
$existing = @()
foreach ($name in $targets) {
    $p = Join-Path $root $name
    if (Test-Path -LiteralPath $p) {
        $existing += $p
    }
}

if ($existing.Count -eq 0) {
    Write-Host 'No scripts, scripts_ENG or scripts_CHS folder found. Nothing done.' -ForegroundColor Yellow
    exit 0
}

Write-Host 'Will clear all contents in:' -ForegroundColor Cyan
foreach ($p in $existing) {
    Write-Host "  $p"
}

if ($WhatIf) {
    foreach ($p in $existing) {
        Get-ChildItem -LiteralPath $p -Force | ForEach-Object {
            Write-Host "[WhatIf] would remove: $($_.FullName)" -ForegroundColor DarkGray
        }
    }
    exit 0
}

if (-not $Force) {
    $r = Read-Host 'Confirm? This cannot be undone. [y/N]'
    if ($r -cne 'y' -and $r -cne 'Y') {
        Write-Host 'Cancelled.' -ForegroundColor Yellow
        exit 1
    }
}

foreach ($p in $existing) {
    Get-ChildItem -LiteralPath $p -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    Write-Host "Cleared: $p" -ForegroundColor Green
}

Write-Host 'Done. Copy scripts back from your repo or backup.' -ForegroundColor Green
exit 0
