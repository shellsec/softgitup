@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Simple Software Download Tool

:: Set variables
set "BASE_DIR=%~dp0"
set "CONFIG_FILE=%BASE_DIR%config.json"

:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Not running as administrator. Some operations may fail due to insufficient permissions.
    echo.
    set "ADMIN_WARNING=1"
) else (
    echo Running with administrator privileges.
    set "ADMIN_WARNING=0"
)

:: Read git platform and repo configuration
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Output $config.git_platform } catch { Write-Output 'github' }"') do set "GIT_PLATFORM=%%i"
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Output $config.github_repo } catch { Write-Output '' }"') do set "GITHUB_REPO=%%i"
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Output $config.gitlab_repo } catch { Write-Output '' }"') do set "GITLAB_REPO=%%i"
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Output $config.remote_server } catch { Write-Output '' }"') do set "REMOTE_SERVER=%%i"
for /f "delims=" %%i in ('powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; $mirrors = $config.git_mirrors; if ($mirrors -and $mirrors.Count -gt 0) { Write-Output $mirrors[0] } else { Write-Output '' } } catch { Write-Output '' }"') do set "GIT_MIRROR=%%i"

if "%GIT_PLATFORM%"=="" set "GIT_PLATFORM=github"

:: 如果 git_platform 是 remote，使用 remote_server
if /i "%GIT_PLATFORM%"=="remote" (
    echo Using remote server
    if "%REMOTE_SERVER%"=="" (
        echo Error: git_platform is set to remote, but remote_server is not configured
        timeout /t 3 >nul
        exit /b 1
    )
    set "BASE_REPO=%REMOTE_SERVER%"
    if "%REMOTE_SERVER:~-1%"=="\" set "BASE_REPO=%BASE_REPO:~0,-1%"
    set "LIST_URL=%BASE_REPO%/software/list.txt"
    set "USE_REMOTE_SERVER=1"
    goto :skip_remote_config
) else (
    set "USE_REMOTE_SERVER=0"
)

:skip_remote_config
if /i "%GIT_PLATFORM%"=="gitlab" (
    echo Using GitLab platform
    if "%GIT_MIRROR%"=="" (
        if not "%GITLAB_REPO%"=="" (
            set "BASE_REPO=%GITLAB_REPO%"
        ) else (
            echo Error: GitLab repository not configured
            timeout /t 3 >nul
            exit /b 1
        )
    ) else (
        set "BASE_REPO=%GIT_MIRROR%"
    )
    set "LIST_URL=%BASE_REPO%/-/raw/master/software/list.txt"
) else (
    echo Using GitHub platform
    if "%GIT_MIRROR%"=="" (
        if not "%GITHUB_REPO%"=="" (
            set "BASE_REPO=%GITHUB_REPO%"
            set "LIST_URL=https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup/refs/heads/master/software/list.txt"
        ) else (
            echo Error: GitHub repository not configured
            timeout /t 3 >nul
            exit /b 1
        )
    ) else (
        set "BASE_REPO=%GIT_MIRROR%"
        if "%GIT_MIRROR:~-1%"=="\" set "BASE_REPO=%BASE_REPO:~0,-1%"
        if not "%GIT_MIRROR:refs/heads/%"=="%GIT_MIRROR%" (
            set "LIST_URL=%GIT_MIRROR%/software/list.txt"
        ) else (
            set "LIST_URL=%GIT_MIRROR%/refs/heads/master/software/list.txt"
        )
    )
)

:: Check connectivity (跳过远程服务器检查，直接使用)
if "%USE_REMOTE_SERVER%"=="1" (
    echo Using remote server, skipping connectivity check
    set "USE_BACKUP=0"
) else (
    echo Checking connectivity to: %LIST_URL%
    powershell -Command "try { $response = Invoke-WebRequest -Uri '%LIST_URL%' -TimeoutSec 10 -Method Head; exit 0 } catch { exit 1 }" >nul 2>&1
    
    if %errorlevel% neq 0 (
        echo Primary URL not accessible, using backup URL...
        set "USE_BACKUP=1"
        if /i "%GIT_PLATFORM%"=="gitlab" (
            set "LIST_URL=https://raw.bgithub.xyz/shellsec/softgitup/refs/heads/master/software/list.txt"
        ) else (
            set "LIST_URL=https://raw.bgithub.xyz/shellsec/softgitup/refs/heads/master/software/list.txt"
        )
    ) else (
        echo Primary URL accessible
        set "USE_BACKUP=0"
    )
)

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

