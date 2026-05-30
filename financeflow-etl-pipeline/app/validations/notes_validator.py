"""
Notes Validator

Validates notes field for transaction records.
"""
import re

def validate_notes(notes):
    """
    Validate notes field.
    
    Rules:
    - Can be empty/null (will be handled by cleaner)
    - Should not contain excessive special characters only (e.g., "...", "!!!")
    - Special character-only patterns will be cleaned to null by cleaner
    
    Args:
        notes: Notes value to validate
        
    Returns:
        Tuple (is_valid: bool, error_message: str or None)
    """
    # Notes is optional, so null/empty is valid
    # The cleaner will handle special characters and set appropriate values
    
    # No strict validation needed - cleaner will normalize the values
    return True, None
