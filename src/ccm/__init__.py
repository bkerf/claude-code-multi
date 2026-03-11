"""
Claude Code Model Switcher (CCM)
Cross-platform CLI to switch Claude Code AI providers.
"""

__version__ = "3.0.0"
__author__ = "Peng"

from ccm.config_legacy import Config
from ccm.providers.base import BaseProvider, ProviderConfig

__all__ = [
    "__version__",
    "Config",
    "BaseProvider",
    "ProviderConfig",
]
