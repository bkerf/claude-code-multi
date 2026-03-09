"""Kimi (Moonshot) provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class KimiProvider(BaseProvider):
    """Kimi (Moonshot) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="kimi",
        description="Kimi (Moonshot AI)",
        aliases=["kimi", "kimi2"],
        supports_region=True,
        supports_variant=False,
    )

    BASE_URLS: ClassVar[dict[Region, str]] = {
        Region.GLOBAL: "https://api.moonshot.ai/anthropic",
        Region.CHINA: "https://api.moonshot.cn/anthropic",
    }

    @classmethod
    def get_info(cls) -> ProviderInfo:
        return cls.INFO

    def get_config(
        self,
        api_key: str,
        variant: str | None = None,
        region: Region = Region.GLOBAL,
        model_override: str | None = None,
    ) -> ProviderConfig:
        model = model_override or "kimi-k2.5"
        return ProviderConfig(
            base_url=self.BASE_URLS[region],
            model=model,
            auth_token=api_key,
            default_sonnet=model,
            default_opus=model,
            default_haiku=model,
            subagent_model=model,
        )
