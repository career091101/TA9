"""
Utilities for type-safe date handling in TradingAgents.

This module provides type-safe date conversion and manipulation functions
to ensure consistent handling of datetime and string types throughout the system.
"""

from datetime import datetime, timedelta
from typing import Union, List, Optional, Iterator
from dateutil.relativedelta import relativedelta
import pandas as pd

# Type alias for date inputs
DateType = Union[str, datetime, pd.Timestamp]


def parse_date(date_input: str, format_str: str = "%Y-%m-%d") -> datetime:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_input: Date string to parse
        format_str: Format string for parsing (default: "%Y-%m-%d")
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If date string cannot be parsed
    """
    if not isinstance(date_input, str):
        raise TypeError(f"Expected str, got {type(date_input)}")
    
    try:
        return datetime.strptime(date_input, format_str)
    except ValueError as e:
        raise ValueError(f"Unable to parse date '{date_input}' with format '{format_str}': {e}")


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object into a string.
    
    Args:
        date_obj: Datetime object to format
        format_str: Format string for output (default: "%Y-%m-%d")
        
    Returns:
        str: Formatted date string
        
    Raises:
        TypeError: If input is not a datetime object
    """
    if not isinstance(date_obj, datetime):
        raise TypeError(f"Expected datetime, got {type(date_obj)}")
    
    return date_obj.strftime(format_str)


def ensure_datetime(date_input: DateType, format_str: str = "%Y-%m-%d") -> datetime:
    """
    Convert various date types to datetime object.
    
    Args:
        date_input: Date in string, datetime, or pandas Timestamp format
        format_str: Format string for string parsing (default: "%Y-%m-%d")
        
    Returns:
        datetime: Converted datetime object
        
    Raises:
        TypeError: If input type is not supported
        ValueError: If string cannot be parsed
    """
    if isinstance(date_input, datetime):
        return date_input
    elif isinstance(date_input, str):
        return parse_date(date_input, format_str)
    elif isinstance(date_input, pd.Timestamp):
        return date_input.to_pydatetime()
    else:
        raise TypeError(f"Unsupported date type: {type(date_input)}")


def ensure_string(date_input: DateType, format_str: str = "%Y-%m-%d") -> str:
    """
    Convert various date types to string.
    
    Args:
        date_input: Date in string, datetime, or pandas Timestamp format
        format_str: Format string for output (default: "%Y-%m-%d")
        
    Returns:
        str: Formatted date string
        
    Raises:
        TypeError: If input type is not supported
        ValueError: If datetime conversion fails
    """
    if isinstance(date_input, str):
        # Validate the string by parsing and reformatting
        parsed = parse_date(date_input, format_str)
        return format_date(parsed, format_str)
    elif isinstance(date_input, datetime):
        return format_date(date_input, format_str)
    elif isinstance(date_input, pd.Timestamp):
        return format_date(date_input.to_pydatetime(), format_str)
    else:
        raise TypeError(f"Unsupported date type: {type(date_input)}")


def date_range(
    start_date: DateType,
    end_date: DateType,
    step: int = 1,
    format_str: str = "%Y-%m-%d"
) -> List[str]:
    """
    Generate a list of date strings between start and end dates.
    
    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive) 
        step: Number of days between dates (default: 1)
        format_str: Format string for output (default: "%Y-%m-%d")
        
    Returns:
        List[str]: List of formatted date strings
        
    Raises:
        ValueError: If start_date is after end_date
    """
    start_dt = ensure_datetime(start_date, format_str)
    end_dt = ensure_datetime(end_date, format_str)
    
    if start_dt > end_dt:
        raise ValueError(f"Start date {start_dt} is after end date {end_dt}")
    
    dates = []
    current_dt = start_dt
    
    while current_dt <= end_dt:
        dates.append(format_date(current_dt, format_str))
        current_dt += timedelta(days=step)
    
    return dates


def add_days(date_input: DateType, days: int, format_str: str = "%Y-%m-%d") -> datetime:
    """
    Add days to a date.
    
    Args:
        date_input: Input date
        days: Number of days to add (can be negative)
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        datetime: New datetime object
    """
    date_obj = ensure_datetime(date_input, format_str)
    return date_obj + timedelta(days=days)


def subtract_days(date_input: DateType, days: int, format_str: str = "%Y-%m-%d") -> datetime:
    """
    Subtract days from a date.
    
    Args:
        date_input: Input date
        days: Number of days to subtract
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        datetime: New datetime object
    """
    date_obj = ensure_datetime(date_input, format_str)
    return date_obj - timedelta(days=days)


def add_business_days(
    date_input: DateType, 
    business_days: int, 
    format_str: str = "%Y-%m-%d"
) -> datetime:
    """
    Add business days to a date (skipping weekends).
    
    Args:
        date_input: Input date
        business_days: Number of business days to add
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        datetime: New datetime object
    """
    date_obj = ensure_datetime(date_input, format_str)
    
    if business_days >= 0:
        days_added = 0
        current_date = date_obj
        
        while days_added < business_days:
            current_date += timedelta(days=1)
            # Monday=0, Sunday=6
            if current_date.weekday() < 5:  # Monday to Friday
                days_added += 1
    else:
        days_added = 0
        current_date = date_obj
        
        while days_added > business_days:
            current_date -= timedelta(days=1)
            if current_date.weekday() < 5:  # Monday to Friday
                days_added -= 1
    
    return current_date


def get_trading_days_between(
    start_date: DateType,
    end_date: DateType,
    format_str: str = "%Y-%m-%d"
) -> List[str]:
    """
    Get trading days (weekdays) between two dates.
    
    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
        format_str: Format string for parsing/output (default: "%Y-%m-%d")
        
    Returns:
        List[str]: List of trading day strings
    """
    start_dt = ensure_datetime(start_date, format_str)
    end_dt = ensure_datetime(end_date, format_str)
    
    trading_days = []
    current_date = start_dt
    
    while current_date <= end_dt:
        # Monday=0, Sunday=6, so weekdays are 0-4
        if current_date.weekday() < 5:
            trading_days.append(format_date(current_date, format_str))
        current_date += timedelta(days=1)
    
    return trading_days


def is_business_day(date_input: DateType, format_str: str = "%Y-%m-%d") -> bool:
    """
    Check if a date is a business day (Monday-Friday).
    
    Args:
        date_input: Date to check
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        bool: True if business day, False otherwise
    """
    date_obj = ensure_datetime(date_input, format_str)
    return date_obj.weekday() < 5


def calculate_date_difference(
    date1: DateType,
    date2: DateType,
    format_str: str = "%Y-%m-%d"
) -> int:
    """
    Calculate the difference in days between two dates.
    
    Args:
        date1: First date
        date2: Second date  
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        int: Number of days (date2 - date1)
    """
    dt1 = ensure_datetime(date1, format_str)
    dt2 = ensure_datetime(date2, format_str)
    
    return (dt2 - dt1).days


def normalize_date_to_utc(date_input: DateType, format_str: str = "%Y-%m-%d") -> pd.Timestamp:
    """
    Convert date to pandas Timestamp with UTC timezone.
    
    Args:
        date_input: Input date
        format_str: Format string for parsing strings (default: "%Y-%m-%d")
        
    Returns:
        pd.Timestamp: Normalized timestamp with UTC timezone
    """
    date_obj = ensure_datetime(date_input, format_str)
    return pd.to_datetime(date_obj, utc=True).normalize()