"""
Category Cleaner Module

Cleans and normalizes transaction categories.
Handles typos, abbreviations, and variations from the CSV data.
"""


# Category mapping for common variations, typos, and abbreviations
CATEGORY_MAPPING = {
    # Food variations and typos
    'food': 'Food',
    'foods': 'Food',
    'fod': 'Food',                    # Typo from CSV
    'foodd': 'Food',                  # Typo from CSV
    'dining': 'Food',
    'restaurant': 'Food',
    
    # Groceries
    'groceries': 'Groceries',
    'grocery': 'Groceries',
    
    # Shopping
    'shop': 'Shopping',
    'shopping': 'Shopping',
    
    # Transportation
    'transport': 'Transportation',
    'transportation': 'Transportation',
    'commute': 'Transportation',
    
    # Entertainment variations and typos
    'entertainment': 'Entertainment',
    'entertain': 'Entertainment',     # Abbreviation from CSV
    'entrtnmnt': 'Entertainment',     # Abbreviation from CSV
    'fun': 'Entertainment',
    
    # Utilities variations and typos
    'bills': 'Utilities',
    'utilities': 'Utilities',
    'utility': 'Utilities',
    'utilties': 'Utilities',          # Typo from CSV
    'utlities': 'Utilities',          # Typo from CSV
    
    # Healthcare/Health variations and typos
    'healthcare': 'Health',
    'health': 'Health',
    'helth': 'Health',                # Typo from CSV
    'medical': 'Health',
    
    # Travel variations and typos
    'travel': 'Travel',
    'travl': 'Travel',                # Typo from CSV
    'traval': 'Travel',               # Typo from CSV
    'trip': 'Travel',
    
    # Education variations and typos
    'education': 'Education',
    'educaton': 'Education',          # Typo from CSV
    'edu': 'Education',               # Abbreviation from CSV
    'study': 'Education',
    
    # Personal Care
    'personal care': 'Personal Care',
    'personalcare': 'Personal Care',
    
    # Income variations
    'income': 'Income',
    'freelance': 'Income',            # From CSV
    'bonus': 'Income',                # From CSV
    
    # Salary
    'salary': 'Salary',
    'wage': 'Salary',
    
    # Investment
    'investment': 'Investment',
    'invest': 'Investment',
    
    # Other variations and typos
    'other': 'Other',
    'others': 'Other',                # From CSV
    'misc': 'Other',                  # From CSV
    
    # Rent variations and typos
    'rent': 'Rent',
    'rentt': 'Rent',                  # Typo from CSV
    'rnt': 'Rent',                    # Typo from CSV
    
    # Insurance
    'insurance': 'Insurance',
    
    # Savings variations
    'savings': 'Savings',
    'saving': 'Savings',
    
    # Transfer
    'transfer': 'Transfer'
}


def clean_category(category):
    """
    Clean and normalize category value.
    
    Operations:
    - Strip whitespace
    - Convert to title case
    - Map to standard category names
    - Handle common variations
    
    Args:
        category: Raw category value
        
    Returns:
        str: Cleaned category value
    """
    if category is None or category == '':
        return None
    
    # Convert to string and clean
    category_str = str(category).strip()
    
    # Convert to lowercase for mapping
    category_lower = category_str.lower()
    
    # Check if it exists in mapping
    if category_lower in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[category_lower]
    
    # If not in mapping, return title case version
    return category_str.title()
