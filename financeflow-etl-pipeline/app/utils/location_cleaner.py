"""
Location Cleaner

Cleans and standardizes location values.
"""
import pandas as pd

def clean_location(location):
    """
    Clean and standardize location field.
    
    Cleaning Rules:
    1. If null/empty/NaN → "Unknown"
    2. If "N/A" or "NA" or "na" → "Unknown"
    3. Strip whitespace and convert to title case
    4. Standardize city codes:
       - BAN, BANG → Bangalore
       - AHM, AHMED → Ahmedabad
       - DEL → Delhi
       - KOL → Kolkata
       - LUC → Lucknow
       - CHE, CHEN → Chennai
    
    Args:
        location: Raw location value
        
    Returns:
        Cleaned location string
    """
    # Handle null/empty values
    if pd.isna(location) or location == '' or location is None:
        return "Unknown"
    
    # Convert to string and strip whitespace
    location_str = str(location).strip()
    
    # Check if empty after stripping
    if not location_str:
        return "Unknown"
    
    # Convert to lowercase for comparison
    location_lower = location_str.lower()
    
    # Handle N/A variations
    if location_lower in ['n/a', 'na', 'nan', 'none', 'null']:
        return "Unknown"
    
    # Standardize city codes
    city_code_mapping = {
        'ban': 'Bangalore',
        'bang': 'Bangalore',
        'bangalore': 'Bangalore',
        'ahm': 'Ahmedabad',
        'ahmed': 'Ahmedabad',
        'ahmedabad': 'Ahmedabad',
        'del': 'Delhi',
        'delhi': 'Delhi',
        'kol': 'Kolkata',
        'kolkata': 'Kolkata',
        'luc': 'Lucknow',
        'lucknow': 'Lucknow',
        'che': 'Chennai',
        'chen': 'Chennai',
        'chennai': 'Chennai',
        'pun': 'Pune',
        'pune': 'Pune',
        'hyd': 'Hyderabad',
        'hyderabad': 'Hyderabad',
        'mum': 'Mumbai',
        'mumbai': 'Mumbai'
    }
    
    # Check if location matches a city code
    if location_lower in city_code_mapping:
        return city_code_mapping[location_lower]
    
    # Otherwise, return title-cased location
    return location_str.title()
