"""Provider implementations for CCM."""

from ccm.providers.base import BaseProvider, ProviderConfig, ProviderInfo
from ccm.providers.ali import AliProvider
from ccm.providers.kimi import KimiProvider
from ccm.providers.glm import GLMProvider
from ccm.providers.minimax import MiniMaxProvider
from ccm.providers.deepseek import DeepSeekProvider
from ccm.providers.seed import SeedProvider
from ccm.providers.stepfun import StepFunProvider
from ccm.providers.claude import ClaudeProvider
from ccm.providers.openrouter import OpenRouterProvider

__all__ = [
    "BaseProvider",
    "ProviderConfig",
    "ProviderInfo",
    "AliProvider",
    "KimiProvider",
    "GLMProvider",
    "MiniMaxProvider",
    "DeepSeekProvider",
    "SeedProvider",
    "StepFunProvider",
    "ClaudeProvider",
    "OpenRouterProvider",
]

# Provider registry
PROVIDERS: dict[str, type[BaseProvider]] = {
    "ali": AliProvider,
    "alibaba": AliProvider,
    "kimi": KimiProvider,
    "kimi2": KimiProvider,
    "glm": GLMProvider,
    "glm5": GLMProvider,
    "minimax": MiniMaxProvider,
    "mm": MiniMaxProvider,
    "deepseek": DeepSeekProvider,
    "ds": DeepSeekProvider,
    "seed": SeedProvider,
    "doubao": SeedProvider,
    "stepfun": StepFunProvider,
    "claude": ClaudeProvider,
    "sonnet": ClaudeProvider,
    "s": ClaudeProvider,
    "open": OpenRouterProvider,
    "openrouter": OpenRouterProvider,
}


def get_provider(name: str) -> BaseProvider | None:
    """Get a provider instance by name."""
    provider_class = PROVIDERS.get(name.lower())
    if provider_class:
        return provider_class()
    return None


def is_known_provider(name: str) -> bool:
    """Check if a name is a known provider."""
    return name.lower() in PROVIDERS
