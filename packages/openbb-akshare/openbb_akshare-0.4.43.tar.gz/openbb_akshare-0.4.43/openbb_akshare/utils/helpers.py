"""AKShare helpers module."""

# pylint: disable=unused-argument,too-many-arguments,too-many-branches,too-many-locals,too-many-statements
from typing import Dict, Any, List, Optional, Union
import pandas as pd
from openbb_core.provider.utils.errors import EmptyDataError
from openbb_yfinance.utils.references import INTERVALS, MONTHS, PERIODS
from pandas import DataFrame
from datetime import (
    date as dateType,
    datetime,
)
from .tools import normalize_date, normalize_symbol
import akshare as ak

import logging
from openbb_akshare.utils.tools import setup_logger, normalize_symbol

#setup_logger()
logger = logging.getLogger(__name__)

EQUITY_HISTORY_SCHEMA = {
    "date": "TEXT PRIMARY KEY",
    "open": "REAL",
    "high": "REAL",
    "low": "REAL",
    "close": "REAL",
    "volume": "REAL",
    "vwap": "REAL",
    "change": "REAL",
    "change_percent": "REAL",
    "amount": "REAL"
}

def ak_download_without_cache(
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "",
    ) -> DataFrame:

    symbol_b, symbol_f, market = normalize_symbol(symbol)
    if market == "HK":
        hist_df = ak.stock_hk_hist(symbol_b, period, start_date, end_date, adjust="")
        hist_df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume", "成交额": "amount", "涨跌幅":"change_percent", "涨跌额": "change"}, inplace=True)
        hist_df = hist_df.drop(columns=["振幅"])
        hist_df = hist_df.drop(columns=["换手率"])
    else:
        hist_df = ak.stock_zh_a_hist(symbol_b, period, start_date, end_date, adjust="")
    
        hist_df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume", "成交额": "amount", "涨跌幅":"change_percent", "涨跌额": "change"}, inplace=True)
        hist_df = hist_df.drop(columns=["股票代码"])
        hist_df = hist_df.drop(columns=["振幅"])
        hist_df = hist_df.drop(columns=["换手率"])

    return hist_df


def ak_download_with_cache(
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "",
    ) -> DataFrame:
    """
    Retrieves historical equity data from a cache or downloads it from a remote source.
    
    Handles:
        - Non-dividend cases (return 0)
        - Per-share direct values (e.g., "每股0.38港元")
        - Base-share values (e.g., "10派1元")
        - Complex combinations (e.g., "每股派发现金股利0.088332港元,每10股派送股票股利3股")

    Parameters:
        symbol (str): Stock symbol to fetch data for.
        start_date (str): Start date for fetching data in 'YYYYMMDD' format.
        end_date (str): End date for fetching data in 'YYYYMMDD' format.
        period (str): Data frequency, e.g., "daily", "weekly", "monthly".
        adjust (str): Adjustment type, e.g., "qfq" for forward split, "hfq" for backward split.

    Returns:
        DataFrame: DataFrame containing historical equity data.
    """
    from openbb_akshare.utils.equity_cache import EquityCache
    from openbb_akshare.utils.helpers import EQUITY_HISTORY_SCHEMA
    from openbb_akshare.utils.fetch_equity_info import fetch_equity_info

    # Retrieve data from cache first
    symbol_b, symbol_f, market = normalize_symbol(symbol)
    cache = EquityCache(EQUITY_HISTORY_SCHEMA, table_name=f"{market}{symbol_b}")
    start_dt = datetime.strptime(start_date, "%Y%m%d")
    end_dt = datetime.strptime(end_date, "%Y%m%d")

    start = start_dt.strftime("%Y-%m-%d")
    end = end_dt.strftime("%Y-%m-%d")
    data_from_cache = cache.fetch_date_range(start, end)
    if not data_from_cache.empty:
        return data_from_cache

    # If not in cache, download data
    equity_info = fetch_equity_info(symbol_b)
    listed_date = pd.to_datetime(equity_info["listed_date"], unit='ms')
    
    first_stock_price_date = listed_date.iloc[0].strftime('%Y%m%d')
    today = datetime.now().date().strftime("%Y%m%d")
    # Download data using AKShare
    data_util_today_df = ak_download_without_cache(symbol=symbol_b, period=period, start_date=first_stock_price_date, end_date=today, adjust="")
    cache.write_dataframe(data_util_today_df)
    
    return cache.fetch_date_range(start, end)

def ak_download(
        symbol: str,
        start_date: dateType,
        end_date: dateType,
        period: str = "daily",
        use_cache: Optional[bool] = True,
        adjust: str = "",
    ) -> DataFrame:

    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")
    if use_cache:
        return ak_download_with_cache(symbol, start, end, period, adjust)
    
    result = ak_download_without_cache(symbol, start, end, period, adjust)

    return result


