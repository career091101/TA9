# チケット009: 型チェックテスト戦略

## 概要

TradingAgentsプロジェクトにおける型安全性の継続的な保証のため、包括的な型チェックテスト戦略を実装します。mypyを活用した自動型チェック、型安全性のユニットテスト、型関連のエッジケーステストを整備し、今後の型エラーの発生を防止します。

## 現状分析

### 課題
- 型チェックが手動実行に依存
- 型安全性の回帰テストが不十分
- エラーケースの型安全性テストが不足
- 型定義の網羅性検証が困難

### 目標
- 自動化された型チェックテスト環境の構築
- 型安全性を保証するテストスイートの作成
- 継続的インテグレーションでの型チェック実施
- 型関連バグの早期発見システム確立

## 要件定義

### 機能要件
- [ ] mypyを活用した自動型チェック
- [ ] 型安全性のユニットテスト実装
- [ ] 型エラーの回帰テスト機能
- [ ] 型定義網羅率の測定機能

### 非機能要件
- [ ] テスト実行時間の最適化
- [ ] CI/CDパイプラインとの統合
- [ ] 型チェック結果の可視化
- [ ] 開発者フレンドリーなエラー報告

### 制約事項
- 既存テストスイートとの互換性
- Python 3.13環境での動作保証
- プロジェクト依存関係の最小化

## 実装計画

### テスト構成
```
tests/
├── type_safety/
│   ├── __init__.py
│   ├── test_date_types.py
│   ├── test_langchain_types.py
│   ├── test_function_annotations.py
│   ├── test_yfinance_types.py
│   ├── test_config_types.py
│   ├── test_agent_state_types.py
│   ├── test_dataflow_types.py
│   └── test_memory_types.py
├── mypy_config/
│   ├── mypy.ini
│   ├── strict.ini
│   └── baseline.ini
└── type_coverage/
    └── measure_coverage.py
```

### 修正方針

1. **mypy設定の最適化**
   ```ini
   [mypy]
   python_version = 3.13
   warn_return_any = True
   warn_unused_configs = True
   disallow_untyped_defs = True
   disallow_incomplete_defs = True
   check_untyped_defs = True
   disallow_untyped_decorators = True
   ```

2. **型安全性テストの実装**
   ```python
   def test_date_type_safety():
       # 日付型の安全性テスト
       from tradingagents.dataflows.interface import get_finnhub_news
       
       # 型チェック対象の関数呼び出し
       result = get_finnhub_news("AAPL", datetime.now())
       assert isinstance(result, (list, type(None)))
   ```

3. **型エラー回帰テストの実装**
   ```python
   def test_no_type_regression():
       # 以前修正した型エラーの再発防止
       import subprocess
       result = subprocess.run(
           ["mypy", "--config-file", "tests/mypy_config/strict.ini", "tradingagents/"],
           capture_output=True, text=True
       )
       assert result.returncode == 0, f"Type errors detected:\n{result.stdout}"
   ```

### 見積もり工数
- テスト設計: 1日
- テスト実装: 3日
- CI/CD統合: 1日
- ドキュメント: 1日
- **合計: 6日**

## 受け入れ条件

- [ ] 全てのモジュールで型チェックが通過する
- [ ] 型安全性テストスイートが完成する
- [ ] CI/CDパイプラインで自動型チェックが動作する
- [ ] 型カバレッジが90%以上になる
- [ ] 型エラーの回帰テストが機能する

## Todoリスト

### Phase 1: テスト基盤整備
- [ ] テスト用ディレクトリ構造の作成
- [ ] mypy設定ファイルの作成（strict, baseline）
- [ ] pytest設定の型チェック対応
- [ ] テスト用ユーティリティ関数の実装

### Phase 2: モジュール別型テスト実装
- [ ] 日付処理の型安全性テスト (test_date_types.py)
- [ ] LangChainメッセージ型テスト (test_langchain_types.py)
- [ ] 関数注釈テスト (test_function_annotations.py)
- [ ] YFinanceラッパー型テスト (test_yfinance_types.py)
- [ ] 設定型テスト (test_config_types.py)
- [ ] エージェント状態型テスト (test_agent_state_types.py)
- [ ] データフロー型テスト (test_dataflow_types.py)
- [ ] メモリ型テスト (test_memory_types.py)

### Phase 3: 回帰テスト実装
- [ ] 型エラー回帰防止テスト
- [ ] 型定義変更の影響テスト
- [ ] 後方互換性の型テスト
- [ ] パフォーマンス影響測定テスト

### Phase 4: 型カバレッジ測定
- [ ] 型注釈カバレッジ測定ツール実装
- [ ] 未注釈関数の検出機能
- [ ] カバレッジレポート生成機能
- [ ] カバレッジしきい値の設定

### Phase 5: CI/CD統合
- [ ] GitHub Actions/GitLab CIでの型チェック実装
- [ ] 型チェック失敗時の詳細レポート
- [ ] プルリクエスト時の自動型チェック
- [ ] 型チェック結果の通知機能

### Phase 6: 開発支援ツール
- [ ] 開発用pre-commit hook設定
- [ ] VS Code設定ファイル作成
- [ ] 型エラー修正支援スクリプト
- [ ] 型定義自動生成ツール

### Phase 7: ドキュメントとガイドライン
- [ ] 型安全性テストガイド作成
- [ ] 新規開発時の型チェック手順
- [ ] 型エラー対応マニュアル
- [ ] ベストプラクティス集

