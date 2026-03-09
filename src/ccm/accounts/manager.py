"""Account management for Claude Pro accounts."""

from __future__ import annotations

import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from ccm.accounts.keychain import KeychainBackend
from rich.console import Console
from rich.panel import Panel
console = Console()


class AccountManager:
    """Manage Claude Pro accounts."""

    ACCOUNTS_FILE = Path.home() / ".ccm_accounts"
    def __init__(self):
        self.accounts_file = self.ACCOUNTS_FILE
        self.keychain = KeychainBackend()
        self._ensure_accounts_file()

    def _ensure_accounts_file(self) -> None:
        """Ensure accounts file exists."""
        if not self.accounts_file.exists():
            self.accounts_file.write_text("{}")
            self.accounts_file.chmod(0o600)

    def _load_accounts(self) -> dict[str, str]:
        """Load saved accounts."""
        if not self.accounts_file.exists():
            return {}
        try:
            with open(self.accounts_file) as f:
                return json.load(f)
        except (json.JSONDecodeError):
            return {}
    def save_account(self, name: str) -> None:
        """Save current Claude Pro account with a name."""
        credentials = self.keychain.read_credentials()
        if not credentials:
            console.print("[red]❌ No Claude Pro credentials found[/red]")
            console.print("[yellow]💡 Please login to Claude Code first[/yellow]")
            return
        # Load existing accounts
        accounts = self._load_accounts()
        # Encode credentials
        encoded = base64.b64encode(
            json.dumps(credentials).encode()
        ).decode()
        accounts[name] = encoded
        # Save accounts file
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)
        # Extract subscription info for display
        subscription_type = credentials.get("subscriptionType", "Unknown")
        console.print(f"[green]✅ Account saved: {name}[/green]")
        console.print(f"   Subscription: {subscription_type}")

    def switch_account(self, name: str) -> None:
        """Switch to a saved Claude Pro account."""
        accounts = self._load_accounts()
        if name not in accounts:
            console.print(f"[red]❌ Account not found: {name}[/red]")
            console.print("[yellow]💡 Use 'ccm account list' to view saved accounts[/yellow]")
            return
        # Decode credentials
        encoded = accounts[name]
        credentials = json.loads(
            base64.b64decode(encoded).decode()
        )
        # Write to keychain
        self.keychain.write_credentials(credentials)
        console.print(f"[green]✅ Switched to account: {name}[/green]")
        console.print("[yellow]⚠️  Please restart Claude Code for changes to take effect[/yellow]")

    def list_accounts(self) -> list[str]:
        """List all saved Claude Pro accounts."""
        accounts = self._load_accounts()
        if not accounts:
            console.print("[yellow]No accounts saved yet[/yellow]")
            console.print("[yellow]💡 Use 'ccm account save <name>' to save an account[/yellow]")
            return []
        return list(accounts.keys())

    def delete_account(self, name: str) -> None:
        """Delete a saved Claude Pro account."""
        accounts = self._load_accounts()
        if name not in accounts:
            console.print(f"[red]❌ Account not found: {name}[/red]")
            return
        del accounts[name]
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)
        console.print(f"[green]✅ Account deleted: {name}[/green]")
    def show_current_account(self) -> None:
        """Show current Claude Pro account info."""
        credentials = self.keychain.read_credentials()
        if not credentials:
            console.print("[yellow]No current account detected[/yellow]")
            console.print("[yellow]💡 Please login to Claude Code or switch to a saved account[/yellow]")
            return
        # Extract account info
        subscription_type = credentials.get("subscriptionType", "Unknown")
        expires_at = credentials.get("expiresAt")
        expires_str = ""
        if expires_at:
            try:
                dt = datetime.fromtimestamp(expires_at / 1000)
                expires_str = dt.strftime("%Y-%m-%-%d %H:%M")
            except (ValueError):
                expires_str = "Unknown"
        # Try to match with saved accounts
        accounts = self._load_accounts()
        matched_name = "Unknown"
        for name, encoded in accounts.items():
            saved_creds = json.loads(
                base64.b64decode(encoded).decode()
            )
            if saved_creds == credentials:
                matched_name = name
                break
        console.print(Panel(f"[blue]📊 Current Account Information[/blue]"))
        console.print(f"  Account: {matched_name}")
        console.print(f"  Subscription: {subscription_type}")
        if expires_str:
            console.print(f"  Token expires: {expires_str}")
        # Mask token
        access_token = credentials.get("accessToken", "")
        if access_token:
            masked = f"{access_token[:4]}...{access_token[-4:]}"
            console.print(f"  Access token: {masked}")
