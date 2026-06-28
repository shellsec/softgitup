# 打包 Windows Release：dist/release/gh-release-fetch-windows-<版本>.zip
# 用法:
#   powershell -ExecutionPolicy Bypass -File tools\pack_windows_release.ps1
#   powershell -ExecutionPolicy Bypass -File tools\pack_windows_release.ps1 -Version 1.0.0
#   powershell -ExecutionPolicy Bypass -File tools\pack_windows_release.ps1 -SkipBuild
param(
    [switch]$SkipBuild,
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Get-ReleaseVersion {
    param([string]$Explicit)
    if ($Explicit) { return $Explicit.Trim() }
    $tag = git describe --tags --always 2>$null
    if ($LASTEXITCODE -eq 0 -and $tag) { return $tag -replace '[\\/:*?"<>|]', '-' }
    return (Get-Date -Format "yyyyMMdd")
}

$ver = Get-ReleaseVersion -Explicit $Version
$StageName = "gh-release-fetch-windows-$ver"
$OutDir = Join-Path $Root "dist\release"
$Stage = Join-Path $OutDir $StageName
$ZipPath = Join-Path $OutDir "$StageName.zip"

Write-Host "== Pack Windows release: $StageName ==" -ForegroundColor Cyan

if (-not $SkipBuild) {
    & (Join-Path $Root "tools\build_exe.ps1")
}

$ExeDir = Join-Path $Root "dist\exe"
$exes = @("lookup_app.exe", "run_saved_apps.exe", "search_soft_pages.exe", "search_games.exe", "auto_update.exe")
foreach ($name in $exes) {
    $p = Join-Path $ExeDir $name
    if (-not (Test-Path $p)) {
        throw "Missing $p — run tools\build_exe.ps1 first."
    }
}

if (Test-Path $Stage) { Remove-Item $Stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Stage | Out-Null

Write-Host "Copy exes and bats..."
foreach ($name in $exes) {
    Copy-Item (Join-Path $ExeDir $name) (Join-Path $Stage $name) -Force
}
$bats = @("lookup_app.bat", "run_saved_apps.bat", "search_soft_pages.bat", "search_games.bat", "run_update.bat")
foreach ($name in $bats) {
    Copy-Item (Join-Path $Root $name) (Join-Path $Stage $name) -Force
}

Write-Host "Copy apps/ apps-mobile/ ..."
Copy-Item (Join-Path $Root "apps") (Join-Path $Stage "apps") -Recurse -Force
if (Test-Path (Join-Path $Root "apps-mobile")) {
    Copy-Item (Join-Path $Root "apps-mobile") (Join-Path $Stage "apps-mobile") -Recurse -Force
}

Write-Host "Copy soft_page_check index (search_soft_pages)..."
$spcSrc = Join-Path $Root "tools\soft_page_check"
$spcDst = Join-Path $Stage "tools\soft_page_check"
New-Item -ItemType Directory -Force -Path $spcDst | Out-Null
$spcItems = @("history", "list", "soft_pages_urls.txt", "watch_tier_a_urls.txt", "list_scopes.py", "423down_digest_urls.txt")
foreach ($item in $spcItems) {
    $src = Join-Path $spcSrc $item
    if (-not (Test-Path $src)) { continue }
    $dst = Join-Path $spcDst $item
    if (Test-Path $src -PathType Container) {
        Copy-Item $src $dst -Recurse -Force
    } else {
        Copy-Item $src $dst -Force
    }
}

Write-Host "Copy docs..."
$docs = @(
    "CATALOG.md",
    "CATALOG.mobile.md",
    "RECOMMENDED.zh-CN.md",
    "RECOMMENDED.md"
)
foreach ($name in $docs) {
    $src = Join-Path $Root $name
    if (Test-Path $src) { Copy-Item $src (Join-Path $Stage $name) -Force }
}

Copy-Item (Join-Path $Root "release\windows\README.txt") (Join-Path $Stage "README.txt") -Force
Copy-Item (Join-Path $Root "release\windows\saved_apps_windows.example.json") (Join-Path $Stage "saved_apps_windows.example.json") -Force
Set-Content -Path (Join-Path $Stage "VERSION.txt") -Value $ver -Encoding utf8

if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
Write-Host "Compress -> $ZipPath"
Compress-Archive -Path $Stage -DestinationPath $ZipPath -CompressionLevel Optimal

$sizeMb = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)
Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "  Folder: $Stage"
Write-Host "  Zip:    $ZipPath  ($sizeMb MB)"
Write-Host "  Upload the zip to GitHub Releases as Windows portable bundle."
