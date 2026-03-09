"""Claude (official) provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class ClaudeProvider(BaseProvider):
    """Claude (official Anthropic) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="claude",
        description="Claude (official Anthropic)",
        aliases=["claude", "sonnet", "s"],
        supports_region=False,
        supports_variant=False,
    )

    @classmethod
    def get_info(cls) -> ProviderInfo:
        return cls.INFO

    def get_config(
        self,
        api_key: str | None = None,
        variant: str | None = None,
        region: Region = Region.GLOBAL,
        model_override: str | None = None,
    ) -> ProviderConfig:
        model = model_override or "claude-sonnet-4-5-20250929"
        return ProviderConfig(
            base_url="https://api.anthropic.com/",
            model=model,
            auth_token=api_key,  # May be None for Claude Pro subscription
            default_sonnet=model,
            default_opus="claude-opus-4-6",
            default_haiku="claude-haiku-4-5-20251001",
            subagent_model=model,
        )

    def get_env_exports(self, config: ProviderConfig) -> dict[str, str | None]:
        """Override to handle Claude Pro subscription (no API key)."""
        exports = super().get_env_exports(config)

        # For Claude Pro subscription, we don't set auth token
        if config.auth_token is None:
            exports["ANTHROPIC_AUTH_TOKEN"] = None
            exports["ANTHROPIC_API_KEY"] = None

        return exports
