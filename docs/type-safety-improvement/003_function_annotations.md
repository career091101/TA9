# チケット003: 関数の型注釈標準化

## 概要
プロジェクト全体で35件の関数に型注釈が不足している。統一的な型注釈標準を定義し、全関数に適用する。

## 現状分析

### エラー件数
- **総エラー数**: 35件
- **エラータイプ**: `[no-untyped-def]`
- **影響範囲**: agents配下のほぼ全ファイル

### 主要な問題パターン
1. 引数の型注釈なし
2. 戻り値の型注釈なし  
3. ジェネリック型の未使用
4. Any型の過度な使用

### 影響モジュール
- `tradingagents/agents/analysts/`
- `tradingagents/agents/researchers/`
- `tradingagents/agents/managers/`
- `tradingagents/agents/risk_mgmt/`
- `tradingagents/agents/trader/`

## 要件定義

### 機能要件
- FR-001: 全関数への型注釈追加
- FR-002: 型エイリアスの定義と活用
- FR-003: プロトコル定義による抽象化

### 非機能要件
- NFR-001: IDEの補完機能向上
- NFR-002: 型注釈の一貫性
- NFR-003: 保守性の向上

### 制約事項
- 既存の関数シグネチャを変更しない
- パフォーマンスへの影響なし

## 実装計画

### 標準型定義の作成
```python
# tradingagents/types.py
from typing import Callable, Dict, Any, TypeAlias, Protocol
from langchain_openai import ChatOpenAI

# 型エイリアス
AgentNodeType: TypeAlias = Callable[[Dict[str, Any]], Dict[str, Any]]
ConfigType: TypeAlias = Dict[str, Any]
ReportType: TypeAlias = str
ToolkitType: TypeAlias = Any  # 後で具体化

# プロトコル定義
class AgentProtocol(Protocol):
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]: ...

class AnalystFactory(Protocol):
    def __call__(self, llm: ChatOpenAI, toolkit: ToolkitType) -> AgentNodeType: ...
```

### 実装パターン
```python
# 修正前
def create_market_analyst(llm, toolkit):
    def market_analyst_node(state):
        return {"messages": [result]}

# 修正後
from typing import Dict, Any
from tradingagents.types import AgentNodeType, ToolkitType
from langchain_openai import ChatOpenAI

def create_market_analyst(
    llm: ChatOpenAI, 
    toolkit: ToolkitType
) -> AgentNodeType:
    def market_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
        current_date: str = state["trade_date"]
        ticker: str = state["company_of_interest"]
        return {"messages": [result], "market_report": report}
    return market_analyst_node
```

### 見積もり工数
- 分析: 0.5日
- 実装: 3.5日
- テスト: 1日
- **合計: 5日**

## 受け入れ条件

### 必須条件
- [ ] no-untyped-defエラーが0件
- [ ] 全関数に型注釈が追加
- [ ] 型チェックが通る

### 推奨条件
- [ ] 型注釈スタイルガイドの作成
- [ ] 自動型注釈ツールの導入検討

## Todoリスト

### 準備作業
- [ ] 型注釈が必要な関数のリストアップ
- [ ] 標準型定義の設計
- [ ] 命名規則の決定

### 共通型定義の作成
- [ ] types.pyの作成
  - [ ] 基本型エイリアスの定義
  - [ ] プロトコルの定義
  - [ ] カスタム型の定義
- [ ] agent_types.pyの作成
  - [ ] エージェント固有の型定義
  - [ ] ファクトリ関数の型定義

### アナリストエージェントの型注釈
- [ ] market_analyst.py
  - [ ] create_market_analyst関数
  - [ ] 内部関数の型注釈
- [ ] news_analyst.py
  - [ ] create_news_analyst関数
- [ ] social_media_analyst.py
  - [ ] create_social_media_analyst関数
- [ ] fundamentals_analyst.py
  - [ ] create_fundamentals_analyst関数

### リサーチャーエージェントの型注釈
- [ ] bull_researcher.py
  - [ ] create_bull_researcher関数
- [ ] bear_researcher.py
  - [ ] create_bear_researcher関数

### マネージャーエージェントの型注釈
- [ ] research_manager.py
  - [ ] create_research_manager関数
- [ ] risk_manager.py
  - [ ] create_risk_manager関数

### リスク管理エージェントの型注釈
- [ ] aggressive_debator.py
  - [ ] create_risky_debator関数
- [ ] conservative_debator.py
  - [ ] create_safe_debator関数
- [ ] neutral_debator.py
  - [ ] create_neutral_debator関数

### トレーダーエージェントの型注釈
- [ ] trader.py
  - [ ] create_trader関数
  - [ ] ヘルパー関数の型注釈

### テスト作業
- [ ] 型チェックの実行
  - [ ] 個別モジュールのチェック
  - [ ] 全体チェック
- [ ] IDEでの補完テスト
- [ ] 実行時テスト

### ドキュメント
- [ ] 型注釈スタイルガイド
- [ ] 型定義の使用例
- [ ] マイグレーションガイド

## 依存関係
- チケット005（設定の型安全性）の完了後が望ましい
- チケット006（エージェント状態の型定義）と並行実装可能

## 優先度
**High** - 開発効率とコード品質に直接影響

## リスクと対策

### リスク1: 型注釈の複雑化
**対策**:
- シンプルな型から開始
- 段階的な詳細化
- 過度な一般化を避ける

### リスク2: 循環参照
**対策**:
- TYPE_CHECKINGを使用
- 前方参照の活用
- インポート構造の見直し

### リスク3: メンテナンスコスト
**対策**:
- 型エイリアスの活用
- プロトコルによる抽象化
- 自動化ツールの導入

## 参考情報

### 型注釈のベストプラクティス
```python
from typing import Optional, Union, List, Dict, Any

# 良い例
def process_data(
    data: List[Dict[str, Any]],
    config: Optional[Dict[str, str]] = None
) -> Union[str, None]:
    pass

# 避けるべき例
def process_data(data, config=None):  # 型注釈なし
    pass
```

### PEP 484準拠の型注釈
- https://www.python.org/dev/peps/pep-0484/
- https://docs.python.org/3/library/typing.html

## 完了確認
- [ ] 全てのTodoが完了
- [ ] 型エラーが解消（no-untyped-def: 0件）
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了
- [ ] IDEサポートの確認