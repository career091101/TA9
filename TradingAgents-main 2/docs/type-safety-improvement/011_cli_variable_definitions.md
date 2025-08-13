# CLI層の変数定義問題改修

## 概要

cli/utils.pyおよび関連CLI層における変数定義問題を解決する。主に未定義変数（console）の使用と、関数の重複定義により、合計9件のエラーが発生している。CLI層はユーザーインターフェースの根幹であり、これらのエラーはユーザー体験に直接影響する。

## 現状分析

### エラー内容と件数（9件）

1. **未定義変数エラー** - 7箇所
   - `cli/utils.py:28`: Name "console" is not defined
   - `cli/utils.py:61`: Name "console" is not defined
   - `cli/utils.py:87`: Name "console" is not defined
   - `cli/utils.py:119`: Name "console" is not defined
   - `cli/utils.py:175`: Name "console" is not defined
   - `cli/utils.py:237`: Name "console" is not defined
   - `cli/utils.py:270`: Name "console" is not defined

2. **関数重複定義エラー** - 2箇所
   - `cli/main.py:496`: Name "get_ticker" already defined
   - `cli/main.py:501`: Name "get_analysis_date" already defined

### 根本原因

- Rich Consoleオブジェクトのimportまたは初期化が不完全
- 関数名の衝突（import文と関数定義の競合）
- モジュール間のimport管理の不整合

## 要件定義

### 機能要件

1. **Console変数の適切な定義**
   - Rich Consoleオブジェクトの適切なimportと初期化
   - 全てのconsole使用箇所での一貫した動作
   - エラーハンドリングの実装

2. **関数名競合の解消**
   - 重複定義関数の名前空間分離
   - import文と関数定義の競合解消
   - 適切な関数スコープの設定

3. **型安全なCLI実装**
   - 変数の型ヒント追加
   - 関数の戻り値型定義
   - 入力検証の強化

### 非機能要件

1. **ユーザー体験の維持**
   - 既存のCLI動作を変更しない
   - レスポンス時間の悪化を避ける
   - エラーメッセージの改善

2. **保守性**
   - コードの可読性向上
   - デバッグ情報の充実
   - テストしやすい構造への変更

3. **互換性**
   - 他のCLIツールとの競合回避
   - 依存ライブラリバージョンの互換性確保

## 実装計画

### Phase 1: Console変数の修正（2時間）

1. Rich Consoleの適切なimport
2. グローバルconsole変数の初期化
3. 使用箇所での動作確認

### Phase 2: 関数重複の解消（2時間）

1. 重複関数の名前空間分析
2. import文の整理
3. 関数名の変更または削除

### Phase 3: 型安全性の強化（3時間）

1. 変数の型ヒント追加
2. 関数の型注釈追加
3. 入力検証の実装

### Phase 4: テストと統合（1時間）

1. CLI動作テスト
2. 型チェックの実行
3. ユーザーインターフェースの確認

**総見積もり時間: 8時間**

## Todoリスト

- [ ] cli/utils.pyの現状コードレビュー
- [ ] Rich Consoleの使用パターン調査
- [ ] console変数の適切な定義と初期化
- [ ] cli/utils.pyの7箇所のconsole使用箇所修正
- [ ] cli/main.pyの関数重複分析
- [ ] get_ticker関数の重複解消
- [ ] get_analysis_date関数の重複解消
- [ ] import文の整理と最適化
- [ ] 変数・関数の型ヒント追加
- [ ] 入力検証ロジックの実装
- [ ] エラーハンドリングの強化
- [ ] CLI動作テスト（対話モード）
- [ ] CLI動作テスト（非対話モード）
- [ ] 型チェック（mypy）の実行
- [ ] パフォーマンステスト
- [ ] ユーザビリティテスト
- [ ] コードレビューとリファクタリング

## 受け入れ条件

1. **変数定義エラーの完全解消**
   - cli/utils.py関連の7件の未定義変数エラーが解消される
   - console変数が全ての使用箇所で正常に動作する

2. **関数重複エラーの解消**
   - cli/main.pyの2件の重複定義エラーが解消される
   - 全ての関数が適切な名前空間で定義される

3. **CLI機能の正常動作**
   - 対話モードが正常に動作する
   - 非対話モードが正常に動作する
   - Rich UIコンポーネントが適切に表示される

4. **型チェックの完全通過**
   - mypy --strict でエラーが発生しない
   - 全ての変数・関数に適切な型注釈が付与される

5. **ユーザー体験の維持**
   - 既存のCLI操作方法が変更されない
   - エラーメッセージが改善される
   - レスポンス時間が悪化しない

## 依存関係

### 前提条件
- 010_agent_states_circular.md: 状態型の安定化により、CLI層での状態表示も安定する（推奨）

### 後続タスクへの影響
- 013_agent_function_annotations.md: CLI層の型安全化により、エージェント関数の型定義も明確になる

### 関連ファイル
- cli/models.py
- cli/main.py
- tradingagents/utils/message_utils.py（CLI表示用）

### 外部依存関係
- Rich library (≥13.0.0)
- Questionary library (≥2.1.0)

## 完了確認

- [ ] 全てのTodoが完了
- [ ] console未定義エラー7件が解消
- [ ] 関数重複エラー2件が解消
- [ ] mypy型チェックが全てパス
- [ ] CLI対話モードテストが全てパス
- [ ] CLI非対話モードテストが全てパス
- [ ] Rich UIコンポーネントテストが全てパス
- [ ] パフォーマンステストが完了
- [ ] ユーザビリティテストが完了
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了