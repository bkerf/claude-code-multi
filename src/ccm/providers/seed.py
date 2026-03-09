"""Seed/Doubao provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class SeedProvider(BaseProvider):
    """Seed/Doubao (ByteDance) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="seed",
        description="Doubao/Seed-Code (ByteDance)",
        aliases=["seed", "doubao"],
        supports_region=False,
        supports_variant=True,
        variants=["doubao", "glm", "deepseek", "kimi"],
    )

    VARIANT_MODELS: ClassVar[dict[str, str]] = {
        "default": "ark-code-latest",
        "doubao": "doubao-seed-code",
        "seed": "doubao-seed-code",
        "glm": "glm-5",
        "glm5": "glm-5",
        "deepseek": "deepseek-v3.2",
        "ds": "deepseek-v3.2",
        "kimi": "kimi-k2.5",
        "kimi2": "kimi-k2.5",
    }

    @classmethod
    def get_info(cls) -> ProviderInfo:
        return cls.INFO

    def get_config(
        self,
        api_key: str,
        variant: str | None = None,
        region: Region = Region.GLOBAL,  # Not used for Seed
        model_override: str | None = None,
    ) -> ProviderConfig:
        if model_override:
            model = model_override
        elif variant:
            model = self.VARIANT_MODELS.get(variant.lower(), "ark-code-latest")
        else:
            model = "ark-code-latest"

        return ProviderConfig(
            base_url="https://ark.cn-beijing.volces.com/api/coding",
            model=model,
            auth_token=api_key,
            default_sonnet=model,
            default_opus=model,
            default_haiku=model,
            subagent_model=model,
        )
