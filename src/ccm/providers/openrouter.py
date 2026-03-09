"""OpenRouter provider implementation."""

from __future__ import annotations

from typing import ClassVar

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo, Region


class OpenRouterProvider(BaseProvider):
    """OpenRouter provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="openrouter",
        description="OpenRouter (multi-provider gateway)",
        aliases=["open", "openrouter"],
        supports_region=False,
        supports_variant=True,
        variants=[
            "claude",
            "kimi",
            "deepseek",
            "glm",
            "ali",
            "minimax",
            "stepfun",
            "stepfun-free",
        ],
    )

    PROVIDER_MODELS: ClassVar[dict[str, tuple[str, str, str]]] = {
        # provider: (model, sonnet, opus)
        "claude": ("anthropic/claude-sonnet-4.5", "anthropic/claude-sonnet-4.5", "anthropic/claude-opus-4.6"),
        "anthropic": ("anthropic/claude-sonnet-4.5", "anthropic/claude-sonnet-4.5", "anthropic/claude-opus-4.6"),
        "default": ("anthropic/claude-sonnet-4.5", "anthropic/claude-sonnet-4.5", "anthropic/claude-opus-4.6"),
        "kimi": ("moonshotai/kimi-k2.5", "moonshotai/kimi-k2.5", "moonshotai/kimi-k2.5"),
        "deepseek": ("deepseek/deepseek-v3.2", "deepseek/deepseek-v3.2", "deepseek/deepseek-v3.2"),
        "ds": ("deepseek/deepseek-v3.2", "deepseek/deepseek-v3.2", "deepseek/deepseek-v3.2"),
        "glm": ("z-ai/glm-5", "z-ai/glm-5", "z-ai/glm-5"),
        "glm5": ("z-ai/glm-5", "z-ai/glm-5", "z-ai/glm-5"),
        "ali": ("qwen/qwen3-coder-next", "qwen/qwen3-coder-next", "qwen/qwen3-coder-plus"),
        "alibaba": ("qwen/qwen3-coder-next", "qwen/qwen3-coder-next", "qwen/qwen3-coder-plus"),
        "minimax": ("minimax/minimax-m2.5", "minimax/minimax-m2.5", "minimax/minimax-m2.5"),
        "mm": ("minimax/minimax-m2.5", "minimax/minimax-m2.5", "minimax/minimax-m2.5"),
        "stepfun": ("stepfun/step-3.5-flash", "stepfun/step-3.5-flash", "stepfun/step-3.5-flash"),
        "sf": ("stepfun/step-3.5-flash", "stepfun/step-3.5-flash", "stepfun/step-3.5-flash"),
        "stepfun-free": ("stepfun/step-3.5-flash:free", "stepfun/step-3.5-flash:free", "stepfun/step-3.5-flash:free"),
        "sf-free": ("stepfun/step-3.5-flash:free", "stepfun/step-3.5-flash:free", "stepfun/step-3.5-flash:free"),
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
        provider_key = (variant or "claude").lower()
        models = self.PROVIDER_MODELS.get(provider_key, self.PROVIDER_MODELS["default"])

        model, sonnet, opus = models
        if model_override:
            model = model_override

        return ProviderConfig(
            base_url="https://openrouter.ai/api",
            model=model,
            auth_token=api_key,
            default_sonnet=sonnet,
            default_opus=opus,
            default_haiku=model,
            subagent_model=model,
        )
