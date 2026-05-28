"""
Test script to verify category validation and cleaning with actual CSV variations
"""

import sys
sys.path.append('/Users/udayshankar/Documents/JOB/FinanceFlow')

from app.validations.category_validator import validate_category
from app.utils.category_cleaner import clean_category

# Test categories from actual CSV (including typos and variations)
test_categories = [
    # Food variations
    ('Fod', 'Food'),                    # Typo
    ('Foods', 'Food'),                  # Plural
    ('Foodd', 'Food'),                  # Typo
    ('food', 'Food'),                   # Lowercase
    ('FOOD', 'Food'),                   # Uppercase
    ('Food', 'Food'),                   # Correct
    
    # Education variations
    ('Educaton', 'Education'),          # Typo
    ('EDU', 'Education'),               # Abbreviation
    ('education', 'Education'),         # Lowercase
    ('Education', 'Education'),         # Correct
    
    # Utilities variations
    ('Utilties', 'Utilities'),          # Typo
    ('Utlities', 'Utilities'),          # Typo
    ('Utility', 'Utilities'),           # Singular
    ('utilities', 'Utilities'),         # Lowercase
    ('Utilities', 'Utilities'),         # Correct
    
    # Rent variations
    ('Rentt', 'Rent'),                  # Typo
    ('Rnt', 'Rent'),                    # Typo
    ('rent', 'Rent'),                   # Lowercase
    ('RENT', 'Rent'),                   # Uppercase
    ('Rent', 'Rent'),                   # Correct
    
    # Travel variations
    ('Travl', 'Travel'),                # Typo
    ('Traval', 'Travel'),               # Typo
    ('travel', 'Travel'),               # Lowercase
    ('TRAVEL', 'Travel'),               # Uppercase
    ('Travel', 'Travel'),               # Correct
    
    # Health variations
    ('Helth', 'Health'),                # Typo
    ('health', 'Health'),               # Lowercase
    ('HEALTH', 'Health'),               # Uppercase
    ('Health', 'Health'),               # Correct
    
    # Entertainment variations
    ('Entertain', 'Entertainment'),     # Abbreviation
    ('Entrtnmnt', 'Entertainment'),     # Abbreviation
    ('entertainment', 'Entertainment'), # Lowercase
    ('Entertainment', 'Entertainment'), # Correct
    
    # Savings variations
    ('Saving', 'Savings'),              # Singular
    ('savings', 'Savings'),             # Lowercase
    ('SAVINGS', 'Savings'),             # Uppercase
    ('Savings', 'Savings'),             # Correct
    
    # Other variations
    ('Others', 'Other'),                # Plural
    ('others', 'Other'),                # Lowercase plural
    ('OTHERS', 'Other'),                # Uppercase plural
    ('Misc', 'Other'),                  # Synonym
    ('Other', 'Other'),                 # Correct
    
    # Income variations
    ('Freelance', 'Income'),            # Type of income
    ('Bonus', 'Income'),                # Type of income
    ('Salary', 'Salary'),               # Separate category
    
    # Edge cases
    ('', None),                         # Empty
    (None, None),                       # None
]

print("Category Validation and Cleaning Test")
print("=" * 90)
print(f"{'Original':<20} {'Expected':<20} {'Cleaned':<20} {'Valid':<10} {'Status'}")
print("-" * 90)

success_count = 0
fail_count = 0

for original, expected in test_categories:
    # Clean the category
    cleaned = clean_category(original)
    
    # Validate the cleaned category
    is_valid, error = validate_category(cleaned)
    
    # Check if it matches expected
    if expected is None:
        status = "✅ PASS" if not is_valid else "❌ FAIL"
        success_count += 1 if status == "✅ PASS" else 0
        fail_count += 1 if status == "❌ FAIL" else 0
    else:
        status = "✅ PASS" if (cleaned == expected and is_valid) else "❌ FAIL"
        success_count += 1 if status == "✅ PASS" else 0
        fail_count += 1 if status == "❌ FAIL" else 0
    
    print(f"{str(original):<20} {str(expected):<20} {str(cleaned):<20} {str(is_valid):<10} {status}")

print("-" * 90)
print(f"Total: {len(test_categories)} | ✅ Pass: {success_count} | ❌ Fail: {fail_count}")
print()

# Test with random sample from CSV
print("\n" + "=" * 90)
print("Sample from actual CSV categories:")
print("=" * 90)

csv_samples = ['Educaton', 'rent', 'Freelance', 'Fod', 'entertainment', 
               'Utilties', 'Rentt', 'FOOD', 'Travl', 'Helth', 'EDU', 
               'Entertain', 'Misc', 'Others', 'Bonus']

for category in csv_samples:
    cleaned = clean_category(category)
    is_valid, error = validate_category(cleaned)
    status = "✅" if is_valid else "❌"
    print(f"{status} '{category}' → '{cleaned}' (Valid: {is_valid})")
