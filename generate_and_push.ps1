# SoftGitUp - 一键生成和推送工具 (PowerShell版本)
Write-Host "========================================" -ForegroundColor Green
Write-Host "SoftGitUp - 一键生成和推送工具" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "正在生成软件列表..." -ForegroundColor Yellow
python soft_manager.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "软件列表生成成功！" -ForegroundColor Green
    Write-Host "已自动推送到GitHub" -ForegroundColor Green
    Write-Host ""
    Write-Host "操作完成！" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "操作失败，请检查错误信息" -ForegroundColor Red
}

Write-Host ""
Read-Host "按回车键继续" 