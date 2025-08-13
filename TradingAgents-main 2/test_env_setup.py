#!/usr/bin/env python3
"""
環境変数設定のテストスクリプト

このスクリプトは.envファイルとAPIキーの設定が正しく動作するかテストします。
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents import (
    validate_api_keys,
    load_config,
    get_api_key,
    check_environment,
    setup_environment
)
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_dotenv_loading():
    """dotenvライブラリの動作テスト"""
    try:
        from dotenv import load_dotenv
        console.print("[green]✅ python-dotenv正常にインポート[/green]")
        
        # .envファイルを読み込み
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            console.print(f"[green]✅ .envファイル読み込み成功: {env_file}[/green]")
        else:
            console.print(f"[yellow]⚠️ .envファイルが見つかりません: {env_file}[/yellow]")
            
        return True
    except ImportError:
        console.print("[red]❌ python-dotenvがインストールされていません[/red]")
        console.print("pip install python-dotenv を実行してください")
        return False


def test_api_key_loading():
    """APIキー読み込みのテスト"""
    console.print("\n[bold blue]🔑 APIキー読み込みテスト[/bold blue]")
    
    api_keys = {
        "OPENAI_API_KEY": "OpenAI API",
        "FINNHUB_API_KEY": "Finnhub API", 
        "ANTHROPIC_API_KEY": "Anthropic Claude API",
        "GOOGLE_API_KEY": "Google Generative AI API"
    }
    
    results = {}
    for key_name, description in api_keys.items():
        value = get_api_key(key_name)
        if value:
            # セキュリティのため最初の8文字のみ表示
            masked_value = value[:8] + "..." if len(value) > 8 else value
            console.print(f"  {key_name}: [green]✅ 設定済み ({masked_value})[/green]")
            results[key_name] = True
        else:
            console.print(f"  {key_name} ({description}): [red]❌ 未設定[/red]")
            results[key_name] = False
    
    return results


def test_config_loading():
    """設定読み込みのテスト"""
    console.print("\n[bold blue]⚙️ 設定読み込みテスト[/bold blue]")
    
    try:
        # APIキー検証なしで設定を読み込み
        config = load_config(validate_keys=False)
        console.print("[green]✅ 設定読み込み成功[/green]")
        
        # 主要な設定項目を表示
        console.print(f"  LLMプロバイダー: {config['llm_provider']}")
        console.print(f"  深く考える時のLLM: {config['deep_think_llm']}")
        console.print(f"  素早く考える時のLLM: {config['quick_think_llm']}")
        console.print(f"  オンラインツール: {config['online_tools']}")
        
        return True
    except Exception as e:
        console.print(f"[red]❌ 設定読み込み失敗: {e}[/red]")
        return False


def test_api_key_validation():
    """APIキー検証機能のテスト"""
    console.print("\n[bold blue]🔍 APIキー検証テスト[/bold blue]")
    
    try:
        # 検証を実行（出力を抑制）
        import io
        from contextlib import redirect_stdout
        
        with redirect_stdout(io.StringIO()):
            is_valid = validate_api_keys()
        
        if is_valid:
            console.print("[green]✅ 必須APIキーがすべて設定されています[/green]")
        else:
            console.print("[yellow]⚠️ 一部のAPIキーが不足しています[/yellow]")
        
        return is_valid
    except Exception as e:
        console.print(f"[red]❌ APIキー検証でエラー: {e}[/red]")
        return False


def main():
    """メイン実行関数"""
    console.print(Panel(
        "[bold green]TradingAgents 環境テスト[/bold green]\n\n"
        "このスクリプトは以下をテストします：\n"
        "• python-dotenvの動作確認\n"
        "• .envファイルの読み込み\n"
        "• APIキーの取得\n"
        "• 設定の読み込み\n"
        "• APIキーの検証",
        title="環境テスト開始",
        border_style="blue"
    ))
    
    # テスト実行
    test_results = {}
    
    # 1. dotenvライブラリのテスト
    test_results["dotenv"] = test_dotenv_loading()
    
    # 2. APIキー読み込みのテスト
    api_key_results = test_api_key_loading()
    test_results["api_keys"] = api_key_results
    
    # 3. 設定読み込みのテスト
    test_results["config"] = test_config_loading()
    
    # 4. APIキー検証のテスト
    test_results["validation"] = test_api_key_validation()
    
    # 結果サマリー
    console.print("\n" + "="*50)
    console.print("[bold blue]📊 テスト結果サマリー[/bold blue]")
    
    all_passed = True
    
    if test_results["dotenv"]:
        console.print("[green]✅ python-dotenv: 正常[/green]")
    else:
        console.print("[red]❌ python-dotenv: エラー[/red]")
        all_passed = False
    
    required_keys_ok = all(api_key_results.get(k, False) for k in ["OPENAI_API_KEY", "FINNHUB_API_KEY"])
    if required_keys_ok:
        console.print("[green]✅ 必須APIキー: 設定済み[/green]")
    else:
        console.print("[red]❌ 必須APIキー: 不足[/red]")
        all_passed = False
    
    if test_results["config"]:
        console.print("[green]✅ 設定読み込み: 正常[/green]")
    else:
        console.print("[red]❌ 設定読み込み: エラー[/red]")
        all_passed = False
    
    if test_results["validation"]:
        console.print("[green]✅ APIキー検証: 正常[/green]")
    else:
        console.print("[yellow]⚠️ APIキー検証: 警告[/yellow]")
    
    # 最終結果
    if all_passed:
        console.print("\n[bold green]🎉 すべてのテストが正常に完了しました！[/bold green]")
        console.print("TradingAgentsを起動する準備が整いました。")
        console.print("\n次のコマンドでアプリケーションを開始できます：")
        console.print("  python main.py")
        console.print("  python -m cli.main")
    else:
        console.print("\n[bold red]⚠️ 一部のテストで問題が発見されました[/bold red]")
        console.print("以下のコマンドでセットアップを実行してください：")
        console.print("  python -m tradingagents.setup_utils")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)