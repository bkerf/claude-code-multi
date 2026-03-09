"""Alibaba Cloud Coding Plan provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class AliProvider(BaseProvider):
    """Alibaba Cloud Coding Plan provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="ali",
        description="Alibaba Cloud Coding Plan",
        aliases=["ali", "alibaba"],
        supports_region=True,
        supports_variant=True,
        variants=["qwen", "kimi", "glm", "minimax"],
    )

    BASE_URLS: ClassVar[dict[Region, str]] = {
        Region.GLOBAL: "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic",
        Region.CHINA: "https://coding.dashscope.aliyuncs.com/apps/anthropic",
    }

    VARIANT_MODELS: ClassVar[dict[str, str]] = {
        "qwen": "qwen3.5-plus",
        "qwen3.5": "qwen3.5-plus",
        "kimi": "kimi-k2.5",
        "kimi-k2.5": "kimi-k2.5",
        "glm": "glm-5",
        "glm5": "glm-5",
        "minimax": "MiniMax-M2.5",
        "mm": "MiniMax-M2.5",
    }

    @classmethod
    def get_info(cls) -> ProviderInfo:
        return cls.INFO

    def get_config(
        self,
        api_key: str,
        variant: str | None = None,
        region: Region = Region.CHINA,  # Default to China for Ali
        model_override: str | None = None,
    ) -> ProviderConfig:
        if model_override:
            model = model_override
        elif variant:
            model = self.VARIANT_MODELS.get(variant.lower(), "qwen3.5-plus")
        else:
            model = "qwen3.5-plus"

        return ProviderConfig(
            base_url=self.BASE_URLS[region],
            model=model,
            auth_token=api_key,
            default_sonnet=model,
            default_opus=model,
            default_haiku=model,
            subagent_model=model,
        )
