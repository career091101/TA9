# チケット008: メモリシステムの型定義改修

## 概要

TradingAgentsプロジェクトにおけるメモリシステム（`FinancialSituationMemory`クラス）の型安全性を向上させます。現在、メモリクラスのコンストラクタ引数エラーが1件発生しており、エージェントの記憶機能の信頼性に影響を与えています。

## 現状分析

### 影響範囲
- **agents/utils/memory.py**: 1件の引数エラー
- メモリを使用する全てのエージェント
- 長期的な学習・記憶機能

### 主要なエラーパターン

1. **コンストラクタ引数の不足**
   ```python
   # 問題のあるコード
   memory = FinancialSituationMemory()  # [call-arg] missing required args
   
   # 期待される呼び出し
   memory = FinancialSituationMemory(name="trading_memory", config=config)
   ```

2. **メモリ状態の型定義不備**
   ```python
   # 型が不明確なメモリ操作
   memory.store(data)  # dataの型が不明
   result = memory.retrieve(query)  # 戻り値の型が不明
   ```

## 要件定義

### 機能要件
- [ ] FinancialSituationMemoryクラスの型安全化
- [ ] メモリ操作APIの型定義改善
- [ ] 記憶データの型安全な管理
- [ ] メモリ永続化の型安全性確保

### 非機能要件
- [ ] 既存のメモリ機能の互換性維持
- [ ] メモリアクセス性能の保持
- [ ] 並行アクセスの安全性
- [ ] データ整合性の保証

### 制約事項
- 既存のメモリデータ形式との互換性
- LangChainメモリシステムとの統合
- ディスク永続化機能の維持

## 実装計画

### 対象ファイル一覧
- `tradingagents/agents/utils/memory.py`
- メモリを使用するエージェントクラス
- メモリ設定関連ファイル

### 修正方針

1. **MemoryConfigの型定義**
   ```python
   from typing import TypedDict, Optional
   
   class MemoryConfig(TypedDict):
       storage_path: Optional[str]
       max_entries: int
       retention_days: int
       enable_persistence: bool
   ```

2. **型安全なメモリクラス**
   ```python
   from typing import Generic, TypeVar, List, Dict, Any, Optional
   
   T = TypeVar('T')
   
   class FinancialSituationMemory(Generic[T]):
       def __init__(
           self, 
           name: str, 
           config: MemoryConfig
       ) -> None:
           self.name = name
           self.config = config
           
       def store(self, key: str, data: T) -> bool:
           """型安全なデータ保存"""
           
       def retrieve(self, key: str) -> Optional[T]:
           """型安全なデータ取得"""
   ```

3. **メモリ操作の標準化**
   ```python
   class MemoryOperations:
       def create_memory(
           self,
           name: str,
           config: Optional[MemoryConfig] = None
       ) -> FinancialSituationMemory:
           """型安全なメモリインスタンス作成"""
   ```

### 見積もり工数
- 設計・調査: 0.5日
- 実装: 1.5日
- テスト・検証: 1日
- **合計: 3日**

## 受け入れ条件

- [ ] メモリ関連の型エラー1件が解消される
- [ ] FinancialSituationMemoryの型チェックが通過する
- [ ] 既存のメモリ機能が正常動作する
- [ ] メモリの並行アクセスが安全に動作する
- [ ] 永続化機能が正常に動作する

## Todoリスト

### Phase 1: メモリ型設計
- [ ] MemoryConfigの詳細設計
- [ ] メモリデータ型の定義
- [ ] ジェネリック型パラメータの設計
- [ ] メモリ操作インターフェースの設計

### Phase 2: 基盤実装
- [ ] MemoryConfigクラスの実装
- [ ] 型安全なメモリベースクラス実装
- [ ] データシリアライゼーションの型対応
- [ ] エラーハンドリングの型安全化

### Phase 3: FinancialSituationMemory修正
- [ ] コンストラクタ引数の修正
- [ ] store/retrieveメソッドの型安全化
- [ ] メモリ検索機能の型安全化
- [ ] メモリクリア機能の型安全化

### Phase 4: 永続化機能の型安全化
- [ ] ファイル保存の型安全性確保
- [ ] デシリアライゼーションの型安全性
- [ ] 設定ファイルの型安全な読み込み
- [ ] バックアップ機能の型安全化

### Phase 5: エージェント統合
- [ ] エージェントでのメモリ利用修正
- [ ] メモリファクトリー関数の実装
- [ ] 設定からのメモリ初期化修正
- [ ] エラーハンドリングの統合

### Phase 6: テストと検証
- [ ] メモリ操作のユニットテスト
- [ ] 並行アクセステスト
- [ ] 永続化機能のテスト
- [ ] メモリリークテスト

### Phase 7: ドキュメント整備
- [ ] メモリシステム利用ガイド
- [ ] 型安全なメモリ操作のベストプラクティス
- [ ] 設定オプションのリファレンス

## 依存関係

### 前提条件
- **003_function_annotations.md**: 基本的な型注釈標準
- **005_config_type_safety.md**: 設定システムの型安全性

