"""
Location Validator

Validates location field for transaction records.
"""

def validate_location(location):
    """
    Validate location field.
    
    Rules:
    - Can be empty/null (will be handled by cleaner)
    - If present, should be non-empty string after stripping
    - Any location value is acceptable after cleaning
    
    Args:
        location: Location value to validate
        
    Returns:
        Tuple (is_valid: bool, error_message: str or None)
    """
    # Location is optional, so null/empty is valid
    # The cleaner will handle setting it to "Unknown"
    
    # No specific validation rules needed as location can be any string
    # and will be standardized by the cleaner
    
    return True, None
