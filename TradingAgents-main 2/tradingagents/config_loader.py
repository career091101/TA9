"""
TradingAgentsプロジェクトの型安全な設定ローダー

このモジュールは設定の読み込み、検証、環境変数の処理を提供します。
.envファイルからの環境変数読み込みをサポートします。
"""

import os
from typing import Optional, Any
from .config_types import TradingAgentsConfig, PartialConfig, LLMProviderType

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False


def get_bool_env(key: str, default: bool) -> bool:
    """環境変数をbool型として型安全に読み込む
    
    Args:
        key: 環境変数名
        default: デフォルト値
        
    Returns:
        bool: 環境変数の値またはデフォルト値
    """
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def get_int_env(key: str, default: int) -> int:
    """環境変数をint型として型安全に読み込む
    
    Args:
        key: 環境変数名
        default: デフォルト値
        
    Returns:
        int: 環境変数の値またはデフォルト値
        
    Raises:
        ValueError: 環境変数がintに変換できない場合
    """
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Environment variable {key}='{value}' cannot be converted to int") from e


def get_str_env(key: str, default: str) -> str:
    """環境変数をstr型として型安全に読み込む
    
    Args:
        key: 環境変数名
        default: デフォルト値
        
    Returns:
        str: 環境変数の値またはデフォルト値
    """
    return os.getenv(key, default)


def load_env_file() -> None:
    """環境変数ファイル(.env)を読み込む
    
    python-dotenvが利用可能な場合、プロジェクトルートの.envファイルを読み込みます。
    """
    if _DOTENV_AVAILABLE:
        # プロジェクトルートの.envファイルを探す
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        env_file = os.path.join(project_root, ".env")
        
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"環境変数ファイルを読み込みました: {env_file}")
        else:
            print(f"環境変数ファイルが見つかりません: {env_file}")
            print("APIキーは環境変数から直接読み込まれます。")
    else:
        print("警告: python-dotenvがインストールされていません。")
        print("pip install python-dotenvでインストールしてください。")


def validate_api_keys() -> dict[str, bool]:
    """APIキーの存在を確認する
    
    Returns:
        dict[str, bool]: 各APIキーの存在状況
    """
    api_keys = {
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        "FINNHUB_API_KEY": bool(os.getenv("FINNHUB_API_KEY")),
        "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
        "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
    }
    
    # 必須APIキーのチェック
    missing_required = []
    if not api_keys["OPENAI_API_KEY"]:
        missing_required.append("OPENAI_API_KEY")
    if not api_keys["FINNHUB_API_KEY"]:
        missing_required.append("FINNHUB_API_KEY")
    
    if missing_required:
        print(f"警告: 必須APIキーが設定されていません: {', '.join(missing_required)}")
        print("プロジェクトルートに.envファイルを作成して設定してください。")
        print(".env.exampleファイルを参考にしてください。")
    
    return api_keys


def get_config_from_env() -> PartialConfig:
    """環境変数から設定を型安全に読み込む
    
    Returns:
        PartialConfig: 環境変数から読み込んだ設定
    """
    # .envファイルを読み込み
    load_env_file()
    
    # APIキーの確認
    validate_api_keys()
    
    config: PartialConfig = {}
    
    # パス設定
    if os.getenv("TRADINGAGENTS_RESULTS_DIR"):
        config["results_dir"] = get_str_env("TRADINGAGENTS_RESULTS_DIR", "./results")
    
    if os.getenv("TRADINGAGENTS_DATA_DIR"):
        config["data_dir"] = get_str_env("TRADINGAGENTS_DATA_DIR", "/data")
    
    # LLM設定
    if os.getenv("TRADINGAGENTS_LLM_PROVIDER"):
        provider = get_str_env("TRADINGAGENTS_LLM_PROVIDER", "openai")
        if provider in ("openai", "anthropic", "google", "ollama", "openrouter"):
            config["llm_provider"] = provider  # type: ignore
        else:
            raise ValueError(f"Unsupported LLM provider from environment: {provider}")
    
    if os.getenv("TRADINGAGENTS_DEEP_THINK_LLM"):
        config["deep_think_llm"] = get_str_env("TRADINGAGENTS_DEEP_THINK_LLM", "o4-mini")
    
    if os.getenv("TRADINGAGENTS_QUICK_THINK_LLM"):
        config["quick_think_llm"] = get_str_env("TRADINGAGENTS_QUICK_THINK_LLM", "gpt-4o-mini")
    
    if os.getenv("TRADINGAGENTS_BACKEND_URL"):
        config["backend_url"] = get_str_env("TRADINGAGENTS_BACKEND_URL", "https://api.openai.com/v1")
    
    # 動作設定
    if os.getenv("TRADINGAGENTS_MAX_DEBATE_ROUNDS"):
        config["max_debate_rounds"] = get_int_env("TRADINGAGENTS_MAX_DEBATE_ROUNDS", 1)
    
    if os.getenv("TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS"):
        config["max_risk_discuss_rounds"] = get_int_env("TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS", 1)
    
    if os.getenv("TRADINGAGENTS_MAX_RECUR_LIMIT"):
        config["max_recur_limit"] = get_int_env("TRADINGAGENTS_MAX_RECUR_LIMIT", 100)
    
    if os.getenv("TRADINGAGENTS_ONLINE_TOOLS"):
        config["online_tools"] = get_bool_env("TRADINGAGENTS_ONLINE_TOOLS", True)
    
    return config


