; ==============================================
; 只屏蔽多余快捷键
; 保留：Ctrl+C/V/X/Z/A/S 等所有正常编辑快捷键
; ==============================================

; 禁用 Win 键（防止误触 Win+D/Win+E 等）
LWin::return
RWin::return

; 禁用 Alt+Tab 切换窗口
!Tab::return
!+Tab::return

; 禁用 Ctrl+Esc 打开开始菜单
^Esc::return

; 禁用 Alt+Esc 切换窗口
!Esc::return

; 禁用 Ctrl+Shift+Esc 任务管理器
^+Esc::return

; 禁用 Alt+F4 关闭窗口
!F4::return

; 禁用 PrintScreen 截图
PrintScreen::return
^PrintScreen::return
!PrintScreen::return

; 禁用一些常见全局快捷键
^!d::return    ; 有些软件用的显示桌面
^!t::return    ; 有些浏览器/软件新建窗口
^+a::return    ; 防止某些软件冲突，系统全选 Ctrl+A 不受影响
^+z::return

; 下面这些完全保留，不会动：
; Ctrl+C 复制
; Ctrl+V 粘贴
; Ctrl+X 剪切
; Ctrl+Z 撤销
; Ctrl+A 全选
; Ctrl+S 保存
; Ctrl+F 查找
; 所有正常输入、打字都正常