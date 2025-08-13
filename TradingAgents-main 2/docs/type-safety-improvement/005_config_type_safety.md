# チケット005: 設定の型安全性改修

## 概要

TradingAgentsプロジェクトにおける設定管理システムの型安全性を確保します。現在、設定の読み込み・保存・アクセスにおいて型エラーが発生しており、LLMプロバイダーの設定やチャット設定などの重要な設定値の型安全性が確保されていません。

## 現状分析

### 影響範囲
- **dataflows/config.py**: 2件の設定管理エラー
- **graph/trading_graph.py**: 12件の設定利用エラー
- **default_config.py**: 設定値の型定義不備

### 主要なエラーパターン

1. **設定値の型不安全なアクセス**
   ```python
   # 問題のあるコード
   config_value: str = get_config().get("api_key")  # [assignment] object | Any -> str
   ```

2. **None値のnon-safeアクセス**
   ```python
   # 問題のあるコード  
   config_dict = get_config()  # dict | None
   result = config_dict.copy()  # [union-attr] None has no attribute 'copy'
   ```

3. **LLMプロバイダー設定の型エラー**
   ```python
   # 問題のあるコード
   llm: ChatOpenAI = create_llm(config["llm_provider"])  # [assignment] 型不一致
   ```

## 要件定義

### 機能要件
- [ ] 型安全な設定管理システムの実装
- [ ] 設定値の型定義とバリデーション
- [ ] デフォルト値の型安全な提供
- [ ] 設定変更の型安全なAPI

### 非機能要件
- [ ] 既存設定ファイルとの互換性維持
- [ ] 実行時オーバーヘッドの最小化
- [ ] 設定変更の検証機能
- [ ] エラーメッセージの分かりやすさ

### 制約事項
- JSON/YAML設定ファイルとの互換性
- 環境変数からの設定読み込み対応
- 既存のdefault_config.pyとの統合

## 実装計画

### 対象ファイル一覧
- `tradingagents/dataflows/config.py`
- `tradingagents/default_config.py`
- `tradingagents/graph/trading_graph.py`

### 修正方針

1. **型安全な設定定義**
   ```python
   from typing import TypedDict, Optional, Literal, Union
   from dataclasses import dataclass
   
   class TradingConfig(TypedDict):
       # LLM設定
       llm_provider: Literal["openai", "anthropic", "google"]
       deep_think_llm: str
       quick_think_llm: str
       
       # API設定
       openai_api_key: Optional[str]
       anthropic_api_key: Optional[str]
       
       # データベース設定
       online_tools: bool
       max_debate_rounds: int
   ```

2. **型安全な設定アクセス**
   ```python
   def get_config() -> Optional[TradingConfig]:
       """設定を型安全に取得"""
       
   def get_config_value(key: str, default: T) -> T:
       """型安全なデフォルト値付き取得"""
   ```

3. **バリデーション付き設定**
   ```python
   @dataclass
   class ConfigValidator:
       def validate_llm_config(self, config: TradingConfig) -> bool:
           """LLM設定のバリデーション"""
   ```

### 見積もり工数
- 設計: 1日
- 実装: 2日
- 検証: 1日
- **合計: 4日**

## 受け入れ条件

- [ ] 設定関連の型エラー14件が全て解消される
- [ ] mypyで設定関連ファイルの型チェックが通過する
- [ ] 既存の設定ファイルが正常に読み込める
- [ ] 設定値のバリデーションが機能する
- [ ] デフォルト設定の型安全性が確保される

## Todoリスト

### Phase 1: 設定型定義
- [ ] TradingConfig TypedDictの定義
- [ ] 設定値の詳細な型定義
- [ ] デフォルト値の型安全な定義
- [ ] 設定カテゴリの分類

### Phase 2: config.py の修正
- [ ] get_config関数の型安全化
- [ ] set_config関数の型安全化
- [ ] 設定保存の型安全性確保
- [ ] エラーハンドリングの改善

