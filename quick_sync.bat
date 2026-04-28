@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Simple Software Download Tool

:: Set variables
set "BASE_DIR=%~dp0"
set "CONFIG_FILE=%BASE_DIR%config.json"

:: Check config file
if not exist "%CONFIG_FILE%" (
    echo Error: Config file not found
    timeout /t 3 >nul
    exit /b 1
)

:: Read target directory
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Output $config.sync_base_path } catch { Write-Output 'ERROR' }"') do set "TARGET_DIR=%%i"

if "%TARGET_DIR%"=="ERROR" (
    echo Error: Cannot read config file
    timeout /t 3 >nul
    exit /b 1
)

:: Create target directory if not exists
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%" 2>nul

echo Downloading software to: %TARGET_DIR%
echo.

:: Create PowerShell script
set "PS_TEMP=%TEMP%\simple_download.ps1"

echo $ErrorActionPreference = "Continue" > "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo try { >> "%PS_TEMP%"
echo     $listUrl = 'https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup/refs/heads/master/software/list.txt' >> "%PS_TEMP%"
echo     Write-Host 'Getting software list...' >> "%PS_TEMP%"
echo     $list = (Invoke-WebRequest -Uri $listUrl -TimeoutSec 30).Content ^| ConvertFrom-Json >> "%PS_TEMP%"
echo     Write-Host "Found $($list.software.Count) software packages" >> "%PS_TEMP%"
echo     Write-Host '' >> "%PS_TEMP%"
echo } catch { >> "%PS_TEMP%"
echo     Write-Host 'Cannot get software list' -ForegroundColor Red >> "%PS_TEMP%"
echo     exit 1 >> "%PS_TEMP%"
echo } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo $baseUrl = 'https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup/refs/heads/master/software' >> "%PS_TEMP%"
echo $webClient = New-Object System.Net.WebClient >> "%PS_TEMP%"
echo $webClient.Headers.Add('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36') >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo $totalFiles = 0 >> "%PS_TEMP%"
echo $successFiles = 0 >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo foreach ($software in $list.software.PSObject.Properties) { >> "%PS_TEMP%"
echo     $softwareName = $software.Name >> "%PS_TEMP%"
echo     $files = $software.Value.files >> "%PS_TEMP%"
echo     $totalFiles += $files.Count >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo     Write-Host "Downloading $softwareName ($($files.Count) files)..." -ForegroundColor Cyan >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo     foreach ($file in $files) { >> "%PS_TEMP%"
echo         $filePath = $file.path -replace '\\', '/' >> "%PS_TEMP%"
echo         $fileUrl = "$baseUrl/$softwareName/$filePath" >> "%PS_TEMP%"
echo         $localPath = Join-Path '%TARGET_DIR%' $softwareName >> "%PS_TEMP%"
echo         $localPath = Join-Path $localPath $file.path >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo         $dir = Split-Path $localPath -Parent >> "%PS_TEMP%"
echo         if (!(Test-Path $dir)) { >> "%PS_TEMP%"
echo             New-Item -ItemType Directory -Path $dir -Force ^| Out-Null >> "%PS_TEMP%"
echo         } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo         try { >> "%PS_TEMP%"
echo             $webClient.DownloadFile($fileUrl, $localPath) >> "%PS_TEMP%"
echo             $successFiles++ >> "%PS_TEMP%"
echo             Write-Host "  [OK] $($file.path)" -ForegroundColor Green >> "%PS_TEMP%"
echo         } catch { >> "%PS_TEMP%"
echo             Write-Host "  [FAIL] $($file.path)" -ForegroundColor Red >> "%PS_TEMP%"
echo         } >> "%PS_TEMP%"
echo     } >> "%PS_TEMP%"
echo     Write-Host '' >> "%PS_TEMP%"
echo } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo $webClient.Dispose() >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo Write-Host '===============================' >> "%PS_TEMP%"
echo Write-Host "Download completed: $successFiles/$totalFiles files" >> "%PS_TEMP%"
echo Write-Host '===============================' >> "%PS_TEMP%"

:: Execute PowerShell script
powershell -ExecutionPolicy Bypass -File "%PS_TEMP%"

:: Clean up
del "%PS_TEMP%" 2>nul

if %errorlevel% equ 0 (
    echo.
    echo Download completed successfully!
    echo.
    set /p "OPEN_DIR=Open target directory? (y/n): "
    if /i "!OPEN_DIR!"=="y" explorer "%TARGET_DIR%"
) else (
    echo.
    echo Download failed with errors
    timeout /t 5 >nul
)