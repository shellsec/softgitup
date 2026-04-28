#Requires -Version 5.1
param(
    [Parameter(Mandatory = $true)]
    [string] $IndexHtmlPath
)

function Get-DesktopFolder {
    $seen = @{}
    $list = @(
        [Environment]::GetFolderPath("Desktop")
    )
    $prof = $env:USERPROFILE
    if ($prof) {
        $list += (Join-Path $prof "Desktop")
        Get-ChildItem -LiteralPath $prof -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -like "OneDrive*" } |
            ForEach-Object { Join-Path $_.FullName "Desktop" } |
            ForEach-Object { $list += $_ }
    }
    foreach ($d in $list) {
        if ([string]::IsNullOrWhiteSpace($d)) { continue }
        if ($seen.ContainsKey($d)) { continue }
        $seen[$d] = $true
        if (Test-Path -LiteralPath $d) { return $d }
    }
    return $null
}

if (-not (Test-Path -LiteralPath $IndexHtmlPath)) {
    Write-Host "[ERROR] index.html not found: $IndexHtmlPath" -ForegroundColor Red
    exit 1
}

$navFile = Resolve-Path -LiteralPath $IndexHtmlPath
$htmlDir = Split-Path -Parent $navFile.Path
$uri = (New-Object System.Uri($navFile.Path)).AbsoluteUri
$content = "[InternetShortcut]`r`nURL=$uri`r`n"

$desktop = Get-DesktopFolder
$finalPath = $null
$desktopErrors = New-Object System.Collections.Generic.List[string]

if ($desktop) {
    # 仅用英文文件名，避免中文「AI导航」在部分系统上显示为乱码（如 AI瀵艰埅）
    $p = Join-Path $desktop "AI-Navigator.url"
    try {
        Set-Content -LiteralPath $p -Encoding ascii -Value $content -Force -ErrorAction Stop
        $finalPath = $p
        $stale = Join-Path $desktop "AI导航.url"
        if ((Test-Path -LiteralPath $stale) -and ($stale -ne $p)) {
            Remove-Item -LiteralPath $stale -Force -ErrorAction SilentlyContinue
        }
    } catch {
        $desktopErrors.Add("$p : $($_.Exception.Message)")
    }
}

if (-not $finalPath) {
    $p = Join-Path $htmlDir "AI-Navigator.url"
    try {
        Set-Content -LiteralPath $p -Encoding ascii -Value $content -Force -ErrorAction Stop
        $finalPath = $p
        Write-Host "[WARN] Could not save shortcut on Desktop (policy, antivirus, or path)." -ForegroundColor Yellow
        foreach ($e in $desktopErrors) { Write-Host "  $e" }
        Write-Host "  Saved next to index.html instead." -ForegroundColor Yellow
    } catch {
        Write-Host "[ERROR] Cannot write shortcut: $p" -ForegroundColor Red
        Write-Host $_.Exception.Message
        foreach ($e in $desktopErrors) { Write-Host "  Desktop try: $e" }
        exit 2
    }
}

Write-Host "Shortcut file: $finalPath"

try {
    Start-Process $uri
    Write-Host "Opened: $uri"
} catch {
    Write-Host "[WARN] Browser did not open automatically: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "Double-click the .url file above or open this path in browser:"
    Write-Host "  $uri"
}

exit 0