### 影響を与えるチケット
- **006_agent_state_types.md**: エージェント状態との統合

### 後続チケット
- **009_testing_strategy.md**: メモリ機能のテスト戦略

## 優先度: Medium

### 根拠
- エージェント学習機能の重要な基盤
- 1件のエラーだが影響範囲が広い
- 長期的な動作安定性に重要
- データ整合性の確保が必要

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 既存メモリデータ互換性 | 中 | 低 | 移行ツールとバックワード互換性 |
| メモリ性能劣化 | 中 | 低 | 効率的な型チェック実装 |
| 並行アクセス問題 | 高 | 低 | スレッドセーフな実装 |
| データ損失リスク | 高 | 極低 | 十分なテストと段階的移行 |

## 技術仕様

### メモリ型定義

```python
from typing import TypedDict, Generic, TypeVar, Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import threading

# メモリ設定型
class MemoryConfig(TypedDict):
    storage_path: Optional[str]
    max_entries: int
    retention_days: int
    enable_persistence: bool
    cache_size: int
    compression: bool

# メモリエントリ型
@dataclass
class MemoryEntry:
    key: str
    data: Any
    timestamp: datetime
    access_count: int
    tags: List[str]

T = TypeVar('T')

# ジェネリックメモリクラス
class FinancialSituationMemory(Generic[T]):
    def __init__(
        self, 
        name: str, 
        config: MemoryConfig
    ) -> None:
        self.name = name
        self.config = config
        self._storage: Dict[str, MemoryEntry] = {}
        self._lock = threading.RLock()
        
        if config.get("enable_persistence", False):
            self._load_from_disk()
    
    def store(
        self, 
        key: str, 
        data: T, 
        tags: Optional[List[str]] = None
    ) -> bool:
        """型安全なデータ保存"""
        
    def retrieve(self, key: str) -> Optional[T]:
        """型安全なデータ取得"""
        
    def search(
        self, 
        query: str, 
        tags: Optional[List[str]] = None
    ) -> List[T]:
        """型安全な検索"""
        
    def clear(self, older_than: Optional[datetime] = None) -> int:
        """メモリクリア（削除件数を返す）"""
```

### 専用メモリ型

```python
# 取引記録用メモリ
class TradeMemory(FinancialSituationMemory[Dict[str, Any]]):
    def store_trade(
        self,
        ticker: str,
        action: str,
        price: float,
        quantity: int,
        timestamp: datetime
    ) -> bool:
        trade_data = {
            "ticker": ticker,
            "action": action,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp
        }
        return self.store(f"trade_{ticker}_{timestamp}", trade_data)

# 分析結果用メモリ
class AnalysisMemory(FinancialSituationMemory[str]):
    def store_analysis(
        self,
        ticker: str,
        analysis_type: str,
        result: str,
        confidence: float
    ) -> bool:
        key = f"analysis_{ticker}_{analysis_type}_{datetime.now()}"
        return self.store(key, result, tags=[analysis_type, ticker])
```

### メモリファクトリー

```python
from typing import Type, TypeVar

M = TypeVar('M', bound=FinancialSituationMemory)

class MemoryFactory:
    def __init__(self, default_config: MemoryConfig):
        self.default_config = default_config
    
    def create_memory(
        self,
        memory_class: Type[M],
        name: str,
        config: Optional[MemoryConfig] = None
    ) -> M:
        """型安全なメモリインスタンス作成"""
        final_config = config or self.default_config
        return memory_class(name=name, config=final_config)
    
    def create_trade_memory(self, name: str) -> TradeMemory:
        """取引記録メモリの作成"""
        return self.create_memory(TradeMemory, name)
    
    def create_analysis_memory(self, name: str) -> AnalysisMemory:
        """分析結果メモリの作成"""
        return self.create_memory(AnalysisMemory, name)

# 使用例
factory = MemoryFactory(default_config={
    "storage_path": "./memory",
    "max_entries": 1000,
    "retention_days": 30,
    "enable_persistence": True,
    "cache_size": 100,
    "compression": True
})

trade_memory = factory.create_trade_memory("agent_trades")
analysis_memory = factory.create_analysis_memory("market_analysis")
```

### 永続化機能

```python
import json
import pickle
from pathlib import Path

class MemoryPersistence:
    @staticmethod
    def save_memory(
        memory: FinancialSituationMemory,
        path: str
    ) -> bool:
        """型安全なメモリ保存"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'wb') as f:
                pickle.dump(memory._storage, f)
            return True
            
        except Exception as e:
            logger.error(f"Memory save failed: {e}")
            return False
    
    @staticmethod
    def load_memory(
        memory: FinancialSituationMemory,
        path: str
    ) -> bool:
        """型安全なメモリ読み込み"""
        try:
            if not Path(path).exists():
                return True  # 新規メモリの場合
                
            with open(path, 'rb') as f:
                memory._storage = pickle.load(f)
            return True
            
        except Exception as e:
            logger.error(f"Memory load failed: {e}")
            return False
```