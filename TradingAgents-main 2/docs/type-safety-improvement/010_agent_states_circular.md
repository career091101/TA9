# agent_states.pyの循環定義問題改修

## 概要

tradingagents/agents/utils/agent_states.pyにおける循環定義問題を解決する。TypedDict定義において循環参照が発生し、5件のmiscエラーが発生している。これらのエラーはエージェント間の状態管理の根幹に関わるため、システム全体の安定性に影響する重要な課題である。

## 現状分析

### エラー内容と件数（5件）

1. **循環定義エラー** - 5箇所
   - `tradingagents/agents/utils/agent_states.py`: Cannot resolve TypedDict item (possible cyclic definition)
   - `tradingagents/agents/utils/agent_states.py:5`: Cannot resolve name "InvestDebateState"
   - `tradingagents/agents/utils/agent_states.py:5`: Cannot resolve name "RiskDebateState"
   - `tradingagents/agents/utils/agent_states.py:65`: Cannot resolve name "InvestDebateState"
   - `tradingagents/agents/utils/agent_states.py:73`: Cannot resolve name "RiskDebateState"

### 関連エラー（4件）

2. **import関連エラー** - 4箇所
   - `tradingagents/agents/__init__.py:2`: Module has no attribute "InvestDebateState"
   - `tradingagents/agents/__init__.py:2`: Module has no attribute "RiskDebateState"
   - `tradingagents/graph/propagation.py:4`: Module has no attribute "InvestDebateState"
   - `tradingagents/graph/propagation.py:4`: Module has no attribute "RiskDebateState"
   - `tradingagents/graph/trading_graph.py:19`: 同様のエラー2件

### 根本原因

- TypedDict定義で相互参照が発生している
- Forward referenceの不適切な使用
- 型定義の依存関係が複雑になっている

## 要件定義

### 機能要件

1. **循環定義の解消**
   - InvestDebateStateとRiskDebateStateの循環参照解消
   - Forward referenceの適切な実装
   - 型定義の階層構造の再設計

2. **型安全性の確保**
   - 全てのTypedDictが適切に解決される
   - importエラーの解消
   - 型チェックの完全通過

3. **状態管理の整合性**
   - エージェント状態間の依存関係の明確化
   - 状態遷移の型安全性確保
   - デバッグ情報の適切な型定義

### 非機能要件

1. **互換性の保持**
   - 既存のエージェント実装に影響を与えない
   - 状態管理APIの変更を最小限に抑制

2. **保守性**
   - 型定義の可読性向上
   - 新しい状態追加時の拡張性確保

3. **パフォーマンス**
   - 型チェック時間の短縮
   - ランタイムオーバーヘッドの最小化

## 実装計画

### Phase 1: 現状分析と設計（2時間）

1. 循環参照の詳細分析
2. 依存関係グラフの作成
3. 新しい型定義構造の設計

### Phase 2: 型定義の再構築（4時間）

1. 基本状態の定義（AgentState）
2. 専門状態の定義（InvestDebateState, RiskDebateState）
3. Forward referenceの適切な実装
4. Union型の活用による型安全性確保

### Phase 3: インポート・使用箇所の修正（2時間）

1. __init__.pyの修正
2. propagation.pyの修正
3. trading_graph.pyの修正
4. その他関連ファイルの修正

### Phase 4: テストと検証（2時間）

1. 型チェックの実行
2. エージェント動作の確認
3. 状態遷移のテスト

**総見積もり時間: 10時間**

## Todoリスト

- [ ] agent_states.pyの現状コードレビュー
- [ ] 循環参照箇所の特定と分析
- [ ] 依存関係グラフの作成
- [ ] 新しい型定義構造の設計
- [ ] AgentState基本型の定義
- [ ] InvestDebateStateの再定義
- [ ] RiskDebateStateの再定義
- [ ] Forward referenceの実装
- [ ] __init__.pyのimport修正
- [ ] propagation.pyの型参照修正
- [ ] trading_graph.pyの型参照修正
- [ ] その他関連ファイルの修正
- [ ] 型チェック（mypy）の実行
- [ ] エージェント動作テスト
- [ ] 状態遷移テスト
- [ ] パフォーマンステスト
- [ ] コードレビューとドキュメント更新

## 受け入れ条件

1. **循環定義エラーの完全解消**
   - agent_states.py関連の全5件のmiscエラーが解消される
   - 全てのTypedDictが適切に解決される

2. **インポートエラーの解消**
   - 関連する4件のattr-definedエラーが解消される
   - 全ての状態型が適切にインポートされる

3. **型チェックの完全通過**
   - mypy --strict でエラーが発生しない
   - 全ての型アノテーションが正しく解決される

4. **機能の正常動作**
   - エージェント間の状態遷移が正常に動作する
   - デバッグ情報が適切に記録される
   - 既存のワークフローが影響を受けない

5. **コード品質**
   - 型定義の可読性が向上する
   - 新しい状態の追加が容易になる
   - ドキュメントが更新される

## 依存関係

### 前提条件
- 009_interface_union_types.md: データフロー層の型安定化（推奨、必須ではない）

### 後続タスクへの影響
- 011_cli_variable_definitions.md: 状態型の安定化により、CLI層での状態処理も安定する
- 013_agent_function_annotations.md: エージェント関数の型注釈で安定した状態型を使用可能

### 関連ファイル
- tradingagents/agents/utils/memory.py
- tradingagents/graph/conditional_logic.py
- tradingagents/graph/setup.py
- cli/models.py

## 完了確認

- [ ] 全てのTodoが完了
- [ ] 循環定義エラー5件が解消
- [ ] インポートエラー4件が解消
- [ ] mypy型チェックが全てパス
- [ ] エージェント動作テストが全てパス
- [ ] 状態遷移テストが全てパス
- [ ] パフォーマンステストが完了
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了