# TradingAgents 型安全性改善ガイド

## 現状の型安全性評価
- **型安全性スコア**: D+
- **型カバレッジ率**: 約35%
- **検出された型エラー**: 113個

## 高優先度の修正箇所

### 1. 日付処理の型修正
```python
# 修正前（問題あり）
start_date = datetime.strptime(start_date, "%Y-%m-%d")  # datetimeオブジェクト
before = start_date - relativedelta(days=look_back_days)  # str型変数に代入

# 修正後
from datetime import datetime
from typing import Union
from dateutil.relativedelta import relativedelta

def get_reddit_global_news(
    start_date: str, 
    look_back_days: int, 
    max_limit_per_day: int
) -> str:
    start_date_obj: datetime = datetime.strptime(start_date, "%Y-%m-%d")
    before_obj: datetime = start_date_obj - relativedelta(days=look_back_days)
    before: str = before_obj.strftime("%Y-%m-%d")
```

### 2. LLMプロバイダの型定義
```python
from typing import Union, Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

LLMType = Union[ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI]

class TradingAgentsGraph:
    def __init__(
        self,
        selected_analysts: List[str] = ["market", "social", "news", "fundamentals"],
        debug: bool = False,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.deep_thinking_llm: LLMType
        self.quick_thinking_llm: LLMType
```

### 3. 設定クラスの型安全化
```python
from typing import TypedDict, Literal

class TradingAgentsConfig(TypedDict):
    project_dir: str
    results_dir: str
    data_dir: str
    data_cache_dir: str
    llm_provider: Literal["openai", "anthropic", "google"]
    deep_think_llm: str
    quick_think_llm: str
    backend_url: str
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    max_recur_limit: int
    online_tools: bool
```

### 4. エージェント関数の型定義
```python
from typing import Callable, Dict, Any
from tradingagents.agents.utils.agent_states import AgentState

AgentNodeType = Callable[[AgentState], Dict[str, Any]]

def create_market_analyst(
    llm: ChatOpenAI, 
    toolkit: 'Toolkit'
) -> AgentNodeType:
    def market_analyst_node(state: AgentState) -> Dict[str, Any]:
        current_date: str = state["trade_date"]
        ticker: str = state["company_of_interest"]
        return {
            "messages": [result],
            "market_report": report,
        }
    return market_analyst_node
```

## 実装手順

### フェーズ1: 基本的な型ヒント（1-2週間）
1. 全関数に引数と戻り値の型ヒントを追加
2. 設定クラスをTypedDictに変換
3. mypy設定ファイルを導入

### フェーズ2: エージェント状態の型定義（2-3週間）
1. AgentState, InvestDebateState, RiskDebateStateの厳密な型定義
2. メッセージ型の安全な処理実装
3. 外部ライブラリとの型互換性改善

### フェーズ3: 高度な型機能（3-4週間）
1. Protocolによるインターフェース定義
2. Genericを使用した汎用型の実装
3. 型ガードによる動的型チェック

## 型チェックの実行

```bash
# mypyのインストール
pip install mypy types-requests types-dateutil types-pytz

# 型チェックの実行
mypy tradingagents/ --config-file mypy.ini

# 段階的な型チェック（エラーを無視しながら進める）
mypy tradingagents/ --config-file mypy.ini --ignore-errors
```

## CI/CDへの統合

GitHub Actionsワークフロー（`.github/workflows/type-check.yml`）:
```yaml
name: Type Check
on: [push, pull_request]
jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install mypy types-requests types-dateutil
    - name: Run mypy
      run: mypy tradingagents/ --config-file mypy.ini
```

## 期待される効果

### 短期的効果
- ランタイムエラーの大幅削減
- IDEの補完機能向上
- コードレビューの効率化

### 長期的効果
- 保守性の向上
- 新規開発者のオンボーディング改善
- リファクタリングの安全性向上

## 型安全性の目標

| メトリクス | 現在 | 目標（3ヶ月後） |
|---------|-----|--------------|
| 型安全性スコア | D+ | B+ |
| 型カバレッジ率 | 35% | 85% |
| 型エラー数 | 113個 | 10個以下 |

## 参考資料
- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [LangChain Type Definitions](https://github.com/langchain-ai/langchain/tree/main/libs/core/langchain_core/types)