"""
Payment Mode Cleaner

Cleans and standardizes payment_mode values.
"""
import pandas as pd

def clean_payment_mode(payment_mode):
    """
    Clean and standardize payment_mode field.
    
    Cleaning Rules:
    1. If null/empty/NaN → "unknown"
    2. Convert to lowercase and strip whitespace
    3. Standardize variations:
       - cash, csh, Cash, CSH → cash
       - card, crd, Card, CRD, CARD → card
       - upi, UPI, Upi → upi
       - bank_transfer, Bank Transfer, bank transfer, BANK TRANSFER → bank_transfer
    4. Remove underscores and spaces for matching, then apply standard format
    
    Args:
        payment_mode: Raw payment_mode value
        
    Returns:
        Cleaned payment_mode string
    """
    # Handle null/empty values
    if pd.isna(payment_mode) or payment_mode == '' or payment_mode is None:
        return "unknown"
    
    # Convert to string, lowercase, and strip whitespace
    mode_str = str(payment_mode).strip().lower()
    
    # Check if empty after stripping
    if not mode_str:
        return "unknown"
    
    # Remove extra spaces and underscores for comparison
    mode_normalized = mode_str.replace('_', '').replace(' ', '')
    
    # Standardize payment mode variations
    if mode_normalized in ['cash', 'csh', 'ca']:
        return 'cash'
    
    elif mode_normalized in ['card', 'crd', 'debitcard', 'creditcard', 'cd']:
        return 'card'
    
    elif mode_normalized in ['upi', 'u']:
        return 'upi'
    
    elif mode_normalized in ['banktransfer', 'bank', 'transfer', 'neft', 'imps', 'rtgs']:
        return 'bank_transfer'
    
    elif mode_normalized in ['na', 'n/a', 'nan', 'none', 'null']:
        return 'unknown'
    
    # If not recognized, return unknown
    else:
        return 'unknown'
