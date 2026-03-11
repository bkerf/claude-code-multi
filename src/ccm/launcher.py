"""Launcher for Claude Code - switches provider and launches Claude CLI."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import Annotated, Callable

import typer
from rich.console import Console

from ccm import __version__

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
    return "bash"


def launch_claude(env: dict) -> None:
    """Launch Claude Code with environment."""
    # Find claude executable
    claude_cmd = None
    for cmd_name in ["claude"]:
        claude_cmd = shutil.which(cmd_name)
        if claude_cmd:
            break

    if not claude_cmd:
        console.print("[red]error: 'claude' CLI not found. Install: npm install -g @anthropic-ai/claude-code[/red]")
        sys.exit(127)

    # Windows: use PowerShell to launch with focus
    if os.name == "nt":
        import tempfile

        cwd = os.getcwd()

        # Create temporary script with environment variables
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
            script_path = f.name
            # Write environment variables
            for key, val in env.items():
                if val is not None:
                    # Skip environment variables with special characters in names
                    # PowerShell doesn't support parentheses in $env: syntax
                    if '(' in key or ')' in key:
                        continue
                    val_escaped = val.replace("'", "''")
                    f.write(f"$env:{key}='{val_escaped}'\n")
            # Change to working directory and launch claude
            f.write(f"Set-Location '{cwd}'\n")
            f.write("claude --dangerously-skip-permissions\n")

        # Try to launch with Windows Terminal, fallback to PowerShell
        wt_path = shutil.which("wt.exe")
        if wt_path:
            # Use Windows Terminal (profile will be loaded)
            try:
                subprocess.Popen(
                    [wt_path, "new-tab", "--title", "Claude Code", "powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", script_path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                )
                console.print("[dim]Launched in Windows Terminal[/dim]")
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to launch Windows Terminal: {e}[/yellow]")
                # Fallback to regular PowerShell
                subprocess.Popen(
                    ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", script_path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                )
                console.print("[dim]Launched in PowerShell[/dim]")
        else:
            # No Windows Terminal, use regular PowerShell (profile will be loaded)
            subprocess.Popen(
                ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
            )
            console.print("[dim]Launched in PowerShell[/dim]")

        sys.exit(0)
    else:
        # Unix/macOS: launch in current terminal with env vars
        try:
            # Set environment variables and launch
            env_copy = os.environ.copy()
            env_copy.update(env)

            # Use subprocess to launch claude in the same terminal
            result = subprocess.run(
                [claude_cmd, "--dangerously-skip-permissions"],
                env=env_copy
            )
            sys.exit(result.returncode)
        except FileNotFoundError:
            console.print(f"[red]error: 'claude' command not found at {claude_cmd}[/red]")
            sys.exit(127)
        except Exception as e:
            console.print(f"[red]error: Failed to launch Claude Code: {e}[/red]")
            sys.exit(1)


def switch_and_launch(service_name: str):
    """Switch service and launch Claude Code."""
    from ccm.config.services import get_services_config

    try:
        config = get_services_config()
    except FileNotFoundError as e:
        console.print(f"[red]error: {e}[/red]")
        console.print("[yellow]💡 复制 ccm_services.template 到 ~/.ccm_services.toml[/yellow]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[red]error: {e}[/red]")
        raise typer.Exit(1)

    service = config.get_service(service_name)
    if not service:
        console.print(f"[red]error: Unknown service: {service_name}[/red]")
        console.print(f"[yellow]💡 可用服务: {', '.join(config.list_services())}[/yellow]")
        raise typer.Exit(1)

    # Check API key
    if not service.api_key:
        console.print(f"[red]error: Service '{service_name}' 未配置 api_key[/red]")
        console.print("[yellow]💡 编辑 ~/.ccm_services.toml 设置 api_key[/yellow]")
        raise typer.Exit(1)

    # Get provider config
    provider_config = service.to_provider_config()

    # Set environment variables
    env = os.environ.copy()
    env["ANTHROPIC_BASE_URL"] = provider_config.base_url
    if provider_config.auth_token:
        env[provider_config.auth_env_var] = provider_config.auth_token
    env["ANTHROPIC_MODEL"] = provider_config.model
    env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = provider_config.default_sonnet or provider_config.model
    env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = provider_config.default_opus or provider_config.model
    env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = provider_config.default_haiku or provider_config.model
    env["CLAUDE_CODE_SUBAGENT_MODEL"] = provider_config.subagent_model or provider_config.model
    env["CLAUDE_CODE_EFFORT_LEVEL"] = provider_config.effort_level
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = provider_config.disable_nonessential_traffic
    env["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"] = provider_config.experimental_agent_teams

    console.print(f"[green]✅ Switched to {service_name}[/green]")
    console.print(f"   [blue]Type:[/blue] {service.type}")
    console.print(f"   [blue]Model:[/blue] {provider_config.model}")
    console.print(f"   [blue]Base URL:[/blue] {provider_config.base_url}")
    console.print()
    console.print("[blue]🚀 Launching Claude Code...[/blue]")

    # Launch claude
    launch_claude(env)


def create_launcher_command(service_name: str) -> Callable:
    """Create a launcher command for a service."""
    def command():
        switch_and_launch(service_name)
    command.__name__ = service_name
    command.__doc__ = f"Switch to {service_name} and launch Claude Code."
    return command


def register_dynamic_commands():
    """Register dynamic commands from services config."""
    from ccm.config.services import get_services_config

    try:
        config = get_services_config()
        for service_name in config.list_services():
            app.command(name=service_name)(create_launcher_command(service_name))
    except (FileNotFoundError, ValueError):
        # Config not ready, skip dynamic commands
        pass


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[bool, typer.Option("--version", "-v", help="Show version")] = False,
):
    """Claude Code launcher - switch provider and exec claude."""
    if version:
        console.print(f"ccc version {__version__}")
        raise typer.Exit(0)
        from ccm.config.services import get_services_config

        console.print("\n[bold yellow]Usage:[/bold yellow] ccc <service>")
        console.print("\n[bold]Services:[/bold]")

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
            console.print("  [yellow]Configure ~/.ccm_services.toml to enable services[/yellow]")

        console.print("\n[bold]Examples:[/bold]")
        console.print("  ccc kimi          # Switch to Kimi and launch")
        console.print("  ccc ali-qwen-cn   # Switch to Alibaba Qwen China and launch")
        raise typer.Exit(0)


def run():
    """Entry point for ccc command."""
    register_dynamic_commands()
    app()


if __name__ == "__main__":
    run()
