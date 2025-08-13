# チケット007: データフローの型安全性改修

## 概要

TradingAgentsプロジェクトにおけるデータフロー層の型安全性を向上させます。現在、引数の型不一致、戻り値の型エラー、外部ライブラリの型スタブ不備などが16件発生しており、データ取得・処理の信頼性に影響を与えています。

## 現状分析

### 影響範囲
- **dataflows/interface.py**: 12件のエラー
- **dataflows/googlenews_utils.py**: 1件のエラー  
- **dataflows/stockstats_utils.py**: 1件のエラー
- **dataflows/reddit_utils.py**: 1件のエラー
- **dataflows/utils.py**: 1件のエラー

### 主要なエラーパターン

1. **引数の型不一致**
   ```python
   # 問題のあるコード
   file_path = join(cache_dir, filename)  # [arg-type] str | None -> str
   ```

2. **戻り値の型不一致**
   ```python
   # 問題のあるコード
   def get_YFin_data() -> str:
       return pd.DataFrame()  # [return-value] DataFrame -> str
   ```

3. **外部ライブラリの型スタブ不備**
   ```python
   # 問題のあるコード
   from bs4 import BeautifulSoup  # [import-untyped] missing stubs
   from tqdm import tqdm  # [import-untyped] missing stubs
   ```

4. **Union型の不安全な処理**
   ```python
   # 問題のあるコード
   data_frame.reset_index()  # [union-attr] DataFrame | None
   ```

## 要件定義

### 機能要件
- [ ] 全データフロー関数の型安全性確保
- [ ] 外部ライブラリとの型安全な統合
- [ ] エラーハンドリングの型安全性向上
- [ ] キャッシュシステムの型安全化

### 非機能要件
- [ ] 既存のデータ処理APIの互換性維持
- [ ] パフォーマンスの劣化防止
- [ ] データ品質の維持
- [ ] 外部API制限の考慮

### 制約事項
- pandas、BeautifulSoup、tqdm等の外部依存関係
- FinnHub、Reddit等のAPI仕様との互換性
- 既存のキャッシュファイル形式の維持

## 実装計画

### 対象ファイル一覧
- `tradingagents/dataflows/interface.py`
- `tradingagents/dataflows/googlenews_utils.py`
- `tradingagents/dataflows/stockstats_utils.py` 
- `tradingagents/dataflows/reddit_utils.py`
- `tradingagents/dataflows/utils.py`

### 修正方針

1. **型スタブの追加とtype: ignoreの適切な使用**
   ```python
   # 型スタブが利用可能な場合
   from bs4 import BeautifulSoup  # type: ignore[import-untyped]
   from tqdm import tqdm  # type: ignore[import-untyped]
   
   # または requirements に型スタブを追加
   # types-beautifulsoup4, types-tqdm
   ```

2. **None安全なデータ処理**
   ```python
   def safe_dataframe_operation(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
       if df is not None:
           return df.reset_index()
       return None
   ```

3. **戻り値型の統一**
   ```python
   def get_financial_data(ticker: str) -> Union[pd.DataFrame, str]:
       """データまたはエラーメッセージを返す"""
       try:
           data = fetch_data(ticker)
           return data  # pd.DataFrame
       except Exception as e:
           return f"Error: {str(e)}"  # str
   ```

### 見積もり工数
- 調査・設計: 1日
- 実装: 2.5日
- テスト・検証: 1.5日
- **合計: 5日**

## 受け入れ条件

- [ ] データフロー関連の型エラー16件が全て解消される
- [ ] mypyで該当ファイルの型チェックが通過する
- [ ] 既存のデータ取得機能が正常動作する
- [ ] キャッシュ機能が正常に動作する
- [ ] エラーハンドリングが適切に機能する

## Todoリスト

### Phase 1: 外部ライブラリ対応
- [ ] 必要な型スタブパッケージの調査と追加
- [ ] BeautifulSoup4の型対応 (types-beautifulsoup4)
- [ ] tqdmの型対応 (types-tqdm)  
- [ ] 型スタブが無いライブラリのtype: ignore対応

### Phase 2: interface.py の型安全化
- [ ] join関数の引数null安全性確保（5箇所）
- [ ] get_YFin_data関数の戻り値型修正
- [ ] ファイルパス処理の型安全性改善
- [ ] エラーハンドリングの型安全化

### Phase 3: 各ユーティリティモジュールの修正
- [ ] googlenews_utils.pyのBeautifulSoup型対応
- [ ] stockstats_utils.pyのDataFrame null安全性
- [ ] reddit_utils.pyのOptional引数修正
- [ ] utils.pyのOptional引数修正

### Phase 4: データ処理の型安全化
- [ ] pandas DataFrame操作の null安全性確保
- [ ] JSONデータ処理の型安全性向上
- [ ] ファイルIO操作の型安全化
- [ ] キャッシュ操作の型安全化

