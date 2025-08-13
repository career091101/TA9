"""
TradingAgentsプロジェクトのデフォルト設定

このモジュールは後方互換性のために保持されています。
新しいコードでは config_loader.load_config() の使用を推奨します。
"""

import os
from typing import Dict, Any
from .config_types import TradingAgentsConfig
from .config_loader import load_config

# 後方互換性のためのデフォルト設定（Dict[str, Any]型）
DEFAULT_CONFIG: Dict[str, Any] = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
}


def get_default_config() -> TradingAgentsConfig:
    """型安全なデフォルト設定を取得
    
    Returns:
        TradingAgentsConfig: デフォルト設定
    """
    return load_config()
