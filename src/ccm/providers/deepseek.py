"""DeepSeek provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class DeepSeekProvider(BaseProvider):
    """DeepSeek provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="deepseek",
        description="DeepSeek AI",
        aliases=["deepseek", "ds"],
        supports_region=False,
        supports_variant=False,
    )

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
        model = model_override or "deepseek-chat"
        return ProviderConfig(
            base_url="https://api.deepseek.com/anthropic",
            model=model,
            auth_token=api_key,
            default_sonnet="deepseek/deepseek-v3.2",
            default_opus="deepseek/deepseek-v3.2",
            default_haiku="deepseek/deepseek-v3.2",
            subagent_model=model,
        )
