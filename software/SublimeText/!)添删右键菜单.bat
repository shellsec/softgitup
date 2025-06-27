@ECHO OFF&(PUSHD "%~DP0")&(REG QUERY "HKU\S-1-5-19">NUL 2>&1)||(
powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs"&&EXIT)

VER|FINDSTR "5\.[0-9]\.[0-9][0-9]*" > NUL && (
ECHO.&ECHO 当前版本不支持WinXP &PAUSE>NUL&EXIT)

rd/s/q "%AppData%\Sublime Text" 2>NUL

:MENU
ECHO.&ECHO 1、添加系统右键 Sublime Text 打开项
ECHO.&ECHO 2、移除系统右键 Sublime Text 打开项
IF EXIST "%WinDir%\System32\CHOICE.exe" CHOICE /C 12 /N >NUL 2>NUL
IF EXIST "%WinDir%\System32\CHOICE.exe" IF "%ERRORLEVEL%"=="2" GOTO RemoveMenu
IF EXIST "%WinDir%\System32\CHOICE.exe" IF "%ERRORLEVEL%"=="1" GOTO AddMenu
IF NOT EXIST "%WinDir%\System32\CHOICE.exe" ECHO.&SET /p choice=输入数字项敲回车键：
IF NOT EXIST "%WinDir%\System32\CHOICE.exe" IF NOT "%choice%"=="" SET choice=%choice:~0,1%
IF NOT EXIST "%WinDir%\System32\CHOICE.exe" IF /I "%choice%"=="1" GOTO AddMenu
IF NOT EXIST "%WinDir%\System32\CHOICE.exe" IF /I "%choice%"=="2" GOTO RemoveMenu
IF NOT EXIST "%WinDir%\System32\CHOICE.exe" ECHO.&ECHO 输入无效 &PAUSE&CLS&GOTO MENU

:AddMenu
reg add "HKCR\*\shell\Sublime Text" /f /v "" /d "用 &Sublime Text 打开" >NUL 2>NUL
reg add "HKCR\*\shell\Sublime Text" /f /v "Icon" /d "%~dp0sublime_text.exe" >NUL 2>NUL
reg add "HKCR\*\shell\Sublime Text\command" /f /v "" /d "%~dp0sublime_text.exe \"%%1\"" >NUL 2>NUL
IF EXIST "%WinDir%\System32\CHOICE.exe" ( 
ECHO.&ECHO 添加完成
ECHO.&ECHO 423Down.com
TIMEOUT /t 2 >NUL & CLS & GOTO MENU
) ELSE ( 
ECHO.&ECHO 已添加，任意键返回 &PAUSE>NUL&CLS&GOTO MENU) 

:RemoveMenu
reg delete "HKCR\*\shell\Sublime Text" /f >NUL 2>NUL
reg delete "HKLM\*\shell\Sublime Text" /f >NUL 2>NUL
IF EXIST "%WinDir%\System32\CHOICE.exe" ( 
ECHO.&ECHO 移除完成
ECHO.&ECHO ghxi.com
TIMEOUT /t 2 >NUL & CLS & GOTO MENU
) ELSE ( 
ECHO.&ECHO 已删除，任意键返回 &PAUSE>NUL&CLS&GOTO MENU) 