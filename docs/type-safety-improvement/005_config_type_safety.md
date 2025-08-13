# チケット005: 設定の型安全性

## 概要
プロジェクトの設定（config）がDict[str, Any]として扱われており、型安全性が欠如している。TypedDictを使用して型安全な設定システムを構築する。

## 現状分析

### エラー件数
- **直接エラー数**: 15件
- **間接的影響**: プロジェクト全体
- **主要エラー**: `[assignment]` 型の不一致

### 主要な問題パターン
1. 設定値の型が不明確
2. キーの存在チェックなし
3. Any型の過度な使用
4. 環境変数との型不整合

### 影響ファイル
- `tradingagents/default_config.py`
- `tradingagents/graph/trading_graph.py`
- `tradingagents/dataflows/config.py`
- 全エージェントファイル（configを使用）

## 要件定義

### 機能要件
- FR-001: TypedDictによる設定型の定義
- FR-002: 環境変数の型安全な読み込み
- FR-003: 設定値の検証機能

### 非機能要件
- NFR-001: 後方互換性の維持
- NFR-002: 設定の拡張性
- NFR-003: 明確なエラーメッセージ

### 制約事項
- 既存の設定キーを変更しない
- 環境変数名を変更しない

## 実装計画

### 型定義の作成

#### 1. 設定型の定義
```python
# tradingagents/config_types.py
from typing import TypedDict, Literal, Optional

class TradingAgentsConfig(TypedDict):
    """TradingAgentsの設定型定義"""
    # パス設定
    project_dir: str
    results_dir: str
    data_dir: str
    data_cache_dir: str
    
    # LLM設定
    llm_provider: Literal["openai", "anthropic", "google", "ollama", "openrouter"]
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str
    
    # 動作設定
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    max_recur_limit: int
    online_tools: bool

class PartialConfig(TypedDict, total=False):
    """部分的な設定（オーバーライド用）"""
    llm_provider: Literal["openai", "anthropic", "google", "ollama", "openrouter"]
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    online_tools: bool
```

#### 2. 設定ローダーの実装
```python
# tradingagents/config_loader.py
import os
from typing import Optional
from tradingagents.config_types import TradingAgentsConfig, PartialConfig

def load_config(override: Optional[PartialConfig] = None) -> TradingAgentsConfig:
    """型安全な設定のロード"""
    config: TradingAgentsConfig = {
        "project_dir": os.path.abspath(os.path.dirname(__file__)),
        "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
        "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", "/data"),
        "data_cache_dir": os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "dataflows/data_cache"
        ),
        "llm_provider": "openai",
        "deep_think_llm": "o4-mini",
        "quick_think_llm": "gpt-4o-mini",
        "backend_url": "https://api.openai.com/v1",
        "max_debate_rounds": 1,
        "max_risk_discuss_rounds": 1,
        "max_recur_limit": 100,
        "online_tools": True,
    }
    
    if override:
        config.update(override)
    
    return validate_config(config)

def validate_config(config: TradingAgentsConfig) -> TradingAgentsConfig:
    """設定の検証"""
    if config["max_debate_rounds"] < 0:
        raise ValueError("max_debate_rounds must be non-negative")
    
    if config["llm_provider"] not in ["openai", "anthropic", "google", "ollama", "openrouter"]:
        raise ValueError(f"Unsupported LLM provider: {config['llm_provider']}")
    
    return config
```

### 見積もり工数
- 分析: 0.5日
- 実装: 1日
- テスト: 0.5日
- **合計: 2日**

## 受け入れ条件

### 必須条件
- [ ] 設定関連の型エラーが0件
- [ ] TypedDictによる型定義完了
- [ ] 既存コードとの互換性維持

### 推奨条件
- [ ] 設定のバリデーション実装
- [ ] 設定のシリアライズ/デシリアライズ

## Todoリスト

### 準備作業
- [ ] 現在の設定項目の洗い出し
- [ ] 環境変数の使用箇所確認
- [ ] デフォルト値の確認

### 実装作業

#### config_types.pyの作成
- [ ] TradingAgentsConfig型の定義
  - [ ] 必須フィールドの定義
  - [ ] 型制約の設定（Literal型）
  - [ ] ドキュメント文字列の追加
- [ ] PartialConfig型の定義
  - [ ] total=Falseの設定
  - [ ] オーバーライド可能項目の定義
- [ ] 補助型の定義
  - [ ] LLMProviderType
  - [ ] PathConfigType

#### config_loader.pyの作成
- [ ] load_config関数の実装
  - [ ] デフォルト値の設定
  - [ ] 環境変数の読み込み
  - [ ] オーバーライド処理
- [ ] validate_config関数の実装
  - [ ] 値の範囲チェック
  - [ ] 必須項目の確認
  - [ ] 型の検証
- [ ] get_config_from_env関数
  - [ ] 環境変数の型安全な読み込み

#### 既存コードの修正
- [ ] default_config.pyの更新
  - [ ] TypedDictの使用
  - [ ] インポートの更新
- [ ] trading_graph.pyの修正
  - [ ] config引数の型注釈
  - [ ] 設定アクセスの型安全化
- [ ] dataflows/config.pyの修正
  - [ ] グローバル設定の型定義
  - [ ] set_config関数の型注釈

#### 各エージェントの更新
- [ ] configパラメータの型注釈追加
- [ ] 設定値アクセスの型安全化

### テスト作業
- [ ] ユニットテストの作成
  - [ ] config_loaderのテスト
  - [ ] validateのテスト
  - [ ] 環境変数のテスト
- [ ] 統合テストの実行
  - [ ] 設定オーバーライドのテスト
  - [ ] エラーケースのテスト
- [ ] 型チェックの実行

### ドキュメント
- [ ] 設定項目の一覧作成
- [ ] 環境変数の説明
- [ ] カスタマイズガイド

## 依存関係
- 他のチケットから参照される基盤機能
- 最優先で実装すべき

## 優先度
**Critical** - システム全体の基盤

## リスクと対策

### リスク1: 後方互換性の破壊
**対策**:
- 段階的な移行
- 互換性レイヤーの提供
- 非推奨警告の実装

### リスク2: 設定の硬直化
**対策**:
- 拡張可能な設計
- プラグイン機構
- 動的設定の許可

### リスク3: 複雑性の増加
**対策**:
- シンプルなAPI
- 明確なドキュメント
- デフォルト値の提供

## 参考情報

### TypedDictの使用例
```python
from typing import TypedDict, Literal

class Config(TypedDict):
    name: str
    debug: bool
    mode: Literal["dev", "prod"]

# 使用
config: Config = {
    "name": "myapp",
    "debug": True,
    "mode": "dev"
}
```

### 環境変数の型安全な読み込み
```python
def get_bool_env(key: str, default: bool) -> bool:
    value = os.getenv(key, str(default))
    return value.lower() in ("true", "1", "yes")

def get_int_env(key: str, default: int) -> int:
    value = os.getenv(key, str(default))
    return int(value)
```

## 完了確認
- [ ] 全てのTodoが完了
- [ ] 型エラーが解消
- [ ] テストが全てパス
- [ ] 後方互換性の確認
- [ ] ドキュメント更新完了