def get_post_tax_dividend_per_share(dividend_str: str) -> float:
    """
    Parses Chinese dividend descriptions and returns post-tax dividend per share.
    
    Handles:
        - Non-dividend cases (return 0)
        - Per-share direct values (e.g., "每股0.38港元")
        - Base-share values (e.g., "10派1元")
        - Complex combinations (e.g., "每股派发现金股利0.088332港元,每10股派送股票股利3股")

    Parameters:
        dividend_str (str): Dividend description string

    Returns:
        float: Post-tax dividend amount per share, rounded to 4 decimal places
    """
    import re

    # Case 1: Non-dividend cases
    if re.search(r'不分红|不分配不转增|转增.*不分配', dividend_str):
        return 0.0
    
    # If A股 is present, extract only that part
    a_share_match = re.search(r'(A股[^,]*)', dividend_str)
    if a_share_match:
        dividend_str = a_share_match.group(1)
    # Remove 'A股' prefix if present
    dividend_str = dividend_str.replace('A股', '')

     # Extract base shares
    base_match = re.match(r'(\d+(?:\.\d+)?)', dividend_str)
    base = float(base_match.group(1)) if base_match else 0.0

    # Extract bonus shares (送)
    bonus_match = re.search(r'送(\d+(?:\.\d+)?)股', dividend_str)
    bonus = float(bonus_match.group(1)) if bonus_match else 0.0

    # Extract conversion shares (转)
    conversion_match = re.search(r'转(\d+(?:\.\d+)?)股', dividend_str)
    conversion = float(conversion_match.group(1)) if conversion_match else 0.0

    # Extract cash dividend (派)
    cash_match = re.search(r'派(\d+(?:\.\d+)?)元', dividend_str)
    cash = float(cash_match.group(1)) if cash_match else 0.0

    if base != 0 and cash != 0:
        return round(cash / base, 4)
       
    # Case 2: Direct per-share values (e.g., "每股0.38港元", "每股人民币0.25元")
    direct_match = re.search(r'每股[\u4e00-\u9fa5]*([\d\.]+)[^\d]*(?:港元|人民币|元)', dividend_str)
    if direct_match:
        return round(float(direct_match.group(1)), 4)
    
    # Case 3: Base-share values (e.g., "10派1元", "10转10股派1元")
    # Match "10转10股派1元" or similar
    match = re.match(r'(\d+)转(\d+)股派([\d\.]+)元', dividend_str)
    if match:
        base = int(match.group(1))
        bonus = int(match.group(2))
        cash = float(match.group(3))
        total_shares = base
        return round(cash / total_shares, 4)
    # Handle "10派1元" or "10.00派2.00元"
    match = re.match(r'(\d+(?:\.\d+)?)派([\d\.]+)元', dividend_str)
    if match:
        base = int(float(match.group(1)))
        cash = float(match.group(2))
        return round(cash / base, 4)

    base_match = re.search(r'(\d+)(?:[转股]+[\d\.]+)*(?:派|现金股利)([\d\.]+)', dividend_str)
    if base_match:
        base_shares = int(float(base_match.group(1)))  # Handle '10.00' cases
        dividend_amount = float(base_match.group(2))
        return round(dividend_amount / base_shares, 4)
    
    # Case 4: Complex mixed formats (e.g., "每股派发现金股利0.088332港元,每10股派送股票股利3股")
    complex_match = re.search(r'每股[\u4e00-\u9fa5]*([\d\.]+)[^\d]*(?:港元|人民币|元)', dividend_str)
    if complex_match:
        return round(float(complex_match.group(1)), 4)
    
    # Default: Return 0 for unrecognized formats
    return 0.0
def get_a_dividends(
    symbol: str,
    start_date: Optional[Union[str, "date"]] = None,
    end_date: Optional[Union[str, "date"]] = None,
) -> List[Dict]:
    """
    Fetches historical dividends for a Shanghai/Shenzhen/Beijing stock symbol.

    Parameters:
        symbol (str): Stock symbol to fetch dividends for.
        start_date (Optional[Union[str, date]]): Start date for fetching dividends.
        end_date (Optional[Union[str, date]]): End date for fetching dividends.

    Returns:
        DataFrame: DataFrame containing dividend information.
    """
    import akshare as ak

    if not symbol:
        raise EmptyDataError("Symbol cannot be empty.")

    div_df = ak.stock_fhps_detail_ths(symbol)
    div_df.dropna(inplace=True)
    ticker = div_df[['实施公告日',
                        '分红方案说明',
                        'A股股权登记日',
                        'A股除权除息日']]
    ticker['amount'] = div_df['分红方案说明'].apply(
        lambda x: get_post_tax_dividend_per_share(x) if isinstance(x, str) else None
    )
    ticker.rename(columns={'实施公告日': "report_date",
                            '分红方案说明': "description", 
                            'A股股权登记日': "record_date",
                            'A股除权除息日': "ex_dividend_date"}, inplace=True)
    dividends = ticker.to_dict("records")  # type: ignore
    
    if not dividends:
        raise EmptyDataError(f"No dividend data found for {symbol}.")

    return dividends

def get_hk_dividends(
    symbol: str,
    start_date: Optional[Union[str, "date"]] = None,
    end_date: Optional[Union[str, "date"]] = None,
) -> List[Dict]:
    """
    Fetches historical dividends for a Hong Kong stock symbol.

    Parameters:
        symbol (str): Stock symbol to fetch dividends for.
        start_date (Optional[Union[str, date]]): Start date for fetching dividends.
        end_date (Optional[Union[str, date]]): End date for fetching dividends.

    Returns:
        DataFrame: DataFrame containing dividend information.
    """
    import akshare as ak

    if not symbol:
        raise EmptyDataError("Symbol cannot be empty.")

    div_df = ak.stock_hk_fhpx_detail_ths(symbol[1:])
    div_df.dropna(inplace=True)
    ticker = div_df[['公告日期',
                        '方案',
                        '除净日',
                        '派息日']]
    ticker['amount'] = div_df['方案'].apply(
        lambda x: get_post_tax_dividend_per_share(x) if isinstance(x, str) else None
    )
    ticker.rename(columns={'公告日期': "report_date",
                            '方案': "description", 
                            '除净日': "record_date",
                            '派息日': "ex_dividend_date"}, inplace=True)
    dividends = ticker.to_dict("records")  # type: ignore
    
    if not dividends:
        raise EmptyDataError(f"No dividend data found for {symbol}.")

    return dividends