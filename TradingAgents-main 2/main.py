from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents import load_config, validate_api_keys
from tradingagents.default_config import DEFAULT_CONFIG

# APIキーの検証と.envファイルの読み込み
print("🔑 APIキーを確認中...")
if not validate_api_keys():
    print("❗ APIキーが不足しています。アプリケーションを終了します。")
    exit(1)

print("✅ APIキーの確認が完了しました。")

# 設定をロード（APIキー検証は上で完了済みなのでスキップ）
try:
    config = load_config(validate_keys=False)  # 既に検証済みなのでFalse
except Exception as e:
    print(f"❗ 設定の読み込みに失敗しました: {e}")
    print("フォールバックでデフォルト設定を使用します...")
    config = DEFAULT_CONFIG.copy()

# カスタム設定の適用
# config["llm_provider"] = "google"  # 他のLLMプロバイダーを使用する場合
# config["backend_url"] = "https://generativelanguage.googleapis.com/v1"  # Google APIの場合
# config["deep_think_llm"] = "gemini-2.0-flash"  # Googleモデルを使用する場合
# config["quick_think_llm"] = "gemini-2.0-flash"  # Googleモデルを使用する場合
config["max_debate_rounds"] = 1  # ディベートラウンド数
config["online_tools"] = True  # オンラインツールの使用

# グラフの初期化
print("🚀 TradingAgentsグラフを初期化中...")
ta = TradingAgentsGraph(debug=True, config=config)

# 取引分析の実行
ticker = "NVDA"
date = "2024-05-10"

print(f"📈 {ticker} ({date}) の分析を開始...")
_, decision = ta.propagate(ticker, date)

print(f"
📋 分析結果:")
print(decision)

# メモリ機能（オプション）
# ポジションのリターンをパラメーターとして指定
# ta.reflect_and_remember(1000)
print("
✅ 分析が完了しました。")
