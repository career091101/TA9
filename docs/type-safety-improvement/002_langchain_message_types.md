# チケット002: LangChainメッセージ型の安全な処理

## 概要
LangChainのメッセージ型において、tool_calls属性への安全でないアクセスが多数存在し、Union型のエラーが発生している。型ガードを実装して安全性を確保する。

## 現状分析

### エラー件数
- **総エラー数**: 32件
- **影響ファイル数**: 3ファイル
- **エラータイプ**: `[union-attr]`

### 主要な問題パターン
```python
# 問題: 全てのメッセージ型にtool_callsが存在すると仮定
if last_message.tool_calls:  # エラー: 一部の型にはtool_calls属性がない
```

### 影響ファイル
- `tradingagents/graph/conditional_logic.py`
- `tradingagents/graph/propagation.py`
- `tradingagents/graph/setup.py`

## 要件定義

### 機能要件
- FR-001: メッセージ型の安全な判定
- FR-002: 型ガード関数の実装
- FR-003: 属性アクセスの安全性確保

### 非機能要件
- NFR-001: ランタイムオーバーヘッドの最小化
- NFR-002: 可読性の維持
- NFR-003: LangChainのバージョンアップへの対応

### 制約事項
- LangChain APIの仕様に準拠
- 既存のメッセージフローを変更しない

## 実装計画

### 実装方針

#### 1. 型ガードユーティリティの作成
```python
# tradingagents/utils/message_utils.py
from typing import TypeGuard
from langchain_core.messages import AIMessage, BaseMessage

def has_tool_calls(message: BaseMessage) -> TypeGuard[AIMessage]:
    """メッセージがtool_calls属性を持つか判定"""
    return isinstance(message, AIMessage) and hasattr(message, 'tool_calls')

def get_tool_calls_safely(message: BaseMessage):
    """安全にtool_callsを取得"""
    if has_tool_calls(message):
        return message.tool_calls
    return None
```

#### 2. conditional_logic.pyの修正
```python
# 修正前
if last_message.tool_calls:

# 修正後
from tradingagents.utils.message_utils import has_tool_calls

if has_tool_calls(last_message) and last_message.tool_calls:
```

### 見積もり工数
- 分析: 0.5日
- 実装: 2.5日
- テスト: 1日
- **合計: 4日**

## 受け入れ条件

### 必須条件
- [ ] メッセージ型関連のunion-attrエラーが0件
- [ ] 全ての条件分岐で型ガードを使用
- [ ] 既存の動作が変更されていない

### 推奨条件
- [ ] メッセージ処理のベストプラクティス文書
- [ ] パフォーマンステストの実施

## Todoリスト

### 準備作業
- [ ] LangChainメッセージ型の仕様確認
- [ ] 影響箇所の詳細調査
- [ ] テストシナリオの作成

### 実装作業

#### message_utils.pyの作成
- [ ] 型ガード関数の実装
  - [ ] has_tool_calls関数
  - [ ] has_content関数
  - [ ] is_ai_message関数
  - [ ] is_human_message関数
- [ ] 安全なアクセサ関数
  - [ ] get_tool_calls_safely
  - [ ] get_content_safely
  - [ ] get_message_type
- [ ] 型注釈の完備

#### conditional_logic.pyの修正
- [ ] should_continue_market関数
  - [ ] 型ガードの適用
  - [ ] エラーハンドリング追加
- [ ] should_continue_fundamentals関数
  - [ ] 型ガードの適用
- [ ] should_continue_social関数
  - [ ] 型ガードの適用
- [ ] should_continue_news関数
  - [ ] 型ガードの適用
- [ ] その他の条件分岐関数
  - [ ] 全関数の型安全性確保

#### propagation.pyの修正
- [ ] メッセージ処理部分の型安全化
- [ ] エラーハンドリングの追加

#### setup.pyの修正
- [ ] グラフセットアップ時の型チェック
- [ ] メッセージフローの型安全性確保

### テスト作業
- [ ] ユニットテストの作成
  - [ ] message_utilsのテスト
  - [ ] 各型ガード関数のテスト
  - [ ] エッジケースのテスト
- [ ] 統合テストの実行
  - [ ] メッセージフローのテスト
  - [ ] 条件分岐のテスト
- [ ] 型チェックの実行

### ドキュメント
- [ ] メッセージ型処理ガイドライン
- [ ] 型ガード使用例の文書化
- [ ] トラブルシューティングガイド

## 依存関係
- チケット006（エージェント状態の型定義）と関連あり
- 並行実装可能

## 優先度
**Critical** - エージェント間通信の中核機能

## リスクと対策

### リスク1: LangChainバージョンアップでの破壊的変更
**対策**:
- バージョン固定
- 抽象化レイヤーの実装
- 定期的な互換性テスト

### リスク2: パフォーマンスへの影響
**対策**:
- 型ガードの最適化
- キャッシュの活用
- プロファイリング実施

### リスク3: 複雑性の増加
**対策**:
- シンプルなAPIの提供
- 明確なドキュメント
- コード例の充実

## 参考情報

### LangChainメッセージ型の階層
```
BaseMessage
├── AIMessage (tool_calls属性あり)
├── HumanMessage
├── SystemMessage
├── FunctionMessage
├── ToolMessage
└── ChatMessage
```

### 型ガードのベストプラクティス
```python
from typing import TypeGuard, Union

def is_specific_type(obj: Union[TypeA, TypeB]) -> TypeGuard[TypeA]:
    return isinstance(obj, TypeA)

# 使用例
if is_specific_type(message):
    # ここではmessageはTypeA型として扱われる
    message.specific_method()
```

## 完了確認
- [ ] 全てのTodoが完了
- [ ] 型エラーが解消
- [ ] コードレビュー完了
- [ ] テストが全てパス
- [ ] ドキュメント更新完了