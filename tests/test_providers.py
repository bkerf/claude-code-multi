"""Tests for CCM providers."""

import pytest
from ccm.providers import get_provider, is_known_provider, PROVIDERS
from ccm.providers.base import Region
from ccm.providers.ali import AliProvider
from ccm.providers.kimi import KimiProvider
from ccm.providers.glm import GLMProvider
from ccm.providers.minimax import MiniMaxProvider
from ccm.providers.deepseek import DeepSeekProvider
from ccm.providers.seed import SeedProvider
from ccm.providers.claude import ClaudeProvider
from ccm.providers.openrouter import OpenRouterProvider
from ccm.providers.stepfun import StepFunProvider


from ccm.providers.base import BaseProvider


class TestProviders:
    """Test provider registry."""

    def test_get_deepseek(self):
        provider = get_provider("deepseek")
        assert provider is not None
        assert isinstance(provider, DeepSeekProvider)

        info = provider.get_info()
        assert info.name == "deepseek"

    def test_get_kimi(self):
        provider = get_provider("kimi")
        assert provider is not None
        assert isinstance(provider, KimiProvider)
        info = provider.get_info()
        assert info.name == "kimi"

    def test_get_glm(self):
        provider = get_provider("glm")
        assert provider is not None
        assert isinstance(provider, GLMProvider)
        info = provider.get_info()
        assert info.name == "glm"

    def test_get_minimax(self):
        provider = get_provider("minimax")
        assert provider is not None
        assert isinstance(provider, MiniMaxProvider)
        info = provider.get_info()
        assert info.name == "minimax"

    def test_get_seed(self):
        provider = get_provider("seed")
        assert provider is not None
        assert isinstance(provider, SeedProvider)
        info = provider.get_info()
        assert info.name == "seed"

    def test_get_claude(self):
        provider = get_provider("claude")
        assert provider is not None
        assert isinstance(provider, ClaudeProvider)
        info = provider.get_info()
        assert info.name == "claude"

    def test_get_openrouter(self):
        provider = get_provider("openrouter")
        assert provider is not None
        assert isinstance(provider, OpenRouterProvider)
        info = provider.get_info()
        assert info.name == "openrouter"
        assert info.variants is not None
        assert "claude" in info.variants

        assert "deepseek" in info.variants

        assert "kimi" in info.variants

    def test_get_stepfun(self):
        provider = get_provider("stepfun")
        assert provider is not None
        assert isinstance(provider, StepFunProvider)
        info = provider.get_info()
        assert info.name == "stepfun"


class TestProviderConfig:
    """Test provider configurations."""

    def test_deepseek_config(self):
        provider = get_provider("deepseek")
        config = provider.get_config(api_key="test-key")
        assert config.base_url == "https://api.deepseek.com/anthropic"
        assert config.model == "deepseek-chat"
        assert config.auth_token == "test-key"

    def test_kimi_global_config(self):
        provider = get_provider("kimi")
        config = provider.get_config(api_key="test-key", region=Region.GLOBAL)
        assert config.base_url == "https://api.moonshot.ai/anthropic"
        assert config.model == "kimi-k2.5"

    def test_kimi_china_config(self):
        provider = get_provider("kimi")
        config = provider.get_config(api_key="test-key", region=Region.CHINA)
        assert config.base_url == "https://api.moonshot.cn/anthropic"
        assert config.model == "kimi-k2.5"

    def test_glm_global_config(self):
        provider = get_provider("glm")
        config = provider.get_config(api_key="test-key", region=Region.GLOBAL)
        assert config.base_url == "https://api.z.ai/api/anthropic"
        assert config.model == "glm-5"

    def test_glm_china_config(self):
        provider = get_provider("glm")
        config = provider.get_config(api_key="test-key", region=Region.CHINA)
        assert config.base_url == "https://open.bigmodel.cn/api/anthropic"
        assert config.model == "glm-5"

    def test_ali_qwen_config(self):
        provider = get_provider("ali")
        config = provider.get_config(api_key="test-key", variant="qwen", region=Region.CHINA)
        assert config.base_url == "https://coding.dashscope.aliyuncs.com/apps/anthropic"
        assert config.model == "qwen3.5-plus"

    def test_ali_kimi_config(self):
        provider = get_provider("ali")
        config = provider.get_config(api_key="test-key", variant="kimi", region=Region.CHINA)
        assert config.model == "kimi-k2.5"

    def test_seed_default_config(self):
        provider = get_provider("seed")
        config = provider.get_config(api_key="test-key")
        assert config.base_url == "https://ark.cn-beijing.volces.com/api/coding"
        assert config.model == "ark-code-latest"

    def test_seed_variant_config(self):
        provider = get_provider("seed")
        config = provider.get_config(api_key="test-key", variant="glm")
        assert config.model == "glm-5"

    def test_openrouter_claude_config(self):
        provider = get_provider("openrouter")
        config = provider.get_config(api_key="test-key", variant="claude")
        assert config.base_url == "https://openrouter.ai/api"
        assert config.model == "anthropic/claude-sonnet-4.5"


class TestRegion:
    """Test region normalization."""

    def test_global_region(self):
        assert Region.normalize("global") == Region.GLOBAL
        assert Region.normalize("g") == Region.GLOBAL
        assert Region.normalize("intl") == Region.GLOBAL
        assert Region.normalize("overseas") == Region.GLOBAL

    def test_china_region(self):
        assert Region.normalize("china") == Region.CHINA
        assert Region.normalize("cn") == Region.CHINA
        assert Region.normalize("zh") == Region.CHINA
        assert Region.normalize("domestic") == Region.CHINA

    def test_invalid_region(self):
        with pytest.raises(ValueError):
            Region.normalize("invalid")
