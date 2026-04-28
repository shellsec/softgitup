@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Restore Default DNS Settings

echo ========================================
echo    Restore Default DNS Settings
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

:: Restore DNS to automatic (DHCP)
echo [Step 2] Restoring DNS to automatic (DHCP)...
netsh interface ipv4 set dns name="%ADAPTER_NAME%" dhcp >nul 2>&1
if %errorlevel% neq 0 (
    netsh interface ip set dns name="%ADAPTER_NAME%" dhcp >nul 2>&1
)

echo [OK] DNS restored to automatic (DHCP)
echo.

:: Remove DoH configuration via PowerShell
echo [Step 3] Removing DoH encryption configuration...
echo    This may take a few seconds, please wait...
echo.

set "PS_SCRIPT=%TEMP%\restore_dns.ps1"

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
echo # DoH configuration path
echo $dohPath = "HKLM:\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters\DohInterfaceSettings\$adapterGuid"
echo.
echo # Remove DoH configuration if exists
echo if (Test-Path $dohPath^) {
echo     try {
echo         Remove-Item -Path $dohPath -Recurse -Force
echo         Write-Host "[OK] DoH configuration removed" -ForegroundColor Green
echo     } catch {
echo         Write-Host "[WARNING] Failed to remove DoH configuration: $_" -ForegroundColor Yellow
echo         Write-Host "[INFO] You may need to manually remove DoH settings in system settings" -ForegroundColor Yellow
echo     }
echo } else {
echo     Write-Host "[INFO] No DoH configuration found" -ForegroundColor Cyan
echo }
echo.
echo Write-Host "[OK] DNS restore completed!" -ForegroundColor Green
) > "%PS_SCRIPT%"

:: Verify script file was created
if not exist "%PS_SCRIPT%" (
    echo [ERROR] Failed to create PowerShell script file
    echo [INFO] Path: %PS_SCRIPT%
    echo [TIP] Check TEMP directory permissions
    pause
    exit /b 1
)

:: Execute PowerShell script
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
set "PS_RESULT=%errorlevel%"

:: Cleanup
del "%PS_SCRIPT%" >nul 2>&1

if %PS_RESULT% neq 0 (
    echo.
    echo [WARNING] Some operations may have failed
    echo [TIP] Please check system settings manually
    echo.
) else (
    echo.
    echo [OK] DoH configuration removed
    echo.
)

:: Flush DNS cache
echo [Step 4] Flushing DNS cache...
ipconfig /flushdns >nul 2>&1
echo [OK] DNS cache flushed
echo.

:: Verification
echo ========================================
echo    DNS Restore Completed!
echo ========================================
echo.
echo [INFO] DNS settings have been restored to default:
echo   - DNS server: Automatic (DHCP^)
echo   - DoH encryption: Removed
echo.
echo [Verification] Please verify:
echo.
echo 1. Check system settings:
echo    Settings ^> Network ^& Internet ^> Ethernet (or WLAN^)
echo    ^> Hardware properties ^> DNS server assignment
echo    Should show "Automatic (DHCP^)"
echo.
echo 2. If DNS is still not automatic:
echo    - Restart network adapter
echo    - Or manually set to "Automatic" in system settings
echo.
echo 3. If DoH is still enabled:
echo    - Manually disable DoH in system settings
echo    - Or restart your computer
echo.
echo ========================================
echo.

pause

