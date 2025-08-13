# チケット001: 日付処理の型安全性

## 概要
日付処理において、datetime型とstr型が混在して使用されており、型エラーの主要な原因となっている。このチケットでは、日付処理の型安全性を確保する。

## 現状分析

### エラー件数
- **総エラー数**: 20件
- **影響ファイル数**: 5ファイル

### 主要な問題パターン
1. datetime型の変数にstr型を代入
2. str型の変数でstrftimeメソッドを呼び出し
3. 日付演算での型不一致

### 影響ファイル
- `tradingagents/dataflows/interface.py`
- `tradingagents/dataflows/yfin_utils.py`
- `tradingagents/dataflows/stockstats_utils.py`
- `tradingagents/dataflows/reddit_utils.py`
- `tradingagents/dataflows/googlenews_utils.py`

## 要件定義

### 機能要件
- FR-001: 日付型の一貫した使用
- FR-002: 型安全な日付変換ユーティリティの実装
- FR-003: 日付フォーマットの標準化

### 非機能要件
- NFR-001: 既存APIの後方互換性維持
- NFR-002: パフォーマンスの劣化なし
- NFR-003: 明確なエラーメッセージ

### 制約事項
- 外部APIの日付フォーマット要件に準拠
- pandas.Timestampとの互換性維持

## 実装計画

### 対象ファイルと修正内容

#### 1. `tradingagents/dataflows/interface.py`
```python
# 修正前
start_date = datetime.strptime(start_date, "%Y-%m-%d")
before = start_date - relativedelta(days=look_back_days)

# 修正後
from datetime import datetime
from typing import Union

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date_obj: datetime) -> str:
    return date_obj.strftime("%Y-%m-%d")

start_date_obj = parse_date(start_date)
before_obj = start_date_obj - relativedelta(days=look_back_days)
before_str = format_date(before_obj)
```

#### 2. 共通ユーティリティの作成
`tradingagents/utils/date_utils.py`を新規作成

### 見積もり工数
- 分析: 0.5日
- 実装: 2日
- テスト: 0.5日
- **合計: 3日**

## 受け入れ条件

### 必須条件
- [ ] 日付関連の型エラーが0件
- [ ] 全ての日付処理関数に型注釈が追加されている
- [ ] 既存のテストが全てパス

### 推奨条件
- [ ] 日付ユーティリティのユニットテスト追加
- [ ] ドキュメントの更新

## Todoリスト

### 準備作業
- [ ] 影響範囲の最終確認
- [ ] テストケースの洗い出し
- [ ] 日付フォーマットの仕様確認

### 実装作業
- [ ] date_utils.pyの作成
  - [ ] parse_date関数の実装
  - [ ] format_date関数の実装
  - [ ] date_range関数の実装
  - [ ] 型注釈の追加
- [ ] interface.pyの修正
  - [ ] get_reddit_global_news関数の修正
  - [ ] get_finnhub_data関数の修正
  - [ ] 型注釈の追加
- [ ] yfin_utils.pyの修正
  - [ ] get_stock_data関数の修正
  - [ ] 日付処理の統一
- [ ] stockstats_utils.pyの修正
  - [ ] get_stock_stats関数の修正
  - [ ] 日付型の一貫性確保
- [ ] reddit_utils.pyの修正
  - [ ] fetch_top_from_category関数の修正
- [ ] googlenews_utils.pyの修正
  - [ ] get_google_news関数の修正

### テスト作業
- [ ] ユニットテストの作成
  - [ ] date_utilsのテスト
  - [ ] 各修正関数のテスト
- [ ] 統合テストの実行
- [ ] 型チェックの実行（mypy）

### ドキュメント
- [ ] 日付処理ガイドラインの作成
- [ ] APIドキュメントの更新
- [ ] CHANGELOG.mdの更新

## 依存関係
- なし（独立して実装可能）

## 優先度
**Critical** - システム全体で使用される基本機能

## リスクと対策

### リスク1: 既存コードの破壊的変更
**対策**: 
- 段階的な移行
- 互換性レイヤーの提供
- 十分なテスト

### リスク2: 外部APIとの不整合
**対策**:
- APIドキュメントの確認
- エッジケースのテスト
- エラーハンドリングの強化

## 参考情報

### Python日付処理のベストプラクティス
```python
from datetime import datetime
from typing import Union, Optional

DateType = Union[str, datetime]

def ensure_datetime(date: DateType) -> datetime:
    if isinstance(date, str):
        return datetime.strptime(date, "%Y-%m-%d")
    return date

def ensure_string(date: DateType) -> str:
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    return date
```

## 完了確認
- [ ] 全てのTodoが完了
- [ ] 型チェックがパス
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了