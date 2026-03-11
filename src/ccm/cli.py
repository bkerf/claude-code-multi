"""CLI for Claude Code Model Switcher."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional, Callable

import typer
from rich.console import Console
from rich.table import Table

from ccm import __version__

app = typer.Typer(
    name="ccm",
    help="Claude Code Model Switcher - Cross-platform CLI to switch AI providers",
    add_completion=False,
)
console = Console()


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
    if value and value and not value.startswith("your-") and not value.startswith("sk-your"):
        return "[Set]"
    return "[Not Set]"


# ============================================================================
# Dynamic service command (new config system)
# ============================================================================


def switch_service(service_name: str):
    """Switch to a service from the new config system and output export statements."""
    from ccm.config.services import get_services_config

    try:
        config = get_services_config()
    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        console.print("[yellow]💡 复制 ccm_services.template 到 ~/.ccm_services 并填写 API Key[/yellow]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        raise typer.Exit(1)

    service = config.get_service(service_name)
    if not service:
        console.print(f"[red]❌ Unknown service: {service_name}[/red]")
        console.print(f"[yellow]💡 可用服务: {', '.join(config.list_services())}[/yellow]")
        raise typer.Exit(1)

    # Check API key
    if not service.api_key:
        console.print(f"[red]❌ Service '{service_name}' 未配置 api_key[/red]")
        console.print(f"[yellow]💡 编辑 ~/.ccm_services 并设置 api_key[/yellow]")
        raise typer.Exit(1)

    # Get provider config
    provider_config = service.to_provider_config()

    # Show status
    console.print(f"\n[green]✅ Switched to {service_name}[/green]")
    console.print(f"   [blue]Type:[/blue] {service.type}")
    console.print(f"   [blue]Model:[/blue] {provider_config.model}")
    console.print(f"   [blue]Base URL:[/blue] {provider_config.base_url}")
    console.print()

    # Output export statements
    shell = get_shell()
    exports: list[str] = []

    if shell == "powershell":
        exports.append(f'$env:ANTHROPIC_BASE_URL = "{provider_config.base_url}"')
        if provider_config.auth_token:
            exports.append(f'$env:{provider_config.auth_env_var} = "{provider_config.auth_token}"')
        exports.append(f'$env:ANTHROPIC_MODEL = "{provider_config.model}"')
        exports.append(f'$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "{provider_config.default_sonnet or provider_config.model}"')
        exports.append(f'$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "{provider_config.default_opus or provider_config.model}"')
        exports.append(f'$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "{provider_config.default_haiku or provider_config.model}"')
        exports.append(f'$env:CLAUDE_CODE_SUBAGENT_MODEL = "{provider_config.subagent_model or provider_config.model}"')
        exports.append(f'$env:CLAUDE_CODE_EFFORT_LEVEL = "{provider_config.effort_level}"')
        exports.append(f'$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "{provider_config.disable_nonessential_traffic}"')
        exports.append(f'$env:CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "{provider_config.experimental_agent_teams}"')
    elif shell == "fish":
        exports.append(f"set -gx ANTHROPIC_BASE_URL '{provider_config.base_url}'")
        if provider_config.auth_token:
            exports.append(f"set -gx {provider_config.auth_env_var} '{provider_config.auth_token}'")
        exports.append(f"set -gx ANTHROPIC_MODEL '{provider_config.model}'")
        exports.append(f"set -gx ANTHROPIC_DEFAULT_SONNET_MODEL '{provider_config.default_sonnet or provider_config.model}'")
        exports.append(f"set -gx ANTHROPIC_DEFAULT_OPUS_MODEL '{provider_config.default_opus or provider_config.model}'")
        exports.append(f"set -gx ANTHROPIC_DEFAULT_HAIKU_MODEL '{provider_config.default_haiku or provider_config.model}'")
        exports.append(f"set -gx CLAUDE_CODE_SUBAGENT_MODEL '{provider_config.subagent_model or provider_config.model}'")
        exports.append(f"set -gx CLAUDE_CODE_EFFORT_LEVEL '{provider_config.effort_level}'")
        exports.append(f"set -gx CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC '{provider_config.disable_nonessential_traffic}'")
        exports.append(f"set -gx CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS '{provider_config.experimental_agent_teams}'")
    else:
        # bash/zsh
        exports.append(f"export ANTHROPIC_BASE_URL='{provider_config.base_url}'")
        if provider_config.auth_token:
            exports.append(f"export {provider_config.auth_env_var}='{provider_config.auth_token}'")
        exports.append(f"export ANTHROPIC_MODEL='{provider_config.model}'")
        exports.append(f"export ANTHROPIC_DEFAULT_SONNET_MODEL='{provider_config.default_sonnet or provider_config.model}'")
        exports.append(f"export ANTHROPIC_DEFAULT_OPUS_MODEL='{provider_config.default_opus or provider_config.model}'")
        exports.append(f"export ANTHROPIC_DEFAULT_HAIKU_MODEL='{provider_config.default_haiku or provider_config.model}'")
        exports.append(f"export CLAUDE_CODE_SUBAGENT_MODEL='{provider_config.subagent_model or provider_config.model}'")
        exports.append(f"export CLAUDE_CODE_EFFORT_LEVEL='{provider_config.effort_level}'")
        exports.append(f"export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='{provider_config.disable_nonessential_traffic}'")
        exports.append(f"export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS='{provider_config.experimental_agent_teams}'")

    print("\n".join(exports))

    # Print environment variables summary
    console.print("\n[blue]📋 Environment Variables[/blue]")
    console.print(f"   ANTHROPIC_BASE_URL='{provider_config.base_url}'")
    if provider_config.auth_token:
        masked = f"{provider_config.auth_token[:4]}...{provider_config.auth_token[-4:]}" if len(provider_config.auth_token) > 8 else "****"
        console.print(f"   {provider_config.auth_env_var}='{masked}'")
    console.print(f"   ANTHROPIC_MODEL='{provider_config.model}'")
    console.print()


def create_service_command(service_name: str) -> Callable:
    """Create a command function for a service."""
    def command():
        switch_service(service_name)
    command.__name__ = service_name
    command.__doc__ = f"Switch to {service_name} service."
    return command


# ============================================================================
# Status command
# ============================================================================


@app.command()
def status():
    """Show current configuration status."""
    console.print("\n[blue]📊 Current Configuration[/blue]")
    console.print(f"   BASE_URL: {os.environ.get('ANTHROPIC_BASE_URL', 'Default (Anthropic)')}")
    console.print(f"   AUTH_TOKEN: {mask_token(os.environ.get('ANTHROPIC_AUTH_TOKEN') or os.environ.get('ANTHROPIC_API_KEY'))}")
    console.print(f"   MODEL: {os.environ.get('ANTHROPIC_MODEL', '[Not Set]')}")
    console.print(f"   SUBAGENT_MODEL: {os.environ.get('CLAUDE_CODE_SUBAGENT_MODEL', '[Not Set]')}")
    console.print()


@app.command(name="list")
def list_services():
    """List all configured services."""
    from ccm.config.services import get_services_config

    try:
        config = get_services_config()
    except (FileNotFoundError, ValueError):
        console.print("[yellow]⚠️  配置文件不存在或无效[/yellow]")
        console.print("[yellow]💡 复制 ccm_services.template 到 ~/.ccm_services.toml[/yellow]")
        return

    table = Table(title="Configured Services")
    table.add_column("Service", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Base URL", style="blue")
    table.add_column("API Key", style="yellow")

    for name, service in config.services.items():
        api_status = "✓" if service.api_key else "✗"
        table.add_row(
            name,
            service.type,
            service.base_url,
            api_status,
        )

    console.print(table)


@app.command(name="config")
def config_cmd():
    """Open configuration file for editing."""
    config_path = Path.home() / ".ccm_services"

    if not config_path.exists():
        console.print(f"[yellow]📝 Creating config file from template...[/yellow]")
        template_path = Path(__file__).parent.parent.parent.parent / "ccm_services.template"
        if template_path.exists():
            import shutil as sh
            sh.copy(template_path, config_path)
            console.print(f"[green]✅ Created: {config_path}[/green]")
        else:
            console.print(f"[red]❌ Template not found: {template_path}[/red]")
            return

    console.print(f"[green]📝 Opening config file: {config_path}[/green]")

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


# ============================================================================
# Main entry point
# ============================================================================


def register_dynamic_commands():
    """Register dynamic commands from services config."""
    from ccm.config.services import get_services_config

    try:
        config = get_services_config()
        for service_name in config.list_services():
            # Skip if command already exists
            if service_name in ["status", "list", "config"]:
                continue
            app.command(name=service_name)(create_service_command(service_name))
    except (FileNotFoundError, ValueError):
        # Config not ready, skip dynamic commands
        pass


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[bool, typer.Option("--version", "-v", help="Show version")] = False,
):
    """Claude Code Model Switcher - Cross-platform CLI to switch AI providers."""
    if version:
        console.print(f"ccm version {__version__}")
        sys.exit(0)

    # Register dynamic commands on first run
    register_dynamic_commands()

    # If no subcommand provided, show help
    if len(sys.argv) == 1:
        from ccm.config.services import get_services_config

        console.print("\n[bold yellow]Usage:[/bold yellow] ccm <service> [options]")
        console.print("\n[bold]Commands:[/bold]")

        try:
            config = get_services_config()
            services = config.list_services()
            # Show first 10 services
            for name in services[:10]:
                service = config.get_service(name)
                if service:
                    api_status = "✓" if service.api_key else "✗"
                    console.print(f"  {name:<16} {service.type} ({api_status})")
            if len(services) > 10:
                console.print(f"  ... and {len(services) - 10} more (use 'ccm list' to see all)")
        except (FileNotFoundError, ValueError):
            console.print("  [yellow]Configure ~/.ccm_services to enable services[/yellow]")

        console.print("\n[bold]Management:[/bold]")
        console.print("  status           Show current configuration")
        console.print("  config           Open configuration file for editing")
        console.print("  list             List all configured services")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  eval \"$(ccm kimi)\"         # Switch to Kimi")
        console.print("  eval \"$(ccm ali-qwen-cn)\"  # Switch to Alibaba Qwen China")
        console.print("  ccc kimi                    # Switch and launch Claude Code")
        sys.exit(0)


def run():
    """Entry point for the CLI."""
    register_dynamic_commands()
    app()


if __name__ == "__main__":
    run()