### Phase 5: エラーハンドリング改善
- [ ] 型安全なエラー情報の伝達
- [ ] データ検証の型安全性確保
- [ ] 例外処理の型注釈追加
- [ ] ログ出力の型安全化

### Phase 6: テストと検証
- [ ] データフロー処理のユニットテスト
- [ ] 統合テスト（実際のAPI呼び出し）
- [ ] エラーケースのテスト
- [ ] パフォーマンステスト

### Phase 7: ドキュメント整備
- [ ] データフローAPIドキュメント更新
- [ ] 型安全なデータ処理ガイド作成
- [ ] エラーハンドリングのベストプラクティス
- [ ] 外部ライブラリ統合ガイド

## 依存関係

### 前提条件
- **001_date_type_safety.md**: 日付処理の型安全性
- **003_function_annotations.md**: 基本的な型注釈標準

### 影響を与えるチケット
- **004_yfinance_wrapper.md**: YFinance統合
- **008_memory_types.md**: データキャッシュとの統合

### 外部依存
- 型スタブパッケージの追加
- 外部API仕様との互換性維持

## 優先度: High

### 根拠
- データ取得・処理の中核機能
- 16件のエラーによる影響範囲の広さ
- 外部APIとの統合における信頼性
- 実行時エラーの防止

## リスク評価

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| 外部ライブラリ互換性 | 中 | 低 | バージョン固定とテスト |
| データ処理性能劣化 | 中 | 低 | 効率的な型チェック |
| API制限への影響 | 低 | 低 | 既存制限機能の維持 |
| キャッシュ機能の破綻 | 中 | 低 | 段階的移行とテスト |

## 技術仕様

### データフロー型定義

```python
from typing import TypedDict, Optional, Union, Dict, Any, List
from datetime import datetime
import pandas as pd

# データ型定義
class MarketData(TypedDict):
    ticker: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class NewsItem(TypedDict):
    title: str
    content: str
    published: datetime
    source: str
    sentiment: Optional[float]

class CompanyInfo(TypedDict):
    ticker: str
    name: str
    sector: str
    industry: str
    market_cap: Optional[float]

# データソース結果型
DataResult = Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
```

### 型安全なデータアクセス

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class DataProvider(Protocol):
    def get_stock_data(
        self, 
        ticker: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Optional[pd.DataFrame]:
        """株価データを取得"""
        
    def get_news_data(
        self,
        query: str,
        limit: int = 10
    ) -> List[NewsItem]:
        """ニュースデータを取得"""

class SafeDataInterface:
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir or "/tmp/trading_cache"
    
    def safe_get_data(
        self,
        provider: DataProvider,
        operation: str,
        **kwargs
    ) -> Optional[DataResult]:
        """型安全なデータ取得の共通インターフェース"""
        try:
            method = getattr(provider, operation)
            return method(**kwargs)
        except Exception as e:
            self._log_error(f"Data fetch error: {e}")
            return None
    
    def _safe_join_path(self, *parts: Optional[str]) -> Optional[str]:
        """null安全なパス結合"""
        clean_parts = [p for p in parts if p is not None]
        if not clean_parts:
            return None
        return os.path.join(*clean_parts)
```

### エラーハンドリングパターン

```python
from dataclasses import dataclass
from enum import Enum

class DataError(Enum):
    NETWORK_ERROR = "network_error"
    PARSE_ERROR = "parse_error"
    CACHE_ERROR = "cache_error"
    VALIDATION_ERROR = "validation_error"

@dataclass
class DataOperationResult:
    success: bool
    data: Optional[DataResult] = None
    error: Optional[DataError] = None
    message: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        return self.success and self.data is not None

def safe_data_operation(operation: Callable) -> DataOperationResult:
    """データ操作の安全な実行"""
    try:
        result = operation()
        return DataOperationResult(success=True, data=result)
    except NetworkException as e:
        return DataOperationResult(
            success=False, 
            error=DataError.NETWORK_ERROR,
            message=str(e)
        )
    except Exception as e:
        return DataOperationResult(
            success=False,
            error=DataError.PARSE_ERROR,
            message=str(e)
        )
```

### 外部ライブラリ統合

```python
# requirements.txt に追加
# types-beautifulsoup4
# types-tqdm
# types-requests

# 型安全なライブラリ使用
try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag, NavigableString
except ImportError:
    BeautifulSoup = None  # type: ignore
    
def safe_parse_html(html: str) -> Optional[Dict[str, Any]]:
    """型安全なHTML解析"""
    if BeautifulSoup is None:
        return None
        
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    
    # 型安全な要素アクセス
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "No title"
    
    return {"title": title, "content": soup.get_text()}
```