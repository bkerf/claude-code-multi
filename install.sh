#!/usr/bin/env bash
set -euo pipefail

# Claude Code Model Switcher - Install Script
# Supported: macOS, Linux, WSL

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

check_pip() {
    if command -v pip3 &>/dev/null; then
        echo "pip3"
    elif command -v pip &>/dev/null; then
        echo "pip"
    else
        log_error "pip not found. Please install Python and pip first."
    fi
}

main() {
    local pip
    pip=$(check_pip)

    log_info "Installing claude-code-multi via $pip..."
    $pip install -U claude-code-multi

    log_info "Installation complete!"

    # Check PATH
    if command -v ccm &>/dev/null; then
        log_info "Run 'ccm --help' to get started."
    else
        log_warn "ccm command not found. Add this to your shell rc:"
        echo ""
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then run: source ~/.zshrc  (or ~/.bashrc)"
    fi
}

main "$@"
