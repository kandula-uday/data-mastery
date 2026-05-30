"""
Notes Cleaner

Cleans and standardizes notes values.
"""
import pandas as pd
import re

def clean_notes(notes):
    """
    Clean and standardize notes field.
    
    Cleaning Rules:
    1. If null/empty/NaN → "NaN" (string)
    2. If contains only special characters (e.g., "...", "!!!", "???") → "NaN"
    3. If "N/A", "NA", "na", "test", "xyz123", "asdfgh" → "NaN"
    4. Strip whitespace
    5. Remove excessive special characters (more than 3 repeated)
    6. If empty after cleaning → "NaN"
    
    Args:
        notes: Raw notes value
        
    Returns:
        Cleaned notes string or "NaN"
    """
    # Handle null/empty values
    if pd.isna(notes) or notes == '' or notes is None:
        return "NaN"
    
    # Convert to string and strip whitespace
    notes_str = str(notes).strip()
    
    # Check if empty after stripping
    if not notes_str:
        return "NaN"
    
    # Convert to lowercase for comparison
    notes_lower = notes_str.lower()
    
    # Handle placeholder/invalid values
    invalid_values = [
        'n/a', 'na', 'nan', 'none', 'null',
        'test', 'testing', 'xyz', 'abc',
        'asdfgh', 'qwerty', 'xyz123', 'abc123',
        'misc', 'miscellaneous'
    ]
    
    if notes_lower in invalid_values:
        return "NaN"
    
    # Check if notes contains only special characters
    # Remove all alphanumeric characters and see what's left
    alphanumeric_only = re.sub(r'[^a-zA-Z0-9]', '', notes_str)
    
    if not alphanumeric_only:
        # Only special characters remain
        return "NaN"
    
    # Remove excessive repeated special characters (more than 3 in a row)
    # e.g., "!!!!!!" → "!!!", "......" → "..."
    cleaned = re.sub(r'([!.?,-])\1{3,}', r'\1\1\1', notes_str)
    
    # Remove leading/trailing special characters
    cleaned = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', cleaned)
    
    # Final check if empty after cleaning
    if not cleaned or len(cleaned) < 2:
        return "NaN"
    
    return cleaned.strip()
