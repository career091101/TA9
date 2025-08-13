# チケット010: CI/CD統合計画

## 概要

TradingAgentsプロジェクトのCI/CDパイプラインに型チェック機能を統合し、継続的な型安全性の保証を実現します。GitHub Actions または同等のCI/CDサービスを活用し、プルリクエストやコミット時の自動型チェック、型エラーの早期発見、品質ゲートの設定を行います。

## 現状分析

### 現在の課題
- 型チェックが開発者の手動実行に依存
- コードレビュー時の型安全性チェック不足
- 型エラーの本番環境での発見リスク
- 品質基準の自動化不足

### 改善目標
- 型チェックの完全自動化
- プルリクエスト時の品質ゲート設定
- 型エラーの早期発見と通知
- 開発効率の向上

## 要件定義

### 機能要件
- [ ] CI/CDパイプラインでの自動型チェック
- [ ] プルリクエスト時の型安全性検証
- [ ] 型チェック結果の可視化とレポート
- [ ] 型エラー発生時の自動通知機能

### 非機能要件
- [ ] CI/CD実行時間の最適化（5分以内）
- [ ] 並列実行によるパフォーマンス向上
- [ ] 失敗時の詳細な診断情報提供
- [ ] 開発者フレンドリーなエラー報告

### 制約事項
- GitHub Actions の使用制限内での実装
- 既存のCI/CDワークフローとの統合
- セキュリティとコスト効率の両立

## 実装計画

### CI/CDファイル構成
```
.github/
├── workflows/
│   ├── type-check.yml
│   ├── type-check-pr.yml
│   └── type-coverage.yml
├── actions/
│   └── setup-type-check/
│       ├── action.yml
│       └── setup.sh
└── dependabot.yml
```

### 修正方針

1. **段階的な型チェック実装**
   ```yaml
   # 基本的な型チェック
   - name: Basic Type Check
     run: mypy tradingagents/ --config-file mypy.ini
   
   # 厳密モード型チェック
   - name: Strict Type Check  
     run: mypy tradingagents/ --config-file mypy-strict.ini
   ```

2. **プルリクエスト品質ゲート**
   ```yaml
   # PRでの必須チェック
   - name: Type Safety Gate
     run: |
       if ! mypy tradingagents/ --config-file mypy.ini; then
         echo "Type check failed - PR cannot be merged"
         exit 1
       fi
   ```

3. **並列実行による高速化**
   ```yaml
   strategy:
     matrix:
       module: [dataflows, agents, graph, cli]
   steps:
     - name: Type Check ${{ matrix.module }}
       run: mypy tradingagents/${{ matrix.module }}/ --config-file mypy.ini
   ```

### 見積もり工数
- CI/CD設計: 1日
- ワークフロー実装: 1.5日
- テスト・調整: 1日
- ドキュメント: 0.5日
- **合計: 4日**

## 受け入れ条件

- [ ] CI/CDパイプラインで型チェックが自動実行される
- [ ] プルリクエスト時の品質ゲートが機能する
- [ ] 型チェック実行時間が5分以内に収まる
- [ ] 型エラー発生時の通知機能が動作する
- [ ] 型カバレッジレポートが自動生成される

## Todoリスト

### Phase 1: CI/CD基盤設計
- [ ] GitHub Actions ワークフロー設計
- [ ] 型チェック実行戦略の決定
- [ ] 並列実行とキャッシュ戦略の設計
- [ ] エラーハンドリングとレポート戦略の設計

### Phase 2: 基本ワークフロー実装
- [ ] type-check.yml の実装（メインブランチ用）
- [ ] type-check-pr.yml の実装（PR用）
- [ ] setup-type-check アクションの実装
- [ ] 依存関係キャッシュの設定

### Phase 3: 品質ゲート設定
- [ ] PRマージ条件の設定
- [ ] 型チェック失敗時のブロック機能
- [ ] 型カバレッジしきい値の設定
- [ ] ブランチ保護ルールの設定

### Phase 4: パフォーマンス最適化
- [ ] 並列実行による高速化
- [ ] 依存関係キャッシュの最適化
- [ ] 増分型チェックの実装
- [ ] 不要なチェックの除外

### Phase 5: 通知とレポート機能
- [ ] Slack/Discord通知の設定
- [ ] 型チェック結果のPRコメント機能
- [ ] 型カバレッジレポートの生成
- [ ] 型エラートレンドの可視化

### Phase 6: 開発者支援機能
- [ ] pre-commit hookの設定
- [ ] ローカル開発環境の型チェック設定
- [ ] VS Code設定の自動化
- [ ] 型エラー修正支援ツールの統合

### Phase 7: 監視と改善
- [ ] CI/CDメトリクスの収集
- [ ] 型チェック実行時間の監視
- [ ] 型エラー発生頻度の分析
- [ ] 継続的な改善プロセス確立

## 依存関係

### 前提条件
- **009_testing_strategy.md**: 型チェックテスト環境の整備
- **001-008**: 全ての型改修チケットの完了

### 影響を与えるチケット
- 今後の開発プロセス全体

