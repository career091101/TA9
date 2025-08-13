# CLAUDE.md

このファイルは、このリポジトリのコードを扱う際のClaude Code (claude.ai/code) へのガイダンスを提供します。

## プロジェクト概要

TradingAgentsは、実世界のトレーディング会社のダイナミクスをシミュレートする、マルチエージェントLLM駆動の金融取引フレームワークです。このフレームワークは、市場状況を評価し取引決定を行うために協力する専門エージェント（アナリスト、リサーチャー、トレーダー、リスクマネージャー）を使用します。

## 必須コマンド

### インストール
```bash
# 仮想環境の作成
conda create -n tradingagents python=3.13
conda activate tradingagents

# 依存関係のインストール
pip install -r requirements.txt
```

### アプリケーションの実行
```bash
# CLIインターフェース（対話モード）
python -m cli.main

# カスタム設定での直接実行
python main.py
```

### 必要な環境変数
```bash
export FINNHUB_API_KEY=$YOUR_FINNHUB_API_KEY  # 金融データ取得に必要
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY    # LLMエージェントに必要
```

## アーキテクチャ概要

### コアシステムフロー
1. **データ収集**: FinnHub APIまたはキャッシュデータから金融データを取得
2. **分析フェーズ**: 複数のアナリストエージェントが異なるデータ側面を処理:
   - マーケットアナリスト: テクニカル指標（MACD、RSI）
   - ニュースアナリスト: グローバルニュースとマクロ経済指標
   - ソーシャルメディアアナリスト: ソーシャルプラットフォームからのセンチメント分析
   - ファンダメンタルズアナリスト: 企業財務とパフォーマンス指標
3. **リサーチフェーズ**: ブル派とベア派のリサーチャーが洞察を議論
4. **取引決定**: トレーダーエージェントがレポートを統合し決定を下す
5. **リスク管理**: リスクチームが取引を評価し承認/却下

### 主要コンポーネント

**グラフアーキテクチャ** (`tradingagents/graph/`):
- `trading_graph.py`: メインオーケストレータークラス `TradingAgentsGraph`
- `setup.py`: グラフ初期化とエージェントセットアップ
- `propagation.py`: メッセージ伝播ロジック
- `conditional_logic.py`: エージェント間の決定ルーティング
- `reflection.py`: 過去の決定からの学習
- `signal_processing.py`: 取引シグナル処理

**エージェントシステム** (`tradingagents/agents/`):
- 各エージェントタイプはファクトリ関数（`create_*_analyst`）を持つ独自のモジュールを持つ
- エージェントはLangGraphの状態管理を通じて通信
- メモリシステムは取引セッション間でコンテキストを維持

**データレイヤー** (`tradingagents/dataflows/`):
- `interface.py`: メインデータアクセスインターフェース
- プロバイダー固有のユーティリティ: `finnhub_utils.py`, `yfin_utils.py`, `reddit_utils.py`
- `dataflows/data_cache/`でのデータキャッシング

### 設定システム

`tradingagents/default_config.py`で管理される設定:
- LLM設定: `deep_think_llm`, `quick_think_llm`, `llm_provider`
- ディベートラウンド: `max_debate_rounds`, `max_risk_discuss_rounds`
- データ設定: `online_tools` (trueでリアルタイム、falseでキャッシュ)

カスタム設定の例:
```python
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # LLMを変更
config["max_debate_rounds"] = 2           # ディベートラウンドを増やす
config["online_tools"] = True             # リアルタイムデータを使用
```

### CLIインターフェース

CLI (`cli/main.py`)は以下を備えた対話型インターフェースを提供:
- リアルタイムのエージェントステータス表示
- メッセージバッファリングと表示管理
- 進捗追跡機能付きのリッチなターミナルUI
- 複数のティッカーと日付選択のサポート

## 開発ガイドライン

### 新しいエージェントの追加
1. `tradingagents/agents/[category]/`にエージェントモジュールを作成
2. ファクトリ関数 `create_[agent_name]`を実装
3. `__init__.py`のエクスポートに追加
4. `tradingagents/graph/setup.py`のグラフセットアップを更新

### 取引ロジックの変更
- コア決定ロジック: `tradingagents/graph/conditional_logic.py`
- エージェント通信: `agent_states.py`の状態定義を更新
- メモリ永続化: `FinancialSituationMemory`クラスを変更

### データプロバイダー統合
1. `tradingagents/dataflows/`にユーティリティモジュールを追加
2. `interface.py`に登録
3. `online_tools=False`の場合のキャッシングを処理

## 技術仕様

### 技術スタック

**コアフレームワーク**:
- **LangChain (0.3.x)**: エージェントオーケストレーションとプロンプト管理
- **LangGraph (0.4.x)**: 状態管理とエージェント通信グラフ
- **ChromaDB (1.0.x)**: メモリ永続化とセマンティック検索用のベクトルデータベース
- **OpenAI API**: LLM統合（GPT-4、o4-miniモデル）
- **Anthropic/Google Generative AI**: 代替LLMプロバイダー

