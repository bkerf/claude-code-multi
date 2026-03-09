"""Project-level settings management."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from ccm.providers.base import ProviderConfig, Region
from ccm.providers import get_provider


from ccm.config import get_config


def get_project_settings_path() -> Path:
    """Get project settings file path."""
    return Path.cwd() / ".claude" / "settings.local.json"


def write_project_settings(
    provider_name: str,
    region: Region,
    api_key: str,
) -> None:
    """Write provider settings to project-level settings file."""
    provider = get_provider(provider_name)
    if not provider:
        raise ValueError(f"Unknown provider: {provider_name}")

    settings_path = get_project_settings_path()
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

    # Ensure directory exists
    settings_dir.mkdir(parents=True, exist_ok=True)
    # Build settings
    settings = {
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
        }
    }
    if provider_config.auth_token:
        settings["env"]["ANTHROPIC_AUTH_TOKEN"] = provider_config.auth_token
    # Write settings
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    os.chmod(settings_path, 0o600)
    print(f"✅ Wrote project settings for {provider_name}")
    print(f"   File: {settings_path}")
    print("💡 This overrides user settings for this project only")
    print("💡 Use 'ccm project reset' to remove")


def reset_project_settings() -> None:
    """Reset project-level settings."""
    from ccm.config import get_config

    settings_path = get_project_settings_path()
    if not settings_path.exists():
        settings_path.unlink()
        print("✅ Removed project settings")
        print("💡 Claude Code will fall back to user settings")
    else:
        print("⚠️  No project settings to reset")
