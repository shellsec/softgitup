@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Configure AdGuard DNS (DoH)

echo ========================================
echo    Configure AdGuard DNS (DoH)
echo ========================================
echo.

:: Check administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Please run as administrator!
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [OK] Administrator privileges detected
echo.

:: AdGuard DNS configuration (Default - blocks ads, trackers, malware)
set "DNS_PRIMARY=94.140.14.14"
set "DNS_SECONDARY=94.140.15.15"
set "DOH_TEMPLATE=https://dns.adguard-dns.com/dns-query"

echo [INFO] AdGuard DNS Configuration:
echo   Primary DNS: %DNS_PRIMARY%
echo   Secondary DNS: %DNS_SECONDARY%
echo   DoH Template: %DOH_TEMPLATE%
echo.
echo [NOTE] AdGuard DNS is FREE and blocks:
echo   - Ads and trackers
echo   - Known malicious websites
echo   - Adult content (optional)
echo.

:: Get active network adapter
echo [Step 1] Detecting active network adapter...
for /f "tokens=*" %%i in ('netsh interface show interface ^| findstr /i "Connected"') do (
    for /f "tokens=3*" %%j in ("%%i") do (
        set "ADAPTER_NAME=%%k"
        goto :found_adapter
    )
)

:: Try to get Ethernet adapter
for /f "tokens=*" %%i in ('netsh interface show interface ^| findstr /i "Ethernet"') do (
    for /f "tokens=3*" %%j in ("%%i") do (
        set "ADAPTER_NAME=%%k"
        goto :found_adapter
    )
)

:: Manual input if not found
echo [WARNING] Cannot auto-detect network adapter
echo.
echo Please manually enter adapter name (e.g., Ethernet, WLAN)
set /p ADAPTER_NAME="Enter adapter name: "
if "!ADAPTER_NAME!"=="" (
    echo [ERROR] No adapter name entered
    pause
    exit /b 1
)

:found_adapter
echo [OK] Found network adapter: %ADAPTER_NAME%
echo.

:: Set DNS server addresses
echo [Step 2] Setting DNS server addresses...
netsh interface ipv4 set dns name="%ADAPTER_NAME%" static %DNS_PRIMARY% primary >nul 2>&1
if %errorlevel% neq 0 (
    netsh interface ip set dns name="%ADAPTER_NAME%" static %DNS_PRIMARY% >nul 2>&1
)

netsh interface ipv4 add dns name="%ADAPTER_NAME%" %DNS_SECONDARY% index=2 >nul 2>&1
if %errorlevel% neq 0 (
    netsh interface ip add dns name="%ADAPTER_NAME%" %DNS_SECONDARY% index=2 >nul 2>&1
)

echo [OK] DNS server addresses configured
echo.

:: Configure DoH template via PowerShell
echo [Step 3] Configuring DoH encryption template...
echo    This may take a few seconds, please wait...
echo.

set "PS_SCRIPT=%TEMP%\configure_doh_adguard.ps1"

