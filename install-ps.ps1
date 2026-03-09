# Claude Code Model Switcher - PowerShell Installer
# Run this script to set up ccm/ccc functions in PowerShell

$ProfileContent = @'

# ============================================================================
# CCM - Claude Code Model Switcher
# ============================================================================

function ccm {
    <#
    .SYNOPSIS
    Switch Claude Code AI provider

    .EXAMPLE
    ccm glm china    # Switch to GLM China
    ccm kimi global  # Switch to Kimi Global
    ccm minimax      # Switch to MiniMax
    ccm list         # List all providers
    ccm status       # Show current config
    #>
    # Try installed command first, fallback to python -m
    $cmd = Get-Command ccm -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.CommandType -eq "Application") {
        $output = & ccm $args 2>&1
    } else {
        $output = python -m ccm.cli $args 2>&1
    }
    $output | ForEach-Object {
        Write-Host $_
        if ($_ -match '^\$env:\w+\s*=\s*".*"') {
            Invoke-Expression $_
        }
    }
}

function ccc {
    <#
    .SYNOPSIS
    Switch provider and launch Claude Code

    .EXAMPLE
    ccc glm china    # Switch to GLM China and launch
    ccc kimi         # Switch to Kimi and launch
    #>
    # Try installed command first, fallback to python -m
    $cmd = Get-Command ccc -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.CommandType -eq "Application") {
        & ccc $args
    } else {
        python -m ccm.launcher $args
    }
}

# ============================================================================

'@

$ProfilePath = $PROFILE

# Check if already installed
if (Test-Path $ProfilePath) {
    $existingContent = Get-Content $ProfilePath -Raw
    if ($existingContent -match "# CCM - Claude Code Model Switcher") {
        Write-Host "CCM already installed in PowerShell profile." -ForegroundColor Yellow
        Write-Host "To reinstall, remove the CCM section from $ProfilePath and run again." -ForegroundColor Yellow
        exit 0
    }
}

# Append to profile
Add-Content -Path $ProfilePath -Value $ProfileContent

Write-Host @"

========================================
CCM installed successfully!
========================================

Profile: $ProfilePath

To use ccm/ccc now, reload your profile:

    . `$PROFILE

Or restart PowerShell.

Usage:
    ccm glm china     # Switch to GLM China
    ccm kimi global   # Switch to Kimi Global
    ccm minimax       # Switch to MiniMax
    ccm list          # List all providers
    ccm status        # Show current config
    ccm config        # Edit config file

    ccc glm china     # Switch and launch Claude Code

"@