**データ＆分析**:
- **pandas (2.3.0+)**: データ操作と分析
- **yfinance (0.2.63+)**: Yahoo Finance市場データAPI
- **finnhub-python (2.4.23+)**: プロフェッショナル金融データプロバイダー
- **stockstats (0.6.5+)**: テクニカル指標計算
- **praw (7.8.1+)**: ソーシャルセンチメント用Reddit API
- **feedparser (6.0.11+)**: ニュースフィード処理

**UI＆インフラ**:
- **Rich (14.0.0+)**: 進捗追跡付きターミナルUI
- **Questionary (2.1.0+)**: 対話型CLIプロンプト
- **Redis (6.2.0+)**: キャッシングとセッション管理
- **Chainlit (2.5.5+)**: チャットインターフェース用Web UI

### アーキテクチャパターン

**実装されたデザインパターン**:
1. **ファクトリーパターン**: `create_*`関数によるエージェント作成
2. **ステートマシン**: LangGraphベースの状態遷移
3. **オブザーバーパターン**: エージェント間のメッセージ伝播
4. **ストラテジーパターン**: 設定可能なLLMプロバイダーとデータソース
5. **メモリパターン**: エンベディング付きChromaDBベースのセマンティックメモリ

**状態管理**:
```python
# 3つの主要な状態タイプ:
- AgentState: 一般的なエージェント通信状態
- InvestDebateState: リサーチャーチームのディベート状態
- RiskDebateState: リスク管理チームのディスカッション状態
```

## ベストプラクティス

### コード構成

1. **モジュール構造**:
   - エージェントロジックをファクトリ関数（`create_*_analyst`）に保持
   - 関心事の分離: データフロー、エージェント、グラフロジック
   - クリーンなエクスポートのために`__init__.py`を使用

2. **エージェント開発**:
   ```python
   def create_agent_name(llm, toolkit):
       def agent_node(state):
           # 1. 状態変数を抽出
           # 2. online_toolsフラグに基づいてツールを設定
           # 3. システムメッセージでプロンプトを構築
           # 4. LLMで処理
           # 5. 結果で状態を更新
           return {"messages": [result], "reports": {...}}
       return agent_node
   ```

3. **状態更新**:
   - 常に更新する状態キーを含む辞書を返す
   - 変更しない場合は既存の状態データを保持
   - 状態変数に適切な型アノテーションを使用

### エラーハンドリングと信頼性

1. **API呼び出し管理**:
   ```python
   # 常にonline_toolsフラグをチェック
   if toolkit.config["online_tools"]:
       tools = [online_tool_1, online_tool_2]
   else:
       tools = [cached_tool_1, cached_tool_2]
   ```

2. **例外処理**:
   - 外部API呼び出しをtry-exceptブロックでラップ
   - APIが失敗した場合はキャッシュデータへのフォールバックを提供
   - システムをクラッシュさせずにデバッグ用にエラーをログ記録

3. **データ検証**:
   - 処理前にティッカーシンボルと日付を検証
   - 金融指標の欠損データをチェック
   - エッジケースを処理（市場休日、上場廃止株）

### パフォーマンス最適化

1. **LLMコスト管理**:
   - 開発/テストには`gpt-4o-mini`を使用
   - 繰り返しクエリのためのキャッシングを実装
   - 可能な場合はAPI呼び出しをバッチ処理

2. **メモリ効率**:
   - すべてのメモリをロードする代わりにChromaDBのセマンティック検索を使用
   - `max_debate_rounds`設定でディベートラウンドを制限
   - 大規模データセットのためのページネーションを実装

3. **キャッシング戦略**:
   - 金融データを`dataflows/data_cache/`にローカルキャッシュ
   - セッション管理にRedisを使用
   - 時間依存データのためのTTLを実装

### セキュリティ考慮事項

1. **APIキー管理**:
   - APIキーをハードコードしない
   - 環境変数を排他的に使用
   - 起動時にAPIキーを検証

2. **データ保護**:
   - ユーザー入力をサニタイズ（ティッカーシンボル、日付）
   - 機密金融データのログ記録を避ける
   - API呼び出しのレート制限を実装

3. **メモリセキュリティ**:
   - ChromaDBの機密データを暗号化
   - 使用後にセッションデータをクリア
   - マルチユーザーシナリオのためのアクセス制御を実装

### テストガイドライン

1. **単体テスト**:
   - 各エージェントファクトリ関数を独立してテスト
   - 一貫したテストのために外部API呼び出しをモック
   - 状態変換を検証

2. **統合テスト**:
   - キャッシュデータで完全なグラフ伝播をテスト
   - エージェント通信フローを検証
   - エラー回復メカニズムをテスト

