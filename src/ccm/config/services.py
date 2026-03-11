"""Dynamic services configuration for CCM."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from ccm.providers.base import ProviderConfig


@dataclass
class ServiceConfig:
    """统一服务配置 - 所有字段必填"""

    name: str
    type: str
    base_url: str
    api_key: str
    model: str
    default_sonnet: str
    default_opus: str
    default_haiku: str
    subagent_model: str

    def to_provider_config(self) -> ProviderConfig:
        """转换为 ProviderConfig"""
        # 所有服务统一使用 ANTHROPIC_AUTH_TOKEN
        return ProviderConfig(
            base_url=self.base_url,
            model=self.model,
            auth_token=self.api_key or None,
            default_sonnet=self.default_sonnet,
            default_opus=self.default_opus,
            default_haiku=self.default_haiku,
            subagent_model=self.subagent_model,
            auth_env_var="ANTHROPIC_AUTH_TOKEN",
        )

    @classmethod
    def from_toml(cls, name: str, data: dict[str, Any]) -> ServiceConfig:
        """从 TOML 数据创建 ServiceConfig"""
        return cls(
            name=name,
            type=data.get("type", ""),
            base_url=data.get("base_url", ""),
            api_key=data.get("api_key", ""),
            model=data.get("model", ""),
            default_sonnet=data.get("default_sonnet", data.get("model", "")),
            default_opus=data.get("default_opus", data.get("model", "")),
            default_haiku=data.get("default_haiku", data.get("model", "")),
            subagent_model=data.get("subagent_model", data.get("model", "")),
        )


@dataclass
class ServicesConfig:
    """所有服务配置"""

    language: str = "zh"
    services: dict[str, ServiceConfig] = field(default_factory=dict)
    config_path: Path = field(default=Path.home() / ".ccm_services.toml", init=False)

    @classmethod
    def get_config_path(cls) -> Path:
        """获取配置文件路径"""
        return Path.home() / ".ccm_services.toml"

    @classmethod
    def load(cls) -> ServicesConfig:
        """从 ~/.ccm_services 加载 TOML"""
        config_path = cls.get_config_path()

        if not config_path.exists():
            raise FileNotFoundError(
                f"配置文件不存在: {config_path}\n"
                f"请复制 ccm_services.template 到 {config_path} 并填写 API Key"
            )

        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            raise ValueError(f"解析配置文件失败: {e}")

        language = data.get("language", "zh")
        services: dict[str, ServiceConfig] = {}

        # 解析 [service.xxx] 段 - TOML 会将其解析为嵌套字典
        service_section = data.get("service", {})
        if isinstance(service_section, dict):
            for service_name, service_data in service_section.items():
                if isinstance(service_data, dict):
                    services[service_name] = ServiceConfig.from_toml(service_name, service_data)

        if not services:
            raise ValueError(f"配置文件中未找到任何服务定义: {config_path}")

        return cls(language=language, services=services)

    def get_service(self, name: str) -> ServiceConfig | None:
        """获取指定服务配置"""
        return self.services.get(name)

    def list_services(self) -> list[str]:
        """列出所有服务名"""
        return list(self.services.keys())

    def get_service_names_by_type(self, service_type: str) -> list[str]:
        """按类型获取服务名列表"""
        return [name for name, cfg in self.services.items() if cfg.type == service_type]


# 全局缓存
_services_config: ServicesConfig | None = None


def get_services_config() -> ServicesConfig:
    """获取服务配置（带缓存）"""
    global _services_config
    if _services_config is None:
        _services_config = ServicesConfig.load()
    return _services_config


def reload_services_config() -> ServicesConfig:
    """重新加载服务配置"""
    global _services_config
    _services_config = ServicesConfig.load()
    return _services_config
