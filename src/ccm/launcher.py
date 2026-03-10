"""Launcher for Claude Code - switches provider and launches Claude CLI."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import Annotated, Optional

import typer
from rich.console import Console

from ccm import __version__
from ccm.config import get_config
from ccm.providers import get_provider
from ccm.providers.base import Region

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
        # Unix: set env vars and exec
        for key, val in env.items():
            os.environ[key] = val
        try:
            os.execvp(claude_cmd, [claude_cmd, "--dangerously-skip-permissions"])
        except Exception as e:
            console.print(f"[red]error: Failed to launch Claude Code: {e}[/red]")
            sys.exit(1)


def switch_and_launch(provider: str, region: str = "global", variant: Optional[str] = None):
    """Switch provider and launch Claude Code."""
    config = get_config()

    # Get provider instance
    provider_instance = get_provider(provider)
    if not provider_instance:
        console.print(f"[red]error: Unknown provider: {provider}[/red]")
        console.print("[yellow]💡 Available: glm, kimi, deepseek, minimax, ali, seed, claude, stepfun[/yellow]")
        raise typer.Exit(1)

    # Normalize region
    try:
        normalized_region = Region(region)
    except ValueError:
        console.print(f"[red]error: Invalid region: {region}[/red]")
        console.print("[yellow]💡 Valid regions: global, china[/yellow]")
        raise typer.Exit(1)

    # Get API key
    api_key = config.get_api_key(provider)
    if not api_key or api_key.startswith("your-"):
        console.print(f"[red]error: {provider.upper()}_API_KEY not set[/red]")
        console.print("[yellow]💡 Add to ~/.ccm_config or[/yellow]")
        raise typer.Exit(1)

    # Get model override - only use if NO variant is specified
    model_override = None
    if not variant:
        model_override = config.get_model(provider, normalized_region.value)

    # Get provider config
    provider_config = provider_instance.get_config(
        api_key=api_key,
        variant=variant,
        region=normalized_region,
        model_override=model_override,
    )

    # Set environment variables
    env = os.environ.copy()
    env_vars = provider_instance.get_env_exports(provider_config)
    for key, val in env_vars.items():
        if val is None:
            env.pop(key, None)
        else:
            env[key] = val

    console.print(f"[green]✅ Switched to {provider_instance.INFO.description}[/green]")
    console.print(f"   [blue]Model:[/blue] {provider_config.model}")
    console.print(f"   [blue]Base URL:[/blue] {provider_config.base_url}")
    console.print()
    console.print("[blue]🚀 Launching Claude Code...[/blue]")

    # Launch claude
    launch_claude(env)


@app.command()
def kimi(region: Annotated[str, typer.Argument(help="Region: china or global (default: china)")] = "china"):
    """Switch to Kimi and launch Claude Code."""
    switch_and_launch("kimi", region)


@app.command()
def deepseek():
    """Switch to DeepSeek and launch Claude Code."""
    switch_and_launch("deepseek", "global")


@app.command()
def minimax(region: Annotated[str, typer.Argument(help="Region: china or global (default: china)")] = "china"):
    """Switch to MiniMax and launch Claude Code."""
    switch_and_launch("minimax", region)


@app.command()
def ali(variant: Annotated[Optional[str], typer.Argument(help="qwen/kimi/glm/minimax")] = None, region: Annotated[str, typer.Argument(help="Region: china or global (default: china)")] = "china"):
    """Switch to Alibaba and launch Claude Code."""
    switch_and_launch("ali", region, variant)


@app.command()
def seed(variant: Annotated[Optional[str], typer.Argument(help="Model variant")] = None):
    """Switch to Seed/Doubao and launch Claude Code."""
    switch_and_launch("seed", "global", variant)


@app.command()
def glm(region: Annotated[str, typer.Argument(help="Region: china or global (default: china)")] = "china"):
    """Switch to GLM and launch Claude Code."""
    switch_and_launch("glm", region)


@app.command()
def claude():
    """Switch to Claude official and launch Claude Code."""
    switch_and_launch("claude", "global")


@app.command()
def stepfun():
    """Switch to StepFun and launch Claude Code."""
    switch_and_launch("stepfun", "global")


def main():
    """Entry point for ccc command."""
    app()


if __name__ == "__main__":
    main()
