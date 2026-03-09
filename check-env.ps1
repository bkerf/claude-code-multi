# Check where MINIMAX env var is set
Write-Host "=== Current Session Env Vars ===" -ForegroundColor Cyan
Get-ChildItem Env: | Where-Object { $_.Name -like '*MINIMAX*' }

Write-Host ""
Write-Host "=== Machine Level Env Vars ===" -ForegroundColor Cyan
[System.Environment]::GetEnvironmentVariable('MINIMAX_API_KEY', 'Machine')

Write-Host ""
Write-Host "=== User Level Env Vars ===" -ForegroundColor Cyan
[System.Environment]::GetEnvironmentVariable('MINIMAX_API_KEY', 'User')