(
echo $ErrorActionPreference = 'Stop'
echo $OutputEncoding = [System.Text.Encoding]::UTF8
echo.
echo # Get first active network adapter ^(avoid encoding issues^)
echo $adapter = Get-NetAdapter ^| Where-Object { $_.Status -eq 'Up' } ^| Select-Object -First 1
echo.
echo if ($null -eq $adapter^) {
echo     Write-Host "[ERROR] Cannot find active network adapter" -ForegroundColor Red
echo     exit 1
echo }
echo.
echo $adapterGuid = $adapter.InterfaceGuid
echo $adapterName = $adapter.Name
echo Write-Host "[INFO] Adapter: $adapterName" -ForegroundColor Cyan
echo Write-Host "[INFO] Adapter GUID: $adapterGuid" -ForegroundColor Cyan
echo.
echo # DoH configuration base path
echo $basePath = 'HKLM:\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters'
echo $dohBasePath = "$basePath\DohInterfaceSettings"
echo.
echo # Create base path if not exists
echo if (!(Test-Path $dohBasePath^)^) {
echo     try {
echo         $null = New-Item -Path $dohBasePath -Force
echo         Write-Host "[OK] Created DoH base path" -ForegroundColor Green
echo     } catch {
echo         Write-Host "[WARNING] Failed to create DoH base path: $_" -ForegroundColor Yellow
echo     }
echo }
echo.
echo # DoH configuration path for this adapter
echo $dohPath = Join-Path $dohBasePath $adapterGuid
echo.
echo # Create adapter GUID path if not exists
echo if (!(Test-Path $dohPath^)^) {
echo     try {
echo         $null = New-Item -Path $dohPath -Force
echo         Write-Host "[OK] Created adapter GUID path" -ForegroundColor Green
echo     } catch {
echo         Write-Host "[ERROR] Failed to create adapter GUID path: $_" -ForegroundColor Red
echo         Write-Host "[INFO] You may need to manually configure DoH in system settings" -ForegroundColor Yellow
echo         exit 1
echo     }
echo }
echo.
echo # Configure primary DNS DoH
echo $primaryKey = Join-Path $dohPath '94.140.14.14'
echo if (!(Test-Path $primaryKey^)^) {
echo     try {
echo         $null = New-Item -Path $primaryKey -Force
echo         Write-Host "[OK] Created primary DNS key" -ForegroundColor Green
echo     } catch {
echo         Write-Host "[ERROR] Failed to create primary DNS key: $_" -ForegroundColor Red
echo         exit 1
echo     }
echo }
echo try {
echo     Set-ItemProperty -Path $primaryKey -Name 'Template' -Value '%DOH_TEMPLATE%' -Type String -Force
echo     Set-ItemProperty -Path $primaryKey -Name 'Flags' -Value 1 -Type DWord -Force
echo     Write-Host "[OK] Primary DNS DoH configured: %DOH_TEMPLATE%" -ForegroundColor Green
echo } catch {
echo     Write-Host "[ERROR] Failed to configure primary DNS DoH: $_" -ForegroundColor Red
echo     Write-Host "[INFO] Path: $primaryKey" -ForegroundColor Yellow
echo }
echo.
echo # Configure secondary DNS DoH
echo $secondaryKey = Join-Path $dohPath '94.140.15.15'
echo if (!(Test-Path $secondaryKey^)^) {
echo     try {
echo         $null = New-Item -Path $secondaryKey -Force
echo         Write-Host "[OK] Created secondary DNS key" -ForegroundColor Green
echo     } catch {
echo         Write-Host "[ERROR] Failed to create secondary DNS key: $_" -ForegroundColor Red
echo         exit 1
echo     }
echo }
echo try {
echo     Set-ItemProperty -Path $secondaryKey -Name 'Template' -Value '%DOH_TEMPLATE%' -Type String -Force
echo     Set-ItemProperty -Path $secondaryKey -Name 'Flags' -Value 1 -Type DWord -Force
echo     Write-Host "[OK] Secondary DNS DoH configured: %DOH_TEMPLATE%" -ForegroundColor Green
echo } catch {
echo     Write-Host "[ERROR] Failed to configure secondary DNS DoH: $_" -ForegroundColor Red
echo     Write-Host "[INFO] Path: $secondaryKey" -ForegroundColor Yellow
echo }
echo.
echo Write-Host "[OK] DoH configuration completed!" -ForegroundColor Green
) > "%PS_SCRIPT%"

:: Execute PowerShell script
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
set "PS_RESULT=%errorlevel%"

:: Cleanup
del "%PS_SCRIPT%" >nul 2>&1

if %PS_RESULT% neq 0 (
    echo.
    echo [WARNING] DoH configuration may not be fully effective
    echo [TIP] Please verify DoH configuration in system settings
    echo.
) else (
    echo.
    echo [OK] DoH configuration completed
    echo.
)

:: Flush DNS cache
echo [Step 4] Flushing DNS cache...
ipconfig /flushdns >nul 2>&1
echo [OK] DNS cache flushed
echo.

:: Verification
echo ========================================
echo    Configuration Completed!
echo ========================================
echo.
echo [Verification] Please verify configuration:
echo.
echo 1. Check system settings:
echo    Settings ^> Network ^& Internet ^> Ethernet (or WLAN^)
echo    ^> Hardware properties ^> DNS server assignment
echo    Should show "Encrypted"
echo.
echo 2. Test DNS resolution:
echo    Open browser and visit some websites
echo    Ads should be blocked automatically
echo.
echo 3. If DoH is not effective, you may need to:
echo    - Restart network adapter
echo    - Or manually enable DoH in system settings
echo.
echo [INFO] AdGuard DNS Features:
echo   - Blocks ads and trackers
echo   - Blocks known malicious websites
echo   - Fast and reliable DNS resolution
echo   - FREE public DNS service
echo.
echo ========================================
echo.

pause

