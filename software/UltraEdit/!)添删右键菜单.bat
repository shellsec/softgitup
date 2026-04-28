@ECHO OFF&(PUSHD "%~DP0")&(REG QUERY "HKU\S-1-5-19">NUL 2>&1)||(
powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs"&&EXIT)

rd/s/q "%AppData%\IDMComp\UltraEdit"2>NUL

:MENU
ECHO.&ECHO  1、添加资源管理器右键菜单项
ECHO.&ECHO  2、删除资源管理器右键菜单项

CHOICE /C 12 /N >NUL 2>NUL
IF "%ERRORLEVEL%"=="2" GOTO RemoveMenu
IF "%ERRORLEVEL%"=="1" GOTO AddMenu

:AddMenu
reg add "HKCR\*\OpenWithList\uedit64.exe" /f >NUL 2>NUL
reg add "HKCR\*\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" >NUL 2>NUL
reg add "HKCR\Applications\uedit64.exe\shell\edit\Command" /f /ve /d "\"%~dp0uedit64.exe\" \"%%1\"" >NUL 2>NUL
reg add "HKCR\Applications\uedit64.exe\shell\open\Command" /f /ve /d "\"%~dp0uedit64.exe\" \"%%1\"" >NUL 2>NUL
reg add "HKCR\Applications\uedit64.exe\shell\print\Command" /f /ve /d "\"%~dp0uedit64.exe\" /p \"%%1\"" >NUL 2>NUL
reg add "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /ve /d "%~dp0ue64ctmn.dll" >NUL 2>NUL
reg add "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /v "ThreadingModel" /d "Apartment" >NUL 2>NUL
reg add "HKCR\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" >NUL 2>NUL
reg add "HKCR\*\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" /reg:32 >NUL 2>NUL
reg add "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /ve /d "%~dp0ue32ctmn.dll" /reg:32 >NUL 2>NUL
reg add "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /v "ThreadingModel" /d "Apartment" /reg:32 >NUL 2>NUL
reg add "HKCR\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" /reg:32 >NUL 2>NUL
reg add "HKCU\Software\Classes\*\OpenWithList\uedit64.exe" /f /ve /d "" >NUL 2>NUL
reg add "HKCU\Software\Classes\*\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" >NUL 2>NUL
reg add "HKCU\Software\Classes\Applications\uedit64.exe\shell\edit\Command" /f /ve /d "\"%~dp0uedit64.exe\" \"%%1\"" >NUL 2>NUL
reg add "HKCU\Software\Classes\Applications\uedit64.exe\shell\open\Command" /f /ve /d "\"%~dp0uedit64.exe\" \"%%1\"" >NUL 2>NUL
reg add "HKCU\Software\Classes\Applications\uedit64.exe\shell\print\Command" /f /ve /d "\"%~dp0uedit64.exe\" /p \"%%1\"" >NUL 2>NUL
reg add "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /ve /d "%~dp0ue64ctmn.dll" >NUL 2>NUL
reg add "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /v "ThreadingModel" /d "Apartment" >NUL 2>NUL
reg add "HKCU\Software\Classes\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" >NUL 2>NUL
reg add "HKCU\Software\Classes\*\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" /reg:32 >NUL 2>NUL
reg add "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /ve /d "%~dp0ue32ctmn.dll" /reg:32 >NUL 2>NUL
reg add "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}\InProcServer32" /f /v "ThreadingModel" /d "Apartment" /reg:32 >NUL 2>NUL
reg add "HKCU\Software\Classes\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /ve /d "{b5eedee0-c06e-11cf-8c56-444553540000}" /reg:32 >NUL 2>NUL
reg add "HKCU\Software\IDM Computer Solutions\UltraEdit" /f /v "ContextFolderMenuText" /d "用 UltraEdit 打开" >NUL 2>NUL
reg add "HKCU\Software\IDM Computer Solutions\UltraEdit" /f /v "ContextMenuText" /d "&UltraEdit" >NUL 2>NUL
reg add "HKCU\Software\IDM Computer Solutions\UltraEdit" /f /v "FirstRun" /d "1" >NUL 2>NUL
reg add "HKCU\Software\IDM Computer Solutions\UltraEdit" /f /v "IntegrateWithExplorer" /t REG_DWORD /d "1" >NUL 2>NUL
reg add "HKCU\Software\IDM Computer Solutions\UltraEdit\Locks" /f >NUL 2>NUL
ECHO.&ECHO 完成 &TIMEOUT /t 2 >NUL&CLS&GOTO MENU

:RemoveMenu
reg delete "HKCR\*\OpenWithList\uedit64.exe" /f >NUL 2>NUL
reg delete "HKCR\*\shellex\ContextMenuHandlers\UltraEdit" /f >NUL 2>NUL
reg delete "HKCR\Applications\uedit64.exe" /f >NUL 2>NUL
reg delete "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}" /f >NUL 2>NUL
reg delete "HKCR\Folder\shellex\ContextMenuHandlers\UltraEdit" /f >NUL 2>NUL
reg delete "HKCR\*\shellex\ContextMenuHandlers\UltraEdit" /f /reg:32 >NUL 2>NUL
reg delete "HKCR\CLSID\{9b4c79e8-d476-48e1-ad17-2253d0531ebb}" /f /reg:32 >NUL 2>NUL
reg delete "HKCR\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}" /f /reg:32 >NUL 2>NUL
reg delete "HKCR\CLSID\{bf2611c5-cf99-4e19-be15-83e593688709}" /f /reg:32 >NUL 2>NUL
reg delete "HKCR\CLSID\{c0bf323d-faa8-4b16-bdc9-92c6acb76dc1}" /f /reg:32 >NUL 2>NUL
reg delete "HKCR\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /reg:32 >NUL 2>NUL
reg delete "HKCU\Software\Classes\*\OpenWithList\uedit64.exe" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\*\shellex\ContextMenuHandlers\UltraEdit" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\Applications\uedit64.exe" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\Folder\shellex\ContextMenuHandlers\UltraEdit" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\*\shellex\ContextMenuHandlers\UltraEdit" /f /reg:32 >NUL 2>NUL
reg delete "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}" /f /reg:32 >NUL 2>NUL
reg delete "HKCU\Software\Classes\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /reg:32 >NUL 2>NUL
reg delete "HKCU\Software\IDM Computer Solutions\UltraEdit" /f >NUL 2>NUL

ECHO.&ECHO 完成 &TIMEOUT /t 2 >NUL&CLS&GOTO MENU