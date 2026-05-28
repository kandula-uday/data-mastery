"""
Category Validator Module

Validates transaction categories against allowed values.
"""

# Define allowed categories (standardized names after cleaning)
VALID_CATEGORIES = {
    'Food',
    'Groceries',
    'Shopping',
    'Transportation',
    'Entertainment',
    'Utilities',
    'Health',
    'Travel',
    'Education',
    'Personal Care',
    'Income',
    'Salary',
    'Investment',
    'Other',
    'Rent',
    'Insurance',
    'Savings',
    'Transfer'
}


def validate_category(category):
    """
    Validate transaction category.
    
    Checks:
    - Category is not null/empty
    - Category is in allowed list
    
    Args:
        category: Transaction category value
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if category is None or category == '':
        return False, "Category is missing"
    
    category_str = str(category).strip()
    
    if not category_str:
        return False, "Category is empty"
    
    # Case-insensitive check against valid categories
    category_normalized = category_str.title()
    
    # Check if category exists in valid list (case-insensitive)
    if not any(cat.lower() == category_str.lower() for cat in VALID_CATEGORIES):
        return False, f"Invalid category: {category_str}"
    
    return True, None


def get_valid_categories():
    """
    Get list of valid categories.
    
    Returns:
        set: Valid category names
    """
    return VALID_CATEGORIES
