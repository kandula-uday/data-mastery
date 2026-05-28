"""
Amount Validator Module

Validates transaction amounts for correctness and validity.
"""

import re


def validate_amount(amount):
    """
    Validate transaction amount.
    
    Checks:
    - Amount is not null/empty
    - Amount is numeric (after cleaning currency symbols)
    - Amount is positive
    - Amount is within reasonable range
    
    Handles formats from CSV:
    - Plain numbers: 3888, 649, 13239
    - With Rs. prefix: Rs.828, Rs.5554
    - With ₹ symbol: ₹5070, ₹2553
    - With $ symbol: $4262, $7619
    - With INR suffix: 5107 INR, 1380 INR
    - Large numbers: 999999999, 999999
    
    Args:
        amount: Transaction amount value
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if amount is None or amount == '':
        return False, "Amount is missing"
    
    # Convert to string for processing
    amount_str = str(amount).strip()
    
    if not amount_str:
        return False, "Amount is empty"
    
    try:
        # Clean amount: remove currency symbols and text
        # Remove: Rs., ₹, $, commas, spaces, INR
        cleaned_amount = amount_str
        
        # Remove "Rs." or "Rs" prefix (case insensitive)
        cleaned_amount = re.sub(r'Rs\.?', '', cleaned_amount, flags=re.IGNORECASE)
        
        # Remove currency symbols
        cleaned_amount = re.sub(r'[₹$€£¥,\s]', '', cleaned_amount)
        
        # Remove "INR" text (case insensitive)
        cleaned_amount = re.sub(r'INR', '', cleaned_amount, flags=re.IGNORECASE)
        
        # Final cleanup
        cleaned_amount = cleaned_amount.strip()
        
        if not cleaned_amount:
            return False, f"Amount contains no numeric value: {amount}"
        
        # Convert to float
        amount_float = float(cleaned_amount)
        
    except (ValueError, TypeError) as e:
        return False, f"Amount is not numeric: {amount}"
    
    # Check if amount is positive
    if amount_float <= 0:
        return False, f"Amount must be positive: {amount_float}"
    
    # Check for unreasonably large amounts (e.g., > 100 million)
    # Note: Updated limit since CSV has values like 999999999
    if amount_float > 100000000:
        return False, f"Amount exceeds maximum limit (100M): {amount_float}"
    
    return True, None
