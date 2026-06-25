@ECHO OFF&(PUSHD "%~DP0")&(REG QUERY "HKU\S-1-5-19">NUL 2>&1)||(
powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs"&&EXIT)

:: 注册信息
reg add "HKCU\SOFTWARE\ES-Computing\EditPlus\Install" /f /v "License" /t REG_BINARY /d "db892918015e0c5e789ce374ccc951082d4e2d2a963573b37474d23575723534d0b5b48c3272d435750e3773d135700e31360500dbb00a32" >NUL 2>NUL
reg add "HKCU\SOFTWARE\ES-Computing\EditPlus\Install" /f /v "License 5" /t REG_BINARY /d "db892918215e1e5e789c630d63c86728634864c8639035607064706730613063d065f0024213060b065720db19483a024967201b246206c4e140b62b5024142813cec0c000006e00095b" >NUL 2>NUL
reg add "HKCU\SOFTWARE\ES-Computing\EditPlus\Install" /f /v "License 4" /t REG_BINARY /d "db892918215e1d5e789c1589bb11803014c3d4304646a078f9c1006405fa2c103ae6479ccf3e9dbcdd3cbc4c1629a81c04999dd304852e37b7ba4dfe4db643ee9acb67001f4cae0831" >NUL 2>NUL

:Menu
Echo.&Echo  已添加注册信息完成激活！
Echo.&Echo  1、添加右键使用 EditPlus 打开项
Echo.&Echo  2、删除右键使用 EditPlus 打开项
Echo.&Echo  3、清理 EditPlus 注册信息和设置

CHOICE /C 12 /N >NUL 2>NUL
IF "%ERRORLEVEL%"=="2" GOTO RemoveMenu
IF "%ERRORLEVEL%"=="1" GOTO AddMenu

:AddMenu
reg add "HKCR\*\shell\EditPlus" /f /ve /d "用 EditPlus 打开"  >NUL 2>NUL
reg add "HKCR\*\shell\EditPlus" /f /v "Icon" /t REG_EXPAND_SZ /d "%~dp0editplus.exe" >NUL 2>NUL
reg add "HKCR\*\shell\EditPlus\command" /f /ve /d "%~dp0editplus.exe \"%%1\"" >NUL 2>NUL

ECHO.&ECHO 添加完成, 任意键返回!
PAUSE>NUL&CLS&GOTO MENU

:DelMenu
regsvr32 /s /u eppshell64.dll
reg delete "HKCR\*\shell\EditPlus" /f >NUL 2>NUL
reg delete "HKCR\*\shell\EditPlus" /f >NUL 2>NUL
ECHO.&ECHO 删除完成, 任意键返回!
PAUSE>NUL&CLS&GOTO MENU

:Clean
regsvr32 /s /u eppshell64.dll
reg delete "HKCR\*\shell\EditPlus" /f >NUL 2>NUL
reg delete "HKCR\*\shell\EditPlus" /f >NUL 2>NUL
reg delete "HKCU\SOFTWARE\ES-Computing" /f >NUL 2>NUL
reg delete "HKLM\SOFTWARE\ES-Computing" /f >NUL 2>NUL
ECHO.&ECHO 清理完成，任意键返回!
PAUSE>NUL&CLS&GOTO MENU