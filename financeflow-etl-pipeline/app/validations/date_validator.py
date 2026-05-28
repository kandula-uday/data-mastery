"""
Date Validator Module

Validates transaction dates for correctness and validity.
"""

from datetime import datetime
import pandas as pd


def validate_date(date_value):
    """
    Validate transaction date.
    
    Checks:
    - Date is not null/empty
    - Date is in valid format
    - Date is not in future
    - Date is within reasonable range (not too old)
    
    Args:
        date_value: Transaction date value
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if date_value is None or date_value == '':
        return False, "Date is missing"
    
    # Try to parse the date
    try:
        # Handle pandas Timestamp
        if isinstance(date_value, pd.Timestamp):
            parsed_date = date_value.to_pydatetime()
        else:
            # Try common date formats
            date_str = str(date_value).strip()
            parsed_date = None
            
            date_formats = [
                '%Y-%m-%d',      # 2023-04-25, 2024-12-12
                '%m/%d/%Y',      # 08/05/2022, 10/28/2022
                '%d-%m-%y',      # 31-12-23, 13-03-24, 25-07-24
                '%d-%m-%Y',      # 22-06-2023, 26-02-2022, 12-01-2024
                '%d/%m/%Y',      # 25/04/2023 (if any)
                '%Y/%m/%d',      # 2023/04/25 (if any)
                '%Y-%m-%d %H:%M:%S',
                '%d-%m-%Y %H:%M:%S',
                '%m/%d/%Y %H:%M:%S'
            ]
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if parsed_date is None:
                return False, f"Invalid date format: {date_value}"
    
    except Exception as e:
        return False, f"Date parsing error: {str(e)}"
    
    # Check if date is in the future
    if parsed_date > datetime.now():
        return False, f"Date cannot be in the future: {parsed_date.strftime('%Y-%m-%d')}"
    
    # Check if date is too old (e.g., before year 2000)
    if parsed_date.year < 2000:
        return False, f"Date is too old: {parsed_date.strftime('%Y-%m-%d')}"
    
    return True, None