:: If sync_base_path is empty, use current directory (batch file location)
if "%TARGET_DIR%"=="" (
    set "TARGET_DIR=%BASE_DIR%"
    echo Using current directory as target: %TARGET_DIR%
) else (
    :: Create target directory if not exists
    echo Creating target directory...
    if not exist "%TARGET_DIR%" (
        mkdir "%TARGET_DIR%" 2>nul
        if %errorlevel% neq 0 (
            echo Error: Cannot create target directory: %TARGET_DIR%
            echo Please check permissions or run as administrator.
            timeout /t 5 >nul
            exit /b 1
        )
        echo Target directory created successfully.
    ) else (
        echo Target directory already exists.
    )
)

echo Downloading software to: %TARGET_DIR%
echo.

:: Pre-create all software directories
echo Pre-creating software directories...
call :CreateSoftwareDirectories

:: Create PowerShell script
set "PS_TEMP=%TEMP%\simple_download.ps1"

echo $ErrorActionPreference = "Continue" > "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo $gitPlatform = '%GIT_PLATFORM%' >> "%PS_TEMP%"
echo $baseRepo = '%BASE_REPO%' >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo try { >> "%PS_TEMP%"
echo     $listUrl = '%LIST_URL%' >> "%PS_TEMP%"
echo     Write-Host 'Getting software list...' >> "%PS_TEMP%"
echo     $list = (Invoke-WebRequest -Uri $listUrl -TimeoutSec 30).Content ^| ConvertFrom-Json >> "%PS_TEMP%"
echo     Write-Host "Found $($list.software.Count) software packages" >> "%PS_TEMP%"
echo     Write-Host '' >> "%PS_TEMP%"
echo } catch { >> "%PS_TEMP%"
echo     Write-Host 'Cannot get software list' -ForegroundColor Red >> "%PS_TEMP%"
echo     exit 1 >> "%PS_TEMP%"
echo } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
if "%USE_REMOTE_SERVER%"=="1" (
    echo if ($gitPlatform -eq 'remote') { >> "%PS_TEMP%"
    echo     if ($baseRepo.EndsWith('/')) { $baseRepo = $baseRepo.Substring(0, $baseRepo.Length - 1) } >> "%PS_TEMP%"
    echo     $baseUrl = "$baseRepo/software" >> "%PS_TEMP%"
    echo } elseif ($gitPlatform -eq 'gitlab') { >> "%PS_TEMP%"
    echo     if ($baseRepo.EndsWith('/')) { $baseRepo = $baseRepo.Substring(0, $baseRepo.Length - 1) } >> "%PS_TEMP%"
    echo     $baseUrl = "$baseRepo/-/raw/master/software" >> "%PS_TEMP%"
    echo } else { >> "%PS_TEMP%"
    if "%USE_BACKUP%"=="1" (
        echo     $baseUrl = 'https://raw.bgithub.xyz/shellsec/softgitup/refs/heads/master/software' >> "%PS_TEMP%"
    ) else (
        echo     if ($baseRepo -match 'refs/heads/') { >> "%PS_TEMP%"
        echo         $baseUrl = "$baseRepo/software" >> "%PS_TEMP%"
        echo     } else { >> "%PS_TEMP%"
        echo         $baseUrl = 'https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup/refs/heads/master/software' >> "%PS_TEMP%"
        echo     } >> "%PS_TEMP%"
    )
    echo } >> "%PS_TEMP%"
) else (
    echo if ($gitPlatform -eq 'gitlab') { >> "%PS_TEMP%"
    echo     if ($baseRepo.EndsWith('/')) { $baseRepo = $baseRepo.Substring(0, $baseRepo.Length - 1) } >> "%PS_TEMP%"
    echo     $baseUrl = "$baseRepo/-/raw/master/software" >> "%PS_TEMP%"
    echo } else { >> "%PS_TEMP%"
    if "%USE_BACKUP%"=="1" (
        echo     $baseUrl = 'https://raw.bgithub.xyz/shellsec/softgitup/refs/heads/master/software' >> "%PS_TEMP%"
    ) else (
        echo     if ($baseRepo -match 'refs/heads/') { >> "%PS_TEMP%"
        echo         $baseUrl = "$baseRepo/software" >> "%PS_TEMP%"
        echo     } else { >> "%PS_TEMP%"
        echo         $baseUrl = 'https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/softgitup/refs/heads/master/software' >> "%PS_TEMP%"
        echo     } >> "%PS_TEMP%"
    )
    echo } >> "%PS_TEMP%"
)
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
echo             try { >> "%PS_TEMP%"
echo                 New-Item -ItemType Directory -Path $dir -Force ^| Out-Null >> "%PS_TEMP%"
echo                 Write-Host "  [DIR] Created: $dir" -ForegroundColor Green >> "%PS_TEMP%"
echo             } catch { >> "%PS_TEMP%"
echo                 Write-Host "  [ERROR] Failed to create directory: $dir" -ForegroundColor Red >> "%PS_TEMP%"
echo                 Write-Host "  [ERROR] Error: $($_.Exception.Message)" -ForegroundColor Red >> "%PS_TEMP%"
echo                 continue >> "%PS_TEMP%"
echo             } >> "%PS_TEMP%"
echo         } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo         try { >> "%PS_TEMP%"
echo             $webClient.DownloadFile($fileUrl, $localPath) >> "%PS_TEMP%"
echo             $successFiles++ >> "%PS_TEMP%"
echo             Write-Host "  [OK] $($file.path)" -ForegroundColor Green >> "%PS_TEMP%"
echo         } catch { >> "%PS_TEMP%"
echo             Write-Host "  [FAIL] $($file.path)" -ForegroundColor Red >> "%PS_TEMP%"
echo             Write-Host "  [ERROR] $($_.Exception.Message)" -ForegroundColor Red >> "%PS_TEMP%"
echo             if ($_.Exception.Message -like "*permission*" -or $_.Exception.Message -like "*access*") { >> "%PS_TEMP%"
echo                 Write-Host "  [HINT] Try running as administrator or check file permissions" -ForegroundColor Yellow >> "%PS_TEMP%"
echo             } >> "%PS_TEMP%"
echo         } >> "%PS_TEMP%"
echo     } >> "%PS_TEMP%"
echo     Write-Host '' >> "%PS_TEMP%"
echo } >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo $webClient.Dispose() >> "%PS_TEMP%"
echo. >> "%PS_TEMP%"
echo Write-Host '===============================' >> "%PS_TEMP%"
echo Write-Host "Download completed: $successFiles/$totalFiles files" >> "%PS_TEMP%"
echo if ($successFiles -lt $totalFiles) { >> "%PS_TEMP%"
echo     Write-Host "Some files failed to download. Check error messages above." -ForegroundColor Yellow >> "%PS_TEMP%"
echo     Write-Host "Common solutions:" -ForegroundColor Yellow >> "%PS_TEMP%"
echo     Write-Host "1. Run as administrator" -ForegroundColor Yellow >> "%PS_TEMP%"
echo     Write-Host "2. Check internet connection" -ForegroundColor Yellow >> "%PS_TEMP%"
echo     Write-Host "3. Check target directory permissions" -ForegroundColor Yellow >> "%PS_TEMP%"
echo } >> "%PS_TEMP%"
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

