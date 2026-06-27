# PyInstaller: dist/exe/auto_update.exe, lookup_app.exe, run_saved_apps.exe
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== GH Release Fetch: build 3 exe ==" -ForegroundColor Cyan

python --version 2>$null
if (-not $?) {
    throw "Python 3 not found."
}

pip install -r requirements.txt pyinstaller --quiet

$Dist = Join-Path $Root "dist\exe"
$Work = Join-Path $Root "build\pyinstaller"
New-Item -ItemType Directory -Force -Path $Dist, $Work | Out-Null

$Hidden = @(
    "--hidden-import", "tools.app_list",
    "--hidden-import", "tools.ghrf_runtime",
    "--hidden-import", "tools.apply_enabled_snapshot"
)
$Common = @(
    "--noconfirm", "--clean",
    "--distpath", $Dist,
    "--workpath", $Work,
    "--specpath", $Work,
    "--paths", $Root
) + $Hidden

function Build-One($Name, $Entry) {
    Write-Host ""
    Write-Host ">> $Name" -ForegroundColor Yellow
    pyinstaller @Common --onefile --name $Name $Entry
    if ($LASTEXITCODE -ne 0) { throw "pyinstaller failed: $Name" }
}

Build-One "auto_update" "auto_update.py"
Build-One "lookup_app" "lookup_app.py"
Build-One "run_saved_apps" "tools\run_saved_apps.py"

Write-Host ""
Write-Host "Done: $Dist" -ForegroundColor Green
Write-Host "Copy auto_update.exe lookup_app.exe run_saved_apps.exe to repo root (next to apps/)."
