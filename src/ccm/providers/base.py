"""Base provider interface for CCM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Region(str, Enum):
    """Supported regions."""

    CHINA = "china"
    GLOBAL = "global"

    @classmethod
    def normalize(cls, value: str) -> Region:
        """Normalize a region string to a Region enum."""
        value = value.lower().strip()
        if value in ("global", "g", "intl", "international", "overseas"):
            return cls.GLOBAL
        if value in ("china", "cn", "zh", "domestic"):
            return cls.CHINA
        raise ValueError(f"Unknown region: {value}")


@dataclass
class ProviderInfo:
    """Provider metadata."""

    name: str
    description: str
    aliases: list[str]
    supports_region: bool = False
    supports_variant: bool = False
    variants: list[str] | None = None


@dataclass
class ProviderConfig:
    """Configuration for a provider."""

    base_url: str
    model: str
    auth_token: str | None = None
    default_sonnet: str | None = None
    default_opus: str | None = None
    default_haiku: str | None = None
    subagent_model: str | None = None
    effort_level: str = "high"
    disable_nonessential_traffic: str = "1"
    experimental_agent_teams: str = "1"
    auth_env_var: str = "ANTHROPIC_AUTH_TOKEN"


class BaseProvider(ABC):
    """Base class for all providers."""

    # Provider metadata (override in subclass)
    INFO: ClassVar[ProviderInfo]

    @classmethod
    @abstractmethod
    def get_info(cls) -> ProviderInfo:
        """Get provider information."""
        pass

    @abstractmethod
    def get_config(
        self,
        api_key: str,
        variant: str | None = None,
        region: Region = Region.GLOBAL,
        model_override: str | None = None,
    ) -> ProviderConfig:
        """Get provider configuration.

        Args:
            api_key: The API key for authentication
            variant: Model variant (if supported)
            region: The region to use (china/global)
            model_override: Override the model ID

        Returns:
            ProviderConfig with all necessary settings
        """
        pass

    def get_env_exports(self, config: ProviderConfig) -> dict[str, str | None]:
        """Get environment variable exports for the configuration.

        Returns a dict of env vars to set. None values mean unset.
        """
        exports: dict[str, str | None] = {
            "ANTHROPIC_BASE_URL": config.base_url,
            config.auth_env_var: config.auth_token,
            "ANTHROPIC_MODEL": config.model,
            "ANTHROPIC_DEFAULT_SONNET_MODEL": config.default_sonnet or config.model,
            "ANTHROPIC_DEFAULT_OPUS_MODEL": config.default_opus or config.model,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": config.default_haiku or config.model,
            "CLAUDE_CODE_SUBAGENT_MODEL": config.subagent_model or config.model,
            "CLAUDE_CODE_EFFORT_LEVEL": config.effort_level,
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": config.disable_nonessential_traffic,
            "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": config.experimental_agent_teams,
        }
        return exports

    def format_exports(self, config: ProviderConfig, shell: str = "bash") -> str:
        """Format exports for shell eval.

        Args:
            config: Provider configuration
            shell: Target shell (bash/zsh, fish, or powershell)

        Returns:
            Shell commands to set environment variables
        """
        exports = self.get_env_exports(config)
        lines = []

        if shell == "powershell":
            for key, value in exports.items():
                if value is None:
                    lines.append(f"Remove-Item Env:{key}")
                else:
                    lines.append(f'$env:{key} = "{value}"')
        elif shell == "fish":
            for key, value in exports.items():
                if value is None:
                    lines.append(f"set -e {key}")
                else:
                    lines.append(f"set -gx {key} '{value}'")
        else:
            # bash/zsh
            for key, value in exports.items():
                if value is None:
                    lines.append(f"unset {key}")
                else:
                    lines.append(f"export {key}='{value}'")

        return "\n".join(lines)