goto :eof

:: Function to create all software directories
:CreateSoftwareDirectories
echo Getting software list to pre-create directories...

:: Create temporary PowerShell script to get software list
set "PS_LIST_TEMP=%TEMP%\get_software_list.ps1"

echo $ErrorActionPreference = "Continue" > "%PS_LIST_TEMP%"
echo. >> "%PS_LIST_TEMP%"
echo $gitPlatform = '%GIT_PLATFORM%' >> "%PS_LIST_TEMP%"
echo $baseRepo = '%BASE_REPO%' >> "%PS_LIST_TEMP%"
echo. >> "%PS_LIST_TEMP%"
echo try { >> "%PS_LIST_TEMP%"
echo     $listUrl = '%LIST_URL%' >> "%PS_LIST_TEMP%"
echo     $list = (Invoke-WebRequest -Uri $listUrl -TimeoutSec 30).Content ^| ConvertFrom-Json >> "%PS_LIST_TEMP%"
echo     foreach ($software in $list.software.PSObject.Properties) { >> "%PS_LIST_TEMP%"
echo         $softwareName = $software.Name >> "%PS_LIST_TEMP%"
echo         $softwareDir = Join-Path '%TARGET_DIR%' $softwareName >> "%PS_LIST_TEMP%"
echo         if (!(Test-Path $softwareDir)) { >> "%PS_LIST_TEMP%"
echo             New-Item -ItemType Directory -Path $softwareDir -Force ^| Out-Null >> "%PS_LIST_TEMP%"
echo             Write-Host "Created directory: $softwareName" -ForegroundColor Green >> "%PS_LIST_TEMP%"
echo         } else { >> "%PS_LIST_TEMP%"
echo             Write-Host "Directory exists: $softwareName" -ForegroundColor Yellow >> "%PS_LIST_TEMP%"
echo         } >> "%PS_LIST_TEMP%"
echo     } >> "%PS_LIST_TEMP%"
echo     Write-Host "Directory creation completed." -ForegroundColor Cyan >> "%PS_LIST_TEMP%"
echo } catch { >> "%PS_LIST_TEMP%"
echo     Write-Host 'Failed to get software list for directory creation' -ForegroundColor Red >> "%PS_LIST_TEMP%"
echo     Write-Host 'Will create directories during download process' -ForegroundColor Yellow >> "%PS_LIST_TEMP%"
echo } >> "%PS_LIST_TEMP%"

:: Execute directory creation script
powershell -ExecutionPolicy Bypass -File "%PS_LIST_TEMP%"

:: Clean up
del "%PS_LIST_TEMP%" 2>nul

echo.
goto :eof