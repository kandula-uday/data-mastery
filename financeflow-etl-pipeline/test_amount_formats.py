"""
Test script to verify amount validation and cleaning with actual CSV formats
"""

import sys
sys.path.append('/Users/udayshankar/Documents/JOB/FinanceFlow')

from app.validations.amount_validator import validate_amount
from app.utils.amount_cleaner import clean_amount

# Test amounts from actual CSV
test_amounts = [
    '3888',          # Plain number
    '649',           # Plain number
    'Rs.828',        # Rs. prefix
    '₹5070',         # Rupee symbol
    '999999999',     # Very large number
    '$4262',         # Dollar sign
    '5107 INR',      # INR suffix
    '₹2553',         # Rupee symbol
    '1380 INR',      # INR suffix
    '$7619',         # Dollar sign
    'Rs.5554',       # Rs. prefix
    '₹41573',        # Rupee symbol
    '7397 INR',      # INR suffix
    'Rs.864',        # Rs. prefix
    '₹999999',       # Large with rupee symbol
    'Rs.9705',       # Rs. prefix
    '',              # Empty
    None,            # None
    '0',             # Zero (should fail - not positive)
    '-500',          # Negative (should fail)
]

print("Amount Validation and Cleaning Test")
print("=" * 80)
print()

for amount in test_amounts:
    print(f"Original: {amount!r}")
    
    # Validate
    is_valid, error = validate_amount(amount)
    print(f"  Valid: {is_valid}")
    if not is_valid:
        print(f"  Error: {error}")
    
    # Clean
    if is_valid:
        cleaned = clean_amount(amount)
        print(f"  Cleaned: {cleaned}")
    
    print()
