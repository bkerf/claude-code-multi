"""GLM (Zhipu) provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class GLMProvider(BaseProvider):
    """GLM (Zhipu AI) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="glm",
        description="GLM (Zhipu AI)",
        aliases=["glm", "glm5", "glm4", "glm4.6", "glm4.7"],
        supports_region=True,
        supports_variant=False,
    )

    BASE_URLS: ClassVar[dict[Region, str]] = {
        Region.GLOBAL: "https://api.z.ai/api/anthropic",
        Region.CHINA: "https://open.bigmodel.cn/api/anthropic",
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
        model = model_override or "glm-5"
        return ProviderConfig(
            base_url=self.BASE_URLS[region],
            model=model,
            auth_token=api_key,
            default_sonnet=model,
            default_opus=model,
            default_haiku=model,
            subagent_model=model,
        )
