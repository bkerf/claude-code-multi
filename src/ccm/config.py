"""Configuration management for CCM."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class APIKeys:
    """API key configuration."""

    deepseek: str | None = None
    glm: str | None = None
    kimi: str | None = None
    minimax: str | None = None
    ark: str | None = None  # Seed/Doubao
    qwen: str | None = None  # Alibaba
    stepfun: str | None = None
    claude: str | None = None
    openrouter: str | None = None


@dataclass
class ModelOverrides:
    """Model ID overrides."""

    deepseek: str = "deepseek-chat"
    kimi: str = "kimi-k2.5"
    kimi_cn: str = "kimi-k2.5"
    qwen: str = "qwen3-max-2026-01-23"
    glm: str = "glm-5"
    claude: str = "claude-sonnet-4-5-20250929"
    opus: str = "claude-opus-4-6"
    haiku: str = "claude-haiku-4-5-20251001"
    minimax: str = "MiniMax-M2.5"
    seed: str = "ark-code-latest"
    stepfun: str = "step-3.5-flash"


@dataclass
class Config:
    """CCM configuration."""

    language: str = "en"
    api_keys: APIKeys = field(default_factory=APIKeys)
    models: ModelOverrides = field(default_factory=ModelOverrides)

    # Config file path
    CONFIG_FILE: Path = field(default=Path.home() / ".ccm_config", init=False)
    ACCOUNTS_FILE: Path = field(default=Path.home() / ".ccm_accounts", init=False)

    @classmethod
    def get_config_path(cls) -> Path:
        """Get config file path."""
        return Path.home() / ".ccm_config"

    @classmethod
    def get_accounts_path(cls) -> Path:
        """Get accounts file path."""
        return Path.home() / ".ccm_accounts"

    @classmethod
    def load(cls) -> Config:
        """Load configuration from file and environment."""
        config = cls()

        # Load from file if exists
        config_file = cls.get_config_path()
        if config_file.exists():
            config._load_from_file(config_file)

        # Override from environment variables
        config._load_from_env()

        return config

    def _load_from_file(self, path: Path) -> None:
        """Load configuration from TOML file."""
        try:
            content = path.read_text()
            # Parse as simple key=value format (compatible with old bash config)
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    # Remove 'export ' prefix if present
                    if key.startswith("export "):
                        key = key[7:].strip()
                    value = value.strip().strip('"').strip("'")

                    self._set_value(key, value)
        except Exception:
            pass

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        env_mapping = {
            "CCM_LANGUAGE": ("language", str),
            "DEEPSEEK_API_KEY": ("api_keys.deepseek", str),
            "GLM_API_KEY": ("api_keys.glm", str),
            "KIMI_API_KEY": ("api_keys.kimi", str),
            "MINIMAX_API_KEY": ("api_keys.minimax", str),
            "ARK_API_KEY": ("api_keys.ark", str),
            "QWEN_API_KEY": ("api_keys.qwen", str),
            "STEPFUN_API_KEY": ("api_keys.stepfun", str),
            "CLAUDE_API_KEY": ("api_keys.claude", str),
            "OPENROUTER_API_KEY": ("api_keys.openrouter", str),
            "DEEPSEEK_MODEL": ("models.deepseek", str),
            "KIMI_MODEL": ("models.kimi", str),
            "KIMI_CN_MODEL": ("models.kimi_cn", str),
            "QWEN_MODEL": ("models.qwen", str),
            "GLM_MODEL": ("models.glm", str),
            "CLAUDE_MODEL": ("models.claude", str),
            "OPUS_MODEL": ("models.opus", str),
            "HAIKU_MODEL": ("models.haiku", str),
            "MINIMAX_MODEL": ("models.minimax", str),
            "SEED_MODEL": ("models.seed", str),
            "STEPFUN_MODEL": ("models.stepfun", str),
        }

        for env_key, (path, _) in env_mapping.items():
            value = os.environ.get(env_key)
            if value and not self._is_placeholder(value):
                self._set_nested(path, value)

    def _set_value(self, key: str, value: str) -> None:
        """Set a configuration value by key name."""
        mapping = {
            "CCM_LANGUAGE": "language",
            "DEEPSEEK_API_KEY": "api_keys.deepseek",
            "GLM_API_KEY": "api_keys.glm",
            "KIMI_API_KEY": "api_keys.kimi",
            "MINIMAX_API_KEY": "api_keys.minimax",
            "ARK_API_KEY": "api_keys.ark",
            "QWEN_API_KEY": "api_keys.qwen",
            "STEPFUN_API_KEY": "api_keys.stepfun",
            "CLAUDE_API_KEY": "api_keys.claude",
            "OPENROUTER_API_KEY": "api_keys.openrouter",
            "DEEPSEEK_MODEL": "models.deepseek",
            "KIMI_MODEL": "models.kimi",
            "KIMI_CN_MODEL": "models.kimi_cn",
            "QWEN_MODEL": "models.qwen",
            "GLM_MODEL": "models.glm",
            "CLAUDE_MODEL": "models.claude",
            "OPUS_MODEL": "models.opus",
            "HAIKU_MODEL": "models.haiku",
            "MINIMAX_MODEL": "models.minimax",
            "SEED_MODEL": "models.seed",
            "STEPFUN_MODEL": "models.stepfun",
        }

        if key in mapping:
            # Skip placeholder values
            if not self._is_placeholder(value):
                self._set_nested(mapping[key], value)

    def _set_nested(self, path: str, value: Any) -> None:
        """Set a nested attribute using dot notation."""
        parts = path.split(".")
        obj = self

        for part in parts[:-1]:
            obj = getattr(obj, part)

        setattr(obj, parts[-1], value)

    def _is_placeholder(self, value: str) -> bool:
        """Check if value is a placeholder."""
        lower = value.lower()
        return "your" in lower and "api" in lower and "key" in lower

    def is_effectively_set(self, value: str | None) -> bool:
        """Check if a value is effectively set (not empty and not placeholder)."""
        if not value:
            return False
        return not self._is_placeholder(value)

    def get_api_key(self, provider: str) -> str | None:
        """Get API key for a provider."""
        key_mapping = {
            "deepseek": self.api_keys.deepseek,
            "ds": self.api_keys.deepseek,
            "glm": self.api_keys.glm,
            "glm5": self.api_keys.glm,
            "kimi": self.api_keys.kimi,
            "kimi2": self.api_keys.kimi,
            "minimax": self.api_keys.minimax,
            "mm": self.api_keys.minimax,
            "seed": self.api_keys.ark,
            "doubao": self.api_keys.ark,
            "ali": self.api_keys.qwen,
            "alibaba": self.api_keys.qwen,
            "stepfun": self.api_keys.stepfun,
            "claude": self.api_keys.claude,
            "sonnet": self.api_keys.claude,
            "openrouter": self.api_keys.openrouter,
        }
        return key_mapping.get(provider)

    def get_model(self, provider: str, region: str = "global") -> str:
        """Get model ID for a provider."""
        model_mapping = {
            "deepseek": self.models.deepseek,
            "ds": self.models.deepseek,
            "glm": self.models.glm,
            "glm5": self.models.glm,
            "kimi": self.models.kimi if region == "global" else self.models.kimi_cn,
            "kimi2": self.models.kimi if region == "global" else self.models.kimi_cn,
            "minimax": self.models.minimax,
            "mm": self.models.minimax,
            "seed": self.models.seed,
            "doubao": self.models.seed,
            "ali": self.models.qwen,
            "alibaba": self.models.qwen,
            "stepfun": self.models.stepfun,
            "claude": self.models.claude,
            "sonnet": self.models.claude,
        }
        return model_mapping.get(provider, "")

    def save(self) -> None:
        """Save configuration to file."""
        path = self.get_config_path()

        lines = [
            "# CCM Configuration File",
            "# Replace placeholder values with your actual API keys",
            "# Note: Environment variables take precedence over this file",
            "",
            f"CCM_LANGUAGE={self.language}",
            "",
            "# API Keys",
        ]

        if self.api_keys.deepseek:
            lines.append(f"DEEPSEEK_API_KEY={self.api_keys.deepseek}")
        else:
            lines.append("DEEPSEEK_API_KEY=sk-your-deepseek-api-key")

        if self.api_keys.glm:
            lines.append(f"GLM_API_KEY={self.api_keys.glm}")
        else:
            lines.append("GLM_API_KEY=your-glm-api-key")

        if self.api_keys.kimi:
            lines.append(f"KIMI_API_KEY={self.api_keys.kimi}")
        else:
            lines.append("KIMI_API_KEY=your-kimi-api-key")

        if self.api_keys.minimax:
            lines.append(f"MINIMAX_API_KEY={self.api_keys.minimax}")
        else:
            lines.append("MINIMAX_API_KEY=your-minimax-api-key")

        if self.api_keys.ark:
            lines.append(f"ARK_API_KEY={self.api_keys.ark}")
        else:
            lines.append("ARK_API_KEY=your-ark-api-key")

        if self.api_keys.qwen:
            lines.append(f"QWEN_API_KEY={self.api_keys.qwen}")
        else:
            lines.append("QWEN_API_KEY=your-qwen-api-key")

        if self.api_keys.stepfun:
            lines.append(f"STEPFUN_API_KEY={self.api_keys.stepfun}")
        else:
            lines.append("STEPFUN_API_KEY=your-stepfun-api-key")

        if self.api_keys.claude:
            lines.append(f"CLAUDE_API_KEY={self.api_keys.claude}")
        else:
            lines.append("CLAUDE_API_KEY=your-claude-api-key")

        if self.api_keys.openrouter:
            lines.append(f"OPENROUTER_API_KEY={self.api_keys.openrouter}")
        else:
            lines.append("OPENROUTER_API_KEY=your-openrouter-api-key")

        lines.extend([
            "",
            "# Model ID Overrides (optional)",
            f"DEEPSEEK_MODEL={self.models.deepseek}",
            f"KIMI_MODEL={self.models.kimi}",
            f"KIMI_CN_MODEL={self.models.kimi_cn}",
            f"QWEN_MODEL={self.models.qwen}",
            f"GLM_MODEL={self.models.glm}",
            f"CLAUDE_MODEL={self.models.claude}",
            f"OPUS_MODEL={self.models.opus}",
            f"HAIKU_MODEL={self.models.haiku}",
            f"MINIMAX_MODEL={self.models.minimax}",
            f"SEED_MODEL={self.models.seed}",
            f"STEPFUN_MODEL={self.models.stepfun}",
            "",
        ])

        path.write_text("\n".join(lines))
        path.chmod(0o600)


def get_config() -> Config:
    """Get the current configuration."""
    return Config.load()
