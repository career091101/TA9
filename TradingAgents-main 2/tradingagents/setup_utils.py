"""
TradingAgentsプロジェクトのセットアップ支援ユーティリティ

このモジュールは初回セットアップ時の支援機能を提供します。
"""

import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()


def check_environment() -> dict:
    """開発環境の状況をチェック
    
    Returns:
        dict: 環境チェック結果
    """
    results = {
        "python_dotenv": False,
        "env_file_exists": False,
        "env_example_exists": False,
        "required_api_keys": {},
        "optional_api_keys": {}
    }
    
    # python-dotenvのチェック
    try:
        import dotenv
        results["python_dotenv"] = True
    except ImportError:
        results["python_dotenv"] = False
    
    # ファイル存在チェック
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    results["env_file_exists"] = env_file.exists()
    results["env_example_exists"] = env_example.exists()
    
    # APIキーの存在チェック
    required_keys = ["OPENAI_API_KEY", "FINNHUB_API_KEY"]
    optional_keys = ["ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]
    
    for key in required_keys:
        results["required_api_keys"][key] = bool(os.getenv(key))
    
    for key in optional_keys:
        results["optional_api_keys"][key] = bool(os.getenv(key))
    
    return results


def display_environment_status(results: dict) -> None:
    """環境状況を表示"""
    console.print("\n[bold blue]🔍 環境チェック結果[/bold blue]")
    
    # 依存関係チェック
    dotenv_status = "✅ インストール済み" if results["python_dotenv"] else "❌ 未インストール"
    console.print(f"  python-dotenv: {dotenv_status}")
    
    # ファイル存在チェック
    env_status = "✅ 存在" if results["env_file_exists"] else "❌ 未作成"
    example_status = "✅ 存在" if results["env_example_exists"] else "❌ 未作成"
    console.print(f"  .env ファイル: {env_status}")
    console.print(f"  .env.example ファイル: {example_status}")
    
    # APIキーチェック
    console.print("\n[bold]🔑 APIキー設定状況:[/bold]")
    console.print("  [bold]必須キー:[/bold]")
    for key, exists in results["required_api_keys"].items():
        status = "✅ 設定済み" if exists else "❌ 未設定"
        console.print(f"    {key}: {status}")
    
    console.print("  [bold]オプションキー:[/bold]")
    for key, exists in results["optional_api_keys"].items():
        status = "✅ 設定済み" if exists else "⚠️ 未設定"
        console.print(f"    {key}: {status}")


def setup_environment() -> bool:
    """環境セットアップを実行
    
    Returns:
        bool: セットアップが成功したかどうか
    """
    console.print("[bold green]🚀 TradingAgents環境セットアップ[/bold green]\n")
    
    # 環境チェック
    results = check_environment()
    display_environment_status(results)
    
    setup_needed = False
    
    # python-dotenvが必要な場合
    if not results["python_dotenv"]:
        console.print("\n[bold yellow]⚠️ python-dotenvが必要です[/bold yellow]")
        if Confirm.ask("pip install python-dotenvを実行しますか？"):
            os.system("pip install python-dotenv")
            setup_needed = True
    
    # .envファイルが存在しない場合
    if not results["env_file_exists"]:
        console.print("\n[bold yellow]⚠️ .envファイルが存在しません[/bold yellow]")
        
        if results["env_example_exists"]:
            if Confirm.ask(".env.exampleから.envファイルを作成しますか？"):
                project_root = Path(__file__).parent.parent
                shutil.copy(project_root / ".env.example", project_root / ".env")
                console.print("[green]✅ .envファイルを作成しました[/green]")
                setup_needed = True
        else:
            console.print("[red]❌ .env.exampleファイルが見つかりません[/red]")
            return False
    
    # APIキーが不足している場合
    missing_required = [k for k, v in results["required_api_keys"].items() if not v]
    if missing_required:
        console.print(f"\n[bold red]⚠️ 必須APIキーが未設定です: {', '.join(missing_required)}[/bold red]")
        console.print("以下の手順でAPIキーを設定してください：")
        console.print("1. .envファイルを編集")
        console.print("2. 該当するAPIキーを設定")
        console.print("3. アプリケーションを再起動")
        
        # エディタで.envファイルを開く
        if Confirm.ask(".envファイルをエディタで開きますか？"):
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"
            if env_file.exists():
                # システムのデフォルトエディタで開く
                os.system(f"open {env_file}")  # macOS
                # os.system(f"notepad {env_file}")  # Windows
                # os.system(f"nano {env_file}")  # Linux
    
    return setup_needed or len(missing_required) == 0


def create_env_template() -> None:
    """環境変数テンプレートを作成（.env.exampleが存在しない場合）"""
    project_root = Path(__file__).parent.parent
    env_example = project_root / ".env.example"
    
    if env_example.exists():
        console.print("[yellow]⚠️ .env.exampleファイルは既に存在します[/yellow]")
        return
    
    template_content = """# TradingAgents 環境変数設定ファイル
# このファイルを .env にコピーして、実際の値を設定してください

# =================================
# 必須 API キー
# =================================

# OpenAI API キー（必須）
OPENAI_API_KEY=your_openai_api_key_here

# Finnhub API キー（必須）
FINNHUB_API_KEY=your_finnhub_api_key_here

# =================================
# オプション API キー
# =================================

# Anthropic (Claude) API キー（オプション）
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Generative AI API キー（オプション）
GOOGLE_API_KEY=your_google_api_key_here

# =================================
# 動作設定（オプション）
# =================================

# オンラインツール使用フラグ（true/false）
TRADINGAGENTS_ONLINE_TOOLS=true

# デバッグモード（true/false）
TRADINGAGENTS_DEBUG=false
"""
    
    with open(env_example, "w", encoding="utf-8") as f:
        f.write(template_content)
    
    console.print(f"[green]✅ .env.exampleファイルを作成しました: {env_example}[/green]")


def quick_setup() -> bool:
    """クイックセットアップ（対話式）
    
    Returns:
        bool: セットアップが完了したかどうか
    """
    console.print(Panel(
        "[bold green]TradingAgents クイックセットアップ[/bold green]\n\n"
        "このセットアップでは以下を行います：\n"
        "• 依存関係のチェック\n"
        "• .envファイルの作成\n"
        "• APIキーの設定確認\n"
        "• 基本動作確認",
        title="セットアップ開始",
        border_style="green"
    ))
    
    if not Confirm.ask("\nセットアップを開始しますか？"):
        return False
    
    # 環境セットアップを実行
    success = setup_environment()
    
    if success:
        console.print("\n[bold green]🎉 セットアップが完了しました！[/bold green]")
        console.print("\n次のステップ：")
        console.print("1. .envファイルに正しいAPIキーを設定")
        console.print("2. python main.py または python -m cli.main でアプリケーションを起動")
        console.print("3. 問題がある場合は python -m tradingagents.setup_utils でセットアップを再実行")
    else:
        console.print("\n[bold red]❌ セットアップに問題がありました[/bold red]")
        console.print("手動で.envファイルを作成し、APIキーを設定してください。")
    
    return success


if __name__ == "__main__":
    """コマンドラインから直接実行された場合"""
    quick_setup()