# チケット003: 関数の型注釈標準化

## 概要

TradingAgentsプロジェクト全体における関数の型注釈を標準化し、型安全性を向上させます。現在、多くの関数で型注釈が不足または不正確であり、特にOptional引数やUnion型の処理に問題があります。統一された型注釈標準を確立し、全関数に適用します。

## 現状分析

### 影響範囲
- **dataflows/**: 15件の型注釈不備
- **agents/**: 8件の型注釈不備
- **graph/**: 7件の型注釈不備
- **cli/**: 5件の型注釈不備

### 主要な問題パターン

1. **implicit Optional引数**
   ```python
   # 問題のあるコード (PEP 484違反)
   def save_output(data: str, save_path: str = None):  # [assignment] error
   
   # 修正後
   def save_output(data: str, save_path: Optional[str] = None):
   ```

2. **戻り値型の不一致**
   ```python
   # 問題のあるコード
   def get_data() -> str:
       return pd.DataFrame()  # [return-value] error
   
   # 修正後  
   def get_data() -> Union[str, pd.DataFrame]:
   ```

3. **selfパラメータの型エラー**
   ```python
   # 問題のあるコード
   def get_stock_data(ticker: str):  # [misc] self missing
   
   # 修正後
   def get_stock_data(self, ticker: str):
   ```

## 要件定義

### 機能要件
- [ ] 全関数に適切な型注釈を付与
- [ ] Optional型とUnion型の正確な使用
- [ ] 戻り値型の明確な定義
- [ ] ジェネリック型の適切な使用

### 非機能要件
- [ ] PEP 484、PEP 526準拠
- [ ] mypy strict mode対応
- [ ] IDEでの型ヒント完全動作
- [ ] 後方互換性の維持

### 制約事項
- Python 3.13新機能の活用
- 既存APIシグネチャの最小変更
- パフォーマンスへの影響なし

## 実装計画

### 対象ファイル一覧

#### 高優先度（Critical/Highエラー含む）
- `tradingagents/dataflows/utils.py`
- `tradingagents/dataflows/reddit_utils.py`
- `tradingagents/dataflows/yfin_utils.py`
- `tradingagents/agents/utils/memory.py`

#### 中優先度（関数定義の標準化）
- `tradingagents/graph/signal_processing.py`
- `tradingagents/graph/reflection.py`
- `cli/utils.py`

### 修正方針

1. **型注釈標準の確立**
   ```python
   from typing import Optional, Union, List, Dict, Any, TypeVar, Generic
   
   # 標準パターン
   def process_data(
       data: Union[str, Dict[str, Any]], 
       config: Optional[Dict[str, Any]] = None,
       validate: bool = True
   ) -> Optional[List[Dict[str, Any]]]:
   ```

2. **Optional型の明示化**
   ```python
   # Before
   def save_output(data: str, save_path: str = None):
   
   # After
   def save_output(data: str, save_path: Optional[str] = None) -> bool:
   ```

3. **戻り値型の明確化**
   ```python
   # Before
   def get_stock_data(ticker):  # 型情報なし
   
   # After
   def get_stock_data(self, ticker: str) -> Optional[pd.DataFrame]:
   ```

### 見積もり工数
- 標準設計: 0.5日
- 実装: 2日
- 検証・テスト: 1日
- ドキュメント: 0.5日
- **合計: 4日**

## 受け入れ条件

- [ ] 関数型注釈関連エラー35件が全て解消される
- [ ] 全関数が統一された型注釈標準に準拠する
- [ ] mypyのstrict mode で型チェック通過する
- [ ] 既存テストが全て通過する
- [ ] 型注釈標準ドキュメントが作成される

## Todoリスト

### Phase 1: 標準化設計
- [ ] 型注釈標準の策定
- [ ] 共通型定義の設計 (TypeAlias使用)
- [ ] プロジェクト固有型の定義
- [ ] 命名規則の統一

### Phase 2: 基盤型定義
- [ ] 共通型定義ファイルの作成
- [ ] プロジェクト固有TypeAliasの定義
- [ ] ジェネリック型の基盤クラス作成
- [ ] 型チェック用ユーティリティの実装

### Phase 3: Criticalエラー修正
- [ ] yfin_utils.py のself引数エラー修正 (8箇所)
- [ ] memory.py のコンストラクタ引数エラー修正
- [ ] utils.py のOptional引数エラー修正
- [ ] reddit_utils.py のOptional引数エラー修正

### Phase 4: 戻り値型の統一
- [ ] signal_processing.py の戻り値型修正
- [ ] reflection.py の戻り値型修正
- [ ] interface.py の戻り値型統一
- [ ] データ処理関数の型統一

### Phase 5: 全体統一
- [ ] 全モジュールの型注釈レビュー
- [ ] 一貫性のチェックと修正
- [ ] 型エイリアスの適用
- [ ] ドキュメント文字列の型情報更新

### Phase 6: 検証とテスト
- [ ] mypyの厳密モードでの型チェック
- [ ] 型注釈専用テストケース作成
- [ ] IDEでの型ヒント動作確認
- [ ] パフォーマンス影響の測定

### Phase 7: ドキュメント整備
- [ ] 型注釈標準ドキュメント作成
- [ ] 開発者向けガイドライン作成
- [ ] 型定義リファレンス作成
- [ ] ベストプラクティス集作成

## 依存関係

### 前提条件
- なし（独立実装可能）

### 影響を与えるチケット
- **001_date_type_safety.md**: 日付関連の型定義標準
- **002_langchain_message_types.md**: メッセージ型の標準
- **004_yfinance_wrapper.md**: YFinance関連の型定義

### 後続チケット
- **007_dataflow_types.md**: データフロー型安全性
- **009_testing_strategy.md**: 型チェックテスト戦略

## 優先度: Medium

### 根拠
- プロジェクト全体の型安全性基盤
- 他チケットの実装品質に影響
- 開発効率と保守性の向上
- エラー件数は中程度だが影響範囲が広い

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 既存API互換性問題 | 中 | 低 | 段階的適用と互換性テスト |
| 開発者の学習コスト | 低 | 高 | ガイドラインとサンプル提供 |
| 型定義の複雑化 | 中 | 中 | シンプルで分かりやすい標準 |
| パフォーマンス影響 | 低 | 低 | 実行時オーバーヘッドなし |

## 技術標準

### 基本型注釈パターン

```python
from typing import Optional, Union, List, Dict, Any, TypeVar, Protocol
from collections.abc import Callable
from datetime import datetime

# プリミティブ型
def process_string(text: str) -> str:
    pass

# Optional型（None許可）
def save_data(data: str, path: Optional[str] = None) -> bool:
    pass

# Union型（複数型許可）  
def parse_date(date: Union[str, datetime]) -> datetime:
    pass

# コレクション型
def get_items() -> List[Dict[str, Any]]:
    pass

# 関数型
def apply_transform(data: List[str], func: Callable[[str], str]) -> List[str]:
    pass

# ジェネリック型
T = TypeVar('T')
def first_item(items: List[T]) -> Optional[T]:
    pass
```

### 型エイリアス定義

```python
# プロジェクト固有型
DateLike = Union[str, datetime]
ConfigDict = Dict[str, Any]  
DataPoint = Dict[str, Union[str, float, int]]
MessageList = List[BaseMessage]

# 使用例
def process_market_data(
    ticker: str,
    start_date: DateLike,
    config: Optional[ConfigDict] = None
) -> List[DataPoint]:
    pass
```