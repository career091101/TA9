# チケット001: 日付処理の型安全性改修

## 概要

TradingAgentsプロジェクトにおいて、日付・時刻処理に関する型エラーが32件検出されています。主にdatetime型とstr型の混在、pandas.Timestampとstrの型不一致が原因です。これらのエラーを解決し、日付処理の型安全性を確保します。

## 現状分析

### 影響範囲
- **dataflows/interface.py**: 27件のエラー
- **dataflows/yfin_utils.py**: 3件のエラー  
- **dataflows/stockstats_utils.py**: 2件のエラー

### 主要なエラーパターン

1. **datetime vs str の型不一致**
   ```python
   # エラー例
   analysis_date: datetime = "2024-01-01"  # [assignment] error
   ```

2. **Timestamp属性へのstr型でのアクセス**
   ```python
   # エラー例
   date_str.strftime("%Y-%m-%d")  # [attr-defined] error
   ```

3. **relativedelta演算での型不一致**
   ```python
   # エラー例
   str_date - relativedelta(days=30)  # [operator] error
   ```

## 要件定義

### 機能要件
- [ ] 全ての日付パラメータに正しい型注釈を付与
- [ ] 日付文字列とdatetimeオブジェクトの明確な区別
- [ ] 日付変換処理の型安全性確保
- [ ] pandas.Timestampとdatetimeの適切な変換

### 非機能要件
- [ ] 既存のAPI署名を可能な限り維持
- [ ] パフォーマンスへの影響を最小化
- [ ] 日付処理ロジックの動作保持

### 制約事項
- datetime、pandas、dateutil.relativedelta依存関係の維持
- ISO8601フォーマット文字列との互換性
- タイムゾーン処理の考慮

## 実装計画

### 対象ファイル一覧
- `tradingagents/dataflows/interface.py`
- `tradingagents/dataflows/yfin_utils.py`
- `tradingagents/dataflows/stockstats_utils.py`
- `tradingagents/dataflows/utils.py`

### 修正方針

1. **型注釈の修正**
   ```python
   # Before
   def get_data(date: str, end_date: str):
   
   # After  
   def get_data(date: Union[str, datetime], end_date: Union[str, datetime]):
   ```

2. **日付変換ユーティリティの作成**
   ```python
   def ensure_datetime(date: Union[str, datetime]) -> datetime:
       if isinstance(date, str):
           return datetime.fromisoformat(date)
       return date
   ```

3. **pandasとの統合改善**
   ```python
   def timestamp_to_str(ts: pd.Timestamp) -> str:
       return ts.strftime("%Y-%m-%d") if hasattr(ts, 'strftime') else str(ts)
   ```

### 見積もり工数
- 調査・設計: 0.5日
- 実装: 1.5日
- テスト・検証: 1日
- **合計: 3日**

## 受け入れ条件

- [ ] 日付関連の型エラー32件が全て解消される
- [ ] mypyで該当ファイルの型チェックが通過する
- [ ] 既存テストが全て通過する
- [ ] 新規の型安全性テストが追加される
- [ ] パフォーマンスが5%以上劣化しない

## Todoリスト

### Phase 1: 分析と設計
- [ ] 各ファイルの日付処理パターンを詳細分析
- [ ] 共通の型定義とユーティリティ関数を設計
- [ ] 既存のテストケースを確認

### Phase 2: 基盤整備
- [ ] 日付処理用の型定義を作成 (Union[str, datetime])
- [ ] 日付変換ユーティリティ関数を実装
- [ ] pandas Timestamp対応の処理を実装

### Phase 3: interface.py の修正
- [ ] get_finnhub_news関数の日付型修正
- [ ] get_reddit_global_news関数の日付演算修正
- [ ] get_reddit_company_news関数の日付演算修正
- [ ] get_stock_stats_indicators_window関数の日付処理修正
- [ ] get_stockstats_indicator関数の日付処理修正
- [ ] その他21件の日付関連エラー修正

### Phase 4: その他ファイルの修正
- [ ] yfin_utils.pyのTimestamp型エラー修正
- [ ] stockstats_utils.pyの日付変換エラー修正  
- [ ] utils.pyのOptional型引数修正

### Phase 5: テストと検証
- [ ] 型チェック用テストケース追加
- [ ] 既存テストの実行と修正
- [ ] パフォーマンステストの実行
- [ ] エッジケース（無効な日付形式など）のテスト追加

### Phase 6: ドキュメント整備
- [ ] 日付処理のガイドライン作成
- [ ] APIドキュメントの更新
- [ ] 型注釈の仕様書更新

## 依存関係

### 前提条件
- なし（このチケットは独立して実装可能）

### 影響を与えるチケット
- **003_function_annotations.md**: 関数型注釈の統一基準
- **007_dataflow_types.md**: データフロー全体の型安全性

### 後続チケット
- **009_testing_strategy.md**: 型チェックテストの統合

## 優先度: Critical

### 根拠
- データフロー処理の中核機能に影響
- 32件と最多のエラー数
- 実行時エラーの可能性が高い
- 他のモジュールからの依存度が高い

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 既存データ処理の破綻 | 高 | 中 | 段階的実装とテスト強化 |
| パフォーマンス劣化 | 中 | 低 | 最適化されたユーティリティ関数 |
| 外部API互換性問題 | 中 | 低 | 既存形式の並行サポート |
| タイムゾーン処理の複雑化 | 低 | 中 | 明確な仕様定義 |