3. **パフォーマンステスト**:
   - API呼び出し回数とコストを監視
   - 各エージェントの応答時間を測定
   - さまざまな市場条件でテスト

### デバッグのヒント

1. **デバッグモードを有効化**:
   ```python
   ta = TradingAgentsGraph(debug=True, config=config)
   ```

2. **エージェント監視**:
   - エージェントの入出力をログ記録
   - 各ノードでの状態変化を追跡
   - メモリ使用量とAPI呼び出しを監視

3. **よくある問題**:
   - APIキーの欠落: 環境変数を確認
   - レート制限: 指数バックオフを実装
   - データの不整合: キャッシュの鮮度を検証

### 設定のベストプラクティス

1. **環境固有の設定**:
   ```python
   # 開発環境
   config["max_debate_rounds"] = 1
   config["online_tools"] = False
   
   # 本番環境
   config["max_debate_rounds"] = 3
   config["online_tools"] = True
   ```

2. **モデル選択**:
   - 開発: `gpt-4o-mini` (コスト効率的)
   - 本番: `o4-mini` または `gpt-4o` (高品質)
   - テスト: 可能な場合はキャッシュされたレスポンスを使用

3. **リソース制限**:
   - API呼び出しに適切なタイムアウトを設定
   - 同時エージェント実行を制限
   - メモリコレクションサイズを設定

## 重要事項

- フレームワークは大量のAPI呼び出しを行う - コスト削減のためテストには`gpt-4o-mini`を使用
- デフォルトモデル: `o4-mini` (深い思考)、`gpt-4o-mini` (素早い思考)
- データキャッシュディレクトリ: `tradingagents/dataflows/data_cache/`
- 結果保存先: `./results/` (`TRADINGAGENTS_RESULTS_DIR`で設定可能)
- 依存関係の競合を避けるため常に仮想環境で実行
- 予期しないコストを避けるためAPI使用量を監視

## タスク管理ガイドライン

### Todoリストの管理

プロジェクト内のドキュメント（特に`/docs/type-safety-improvement/`配下）では、Markdownのチェックボックスを使用してタスク管理を行います。

#### チェックボックスの記法
- **未完了タスク**: `- [ ]` タスク内容
- **完了タスク**: `- [x]` タスク内容

#### 例
```markdown
### 実装タスク
- [x] 要件定義の作成
- [x] 型定義ファイルの作成
- [ ] ユニットテストの実装
- [ ] 統合テストの実行
```

#### タスク完了時の更新手順
1. 該当するマークダウンファイルを開く
2. 完了したタスクの `- [ ]` を `- [x]` に変更
3. 完了日時をコメントで追加（オプション）
   ```markdown
   - [x] 型定義ファイルの作成 <!-- 2025-08-13 完了 -->
   ```

#### 進捗の追跡
各チケットファイルの「完了確認」セクションで全体の進捗を確認できます：
```markdown
## 完了確認
- [x] 全てのTodoが完了
- [x] 型エラーが解消
- [ ] テストが全てパス
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了
```

### チケット管理

型エラー改修プロジェクトでは、以下の連番付きチケットファイルで管理しています：

#### フェーズ1: 基本型安全性（完了済み）
| ファイル名 | 内容 | 優先度 | ステータス |
|-----------|------|--------|----------|
| 000_requirements_overview.md | 要件定義概要 | - | ✅ 完了 |
| 001_date_type_safety.md | 日付処理の型安全性 | Critical | ✅ 完了 |
| 002_langchain_message_types.md | LangChainメッセージ型 | Critical | ✅ 完了 |
| 003_function_annotations.md | 関数の型注釈 | High | 📋 待機中 |
| 004_yfinance_wrapper.md | YFinanceラッパー | High | 📋 待機中 |
| 005_config_type_safety.md | 設定の型安全性 | Critical | ✅ 完了 |

#### フェーズ2: 構造的問題解決（新規作成）
| ファイル名 | 内容 | 優先度 | ステータス |
|-----------|------|--------|----------|
| 009_interface_union_types.md | interface.pyのUnion型問題 | **最高** | 📋 作成完了 |
| 010_agent_states_circular.md | agent_states.pyの循環定義 | **最高** | 📋 作成完了 |
| 011_cli_variable_definitions.md | CLI層の変数定義問題 | **高** | 📋 作成完了 |
| 012_yfin_utils_annotations.md | yfin_utils.pyの型注釈不足 | **高** | 📋 作成完了 |
| 013_agent_function_annotations.md | エージェント関数の型注釈 | **高** | 📋 作成完了 |

各チケットには以下が含まれます：
- 概要と現状分析
- 要件定義（機能要件・非機能要件）
- 実装計画と見積もり
- Todoリスト（チェックボックス形式 `- [ ]` / `- [x]`）
- 受け入れ条件
- 依存関係