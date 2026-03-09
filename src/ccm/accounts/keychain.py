"""Cross-platform key keychain backend using keyring library."""

from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

from rich.console import Console

console = Console()


class KeychainBackend:
    """Cross-platform keychain backend."""

    # Service names to try for Claude Code credentials
    SERVICE_NAMES = [
        "Claude Code-credentials",
        "Claude Code - credentials",
        "Claude Code",
        "claude",
        "claude.ai",
    ]
    # Credentials file path (for Linux)
    CREDENTIALS_FILE = Path.home() / ".claude" / ".credentials.json"
    def __init__(self):
        """Initialize keychain backend."""
        self.system = platform.system().lower()
    def read_credentials(self) -> dict[str, Any] | None:
        """Read Claude Code credentials from keychain."""
        if self.system == "darwin":
            return self._read_macos_keychain()
        elif self.system == "linux":
            return self._read_linux_credentials()
        elif self.system == "windows":
            return self._read_windows_credentials()
        else:
            console.print(f"[yellow]⚠️  Unsupported OS: {self.system}[/yellow]")
            return None
    def _read_macos_keychain(self) -> dict[str, Any] | None:
        """Read credentials from macOS Keychain."""
        import subprocess
        for service in self.SERVICE_NAMES:
            try:
                result = subprocess.run(
                    ["security", "find-generic-password", "-s", service, "-w"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 and result.stdout.strip():
                    credentials = json.loads(result.stdout.strip())
                    if credentials:
                        return credentials
            except (subprocess.CalledProcessError):
                continue
        return None
    def _read_linux_credentials(self) -> dict[str, Any] | None:
        """Read credentials from Linux file."""
        if not self.CREDENTIALS_FILE.exists():
            return None
        try:
            with open(self.CREDENTIALS_FILE) as f:
                data = json.load(f)
            return data.get("claudeAiOauth")
        except (json.JSONDecodeError):
            return None
    def _read_windows_credentials(self) -> dict[str, Any] | None:
        """Read credentials from Windows Credential Manager."""
        try:
            import keyring
            for service in self.SERVICE_NAMES:
                try:
                    credentials = keyring.get_password("claude-code", service)
                    if credentials:
                        return json.loads(credentials)
                except keyring.errors.KeyringError:
                    continue
        except ImportError:
            console.print("[yellow]⚠️  keyring library not available[/yellow]")
            return None
        return None
    def write_credentials(self, credentials: dict[str, Any]) -> None:
        """Write credentials to keychain."""
        if self.system == "darwin":
            self._write_macos_keychain(credentials)
        elif self.system == "linux":
            self._write_linux_credentials(credentials)
        elif self.system == "windows":
            self._write_windows_credentials(credentials)
    def _write_macos_keychain(self, credentials: dict[str, Any]) -> None:
        """Write credentials to macOS Keychain."""
        import subprocess
        username = os.environ.get("USER", "unknown")
        service = self.SERVICE_NAMES[0]  # Try each service name
        for svc in service:
            # Delete existing
            subprocess.run(["security", "delete-generic-password", "-s", svc], capture_output=True)
            # Add new
            json_credentials = json.dumps(credentials)
            result = subprocess.run(
                ["security", "add-generic-password", "-a", username, "-s", svc, "-w", json_credentials],
                capture_output=True,
            )
            if result.returncode == 0:
                console.print(f"[blue]🔑 Credentials written to Keychain (service: {svc})[/blue]")
                return
        console.print("[red]❌ Failed to write to Keychain[/red]")
    def _write_linux_credentials(self, credentials: dict[str, Any]) -> None:
        """Write credentials to Linux file."""
        # Ensure directory exists
        self.CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Load existing data
        data: dict[str, Any] = {}
        if self.CREDENTIALS_FILE.exists():
            try:
                with open(self.CREDENTIALS_FILE) as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        # Update claudeAiOauth
        data["claudeAiOauth"] = credentials
        # Write
        self.CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CREDENTIALS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        self.CREDENTIALS_FILE.chmod(0o600)
        console.print(f"[blue]🔑 Credentials written to file: {self.CREDENTIALS_FILE}[/blue]")
    def _write_windows_credentials(self, credentials: dict[str, Any]) -> None:
        """Write credentials to Windows Credential Manager."""
        try:
            import keyring
            username = os.environ.get("USERNAME", "unknown")
            service = self.SERVICE_NAMES[0]
            # Try each service name
            for svc in service:
                try:
                    keyring.set_password("claude-code", svc, json.dumps(credentials))
                    console.print(f"[blue]🔑 Credentials written to Windows Credential Manager[/blue]")
                    return
                except keyring.errors.KeyringError:
                    continue
        except ImportError:
            console.print("[yellow]⚠️  keyring library not available[/yellow]")
