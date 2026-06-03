@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "ROOT=%~dp0.."
set "REPORT=%~dp0reports\index.html"

:menu
cls
echo.
echo  ============================================================
echo   SoftGitUp · soft_page_check 月度更新 SOP
echo  ============================================================
echo.
echo   原则: 不更 software/ 也完全可用 ^| 有变化再动手 ^| 破解须手工下载
echo.
echo   [1] 完整月度 SOP（推荐，带步骤引导）
echo   [2] 仅 A 类快检（约 15 秒 + 报告页）
echo   [3] 仅发布（已手工更新 software，直接 push）
echo   [4] 季度 423down digest 检查
echo   [5] 7xiazai 软件页检查（~650+ 软件 title）
echo   [6] 打开 HTML 报告页
echo   [7] list 三站检查（系统+移动 分开，hybase/dayanzai/down66）
echo   [0] 退出
echo.
set /p "MENU=请选择 [0-7]: "
if "%MENU%"=="1" goto sop
if "%MENU%"=="2" goto quick_only
if "%MENU%"=="3" goto push_only
if "%MENU%"=="4" goto digest
if "%MENU%"=="5" goto xiazai
if "%MENU%"=="6" goto open_report
if "%MENU%"=="7" goto list_sites
if "%MENU%"=="0" exit /b 0
echo 无效选项，请重试。
timeout /t 2 /nobreak >nul
goto menu

:run_a_check
echo.
echo  --- 正在运行 A 类快检 ---
python extract_pages.py
if errorlevel 1 goto check_fail
python build_watchlist.py
if errorlevel 1 goto check_fail
python fetch_titles.py --scope a --compare
if errorlevel 1 goto check_fail
if exist "%REPORT%" start "" "%REPORT%"
echo.
if exist "changed_tier_a_urls.txt" (
    call :count_lines "changed_tier_a_urls.txt"
    echo  A 类标题变化: %CHG% 个（见报告页）
) else (
    echo  无 changed_tier_a_urls.txt（可能无变化或首次运行需再快检一次）
)
goto :eof

:count_lines
set "CHG=0"
if not exist "%~1" exit /b 0
for /f "usebackq delims=" %%L in ("%~1") do set /a CHG+=1
exit /b 0

:check_fail
echo [错误] 快检失败，请查看上方 Python 输出。
pause
exit /b 1

:quick_only
call :run_a_check
echo.
pause
goto menu

:open_report
if exist "%REPORT%" (
    python report_html.py >nul 2>&1
    start "" "%REPORT%"
) else (
    echo 报告不存在，请先运行快检。
    pause
)
goto menu

:digest
echo.
echo  --- 423down digest 全量（约 356 条，1~2 分钟）---
call monthly_check_423down.bat
goto menu

:xiazai
echo.
echo  --- 7xiazai 软件详情页 title ---
call monthly_check_7xiazai.bat
goto menu

:list_sites
echo.
echo  --- list 三站（hybase + dayanzai + down66）---
call monthly_check_list.bat
goto menu

:push_only
echo.
echo  --- 发布: 生成 list.txt 并 push ---
cd /d "%ROOT%"
call generate_and_push.bat
echo.
echo 请在各客户端运行 sync_software.bat 拉取更新。
pause
cd /d "%~dp0"
goto menu

:sop
cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 1/5 · A 类快检
echo  ============================================================
echo.
echo   将: 刷新 URL -^> 抓取 A 类页面标题 -^> 与历史比对 -^> 打开报告页
echo   首次使用需连续完成两次月度 SOP 或快检，第二次才有「标题变化」。
echo.
choice /C YN /M "是否现在运行 A 类快检"
if errorlevel 2 goto sop_step2_skip_check
call :run_a_check
goto sop_step2

:sop_step2_skip_check
echo 已跳过快检。
if exist "%REPORT%" (
    choice /C YN /M "是否打开已有报告页"
    if not errorlevel 2 (
        python report_html.py >nul 2>&1
        start "" "%REPORT%"
    )
)

:sop_step2
cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 2/5 · 查看报告
echo  ============================================================
echo.
echo   报告: soft_page_check\reports\index.html
echo.
echo   请看「A 类 · 同步软件」分区:
echo     - 标题变化 = 0  ^-^>  本月通常无需更新，可直接结束
echo     - 有变化        ^-^>  点链接或「依次打开变化页」人工确认
echo.
echo   提示: 标题变化不等于必须更新（423down SEO 也会触发）
echo.
pause

cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 3/5 · 是否更新 software/
echo  ============================================================
echo.
choice /C YN /M "本次是否要更新 software 目录中的软件包"
if errorlevel 2 goto sop_done_no_update

cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 3 续 · 下载与替换（手工）
echo  ============================================================
echo.
echo   [GitHub · soft_page_check 内下载（仅快检有变化的项）]
echo     fetch_github_on_changes.bat
echo.
echo   [423down / 网盘 / 破解版 · 浏览器手工]
echo     报告页打开链接 -^> 下载 -^> 解压替换到:
echo     %ROOT%\software\对应子目录\
echo.
choice /C YN /M "是否现在按 GitHub 变化下载 Release（fetch_github_on_changes）"
if not errorlevel 2 (
    call "%~dp0fetch_github_on_changes.bat" --dry-run
    echo.
    choice /C YN /M "确认执行下载"
    if not errorlevel 2 call "%~dp0fetch_github_on_changes.bat"
)

echo.
echo 请完成手工下载并替换 software\ 下对应目录后按任意键继续...
pause

cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 4/5 · 更新文档（可选）
echo  ============================================================
echo.
echo   若修改了软件版本或链接，可编辑:
echo     %ROOT%\Lastb_soft_version.txt  （装机区说明）
echo.
echo   可选: 在 digest 区追加一行  # [YYYY-MM-DD] 本月变更摘要
echo.
echo   按任意键继续（不编辑文档也可直接发布）...
pause

cls
echo.
echo  ============================================================
echo   月度更新 SOP · 步骤 5/5 · 发布与客户端同步
echo  ============================================================
echo.
echo   generate_and_push.bat 将:
echo     - 复制 Lastb_soft_version.txt 到 system_good
echo     - 生成 software\list.txt
echo     - 执行 push_git.bat
echo.
choice /C YN /M "是否已替换 software 并准备发布到 Git"
if errorlevel 2 goto sop_done_manual_only

cd /d "%ROOT%"
call generate_and_push.bat
cd /d "%~dp0"
echo.
echo  [完成] 请在各客户端运行 sync_software.bat 拉取更新。
pause
goto menu

:sop_done_no_update
cls
echo.
echo  ============================================================
echo   本月 SOP 完成 · 无需更新
echo  ============================================================
echo.
echo   当前 software/ 继续可用。下次想查再运行本 SOP 或 monthly_check.bat
echo.
pause
goto menu

:sop_done_manual_only
cls
echo.
echo  ============================================================
echo   已更新 software/ · 未执行 Git 发布
echo  ============================================================
echo.
echo   需要发布时请选主菜单 [3] 或手动运行:
echo     %ROOT%\generate_and_push.bat
echo.
pause
goto menu
