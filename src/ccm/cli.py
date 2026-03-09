"""CLI for Claude Code Model Switcher."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional

from enum import Enum

import typer
from rich.console import Console
from rich.table import Table

from rich.panel import Panel

from ccm import __version__
from ccm.config import Config, get_config
from ccm.providers import get_provider, is_known_provider, PROVIDERS
from ccm.providers.base import Region
from ccm.accounts.manager import AccountManager

from ccm.accounts.keychain import KeychainBackend

app = typer.Typer(
    name="ccm",
    help="Claude Code Model Switcher - Cross-platform CLI to switch AI providers",
    add_completion=False,
)
console = Console()


class ProviderType(str, Enum):
    """Provider types for dynamic dispatch."""
    DEEPSEEK = "deepseek"
    KIMI = "kimi"
    GLM = "glm"
    MINIMAX = "minimax"
    ALI = "ali"
    SEED = "seed"
    STEPFUN = "stepfun"
    CLAUDE = "claude"
    OPENROUTER = "openrouter"


def get_shell() -> str:
    """Detect current shell type."""
    shell = os.environ.get("SHELL", "").lower()
    # Check for PowerShell on Windows
    if os.name == "nt" or "PSModulePath" in os.environ:
        return "powershell"
    if "fish" in shell:
        return "fish"
    elif "zsh" in shell or "bash" in shell:
        return "bash"
    return "bash"


def mask_token(token: str | None) -> str:
    """Mask a token for display."""
    if not token:
        return "[Not Set]"
    if len(token) <= 8:
        return "[Set] ****"
    return f"[Set] {token[:4]}...{token[-4:]}"


def mask_presence(value: str | None) -> str:
    """Check if a value is effectively set."""
    if value and not _is_placeholder(value):
        return "[Set]"
    return "[Not Set]"


def _is_placeholder(value: str) -> bool:
    """Check if value is a placeholder."""
    lower = value.lower()
    return "your" in lower and "api" in lower and "key" in lower


# ============================================================================
# Dynamic provider command
# ============================================================================


def switch_provider(
    provider_type: ProviderType,
    variant: Annotated[Optional[str], typer.Argument(help="Model variant (e.g., qwen for ali)")] = None,
    region: Annotated[str, typer.Argument(help="Region: china or global (default: china)")] = "china",
):
    """Switch to a provider and output export statements."""
    # Debug: print received parameters
    console.print(f"[dim]🔧 Parameters: provider={provider_type.value}, variant={variant}, region={region}[/dim]")

    config = get_config()
    provider_name = provider_type.value

    provider = get_provider(provider_name)
    if not provider:
        console.print(f"[red]❌ Unknown provider: {provider_name}[/red]")
        raise typer.Exit(1)
    # Get API key
    api_key = config.get_api_key(provider_name)
    if not config.is_effectively_set(api_key):
        key_name = f"{provider_name.upper()}_API_KEY"
        console.print(f"[red]❌ Please configure {key_name}[/red]")
        console.print(f"[yellow]💡 Set environment variable or add to ~/.ccm_config[/yellow]")
        raise typer.Exit(1)
    # Normalize region
    try:
        normalized_region = Region.normalize(region)
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        raise typer.Exit(1)
    # Get model override from config - only use if NO variant is specified
    # When variant is provided, let the provider handle model selection
    model_override = None
    if not variant:
        model_override = config.get_model(provider_name, normalized_region.value)

    # Get provider config
    provider_config = provider.get_config(
        api_key=api_key,
        variant=variant,
        region=normalized_region,
        model_override=model_override,
    )
    # Show status
    info = provider.get_info()
    console.print(f"\n[green]✅ Switched to {info.description}[/green]")
    if info.supports_region:
        console.print(f"   [blue]Region:[/blue] {normalized_region.value}")
    if variant:
        console.print(f"   [blue]Variant:[/blue] {variant}")
    console.print(f"   [blue]Model:[/blue] {provider_config.model}")
    console.print(f"   [blue]Base URL:[/blue] {provider_config.base_url}")
    console.print()
    # Output export statements
    shell = get_shell()
    exports = provider.format_exports(provider_config, shell)
    print(exports)

    # Print environment variables (like Windows does)
    env_vars = provider.get_env_exports(provider_config)
    console.print("\n[blue]📋 Environment Variables[/blue]")
    for key, val in env_vars.items():
        if val is not None:
            # Mask sensitive tokens
            if "TOKEN" in key or "API_KEY" in key or "AUTH" in key:
                masked = f"{val[:4]}...{val[-4:]}" if len(val) > 8 else "****"
                console.print(f"   {key}='{masked}'")
            else:
                console.print(f"   {key}='{val}'")
    console.print()


# ============================================================================
# OpenRouter command
# ============================================================================


@app.command(name="open")
def openrouter(
    provider: Annotated[str, typer.Argument(help="Provider via OpenRouter (claude, kimi, deepseek, glm, stepfun)")] = "claude",
):
    """Switch via OpenRouter."""
    config = get_config()
    api_key = config.api_keys.openrouter
    if not config.is_effectively_set(api_key):
        console.print("[red]❌ Please configure OPENROUTER_API_KEY[/red]")
        raise typer.Exit(1)
    provider_instance = get_provider("openrouter")
    if not provider_instance:
        console.print("[red]❌ OpenRouter provider not available[/red]")
        raise typer.Exit(1)
    provider_config = provider_instance.get_config(
        api_key=api_key,
        variant=provider,
        region=Region.GLOBAL,
    )
    console.print(f"\n[green]✅ Switched to OpenRouter ({provider})[/green]")
    console.print(f"   [blue]Model:[/blue] {provider_config.model}")
    console.print(f"   [blue]Base URL:[/blue] {provider_config.base_url}")
    console.print()
    # Output exports
    shell = get_shell()
    exports = provider_instance.format_exports(provider_config, shell)
    print(exports)


# ============================================================================
# Status command
# ============================================================================


@app.command()
def status():
    """Show current configuration status."""
    config = get_config()

    console.print("\n[blue]📊 Current Configuration[/blue]")
    console.print(f"   BASE_URL: {os.environ.get('ANTHROPIC_BASE_URL', 'Default (Anthropic)')}")
    console.print(f"   AUTH_TOKEN: {mask_token(os.environ.get('ANTHROPIC_AUTH_TOKEN'))}")
    console.print(f"   MODEL: {os.environ.get('ANTHROPIC_MODEL', '[Not Set]')}")
    console.print(f"   SUBAGENT_MODEL: {os.environ.get('CLAUDE_CODE_SUBAGENT_MODEL', '[Not Set]')}")
    console.print()
    console.print("[blue]🔧 API Keys Status[/blue]")
    console.print(f"   GLM_API_KEY: {mask_presence(config.api_keys.glm)}")
    console.print(f"   KIMI_API_KEY: {mask_presence(config.api_keys.kimi)}")
    console.print(f"   MINIMAX_API_KEY: {mask_presence(config.api_keys.minimax)}")
    console.print(f"   DEEPSEEK_API_KEY: {mask_presence(config.api_keys.deepseek)}")
    console.print(f"   ARK_API_KEY: {mask_presence(config.api_keys.ark)}")
    console.print(f"   QWEN_API_KEY: {mask_presence(config.api_keys.qwen)}")
    console.print(f"   OPENROUTER_API_KEY: {mask_presence(config.api_keys.openrouter)}")
    console.print()


@app.command(name="config")
def config_cmd():
    """Open configuration file for editing."""
    config_path = Config.get_config_path()
    if not config_path.exists():
        console.print(f"[green]📝 Opening config file: {config_path}[/green]")
    else:
        console.print(f"[yellow]📝 Creating config file: {config_path}[/yellow]")
        get_config().save()
    # Try editors in order
    editors = ["cursor", "code", "vim", "nano"]
    for editor in editors:
        editor_path = shutil.which(editor)
        if editor_path:
            try:
                console.print(f"[blue]🔧 Opening with {editor}...[/blue]")
                if sys.platform == "win32":
                    os.startfile(str(config_path))
                else:
                    subprocess.run([editor, str(config_path)])
                return
            except Exception:
                continue
    console.print(f"[yellow]No editor found. Edit manually:[/yellow]")
    console.print(f"[white]  {config_path}[/white]")


@app.command(name="list")
def list_providers():
    """List all supported providers."""
    table = Table(title="Supported Providers")
    table.add_column("Provider", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Region", style="yellow")
    table.add_column("Variants", style="magenta")
    seen: set[type[BaseProvider]] = set()
    for name, provider_class in PROVIDERS.items():
        if provider_class in seen:
            continue
        seen.add(provider_class)
        info = provider_class.get_info()
        table.add_row(
            info.name,
            info.description,
            "Yes" if info.supports_region else "No",
            ", ".join(info.variants) if info.variants else "-",
        )
    console.print(table)


# ============================================================================
# User settings commands
# ============================================================================

settings_app = typer.Typer(help="Manage user-level settings")
app.add_typer(settings_app, name="user")


@settings_app.command("set")
def user_settings(
    provider: str,
    region: Annotated[str, typer.Argument(help="Region: china or global (default: global)")] = "global",
):
    """Write provider settings to user-level (~/.claude/settings.json)."""
    _write_settings(provider, region, user=True)


@settings_app.command("reset")
def user_reset():
    """Reset user-level settings."""
    _reset_settings(user=True)


    console.print("[green]✅ Removed user-level settings[/green]")
    console.print("[yellow]💡 Claude Code will now use environment variables[/yellow]")


def _write_settings(provider: str, region: str, user_level: bool = False) -> None:
    """Write provider settings to settings file."""
    from ccm.settings.user import write_user_settings
    from ccm.settings.project import write_project_settings

    from ccm.providers import get_provider
    from ccm.providers.base import Region
    from ccm.config import get_config

    config = get_config()
    provider_lower = provider.lower()
    region_enum = Region.normalize(region)
    provider_instance = get_provider(provider_lower)
    if not provider_instance:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise typer.Exit(1)
    # Get API key
    api_key = config.get_api_key(provider_lower)
    if not config.is_effectively_set(api_key):
        console.print(f"[red]Please configure {provider.upper()}_API_KEY first[/red]")
        raise typer.Exit(1)
    write_user_settings(provider_instance, region_enum, api_key, user_level=user_level)


    console.print(f"[green]✅ Wrote {provider} settings to {'user' if user_level else 'project'} settings[/green]")
    console.print(f"   [blue]File:[/blue] {Config.get_user_settings_path() if user_level else Config.get_project_settings_path()}")
    console.print("[yellow]💡 This overrides environment variables[/yellow]")
    if user_level:
        console.print("[yellow]💡 Use 'ccm user reset' to restore env var control[/yellow]")
    else:
        console.print("[yellow]💡 Use 'ccm project reset' to restore project override[/yellow]")


def _reset_settings(user_level: bool = True) -> None:
    """Reset settings to use environment variables."""
    from ccm.settings.user import reset_user_settings
    from ccm.settings.project import reset_project_settings
    console.print("[green]✅ Reset complete[/green]")
    console.print("[yellow]💡 Claude Code will now use environment variables[/yellow]")


# ============================================================================
# Account management commands
# ============================================================================

account_app = typer.Typer(help="Manage Claude Pro accounts")
app.add_typer(account_app, name="account")


@account_app.command("save")
def account_save(name: str):
    """Save current Claude Pro account with a name."""
    manager = AccountManager()
    manager.save_account(name)
    console.print(f"[green]✅ Account saved: {name}[/green]")


@account_app.command("switch")
def account_switch(name: str):
    """Switch to a saved Claude Pro account."""
    manager = AccountManager()
    manager.switch_account(name)
    console.print(f"[green]✅ Switched to account: {name}[/green]")
    console.print("[yellow]⚠️  Please restart Claude Code for changes to take effect[/yellow]")


@account_app.command("list")
def account_list():
    """List all saved Claude Pro accounts."""
    manager = AccountManager()
    accounts = manager.list_accounts()
    if not accounts:
        console.print("[yellow]No accounts saved yet[/yellow]")
        console.print("[yellow]💡 Use 'ccm account save <name>' to save an account[/yellow]")
        return
    console.print("\n[blue]📋 Saved Accounts[/blue]")
    for name in accounts:
        console.print(f"  - {name}")
    console.print()


@account_app.command("delete")
def account_delete(name: str):
    """Delete a saved Claude Pro account."""
    manager = AccountManager()
    manager.delete_account(name)
    console.print(f"[green]✅ Account deleted: {name}[/green]")


@account_app.command("current")
def account_current():
    """Show current Claude Pro account info."""
    manager = AccountManager()
    manager.show_current_account()


# ============================================================================
# Main entry point for direct provider commands
# ============================================================================


@app.command()
def deepseek():
    """Switch to DeepSeek."""
    switch_provider(ProviderType.DEEPSEEK)


@app.command()
def kimi(region: Annotated[str, typer.Argument(help="china or global (default: global)")] = "global"):
    """Switch to Kimi (Moonshot AI)."""
    switch_provider(ProviderType.KIMI, region=region)


@app.command()
def glm(region: Annotated[str, typer.Argument(help="china or global (default: global)")] = "global"):
    """Switch to GLM (Zhipu AI)."""
    switch_provider(ProviderType.GLM, region=region)


@app.command()
def minimax(region: Annotated[str, typer.Argument(help="china or global (default: china)")] = "china"):
    """Switch to MiniMax."""
    switch_provider(ProviderType.MINIMAX, region=region)


@app.command()
def ali(variant: Annotated[Optional[str], typer.Argument(help="qwen/kimi/glm/minimax")] = None, region: Annotated[str, typer.Argument(help="china or global (default: china)")] = "china"):
    """Switch to Alibaba Cloud Coding Plan.

    Args:
        variant: qwen, kimi, glm, or minimax
        region: china or global (default: china)
    """
    switch_provider(ProviderType.ALI, variant=variant, region=region)


@app.command()
def seed(variant: Annotated[Optional[str], typer.Argument(help="Model variant (doubao/glm/deepseek/kimi)")] = None):
    """Switch to Seed/Doubao (ByteDance).

    Args:
        variant: doubao, glm, deepseek, or kimi
    """
    switch_provider(ProviderType.SEED, variant=variant)


@app.command()
def stepfun():
    """Switch to StepFun."""
    switch_provider(ProviderType.STEPFUN)


@app.command()
def claude():
    """Switch to Claude (official Anthropic)."""
    switch_provider(ProviderType.CLAUDE)


# ============================================================================
# Main entry point
# ============================================================================


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[bool, typer.Option("--version", "-v", help="Show version")] = False,
):
    """Claude Code Model Switcher - Cross-platform CLI to switch AI providers."""
    if version:
        console.print(f"ccm version {__version__}")
        sys.exit(0)
    # If no subcommand provided, show help
    if len(sys.argv) == 1:
        console.print("\n[bold yellow]Usage:[/bold yellow] ccm <command> [options]")
        console.print("\n[bold]Commands:[/bold]")
        console.print("  deepseek         Switch to DeepSeek")
        console.print("  kimi             Switch to Kimi (Moonshot AI)")
        console.print("  glm              Switch to GLM (Zhipu AI)")
        console.print("  minimax          Switch to MiniMax")
        console.print("  ali              Switch to Alibaba Cloud Coding Plan")
        console.print("  seed             Switch to Seed/Doubao (ByteDance)")
        console.print("  stepfun          Switch to StepFun")
        console.print("  claude           Switch to Claude (official Anthropic)")
        console.print("  open             Switch via OpenRouter")
        console.print("  status           Show current configuration")
        console.print("  config           Open configuration file for editing")
        console.print("  list             List all supported providers")
        console.print("\n[bold]Account Management:[/bold]")
        console.print("  account save     Save current Claude Pro account")
        console.print("  account switch   Switch to a saved account")
        console.print("  account list     List all saved accounts")
        console.print("  account delete   Delete a saved account")
        console.print("  account current  Show current account info")
        console.print("\n[bold]Settings:[/bold]")
        console.print("  user set         Write provider settings to user-level")
        console.print("  user reset       Reset user-level settings")
        console.print("  project set      Write provider settings to project-level")
        console.print("  project reset    Reset project-level settings")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  eval \"$(ccm deepseek)\"     # Switch to DeepSeek")
        console.print("  eval \"$(ccm kimi china)\"  # Switch to Kimi China")
        console.print("  eval \"$(ccm ali qwen)\"   # Switch to Alibaba with Qwen")
        sys.exit(0)


def run():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    app()
