# チケット004: YFinanceラッパーの型安全性改善

## 概要
YFinanceのラッパー関数でデコレータ使用時のself引数不足と、ticker変数の型不一致が発生している。適切な型定義とデコレータの修正を行う。

## 現状分析

### エラー件数
- **総エラー数**: 8件
- **主要エラー**: `[misc]` Self argument missing
- **影響ファイル**: `tradingagents/dataflows/yfin_utils.py`

### 主要な問題パターン
1. デコレータでtickerをstr型として渡しているが、yfinance.Tickerオブジェクトが必要
2. 非静的メソッドでself引数が不足
3. 戻り値の型がAnyになっている

### 問題のコード例
```python
# 現在の問題のあるコード
@yfinance_wrapper
def get_stock_data(symbol: str, ...):
    ticker.history(...)  # tickerはstr型として渡されている
```

## 要件定義

### 機能要件
- FR-001: YFinanceラッパーの型安全な実装
- FR-002: デコレータの適切な型定義
- FR-003: 戻り値の明確な型指定

### 非機能要件
- NFR-001: YFinance APIとの互換性維持
- NFR-002: エラーハンドリングの改善
- NFR-003: キャッシュ機能の保持

### 制約事項
- YFinance APIの仕様変更に対応
- 既存の関数インターフェース維持

## 実装計画

### 修正方針

#### 1. デコレータの修正
```python
import yfinance as yf
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
T = TypeVar('T')

def yfinance_wrapper(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(symbol: str, *args, **kwargs) -> T:
        ticker = yf.Ticker(symbol)
        # tickerオブジェクトを渡す
        return func(ticker, *args, **kwargs)
    return wrapper
```

#### 2. 関数の修正
```python
# 修正後
from typing import Optional
import pandas as pd
import yfinance as yf

@yfinance_wrapper
def get_stock_data(
    ticker: yf.Ticker,  # Tickerオブジェクトを受け取る
    start_date: str,
    end_date: str,
    save_path: Optional[str] = None
) -> pd.DataFrame:
    end_date_obj = pd.to_datetime(end_date) + pd.DateOffset(days=1)
    end_date_str = end_date_obj.strftime("%Y-%m-%d")
    stock_data = ticker.history(start=start_date, end=end_date_str)
    
    if save_path:
        save_data(stock_data, ticker.ticker, save_path)
    
    return stock_data
```

### 見積もり工数
- 分析: 0.5日
- 実装: 1日
- テスト: 0.5日
- **合計: 2日**

## 受け入れ条件

### 必須条件
- [ ] YFinance関連の型エラーが0件
- [ ] デコレータが正しく動作
- [ ] 既存の機能が維持されている

### 推奨条件
- [ ] エラーハンドリングの改善
- [ ] パフォーマンステスト実施

## Todoリスト

### 準備作業
- [ ] YFinance APIドキュメントの確認
- [ ] 現在の使用パターンの調査
- [ ] テストデータの準備

### 実装作業

#### yfinance_wrapperの修正
- [ ] デコレータの型定義修正
  - [ ] ParamSpecの導入
  - [ ] TypeVarの適切な使用
  - [ ] Tickerオブジェクトの生成
- [ ] エラーハンドリング追加
  - [ ] シンボル検証
  - [ ] API例外のキャッチ
  - [ ] リトライロジック

#### 各関数の修正
- [ ] get_stock_data関数
  - [ ] 引数の型修正
  - [ ] 戻り値の型明確化
  - [ ] 日付処理の型安全化
- [ ] get_stock_info関数
  - [ ] Tickerオブジェクトの使用
  - [ ] 戻り値の型定義
- [ ] get_company_info関数
  - [ ] 型注釈の追加
  - [ ] Optional型の適切な使用
- [ ] get_stock_dividends関数
  - [ ] 型安全な実装
  - [ ] エラーハンドリング

#### ヘルパー関数の型定義
- [ ] save_data関数の型注釈
- [ ] 内部ユーティリティの型定義

### テスト作業
- [ ] ユニットテストの作成
  - [ ] デコレータのテスト
  - [ ] 各関数のテスト
  - [ ] エラーケースのテスト
- [ ] 統合テストの実行
  - [ ] 実際のYFinance APIとの連携テスト
  - [ ] キャッシュ機能のテスト
- [ ] 型チェックの実行

### ドキュメント
- [ ] YFinanceラッパーの使用ガイド
- [ ] 型定義の説明
- [ ] エラーハンドリングの文書化

## 依存関係
- チケット001（日付処理の型安全性）の完了後が望ましい
- チケット007（データフローの型安全性）と関連

## 優先度
**High** - データ取得の中核機能

## リスクと対策

### リスク1: YFinance APIの変更
**対策**:
- バージョン固定
- 抽象化レイヤー
- 定期的な互換性テスト

### リスク2: ネットワークエラー
**対策**:
- リトライメカニズム
- タイムアウト設定
- フォールバック処理

### リスク3: データ型の不整合
**対策**:
- 厳密な型チェック
- データ検証
- 変換ユーティリティ

## 参考情報

### YFinance Ticker型の構造
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
# 利用可能なメソッド
ticker.history()  # 価格履歴
ticker.info      # 企業情報（辞書）
ticker.dividends # 配当情報
ticker.ticker    # シンボル文字列
```

### デコレータの型注釈パターン
```python
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

def my_decorator(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # 処理
        return func(*args, **kwargs)
    return wrapper
```

## 完了確認
- [ ] 全てのTodoが完了
- [ ] 型エラーが解消
- [ ] テストが全てパス
- [ ] コードレビュー完了
- [ ] ドキュメント更新完了