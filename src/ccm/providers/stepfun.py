"""StepFun provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class StepFunProvider(BaseProvider):
    """StepFun provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="stepfun",
        description="StepFun AI",
        aliases=["stepfun"],
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
        model = model_override or "step-3.5-flash"
        return ProviderConfig(
            base_url="https://api.stepfun.ai/v1/anthropic",
            model=model,
            auth_token=api_key,
            default_sonnet=model,
            default_opus=model,
            default_haiku=model,
            subagent_model=model,
        )
