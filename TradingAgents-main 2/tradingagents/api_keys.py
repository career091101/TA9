"""
TradingAgentsプロジェクトのAPIキー管理モジュール

このモジュールはAPIキーの安全な管理、検証、および取得機能を提供します。
"""

import os
from typing import Dict, Optional, Tuple
from .config_types import LLMProviderType


class APIKeyManager:
    """APIキーの管理クラス
    
    このクラスはAPIキーの検証、取得、プロバイダー固有の処理を提供します。
    """
    
    # 必須APIキー
    REQUIRED_KEYS = {
        "OPENAI_API_KEY": "OpenAI API",
        "FINNHUB_API_KEY": "Finnhub API"
    }
    
    # オプションAPIキー
    OPTIONAL_KEYS = {
        "ANTHROPIC_API_KEY": "Anthropic Claude API",
        "GOOGLE_API_KEY": "Google Generative AI API"
    }
    
    # プロバイダーごとの必要なAPIキー
    PROVIDER_API_KEYS = {
        "openai": ["OPENAI_API_KEY"],
        "anthropic": ["ANTHROPIC_API_KEY"],
        "google": ["GOOGLE_API_KEY"],
        "ollama": [],  # ローカルなので不要
        "openrouter": ["OPENAI_API_KEY"]  # OpenRouter互換
    }
    
    def __init__(self):
        """APIキーマネージャーを初期化"""
        self._api_keys_cache: Dict[str, str] = {}
        self._load_api_keys()
    
    def _load_api_keys(self) -> None:
        """環境変数からAPIキーを読み込み"""
        all_keys = {**self.REQUIRED_KEYS, **self.OPTIONAL_KEYS}
        
        for key_name in all_keys:
            value = os.getenv(key_name)
            if value:
                self._api_keys_cache[key_name] = value
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """APIキーを安全に取得
        
        Args:
            key_name: APIキー名
            
        Returns:
            Optional[str]: APIキーの値、存在しない場合はNone
        """
        return self._api_keys_cache.get(key_name)
    
    def validate_all_keys(self) -> Tuple[Dict[str, bool], Dict[str, str]]:
        """全APIキーの存在を検証
        
        Returns:
            Tuple[Dict[str, bool], Dict[str, str]]: 
                - キーの存在状況
                - エラーメッセージ
        """
        validation_results = {}
        error_messages = {}
        
        # 必須キーの検証
        for key_name, description in self.REQUIRED_KEYS.items():
            exists = key_name in self._api_keys_cache
            validation_results[key_name] = exists
            
            if not exists:
                error_messages[key_name] = f"必須APIキー '{key_name}' ({description}) が設定されていません"
        
        # オプションキーの検証
        for key_name, description in self.OPTIONAL_KEYS.items():
            exists = key_name in self._api_keys_cache
            validation_results[key_name] = exists
            
            if not exists:
                error_messages[key_name] = f"オプションAPIキー '{key_name}' ({description}) が設定されていません"
        
        return validation_results, error_messages
    
    def validate_provider_keys(self, provider: LLMProviderType) -> Tuple[bool, list[str]]:
        """特定のプロバイダーに必要なAPIキーを検証
        
        Args:
            provider: LLMプロバイダー名
            
        Returns:
            Tuple[bool, list[str]]: 
                - すべてのキーが存在するかどうか
                - 不足しているキーのリスト
        """
        required_keys = self.PROVIDER_API_KEYS.get(provider, [])
        missing_keys = []
        
        for key_name in required_keys:
            if key_name not in self._api_keys_cache:
                missing_keys.append(key_name)
        
        return len(missing_keys) == 0, missing_keys
    
    def get_provider_api_key(self, provider: LLMProviderType) -> Optional[str]:
        """プロバイダーに対応するAPIキーを取得
        
        Args:
            provider: LLMプロバイダー名
            
        Returns:
            Optional[str]: APIキーの値
        """
        required_keys = self.PROVIDER_API_KEYS.get(provider, [])
        
        if not required_keys:
            return None  # ローカルプロバイダーなど
        
        # 最初に見つかったキーを返す
        for key_name in required_keys:
            api_key = self.get_api_key(key_name)
            if api_key:
                return api_key
        
        return None
    
    def print_validation_report(self) -> None:
        """APIキーの検証レポートを表示"""
        validation_results, error_messages = self.validate_all_keys()
        
        print("\n=== APIキー検証レポート ===")
        
        # 必須キーの状況
        print("\n🔑 必須APIキー:")
        for key_name, description in self.REQUIRED_KEYS.items():
            status = "✅ 設定済み" if validation_results[key_name] else "❌ 未設定"
            print(f"  {key_name} ({description}): {status}")
        
        # オプションキーの状況
        print("\n🔧 オプションAPIキー:")
        for key_name, description in self.OPTIONAL_KEYS.items():
            status = "✅ 設定済み" if validation_results[key_name] else "⚠️ 未設定"
            print(f"  {key_name} ({description}): {status}")
        
        # エラーがある場合の対処法を表示
        missing_required = [k for k in self.REQUIRED_KEYS.keys() if not validation_results[k]]
        if missing_required:
            print("\n🚨 対処が必要:")
            print("  1. プロジェクトルートに .env ファイルを作成")
            print("  2. .env.example を参考に以下のキーを設定:")
            for key_name in missing_required:
                print(f"     {key_name}=your_api_key_here")
            print("  3. アプリケーションを再起動")
    
    def has_required_keys(self) -> bool:
        """必須APIキーがすべて設定されているかチェック
        
        Returns:
            bool: 必須キーがすべて設定されている場合True
        """
        for key_name in self.REQUIRED_KEYS.keys():
            if key_name not in self._api_keys_cache:
                return False
        return True


# グローバルなAPIキーマネージャーインスタンス
api_key_manager = APIKeyManager()


def get_api_key(key_name: str) -> Optional[str]:
    """APIキーを取得する便利関数
    
    Args:
        key_name: APIキー名
        
    Returns:
        Optional[str]: APIキーの値
    """
    return api_key_manager.get_api_key(key_name)


def validate_api_keys() -> bool:
    """APIキーを検証する便利関数
    
    Returns:
        bool: 必須キーがすべて設定されている場合True
    """
    api_key_manager.print_validation_report()
    return api_key_manager.has_required_keys()


def get_provider_api_key(provider: LLMProviderType) -> Optional[str]:
    """プロバイダー用のAPIキーを取得する便利関数
    
    Args:
        provider: LLMプロバイダー名
        
    Returns:
        Optional[str]: APIキーの値
    """
    return api_key_manager.get_provider_api_key(provider)