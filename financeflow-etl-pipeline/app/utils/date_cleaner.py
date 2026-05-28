"""
Date Cleaner Module

Cleans and normalizes transaction dates.
"""

from datetime import datetime
import pandas as pd


def clean_date(date_value, output_format='%Y-%m-%d'):
    """
    Clean and normalize date value to standard format.
    
    Operations:
    - Parse various date formats
    - Convert to standard format (YYYY-MM-DD)
    - Strip whitespace
    
    Args:
        date_value: Raw date value
        output_format: Desired output format (default: YYYY-MM-DD)
        
    Returns:
        str: Cleaned date in standard format
    """
    if date_value is None or date_value == '':
        return None
    
    try:
        # Handle pandas Timestamp
        if isinstance(date_value, pd.Timestamp):
            return date_value.strftime(output_format)
        
        # Handle datetime object
        if isinstance(date_value, datetime):
            return date_value.strftime(output_format)
        
        # Try to parse string dates
        date_str = str(date_value).strip()
        
        # Common date formats to try (matching actual CSV data)
        date_formats = [
            '%Y-%m-%d',      # 2023-04-25, 2024-12-12
            '%m/%d/%Y',      # 08/05/2022, 10/28/2022
            '%d-%m-%y',      # 31-12-23, 13-03-24, 25-07-24
            '%d-%m-%Y',      # 22-06-2023, 26-02-2022, 12-01-2024
            '%d/%m/%Y',      # 25/04/2023 (if any)
            '%Y/%m/%d',      # 2023/04/25 (if any)
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%Y/%m/%d %H:%M:%S'
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime(output_format)
            except ValueError:
                continue
        
        # If no format worked, return None
        return None
    
    except Exception:
        return None
