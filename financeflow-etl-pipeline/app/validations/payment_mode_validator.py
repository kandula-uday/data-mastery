"""
Payment Mode Validator

Validates payment_mode field for transaction records.
"""

# Define valid payment modes after standardization
VALID_PAYMENT_MODES = [
    'cash',
    'card',
    'upi',
    'bank_transfer',
    'unknown'
]

def validate_payment_mode(payment_mode):
    """
    Validate payment_mode field.
    
    Rules:
    - Can be empty/null (will be cleaned to "unknown")
    - After cleaning/standardization, must be one of the valid payment modes
    - Validation happens after cleaning
    
    Valid payment modes (after cleaning):
    - cash
    - card
    - upi
    - bank_transfer
    - unknown
    
    Args:
        payment_mode: Payment mode value to validate (after cleaning)
        
    Returns:
        Tuple (is_valid: bool, error_message: str or None)
    """
    if payment_mode is None or str(payment_mode).strip() == '':
        # Empty is valid, will be cleaned to "unknown"
        return True, None
    
    # Check if the cleaned payment mode is in valid list
    if payment_mode.lower() in VALID_PAYMENT_MODES:
        return True, None
    
    return False, f"Invalid payment mode: {payment_mode}. Must be one of {VALID_PAYMENT_MODES}"
