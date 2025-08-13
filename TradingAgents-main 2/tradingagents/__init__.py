"""
TradingAgents - マルチエージェントLLM駆動金融取引フレームワーク

実世界のトレーディング会社のダイナミクスをシミュレートし、
専門エージェント（アナリスト、リサーチャー、トレーダー、リスクマネージャー）が
協力して取引決定を行うフレームワークです。
"""

from .default_config import DEFAULT_CONFIG, get_default_config
from .config_loader import load_config, validate_config, get_config_from_env
from .config_types import TradingAgentsConfig, PartialConfig, LLMProviderType
from .api_keys import (
    APIKeyManager,
    api_key_manager,
    get_api_key,
    validate_api_keys,
    get_provider_api_key
)
from .setup_utils import (
    check_environment,
    setup_environment,
    quick_setup
)

__version__ = "1.0.0"
__author__ = "TradingAgents Team"
__description__ = "Multi-agent LLM-driven financial trading framework"

__all__ = [
    # 設定関連
    "DEFAULT_CONFIG",
    "get_default_config",
    "load_config",
    "validate_config",
    "get_config_from_env",
    "TradingAgentsConfig",
    "PartialConfig",
    "LLMProviderType",
    
    # APIキー管理
    "APIKeyManager",
    "api_key_manager",
    "get_api_key",
    "validate_api_keys",
    "get_provider_api_key",
    
    # セットアップ支援
    "check_environment",
    "setup_environment",
    "quick_setup",
]