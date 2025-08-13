# チケット006: エージェント状態の型定義修正

## 概要

TradingAgentsプロジェクトにおけるエージェント状態管理システムで発生している循環参照エラーと型定義の問題を解決します。現在、`InvestDebateState`と`RiskDebateState`の型定義で循環参照が発生し、7件の重要なエラーが発生しています。

## 現状分析

### 影響範囲
- **agents/utils/agent_states.py**: 5件の循環参照エラー
- **agents/__init__.py**: 2件のインポートエラー
- **graph/propagation.py**: 関連する型定義エラー

### 主要なエラーパターン

1. **循環参照によるTypeDict解決不可**
   ```python
   # 問題のあるコード
   class InvestDebateState(TypedDict):
       # ... 定義内で相互参照
   
   class RiskDebateState(TypedDict):
       # ... InvestDebateStateを参照
   ```

2. **モジュールレベルでの型定義エラー**
   ```python
   # 問題のあるコード
   from agent_states import InvestDebateState, RiskDebateState  # [attr-defined] error
   ```

3. **型の相互依存関係**
   ```python
   # 循環参照パターン
   InvestDebateState -> RiskDebateState -> InvestDebateState
   ```

## 要件定義

### 機能要件
- [ ] エージェント状態の循環参照解決
- [ ] 型安全なエージェント状態管理
- [ ] GraphState との統合改善
- [ ] 状態遷移の型安全性確保

### 非機能要件
- [ ] 既存のエージェント動作の互換性維持
- [ ] グラフ処理パフォーマンスの維持
- [ ] 状態管理の単純性保持
- [ ] メモリ効率の最適化

### 制約事項
- LangGraph との統合維持
- TypedDict の活用継続
- 既存の状態キー名の保持

## 実装計画

### 対象ファイル一覧
- `tradingagents/agents/utils/agent_states.py`
- `tradingagents/agents/__init__.py`
- `tradingagents/graph/propagation.py`
- `tradingagents/graph/trading_graph.py`

### 修正方針

1. **循環参照の解決**
   ```python
   # Before: 循環参照
   class InvestDebateState(TypedDict):
       risk_state: RiskDebateState  # エラー
       
   class RiskDebateState(TypedDict):
       invest_state: InvestDebateState  # エラー
   
   # After: 前方参照の利用
   from typing import TYPE_CHECKING
   
   if TYPE_CHECKING:
       from typing import Dict, Any
       
   InvestDebateState = Dict[str, Any]  # 実行時は汎用型
   RiskDebateState = Dict[str, Any]
   ```

2. **状態型の階層化**
   ```python
   # 基本状態型
   class BaseAgentState(TypedDict):
       messages: List[BaseMessage]
       timestamp: datetime
       
   # 特化状態型
   class MarketAnalysisState(BaseAgentState):
       technical_indicators: Dict[str, float]
       
   class RiskAssessmentState(BaseAgentState):
       risk_score: float
       recommendations: List[str]
   ```

3. **Union型による柔軟性確保**
   ```python
   from typing import Union
   
   AnyAgentState = Union[
       MarketAnalysisState,
       RiskAssessmentState,
       InvestDebateState,
       RiskDebateState
   ]
   ```

### 見積もり工数
- 設計・調査: 1日
- 実装: 2日
- テスト・検証: 1日
- **合計: 4日**

## 受け入れ条件

- [ ] エージェント状態関連の型エラー7件が全て解消される
- [ ] mypyで循環参照エラーが解決される
- [ ] 既存のエージェント動作が正常に機能する
- [ ] グラフの状態遷移が正常に動作する
- [ ] メモリリークが発生しない

## Todoリスト

### Phase 1: 循環参照分析と設計
- [ ] 現在の状態型依存関係の詳細分析
- [ ] 循環参照解決のアーキテクチャ設計
- [ ] 新しい状態型階層の設計
- [ ] 後方互換性の保証方法検討

### Phase 2: 基盤状態型の実装
- [ ] BaseAgentState の定義
- [ ] 共通状態フィールドの抽出
- [ ] 型安全なアクセサーメソッド実装
- [ ] 状態バリデーション機能実装

### Phase 3: agent_states.py の修正
- [ ] 循環参照の除去
- [ ] TYPE_CHECKINGを使用した前方参照実装
- [ ] InvestDebateState の再定義
- [ ] RiskDebateState の再定義
- [ ] その他の状態型の整理

### Phase 4: インポート関係の修正
- [ ] agents/__init__.py のインポートエラー修正
- [ ] 型定義の適切なエクスポート
- [ ] モジュール間依存関係の整理
- [ ] 循環インポートの防止

