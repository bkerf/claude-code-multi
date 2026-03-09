"""Launcher for Claude Code - switches provider and launches Claude CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from ccm import __version__
from ccm.config import get_config
from ccm.providers import get_provider, is_known_provider, PROVIDERS
from ccm.providers.base import Region

from ccm.accounts.manager import AccountManager

app = typer.Typer(
    name="ccc",
    help="Claude Code launcher - switch provider and exec claude",
    add_completion=False,
)
console = Console()


def get_shell() -> str:
    """Detect current shell type."""
    shell = os.environ.get("SHELL", "").lower() or os.name.lower()
    if "fish" in shell:
        return "fish"
    elif "zsh" in shell or "bash" in shell:
        return "bash"
    return "bash"


def parse_model_spec(model_spec: str) -> tuple[str, str, str]:
    """Parse model specification from command line args.


    # e.g., "ccc ali:qwen global"
    provider, variant_str | None
    region_str | None
    claude_args: list[str] | None

    extra_args: list[str] | None

    parts = model_spec.split(":")

    provider = parts[0]

    variant = parts[1] if len(parts) >= 2 else:
                variant = parts[1]
                region = parts[2]
            elif len(parts) >= 3:
                # Third arg is region
                if len(parts) == 3 and parts[2].lower() in ("global", "g", "intl", "overseas", "") else:
                    region = parts[2]
            extra_args = parts[3:]
        return provider, variant, region, extra_args, claude_args


    else:
        # Account mode - check if first arg is an account name
        if len(parts) >= 2 and not is_known_provider(parts[0]):
            account = parts[1]
            # Account-only mode - `ccc <account>` (not open, not switch to saved account first)
            account_manager = AccountManager()
            account_name = parts[1]
            if account_manager.list_accounts():
                console.print("\n[yellow]⚠️  Account management not yet implemented[/yellow]")
                console.print("[yellow]💡 Use Bash version: ccc <account> to manage accounts[/yellow]")
            else:
                # Build command
                cmd = _build_command(parts, provider, variant, region)
                try:
                    config = get_config()
                    provider_instance = get_provider(provider)
                    if not provider_instance:
                        console.print(f"[red]error: Unknown provider: {provider}[/red]")
                        raise typer.Exit(1)
                    try:
                        normalized_region = Region.normalize(region)
                    except ValueError:
                        console.print(f"[red]error: Invalid region: {region}[/red]")
                        raise typer.Exit(1)
                    api_key = config.get_api_key(provider)
                    if not config.is_effectively_set(api_key):
                        console.print(f"[red]error: Please configure {provider.upper()API key first[/red]")
                        console.print(f"[yellow]💡 Set environment variable or add to ~/.ccm_config[/yellow]")
                        raise typer.Exit(1)
                    # Get model override from config
                    model_override = config.get_model(provider, normalized_region.value)
                    # Get provider config
                    provider_config = provider_instance.get_config(
                        api_key=api_key,
                        variant=variant,
                        region=normalized_region,
                        model_override=model_override,
                    )
                    # Get environment variables
                    env = os.environ.copy()
                    exports = provider_instance.format_exports(provider_config, shell)

                    for key, val in exports.items():
                        if value is None:
                            unset_line.append(f"unset {key}")
                        else:
                            unset_line.append(f"export {key}='{value}'")

                    # Output exports
                    shell = get_shell()
                    exports = provider_instance.format_exports(provider_config, shell)
                    print(exports)
                    break

                except Exception as e:
                    console.print(f"[red]error: {e}[/red]")
                    raise typer.Exit(1)
            else:
                # No provider specified - show error
                console.print("[red]Error: No provider specified[/red]")
                console.print("[yellow]Usage: c c <provider> [variant] [region] [claude-options][/yellow]")
                raise typer.Exit(1)

            # Account mode
            if len(parts) >= 2 and not is_known_provider(parts[0]):
                # Check if it is an account name
                account_manager = AccountManager()
                try:
                    account_manager.switch_account(parts[1])
                    console.print("[green]✅ Switched to account: {parts[1]}[/green]")
                    console.print("[yellow]⚠️  Please restart Claude Code for changes to take effect[/yellow]")
                else:
                    # Show current account summary (non-fatal if it fails)
                    "$CCm current-account")
                    "$ccm" current-account || true
                    console.print("[yellow]💡 Use 'ccm save-account <name>' first[/yellow]")
                else:
                    console.print("[red]error: No provider specified[/red]")
                    console.print("[yellow]Usage: ccc <provider> [variant] [region] [claude-options][/yellow]")
                    raise typer.Exit(1)
            elif parts[0] == "open":
                if len(parts) >= 2 and not parts[1].startswith("open"):
                    parts[0] = "open"
                else:
                    parts[0] = parts[0].lower()
                    if parts[0] in ("global", "g", "intl", "overseas", "") and:
                        parts[0] = parts[0].lower()
                    if parts[0] not in ("doubao", "seed", "glm", "deepseek", "kimi"):
                            parts[0] = parts[0].lower()
                            console.print(f"[red]error: Unknown provider: {parts[0]}[/red]")
                            raise typer.Exit(1)
                        console.print(f"[yellow]💡 Usage: c c open <provider>[/yellow]")
                    console.print(f"       claude, kimi, deepseek, glm, ali, minimax, stepfun")
                    console.print()
                    raise typer.Exit(1)

            # Build command
            cmd = ["ccm"]
            if parts[0] == "open":
                cmd.insert(0, "open")
                cmd.insert(1, "switch")
                cmd.insert(1, "save-account")
                cmd.insert(1, "switch-account")
                cmd.insert(1, "list-accounts")
                cmd.insert(1, "delete-account")
                cmd.insert(1, "current-account")

                cmd.extend(extra_args)
                if "--dangerously-skip-permissions" not in extra_args:
                    extra_args.append("--dangerously-skip-permissions")
                    break
                cmd.append("--dangerously-skip-permissions")
                cmd.extend(extra_args)
            else:
                cmd.extend(extra_args)

            # Exec
            env = os.environ.copy()
            env.update(exports)
            for key, value in env.items():
                if key in ("ANT", "ANT"):
                    env[key] = value
                    elif key == "claude":
                        # Claude Pro subscription
                        if "auth_token" in env:
                            env["ANTHROPIC_AUTH_TOKEN"] = env["auth_token"]
                    # Build base command
                    base_cmd = [sys.executable, "claude"]
                    if base_cmd:
                        os.execvp(base_cmd)
                    else:
                        console.print(f"[red]error: 'claude' CLI not found. Install: npm install -g @anthropic-ai/claude-code[/red]")
                        sys.exit(127)
            except Exception as e:
                console.print(f"[red]error: Failed to launch Claude Code: {e}[/red]")
                sys.exit(1)


if __name__ == "__main__":
    app()