### Phase 3: default_config.py の型安全化
- [ ] DEFAULT_CONFIG の型注釈追加
- [ ] 設定値のバリデーション追加
- [ ] 型安全なマージ機能実装
- [ ] 設定継承の型安全性確保

### Phase 4: trading_graph.py の修正
- [ ] LLMプロバイダー選択の型安全化
- [ ] チャット設定の型安全なアクセス
- [ ] 設定による条件分岐の型安全化
- [ ] エラーハンドリングの型安全化

### Phase 5: バリデーションシステム
- [ ] 設定値の妥当性チェック
- [ ] 必須設定の存在確認
- [ ] 設定値の範囲チェック
- [ ] 設定間の整合性チェック

### Phase 6: テストと検証
- [ ] 設定読み込みテスト
- [ ] バリデーションテスト
- [ ] エラーケースのテスト
- [ ] 既存設定ファイルとの互換性テスト

## 依存関係

### 前提条件
- **003_function_annotations.md**: 基本的な型注釈標準

### 影響を与えるチケット
- **002_langchain_message_types.md**: LLM設定との統合
- **006_agent_state_types.md**: エージェント設定との統合

### 後続チケット
- **009_testing_strategy.md**: 設定テストの統合

## 優先度: Critical

### 根拠
- システム全体の動作を制御する中核機能
- 実行時エラーのリスクが高い
- デバッグが困難な設定関連バグの予防
- CI/CD環境での自動化に影響

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 既存設定ファイル互換性 | 高 | 低 | 段階的移行とバックワード互換性 |
| 設定変更の影響範囲 | 中 | 中 | 詳細なテストと検証 |
| パフォーマンス影響 | 低 | 低 | 効率的な型チェック |
| 設定複雑化 | 中 | 中 | シンプルで直感的なAPI設計 |

## 技術仕様

### 設定型定義

```python
from typing import TypedDict, Optional, Literal, Union, Dict, Any
from dataclasses import dataclass, field

# 基本設定型
class LLMConfig(TypedDict):
    provider: Literal["openai", "anthropic", "google"]
    model: str
    api_key: Optional[str]
    base_url: Optional[str]
    temperature: float
    max_tokens: int

class DataConfig(TypedDict):
    online_tools: bool
    finnhub_api_key: Optional[str]
    cache_directory: str
    cache_expiry: int

class TradingConfig(TypedDict):
    llm: LLMConfig
    data: DataConfig
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    results_directory: str
```

### 設定アクセスAPI

```python
class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self._config: Optional[TradingConfig] = None
        self._validator = ConfigValidator()
    
    def load_config(self, path: str) -> TradingConfig:
        """型安全な設定読み込み"""
        
    def get_llm_config(self) -> LLMConfig:
        """LLM設定の型安全な取得"""
        
    def get_data_config(self) -> DataConfig:
        """データ設定の型安全な取得"""
        
    def validate(self) -> List[str]:
        """設定の妥当性検証"""
```

### バリデーション機能

```python
class ConfigValidator:
    def validate_llm_config(self, config: LLMConfig) -> List[str]:
        """LLM設定のバリデーション"""
        errors = []
        
        if config["provider"] not in ["openai", "anthropic", "google"]:
            errors.append("Invalid LLM provider")
            
        if config["temperature"] < 0 or config["temperature"] > 2:
            errors.append("Temperature must be between 0 and 2")
            
        return errors
    
    def validate_required_keys(self, config: Dict[str, Any]) -> List[str]:
        """必須設定キーの存在確認"""
        required_keys = ["llm", "data", "max_debate_rounds"]
        return [key for key in required_keys if key not in config]
```

### 使用例

```python
# 型安全な設定利用
config_manager = ConfigManager("config.yaml")
config = config_manager.load_config()

# 型ヒントが効く
llm_config = config["llm"]  # Type: LLMConfig
provider = llm_config["provider"]  # Type: Literal["openai", "anthropic", "google"]

# バリデーション
errors = config_manager.validate()
if errors:
    raise ValueError(f"Configuration errors: {errors}")
```