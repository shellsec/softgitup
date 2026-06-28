# PyInstaller: dist/exe/*.exe
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== GH Release Fetch: build exe ==" -ForegroundColor Cyan

python --version 2>$null
if (-not $?) { throw "Python 3 not found." }

pip install -r requirements.txt pyinstaller --quiet

$Dist = Join-Path $Root "dist\exe"
$Work = Join-Path $Root "build\pyinstaller"
$SoftCheck = Join-Path $Root "tools\soft_page_check"
New-Item -ItemType Directory -Force -Path $Dist, $Work | Out-Null

$HiddenCore = @(
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
)

function Build-One($Name, $Entry, [string[]]$More = @()) {
    Write-Host ""
    Write-Host ">> $Name" -ForegroundColor Yellow
    pyinstaller @Common @HiddenCore @More --onefile --name $Name $Entry
    if ($LASTEXITCODE -ne 0) { throw "pyinstaller failed: $Name" }
}

Build-One "auto_update" "auto_update.py"
Build-One "lookup_app" "lookup_app.py"
Build-One "run_saved_apps" "tools\run_saved_apps.py"
Build-One "search_soft_pages" "tools\soft_page_check\search_pages.py" @(
    "--paths", $SoftCheck,
    "--hidden-import", "list_scopes",
    "--hidden-import", "gamer520_live_search"
)
Build-One "search_games" "tools\soft_page_check\search_games.py" @(
    "--paths", $SoftCheck,
    "--hidden-import", "list_scopes",
    "--hidden-import", "search_pages",
    "--hidden-import", "gamer520_live_search"
)

Write-Host ""
Write-Host "Done: $Dist" -ForegroundColor Green
Write-Host "Copy to repo root: lookup_app.exe run_saved_apps.exe search_soft_pages.exe search_games.exe auto_update.exe"
