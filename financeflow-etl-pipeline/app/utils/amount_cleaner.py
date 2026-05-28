"""
Amount Cleaner Module

Cleans and normalizes transaction amounts.
"""

import re


def clean_amount(amount):
    """
    Clean and normalize amount value.
    
    Operations:
    - Remove currency symbols (Rs., ₹, $, etc.)
    - Remove currency text (INR)
    - Remove commas and spaces
    - Strip whitespace
    - Convert to float
    - Round to 2 decimal places
    
    Handles formats from CSV:
    - Plain numbers: 3888, 649, 13239
    - With Rs. prefix: Rs.828, Rs.5554
    - With ₹ symbol: ₹5070, ₹2553
    - With $ symbol: $4262, $7619
    - With INR suffix: 5107 INR, 1380 INR
    - Large numbers: 999999999, 999999
    
    Args:
        amount: Raw amount value
        
    Returns:
        float: Cleaned amount value (rounded to 2 decimals)
    """
    if amount is None or amount == '':
        return None
    
    # Convert to string for processing
    amount_str = str(amount).strip()
    
    if not amount_str:
        return None
    
    # Remove "Rs." or "Rs" prefix (case insensitive)
    amount_str = re.sub(r'Rs\.?', '', amount_str, flags=re.IGNORECASE)
    
    # Remove currency symbols (₹, $, €, £, ¥, etc.)
    amount_str = re.sub(r'[€£¥₹$]', '', amount_str)
    
    # Remove "INR" text (case insensitive)
    amount_str = re.sub(r'INR', '', amount_str, flags=re.IGNORECASE)
    
    # Remove commas (e.g., 1,000.00 -> 1000.00)
    amount_str = amount_str.replace(',', '')
    
    # Remove spaces
    amount_str = amount_str.strip()
    
    # Remove any other non-numeric characters except decimal point and minus sign
    amount_str = re.sub(r'[^\d.-]', '', amount_str)
    
    if not amount_str:
        return None
    
    try:
        # Convert to float and round to 2 decimal places
        cleaned_amount = round(float(amount_str), 2)
        return cleaned_amount
    except (ValueError, TypeError):
        return None
