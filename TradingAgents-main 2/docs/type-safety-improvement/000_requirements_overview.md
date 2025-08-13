# TradingAgents 型エラー改修要件定義書

## 1. プロジェクト概要

### 背景
TradingAgentsは多エージェントLLM金融取引フレームワークですが、現在180件の型エラーが検出されており、型安全性の向上が急務となっています。これらのエラーは保守性、可読性、および実行時エラーの予防に影響を与えています。

### 目的
- 型安全性の確保による実行時エラーの削減
- コードの保守性と可読性の向上
- 開発効率の向上（IDEの型ヒント機能の活用）
- CI/CDパイプラインでの型チェック自動化

## 2. 現状分析

### 型エラー分布 (総数: 180件)

| エラーカテゴリ | 件数 | 重要度 | 説明 |
|--------------|------|--------|------|
| union-attr | 44 | High | Union型に対する属性アクセスエラー |
| attr-defined | 24 | High | 未定義属性へのアクセス |
| assignment | 22 | Critical | 型不一致の代入エラー |
| arg-type | 16 | High | 関数引数の型不一致 |
| misc | 13 | Medium | その他の型関連エラー |
| operator | 10 | Medium | 演算子の型エラー |
| name-defined | 7 | Critical | 未定義変数の参照 |
| import-untyped | 6 | Low | 型情報のないライブラリ |
| call-arg | 3 | High | 関数呼び出し引数エラー |
| return-value | 2 | High | 戻り値の型不一致 |

### 問題のある主要モジュール

1. **dataflows/interface.py**: 日付処理の型不一致 (32件)
2. **graph/conditional_logic.py**: LangChainメッセージ型の処理 (40件)
3. **dataflows/yfin_utils.py**: YFinanceラッパーの型問題 (21件)
4. **agents/utils/agent_states.py**: 循環参照による型定義エラー (7件)
5. **cli/utils.py**: 未定義変数参照 (7件)

## 3. 技術要件

### 機能要件
- 全ての型エラーの解決
- 型ヒントの完全性確保
- 型安全なAPIインターフェースの提供

### 非機能要件
- 既存機能への影響なし
- パフォーマンスの劣化なし
- 後方互換性の維持
- テストカバレッジの維持

### 技術制約
- Python 3.13対応
- mypy 1.0+での型チェック通過
- 既存の依存関係の維持
- LangChain、YFinance、Pandasとの互換性

## 4. 改修戦略

### Phase 1: Critical Issues (優先度: Critical)
- 未定義変数参照の修正
- 型不一致の代入エラー修正
- 循環参照の解決

### Phase 2: High Priority (優先度: High)
- LangChainメッセージ型の安全な処理
- 日付処理の型安全性確保
- YFinanceラッパーの型定義修正

### Phase 3: Medium Priority (優先度: Medium)
- Union型の安全な処理
- 演算子の型エラー修正
- 設定管理の型安全性

### Phase 4: Low Priority (優先度: Low)
- 外部ライブラリの型スタブ追加
- 型定義の最適化

## 5. 成功指標

### 量的指標
- 型エラー数: 180件 → 0件
- 型カバレッジ: 現在不明 → 95%以上
- CI/CD成功率: 型チェックでのビルド失敗0件

### 質的指標
- IDEでの型ヒント機能の完全動作
- 新規開発時の型関連バグ削減
- コードレビュー効率の向上

## 6. プロジェクト管理

### タイムライン
- Phase 1: 2-3日
- Phase 2: 4-5日  
- Phase 3: 2-3日
- Phase 4: 1-2日
- 合計: 9-13日

### リソース
- 開発者: 1名
- レビュー担当: 1名
- QA: 既存テストスイート活用

### リスク管理
- 既存機能への影響: 段階的改修とテスト実行
- 依存関係の変更: 最小限の変更に留める
- パフォーマンス劣化: ベンチマークテストの実行

## 7. チケット構成

以下の10個のチケットに分割して実装を行います：

1. **001_date_type_safety.md** - 日付処理の型安全性 (Critical)
2. **002_langchain_message_types.md** - LangChainメッセージ型 (High)  
3. **003_function_annotations.md** - 関数の型注釈 (Medium)
4. **004_yfinance_wrapper.md** - YFinanceラッパー (High)
5. **005_config_type_safety.md** - 設定の型安全性 (Critical)
6. **006_agent_state_types.md** - エージェント状態の型定義 (Critical)
7. **007_dataflow_types.md** - データフローの型安全性 (High)
8. **008_memory_types.md** - メモリシステムの型定義 (Medium)
9. **009_testing_strategy.md** - 型チェックテスト戦略 (Medium)
10. **010_ci_cd_integration.md** - CI/CD統合計画 (Low)

各チケットは独立して実装可能で、依存関係は最小限に抑制されています。