def validate_config(config: TradingAgentsConfig) -> TradingAgentsConfig:
    """設定の検証を行う
    
    Args:
        config: 検証する設定
        
    Returns:
        TradingAgentsConfig: 検証済みの設定
        
    Raises:
        ValueError: 設定値が不正な場合
        TypeError: 設定の型が不正な場合
    """
    # 必須フィールドの存在チェック
    required_fields = [
        "project_dir", "results_dir", "data_dir", "data_cache_dir",
        "llm_provider", "deep_think_llm", "quick_think_llm", "backend_url",
        "max_debate_rounds", "max_risk_discuss_rounds", "max_recur_limit", "online_tools"
    ]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Required configuration field '{field}' is missing")
    
    # 型チェック
    if not isinstance(config["project_dir"], str):
        raise TypeError("project_dir must be a string")
    
    if not isinstance(config["results_dir"], str):
        raise TypeError("results_dir must be a string")
    
    if not isinstance(config["data_dir"], str):
        raise TypeError("data_dir must be a string")
    
    if not isinstance(config["data_cache_dir"], str):
        raise TypeError("data_cache_dir must be a string")
    
    # LLMプロバイダーの検証
    valid_providers = ("openai", "anthropic", "google", "ollama", "openrouter")
    if config["llm_provider"] not in valid_providers:
        raise ValueError(f"Unsupported LLM provider: {config['llm_provider']}. Must be one of: {valid_providers}")
    
    if not isinstance(config["deep_think_llm"], str):
        raise TypeError("deep_think_llm must be a string")
    
    if not isinstance(config["quick_think_llm"], str):
        raise TypeError("quick_think_llm must be a string")
    
    if not isinstance(config["backend_url"], str):
        raise TypeError("backend_url must be a string")
    
    # 数値の検証
    if not isinstance(config["max_debate_rounds"], int):
        raise TypeError("max_debate_rounds must be an integer")
    
    if config["max_debate_rounds"] < 0:
        raise ValueError("max_debate_rounds must be non-negative")
    
    if not isinstance(config["max_risk_discuss_rounds"], int):
        raise TypeError("max_risk_discuss_rounds must be an integer")
    
    if config["max_risk_discuss_rounds"] < 0:
        raise ValueError("max_risk_discuss_rounds must be non-negative")
    
    if not isinstance(config["max_recur_limit"], int):
        raise TypeError("max_recur_limit must be an integer")
    
    if config["max_recur_limit"] <= 0:
        raise ValueError("max_recur_limit must be positive")
    
    # ブール値の検証
    if not isinstance(config["online_tools"], bool):
        raise TypeError("online_tools must be a boolean")
    
    # パスの存在チェック（プロジェクトディレクトリ）
    if not os.path.exists(config["project_dir"]):
        raise ValueError(f"Project directory does not exist: {config['project_dir']}")
    
    return config


def load_config(override: Optional[PartialConfig] = None, validate_keys: bool = True) -> TradingAgentsConfig:
    """型安全な設定のロード
    
    デフォルト設定、環境変数、オーバーライドの順で設定を構築します。
    .env ファイルの読み込みとAPIキーの検証も実行します。
    
    Args:
        override: オーバーライドする設定項目
        validate_keys: APIキーの検証を実行するかどうか (デフォルト: True)
        
    Returns:
        TradingAgentsConfig: 完全な設定オブジェクト
        
    Raises:
        ValueError: 設定値が不正な場合、または必須APIキーが不足している場合
        TypeError: 設定の型が不正な場合
    """
    # デフォルト設定
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    
    config: TradingAgentsConfig = {
        "project_dir": project_dir,
        "results_dir": "./results",
        "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", "/Users/yluo/Documents/Code/ScAI/FR1-data"),
        "data_cache_dir": os.path.join(project_dir, "dataflows/data_cache"),
        "llm_provider": "openai",
        "deep_think_llm": "o4-mini",
        "quick_think_llm": "gpt-4o-mini",
        "backend_url": "https://api.openai.com/v1",
        "max_debate_rounds": 1,
        "max_risk_discuss_rounds": 1,
        "max_recur_limit": 100,
        "online_tools": True,
    }
    
    # 環境変数からの設定を適用
    env_config = get_config_from_env()
    config.update(env_config)  # type: ignore
    
    # オーバーライドを適用
    if override:
        config.update(override)  # type: ignore
    
    # 設定の検証
    validated_config = validate_config(config)
    
    # APIキーの検証（オプション）
    if validate_keys:
        from .api_keys import validate_api_keys
        if not validate_api_keys():
            raise ValueError("必須APIキーが設定されていません。.envファイルを確認してください。")
    
    return validated_config