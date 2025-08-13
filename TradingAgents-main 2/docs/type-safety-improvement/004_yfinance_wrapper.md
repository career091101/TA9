# チケット004: YFinanceラッパーの型安全性改修

## 概要

TradingAgentsプロジェクトにおけるYFinanceラッパー(`YFinanceUtils`クラス)の型エラーを修正し、型安全な金融データアクセスを実現します。現在21件のエラーが発生しており、主にself引数の欠如とライブラリスタブの不備が原因です。

## 現状分析

### 影響範囲
- **dataflows/yfin_utils.py**: 19件のエラー
- **dataflows/stockstats_utils.py**: 2件のエラー

### 主要なエラーパターン

1. **self引数の欠如 (8箇所)**
   ```python
   # 問題のあるコード
   def get_stock_data(ticker: str):  # [misc] self missing
   
   # 修正後
   def get_stock_data(self, ticker: str):
   ```

2. **str型に対する不正な属性アクセス**
   ```python
   # 問題のあるコード  
   ticker_obj = ticker  # str型
   data = ticker_obj.history()  # [attr-defined] error
   
   # 修正後
   ticker_obj = yf.Ticker(ticker)  # yf.Ticker型
   data = ticker_obj.history()
   ```

3. **型スタブの不備**
   ```python
   import yfinance  # [import-untyped] missing stubs
   ```

## 要件定義

### 機能要件
- [ ] YFinanceUtilsクラスの完全な型安全化
- [ ] 全メソッドの適切な型注釈付与
- [ ] yfinanceライブラリとの型安全な統合
- [ ] エラーハンドリングの型安全性確保

### 非機能要件
- [ ] 既存のデータ取得APIの互換性維持
- [ ] パフォーマンスの劣化なし
- [ ] yfinanceライブラリバージョンとの互換性
- [ ] pandas DataFrameとの統合維持

### 制約事項
- yfinance 0.2.x との互換性
- pandas 2.x との互換性
- 既存のキャッシュ機能の維持

## 実装計画

### 対象ファイル一覧
- `tradingagents/dataflows/yfin_utils.py`
- `tradingagents/dataflows/stockstats_utils.py`
- `tradingagents/dataflows/interface.py` (YFinance関連部分)

### 修正方針

1. **クラス定義の修正**
   ```python
   import yfinance as yf
   from typing import Optional, Union, Dict, Any
   import pandas as pd
   
   class YFinanceUtils:
       def __init__(self):
           pass
           
       def get_stock_data(
           self, 
           ticker: str, 
           period: str = "1y",
           save_path: Optional[str] = None
       ) -> Optional[pd.DataFrame]:
   ```

2. **yfinance.Tickerの正しい使用**
   ```python
   def get_stock_info(self, ticker: str) -> Optional[Dict[str, Any]]:
       try:
           ticker_obj = yf.Ticker(ticker)
           return ticker_obj.info
       except Exception as e:
           logger.error(f"Failed to get stock info for {ticker}: {e}")
           return None
   ```

3. **型スタブの対応**
   ```python
   try:
       import yfinance as yf
   except ImportError:
       raise ImportError("yfinance is required but not installed")
   
   # type: ignore を適切に使用
   from yfinance import Ticker  # type: ignore[import-untyped]
   ```

### 見積もり工数
- 設計・調査: 0.5日
- 実装: 2日
- テスト・検証: 1日
- ドキュメント: 0.5日
- **合計: 4日**

## 受け入れ条件

- [ ] YFinance関連の型エラー21件が全て解消される
- [ ] mypyで該当ファイルの型チェックが通過する
- [ ] 既存の金融データ取得機能が正常動作する
- [ ] エラーハンドリングが適切に機能する
- [ ] パフォーマンステストが通過する

## Todoリスト

### Phase 1: 設計と調査
- [ ] yfinanceライブラリの型情報調査
- [ ] 既存のYFinanceUtils使用パターン分析
- [ ] エラーハンドリング戦略の設計
- [ ] データ型の統一方針決定

