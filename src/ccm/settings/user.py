"""User-level settings management."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


from ccm.providers.base import ProviderConfig, Region


from ccm.providers import get_provider


def get_user_settings_path() -> Path:
    """Get user settings file path."""
    return Path.home() / ".claude" / "settings.json"


def write_user_settings(
    provider_name: str,
    region: Region,
    api_key: str,
) -> None:
    """Write provider settings to user-level settings file."""
    provider = get_provider(provider_name)
    if not provider:
        raise ValueError(f"Unknown provider: {provider_name}")

    settings_path = get_user_settings_path()
    settings_dir = settings_path.parent

    # Get provider config
    config = get_config()
    model_override = config.get_model(provider_name, region.value)
    provider_config = provider.get_config(
        api_key=api_key,
        variant=None,
        region=region,
        model_override=model_override,
    )

    # Load existing settings or preserve
    existing: dict[str, Any] = {}
    if settings_path.exists():
        try:
            with open(settings_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError):
            existing = {}
    # Check if ccm-managed
    if not existing.get("ccmManaged"):
        # Backup existing settings
        backup_path = settings_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d-%%%H%M%S')}")
        settings_path.rename(backup_path)
    # Ensure directory exists
    settings_dir.mkdir(parents=True, exist_ok=True)
    # Build new settings
    new_settings = {
        "ccmManaged": True,
        "ccmProvider": provider_name,
        "ccmRegion": region.value,
        "env": {
            "ANTHROPIC_BASE_URL": provider_config.base_url,
            "ANTHROPIC_MODEL": provider_config.model,
            "ANTHROPIC_DEFAULT_SONNET_MODEL": provider_config.default_sonnet or provider_config.model,
            "ANTHROPIC_DEFAULT_OPUS_MODEL": provider_config.default_opus or provider_config.model,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": provider_config.default_haiku or provider_config.model,
            "CLAUDE_CODE_SUBAGENT_MODEL": provider_config.subagent_model or provider_config.model,
            "CLAUDE_CODE_EFFORT_LEVEL": provider_config.effort_level,
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": provider_config.disable_nonessential_traffic,
            "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": provider_config.experimental_agent_teams,
        }
    }
    if provider_config.auth_token:
        new_settings["env"]["ANTHROPIC_AUTH_TOKEN"] = provider_config.auth_token
    # Write settings
    with open(settings_path, "w") as f:
        json.dump(new_settings, f, indent=2)
    os.chmod(settings_path, 0o600)


    print(f"✅ Wrote user settings for {provider_name}")
    print(f"   File: {settings_path}")
    print("💡 This overrides environment variables")
    print("💡 Use 'ccm user reset' to restore env var control")


def reset_user_settings() -> None:
    """Reset user-level settings to use environment variables."""
    from ccm.config import get_config

    settings_path = get_user_settings_path()
    if not settings_path.exists():
        print("⚠️  No user settings to reset")
        return
    with open(settings_path) as f:
        settings = json.load(f)
    if not settings.get("ccmManaged"):
        print("⚠️  Settings file is not ccm-managed. Not modifying.")
        return
    # Backup before reset
    backup_path = settings_path.with_suffix(f".bak.{datetime.now().strftime('%Y%m%d-%%H%M%S')}")
    settings_path.rename(backup_path)
    # Remove ccm-managed keys
    settings.pop("ccmManaged", None)
    settings.pop("ccmProvider", None)
    settings.pop("ccmRegion", None)
    settings.pop("env", None)
    # Write back
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print("✅ Removed ccm-managed settings from user settings")
    print("💡 Claude Code will now use environment variables")