### 外部依存
- GitHub Actions または同等のCI/CDサービス
- mypy, pytest などのツール

## 優先度: Low

### 根拠
- 品質保証の自動化に重要だが、他の修正完了後の実装
- 開発効率の長期的向上に寄与
- 型安全性の継続的保証に不可欠
- プロジェクトの成熟度向上に貢献

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| CI/CD実行時間の増加 | 中 | 中 | 並列実行とキャッシュ最適化 |
| GitHub Actions制限 | 中 | 低 | 効率的なワークフロー設計 |
| 開発フローの混乱 | 高 | 低 | 段階的導入と教育 |
| 偽陽性エラーの発生 | 低 | 中 | 適切な設定と例外処理 |

## 技術仕様

### メインワークフロー

```yaml
# .github/workflows/type-check.yml
name: Type Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  type-check:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    strategy:
      matrix:
        python-version: ['3.13']
        module: ['dataflows', 'agents', 'graph', 'cli']
      fail-fast: false
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
        
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install mypy pytest pytest-mypy types-requests
        
    - name: Cache mypy
      uses: actions/cache@v3
      with:
        path: .mypy_cache
        key: ${{ runner.os }}-mypy-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}
        
    - name: Type check ${{ matrix.module }}
      run: |
        mypy tradingagents/${{ matrix.module }}/ \
          --config-file tests/mypy_config/mypy.ini \
          --cache-dir .mypy_cache
          
    - name: Upload type check results
      if: failure()
      uses: actions/upload-artifact@v3
      with:
        name: type-errors-${{ matrix.module }}
        path: mypy-report.txt
```

### プルリクエスト品質ゲート

```yaml
# .github/workflows/type-check-pr.yml
name: PR Type Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  pr-type-gate:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      checks: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
        cache: 'pip'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install mypy pytest types-requests
        
    - name: Get changed files
      id: changed-files
      uses: tj-actions/changed-files@v40
      with:
        files: '**/*.py'
        
    - name: Type check changed files
      if: steps.changed-files.outputs.any_changed == 'true'
      run: |
        echo "Changed Python files:"
        echo "${{ steps.changed-files.outputs.all_changed_files }}"
        
        # 変更されたファイルのみ型チェック
        mypy ${{ steps.changed-files.outputs.all_changed_files }} \
          --config-file tests/mypy_config/mypy.ini \
          --show-error-codes \
          --pretty > mypy-results.txt 2>&1
        
    - name: Comment PR with results
      if: failure()
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const mypyResults = fs.readFileSync('mypy-results.txt', 'utf8');
          
          const comment = `## 🚨 Type Check Failed
          
          The following type errors were found in your changes:
          
          \`\`\`
          ${mypyResults}
          \`\`\`
          
          Please fix these type errors before merging.
          
          ---
          <sub>🤖 This comment was generated automatically by the Type Check workflow.</sub>`;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

### 型カバレッジレポート

```yaml
# .github/workflows/type-coverage.yml
name: Type Coverage

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # 毎日2時に実行

jobs:
  coverage:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
        cache: 'pip'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install mypy
        
    - name: Generate type coverage report
      run: |
        python tests/type_coverage/measure_coverage.py > coverage-report.txt
        
    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      with:
        name: type-coverage-report
        path: coverage-report.txt
        
    - name: Create coverage badge
      run: |
        COVERAGE=$(python -c "
        import re
        with open('coverage-report.txt', 'r') as f:
            content = f.read()
        match = re.search(r'Overall Coverage: (\d+\.\d+)%', content)
        print(match.group(1) if match else '0')
        ")
        
        echo "COVERAGE=$COVERAGE" >> $GITHUB_ENV
        
    - name: Update README with coverage badge
      run: |
        sed -i "s/coverage-[0-9]*%-brightgreen/coverage-${COVERAGE}%-brightgreen/g" README.md
```

### カスタムアクション

```yaml
# .github/actions/setup-type-check/action.yml
name: 'Setup Type Check Environment'
description: 'Set up Python environment for type checking'
inputs:
  python-version:
    description: 'Python version to use'
    required: false
    default: '3.13'
  cache-key:
    description: 'Cache key for dependencies'
    required: false
    default: 'default'

runs:
  using: 'composite'
  steps:
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ inputs.python-version }}
        cache: 'pip'
        
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ inputs.cache-key }}-${{ hashFiles('**/requirements.txt') }}
        
    - name: Install type check dependencies
      shell: bash
      run: |
        pip install --upgrade pip
        pip install mypy pytest types-requests types-beautifulsoup4 types-tqdm
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

### Dependabot設定

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "maintainer-team"
    labels:
      - "dependencies"
      - "type-safety"
    
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    reviewers:
      - "maintainer-team"
    labels:
      - "ci-cd"
```

### 開発者向けpre-commit設定

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: system
        files: \.py$
        args: [--config-file=tests/mypy_config/mypy.ini]
        
      - id: type-coverage
        name: type-coverage-check
        entry: python
        language: system
        files: \.py$
        args: [tests/type_coverage/check_coverage.py]
        pass_filenames: false
```