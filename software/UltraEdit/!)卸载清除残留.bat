@ECHO OFF&(PUSHD "%~DP0")&(REG QUERY "HKU\S-1-5-19">NUL 2>&1)||(
powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs"&&EXIT)

taskkill /f /im uedit* >NUL 2>NUL
taskkill /f /im ucl.exe >NUL 2>NUL

::清除FTP管理/云服务插件注册表键值
IF EXIST "%ProgramW6432%\IDM Computer Solutions\Common\wodCertificate64.dll" (
regsvr32 /s /u "%ProgramW6432%\IDM Computer Solutions\Common\wodFtpDLX64.dll"
regsvr32 /s /u "%ProgramW6432%\IDM Computer Solutions\Common\wodTelnetDLX64.ocx"
regsvr32 /s /u "%ProgramW6432%\IDM Computer Solutions\Common\wodCertificate64.dll"
rd/s/q "%ProgramW6432%\IDM Computer Solutions"2>NUL
)

rd/s/q "%AppData%\IDMComp"2>NUL
rd/s/q "%ProgramData%\IDMComp"2>NUL
FOR /F "skip=2 tokens=3 " %%i IN ('REG QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v personal') DO (
  FOR /F "delims=*" %%j IN ('ECHO;%%i') DO RD /S/Q "%%j\IDM Computer Solutions"2>NUL)
  

::清除右键菜单关联项注册表相关
reg delete "HKCU\Software\IDM Computer Solutions" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\IDM Computer Solutions" /f >NUL 2>NUL
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
reg delete "HKCU\Software\Classes\*\shellex\ContextMenuHandlers\UltraEdit" /f >NUL 2>NUL
reg delete "HKCU\Software\Classes\CLSID\{b5eedee0-c06e-11cf-8c56-444553540000}" /f /reg:32 >NUL 2>NUL
reg delete "HKCU\Software\Classes\Folder\shellex\ContextMenuHandlers\UltraEdit" /f /reg:32 >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\uedit64.exe" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\uedit64.exe" /f >NUL 2>NUL


reg delete "HKCU\Software\IDM Computer Solutions" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\IDM Computer Solutions" /f >NUL 2>NUL
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
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\uedit64.exe" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\uedit64.exe" /f >NUL 2>NUL


ECHO.&ECHO 清理完成！
TIMEOUT /t 3 >NUL&EXIT