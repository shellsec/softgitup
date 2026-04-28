@ECHO OFF&(REG QUERY "HKU\S-1-5-19">NUL 2>&1)||(powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs"&&EXIT)

schtasks /delete /tn "Wise Care 365.job" /f  >NUL 2>NUL
schtasks /delete /tn "Wise Turbo Checker.job" /f  >NUL 2>NUL 
rd/s/q "%AppData%\Wise Care 365"2>NUL

reg delete "HKLM\SOFTWARE\Classes\.wskn" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Classes\W365.SkinFile" /f >NUL 2>NUL 
reg delete "HKLM\SOFTWARE\WiseCleaner\WiseCare365" /f >NUL 2>NUL 
reg delete "HKLM\SOFTWARE\Classes\*\shell\WShredFile" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\WiseCleaner\WiseCare365" /f /reg:32 >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Classes\Folder\shell\WShredFile" /f >NUL 2>NUL
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\WiseHDInfo" /f >NUL 2>NUL
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\WiseRegNotify" /f >NUL 2>NUL
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\WiseBootAssistant" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Microsoft\Tracing\WiseTray_RASAPI32" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\Classes\CLSID\{7BEFAB15-7B27-4361-80E1-3B61C9E06392}" /f >NUL 2>NUL

ECHO.&ECHO 清理完成！
ECHO.&ECHO ghxi.com
TIMEOUT /t 2 >NUL&EXIT