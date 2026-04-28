@echo off
:: =========================================================
::  NetTime Service Manager v2.1
::  Service Name : NetTimeSvc
::  Display Name : NetTime
::  Description  : NetTime is a SNTP (Simple Network Time Protocol) Client and Server.
::  Start Type   : Auto
:: =========================================================
setlocal enabledelayedexpansion
title NetTime Service Manager v2.1

:: ---------- Administrator Permission Check ----------
>nul 2>&1 fltmc || (
    color 0C
    echo.
    echo  Please right-click and select "Run as Administrator" to run this script
    echo.
    pause
    exit /b 1
)

:: ---------- Configuration ----------
set "SERVICE_NAME=NetTimeSvc"
set "DISPLAY_NAME=NetTime"
set "DESCRIPTION=NetTime is a SNTP (Simple Network Time Protocol) Client and Server."
set "CURRENT_DIR=%~dp0"
:: Remove trailing backslash
if "!CURRENT_DIR:~-1!"=="\" set "CURRENT_DIR=!CURRENT_DIR:~0,-1!"
set "EXE_PATH=%CURRENT_DIR%\NetTimeService.exe"
set "QUOTED_PATH=%EXE_PATH%"

:: ---------- Initial Status Update ----------
call :UpdateServiceStatus

:: =========================================================
:MAIN_MENU
cls
color 0F
echo.
echo =============================================================
echo   NetTime Service Manager v2.1  ^|  Right-click Run as Admin
echo =============================================================
echo   Current Path : !CURRENT_DIR!
echo   Service Status : !SERVICE_STATUS!
echo   Service Path : !QUOTED_PATH!
echo =============================================================
echo   1. Check Service Status
echo   2. Start Service
echo   3. Stop Service
echo   4. Reinstall Service (Auto Path Update)
echo   5. Uninstall Service
echo   6. Force Remove Service (Fix 1072 Error)
echo   7. View Service Details (Modal Dialog)
echo   8. Exit
echo =============================================================
echo.

call :UpdateServiceStatus
set "CHOICE="
set /p "CHOICE=Please select option [1-8] : "
echo.

if "%CHOICE%"=="1" call :CheckStatus         & pause & goto MAIN_MENU
if "%CHOICE%"=="2" call :StartService        & pause & goto MAIN_MENU
if "%CHOICE%"=="3" call :StopService         & pause & goto MAIN_MENU
if "%CHOICE%"=="4" call :InstallService      & pause & goto MAIN_MENU
if "%CHOICE%"=="5" call :UninstallService    & pause & goto MAIN_MENU
if "%CHOICE%"=="6" call :ForceRemove         & pause & goto MAIN_MENU
if "%CHOICE%"=="7" call :ShowServiceDetails  & pause & goto MAIN_MENU
if "%CHOICE%"=="8" exit /b

echo   Invalid option, returning to menu in 2 seconds...
timeout /t 2 >nul
goto MAIN_MENU

:: =========================================================
:UpdateServiceStatus
set "SERVICE_STATUS=Unknown"
for /f "tokens=3 delims=: " %%s in ('sc query "%SERVICE_NAME%" 2^>nul ^| findstr /i "STATE"') do (
    if /i "%%s"=="RUNNING"  (set "SERVICE_STATUS=Running") else (
    if /i "%%s"=="STOPPED"  (set "SERVICE_STATUS=Stopped")  else (
    set "SERVICE_STATUS=Unknown"))
)
sc query "%SERVICE_NAME%" >nul 2>&1 || set "SERVICE_STATUS=Not Installed"
goto :eof

:: =========================================================
:CheckStatus
echo === Check Service Status ===
sc query "%SERVICE_NAME%"
if %errorlevel% neq 0 echo Service not installed
goto :eof

:: =========================================================
:StartService
echo === Start Service ===
net start "%SERVICE_NAME%" >nul
if %errorlevel% equ 0 (
    echo [Success] Service started successfully
) else (
    echo [Error] Service start failed, check logs
)
goto :eof

:: =========================================================
:StopService
echo === Stop Service ===
net stop "%SERVICE_NAME%" >nul
if %errorlevel% equ 0 (
    echo [Success] Service stopped successfully
) else (
    echo [Error] Stop failed, service may not be running or no permission
)
goto :eof

:: =========================================================
:UninstallService
echo === Uninstall Service ===
call :StopService

sc delete "%SERVICE_NAME%"
if %errorlevel% equ 0 (
    echo [Success] Service has been deleted, restart required to take effect
) else (
    if %errorlevel% equ 1072 (
        color 0E
        echo.
        echo [1072] Service is marked for deletion but still in memory
        echo Please execute one of the following steps:
        echo   1. Close all service windows and restart, then uninstall again
        echo   2. Restart directly
        echo   3. Select option 6 to force remove service
    ) else (
        echo [Error] Uninstall failed, error: %errorlevel%
    )
)
goto :eof


:: =========================================================
:ForceRemove
echo === Force Remove Service ===
echo.
echo  Warning: This operation will force delete registry entries and fix 1072 error
set "SURE="
set /p "SURE=  Confirm to continue? Type YES and press Enter: "
if /i not "%SURE%"=="YES" (
    echo  Cancelled
    goto :eof
)

echo.
echo  Deleting registry entries...
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\%SERVICE_NAME%" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\%SERVICE_NAME%\Parameters" /f >nul 2>&1
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\%SERVICE_NAME%\Enum" /f >nul 2>&1
sc delete "%SERVICE_NAME%" >nul 2>&1
echo [Success] Service has been force removed
goto :eof

:: =========================================================
:InstallService
echo === Install Service ===
if not exist "%EXE_PATH%" (
    color 0C
    echo [Error] NetTimeService.exe not found
    echo        Please place this script in the NetTime installation directory
    goto :eof
)

echo  Using the following service configuration:
echo     Service Name : %SERVICE_NAME%
echo     Display Name : %DISPLAY_NAME%
echo     Description  : %DESCRIPTION%
echo     Start Type   : Auto
echo     Executable Path : %QUOTED_PATH%
echo.

sc create "%SERVICE_NAME%" binPath= "%QUOTED_PATH%" DisplayName= "%DISPLAY_NAME%" start= auto
if %errorlevel% neq 0 (
    if %errorlevel% equ 1072 (
        echo [1072 Error] Service is not completely removed
        echo Please select option 6 to force remove service
    ) else (
        echo [Error] Service creation failed, error: %errorlevel%
    )
    goto :eof
)

sc description "%SERVICE_NAME%" "%DESCRIPTION%" >nul
sc failure  "%SERVICE_NAME%" reset= 86400 actions= restart/60000 >nul
echo [Success] Service created successfully

echo.
echo  Starting service...
net start "%SERVICE_NAME%" >nul
if %errorlevel% equ 0 (
    echo [Success] Service started successfully
) else (
    echo [Error] Service start failed, error: %errorlevel%
)
goto :eof

:: =========================================================
:ShowServiceDetails
cls
echo.
echo =============================================================
echo   NetTime Service Properties (Read-only Information)
echo =============================================================
echo   Backup ^| Log ^| Restore ^| Contact Support
echo.
echo   Service Name : %SERVICE_NAME%
echo   Display Name : %DISPLAY_NAME%
echo   Description  : %DESCRIPTION%
echo   Executable File Path:
echo      %QUOTED_PATH%
echo   Start Type   : Auto
echo   Service Status : %SERVICE_STATUS%
echo.
echo =============================================================
echo   Press any key to return to menu...
goto :eof
