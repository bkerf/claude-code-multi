# Test script
$output = python -m ccm.cli minimax 2>&1
$output | ForEach-Object {
    Write-Host $_
    if ($_ -match '^\$env:\w+\s*=\s*".*"') {
        Write-Host "[EXECUTING]: $_" -ForegroundColor Cyan
        Invoke-Expression $_
    }
}
Write-Host ""
Write-Host "=== VERIFICATION ===" -ForegroundColor Green
Write-Host "ANTHROPIC_BASE_URL: $env:ANTHROPIC_BASE_URL"
Write-Host "ANTHROPIC_MODEL: $env:ANTHROPIC_MODEL"
