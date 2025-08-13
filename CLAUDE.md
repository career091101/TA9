# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TradingAgents is a multi-agent LLM-powered financial trading framework that simulates the dynamics of real-world trading firms. The framework uses specialized agents (analysts, researchers, traders, risk managers) that collaborate to evaluate market conditions and make trading decisions.

## Essential Commands

### Installation
```bash
# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# CLI interface (interactive mode)
python -m cli.main

# Direct execution with custom config
python main.py
```

### Required Environment Variables
```bash
export FINNHUB_API_KEY=$YOUR_FINNHUB_API_KEY  # Required for financial data
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY    # Required for LLM agents
```

## Architecture Overview

### Core System Flow
1. **Data Collection**: Financial data fetched via FinnHub API or cached data
2. **Analysis Phase**: Multiple analyst agents process different data aspects:
   - Market Analyst: Technical indicators (MACD, RSI)
   - News Analyst: Global news and macroeconomic indicators
   - Social Media Analyst: Sentiment analysis from social platforms
   - Fundamentals Analyst: Company financials and performance metrics
3. **Research Phase**: Bull and Bear researchers debate insights
4. **Trading Decision**: Trader agent synthesizes reports and makes decisions
5. **Risk Management**: Risk team evaluates and approves/rejects trades

### Key Components

**Graph Architecture** (`tradingagents/graph/`):
- `trading_graph.py`: Main orchestrator class `TradingAgentsGraph`
- `setup.py`: Graph initialization and agent setup
- `propagation.py`: Message propagation logic
- `conditional_logic.py`: Decision routing between agents
- `reflection.py`: Learning from past decisions
- `signal_processing.py`: Trading signal processing

**Agent System** (`tradingagents/agents/`):
- Each agent type has its own module with a factory function (`create_*_analyst`)
- Agents communicate through LangGraph state management
- Memory system maintains context across trading sessions

**Data Layer** (`tradingagents/dataflows/`):
- `interface.py`: Main data access interface
- Provider-specific utilities: `finnhub_utils.py`, `yfin_utils.py`, `reddit_utils.py`
- Data caching in `dataflows/data_cache/`

### Configuration System

Configuration managed via `tradingagents/default_config.py`:
- LLM settings: `deep_think_llm`, `quick_think_llm`, `llm_provider`
- Debate rounds: `max_debate_rounds`, `max_risk_discuss_rounds`
- Data settings: `online_tools` (true for real-time, false for cached)

Example custom configuration:
```python
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Change LLM
config["max_debate_rounds"] = 2           # Increase debate rounds
config["online_tools"] = True             # Use real-time data
```

### CLI Interface

The CLI (`cli/main.py`) provides an interactive interface with:
- Real-time agent status display
- Message buffering and display management
- Rich terminal UI with progress tracking
- Support for multiple tickers and date selection

## Development Guidelines

### Adding New Agents
1. Create agent module in `tradingagents/agents/[category]/`
2. Implement factory function `create_[agent_name]`
3. Add to `__init__.py` exports
4. Update graph setup in `tradingagents/graph/setup.py`

### Modifying Trading Logic
- Core decision logic: `tradingagents/graph/conditional_logic.py`
- Agent communication: Update state definitions in `agent_states.py`
- Memory persistence: Modify `FinancialSituationMemory` class

### Data Provider Integration
1. Add utility module in `tradingagents/dataflows/`
2. Register in `interface.py`
3. Handle caching if `online_tools=False`

## Important Notes

- The framework makes extensive API calls - use `gpt-4o-mini` for testing to reduce costs
- Default models: `o4-mini` (deep thinking), `gpt-4o-mini` (quick thinking)
- Data cache directory: `tradingagents/dataflows/data_cache/`
- Results stored in: `./results/` (configurable via `TRADINGAGENTS_RESULTS_DIR`)