## 依存関係

### 前提条件
- **001-008**: 全ての型改修チケットの完了

### 影響を与えるチケット
- **010_ci_cd_integration.md**: CI/CD環境での統合

### 外部依存
- mypy, pytest, pytest-mypy
- GitHub Actions または同等のCI/CDサービス

## 優先度: Medium

### 根拠
- 型安全性の長期的な保証に重要
- 開発効率の向上に寄与
- 品質保証の自動化に貢献
- 今後の保守性向上に不可欠

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| テスト実行時間の増加 | 中 | 中 | 並列実行とキャッシュ活用 |
| CI/CD環境の複雑化 | 低 | 低 | シンプルな設定と明確な文書化 |
| 開発フローの変更 | 中 | 中 | 段階的導入と教育 |
| 型チェック誤検知 | 低 | 中 | 適切な設定と例外処理 |

## 技術仕様

### mypy設定

```ini
# mypy.ini - 基本設定
[mypy]
python_version = 3.13
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_unreachable = True
strict_equality = True

# strict.ini - 厳密モード
[mypy]
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_any_generics = True
disallow_subclassing_any = True
disallow_untyped_calls = True

# 外部ライブラリの型無視
[mypy-yfinance.*]
ignore_missing_imports = True

[mypy-stockstats.*]
ignore_missing_imports = True
```

### 型安全性テストクラス

```python
import unittest
from typing import Any, Optional, Union, Type
import mypy.api

class TypeSafetyTestBase(unittest.TestCase):
    """型安全性テストの基底クラス"""
    
    def assertTypeChecks(self, code: str) -> None:
        """コードが型チェックを通過することを確認"""
        result = mypy.api.run(["-c", code])
        self.assertEqual(result[2], 0, f"Type check failed: {result[0]}")
    
    def assertTypeError(self, code: str, expected_error: str) -> None:
        """コードが期待された型エラーを発生することを確認"""
        result = mypy.api.run(["-c", code])
        self.assertNotEqual(result[2], 0)
        self.assertIn(expected_error, result[0])
    
    def assertValidType(self, value: Any, expected_type: Type) -> None:
        """値が期待された型であることを確認"""
        self.assertIsInstance(value, expected_type)

class DateTypeSafetyTest(TypeSafetyTestBase):
    """日付型の安全性テスト"""
    
    def test_date_parameter_types(self):
        """日付パラメータの型安全性"""
        code = """
from datetime import datetime
from tradingagents.dataflows.interface import get_finnhub_news

# 正常ケース
result1 = get_finnhub_news("AAPL", datetime.now())
result2 = get_finnhub_news("AAPL", "2024-01-01")

# エラーケース
# result3 = get_finnhub_news("AAPL", 123)  # int -> error
"""
        self.assertTypeChecks(code)
    
    def test_date_conversion_safety(self):
        """日付変換の安全性"""
        from tradingagents.dataflows.utils import ensure_datetime
        from datetime import datetime
        
        # str -> datetime
        result1 = ensure_datetime("2024-01-01")
        self.assertValidType(result1, datetime)
        
        # datetime -> datetime  
        result2 = ensure_datetime(datetime.now())
        self.assertValidType(result2, datetime)
```

### 型カバレッジ測定

```python
import ast
import os
from typing import Dict, List, Tuple

class TypeCoverageMeasurer:
    """型注釈カバレッジの測定"""
    
    def __init__(self, source_dir: str):
        self.source_dir = source_dir
        
    def measure_coverage(self) -> Dict[str, float]:
        """各ファイルの型カバレッジを測定"""
        results = {}
        
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    coverage = self._analyze_file(file_path)
                    results[file_path] = coverage
                    
        return results
    
    def _analyze_file(self, file_path: str) -> float:
        """単一ファイルの型カバレッジ分析"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        total_functions = 0
        typed_functions = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_functions += 1
                
                # 引数の型注釈チェック
                has_arg_annotations = any(
                    arg.annotation for arg in node.args.args
                )
                
                # 戻り値の型注釈チェック
                has_return_annotation = node.returns is not None
                
                if has_arg_annotations or has_return_annotation:
                    typed_functions += 1
        
        return typed_functions / total_functions if total_functions > 0 else 1.0

    def generate_report(self) -> str:
        """カバレッジレポートの生成"""
        coverage_data = self.measure_coverage()
        
        report = "Type Coverage Report\n"
        report += "=" * 50 + "\n"
        
        total_coverage = sum(coverage_data.values()) / len(coverage_data)
        report += f"Overall Coverage: {total_coverage:.2%}\n\n"
        
        for file_path, coverage in sorted(coverage_data.items()):
            report += f"{file_path}: {coverage:.2%}\n"
            
        return report
```

### CI/CD統合例

```yaml
# .github/workflows/type-check.yml
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
        python-version: '3.13'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install mypy pytest pytest-mypy
        
    - name: Run mypy type checking
      run: |
        mypy --config-file tests/mypy_config/mypy.ini tradingagents/
        
    - name: Run type safety tests
      run: |
        pytest tests/type_safety/ -v
        
    - name: Generate type coverage report
      run: |
        python tests/type_coverage/measure_coverage.py > type_coverage_report.txt
        
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      with:
        name: type-coverage-report
        path: type_coverage_report.txt
```