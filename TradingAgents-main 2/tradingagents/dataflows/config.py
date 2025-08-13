"""
データフロー用の設定管理

このモジュールはデータフロー用の設定管理を提供します。
新しいコードでは型安全な設定システムの使用を推奨します。
"""

import tradingagents.default_config as default_config
from typing import Dict, Optional, Union
from tradingagents.config_types import TradingAgentsConfig, PartialConfig

# Use default config but allow it to be overridden  
_config: Optional[Dict] = None
DATA_DIR: Optional[str] = None


def initialize_config():
    """Initialize the configuration with default values."""
    global _config, DATA_DIR
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
        DATA_DIR = _config["data_dir"]


def set_config(config: Union[Dict, TradingAgentsConfig, PartialConfig]):
    """Update the configuration with custom values.
    
    Args:
        config: 設定オブジェクト（Dictionary、TradingAgentsConfig、またはPartialConfig）
    """
    global _config, DATA_DIR
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
    _config.update(config)  # type: ignore
    DATA_DIR = _config["data_dir"]


def get_config() -> Dict:
    """Get the current configuration.
    
    Returns:
        Dict: 現在の設定のコピー
    """
    if _config is None:
        initialize_config()
    return _config.copy()  # type: ignore


def get_data_dir() -> str:
    """Get the current data directory.
    
    Returns:
        str: データディレクトリのパス
    """
    if _config is None:
        initialize_config()
    return DATA_DIR or ""


# Initialize with default config
initialize_config()