### Phase 5: グラフ統合の修正
- [ ] propagation.py の型エラー修正
- [ ] trading_graph.py での状態利用修正
- [ ] 状態遷移ロジックの型安全化
- [ ] エラーハンドリングの改善

### Phase 6: テストと検証
- [ ] 型チェックテストの作成
- [ ] 状態遷移のテスト
- [ ] エージェント動作の回帰テスト
- [ ] メモリ使用量の検証

### Phase 7: ドキュメント整備
- [ ] エージェント状態設計書の更新
- [ ] 型定義ガイドラインの作成
- [ ] 開発者向けドキュメント更新

## 依存関係

### 前提条件
- **003_function_annotations.md**: 基本的な型注釈標準
- **002_langchain_message_types.md**: メッセージ型の定義

### 影響を与えるチケット
- **007_dataflow_types.md**: データフロー状態との統合
- **008_memory_types.md**: メモリ状態との統合

### 後続チケット
- **009_testing_strategy.md**: エージェント状態のテスト戦略

## 優先度: Critical

### 根拠
- エージェントシステムの中核機能
- 循環参照は実行時エラーの原因
- グラフ処理全体への影響
- デバッグが困難な問題

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| エージェント動作変更 | 高 | 中 | 詳細なテストと段階的適用 |
| 状態管理複雑化 | 中 | 低 | シンプルな設計原則維持 |
| パフォーマンス劣化 | 中 | 低 | 効率的な型チェック実装 |
| 循環参照再発 | 低 | 中 | 設計ガイドラインと自動チェック |

## 技術仕様

### 新しい状態型階層

```python
from typing import TypedDict, List, Dict, Any, Optional, Union, TYPE_CHECKING
from datetime import datetime
from langchain_core.messages import BaseMessage

if TYPE_CHECKING:
    # 型チェック時のみの定義
    from typing import Dict, Any

# 基本状態型
class BaseAgentState(TypedDict):
    messages: List[BaseMessage]
    timestamp: datetime
    agent_id: str
    status: str

# 特化状態型
class AnalysisState(BaseAgentState):
    analysis_results: Dict[str, Any]
    confidence_score: float

class DebateState(BaseAgentState):
    position: str  # "bull" or "bear"
    arguments: List[str]
    counter_arguments: List[str]

class RiskState(BaseAgentState):
    risk_level: str
    risk_factors: List[str]
    mitigation_strategies: List[str]

# 統合状態型（循環参照回避）
class TradingGraphState(TypedDict):
    # 各エージェントの状態を辞書として管理
    market_analysis: Optional[AnalysisState]
    news_analysis: Optional[AnalysisState]
    fundamentals_analysis: Optional[AnalysisState]
    social_media_analysis: Optional[AnalysisState]
    
    bull_research: Optional[DebateState]
    bear_research: Optional[DebateState]
    
    risk_assessment: Optional[RiskState]
    
    # 共通フィールド
    messages: List[BaseMessage]
    current_step: str
    iteration_count: int
```

### 型安全なアクセサー

```python
from typing import TypeVar, Type, Optional

T = TypeVar('T', bound=BaseAgentState)

class StateManager:
    def __init__(self, state: TradingGraphState):
        self._state = state
    
    def get_agent_state(self, agent_type: str) -> Optional[BaseAgentState]:
        """エージェント状態の型安全な取得"""
        return self._state.get(agent_type)
    
    def set_agent_state(self, agent_type: str, state: BaseAgentState) -> None:
        """エージェント状態の型安全な設定"""
        self._state[agent_type] = state
    
    def validate_state(self) -> List[str]:
        """状態の妥当性検証"""
        errors = []
        
        # 必須フィールドの確認
        if "messages" not in self._state:
            errors.append("Missing required field: messages")
            
        return errors
```

### 循環参照解決パターン

```python
# 実行時型定義（汎用的）
InvestDebateState = Dict[str, Any]
RiskDebateState = Dict[str, Any]

# 開発時型定義（厳密）  
if TYPE_CHECKING:
    class InvestDebateState(BaseAgentState):
        debate_rounds: int
        bull_arguments: List[str]
        bear_arguments: List[str]
        consensus: Optional[str]
    
    class RiskDebateState(BaseAgentState):
        risk_discussions: List[Dict[str, Any]]
        final_assessment: Optional[str]
        approved: bool

# ユーティリティ関数
def create_invest_debate_state(**kwargs) -> InvestDebateState:
    """型安全な投資討論状態作成"""
    return {
        "messages": [],
        "timestamp": datetime.now(),
        "agent_id": "invest_debate",
        "status": "active",
        **kwargs
    }
```