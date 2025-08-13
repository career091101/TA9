"""
TradingAgentsプロジェクトの設定型定義

このモジュールは設定値の型安全性を確保するためのTypedDictを定義しています。
"""

from typing import TypedDict, Literal, Optional

# 補助型定義
LLMProviderType = Literal["openai", "anthropic", "google", "ollama", "openrouter"]


class TradingAgentsConfig(TypedDict):
    """TradingAgentsの完全な設定型定義
    
    この型は、TradingAgentsシステムで必要なすべての設定項目を定義しています。
    すべてのフィールドが必須です。
    """
    
    # パス設定
    project_dir: str
    results_dir: str
    data_dir: str
    data_cache_dir: str
    
    # LLM設定
    llm_provider: LLMProviderType
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str
    
    # 動作設定
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    max_recur_limit: int
    online_tools: bool


class PartialConfig(TypedDict, total=False):
    """部分的な設定（オーバーライド用）
    
    この型は設定のオーバーライドやカスタマイズに使用されます。
    すべてのフィールドがオプショナルです。
    """
    
    # パス設定
    project_dir: str
    results_dir: str
    data_dir: str
    data_cache_dir: str
    
    # LLM設定
    llm_provider: LLMProviderType
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str
    
    # 動作設定
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    max_recur_limit: int
    online_tools: bool


class PathConfigType(TypedDict):
    """パス関連の設定型"""
    project_dir: str
    results_dir: str
    data_dir: str
    data_cache_dir: str


class LLMConfigType(TypedDict):
    """LLM関連の設定型"""
    llm_provider: LLMProviderType
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str


class OperationConfigType(TypedDict):
    """動作関連の設定型"""
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    max_recur_limit: int
    online_tools: bool