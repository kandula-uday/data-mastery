"""
Test script to verify date validation and cleaning with actual CSV formats
"""

import sys
sys.path.append('/Users/udayshankar/Documents/JOB/FinanceFlow')

from app.validations.date_validator import validate_date
from app.utils.date_cleaner import clean_date

# Test dates from actual CSV
test_dates = [
    '2023-04-25',      # YYYY-MM-DD
    '08/05/2022',      # MM/DD/YYYY
    '31-12-23',        # DD-MM-YY
    '10/28/2022',      # MM/DD/YYYY
    '13-03-24',        # DD-MM-YY
    '22-06-2023',      # DD-MM-YYYY
    '26-02-2022',      # DD-MM-YYYY
    '12-01-2024',      # DD-MM-YYYY
    '25-07-24',        # DD-MM-YY
    '',                # Empty
    None,              # None
]

print("Date Validation and Cleaning Test")
print("=" * 80)
print()

for date in test_dates:
    print(f"Original: {date!r}")
    
    # Validate
    is_valid, error = validate_date(date)
    print(f"  Valid: {is_valid}")
    if not is_valid:
        print(f"  Error: {error}")
    
    # Clean
    if is_valid:
        cleaned = clean_date(date)
        print(f"  Cleaned: {cleaned}")
    
    print()
