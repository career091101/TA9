# gets data/stats

import yfinance as yf
from typing import Annotated, Callable, Any, Optional, Dict, Union, Tuple
from pandas import DataFrame
import pandas as pd
from functools import wraps
from datetime import datetime

from .utils import save_output, SavePathType, decorate_all_methods
# Import type-safe date utilities
from ..utils.date_utils import parse_date, format_date, add_days

# Type aliases for better type safety
# Note: Using Any for yfinance.Ticker due to missing library stubs
DataFrameType = pd.DataFrame
StockInfoType = Dict[str, Any]


def init_ticker(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to initialize yf.Ticker and pass it to the function."""

    @wraps(func)
    def wrapper(self: 'YFinanceUtils', symbol: Annotated[str, "ticker symbol"], *args: Any, **kwargs: Any) -> Any:
        ticker: Any = yf.Ticker(symbol)  # Using Any due to missing yfinance stubs
        return func(self, ticker, *args, **kwargs)

    return wrapper


@decorate_all_methods(init_ticker)
class YFinanceUtils:

    def get_stock_data(
        self,
        ticker: Any,  # yf.Ticker, using Any due to missing stubs
        start_date: Annotated[
            str, "start date for retrieving stock price data, YYYY-mm-dd"
        ],
        end_date: Annotated[
            str, "end date for retrieving stock price data, YYYY-mm-dd"
        ],
        save_path: Optional[SavePathType] = None,
    ) -> DataFrameType:
        """retrieve stock price data for designated ticker symbol"""
        # add one day to the end_date so that the data range is inclusive
        end_date_dt: datetime = add_days(end_date, 1)
        end_date_formatted: str = format_date(end_date_dt)
        stock_data: DataFrameType = ticker.history(start=start_date, end=end_date_formatted)
        # save_output(stock_data, f"Stock data for {ticker.ticker}", save_path)
        return stock_data

    def get_stock_info(
        self,
        ticker: Any,  # yf.Ticker, using Any due to missing stubs
    ) -> StockInfoType:
        """Fetches and returns latest stock information."""
        stock_info: StockInfoType = ticker.info
        return stock_info

    def get_company_info(
        self,
        ticker: Any,  # yf.Ticker, using Any due to missing stubs
        save_path: Optional[str] = None,
    ) -> DataFrameType:
        """Fetches and returns company information as a DataFrame."""
        info: StockInfoType = ticker.info
        company_info: Dict[str, str] = {
            "Company Name": info.get("shortName", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Country": info.get("country", "N/A"),
            "Website": info.get("website", "N/A"),
        }
        company_info_df: DataFrameType = DataFrame([company_info])
        if save_path:
            company_info_df.to_csv(save_path)
            print(f"Company info for {ticker.ticker} saved to {save_path}")
        return company_info_df

    def get_stock_dividends(
        self,
        ticker: Any,  # yf.Ticker, using Any due to missing stubs
        save_path: Optional[str] = None,
    ) -> DataFrameType:
        """Fetches and returns the latest dividends data as a DataFrame."""
        dividends: DataFrameType = ticker.dividends
        if save_path:
            dividends.to_csv(save_path)
            print(f"Dividends for {ticker.ticker} saved to {save_path}")
        return dividends

    def get_income_stmt(self, ticker: Any) -> DataFrameType:  # yf.Ticker, using Any due to missing stubs
        """Fetches and returns the latest income statement of the company as a DataFrame."""
        income_stmt: DataFrameType = ticker.financials
        return income_stmt

    def get_balance_sheet(self, ticker: Any) -> DataFrameType:  # yf.Ticker, using Any due to missing stubs
        """Fetches and returns the latest balance sheet of the company as a DataFrame."""
        balance_sheet: DataFrameType = ticker.balance_sheet
        return balance_sheet

    def get_cash_flow(self, ticker: Any) -> DataFrameType:  # yf.Ticker, using Any due to missing stubs
        """Fetches and returns the latest cash flow statement of the company as a DataFrame."""
        cash_flow: DataFrameType = ticker.cashflow
        return cash_flow

    def get_analyst_recommendations(self, ticker: Any) -> Tuple[Optional[str], Union[int, float]]:  # yf.Ticker, using Any due to missing stubs
        """Fetches the latest analyst recommendations and returns the most common recommendation and its count."""
        recommendations: DataFrameType = ticker.recommendations
        if recommendations.empty:
            return None, 0  # No recommendations available

        # Assuming 'period' column exists and needs to be excluded
        row_0: pd.Series = recommendations.iloc[0, 1:]  # Exclude 'period' column if necessary

        # Find the maximum voting result
        max_votes: Union[int, float] = row_0.max()
        majority_voting_result: list = row_0[row_0 == max_votes].index.tolist()

        return majority_voting_result[0], max_votes