### Phase 2: 基盤修正
- [ ] YFinanceUtilsクラスの基本構造修正
- [ ] 共通的なエラーハンドリング実装
- [ ] 型安全なヘルパー関数作成
- [ ] ログ機能の型安全な統合

### Phase 3: メソッド別修正
- [ ] get_stock_data メソッド修正
- [ ] get_stock_info メソッド修正
- [ ] get_company_info メソッド修正
- [ ] get_stock_dividends メソッド修正
- [ ] get_income_stmt メソッド修正
- [ ] get_balance_sheet メソッド修正
- [ ] get_cash_flow メソッド修正
- [ ] get_analyst_recommendations メソッド修正

### Phase 4: StockStats連携修正
- [ ] stockstats_utils.py の型エラー修正
- [ ] pandasとyfinanceの型統一
- [ ] データフォーマット変換の型安全化
- [ ] インデックス処理の型安全化

### Phase 5: エラーハンドリング強化
- [ ] ネットワークエラーの型安全な処理
- [ ] データ形式エラーの処理
- [ ] APIレート制限の処理
- [ ] 無効ティッカーシンボルの処理

### Phase 6: テストと検証
- [ ] 単体テストの型安全性確認
- [ ] 統合テストの実行
- [ ] エラーケースのテスト
- [ ] パフォーマンステスト

### Phase 7: ドキュメント整備
- [ ] YFinanceラッパー利用ガイド作成
- [ ] エラーハンドリングのドキュメント
- [ ] APIリファレンス更新

## 依存関係

### 前提条件
- **003_function_annotations.md**: 型注釈標準の確立

### 影響を与えるチケット
- **001_date_type_safety.md**: 日付処理との統合
- **007_dataflow_types.md**: データフロー全体の型安全性

### 外部依存
- yfinanceライブラリの型スタブ
- pandasの型定義

## 優先度: High

### 根拠
- 金融データ取得の中核機能
- 21件と高いエラー数
- 実行時エラーの高リスク
- 他のデータ分析モジュールへの影響

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| yfinanceライブラリ変更 | 高 | 中 | バージョン固定と互換性テスト |
| データ取得失敗の増加 | 中 | 低 | ロバストなエラーハンドリング |
| パフォーマンス劣化 | 中 | 低 | 効率的な型チェック実装 |
| API制限への影響 | 低 | 低 | 既存の制限処理維持 |

## 技術仕様

### YFinanceUtils型定義

```python
from typing import Optional, Dict, Any, List, Union
import pandas as pd
import yfinance as yf
from datetime import datetime

class YFinanceUtils:
    """型安全なYFinanceラッパークラス"""
    
    def get_stock_data(
        self,
        ticker: str,
        period: str = "1y", 
        interval: str = "1d",
        save_path: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """株価データを型安全に取得"""
        
    def get_stock_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """企業情報を型安全に取得"""
        
    def get_financial_data(
        self, 
        ticker: str, 
        statement_type: str
    ) -> Optional[pd.DataFrame]:
        """財務データを型安全に取得"""
```

### エラーハンドリングパターン

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Union

class YFinanceError(Enum):
    INVALID_TICKER = "invalid_ticker"
    NETWORK_ERROR = "network_error"
    DATA_FORMAT_ERROR = "data_format_error"
    RATE_LIMIT = "rate_limit"

@dataclass
class YFinanceResult:
    data: Optional[Union[pd.DataFrame, Dict[str, Any]]]
    error: Optional[YFinanceError]
    message: Optional[str]
    
    @property
    def is_success(self) -> bool:
        return self.error is None and self.data is not None
```

### 型安全な使用例

```python
# 推奨パターン
utils = YFinanceUtils()
result = utils.get_stock_data("AAPL")

if result is not None:
    # pandas DataFrameとして安全に使用
    print(result.head())
else:
    # エラーハンドリング
    logger.warning("Failed to get stock data")

# 避けるべきパターン  
data = ticker_str.history()  # str型にhistory()メソッドは存在しない
```